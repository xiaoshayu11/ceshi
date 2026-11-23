extends Node

## ENV-CLEANUP 镇区审计（只读）：实例化正式 Town.tscn，扫描遗留/重复/堵路。
var _meshes: Array[Node] = []

func _ready() -> void:
	GameState.autosave_enabled = false
	var town: Node = (load("res://scenes/world/Town.tscn") as PackedScene).instantiate()
	add_child(town)
	for i in range(6):
		await get_tree().physics_frame
	_collect(town)
	var counts := {}
	for n in _all(town):
		counts[n.get_class()] = int(counts.get(n.get_class(), 0)) + 1
	print("===== TOWN 节点统计 =====")
	for k in counts.keys():
		print("[TCOUNT] %s=%d" % [k, counts[k]])

	print("\n===== 方形薄片 BoxMesh =====")
	for n in _meshes:
		var mi := n as MeshInstance3D
		if mi == null or mi.mesh == null or not (mi.mesh is BoxMesh):
			continue
		var sz: Vector3 = (mi.mesh as BoxMesh).size
		if sz.y <= 0.1 and sz.x >= 2.0 and sz.z >= 2.0:
			print("[TFLAT] %s pos=%s size=%s parent=%s" % [n.name, mi.global_position, sz, n.get_parent().name])

	print("\n===== 建筑附近摆件（半径 5m，排查堵门）=====")
	var bldgs := [Vector3(9,0,-3), Vector3(-9,0,-3), Vector3(9,0,6),
		Vector3(-9,0,6), Vector3(-10,0,-14), Vector3(-18,0,-2),
		Vector3(-18,0,6), Vector3(19,0,-6)]
	for n in _meshes:
		var mi := n as MeshInstance3D
		if mi == null:
			continue
		for b in bldgs:
			var d := mi.global_position.distance_to(b)
			if d < 4.0 and String(n.name).begins_with("@"):
				print("[TNEAR] %s pos=%s d=%.2f parent=%s" % [n.name, mi.global_position, d, n.get_parent().name])
				break

	print("\n===== 重复同名近距 Mesh =====")
	var seen := {}
	for n in _meshes:
		var key := "%s|%s" % [n.get_parent().name, n.name]
		if seen.has(key):
			var pos_a: Vector3 = (seen[key] as MeshInstance3D).global_position
			var pos_b: Vector3 = (n as MeshInstance3D).global_position
			if pos_a.distance_to(pos_b) < 0.6:
				print("[TDUP] parent=%s name=%s posA=%s posB=%s" % [n.get_parent().name, n.name, pos_a, pos_b])
		else:
			seen[key] = n
	print("[DONE] 镇区审计完成")
	get_tree().quit(0)

func _all(root: Node) -> Array[Node]:
	var out: Array[Node] = [root]
	for c in root.get_children():
		out.append_array(_all(c))
	return out

func _collect(root: Node) -> void:
	for n in _all(root):
		if n is MeshInstance3D:
			_meshes.append(n)
