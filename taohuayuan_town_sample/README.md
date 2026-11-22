# 《桃花源物语》小镇样板交付索引

Public Raw 基址（GitHub ceshi 仓库）：
`https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_town_sample/`

## 第二轮精修（先看这里）
- 精修报告：`docs/REFINE_REPORT_V2.md`（前后对比 + 逐项目检 + 性能 + 技术留痕）
- **精修前后全景对比**：`evidence/refine_before_after.png`
- **池塘精修前后对比**：`evidence/pond_before_after.png`
- 新增：地面噪声纹理（`assets/textures/grass_noise.png`）、定制池塘 GLB（`assets/models/custom/custom_pond.glb`）

## 必看（视觉审查 - 精修后）
- 完整样板：`evidence/town_full.png`
- 四向：`evidence/town_s0.png` / `town_s90.png` / `town_s180.png` / `town_s270.png`
- 住宅正面与细节：`evidence/house_front_a.png` / `house_front_b.png` / `house_detail.png`
- 商店：`evidence/shop_front.png`
- NPC 正面/侧面：`evidence/npc_rabbit_front.png` / `npc_rabbit_side.png` / `npc_fox_front.png` / `npc_fox_side.png` / `npc_calf_front.png` / `npc_calf_side.png`
- NPC 动作：`evidence/npc_action.png`
- 组合：`evidence/combo_pond_path.png` / `combo_shop_furniture.png`

## 文档
- `docs/TOWN_SAMPLE_REPORT.md`：视觉验收 + 桌面/Android 分开的性能记录
- `docs/ASSET_LIST.md`：定制/沿用资产清单与统计
- `docs/GEMINI_DESIGN_NOTES.md`：Gemini 独立方案与实际落地/偏差对照（含第二轮 P0/P1）（含第二轮 P0/P1）

## 源文件与资产
- `blender/build_custom_assets.py` / `build_refine_assets.py` / `gen_textures.py`：Blender 4.5 生成脚本（第二轮）
- `blender/town_sample_custom_assets.blend`：可编辑 Blender 源文件（打包最终 GLB）
- `blender/asset_report.json` / `refine_report.json`：定制资产面数
- `assets/models/custom/*.glb`：8 件定制 GLB（含新池塘）
- `assets/models/nature/*.glb`、`assets/models/pp/*.glb`：31 件沿用 GLB
- `project/`：Godot 4.7.2 工程入口与场景脚本

## 工程运行
- 窗口模式出图：`Godot_v4.7.2 --path project scenes/Main.tscn`
- 性能采样：追加 `-- --perf` 写 `evidence/town_perf.csv`
- 纹理位于 `assets/textures/`，随 Godot 工程一并导入

## 工程运行
- 窗口模式出图：`Godot_v4.7.2 --path project scenes/Main.tscn`
- 性能采样：追加 `-- --perf` 写 `evidence/town_perf.csv`
- 纹理位于 `assets/textures/`，随 Godot 工程一并导入

## 统计
- `evidence/town_stats.json`：146,243 静态面 / DC 估算 77 / 38 种模型 / 44 实例记录 / 0 骨骼
- `evidence/town_perf.csv`：桌面 4 组 × 30 样本；Android 未实测（缺设备）
