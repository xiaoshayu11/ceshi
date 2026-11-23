# ENV-2① 农场主屋 GLB 整合·实际运行视觉验收材料

> 2026-11-23 · 供 GPT 验收。工程：Godot 4.7.2《桃花源物语》私有仓（本轮 commit `72e2a3f` + `79b0bcf`）。
> 所有截图来自**正式游戏场景 + 正式生产链路**（`GameState.house.level` → `GameplayRoot._rebuild_house()` → `HouseBuilder` GLB 路径），
> 非手动摆模型；游戏同款相机（正交 + pitch 52°）。测试一律 `--no-autosave`（SAVE-GUARD 沙盒隔离生产档）。

## 一、验收中发现并修复的缺陷（重要）

**GLB 门朝向反转**：首轮四向截图发现 L1 门+台阶出现在南侧（+Z），北侧（玩家来向/门口交互件 z=15.6/院门 z=15 一线）看到的是带单窗的背面。
根因：glTF 导入朝向坑（Blender -Y 前方 → glTF +Z → Godot +Z）。且原 Door_Blocker 封的是北侧实墙，L2 真实 2.4×3.0 门洞在南侧裸露（空壳屋风险）。

修复：整合层整体 `rotation.y = PI`（**MODEL-1 模型本体零改动**，贴地 y=0 不变）→ 门朝 -Z，与 Door_Blocker（z=-3.0/-3.4）、门口交互、院门方向全部对齐。
副作用：L2 耳房东→西（刚性旋转无法既转门又保耳房；模型内门/耳房相对关系与定型渲染一致；耳房在 ±X 均不遮正门）。
连带适配（纯装饰）：石头、木箱两件挪出旋转后西翼占地；草点排除区主屋矩形适配。

## 二、截图清单（screenshots/，23 张）

### 三档四向（0°/90°/180°/270°，yaw 180 从北侧看正面门）
- `acc_L{0,1,2}_view{0,90,180,270}.png`（12 张）

### 细节与组合
- `acc_L{0,1,2}_front_detail.png`：正面特写（L1 双开木门+门楣+门灯+石阶；L2 门楼+红灯笼+格窗）
- `acc_L{0,1,2}_roof_detail.png`：屋顶特写（L0 秃斑茅草 / L1 青瓦+烟囱 / L2 双坡+耳房）
- `acc_L{0,1,2}_surround.png`：房屋与草地/道路/围栏组合

### 屋顶 OcclusionFader 淡出/恢复（L1 实心屋顶，玩家真实移动驱动）
- `acc_fade_near_roof_alpha.png`：玩家贴北面墙外 → 屋顶淡化至 alpha≈0.22（近乎全透，可见玩家）
- `acc_fade_far_roof_restored.png`：玩家走远 → 屋顶恢复不透明蓝灰瓦（alpha=1.00）

## 三、行为验收结果（test_env2_house，29 断言全绿，全文见 test_env2_house.gd.txt）

| 组 | 内容 | 结果 |
|---|---|---|
| A | GLB 三组 Mesh 分工：Wall_All→layer1 trimesh 挡射线 / Roof_All→layer4 遮挡 / Decor_All 零碰撞 | 3 档 15/15 PASS |
| B | 空壳屋钻不入：真实玩家从 N/S/E/W 四向外墙持续推进 75 物理帧 | 3 档泄漏 0/12 |
| C | 绕屋通行：L2 最大占地在院区内绕圈 5 段全部抵达（南腿走围栏↔门洞封堵体间真实走廊 z=15.8） | PASS |
| D | L2 门楼/围栏：门楼柱区无非屋体 layer1 碰撞体；屋体不越 z=15 围栏线；围栏 x=0 缺口（农场内路动线）可通行 | PASS |
| E | 升级档位一致：_rebuild_house 后 House_L{n}_Root + house_level meta + GLB Roof_Body 结构 | 3 档 PASS |
| F | 屋顶淡出/恢复：真实 OcclusionFader + 真实玩家，靠近 alpha=0.22 / 走远 alpha=1.00 | PASS |

按 F 进屋流程（门口交互 → 场景切换 → 室内）由既有回归覆盖：test_house_scene D12/D12b（85 断言全绿）。

## 四、回归与存档安全

- 全量回归：**40 套件 1316 断言 0 FAIL / 0 SCRIPT ERROR**（自动发现含本轮新增套件）
- 生产档污染检查：回归全程 save_v2.json **MD5 与 mtime 前后零变化**（空窗法）
- SAVE-GUARD 拦截 3 次，目标全部为沙盒路径
- 隔离验证：三档外观截图全部在 `--no-autosave` 测试进程中以 `GameState.house.level` 显式设档拍摄，未使用生产存档

## 五、私有仓 commit

- `72e2a3f`：GLB 接入 HouseBuilder（碰撞/遮挡/门洞封堵）+ OcclusionFader 逐表面材质淡出
- `79b0bcf`：验收轮——门朝向修复（180°Y 旋转）+ 行为验收套件 + 装饰物挪位 + 验收截图

## 六、遗留说明（供决策，非阻塞）

- L2 耳房现位于**西侧**（旋转副作用）。若需恢复东侧需镜像模型（会翻绕面），或接受现状。耳房在 ±X 均不遮正门，西侧现为空地无冲突。
- 镇 8 栋建筑（5 商业伞盖屋顶 + 3 住宅灰盒）为 ENV-2② 范围，本轮按边界未动。
