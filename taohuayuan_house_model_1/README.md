# 桃花源物语 MODEL-1 三档房屋 · GPT 复核后最终微调版

日期：2026-11-23（第二轮）｜ 基线：a31ee33 ｜ 管线：bpy 4.5 → GLB → Godot 4.7.2
本轮按 GPT 视觉验收结论微调 L0 / L2，**L1 未做任何修改**（正式定型基准）。

## 复核结论落实情况

| 结论 | 落实 |
|---|---|
| L1 通过定型 | 代码零改动，GLB tri 与材质完全一致（5748 / 7 mats） |
| L0 加强破败 | 秃斑 2→4 个（解析式贴坡面）、檐口茅草残束 ×4、墙体大块色差泥灰修补 ×2、补丁 4→5 块、整墙/角柱/门板歪斜加大；仍保持温馨田园风 |
| L2 弱化中式 | 门楼柱红→暖木色、金匾 1.6×0.5→1.05×0.32、门楼整体缩小并前收至屋檐前 0.35m（门廊感）、红门降饱和保留、灯笼/耳房/青瓦/奶油墙保留 |

**兼容性修复（附带）**：原版 L2 院门楼前伸到 z≈13.2，正骑在农场围栏线 z=15.0（layer1 碰撞）上——横杆穿柱而过。前收后门楼全部在围栏以北（z≥15.95），冲突消除。L0/L1 footprint 与围栏无冲突。

## 面数（Godot 导入后实测，asset_report.json）

| 档位 | tri | 预算 8000 | 材质 | 说明 |
|---|---|---|---|---|
| L0 | 2396 | ✅ | 8 | 旧 1956 → +440（破败细节） |
| L1 | 5748 | ✅ | 7 | 与上版完全一致 |
| L2 | 7916 | ✅ | 9 | 与上版一致（弱化只改尺寸/材质） |

命名 Wall_All/Roof_All/Decor_All、贴地 y=0、门朝 -Z 全部保持。

## 快速查看

1. **前后对比（4 张）**：`before_after/compare_L0_view0.png`、`compare_L0_detail_decay.png`、`compare_L2_view0.png`、`compare_L2_detail_roof.png`
2. **L0 四向**：`blender_four_views/house_l0_{south,east,north,west}.png`
3. **L2 四向**：`blender_four_views/house_l2_{south,east,north,west}.png`
4. **Godot 真机（更新后全量 16 张）**：`godot_gameview/glb_L{0,1,2}_view{0,90,180,270}.png` + 4 张细节
5. **总览**：`blender_four_views/overview_4views.png`
6. **模型**：`glb/` ×3、`blender_source/` ×3、`asset_report.json`

## 执行边界（本轮未做）

HouseBuilder 整合、家具模型、3.7 家具逻辑——均未动。等 GPT 复核批准后进入正式整合。
