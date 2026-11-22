# 素材场景性能统计规格 v1

> 适用：《桃花源物语》素材组装场景（Godot 4.7.2 / gl_compatibility，目标 Android + Windows）
> 范围：50 件外部素材（Polyfork 顶点色低模 + Poly Pizza 骨骼动画）组装进田园展示场景后的性能采集与判定。
> 原则：**Android 真机数据优先**，桌面 FPS 只作参考，不作为"手机性能合格"的依据。

---

## 0. 总采样协议（适用于所有指标）

| 项 | 规定 |
|---|---|
| 采样起点 | 场景装载完成后静置 5 秒（排除加载期毛刺） |
| 采样频率 | 每 1 秒采样一次（`Time.get_ticks_msec()` 驱动，不用 `_process` 计数） |
| 样本数 | 静止机位：连续 60 次（60 秒）；巡游路径：全程等间隔采样，每段路径单独成组 |
| 统计量 | **中位数**（主判据）+ P95 + 最大值 + 最小值，四项全部记录 |
| 场景状态 | 每个机位/路径至少采两组：阴影全开、阴影全关（差值 = 阴影开销） |
| 排除条件 | 采样期间禁止调试断点、禁止窗口失焦；Android 端禁止充电中测试（发热会降频） |

推荐做法：在采集场景中放一个 Autoload 调试 HUD（F3 开关），把 `Performance.get_monitor()` 的值写到 `user://perf_log.csv`，桌面端用编辑器跑，Android 端 debug APK 用 `adb pull` 取回 CSV。**不要依赖肉眼读屏**。

---

## 1. 指标采集方法（Godot 4.7.2 实名接口）

### 1.1 场景总三角面数（静态资产清点 + 帧实际提交数，两个都要）

**A. 资产清点（编辑器内一次性离线统计，导入前验收用）**

对每个导入的 `.glb/.gltf/.obj` Mesh：

```gdscript
var tri := 0
for s in mesh.get_surface_count():
    var arr: PackedVector3Array = mesh.surface_get_arrays(s)[Mesh.ARRAY_VERTEX]
    tri += arr.size() / 3   # 索引化网格下 vertex 数即顶点数，面数按 3 顶点一面估
```

- 更精确：对 ArrayMesh 用 `MeshDataTool` 逐面数（`mdt.get_face_count()`）。
- **同步记录每件素材的 `get_surface_count()`**：surface 数直接决定未来能否合批，surface > 4 的素材要标记。
- 汇总产出《50 件素材面数清单》，作为组装场景前预算核算依据。

**B. 帧实际提交数（运行时，真机采这个）**

```gdscript
Performance.get_monitor(Performance.RENDER_PRIMITIVES_IN_FRAME)  # 上帧实际渲染的图元(≈三角面)数
RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_PRIMITIVES_IN_FRAME)  # 等价接口，二选一
```

- 每 1s 读一次，按总采样协议记录。
- 静态清点数 ≠ 帧提交数（视锥剔除、LOD 会缩），**判定以帧提交数为准**。

### 1.2 实际 Draw Calls

```gdscript
Performance.get_monitor(Performance.RENDER_DRAW_CALLS_IN_FRAME)
RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME)
```

- 同样按总采样协议记录中位数 + P95。
- **配套必采**：`Performance.RENDER_OBJECTS_IN_FRAME`（渲染实例数）。实例数正常、DrawCalls 超标 → 说明问题在材质/surface 碎片化，先合批而不是删内容。

### 1.3 同屏实例数

```gdscript
Performance.get_monitor(Performance.RENDER_OBJECTS_IN_FRAME)
```

- 辅助参考：用 `get_tree().get_nodes_in_group("vegetation").size()` 之类的业务分组计数，对照"场景摆放了多少"和"实际进渲染管线多少"，差值即剔除效率。
- 植被若用 MultiMesh，`RENDER_OBJECTS_IN_FRAME` 会显示为极少的实例数（一个 MultiMesh = 1 个实例）——这是正常且正确的，此时**同屏实例判定改看三角面数与 DrawCalls**，另外离线统计每个 MultiMesh 的 `instance_count` 记入清单。

### 1.4 阴影开销

Godot 无"阴影专用 monitor"，用**开关对比法**（差值即开销），gl_compatibility 下阴影是逐光源重绘场景，开销最敏感：

