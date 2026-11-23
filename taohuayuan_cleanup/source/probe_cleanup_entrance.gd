extends Node

## ENV-CLEANUP 门口专项诊断（只读，不改文件）：逐档扫描主屋门口区域节点/碰撞，
## 真实玩家从正面/左右靠近交互点，检查卡住与多余碰撞体。加 -- --no-autosave。
const SITE := Vector3(-9, 0, 20)
const INTERACT := Vector3(-9, 0.1, 15.6)

func _ready() -> void:
	GameState.autosave_enabled = false
	var world: Node = (load("res://scenes/world/World.tscn") as PackedScene).instantiate()
	add_child(world)
	for i in range(4):
		await get_tree().physics_frame
	var gr := world.get_node("GameplayRoot")
	var player := get_tree().get_first_node_in_group("player") as CharacterBody3D
	if player == null or gr == null:
		printerr("[PROBE] 缺玩家或 GameplayRoot")
		get_tree().quit(1)
		return
	player.set_physics_process(false)

	# 交互件清单
	for n in world.find_children("*", "Interactable", true, false):
		var wp: Vector3 = (n as Node3D).global_position
		if wp.distance_to(INTERACT) < 6.0:
			print("[INTERACT] name=%s pos=%s layer=%d" % [n.name, wp, (n as CollisionObject3D).collision_layer if n is CollisionObject3D else -1])

	for lv in [0, 1, 2]:
		GameState.house.level = int(lv)
		gr.call("_rebuild_house")
		for i in range(6):
			await get_tree().physics_frame
		print("\n===== LEVEL %d =====" % int(lv))
		# 1) 房屋根节点清单（检测旧程序化屋残留：应只有 1 个 House_L{lv}_Root）
		for n in world.find_children("House_L*_Root", "Node3D", true, false):
			print("[ROOT] %s level=%s pos=%s" % [n.name, n.get_meta("house_level", -1), (n as Node3D).global_position])
		# 2) 门口区域 layer1 碰撞体形状查询（y∈[0.3,2.0] 避开地面）
		var space := get_viewport().world_3d.direct_space_state
		var shape := BoxShape3D.new()
		shape.size = Vector3(7.0, 1.7, 5.0)
		var q := PhysicsShapeQueryParameters3D.new()
		q.shape = shape
		q.transform = Transform3D(Basis(), Vector3(-9, 1.15, 16.6))
		q.collision_mask = 1
		var seen := {}
		for h in space.intersect_shape(q, 32):
			var c := h.get("collider") as Node
			if c == null:
				continue
			var key := "%s|%s" % [c.name, c.get_instance_id()]
			if seen.has(key):
				continue
			seen[key] = true
			var path := String(c.get_path())
			var in_house := path.contains("House_L")
			print("[COLL] name=%s layer=%d inHouse=%s path=%s" % [c.name, (c as CollisionObject3D).collision_layer, in_house, path])
		# 3) 玩家三路靠近交互点
		var routes := [
			{"tag": "正面", "p": Vector3(-9, 0.1, 12.5), "to": INTERACT},
			{"tag": "左前", "p": Vector3(-14.5, 0.1, 13.5), "to": INTERACT},
			{"tag": "右前", "p": Vector3(-3.5, 0.1, 13.5), "to": INTERACT},
		]
		for r in routes:
			player.global_position = r["p"]
			player.velocity = Vector3.ZERO
			for i in range(3):
				await get_tree().physics_frame
			var reached := false
			for i in range(300):
				var d: Vector3 = (r["to"] as Vector3) - player.global_position
				d.y = 0.0
				if d.length() < 1.35:
					reached = true
					break
				player.velocity = d.normalized() * 8.0
				player.move_and_slide()
				await get_tree().physics_frame
			print("[ROUTE] L%d %s 到达交互圈=%s 终点=%s 距交互=%.2f" % [int(lv), r["tag"], reached, player.global_position, player.global_position.distance_to(INTERACT)])
	player.set_physics_process(true)
	print("[DONE] 门口诊断完成")
	get_tree().quit(0)
