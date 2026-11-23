extends Node

## ENV-2② 商业建筑样板验收截图（正式镇区 + 正式正交游戏镜头 pitch 52°）。
## 罩：伞盖铺四向、正面/背面/侧面/屋顶特写、与邻栋组合、广场视角。
## 加 -- --no-autosave 防写生产档。

const OUT := "res://tests/evidence/env2b_tune/"

func _ready() -> void:
	GameState.autosave_enabled = false
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	var w: Node = (load("res://scenes/world/Town.tscn") as PackedScene).instantiate()
	add_child(w)
	await get_tree().process_frame
	await get_tree().process_frame
	for c in w.find_children("*", "CanvasLayer", true, false):
		(c as CanvasLayer).visible = false
	for c in w.find_children("*", "Control", true, false):
		if c.get_parent() is CanvasLayer:
			(c as Control).visible = false

	var shop := Vector3(9, 1.6, -3)
	# 四向：yaw=270 为正门（朝广场 -X），yaw=90 背面，0/180 两侧
	for cfg in [
		{"t": shop, "yaw": 0.0, "o": 11.0, "tag": "shop_yaw0_side_s"},
		{"t": shop, "yaw": 90.0, "o": 11.0, "tag": "shop_yaw90_back"},
		{"t": shop, "yaw": 180.0, "o": 11.0, "tag": "shop_yaw180_side_n"},
		{"t": shop, "yaw": 270.0, "o": 11.0, "tag": "shop_yaw270_front"},
		{"t": shop + Vector3(0, 0.8, 0), "yaw": 270.0, "o": 7.5, "tag": "shop_front_detail"},
		{"t": shop + Vector3(0, 0.8, 0), "yaw": 90.0, "o": 7.5, "tag": "shop_back_detail"},
		{"t": shop + Vector3(0, 1.5, 0), "yaw": 270.0, "o": 8.5, "tag": "shop_roof_detail"},
		{"t": Vector3(4.5, 0.8, 1.5), "yaw": 270.0, "o": 17.0, "tag": "town_shop_neighbors"},
		{"t": Vector3(0, 0, 0), "yaw": 270.0, "o": 24.0, "tag": "town_plaza_with_new_shop"},
	]:
		await _shot(cfg["t"], float(cfg["yaw"]), float(cfg["o"]), String(cfg["tag"]))
	print("[DONE] ENV-2② 样板截图完成")
	get_tree().quit(0)

func _shot(target: Vector3, yaw_deg: float, ortho: float, tag: String) -> void:
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
	await get_tree().create_timer(0.35).timeout
	var img: Image = get_viewport().get_texture().get_image()
	var err: Error = img.save_png(ProjectSettings.globalize_path(OUT + tag + ".png"))
	print("[PASS] %s" % tag if err == OK else "[FAIL] %s err=%d" % [tag, err])
	cam.queue_free()
	await get_tree().process_frame
