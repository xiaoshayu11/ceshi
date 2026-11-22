# 小镇样板资产清单

## A. 定制资产（Blender 4.5 生成，单材质顶点色 GLB）
| 文件 | 三角面 | 用途 | 说明 |
|---|---:|---|---|
| custom_house.glb | 3,712 | 玩家主住宅 | 蓝灰青瓦薄屋顶、奶油圆角墙、圆窗/窗棂/门廊/灯笼/烟囱/背侧窗 |
| custom_shop.glb | 4,144 | 杂货小店 | 开放售货台、条纹布篷、葫芦招牌、陶坛果篮、背侧窗 |
| npc_rabbit.glb | 440 | 动物 NPC | 团子比例、粉鼻/眼高光/腮红、垂耳 |
| npc_fox.glb | 600 | 动物 NPC | 大尾、短腿、杏仁眼、粉色内耳 |
| npc_calf.glb | 948 | 动物 NPC | 圆角胶囊身、粉吻、圆钝角、荷叶耳 |
| prop_flowerpot.glb | — | 庭院花盆 | 5 朵花粉色花 |
| prop_crate.glb | — | 木箱 | 圆润板条 |

生成脚本：`blender/build_custom_assets.py`；打包源文件：`blender/town_sample_custom_assets.blend`（由最终 GLB 导入打包，可编辑）。

## B. 沿用资产（来自 pipeline_01 derived，未改原始归档）
树木 5 类、灌木、草、野花、蕨、芦苇、睡莲、水面、石板/圆石、岩石、木栅栏/门、小桥、长椅、灯笼柱、鸟屋、井、桶、手推车、柴房、土路；Poly Pizza 绿头鸭×2、鸡、鸟。合计 31 类沿用资产。

## C. 场景实例与合批
- 38 种模型，41 条实例记录（含 MultiMesh 批量记录）。
- MultiMesh 批次：植被 3 组（草 125 / 野花 42 / 蕨 24），另把石板路、广场石、围栏、岸边石、树/灌木、长椅、花盆、灯笼、木箱、芦苇、中石按同类合批。
- 静态三角面 128,727；DrawCalls 离线估算 80；唯一材质 48（多为一资产一材质 + 运行时 override 共享实例）。
- lint：石灯笼 1（≤3）、秋色树 1（≤3）、NPC 4、无骨骼/蒙皮。

## D. 基础动作
NPC 采用 Godot 节点级 idle 呼吸（sin 位移 ±0.012m）+ nod 点头（-12°），动作截图 `evidence/npc_action.png`；无 AnimationPlayer/Skeleton，零蒙皮开销。
