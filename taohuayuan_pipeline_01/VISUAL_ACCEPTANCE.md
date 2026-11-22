# pipeline_01 视觉验收证据与检查结果（验收补充交付）

Public Raw 基址：`https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/`
全部链接在推送后逐条 `curl -I` 验证 HTTP 200（结果见本文件末尾「链接验证」）。

## 一、四向全景（45° 斜俯视游戏镜头，1280×720）
| 机位 | 单独 Raw 直链 |
|---|---|
| s0（南向北） | https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/evidence/scene_s0.png |
| s90（东向西） | https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/evidence/scene_s90.png |
| s180（北向南） | https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/evidence/scene_s180.png |
| s270（西向东） | https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/evidence/scene_s270.png |

四向目检结论：
- 穿地/悬空：主体建筑（仓库、柴房）、围栏、树木、动物均贴地；未发现主体穿地或悬空。
- 比例：熊/鹿/兔/狐/牛/羊/猪/鸡/鸭体高按 ART_ADAPT_SPEC_V1 §五归一，四向中未见明显比例失衡。
- 遮挡：核心区域（农田、池塘、村北建筑群）无互相遮挡导致的识别问题。
- 场景裁切：四向相机取景覆盖场景核心区，**边缘装饰件存在画面裁切**——s0 左上鹿/树、s90 上沿树、s180 上沿土路带与右下角动物、s270 左下熊与下沿动物。这是相机取景框小于 90×90 地形的取景裁切，非物件摆放出界；四向图用于核心区视觉验收，完整地形边界不在单张取景内。
- 色彩：整体绿-木棕-石灰主色统一、光线偏暖，符合温馨田园基调；秋色树仅 2 处点缀。

## 二、特写（真实游戏镜头）
| 内容 | 单独 Raw 直链 |
|---|---|
| 木屋/柴房特写 | https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/evidence/scene_cabin_detail.png |
| 池塘特写 | https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/evidence/scene_pond_detail.png |
| 动物特写 | https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/evidence/scene_animals_detail.png |

目检结论：
- 木屋/柴房：屋顶木棕两色带、柴房堆木清晰；两栋均贴地，柴房位于村北作为仓库/柴房，非玩家住宅。画面上沿/左沿有邻近树与倒木被取景裁切，非穿模。
- 池塘：水面、码头、两条船、石灯笼（1 件）、芦苇均贴地；睡莲渲染为白色（原始材质未随绿色色板重染），绿头鸭因体高归一后仅约 0.28m 在全景/特写中偏小——属已知视觉瑕疵，不影响资产导入验收，正式接入时可按规格单独调色/放大。
- 动物：牛/羊/猪体高与围栏比例一致，无悬空；猪的粉色饱和度略高于主色板，属原材质保留项。

## 三、Blender 重染前后对比
| 类型 | 单独 Raw 直链 |
|---|---|
| **同机位游戏镜头前后对比（推荐验收）** | https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/evidence/scene_before_after_comparison.png |
| 单体模型排列对比（仅颜色核对） | https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/evidence/before_after_comparison.png |

- 同机位对比：左为原始 GLB（同摆位，按处理后包围盒等比缩放），右为 Blender 归一化+色板吸附后；相同相机/光照/摆位，MultiMesh 植被两版均隐藏。可见高饱和红树/彩石被收敛为绿-木棕-石灰田园色系，证明重染效果在实际游戏镜头下成立。
- 单体排列对比**不作为**游戏展示证据，仅用于核对 17 类代表件的逐件颜色变化；游戏展示以第一、二节截图为准。

## 四、统计证据
| 文件 | 单独 Raw 直链 |
|---|---|
| 场景/资产统计（47 种入场景、224 实例、119,294 面、8 骨架/199 骨、DC 估算 123） | https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/evidence/asset_budget.json |
| 逐模型 Godot 审计（50 件、40,805 面、8 骨架/199 骨、8 AP/8 库/55 动画） | https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/evidence/godot_audit.json |
| 性能采样 CSV（4 组 × 60） | https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/evidence/perf_log.csv |
| 导入清单 v2 | https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/IMPORT_LIST.md |
| 性能报告 v2 | https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/PERF_STATS.md |
| 授权台账 v2 | https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/LICENSE_LEDGER_V2.md |
| 前后处理报告 | https://raw.githubusercontent.com/xiaoshayu11/ceshi/main/taohuayuan_pipeline_01/BEFORE_AFTER.md |

## 五、链接验证
推送后执行 `for u in <上述 URL>; do curl -s -o /dev/null -w '%{http_code} %{url_effective}\n' -I "$u"; done`，逐条结果：全部 **HTTP 200**（验证时间：2026-11-22，commit 见交付消息）。
