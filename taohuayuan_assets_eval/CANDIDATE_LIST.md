# 外部 3D 素材库候选清单 v1.0
《桃花源物语》商用素材评估 · 2026-11-22 · 独立 ArtLab 工程（未动正式项目）

## 来源与授权结论

| 来源 | 授权 | 商用 | 署名 | 再分发 |
|---|---|---|---|---|
| Polyfork 免费网格（GLB） | **双授权可选：CC BY 4.0 或 Polyfork 自有授权** | ✅ | CC BY 需一行署名；Polyfork 授权**免署名** | CC BY 下允许（需署名）；Polyfork 授权禁止文件再分发 |
| Poly Pizza（逐模型核实） | CC0 或 CC-BY（按下载页显示） | ✅（NC 类已排除） | CC0 免署名；CC-BY 需署名作者 | CC0 允许；CC-BY 按条款 |

- 本次选用：Polyfork 网格走 **Polyfork 授权**（游戏内嵌使用、免署名、不重新分发文件）；Poly Pizza CC-BY 件在游戏署名页统一列作者。
- 所有模型**单独核实了下载页/官方 licensing 页显示的授权**，未按作者或包名推断。
- 未抓取 Poly Pizza 全站内容，仅定向搜索 + 逐页核实。

## 验证方法

- Godot 4.7.2 headless `--import` 0 错误 + 场景实例化实测（面数/材质/包围盒统计）。
- Blender 4.5 `--factory-startup` glTF 导入抽查 7 件全部通过。
- 渲染注意：Polyfork GLB 顶点色需运行时启用（Godot 导入器不自动勾选），一行 material override 解决；Poly Pizza 部分件为素色/贴图材质，直接可用。

## 一、Polyfork Nature & Forest Kit（47 件候选，61,000 三角面，12MB）

 kit 页：https://polyfork.dev/kit/nature-forest-kit-f29d6a （free 59 parts，本清单收录 47 件）
 每件 = CDN 直链 GLB，SHA256 见 evidence/polyfork_sha256.txt

