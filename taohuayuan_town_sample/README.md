# 《桃花源物语》小镇样板交付索引

Public Raw 基址（GitHub ceshi 仓库）：
`https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_town_sample/`

## 必看（视觉审查）
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
- `docs/GEMINI_DESIGN_NOTES.md`：Gemini 独立方案与实际落地/偏差对照

## 源文件与资产
- `blender/build_custom_assets.py`：Blender 4.5 生成脚本
- `blender/town_sample_custom_assets.blend`：可编辑 Blender 源文件（打包最终 GLB）
- `blender/asset_report.json`：定制资产面数
- `assets/models/custom/*.glb`：7 件定制 GLB
- `assets/models/nature/*.glb`、`assets/models/pp/*.glb`：31 件沿用 GLB
- `project/`：Godot 4.7.2 工程入口与场景脚本

## 统计
- `evidence/town_stats.json`：128,727 静态面 / DC 估算 80 / 38 种模型 / 41 实例记录 / 0 骨骼
- `evidence/town_perf.csv`：桌面 4 组 × 30 样本；Android 未实测（缺设备）
