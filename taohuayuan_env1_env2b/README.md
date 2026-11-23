# 《桃花源物语》ENV-1 收尾 + ENV-2② 商业建筑样板（交 GPT 视觉验收）

> 私有仓正式整合提交：`1069081`（已推送 `master`）。
> 本目录为 AI 推送材料；正式源码/存档/玩法逻辑未对外。
> 验收边界：**只交付一栋商业样板**，剩余 4 商业 + 3 住宅、家具、3.7 系统均未开始。

---

## 一、ENV-1 地面系统：先核查、再补齐、再验收

### 1. 现状核查
`0db1c78` 已铺好 `GroundTint`（农场 8 斑 / 镇 6 斑 + MultiMesh 草点、道路折线共用、排除区覆盖河带/主屋/田地/建筑），代码层面完整，未重复开发。

### 2. 正式镜头验收发现的问题
12 张正式游戏正交镜头图（四向 + 近景）显示：原实现是**规则同心双圆盘**，草斑边缘是标准圆，达不到「不规则自然边缘」要求；初版替换后色阶又过弱几乎看不见。

### 3. 补齐内容
- `GroundTint.organic_patches()` 改为共享 **28 顶点噪声轮廓 Blob**（三次谐波叠加），每处 1 主瓣（深）+ 3 偏移小瓣（浅/中），逐实例随机旋转 + 非等比缩放。
- 色阶加深（深 -0.18 / 浅 +0.20），关闭背面剔除防绕序误判；仍是**单个 MultiMeshInstance3D、零新增碰撞**。
- 农田网格/种植坐标/碰撞/玩法逻辑零改动；道路与草地通过路缘草点带过渡；房屋/树下/田边排除区保留。
- 四向图与近景目检：无明显网纹、摩尔纹、重复接缝或穿地色块。

**证据**：`screenshots/env1/`（12 张，`farm_yaw0/90/180/270`、`town_yaw0/90/180/270`、`farm_ground_house_road`、`farm_ground_field_edge`、`town_ground_street_edge`、`town_ground_shop_base`）。

---

## 二、ENV-2② 商业建筑样板：杂货铺「轻伞盖顶」

### 1. 美术方向
以已定型 MODEL-1 为统一基准：暖奶油墙、蓝灰伞盖、柔和暖木门窗、圆润温馨、少量乡村点缀（一对小红灯笼 + 木招牌）。**没有**飞檐、斗拱、红柱、金瓦、传统亭子/宫殿感。

保留原杂货铺「伞盖屋顶」识别度，但重新设计比例：
- 屋面厚 0.13m、外挑 0.49m、檐口 3.43m、顶高 4.05m（原版顶大檐低压墙且遮招牌，已按正式镜头反馈缩小抬高）。
- 32 环向 × 6 径向曲面伞盖 + 10 根放射伞骨 + 4 根暖木檐柱；檐柱/石基/台阶**零碰撞**，不挡玩家绕行。
- 正面 1.6×2.2m 真实门洞（可进店）；两侧窗 + 背面双窗与货架，四向都有完整设计。

### 2. 色彩空间修正（关键）
Blender glTF 导出会把 Principled Base Color 线性值编码成 sRGB，首版在 Godot 读到 `(0.687,0.755,0.780)` 近白，和 MODEL-1 青瓦不同色域。脚本 `mat()` 内加 `_srgb_to_linear()` 反解，导入后：
- 屋顶 `(0.510,0.530,0.560)`（MODEL-1 L2 青瓦 `(0.506,0.527,0.556)`）
- 墙 `(0.955,0.930,0.850)`（L1 奶油墙 `(0.955,0.926,0.854)`）
- 木 `(0.620,0.500,0.380)`（L1 暖木 `(0.618,0.496,0.381)`）

### 3. 正式工程整合
- `assets/commercial/shop_umbrella.glb` → `scenes/structures/Buildings/ShopUmbrella.tscn` / `scripts/world/ShopUmbrella.gd`。
- TownGraybox 中杂货铺实例换成样板，节点名仍 `Grocery`（NPC 站位与探针口径不变）；旧 `Grocery.tscn` 保留为风格基线/测试对象，**其余 4 商业 + 3 住宅未动**。
- 碰撞分工沿用既有口径：`Wall_All` → layer1 trimesh；`Roof_All` → layer4 + `house_roof` 组/meta（可被 OcclusionFader 逐表面淡化）；`Decor_All` 纯装饰零碰撞。
- HouseBuilder / 房屋升级价格 / 存档 / 玩法逻辑 / 家具 / 3.7 全部未动。

