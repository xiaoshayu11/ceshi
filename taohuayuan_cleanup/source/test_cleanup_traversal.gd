extends Node

## ENV-CLEANUP 全场景通行性 + 门口专项 + 遗留物回归（第 42 套件）。
## 覆盖：
##   A. 三档门口正面/左前/右前到达交互圈（不能卡在围栏/门板/旧碰撞）
##   B. 交互管理器识别 HouseDoor + 驱动 F 进屋（SceneRouter 到 house 场景）
##   C. 农田道路/桥/池塘/NPC 站位通行（农场 + 镇区）
##   D. 店门通行（杂货铺 GLB 门口可进，不被柜台木箱挡）
##   E. 遗留物回归：不得再有 6×4 方形 BoxMesh 过渡草斑（ENV-1 清理锁定）
##   F. 门口区域不得出现独立木板/箱子 StaticBody（只允许围栏/墙/blocker）
## 加 -- --no-autosave，生产档物理隔离。

const HOUSE := Vector3(-9, 0, 20)
const INTERACT := Vector3(-9, 0.1, 15.6)
const SHOP := Vector3(9, 0, -3)

var _pass := 0
var _fail := 0

func check(cond: bool, msg: String) -> void:
	if cond:
		_pass += 1
		print("  [PASS] " + msg)
	else:
		_fail += 1
		printerr("  [FAIL] " + msg)

func _ready() -> void:
	GameState.autosave_enabled = false
	var args := OS.get_cmdline_user_args()
	if not args.has("town_only"):
		await _farm_suite()
	await _town_suite()
	print("结果：PASS=%d FAIL=%d" % [_pass, _fail])
	get_tree().quit(1 if _fail > 0 else 0)

func _pf(n: int) -> void:
	for i in range(n):
		await get_tree().physics_frame

func _drive_to(player: CharacterBody3D, to: Vector3, timeout := 300, lock_y := -1.0) -> bool:
	for i in range(timeout):
		var d := to - player.global_position
		d.y = 0.0
		if d.length() < 0.9:
			return true
		player.velocity = d.normalized() * 8.0
		player.move_and_slide()
		if lock_y >= 0.0:
			player.global_position.y = lock_y
		await get_tree().physics_frame
	return Vector2(to.x - player.global_position.x, to.z - player.global_position.z).length() < 0.9

# -------------------------------------------------- 农场
func _farm_suite() -> void:
	print("-- 农场：门口通行/F交互/遗留物 --")
	var world: Node = (load("res://scenes/world/World.tscn") as PackedScene).instantiate()
	add_child(world)
	await _pf(6)
	var gr := world.get_node("GameplayRoot")
	var player := get_tree().get_first_node_in_group("player") as CharacterBody3D
	check(player != null and gr != null, "World 场景玩家与 GameplayRoot 存在")
	if player == null or gr == null:
		return
	player.set_physics_process(false)

	# E：遗留方形草斑清零（只允许道路薄片，其 parent 为 Road*）
	var flat_bad: Array[String] = []
	for n in world.find_children("*", "MeshInstance3D", true, false):
		var mi := n as MeshInstance3D
		if mi == null or mi.mesh == null or not (mi.mesh is BoxMesh):
			continue
		var sz: Vector3 = (mi.mesh as BoxMesh).size
		if sz.y <= 0.1 and is_equal_approx(sz.x, 6.0) and is_equal_approx(sz.z, 4.0):
			flat_bad.append("%s@%s" % [n.name, mi.global_position])
	check(flat_bad.is_empty(), "农场无 6×4 方形过渡草斑遗留（发现 %d 块：%s）" % [flat_bad.size(), flat_bad])

	# A/F：三档门口
	for lv in [0, 1, 2]:
		GameState.house.level = int(lv)
		gr.call("_rebuild_house")
		await _pf(5)
		var routes := [
			{"tag": "正面", "p": Vector3(-9, 0.1, 12.5)},
			{"tag": "左前", "p": Vector3(-14.5, 0.1, 13.5)},
			{"tag": "右前", "p": Vector3(-3.5, 0.1, 13.5)},
		]
		for r in routes:
			player.global_position = r["p"]
			player.velocity = Vector3.ZERO
			await _pf(3)
			var reached := false
			for i in range(300):
				var d := INTERACT - player.global_position
				d.y = 0.0
				if d.length() < 1.35:
					reached = true
					break
				player.velocity = d.normalized() * 8.0
				player.move_and_slide()
				await get_tree().physics_frame
			check(reached, "L%d 从%s靠近门口可达交互圈（终点 %s）" % [int(lv), r["tag"], player.global_position])
		# F：门口区非屋体/非围栏的 layer1 障碍清零
		var shape := BoxShape3D.new()
		shape.size = Vector3(7.0, 1.7, 5.0)
		var q := PhysicsShapeQueryParameters3D.new()
		q.shape = shape
		q.transform = Transform3D(Basis(), Vector3(-9, 1.15, 16.6))
		q.collision_mask = 1
		var foreign: Array[String] = []
		for h in get_viewport().world_3d.direct_space_state.intersect_shape(q, 32):
			var c := h.get("collider") as Node
			if c == null:
				continue
			var path := String(c.get_path())
			if path.contains("House_L") or path.contains("FenceBody"):
				continue
			foreign.append(c.name)
		check(foreign.is_empty(), "L%d 门口区无独立木板/箱子等异物碰撞（%s）" % [int(lv), foreign])

	# B：F 进屋（L1/L2；L0 设计上提示不能住）
	GameState.house.level = 1
	gr.call("_rebuild_house")
	await _pf(5)
	var mgr := get_tree().get_first_node_in_group("interaction_manager") as InteractionManager
	check(mgr != null, "交互管理器存在")
	player.global_position = INTERACT
	await _pf(6)
	# 交互刷新在 _process（每帧），等若干 process frame
	for i in range(6):
		await get_tree().process_frame
	var cur := mgr.get_current() if mgr != null else null
	check(cur is HouseDoorInteractable, "门口交互管理器当前对象为 HouseDoor（提示「%s」）" % mgr.get_current_prompt())
	# 真实触发 F：直接调 on_interact 等价于 InputManager._try_interact 分发
	if cur is HouseDoorInteractable:
		cur.call("on_interact")
		for i in range(90):
			await get_tree().process_frame
		var scene_now := get_tree().current_scene
		var ok := scene_now != null and String(scene_now.scene_file_path).contains("HouseInterior")
		check(ok, "F 交互成功切换到室内场景（实际=%s）" % (scene_now.scene_file_path if scene_now != null else "null"))
		# 还原：直接释放刚切进来的室内场景并恢复 current_scene 指向测试壳。
		# 不调用 SceneRouter.change_scene("farm")——那会额外新建一个 World 与
		# 本套件手动 add_child 的 world 重叠，导致后续镇区套件 Ground 互相穿插卡住玩家。
		if scene_now != null and ok:
			get_tree().current_scene = self
			scene_now.queue_free()
			for i in range(6):
				await get_tree().process_frame
	player.set_physics_process(true)
	world.queue_free()
	await _pf(4)