1. 记录阴影全开的 60 秒样本组（三角面数 / DrawCalls / 平均帧时间）。
2. 关闭全部阴影（`DirectionalLight3D.shadow_enabled = false`，所有 `OmniLight3D/SpotLight3D.shadow_enabled = false`），再采 60 秒。
3. 差值三项分别记录：Δ三角面、ΔDrawCalls、Δ帧时间(ms)。
4. 同时记录配置面数：`rendering/lights_and_shadows/directional_shadow/size`（Compatibility 下移动端默认 2048）、positional shadow filter quality——**配置值与实测差值一起进表**，后续调优才可比。
5. 补充：`RenderingServer.get_frame_setup_time_cpu()`（CPU 侧提交开销，异常升高常见于实例/光源过多）。

### 1.5 植被开销

植被单独编组（group: `vegetation`），逐项采集：

| 项 | 方法 |
|---|---|
| 摆放实例数 | 离线统计：逐个 MultiMesh 记 `instance_count()`；散摆 Mesh 记节点数 |
| 实际批次 | 运行时 `RENDER_DRAW_CALLS_IN_FRAME`，并与"植被全部隐藏"再采一组对比，ΔDrawCalls = 植净批次 |
| 植净三角面 | 同上对比组的 ΔPrimitives |
| 植净帧时间 | 同上对比组的 Δ帧时间(ms)，这是**发热与低端机的主指标** |

- 摆放方式硬性要求：同类植被必须走 MultiMesh（gl_compatibility 下 MultiMesh 仍是 1 个 DrawCall 批次，无 GPU instancing 自动拆散的问题；若散摆成百个 MeshInstance3D，DrawCalls 必然崩）。

### 1.6 动物骨骼动画开销

骨骼无独立 monitor，同样用**开关对比法** + 配置清点：

1. 离线清点：每只动物记录 `Skeleton3D.get_bone_count()`、AnimationPlayer 的动画数与时长、是否循环常驻播放。
2. 运行时对比：所有动画暂停（每个 AnimationPlayer `.active = false` 或 `speed_scale = 0`）采 60 秒 vs 全部播放采 60 秒，Δ记录：
   - Δ帧时间 ms（主指标）
   - `Performance.TIME_PROCESS`（脚本/动画逻辑 CPU 时间，ms/帧）
   - ΔRENDER_PRIMITIVES_IN_FRAME（蒙皮后提交面数，确认蒙皮没有把面数撑异常）
3. gl_compatibility 下蒙皮在 GPU 侧做，移动端瓶颈通常仍在面数与填充率；若 Δ帧时间偏高而 Δ面数不变，嫌疑在动画计算 CPU 开销（动画混合数过多），处置是裁剪同时播放的动画数而非减骨。
4. 可见性要求：动物必须挂 `VisibleOnScreenNotifier3D` + 远距离动画降级（超出距离停播），这条写进组装规范。

---

## 2. Android 真机验证方案（Windows 机无 Android 设备）

### 2.1 交给用户自己执行的最小步骤（导出 debug APK + 真机查看）

前提：Windows 已装 Godot 4.7.2。

1. **装导出模板**：编辑器 → 编辑器设置 → 导出 → 下载 4.7.2 官方导出模板（版本必须与编辑器一致，不一致会告警）。
2. **装 Java/Android SDK**：编辑器设置 → 导出 → Android，用 Godot 内置的一键安装（`Install Android Build Template`，4.x 已内置自动装 OpenJDK 与 Android SDK 的流程），装完在"Android SDK 路径"处校验通过。
3. **装 Android 构建模板**：项目 → `Install Android Build Template`（给项目加 gradle 构建）。
4. **导出预设**：项目 → 导出 → 添加 → Android → 选 debug keystore（Godot 会自动生成默认 debug keystore，无需手动建）→ 勾选 **Export Debug**（APK，不需要 keystore 签名配置）。
5. **手机侧**：开发者选项 → 打开"USB 调试" → USB 连电脑，手机弹窗允许调试。
6. **两种安装方式任选**：
   - Godot 编辑器右上角"一键部署"（遥控器图标，需 `adb` 在 PATH 或 Godot 已配置 SDK 路径，直接推到手机并启动，stdout 会回传到编辑器调试器）；
   - 或导出 APK 后手动安装：`adb install -t export_debug.apk`，`-t` 允许 debug 包。
7. **真机看数据**：本项目用**自带 HUD 脚本**（见 1.0 的 Autoload 方案）在屏幕上实时显示 FPS / DrawCalls / Primitives / VideoMem，同时写 `user://perf_log.csv`；测完 `adb pull /sdcard/Android/data/polyfork_eval/files/perf_log.csv .` 取回。
8. **测试纪律**：拔掉充电线、亮度固定 50%、屏幕常亮设置开启、每个机位至少 60 秒、同一手机连测不超过 20 分钟（防降频干扰）、记录手机型号 + Android 版本。

