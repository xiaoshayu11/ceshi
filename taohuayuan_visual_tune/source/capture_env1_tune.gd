extends Node

## ENV-1 地面系统验收截图（正式游戏镜头：正交 pitch 52°，四向 yaw）。
## 只读现状：农场/镇区全景四向 + 地面近景（路缘/田地/房屋衔接）。
## 加 -- --no-autosave 防写生产档。

const OUT := "res://tests/evidence/env1_tune/"

func _ready() -> void:
	GameState.autosave_enabled = false
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	await _shots("res://scenes/world/World.tscn", [
		{"t": Vector3(0, 0, 4), "yaw": 0.0, "o": 26.0, "tag": "farm_yaw0"},
		{"t": Vector3(0, 0, 4), "yaw": 90.0, "o": 26.0, "tag": "farm_yaw90"},
		{"t": Vector3(0, 0, 4), "yaw": 180.0, "o": 26.0, "tag": "farm_yaw180"},
		{"t": Vector3(0, 0, 4), "yaw": 270.0, "o": 26.0, "tag": "farm_yaw270"},
		{"t": Vector3(-5, 0, 8), "yaw": 0.0, "o": 13.0, "tag": "farm_ground_house_road"},
		{"t": Vector3(2, 0, 5), "yaw": 90.0, "o": 13.0, "tag": "farm_ground_field_edge"},
	])
	await _shots("res://scenes/world/Town.tscn", [
		{"t": Vector3(0, 0, 0), "yaw": 0.0, "o": 26.0, "tag": "town_yaw0"},
		{"t": Vector3(0, 0, 0), "yaw": 90.0, "o": 26.0, "tag": "town_yaw90"},
		{"t": Vector3(0, 0, 0), "yaw": 180.0, "o": 26.0, "tag": "town_yaw180"},
		{"t": Vector3(0, 0, 0), "yaw": 270.0, "o": 26.0, "tag": "town_yaw270"},
		{"t": Vector3(4, 0, 2), "yaw": 270.0, "o": 13.0, "tag": "town_ground_street_edge"},
		{"t": Vector3(-9, 0, 6), "yaw": 90.0, "o": 13.0, "tag": "town_ground_shop_base"},
	])
	print("[DONE] ENV-1 验收截图完成")
	get_tree().quit(0)

func _shots(path: String, shots: Array) -> void:
	var w: Node = (load(path) as PackedScene).instantiate()
	add_child(w)
	await get_tree().process_frame
	await get_tree().process_frame
	for c in w.find_children("*", "CanvasLayer", true, false):
		(c as CanvasLayer).visible = false
	for c in w.find_children("*", "Control", true, false):
		if c.get_parent() is CanvasLayer:
			(c as Control).visible = false
	for s in shots:
		await _shot(s["t"], float(s["yaw"]), float(s["o"]), String(s["tag"]))
	w.queue_free()
	await get_tree().process_frame

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
