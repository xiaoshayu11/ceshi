# 小镇样板资产清单（第二轮精修后）

## A. 定制资产（Blender 4.5 生成，单材质顶点色 GLB）
| 文件 | 三角面 | 用途 | 说明 |
|---|---:|---|---|
| custom_house.glb | 3,712 | 玩家主住宅 | 蓝灰青瓦薄屋顶、奶油圆角墙、圆窗/窗棂/门廊/灯笼/烟囱/背侧窗 |
| custom_shop.glb | 4,144 | 杂货小店 | 开放售货台、条纹布篷、葫芦招牌、陶坛果篮、背侧窗 |
| custom_pond.glb | 160 | 精修新增：不规则池塘 | 单网格三圈顶点色深浅水（#6FB2B7/#4A8F97/#2E6872）+ 不规则岸线；法线修正朝上 |
| npc_rabbit.glb | 440 | 动物 NPC | 团子比例、粉鼻/眼高光/腮红、垂耳（精修统一眼高光与腮红） |
| npc_fox.glb | 600 | 动物 NPC | 大尾、短腿、杏仁眼、粉色内耳（精修放大眼/高光） |
| npc_calf.glb | 760 | 动物 NPC | 精修重做：二头身团子（头半径0.38/身0.45）、短粗象腿(0.28)、宽粉吻、大眼+高光+腮红、荷叶耳、圆钝角、抹茶斑 |
| prop_flowerpot.glb | — | 庭院花盆 | 5 朵花粉色花 |
| prop_crate.glb | — | 木箱 | 圆润板条 |

生成脚本：`blender/build_custom_assets.py`（第一版建筑/道具）、`blender/build_refine_assets.py`（第二轮池塘+三 NPC）、`blender/gen_textures.py`（草地噪声/水面波纹纹理）；打包源文件：`blender/town_sample_custom_assets.blend`（由最终 GLB 导入打包，可编辑）。

## B. 程序化纹理（第二轮新增）
| 文件 | 用途 | 参数 |
|---|---|---|
| `assets/textures/grass_noise.png` | 草地明暗层次 | 256×256 无缝瓦片，整数频率正弦叠加，色阶 #5A8058→#759961→#8AAC6C，uv1_scale 2.2×2.2 |
| `assets/textures/water_ripple.png` | 水面细节备选 | 128×128 近白极淡波纹；最终水面改用纯顶点色（叠加近白纹理会洗白水色），保留文件供后续微调 |

## C. 沿用资产（来自 pipeline_01 derived，未改原始归档）
树木 5 类、灌木、草、野花、蕨、芦苇、睡莲、石板/圆石、岩石、木栅栏/门、小桥、长椅、灯笼柱、鸟屋、井、桶、手推车、柴房；Poly Pizza 绿头鸭×2、鸡、鸟。原 `water-blob-f266b8.glb` 已被定制池塘替代，不再入场景。

## D. 场景实例与合批（第二轮最终）
- 38 种模型，44 条实例记录（含 MultiMesh 批量记录）。
- MultiMesh 批次：植被 3 组（草 125 / 野花 42 / 蕨 24），另把石板路、广场石、围栏、岸边石/草/花、树/灌木、长椅、花盆、灯笼、木箱、芦苇、中石、路边过渡草按同类合批。
- 静态三角面 **146,243**（红线 150k ✅）；DrawCalls 离线估算 **77**（红线 100 ✅）；唯一材质 48。
- lint：石灯笼 1（≤3）、秋色树 1（≤3）、NPC 4、无骨骼/蒙皮。
- 土路与地面 `cast_shadow = OFF`：大面积平面自阴影是横纹 acne 根因，关闭后条纹消失且建筑/树木阴影保留。

## E. 基础动作
NPC 采用 Godot 节点级 idle 呼吸（sin 位移 ±0.012m）+ nod 点头（-12°），动作截图 `evidence/npc_action.png`；无 AnimationPlayer/Skeleton，零蒙皮开销。
