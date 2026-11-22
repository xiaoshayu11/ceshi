# 桃花源物语 MODEL-1 三档房屋视觉验收材料

日期：2026-11-23 ｜ 管线：bpy 4.5 程序化脚本 → GLB → Godot 4.7.2
本轮只交付视觉验收材料，未做 HouseBuilder 正式整合，未开始家具模型。

## 1. 总览图（先看这个）

- `blender_four_views/overview_4views.png` — 三档 × 四向（南/东/北/西）12 宫格总览

## 2. Blender 渲染四向图（12 张独立截图）

- `blender_four_views/house_l0_{south,east,north,west}.png` — L0 破屋
- `blender_four_views/house_l1_{south,east,north,west}.png` — L1 木屋
- `blender_four_views/house_l2_{south,east,north,west}.png` — L2 瓦房+耳房

## 3. Godot 实际游戏镜头展示图（真实农场场景 + 游戏同款正交 52° 俯仰相机）

每档四向（view0=南 / view90=东 / view180=北 / view270=西）+ 细节特写：

- L0 破败细节：`godot_gameview/glb_L0_detail_decay.png`（歪斜墙/补丁板/茅草秃斑/危屋木牌）
- L1 标准住宅：`godot_gameview/glb_L1_detail_front.png`（门灯/双窗/台阶/烟囱）
- L2 中国元素：`godot_gameview/glb_L2_detail_roof.png`（凹曲瓦顶/翘角/正脊/灯笼）+ `glb_L2_detail_wing.png`（耳房/院门楼）

## 4. 模型文件

- `glb/house_l{0,1,2}.glb` — 与正式工程 `assets/houses/` 完全一致（已通过 Godot 导入探针）
- `blender_source/house_l{0,1,2}.blend` — Blender 源文件

## 5. 面数统计（asset_report.json，Godot 导入后实测）

| 档位 | 名称 | 三角面 | 预算 8000 | 材质 | Mesh 结构 | 贴地 |
|---|---|---|---|---|---|---|
| L0 | 破屋 | 1956 | ✅ | 7 | Wall_All/Roof_All/Decor_All | y=0 ✅ |
| L1 | 木屋 | 5748 | ✅ | 7 | 同上 | y=0 ✅ |
| L2 | 瓦房+耳房 | 7916 | ✅ | 8 | 同上 | y=0 ✅ |

命名规范：墙体 *Wall*（碰撞层1）/ 屋顶 *Roof*（遮挡层4）/ 装饰 Decor_*，100% 符合。
门朝 -Z，与现有交互（门口按 F 进屋）规格逐条对齐。

## 6. 审查重点

1. **L0 破败感**：当前歪斜/补丁幅度偏保守（已知遗留点，可按反馈加大）
2. **L1 标准住宅**：蓝灰青瓦 + 暖奶油墙 + 暖木门窗（本轮统一配色后效果）
3. **L2 中国元素比例**：凹曲坡屋顶、翘角、正脊脊饰、红灯笼、院门楼金匾——比例是否符合预期
4. 材质均为纯色 Principled（无贴图，符合预算方向）