# -------------------------------------------------- 镇区
func _town_suite() -> void:
	print("-- 镇区：店门通行/道路/遗留物 --")
	var town: Node = (load("res://scenes/world/Town.tscn") as PackedScene).instantiate()
	add_child(town)
	await _pf(6)
	var player := get_tree().get_first_node_in_group("player") as CharacterBody3D
	check(player != null, "镇区玩家存在")
	if player == null:
		return
	player.set_physics_process(false)
	# E：方形草斑清零
	var bad: Array[String] = []
	for n in town.find_children("*", "MeshInstance3D", true, false):
		var mi := n as MeshInstance3D
		if mi == null or mi.mesh == null or not (mi.mesh is BoxMesh):
			continue
		var sz: Vector3 = (mi.mesh as BoxMesh).size
		if sz.y <= 0.1 and is_equal_approx(sz.x, 6.0) and is_equal_approx(sz.z, 4.0):
			bad.append("%s@%s" % [n.name, mi.global_position])
	check(bad.is_empty(), "镇区无 6×4 方形过渡草斑遗留（发现 %d 块：%s）" % [bad.size(), bad])
	# C/D：镇区主动线 + 店门（广场→杂货铺门口→主街→北桥→南口）
	var route := [
		Vector3(0, 0.1, 4), Vector3(5.0, 0.1, -3), Vector3(0, 0.1, 0),
		Vector3(0, 0.1, -20), Vector3(0, 0.1, 24),
	]
	player.global_position = route[0]
	await _pf(3)
	var all_ok := true
	for i in range(1, route.size()):
		# 镇区广场石板盘顶 y≈0.13、玩家胶囊半径 0.35：驱动时固定 y=0.6
		# 避免胶囊底部陷入地形接触面导致 move_and_slide 沿圆盘边缘卡滞。
		var reached := await _drive_to(player, route[i], 400, 0.6)
		if not reached:
			all_ok = false
			printerr("      镇区动线卡死于 leg %d 终点=%s" % [i, player.global_position])
	check(all_ok, "镇区主动线 4 段（店门/广场/北桥/南口）全部抵达")
	# D：杂货铺门洞可进（从 rot -PI/2 后的门侧 x≈5 推进到室内）
	player.global_position = Vector3(5.0, 0.6, -3)
	await _pf(3)
	var entered := await _drive_to(player, Vector3(9.0, 0.6, -3), 240, 0.6)
	check(entered, "杂货铺门口柜台木箱不阻挡进店（终点 %s）" % player.global_position)
	player.set_physics_process(true)
	town.queue_free()
	await _pf(4)
