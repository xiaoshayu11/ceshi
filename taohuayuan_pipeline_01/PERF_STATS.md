# 性能统计报告（pipeline_01 田园展示场景）
依据 PERF_SPEC_V1 · Godot 4.7.2 gl_compatibility · 1280×720 桌面窗口（vsync 开）

## 一、关键限制声明（如实）
Godot 4.7.2 的 **gl_compatibility 渲染器不提供运行时 DrawCalls / Primitives / Objects 计数器**：
`Performance.RENDER_TOTAL_*`、`RenderingServer.get_rendering_info(*)`、`Viewport.get_render_info(*)` 三套接口在本渲染器下全部返回 0（已实测，见 perf_log.csv）。
因此本报告按 PERF_SPEC §2.2 降级口径：**帧时间/FPS/显存 = 桌面实测；DrawCalls/Primitives = 离线结构估算；Android 真机 = 缺件未测**。
不用桌面数据宣布"手机性能合格"。

## 二、桌面实测（4 组 × 60 样本 × 1s，PERF_SPEC §0 协议）
| 组 | FPS 中位 | 帧时间中位 | P95 | VRAM |
|---|---|---|---|---|
| baseline（阴影+动画+植被） | 145~170 | 5.9~6.9 ms | 6.94 ms | 24.5 MB |
| shadow_off / anim_paused / veg_hidden | 与基线差 ≈0 ms | 同上 | 同上 | 24.5 MB |

- 三项开关差值 ≈0：阴影/骨骼动画/植被开销在桌面端低于计时分辨率（≥144 FPS 上限附近），无法用桌面差值法量化——**这些开销的判定必须依赖 Android 真机**（见第四节）。
- VRAM 24.5 MB << 300 MB 绿线（无贴图为主）。

## 三、离线结构估算（红线校验，PERF_SPEC §3）
| 指标 | 估算值 | 红线 | 判定 |
|---|---|---|---|
| 场景总三角面（静态清点） | 33,232 | ≤150,000 | ✅ 合格 |
| 帧提交 Primitives（估算，无视锥剔除富余） | ≈44,379 | ≤150,000 | ✅ 合格 |
| DrawCalls | ≈97 | ≤100 | ✅ 合格（贴线） |
| 骨骼动画 | 1 件（黄牛，骨骼数见 asset_budget.json inventory） | ≤400 骨 | ✅ 合格 |
| 植被批处理 | 草 90 + 野花 22 + 蕨 18 + 围栏 18 = 4 个 MultiMesh 批次（各 1 DC） | 散摆 >300 禁止 | ✅ 合格 |

- DrawCalls 贴线的成因：50 种素材独立节点摆放（每实例 1 DC）。**正式工程组装时必须按类别合并/MultiMesh 化**，本场景已示范围栏+植被的合批模式。
- 估算口径：每实例 × surface 数，不含阴影 depth pass 与天空/后处理；真机以 GPU Profiler 实测为准。

## 四、Android 真机验证（缺件：本机无 adb / 无 Android SDK / 无连接设备）
状态：**未实测**。按 PERF_SPEC §2.1 的最小步骤即可补测（用户手机 + USB）：
1. Godot 编辑器 → 管理导出模板（下载 4.7.2 模板）
2. 编辑器设置 → 导出 → Android → 一键安装 OpenJDK + SDK
3. 项目 → 安装 Android 构建模板 → 导出预设 Android → Export Debug
4. 手机开 USB 调试 → 一键部署或 `adb install -t`
5. 本工程已内置采集 HUD（`--perf` 写 `user://perf_log.csv`），真机跑同样命令后 `adb pull` 取回
6. 测试纪律：拔充电线、亮度 50%、每机位 ≥60 秒、同一手机 ≤20 分钟

判定红线（真机数据填入后套用 PERF_SPEC §3）：帧时间 ≤20ms / Primitives ≤150k / DC ≤100 / 阴影 Δ≤4ms / 动画 Δ≤3ms / 植被 Δ≤5ms。

## 五、结论行
`平台=Windows 桌面(仅结构参考) | 机位=全景 | 结论=结构合格（面数/DC/骨骼/合批） | 超标项=无 | Android=未实测，缺件 | 依据=实测帧时间+离线估算`
