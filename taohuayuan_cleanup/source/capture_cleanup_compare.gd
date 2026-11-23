extends Node

## ENV-CLEANUP 清理前后对比出图（正式游戏镜头）。
## 用法：Godot --path . tests/capture_cleanup_compare.tscn -- --no-autosave before
##       Godot --path . tests/capture_cleanup_compare.tscn -- --no-autosave after
const HOUSE := Vector3(-9, 0, 20)
const SHOP := Vector3(9, 0, -3)

var _out := "res://tests/evidence/cleanup_before/"
var _pass := 0

func _ready() -> void:
	GameState.autosave_enabled = false
	var args := OS.get_cmdline_user_args()
	var phase := "before"
	for a in args:
		if a == "before" or a == "after":
			phase = a
	_out = "res://tests/evidence/cleanup_%s/" % phase
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(_out))

	# ---- 农场（World.tscn 生产链路）----
	var world: Node = (load("res://scenes/world/World.tscn") as PackedScene).instantiate()
	add_child(world)
	_hide_ui(world)
	for i in range(6):
		await get_tree().process_frame
	var gr := world.get_node("GameplayRoot")
	# 四向全景
	for yaw in [0, 90, 180, 270]:
		await _shoot(Vector3(0, 0, 0), float(yaw), 30.0, "farm_yaw%d" % int(yaw))
	# 北口旧方形草斑特写
	await _shoot(Vector3(0, 0, -26), 0.0, 13.0, "farm_north_patches")
	# 三档门口正面（生产_build链路）
	for lv in [0, 1, 2]:
		GameState.house.level = int(lv)
		if gr != null and gr.has_method("_rebuild_house"):
			gr.call("_rebuild_house")
		for i in range(6):
			await get_tree().process_frame
		await _shoot(HOUSE + Vector3(0, 1.1, -2.2), 180.0, 9.5, "house_L%d_entrance" % int(lv))
		await _shoot(HOUSE + Vector3(1.5, 0.9, -3.5), 180.0, 22.0, "house_L%d_yard" % int(lv))
	world.queue_free()
	for i in range(6):
		await get_tree().process_frame

	# ---- 镇区（Town.tscn）----
	var town: Node = (load("res://scenes/world/Town.tscn") as PackedScene).instantiate()
	add_child(town)
	_hide_ui(town)
	for i in range(6):
		await get_tree().process_frame
	for yaw in [0, 90, 180, 270]:
		await _shoot(Vector3(0, 0, 0), float(yaw), 30.0, "town_yaw%d" % int(yaw))
	await _shoot(Vector3(0, 0, 26), 180.0, 13.0, "town_south_patches")
	await _shoot(SHOP + Vector3(0, 0.8, 0), 270.0, 9.0, "shop_entrance")

	print("[DONE] cleanup_%s 出图完成 %d 张" % [phase, _pass])
	get_tree().quit(0)

func _shoot(target: Vector3, yaw_deg: float, ortho: float, tag: String) -> void:
	var cam := Camera3D.new()
	add_child(cam)
	cam.projection = Camera3D.PROJECTION_ORTHOGONAL
	cam.size = ortho
	var rad := deg_to_rad(yaw_deg)
	var horiz := 18.0
	var h := horiz * tan(deg_to_rad(52.0))
	var dir := Vector3(sin(rad), 0.0, cos(rad))
	cam.global_position = target + dir * horiz + Vector3(0, h, 0)
	cam.look_at(target, Vector3.UP)
	cam.make_current()
	await get_tree().process_frame
	await get_tree().create_timer(0.3).timeout
	var img: Image = get_viewport().get_texture().get_image()
	var err: Error = img.save_png(ProjectSettings.globalize_path(_out + tag + ".png"))
	if err == OK:
		_pass += 1
	else:
		printerr("[FAIL] 截图 %s err=%d" % [tag, err])
	cam.queue_free()
	await get_tree().process_frame

func _hide_ui(node: Node) -> void:
	if node is CanvasLayer:
		node.visible = false
	for c in node.get_children():
		_hide_ui(c)
