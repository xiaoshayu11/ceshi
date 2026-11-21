# 《桃花源物语》独立美术资源实验报告 v1.0

> 日期：2026-11-22 · 执行：WorkBuddy（主开发） · 协作：Gemini（模式 D 双 AI 协作） · 待用户/GPT 审查
> 工程位置：本地独立目录 `WorkBuddy/artlab_taohuayuan/`（**完全独立**，未触碰正式游戏工程任何文件）

## 一、结论先行

实验成立。Quaternius CC0 素材 + 运行时材质重配色 + Gemini 光照/布局方案，可以在独立 Godot 4.7 工程里拼出**明亮、温馨、圆润、动森感成立**的田园场景：陶瓦红顶小屋、粉色桃树、层次化绿树、S 型石板小径、木栅栏、岩石堆叠的中式石灯笼。全场景 **81,746 三角面 / 104 实例 / ~178 FPS**（预算 30 万面，Android 余量充足）。

## 二、资源清单与许可证（详见 RESOURCES_LICENSE.md）

| 包 | 作者 | 许可证 | 用途 |
|---|---|---|---|
| Simple Nature（Tree×4/Bush×3/Grass×2/Rock×2） | Quaternius | CC0（可商用/可改/无需署名） | 树、灌木、草、岩石 |
| Textured Fantasy Nature（Flower×3/Mushroom/BigBush） | Quaternius | CC0 | 花与蘑菇点缀 |
| Medieval Village（Fence/Path×2/Well/Cart/Hay/Crate） | Quaternius | CC0 | 栅栏、石板路、院落道具 |
| Buildings（House1） | Quaternius | CC0 | 主屋 |

- 下载通道：HuggingFace `codepawl/quaternius-glb` 镜像（engine 层，无 meshopt，Godot/Blender 直读）；原包页面 quaternius.com / OpenGameArt 均标注 CC0，镜像转存不改变 CC0 属性。
- 红线执行：**未使用任何动森提取素材**（该请求已明确拒绝）；无许可证存疑资源进入工程。

## 三、技术路线与二次加工

1. **Blender 4.5**（`blender/process_glb.py`、`recolor_mats.py`、`inspect_mats.py`）：
   - process_glb.py：GLB 批量落地/缩放/材质 HSV 暖化（Gemini 交付二被 2600 token 截断，WorkBuddy 审查后补全实现并修复了占位残留）；
   - inspect_mats.py：材质名/底色 dump，支撑重配色决策；
   - recolor_mats.py：按材质名重配色。**发现关键坑**：HF 镜像 GLB 带 `KHR_materials_unlit`，经 Blender 重导出会丢失 unlit 标记 → 强光下过曝发白（第一轮验证失败原因）。故**放弃离线重导出**，改用方案 2。
2. **Godot 运行时材质覆盖**（`artdemo/scripts/main.gd::_override_mats`）：不改原始 GLB，实例化后按材质名（lea/grey/white/darkgrey）做 surface override：
   - 树叶两档绿 `#6FAE4E`/`#4E8B3A` + 桃花粉 `#F2A0B5`（东北角桃树、西南小桃树）；
   - 房屋：Grey(屋顶/门廊/门)→陶瓦 `#C96846`、White(墙体)→暖奶油 `#EED9A8`、DarkGrey(窗框)→暖棕 `#6B4A32`。材质↔部位映射由**显色测试**（洋红/绿/蓝/黄四色一次定位）确认，非猜测。
3. **场景搭建**：程序化摆放（沿用正式项目 FarmGraybox 模式），布局按 Gemini 交付一执行：屋后林抱合、微景观簇（1岩+2灌+3花草）、L 型半围合栅栏、S 型石板动线、四向构图保底。
4. **光照/环境**：Gemini 交付三参数直用——暖阳 DirectionalLight（-50°/-35°，`#FFF4D6`，1.2，正交阴影 45m）+ 纯色天 `#87B6C8` + 冷灰环境光 `#6E85A6` 0.55 + ACES + 关 glow（Android 保守）。
5. **中式点缀**（少量）：岩石堆叠石灯笼（自发光灯室 + Omni 暖光）、瘦高太湖石假山。
6. **相机**：正交 size 12、45° 俯角、135° 主对角视角、四向 90° 旋转（与正式项目一致）。

## 四、验证与性能

- Godot 4.7.2 `gl_compatibility`（GLES3 兼容层，Android 同路径），`--import` 全量导入通过。
- 自动截图管线：6 张/轮（四向 + 房屋特写 + 灯笼特写），落 `evidence/`。
- **81,746 三角面 / 104 实例 / 60 帧平均 5.6ms（≈175 FPS，窗口 vsync 上限）**。
- 已知小瑕疵（如实）：石板路件自带立缘，压扁 0.25 后仍有轻微"路缘石"感；推车自带黑色桶件颜色偏暗；灌木低角度会局部遮挡屋顶（s90）。均不阻塞审查。

## 五、Gemini 协作汇报（模式 D）

1. 任务：独立美术实验布局/脚本/材质。
2. 模式：D（模块协作开发）。
3. 调用：✅ 成功 ×2（`relay-gemini`，`gemini-4-argon`；第 1 次 max_tokens 2600 在交付二中截断，第 2 次补齐交付三）。
4. 传递上下文：任务目标、Godot 4.7.2/GLES3/Android 约束、素材包构成、镜头规格、面数预算、交付格式。
5. Gemini 贡献：①布局方案（完整，采用）；②Blender 脚本（截断，WorkBuddy 补全约 40%）；③材质/光照参数表（完整，采用）。
6. WorkBuddy 审查修改：脚本补全 + 修占位残留；布局微调（桃花树位、灯笼堆叠实现）；**推翻离线重导出**改运行时覆盖（unlit 过曝问题，Gemini 未被告知该镜像特性）。
7. 测试结果：见第四节（全部实测，非 Gemini 声明）。
8. 限制如实声明：**Gemini 未看到任何截图/模型**（MCP 纯文本），其视觉类建议（构图/色板）未经其复审；两轮意见均为文本分析。

## 六、交付物清单

- `artdemo/`：独立 Godot 工程（project.godot / scenes/Main.tscn / scripts/main.gd / assets 26 GLB）
- `blender/`：process_glb.py、recolor_mats.py、inspect_mats.py
- `evidence/`：art_view_s0/s90/s180/s270.png、art_detail_house.png、art_detail_lantern.png、art_report_log.txt
- `RESOURCES_LICENSE.md`：资源与许可证清单
- 本报告

## 七、后续建议（待批准，未动正式工程）

1. 正式项目引入路径：按本报告材质覆盖方案做导入自动化（GLB→场景实例→材质 override 配置表）；
2. 破屋/木屋/瓦房三档可在 House1 基础上用同管线换色+构件组合验证后再进 3.6 正式美术；
3. 若采纳，建议先做一栋"三档房屋外观实验"再回 3.6 阶段二，避免程序化灰盒直接转正。