### 4. 证据索引
**正式游戏镜头（9 张，`screenshots/env2b/`）**
- 四向：`shop_yaw270_front.png`（正门·朝广场）、`shop_yaw90_back.png`、`shop_yaw0_side_s.png`、`shop_yaw180_side_n.png`
- 细节：`shop_front_detail.png`、`shop_back_detail.png`、`shop_roof_detail.png`
- 组合/对比：`town_shop_neighbors.png`（与木匠铺/酒楼/住宅同框）、`town_plaza_with_new_shop.png`

**Blender 四向渲染（4 张，`blender_renders/`）**：`shop_umbrella_front/right/back/left.png`

**源文件（`source/`）**：`shop_umbrella.py`（生成脚本）、`shop_umbrella.blend`、`shop_umbrella.glb`、`test_env2b_shop.gd.txt`（行为验收套件）

---

## 三、测试结果

| 项 | 结果 |
|---|---|
| 全量回归 | **41 套件 / 1334 断言 / 0 FAIL / 0 SCRIPT ERROR** |
| 新增第 41 套件 | `test_env2b_shop` **17/17**：三 Mesh 分工、门洞可进、三面墙钻不入、NPC 入口净空、屋顶材质可淡化、不挡主街、邻栋净距 |
| 既有套件 | test_map_graybox 219/219、test_env_assets 103/103、test_house_scene 85/85 |
| 存档安全 | 生产档 MD5 `42753db4…` + mtime 前后零变化；SAVE-GUARD 3 次拦截全沙盒 |

---

## 四、面数 / Mesh / DrawCall 统计

| 项 | 数值 |
|---|---|
| 样板单栋 | **7724 tri**（Decor 5544 / Wall 264 / Roof 1916），3 MeshInstance、7 材质；≤8000 预算（96.5%） |
| 正式镇区 | MeshInstance **335 / 400**（余 65）、MultiMeshInstance 26、探针统计材质 8、三角面 1,998,112 |
| DrawCalls | **219**（桌面窗口实测，`Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME`） |
| 植被 | 重复植被继续 MultiMesh 合批，未新增逐株 MeshInstance |
| Android 真机 | **本环境无法实机验证，待补测**；桌面数据不能替代移动端结论 |

---

## 五、Gemini 协作报告（模式 D · 十项）

1. **任务名称**：ENV-2② 商业建筑样板 Blender 建模脚本
2. **协作模式**：D（双 AI 协作开发，六步流程）
3. **调用是否成功**：成功，一次返回（completion 8368 tokens）
4. **实际模型**：`gemini-4-argon`
5. **传递上下文**：Blender 4.5 约束、占地/朝向/门洞尺寸、MODEL-1 色板与风格红线、三 Mesh 命名分组、≤8000tri、固定函数签名、导出路径、禁止 API、文字由 Godot 侧补
6. **Gemini 原始贡献**：完整 `shop_umbrella.py`（clear_scene/mat/box/cyl/sphere/make_window/umbrella_roof/build_shop/join_by_tag/main）
7. **WorkBuddy 独立审查**：tag_of 仅 Wall_* 入碰撞（柱/台阶/门框/窗框零碰撞）；玻璃改 Decor_ 前缀；bevel 2→1、伞骨 16→10；色彩空间线性反解；按正式镜头反馈缩小抬高伞盖
8. **实际整合文件**：`asset_lab/commercial/shop_umbrella.py`、`assets/commercial/shop_umbrella.glb`、`scripts/world/ShopUmbrella.gd`、`scenes/structures/Buildings/ShopUmbrella.tscn`、`scripts/world/TownGraybox.gd`
9. **测试结果**：Blender 实跑 7724 tri / 3 Mesh / 7 材质；Godot 真机 9 图目检 + 17 断言行为套件 + 全量 41 套件绿
10. **未解决问题/分歧**：无技术分歧；Gemini 无图片通道，视觉判断完全由 WorkBuddy 真机截图承担。伞盖在 45° 正交镜头下仍比普通坡屋顶大，是否再缩小待 GPT 裁决

---

## 六、请 GPT 裁决

1. **样板是否通过视觉验收？**（未通过不批量制作剩余 7 栋）
2. 伞盖尺寸/厚度/颜色是否符合预期？是否需要进一步轻薄化？
3. 与 L1 木屋、L2 青瓦、邻栋旧商业建筑的风格统一度是否足够？
4. 正面招牌、灯笼、柜台等乡村点缀是否得当？
5. 门洞可进 + NPC 门前交互 + 装饰零碰撞的口径是否保留到后续 4 栋商业建筑？
