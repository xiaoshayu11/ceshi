extends Node

## ENV-CLEANUP 进屋实测截图：生产链路——玩家走到门口→F 提示→触发 F→室内场景→返回农场。
## 加 -- --no-autosave（不写生产档）。需窗口渲染（勿 --headless）。
const INTERACT := Vector3(-9, 0.1, 15.6)
const OUT := "res://tests/evidence/cleanup_f_enter/"

var _pass := 0

func _ready() -> void:
	GameState.autosave_enabled = false
	GameState.house.level = 2
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	var world: Node = (load("res://scenes/world/World.tscn") as PackedScene).instantiate()
	add_child(world)
	for i in range(8):
		await get_tree().process_frame
	var player := get_tree().get_first_node_in_group("player") as CharacterBody3D
	var gr := world.get_node("GameplayRoot")
	player.set_physics_process(false)
	# 玩家从院门缺口外走到门口交互点（真实移动）
	player.global_position = Vector3(0, 0.1, 13.2)
	await _drive(player, INTERACT)
	var cam := Camera3D.new()
	add_child(cam)
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = 12.0
	var target := Vector3(-9, 1.0, 17.0)
	cam.global_position = target + Vector3(0, 15.0, -15.0)
	cam.look_at(target, Vector3.UP)
	cam.make_current()
	await get_tree().process_frame
	await get_tree().create_timer(0.3).timeout
	await _snap(cam, "01_at_door")

	# 交互管理器提示
	var mgr := get_tree().get_first_node_in_group("interaction_manager") as InteractionManager
	for i in range(8):
		await get_tree().process_frame
	var cur := mgr.get_current() if mgr != null else null
	print("[INFO] 当前交互对象=%s 提示=%s" % [cur.name if cur != null else "null", mgr.get_current_prompt() if mgr != null else "-"])
	await _snap(cam, "02_f_prompt")

	# 触发 F
	if cur is HouseDoorInteractable:
		cur.call("on_interact")
		cam.queue_free()
		for i in range(100):
			await get_tree().process_frame
		var scene_now := get_tree().current_scene
		var ok := scene_now != null and String(scene_now.scene_file_path).contains("HouseInterior")
		check(ok, "F 交互切换到室内")
		if ok:
			# 室内场景：用一个俯视正交相机拍玩家进屋落位
			var icam := Camera3D.new()
			add_child(icam)
			icam.projection = Camera3D.PROJECTION_ORTHOGONAL
			icam.size = 11.0
			var iplayer := get_tree().get_first_node_in_group("player") as CharacterBody3D
			var it := (iplayer.global_position if iplayer != null else Vector3.ZERO) + Vector3(0, 1.0, 0)
			icam.global_position = it + Vector3(0, 14.0, -14.0)
			icam.look_at(it, Vector3.UP)
			icam.make_current()
			await get_tree().process_frame
			await get_tree().create_timer(0.4).timeout
			await _snap(icam, "03_inside_house")
			icam.queue_free()
			# 返回农场（实拍回程落位）
			SceneRouter.change_scene("farm", "from_house")
			for i in range(100):
				await get_tree().process_frame
			var back := get_tree().current_scene
			check(back != null and String(back.scene_file_path).contains("World"), "室内返回农场")
			var bcam := Camera3D.new()
			add_child(bcam)
			bcam.projection = Camera3D.PROJECTION_ORTHOGONAL
			bcam.size = 14.0
			var bp := get_tree().get_first_node_in_group("player") as CharacterBody3D
			var bt := (bp.global_position if bp != null else Vector3(-9,0,15.6)) + Vector3(0, 1.0, 0)
			bcam.global_position = bt + Vector3(0, 15.0, -15.0)
			bcam.look_at(bt, Vector3.UP)
			bcam.make_current()
			await get_tree().process_frame
			await get_tree().create_timer(0.4).timeout
			await _snap(bcam, "04_back_at_door")
			bcam.queue_free()
	else:
		printerr("[FAIL] 门口无 HouseDoor 交互对象")
	print("[DONE] 进屋实测截图 %d 张" % _pass)
	get_tree().quit(0)

func check(cond: bool, msg: String) -> void:
	if cond:
		_pass += 1
		print("  [PASS] " + msg)
	else:
		printerr("  [FAIL] " + msg)

func _drive(player: CharacterBody3D, to: Vector3) -> void:
	for i in range(300):
		var d := to - player.global_position
		d.y = 0.0
		if d.length() < 1.2:
			break
		player.velocity = d.normalized() * 8.0
		player.move_and_slide()
		await get_tree().physics_frame

func _snap(cam: Camera3D, tag: String) -> void:
	cam.make_current()
	await get_tree().process_frame
	await get_tree().create_timer(0.3).timeout
	var img: Image = get_viewport().get_texture().get_image()
	if img.save_png(ProjectSettings.globalize_path(OUT + tag + ".png")) == OK:
		_pass += 1
		print("[PASS] 截图 %s" % tag)
