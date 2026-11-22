# 《桃花源物语》小镇样板 · 第二轮视觉精修报告

基线：`e35a5fd`（第一轮样板）→ 本轮仅改独立 ArtLab `town_sample/`，未动正式工程/资产，3.6 阶段二维持暂停。
引擎：Godot 4.7.2 · gl_compatibility · 1280×720 · 45° 正交斜俯视游戏镜头。建模：Blender 4.5。

## 一、任务优先级与完成状态

| 优先级 | 目标 | 状态 | 关键证据 |
|---|---|---|---|
| P0 | 地面不再单一绿色平板 | ✅ | 程序化噪声纹理 `grass_noise.png`（256² 无缝、三色柔和色阶、uv1_scale 2.2），全景/四向可见柔和明暗层次 |
| P0 | 池塘不再像蓝色几何平面 | ✅ | 定制 `custom_pond.glb`：不规则岸线 + 三圈顶点色深浅水 + 岸边石/草/花簇状过渡 + 放大鸭子；特写可见蓝青渐变 |
| P1 | 建筑四向光照温暖统一 | ✅ | 暖环境光 + 暖粉补光（随镜头 yaw 同步）+ 能量守恒；背光面由灰褐改善为暖米色，保留层次 |
| P1 | NPC 更可爱（尤其小牛） | ✅ | 小牛重做为二头身团子（760 面）；三只眼/高光/腮红统一；兔狐面部同步放大 |
| P1 | s0 阴影条纹 | ✅ | 定位为平面自阴影 acne（非 Z-fighting），关闭地面/土路 cast_shadow 后消失，树影保留 |

## 二、精修前后对比（游戏镜头，非模型排列）

- **全景前后**：`project/evidence/refine_before_after.png`（左=精修前 e35a5fd，右=精修后；本版重排为左右等尺寸并排，去除了旧版大面积空白）。
- **池塘前后**：`project/evidence/pond_before_after.png`（左=前，右=后）。
- 所有对比均为真实游戏镜头同场景机位，不用单体排列图代替展示效果。

## 三、验收截图清单（精修后）
- 完整样板：`project/evidence/town_full.png`
- 四向：`project/evidence/town_s0.png`、`town_s90.png`、`town_s180.png`、`town_s270.png`
- 地面/池塘特写：`project/evidence/combo_pond_path.png`
- 房屋正面/背光面/细节：`project/evidence/house_front_a.png`、`house_front_b.png`、`house_detail.png`
- 商店：`project/evidence/shop_front.png`
- NPC 正面/侧面/动作：`project/evidence/npc_{rabbit,fox,calf}_{front,side}.png`、`project/evidence/npc_action.png`
- 组合：`project/evidence/combo_shop_furniture.png`

### 逐项目检结论
1. **地面**：由单色平板变为大块柔和明暗过渡，无密集网纹、无荧光色；房屋/路/树周围有草簇过渡。仍非照片级草地纹理，但符合低模卡通风格。
2. **池塘**：不规则蓝青水体（外浅内深）、岸边石草花过渡、睡莲绿色、鸭子可辨；不再是孤立蓝色几何平面。
3. **四向**：建筑/商店无裁切、无严重遮挡；池塘道路庭院各方向完整；无穿地/悬空/比例异常。s0 前景树附近的条纹已消失（见上表排查）。
4. **建筑光照**：四向稳定，背光面暖米色不发灰，阴影柔和，无整体过曝。
5. **NPC**：三只风格统一、面部在近景镜头清晰；小牛明显更可爱。
6. **仍存在的可接受瑕疵**：建筑背光面在 s90/s180 全景远距离仍略暗于正面（已非灰褐，属正常明暗层次）；小牛近景额头略偏白（全景镜头不明显）；地面为程序化噪声而非手绘草地，细节密度低于参考作品；不宣称达到《动物森友会》最终品质。