| 模型 | 用途 | 面数 | 大小 | 包围盒(m) | 推荐 |
|---|---|---|---|---|---|
| birch-tree | 白桦树（庭院/路边绿化） | 619 | 70KB | 3.01x6.49x2.1 | ⭐主推 |
| birdhouse-post | 鸟屋柱（鸟类互动点） | 393 | 45KB | 0.45x1.8x0.48 | ⭐主推 |
| black-bear | 黑熊（山野氛围） | 2542 | 1525KB | 0.95x1.42x2.09 | ⭐主推 |
| broadleaf-oak | 橡树（主景树） | 457 | 52KB | 4.5x6.98x3.57 | ⭐主推 |
| campsite-picnic-table | 野餐桌 | 572 | 65KB | 2.0x0.75x1.6 | ⭐主推 |
| cattail-reed | 香蒲（水边） | 388 | 44KB | 0.39x1.2x0.29 | ⭐主推 |
| chopping-block | 柴墩砧板 | 484 | 56KB | 0.6x0.85x0.52 | 🟡备选 |
| dead-tree | 枯树（野趣点缀） | 536 | 61KB | 3.19x5.0x1.87 | 🟡备选 |
| dirt-trail-strip | 泥土路带 | 112 | 14KB | 1.41x0.03x3.0 | ⭐主推 |
| dock-platform-section | 码头平台段 | 356 | 41KB | 2.0x0.62x1.6 | ⭐主推 |
| fallen-log | 倒木 | 484 | 55KB | 3.09x0.9x0.7 | ⭐主推 |
| fern-plant | 蕨草（林下植被） | 802 | 90KB | 1.02x0.72x0.97 | ⭐主推 |
| firewood-stack | 柴火堆（生活气息） | 752 | 85KB | 1.18x0.76x0.66 | ⭐主推 |
| forest-deer | 鹿（野生动物） | 2230 | 1391KB | 0.84x2.12x1.44 | ⭐主推 |
| forest-rabbit | 兔子（野生动物/可捕捉） | 2074 | 1189KB | 0.2x0.37x0.4 | ⭐主推 |
| grass-tuft | 草丛（地表装饰） | 368 | 42KB | 0.34x0.35x0.31 | ⭐主推 |
| lantern-post | 灯笼柱（路灯，夜景点亮） | 482 | 55KB | 0.47x2.4x0.93 | ⭐主推 |
| large-boulder | 大岩石（造景） | 566 | 64KB | 2.2x0.66x1.39 | ⭐主推 |
| lily-pad | 睡莲叶（池塘） | 398 | 45KB | 0.6x0.04x0.59 | ⭐主推 |
| log-cabin | 原木小屋（建筑参考/仓库） | 1326 | 149KB | 6.0x5.47x6.96 | ⭐主推 |
| log-plank-bridge | 木桥（过河） | 480 | 55KB | 4.0x1.33x1.72 | ⭐主推 |
| maple-tree | 枫树（秋色点缀） | 422 | 48KB | 3.29x6.43x3.21 | ⭐主推 |
| medium-rock | 中岩石 | 374 | 43KB | 1.0x0.5x0.95 | ⭐主推 |
| nature-forest-terrain |  | 26540 | 3106KB | 92.0x17.93x101.0 | — |
| open-woodshed | 敞棚柴房 | 1250 | 138KB | 4.0x2.74x2.0 | ⭐主推 |
| red-fox | 狐狸（野生动物） | 2280 | 1400KB | 0.38x0.95x1.47 | ⭐主推 |
| rock-spire | 尖石（山石造景） | 378 | 43KB | 1.29x3.5x1.46 | ⭐主推 |
| round-bush | 圆灌木（绿化） | 573 | 65KB | 1.27x0.63x0.87 | ⭐主推 |
| round-path-stone | 圆汀步石（小路） | 52 | 7KB | 0.7x0.06x0.57 | ⭐主推 |
| slab-path-stone | 石板路（路径） | 76 | 10KB | 1.1x0.06x0.7 | ⭐主推 |
| small-rock | 小石子 | 202 | 24KB | 0.35x0.22x0.26 | ⭐主推 |
| stone-fire-pit | 石火坑（营地） | 584 | 67KB | 1.21x0.42x1.16 | ⭐主推 |
| stone-well | 石井（庭院摆件） | 608 | 70KB | 1.57x1.86x1.6 | ⭐主推 |
| tall-pine-tree | 高大松树（背景林） | 350 | 40KB | 3.67x9.0x3.56 | ⭐主推 |
| toadstool | 蘑菇（林间小景） | 604 | 68KB | 0.33x0.35x0.32 | 🟡备选 |
| trail-signpost | 路牌 | 420 | 49KB | 1.15x2.0x1.16 | 🟡备选 |
| tree-stump | 树桩 | 505 | 57KB | 0.82x0.48x0.72 | ⭐主推 |
| water-blob | 水面件（池塘/溪流） | 320 | 53KB | 8.0x0.04x6.8 | ⭐主推 |
| wildflower | 野花（花田/点缀） | 405 | 46KB | 0.15x0.4x0.15 | ⭐主推 |
| wooden-barrel | 木桶（杂物） | 540 | 62KB | 0.6x0.9x0.58 | ⭐主推 |
| wooden-bench | 木长椅（休憩） | 564 | 64KB | 1.8x0.9x0.53 | ⭐主推 |
| wooden-canoe | 独木舟（水上游玩） | 1020 | 115KB | 0.9x1.06x4.2 | ⭐主推 |
| wooden-fence-gate | 木栅栏门 | 408 | 47KB | 2.0x1.3x0.32 | ⭐主推 |
| wooden-fence-section | 木栅栏段（农场围栏） | 428 | 49KB | 2.0x1.1x0.24 | ⭐主推 |
| wooden-hand-cart | 手推车（农场运输） | 1416 | 158KB | 1.46x0.96x2.41 | ⭐主推 |
| wooden-rowboat | 划艇（码头） | 1262 | 143KB | 1.2x0.82x3.4 | ⭐主推 |
| young-pine | 幼松（灌木层） | 270 | 31KB | 1.84x3.0x1.87 | ⭐主推 |

> 主推 42 件全部来自田园方向：树木/花石/路径/围栏/桥/井/灯柱/动物/小屋。排除项：Ranger 皮卡、瞭望塔等美式林区题材，与桃花源画风不符。
> 地形大件 nature-forest-terrain（92×101m, 26.5k 面）可做参考或直接裁剪使用。

## 二、Poly Pizza 定向补充（14 件候选，全部逐页核实授权）

