# 《桃花源物语》小镇样板交付索引

Public Raw 基址（GitHub ceshi 仓库）：
`https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_town_sample/`

**目录约定（本版修正）**：Godot 工程入口为 `project/project.godot`；所有运行时资源位于 `project/assets/`，所有运行产物（截图/统计/性能）写入 `project/evidence/`。没有任何 Windows 软链接、绝对路径或仓库外依赖；克隆后直接可跑。

## 第二轮精修（先看这里）
- 精修报告：`docs/REFINE_REPORT_V2.md`（前后对比 + 逐项目检 + 性能 + 技术留痕）
- **全景前后对比**：`project/evidence/refine_before_after.png`
- **池塘精修前后对比**：`project/evidence/pond_before_after.png`
- 新增：地面噪声纹理 `project/assets/textures/grass_noise.png`、定制池塘 `project/assets/models/custom/custom_pond.glb`

## 必看（视觉审查 - 精修后）
- 完整样板：`project/evidence/town_full.png`
- 四向：`project/evidence/town_s0.png` / `town_s90.png` / `town_s180.png` / `town_s270.png`
- 住宅正面与细节：`project/evidence/house_front_a.png` / `house_front_b.png` / `house_detail.png`
- 商店：`project/evidence/shop_front.png`
- NPC 正面/侧面：`project/evidence/npc_rabbit_front.png` / `npc_rabbit_side.png` / `npc_fox_front.png` / `npc_fox_side.png` / `npc_calf_front.png` / `npc_calf_side.png`
- NPC 动作：`project/evidence/npc_action.png`
- 组合：`project/evidence/combo_pond_path.png` / `combo_shop_furniture.png`

## 文档
- `docs/TOWN_SAMPLE_REPORT.md`：第一轮视觉验收 + 桌面/Android 分开的性能记录
- `docs/REFINE_REPORT_V2.md`：第二轮视觉精修与最终修正说明
- `docs/ASSET_LIST.md`：定制/沿用资产清单与统计
- `docs/GEMINI_DESIGN_NOTES.md`：Gemini 独立方案与实际落地/偏差对照（含第二轮 P0/P1）

## 源文件与资产
- `blender/build_custom_assets.py` / `build_refine_assets.py` / `gen_textures.py` / `pack_blend_source.py`：Blender 4.5 生成脚本，输出统一写入 `project/assets/`
- `blender/town_sample_custom_assets.blend`：可编辑 Blender 源文件
- `blender/asset_report.json` / `refine_report.json`：定制资产面数
- `project/assets/models/custom/*.glb`：8 件定制 GLB（含池塘）
- `project/assets/models/nature/*.glb`：28 件沿用 GLB
- `project/assets/models/pp/*.glb`：4 件沿用 GLB
- `project/assets/textures/*.png`：程序化纹理
- `project/`：Godot 4.7.2 工程入口、场景、脚本、资源与证据

## 工程运行（干净克隆后直接执行）
环境：Godot 4.7.2（gl_compatibility / GLES3）。把 `godot4` 换成实际可执行文件即可；Windows 例如
`$LOCALAPPDATA/Microsoft/WinGet/Packages/GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe/Godot_v4.7.2-stable_win64_console.exe`。

```bash
# 首次导入资源（生成 .godot 缓存；无需提交）
godot4 --headless --path project --import

# 出图：窗口模式（headless 下 frame_post_draw 不触发，无法保存截图）
# 全套截图写入 project/evidence/，末尾打印 SHOTS_DONE
godot4 --path project scenes/Main.tscn

# 性能采样：写 project/evidence/town_perf.csv，末尾打印 PERF_DONE
godot4 --headless --path project scenes/Main.tscn -- --perf
```

`project/scripts/main.gd` 使用的全部 `res://` 路径：`res://scenes/Main.tscn`、`res://scripts/main.gd`、`res://assets/models/{custom,nature,pp}/*.glb`、`res://assets/textures/grass_noise.png`、`res://evidence/…`（均为运行产物路径），在仓库内全部真实存在。

## 统计
- `project/evidence/town_stats.json`：146,243 静态面 / DC 估算 77 / 38 种模型 / 44 实例记录 / 0 骨骼
- `project/evidence/town_perf.csv`：桌面 4 组 × 30 样本；Android 未实测（缺设备），不以桌面数据推断手机合格
