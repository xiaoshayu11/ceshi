# 《桃花源物语》ENV-CLEANUP 正式场景历史遗留物清理与通行验收

> P0 任务｜2026-11-23｜私有仓 commit `ce15ae4`｜42 套件 1355 断言 0 FAIL｜生产档 MD5+mtime 零污染

## 一、门口木板专项溯源（最高优先级）

用户反馈「农场主屋门口出现木板，可能阻挡通行」。逐档溯源结论：

| 检查项 | 结论 |
|---|---|
| 来源 | **MODEL-1 L0 GLB 内部设计装饰**：`L0_Wall_DoorL/DoorR` 破门板（贴墙立面 y≈0.4–2.3m）、窗板（`_WinBoard1/2` 钉在窗上）、`Decor_DangerSign` 危屋木牌、`Decor_BrokenBarrel` 破桶 |
| 旧程序化 HouseBuilder | 未生成（GLB 优先路径加载成功） |
| 独立木板/箱子节点 | 无。门口区 Mesh 只有围栏段 + GLB 三件（Wall_All/Roof_All/Decor_All） |
| 旧 CollisionShape / StaticBody | 无。门口区碰撞仅 FenceBody×4 / Wall_Body / Door_Blocker（L0 无 blocker 属设计） |
| 与 Door_Blocker / 交互区重叠 | 否。交互区在 (-9,0.1,15.6)，blocker 在门洞 z≈-3.0/-3.4 |
| 三档三路到达交互圈 | **全通过**：L0/L1/L2 × 正面/左前/右前，距交互点 1.23–1.33m < 半径 1.4m |
| 按 F 进屋 | **实测通过**：InteractionManager 识别 HouseDoor → SceneRouter 切至 HouseInterior |

**处理**：L0 破败木板为已验收 MODEL-1 定型设计，贴墙且零独立碰撞，不妨碍通行与进屋 → 保留原样。L1/L2 无多余木板或旧残留。

## 二、清理对象（ENV-1 遗留方片）

| 位置 | 对象 | 处理 |
|---|---|---|
| 农场北口 z=-23.9/-26.1/-28.3 | 4 块 6×0.05×4 方形 BoxMesh 草斑 | 删除，改 `GroundTint.organic_patches` 有机 Blob |
| 镇区南口 z=24.8/27.0/29.2 | 2 块同类方片 | 同上 |

首版替换后出现「孤立大圆靶」观感（半径 2.6–2.9m），经美术总监定稿收敛：半径 -50%（1.2–1.4m）、中心从离路 6m 拉到 3.8–4.2m 贴路缘、每侧拆 3 块沿 z 渐变带。最小内缘 2.11m > 路缘带 1.92m，不压路面；6 spots×4 瓣仍是单 MultiMesh，Mesh 预算零增量。

## 三、保留对象（按规则分类，未误删）

- 围栏 FenceBody（z=15 院区边界 + 东侧封口）、Wall_Body、Door_Blocker、WaterWall、桥、池塘挡墙、NPC 交互体
- 商店门口柜台/木箱/桶 = ShopUmbrella GLB 的 `Decor_*`，零碰撞，兔大妈摊位配套
- 石头/木箱/野花/草丛/蘑菇/长椅：PH3 审计后有意布局，已避开道路与主屋
- 喷泉/石板圆盘/路灯/采集占位/NPC 站位脚垫：镇区广场与玩法预留
- 农田/种植网格/道路碰撞：玩法核心零改动

## 四、验证结果

- **新增第 42 套件 `test_cleanup_traversal` 21/21 断言**：三档门口三路通行、门口异物碰撞清零、F 进屋、草斑清零锁定、镇区主动线 4 段、店门通行
- **全量回归 42 套件 / 1355 断言 / 0 FAIL / 0 SCRIPT ERROR**
- 生产档 MD5 `42753db4…` 与 mtime 前后完全一致；SAVE-GUARD 3 次拦截全沙盒路径
- 38 张正式镜头对比图：before 17 + after 17 + F 进屋实测 4

## 五、关键截图索引

| 内容 | 路径（相对本目录） |
|---|---|
| 门口木板 before（L0） | `screenshots/before/house_L0_entrance.png` |
| 农场北口草斑 before / after | `screenshots/before/farm_north_patches.png` / `screenshots/after/farm_north_patches.png` |
| 镇区南口 before / after | `screenshots/before/town_south_patches.png` / `screenshots/after/town_south_patches.png` |
| 农场全景 before / after | `screenshots/before/farm_yaw0.png` / `screenshots/after/farm_yaw0.png` |
| 镇区全景 before / after | `screenshots/before/town_yaw180.png` / `screenshots/after/town_yaw180.png` |
| **玩家门口 + F 提示实测** | `screenshots/f_enter/01_at_door.png` |
| **按 F 进屋实测** | `screenshots/f_enter/03_inside_house.png` |
| 返回农场实测 | `screenshots/f_enter/04_back_at_door.png` |
| 清理规则与清单 | `docs/场景清理规则与清单.md` |
| 通行性测试源码 | `source/test_cleanup_traversal.gd` |

## 六、执行边界遵守

未改 MODEL-1 房屋主体、未重做 ENV-1 地面系统、未增大规模模型、未改种植/商店/任务/NPC 玩法、未删必要碰撞/遮挡/交互节点、未做家具、未启动剩余 7 栋建筑。

## 七、下一步

等待 GPT 对清理结果与通行实测的视觉验收；通过后恢复 ENV-2② 剩余建筑批量制作。
