# 美术实验资源与许可证清单（2026-11-22）

| 资源 | 来源 | 作者/发布方 | 许可证 | 商用 | 署名 | 修改 | 下载文件 | 使用范围 |
|---|---|---|---|---|---|---|---|---|
| Stylized Nature MegaKit (Standard) | https://opengameart.org/node/174566 （官方上传，另见 quaternius.com/packs/stylizednaturemegakit.html） | Quaternius | CC0 1.0 Universal | ✅ 允许 | ❌ 不要求 | ✅ 允许 | stylized_nature_megakitstandard.zip（104MB，68 模型） | 树木/花草/灌木/岩石/草——展示场景植被全部 |
| Medieval Village MegaKit (Standard) | https://opengameart.org/content/medieval-village-megakit | Quaternius | CC0 1.0 Universal | ✅ 允许 | ❌ 不要求 | ✅ 允许 | medieval_village_megakitstandard.zip（100MB，176 模型） | 木栅栏等村庄构件 |
| LowPoly Medieval Village Pack (2020-12) | https://opengameart.org/content/lowpoly-medieval-village-pack （页面经评论页 93950 引导确认） | Quaternius | CC0 1.0 Universal | ✅ 允许 | ❌ 不要求 | ✅ 允许 | medieval_village_pack_-_dec_2020.zip（8.3MB） | 一栋完整房屋（可能再经 Blender 调整比例/配色） |

## 许可证核验依据
- OpenGameArt 两个包页面均由 **quaternius 本人上传**，License 字段明确标注 **CC0**，且归入 "All CC0" 合集。
- quaternius.com 官网两个包页面均标注 "Free to use in personal, educational and commercial projects. (CC0 License)"。
- itch.io 页面 Asset license 字段：Creative Commons Zero v1.0 Universal。
- CC0 含义：可商用、可修改、无需署名、可再分发。本实验仍主动署名致谢。

## 红线确认
- ❌ 不使用任何从《动物森友会》等商业游戏提取的内部素材（已拒绝该请求）。
- ❌ 不使用"轻微修改规避版权"的衍生素材。
- ✅ 仅使用上述 CC0 原创资源；风格向动森靠拢，素材 100% 合法。
- 无法确认许可证的资源一律不进入实验工程（当前无一使用）。

## 二次加工说明（2026-11-22 终版回填）

- 下载通道说明：因 OpenGameArt 下载速度过慢（~19KB/s）与 huggingface.co 被代理阻断，实际经 **hf-mirror.com 镜像**下载 HuggingFace 数据集 `codepawl/quaternius-glb`（Quaternius CC0 模型的 GLB 转存，engine 层无 meshopt）。CC0 允许转存，许可属性不变；原包页面（quaternius.com/OpenGameArt）均为 CC0 标注。Grass3/Rock3 两个变体因镜像端持续返回空而放弃，用 Rock1/2、Grass1/2 替代，不影响验收。
- **Blender**：process_glb.py 批处理（落地/缩放/HSV 暖化）验证可用；House1 暖化版因 GLB `KHR_materials_unlit` 在 Blender 重导出后丢失导致过曝，**未被采用**。
- **Godot 运行时材质覆盖（最终采用）**：树叶 → `#6FAE4E`/`#4E8B3A` 两档绿 + `#F2A0B5` 桃花粉（2 棵）；房屋 Grey(屋顶/门/门廊)→`#C96846` 陶瓦、White(墙)→`#EED9A8` 暖奶油、DarkGrey(窗框)→`#6B4A32` 暖棕。原始 GLB 文件零改动。
- 石板路件 Y 向压扁至 0.25；栅栏 ×3.2；太湖石假山由 Rock1 非均匀缩放（XZ 0.38 / Y 0.95）实现；石灯笼由 Rock1/Rock2 堆叠 + 自发光立方 + OmniLight 组合，均为场景级组合，不改模型文件。
