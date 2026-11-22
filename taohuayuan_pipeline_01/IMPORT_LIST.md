# 实际导入模型清单（pipeline_01 → Godot 4.7.2）· 验收修订版 v2

生成口径：`godot_scene/scripts/main.gd::_run_lint()` 全表面索引三角面清点 + `scripts/audit.gd` 逐模型骨架/动画复核，数据落盘于 `evidence/asset_budget.json` 与 `evidence/godot_audit.json`。

## 0. 统计口径（本次修订重点）
| 口径 | 数值 | 含义 |
|---|---|---|
| 50 件处理后模型合计 | **40,805 三角面** | 每模型只算一次（唯一网格），= Blender `normalize_report.json` 汇总 = Godot 全表面索引三角面汇总 |
| 入场景模型种类 | **47 种**（Polyfork 39 + Poly Pizza 8） | 实际进入展示场景的模型文件 |
| 仅导入/归一化未摆放 | **3 件**（Polyfork） | log-plank-bridge、round-path-stone、stone-fire-pit |
| 场景中模型实例 | **224 个**（含 4 组 MultiMesh 的 148 个实例） | 76 个独立实例 + 4 组 MultiMesh + 2 块地面 |
| 场景静态三角面 | **119,294** | 按实例累计（224 实例 = 119,290）+ 2 块 PlaneMesh（4 面） |
| 摆放模型唯一网格面数 | 39,689 | 47 种入场景模型各算一次 |
| DrawCalls 估算（无剔除） | **123** | 按实际 MeshInstance3D/surface 节点清点，含 MultiMesh 4 组；超 PERF_SPEC 红线 100，见 PERF_STATS |

**旧稿错误更正**：旧稿「33,232 面」= 仅取每个模型 surface 0 的顶点数 ÷3，既漏掉多 surface 模型，又把顶点数当三角面数；既有别于 40,805 的唯一网格口径，也不是场景实际三角面。旧稿「45 种」漏计 grass-tuft / wildflower 两个 MultiMesh 模型种类，实际为 47 种。旧稿「42 件 Polyfork 均为备选」为表格填写错误——39 件已经进入场景，只有 3 件仅完成导入归一化。