### 2.2 替代方案（无导出模板 / 无可连接设备时）

| 方案 | 做法 | 有效度 | 结论可用性 |
|---|---|---|---|
| Web 代理测 | 导出 HTML5（WebGL2，与 gl_compatibility 同管线族），手机浏览器开链接 | DrawCalls/面数趋势可参考 | **只可作方向性参考，不可替代真机**：无降频/发热/驱动差异，结论须降级表述 |
| 借用设备 | 上述 2.1 步骤在任意一台 Android 手机上执行即可，无需开发专用机 | 高 | 任何 2020 年后的中端机都可用作判定基准 |
| 桌面 GLES3 最低端化 | Windows 上强制窗口 720p + 关 VSync + 开 HUD 采数据 | 低 | **禁止**用桌面数据宣布"手机性能合格"，只允许用于提前暴露结构性问题（如 DrawCalls 结构性超标） |

用户既无设备也无意愿装 SDK 时，本规格要求：Android 端结论一律标注"**未实测，推算依据 = Web 代理测 + 桌面结构数据**"，不得写成"手机端已验证"。

---

## 3. 判定阈值（gl_compatibility / Android）

数值均为"中位数过线、P95 不得超 1.25 倍"的双门限。

| 指标 | 绿线（合格） | 红线（必须整改） | 整改方向 |
|---|---|---|---|
| 平均帧时间 | ≤ 20 ms（≥50 FPS） | > 33 ms（<30 FPS） | 先查 DrawCalls 与植被，再查面数 |
| 帧实际三角面 | ≤ 150,000 | > 250,000 | LOD / 视距裁剪 / MultiMesh 合批 |
| DrawCalls | ≤ 100 | > 150 | 合并材质与 surface、MultiMesh、删碎面资产 |
| 同屏渲染实例 | 无硬上限（MultiMesh 形态下） | 散摆 MeshInstance > 300 | 改 MultiMesh |
| 视频内存 | ≤ 300 MB | > 500 MB | 纹理压缩（已开 ETC2/ASTC）、贴图降档 |
| 阴影 Δ帧时间 | ≤ 4 ms | > 8 ms | 降 directional_shadow/size 至 1024、砍 shadow-casting 光源至 1 盏 |
| 植被 ΔDrawCalls | ≤ 20 | > 40 | 全量 MultiMesh 化 |
| 植被 Δ帧时间 | ≤ 5 ms | > 10 ms | 减 instance 数 / 降 LOD / 缩视距 |
| 动物 Δ帧时间 | ≤ 3 ms | > 6 ms | 减同屏动物数、远距停播 |
| 骨骼总量（同屏动物骨数和） | ≤ 400 | > 800 | 精简骨骼 / 减只数 |

平台备注：gl_compatibility 在移动端无 SSAO/SDFGI/体素化这类高端特性，**瓶颈排序通常是：填充率（分辨率）> DrawCalls > 三角面**。红线上再多边面，只要 DrawCalls 被压住，通常还能救；DrawCalls 超标则必须先动结构。

---

## 4. 数据记录表模板

### 4.1 素材清点表（组装前，编辑器离线统计）

| # | 素材名 | 来源 | 三角面 | Surface 数 | 有无骨骼 | 骨数 | 动画数 | 备注 |
|---|---|---|---|---|---|---|---|---|
| 1 | | Polyfork | | | | | | |
| … | | | | | | | | |

### 4.2 真机/桌面采样表（每个设备 × 每个机位一行）

| 日期 | 设备/平台 | 分辨率 | 机位/路径 | 阴影 | 动画状态 | FPS中位 | 帧时间ms中位 | Primitives中位 | Primitives P95 | DrawCalls中位 | DrawCalls P95 | Objects中位 | VideoMem MB | 备注(温度/降频) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | 开/关 | 播/停 | | | | | | | | | |

### 4.3 对比差值表（阴影 / 植被 / 动画开销）

| 开关项 | Δ帧时间ms | ΔPrimitives | ΔDrawCalls | 对应红线 | 判定 |
|---|---|---|---|---|---|
| 阴影 全开→全关 | | | | ≤4ms | 合格/超标 |
| 植被 全显→全隐 | | | | ≤5ms | 合格/超标 |
| 动画 全播→全停 | | | | ≤3ms | 合格/超标 |

### 4.4 结论行（每组测试末尾必填）

`平台=___ | 机位=___ | 结论=合格/超标 | 超标项=___ | 处置=___（引用 §3 整改方向）| 依据=真机实测/推算`

---

*版本：v1。阈值以本表为准；Godot 版本升级或改用 Forward+ 后需重估（本表仅覆盖 gl_compatibility）。*