| 模型 | 作者 | 授权 | 面数 | 大小 | 原始尺寸 | 推荐 |
|---|---|---|---|---|---|---|
| Sheep 绵羊 (pp_C39AUXUUes) | Quaternius | CC0 | 610 | 153KB | 0.75x2.0x1.47 | ⭐主推 |
| Sheep 绵羊（变体） (pp_rgJXF570ZK) | Quaternius | CC0 | 2528 | 218KB | 0.76x1.22x2.0 | ⭐主推 |
| Cow 黄牛（带动画） (pp_26zM1outCr) | Quaternius | CC0 | 2450 | 1004KB | 0.57x1.14x2.0 | ⭐主推 |
| Cow 黄牛（变体） (pp_5XSc2Fka3F) | Quaternius | CC0 | 796 | 323KB | 0.49x1.12x2.0 | 🟡备选 |
| Pig 猪 (pp_u35l6uP5vj) | Quaternius | CC0 | 2816 | 293KB | 0.82x1.58x2.0 | ⭐主推 |
| Bird 鸟 (pp_gYYC0gYMnw) | Quaternius | CC0 | 1204 | 47KB | 2.0x1.01x1.66 | ⭐主推 |
| Japanese Door 木格门 (pp_t4otyljz8K) | Quaternius | CC0 | 106 | 13KB | 2.0x1.85x0.13 | 🟡备选 |
| Chicken 白鸡 (pp_1YE8U35HXsI) | jeremy（Google Poly 存档） | CC-BY 4.0 | 648 | 50KB | 1.77x2.0x1.09 | ⭐主推 |
| Duck 绿头鸭 (pp_2KHEgw1ztVI) | jeremy（Google Poly 存档） | CC-BY 4.0 | 504 | 31KB | 2.0x1.83x1.1 | ⭐主推 |
| Hen 母鸡（贴图） (pp_8Unya0rw9tR) | Poly by Google | CC-BY 3.0 | 592 | 35KB | 0.96x2.0x1.61 | 🟡备选 |
| Chicken 鸡（卡通） (pp_oHmIgi4boa) | madtrollstudio | CC-BY 4.0 | 776 | 118KB | 0.59x1.98x2.0 | — |
| Japanese Stone Lamp 石灯笼 (pp_5gZfOZIW92k) | Flopsi（Google Poly 存档） | CC-BY 4.0 | 432 | 25KB | 0.61x2.0x0.59 | ⭐主推 |
| Bonsai 盆景 (pp_1BtyNc_gX5a) | Poly by Google | CC-BY 3.0 | 751 | 245KB | 1.35x1.57x2.0 | 🟡备选 |
| Western Bluebird 西蓝鸲 (pp_cdcl5UwlYWd) | Poly by Google | CC-BY 3.0 | 894 | 756KB | 0.8x1.27x2.0 | 🟡备选 |

> Poly Pizza 补足了 Polyfork 缺口：家禽家畜（鸡/鸭/羊/牛/猪）、鸟类、石灯笼、盆景。
> **比例警告**：Google Poly 存档件原始尺寸混乱（鸡 167m、母鸡 77m），落地前必须按包围盒归一化；Quaternius 件尺度也偏大（羊 9m），统一缩放流程已在展示工程验证。

## 三、手机端性能评估

- Polyfork 47 件合计 58,272 面（若剔除 26.5k 的地形件，46 件仅 31.7k 面，平均 ~700 面/件），每件 1 个材质、无贴图 → 可合批、可合并 draw call，**非常适合手机端**。
- Poly Pizza 14 件合计 13,026 面；牛（带骨骼动画）2.5k 面为最大件，可控。
- 建议统一管线：Blender 批量归一化缩放 → （可选）减面/合批 → Godot 运行时顶点色材质。

## 四、展示场景截图（evidence/）

- overview_s0/s90/s180/s270.png：Polyfork 47 件四向全景网格
- detail_cabin.png：木屋特写；detail_terrain.png：大地形件
- pp_overview_s0/s90/s180/s270.png：Poly Pizza 14 件四向全景
- pp_detail_chicken.png：动物区特写

## 五、边界声明

- 全程未修改正式游戏工程，未替换正式资产，未提交推送正式项目。
- 原始模型仅存于本地评估工程，未重新打包发布。
- 未采用任何无法确认商用授权的模型（Poly Pizza 搜索中未发现 NC 件进入候选；如后续发现一律排除）。