## 四、性能（桌面 / Android 分开）
- **离线结构**：静态 **146,243** 三角面（红线 150k ✅）；DrawCalls 离线估算 **77**（红线 100 ✅）；唯一材质 48；Skeleton 0 / 骨骼 0 / AnimationPlayer 0；MultiMesh 3 组 + 12 组合批。
- **桌面实测**（gl_compatibility，1280×720，4 组 × 30 样本）：baseline / shadow_off / anim_paused / veg_hidden 帧时间中位均约 **6.90 ms（145 FPS）**。开关差值方向仍不呈预期（vsync/后台抖动），本次采样 VRAM 计数返回 0（该环境下不可用），**不以桌面数据推断手机合格**。
- **Android 真机**：未实测（本机无 adb / SDK / 设备）。工程 `-- --perf` 采集已就绪，按 PERF_SPEC_V1 §2.1 用户侧补测后判定。
- 本轮新增几何（池塘 160 面、岸边与路边草簇）已通过削减冗余草簇把面数压回红线内，未增加骨骼/材质数量。

## 五、技术留痕（关键 bug）
1. 自制池塘法线朝下 → Godot 背面剔除致水面不可见 → `mesh.flip_normals()` 修正。
2. 水面叠加近白波纹纹理会把顶点色洗成草地色 → 最终仅用顶点色深浅渐变。
3. shadow_bias 调大（0.5）会丢失阴影并产生地面扫描线 → 正确解法是关闭大面积平面自阴影 `cast_shadow`。
4. 草地噪声原 6 波叠加过密呈"网纹" → 降为 4 波 + uv1_scale 3.2→2.2，过度柔和。
5. 渲染后过曝发白 → 主光 0.85→0.70、环境光 0.46→0.34、色阶收窄。

## 六、执行边界
未修改正式游戏工程、未替换正式资产、未恢复 3.6、未批量导入剩余候选、未重写资产导入管线；所有改动在独立 ArtLab `town_sample/`。Gemini 未看截图、未声称视觉审查。交 GPT 第二轮终审；若仍不理想将如实指出，不为提交而宣称达标。

## 七、最终交付修正（针对 4967bc7 的审查意见）
1. **资源路径统一（最高优先级）**：Godot 工程入口 `project/project.godot` 保持不变；40 件 GLB 与 2 张程序化纹理全部移入 `project/assets/`，运行产物移入 `project/evidence/`。`main.gd` 的全部 `res://` 路径均已在工程内逐一核对存在；草地纹理增加 `MISSING` 显式报错，MultiMesh 加载增加空指针保护。`build_custom_assets.py` / `build_refine_assets.py` / `gen_textures.py` / `pack_blend_source.py` 输出全部改到 `project/assets/`。删除仓库根 `assets/` 与根 `evidence/` 副本，无软链接、无外部路径、无未提交依赖。
2. **视觉复查**：`s0` 与 `combo_pond_path` 在 1280×720 实际游戏镜头下重新目检，并对行亮度做高通后周期自相关检查（峰值 ≤0.008），未见平行条纹残留；仅有树冠产生的不规则柔和阴影。草地噪声在该距离呈低频柔和明暗层次，可读、无网纹、无摩尔纹。
3. **前后对比图重排**：`refine_before_after.png` 与 `pond_before_after.png` 统一改为左右等尺寸并排 + 顶部标题条，删除旧版大面积空白，前后两图完整显示。
4. **性能边界不变**：未新增模型或几何细节；统计仍为 146,243 静态三角面 / DC 估算 77 / 38 种模型 / 0 骨骼。Android 仍未实测，继续如实标注；正式工程接入需为 NPC、作物、交互物与动态场景预留预算。
5. **干净环境验证**：见 `docs/CLEAN_CLONE_VERIFICATION.md`（从 GitHub 提交后重新克隆、按 README 启动、重出四向截图的实测记录）。
6. **执行边界**：仅改独立 ArtLab `town_sample/`；未修改正式游戏工程、未替换正式资产、未恢复 3.6 阶段二。
