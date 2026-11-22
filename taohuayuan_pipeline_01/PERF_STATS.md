# 性能统计报告（pipeline_01 田园展示场景）· 验收修订版 v2

依据 PERF_SPEC_V1 · Godot 4.7.2 gl_compatibility · 1280×720 桌面窗口（vsync 开）
统计源：`evidence/perf_log.csv`（4 组 × 60 样本）、`evidence/asset_budget.json`（场景结构清点）、`evidence/godot_audit.json`（逐模型骨架动画）。

## 一、关键限制声明（如实）
Godot 4.7.2 的 **gl_compatibility 渲染器不提供运行时 DrawCalls / Primitives / Objects 计数器**：
`Performance.RENDER_TOTAL_*`、`RenderingServer.get_rendering_info(*)`、`Viewport.get_render_info(*)` 三套接口在本渲染器下全部返回 0（已实测，`perf_log.csv` 三列全为 0）。
因此口径：**帧时间/FPS/显存 = 桌面实测；三角面/DrawCalls/骨骼 = 离线结构清点；Android 真机 = 缺件未测**。不用桌面数据宣布手机合格。

## 二、桌面实测（PERF_SPEC §0 协议）
| 组 | FPS 中位 | 帧时间中位 | P95 | VRAM |
|---|---:|---:|---:|---:|
| baseline_shadow_on_anim_on | 170 | 5.88 ms | 5.88 ms | 24.5 MB |
| shadow_off | 170 | 5.88 ms | 5.88 ms | 24.5 MB |
| anim_paused | 170 | 5.88 ms | 5.88 ms | 24.5 MB |
| veg_hidden | 170 | 5.88 ms | 5.88 ms | 24.5 MB |

- 三项开关差值均为 0：桌面被 170 FPS 上限（vsync/计时分辨率）钳住，阴影/动画/植被开销无法用差值法量化；**必须以 Android 真机判定**。
- 旧稿「145~170 FPS / 6.9ms」为采样区间误记，CSV 实际四组中位均为 170 FPS / 5.88 ms，已更正。

## 三、离线结构清点（与 IMPORT_LIST / asset_budget 一致）
| 指标 | 修订值 | 旧稿值 | 红线 | 判定 |
|---|---:|---:|---:|---|
| 50 件唯一网格三角面 | 40,805 | 40,805 | — | 对齐 Blender normalize_report |
| 场景静态三角面（按 224 实例累计） | **119,294** | 33,232（错误口径） | ≤150,000 | ✅ 合格 |
| 帧提交 Primitives 估算（无剔除保守值） | ≈119,294 | ≈44,379（错误口径） | ≤150,000 | ✅ 合格 |
| DrawCalls 估算（全场景节点/surface 清点，无剔除） | **123** | 97（口径不全） | ≤100 | ❌ **超线 23** |
| Skeleton3D | 8 | 1（仅黄牛，错误） | — | 已更正 |
| 骨骼数 | 199 | 未统计 | ≤400 | ✅ 合格 |
| AnimationPlayer / AnimationLibrary / 动画 | 8 / 8 / 55 | 未统计 | — | 已更正 |
| 非骨骼动画 | 0 | 未统计 | — | 全部为骨骼动画 |
| MultiMesh 批次 | 4（草90/野花22/蕨18/围栏18） | 4 | 散摆>300 禁止 | ✅ 合格 |

**DrawCalls 超线说明**：123 是无视锥剔除、按场景全部 MeshInstance3D 与多 surface 逐节点清点的保守值；实际帧提交值本渲染器不可读，不能声称已达标。47 种入场景模型里，重复摆放的树/石/灯笼与 Poly Pizza 多 surface 动物是主要来源。正式工程接入前必须按类别合并/MultiMesh 化或压缩重复实例；本场景已示范围栏+植被的合批模式。以上不改动 ArtLab 场景，留待正式接入时处理。

## 四、性能测试中实际启用的动画
`_play_anims()` 遍历全部 8 个 AnimationPlayer，各取第 1 条动画播放并设 `LOOP_LINEAR`：
熊/鹿/兔/狐 = `Idle`（各 1 实例/2 实例/3 实例/1 实例）；黄牛 = `AnimalArmature|Attack_Headbutt`；绵羊 = `Armature|Idle`；绵羊变体 = `...|Death`；猪 = `...|Death`。anim_paused 组统一 `active=false`。
所有 55 条动画通道经 GLB 元数据核对，target node 全部落在 skin joints 内 → 非骨骼动画 0 条。

## 五、Android 真机验证（缺件：本机无 adb / 无 Android SDK / 无连接设备）
状态：**未实测**。按 PERF_SPEC §2.1 的最小步骤补测（用户手机 + USB）：
1. Godot 编辑器 → 管理导出模板（下载 4.7.2 模板）
2. 编辑器设置 → 导出 → Android → 一键安装 OpenJDK + SDK
3. 项目 → 安装 Android 构建模板 → 导出预设 Android → Export Debug
4. 手机开 USB 调试 → 一键部署或 `adb install -t`
5. 本工程内置采集 HUD（`-- --perf` 写 `user://perf_log.csv`），真机跑同样命令后 `adb pull` 取回
6. 测试纪律：拔充电线、亮度 50%、每机位 ≥60 秒、同一手机 ≤20 分钟

判定红线（真机数据填入后套用 PERF_SPEC §3）：帧时间 ≤20ms / Primitives ≤150k / DC ≤100 / 阴影 Δ≤4ms / 动画 Δ≤3ms / 植被 Δ≤5ms。

## 六、结论行
`平台=Windows 桌面(仅结构参考) | 机位=全景 | 结论=面数/骨骼/合批合格，全场景 DC 估算 123 超线（无剔除保守值） | 超标项=DrawCalls | Android=未实测，缺件 | 依据=实测帧时间+离线结构清点`
