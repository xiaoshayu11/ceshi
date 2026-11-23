extends Node

## ENV-CLEANUP 全场景遗留物审计（只读）：实例化正式 World，遍历所有节点，
## 按类统计 + 打印可疑物（BoxMesh 草斑/碰撞占位/悬浮/重复/门口区）。加 -- --no-autosave。
const HOUSE := Vector3(-9, 0, 20)
const SHOP := Vector3(9, 0, -3)

var _lines: Array[String] = []

func _ready() -> void:
	GameState.autosave_enabled = false
	GameState.house.level = 2
	var world: Node = (load("res://scenes/world/World.tscn") as PackedScene).instantiate()
	add_child(world)
	for i in range(8):
		await get_tree().physics_frame

	var counts := {}
	var mesh_nodes: Array[Node] = []
	_collect(world, mesh_nodes, counts)
	print("===== 场景节点统计 =====")
	for k in counts.keys():
		print("[COUNT] %s=%d" % [k, counts[k]])

	print("\n===== 可疑地面 BoxMesh（薄片/方形补丁）=====")
	for n in mesh_nodes:
		var mi := n as MeshInstance3D
		if mi == null or mi.mesh == null:
			continue
		if mi.mesh is BoxMesh:
			var sz: Vector3 = (mi.mesh as BoxMesh).size
			if sz.y <= 0.1 and sz.x >= 2.0 and sz.z >= 2.0:
				print("[FLATBOX] %s pos=%s size=%s parent=%s" % [n.name, mi.global_position, sz, n.get_parent().name])

	print("\n===== 门口区域节点（主屋半径 7m）=====")
	for n in mesh_nodes:
		var mi := n as MeshInstance3D
		if mi == null:
			continue
		var d := mi.global_position.distance_to(HOUSE)
		if d < 7.0:
			var matname := "none"
			for si in mi.mesh.get_surface_count():
				var m := mi.mesh.surface_get_material(si)
				if m != null:
					matname = str(m.get_name())
					break
			print("[DOORNODE] %s pos=%s mesh=%s mat=%s parent=%s" % [n.name, mi.global_position, mi.mesh.get_class(), matname, n.get_parent().name])

	print("\n===== 商店区域节点（杂货铺半径 6m）=====")
	for n in mesh_nodes:
		var mi := n as MeshInstance3D
		if mi == null:
			continue
		if mi.global_position.distance_to(SHOP) < 6.0:
			print("[SHOPNODE] %s pos=%s mesh=%s parent=%s" % [n.name, mi.global_position, mi.mesh.get_class(), n.get_parent().name])

	print("\n===== 全部 StaticBody3D（名称/层/位置，排查残余碰撞）=====")
	for n in _all_nodes(world):
		if n is StaticBody3D:
			var sb := n as StaticBody3D
			var p := sb.global_position
			# 只打印非边界/非地形的可疑碰撞
			if absf(p.x) < 32 and absf(p.z) < 32:
				print("[BODY] %s layer=%d pos=%s parent=%s" % [n.name, sb.collision_layer, p, n.get_parent().name])

	print("\n===== 重复同名 Mesh（同父+同 name）=====")
	var seen := {}
	for n in mesh_nodes:
		var key := "%s|%s" % [n.get_parent().name, n.name]
		if seen.has(key):
			var a: Vector3 = (seen[key] as MeshInstance3D).global_position
			var b: Vector3 = (n as MeshInstance3D).global_position
			if a.distance_to(b) < 0.6:
				print("[DUP] parent=%s name=%s posA=%s posB=%s" % [n.get_parent().name, n.name, a, b])
		else:
			seen[key] = n

	print("[DONE] 审计完成")
	get_tree().quit(0)

func _all_nodes(root: Node) -> Array[Node]:
	var out: Array[Node] = []
	out.append(root)
	for c in root.get_children():
		out.append_array(_all_nodes(c))
	return out

func _collect(root: Node, meshes: Array[Node], counts: Dictionary) -> void:
	for n in _all_nodes(root):
		var cls := n.get_class()
		counts[cls] = int(counts.get(cls, 0)) + 1
		if n is MeshInstance3D:
			meshes.append(n)