## 1. 逐件清单（面数=处理后唯一网格三角面；摆位=场景实例数）
| # | 文件 | 来源 | 面数 | Surface | Skeleton3D/骨骼 | 动画数 | 场景状态 | 实例数 |
|---|---|---|---:|---:|---|---:|---|---:|
| 1 | birch-tree-181b33.glb | Polyfork | 619 | 1 | — | 0 | 入场景 | 3 |
| 2 | birdhouse-post-66d6c1.glb | Polyfork | 393 | 1 | — | 0 | 入场景 | 1 |
| 3 | black-bear-adbdc7.glb | Polyfork | 2542 | 1 | 1 / 26 | 3 | 入场景 | 1 |
| 4 | broadleaf-oak-997c22.glb | Polyfork | 457 | 1 | — | 0 | 入场景 | 3 |
| 5 | campsite-picnic-table-361d51.glb | Polyfork | 572 | 1 | — | 0 | 入场景 | 1 |
| 6 | cattail-reed-6abbb3.glb | Polyfork | 388 | 1 | — | 0 | 入场景 | 5 |
| 7 | dirt-trail-strip-1be7a6.glb | Polyfork | 112 | 1 | — | 0 | 入场景 | 3 |
| 8 | dock-platform-section-b36e7c.glb | Polyfork | 356 | 1 | — | 0 | 入场景 | 1 |
| 9 | fallen-log-1685fb.glb | Polyfork | 484 | 1 | — | 0 | 入场景 | 1 |
| 10 | fern-plant-1559b8.glb | Polyfork | 802 | 1 | — | 0 | 入场景 | 19 |
| 11 | firewood-stack-8a2899.glb | Polyfork | 752 | 1 | — | 0 | 入场景 | 1 |
| 12 | forest-deer-fe648d.glb | Polyfork | 2230 | 1 | 1 / 26 | 3 | 入场景 | 2 |
| 13 | forest-rabbit-ea2da0.glb | Polyfork | 2074 | 1 | 1 / 26 | 3 | 入场景 | 3 |
| 14 | grass-tuft-a40a08.glb | Polyfork | 368 | 1 | — | 0 | 入场景（MultiMesh 90） | 90 |
| 15 | lantern-post-f47665.glb | Polyfork | 482 | 1 | — | 0 | 入场景 | 3 |
| 16 | large-boulder-a29b99.glb | Polyfork | 566 | 1 | — | 0 | 入场景 | 1 |
| 17 | lily-pad-86edbb.glb | Polyfork | 398 | 1 | — | 0 | 入场景 | 3 |
| 18 | log-cabin-4fac3b.glb | Polyfork | 1326 | 1 | — | 0 | 入场景（村北仓库，非玩家住宅） | 1 |
| 19 | log-plank-bridge-a5f74f.glb | Polyfork | 480 | 1 | — | 0 | **仅导入+归一化，未摆放** | 0 |
| 20 | maple-tree-65fa12.glb | Polyfork | 422 | 1 | — | 0 | 入场景 | 2 |
| 21 | medium-rock-e08405.glb | Polyfork | 374 | 1 | — | 0 | 入场景 | 2 |
| 22 | open-woodshed-050a0a.glb | Polyfork | 1250 | 1 | — | 0 | 入场景（柴房） | 1 |
| 23 | red-fox-5c3bc0.glb | Polyfork | 2280 | 1 | 1 / 26 | 3 | 入场景 | 1 |
| 24 | rock-spire-13819c.glb | Polyfork | 378 | 1 | — | 0 | 入场景 | 1 |
| 25 | round-bush-cd2ac0.glb | Polyfork | 573 | 1 | — | 0 | 入场景 | 3 |
| 26 | round-path-stone-4130f3.glb | Polyfork | 52 | 1 | — | 0 | **仅导入+归一化，未摆放** | 0 |
| 27 | slab-path-stone-e526f7.glb | Polyfork | 76 | 1 | — | 0 | 入场景 | 6 |
| 28 | small-rock-db33a7.glb | Polyfork | 202 | 1 | — | 0 | 入场景 | 2 |
| 29 | stone-fire-pit-4136b0.glb | Polyfork | 584 | 1 | — | 0 | **仅导入+归一化，未摆放** | 0 |
| 30 | stone-well-2b4717.glb | Polyfork | 608 | 1 | — | 0 | 入场景 | 1 |
| 31 | tall-pine-tree-ab4108.glb | Polyfork | 350 | 1 | — | 0 | 入场景 | 2 |
| 32 | tree-stump-ec3f48.glb | Polyfork | 505 | 1 | — | 0 | 入场景 | 1 |
| 33 | water-blob-f266b8.glb | Polyfork | 320 | 1 | — | 0 | 入场景 | 1 |
| 34 | wildflower-68d3a1.glb | Polyfork | 405 | 1 | — | 0 | 入场景（MultiMesh 22） | 22 |
| 35 | wooden-barrel-ab50ca.glb | Polyfork | 540 | 1 | — | 0 | 入场景 | 1 |
| 36 | wooden-bench-02e2c8.glb | Polyfork | 564 | 1 | — | 0 | 入场景 | 1 |
| 37 | wooden-canoe-1d00c5.glb | Polyfork | 1020 | 1 | — | 0 | 入场景 | 1 |
| 38 | wooden-fence-gate-a8735f.glb | Polyfork | 408 | 1 | — | 0 | 入场景 | 1 |
| 39 | wooden-fence-section-5f04b7.glb | Polyfork | 428 | 1 | — | 0 | 入场景（MultiMesh 18） | 18 |
| 40 | wooden-hand-cart-3ae5b5.glb | Polyfork | 1416 | 1 | — | 0 | 入场景 | 1 |
| 41 | wooden-rowboat-916981.glb | Polyfork | 1262 | 1 | — | 0 | 入场景 | 1 |
| 42 | young-pine-0d7695.glb | Polyfork | 270 | 1 | — | 0 | 入场景 | 3 |
| 43 | pp_1YE8U35HXsI.glb | PolyPizza | 648 | 5 | — | 0 | 入场景（白鸡×2） | 2 |
| 44 | pp_26zM1outCr.glb | PolyPizza | 2450 | 7 | 1 / 42 | 25 | 入场景（黄牛） | 1 |
| 45 | pp_2KHEgw1ztVI.glb | PolyPizza | 504 | 7 | — | 0 | 入场景（绿头鸭×2） | 2 |
| 46 | pp_5gZfOZIW92k.glb | PolyPizza | 432 | 1 | — | 0 | 入场景（石灯笼×1，仅点缀） | 1 |
| 47 | pp_C39AUXUUes.glb | PolyPizza | 610 | 2 | 1 / 24 | 2 | 入场景（绵羊） | 1 |
| 48 | pp_gYYC0gYMnw.glb | PolyPizza | 1204 | 1 | — | 0 | 入场景（鸟） | 1 |
| 49 | pp_rgJXF570ZK.glb | PolyPizza | 2528 | 1 | 1 / 16 | 8 | 入场景（绵羊变体） | 1 |
| 50 | pp_u35l6uP5vj.glb | PolyPizza | 2741 | 1 | 1 / 13 | 8 | 入场景（猪） | 1 |

## 2. 骨骼与动画汇总（与 PERF_STATS / asset_budget 一致）
- Skeleton3D：**8 个**（熊/鹿/兔/狐各 1；黄牛/绵羊×2/猪各 1）；骨骼总数 **199**（26×4 + 42 + 24 + 16 + 13）。
- AnimationPlayer：**8 个**；AnimationLibrary：**8 个**；动画资源共 **55 条**（3×4 + 25 + 2 + 8 + 8）。
- 非骨骼动画：**0**。GLB 元数据逐通道核对：所有动画通道 target node 均落在对应 skin joints 内，无对象级位移动画。
- 性能测试：baseline/shadow_off/veg_hidden 组播放 8 个 AnimationPlayer 的第 1 条动画并设 `LOOP_LINEAR`；anim_paused 组将 8 个播放器 `active=false`。

## 3. 验证
- 全部 50 件通过 Godot 4.7.2 headless `--import`（0 错误）+ 场景实例化渲染；lint PASS（石灯笼 1 ≤3、秋色树 2 ≤3、metallic 0）。
- 统计脚本新增：`scripts/audit.gd` + `scenes/Audit.tscn`；证据：`evidence/godot_audit.json`、`evidence/asset_budget.json`。
