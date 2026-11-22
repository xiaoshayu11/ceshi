# 小镇样板 · 干净环境启动验证（最终修正版）

验证目的：把 4967bc7 从“本地能跑”变成“任何人克隆后都能跑”。

## 环境与方法
- 提交：先推送 `2a38090`，再从 GitHub `https://github.com/xiaoshayu11/ceshi.git` 全新 `--depth 1` 克隆到 `C:/Users/小鲨鱼/WorkBuddy/ceshi_clean_verify`（ HEAD = `2a38090` ），未复用原工作目录、未复制任何本地未提交文件、无软链接。
- 引擎：Godot v4.7.2.stable（Win64 console），`gl_compatibility` / OpenGL 3.3（NVIDIA RTX 4060）。
- 严格按 README：`cd taohuayuan_town_sample` → `godot4 --headless --path project --import` → `godot4 --path project scenes/Main.tscn`。
- 说明：出图必须用窗口模式；headless 下 `RenderingServer.frame_post_draw` 不触发，无法保存 PNG。导入与性能采样可 headless。

## 结果
| 检查项 | 实测 |
|---|---|
| `res://` 路径审计（脚本 7 条） | missing = 0 |
| 运行时 GLB | 40 件，全部位于 `project/assets/models/` |
| 纹理 | `grass_noise.png`、`water_ripple.png` 位于 `project/assets/textures/`；导入日志命中 grass_noise 2 次 |
| 旧路径残留 | 根 `assets/` 与根 `evidence/` 均不存在 |
| 首次导入 `--import` | exit 0；ERROR / SCRIPT ERROR / Failed = 0 |
| 窗口模式出图 | exit 0；`SAVED` 18 张；`SHOTS_DONE` 1 次 |
| 加载错误 | `MISSING` 0；`ERROR` / `SCRIPT ERROR` / `Parse Error` 0 |
| 四向截图 | `town_s0/s90/s180/s270.png` 均在干净副本中重新生成 |
| 主住宅 / 商店 / 兔 / 狐 / 小牛 / 池塘 | 干净副本重出的 `town_full.png` 目检全部正常显示，无空白、无缺模型 |
| 草地噪声 | 重出截图可见柔和低频明暗，非纯色平板；无网纹/摩尔纹 |
| 统计一致性 | 重跑 `town_stats.json` 与提交版 SHA256 一致：146,243 面 / DC 77 / 38 种模型 / 44 实例 / 0 骨骼 |

截图文件字节与提交版不完全相同，原因是 NPC idle 呼吸/点头与水面 UV 随时间变化导致逐帧差异；统计 JSON 完全一致，画面经目检无回归。`refine_before_after.png` 与 `town_stats.json` 哈希与提交版一致。

## 性能边界与如实标注
未新增几何；静态 146,243 面仍在 150,000 红线内，DC 估算 77。桌面实测仍沿用先前 4 组 × 30 样本记录（中位约 6.9ms / 145 FPS，VRAM 计数该环境返回 0 已如实标注）。Android 未实测（无设备/SDK），不以桌面数据推断手机合格；正式工程接入需另留 NPC、作物、交互物与动态场景预算。

## 边界
验证仅在公开 `ceshi` 仓库的独立目录与临时干净副本内进行；未修改正式游戏工程、未替换正式资产、未恢复 3.6 阶段二。
