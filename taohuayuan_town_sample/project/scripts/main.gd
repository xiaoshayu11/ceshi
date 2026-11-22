extends Node3D
## 《桃花源物语》小镇样板：真实游戏镜头展示 + 统计 + 性能采样
## 模式：默认出截图；-- --perf 采样；-- --closer 出补充机位

const CUSTOM := "res://assets/models/custom/"
const NATURE := "res://assets/models/nature/"
const PP := "res://assets/models/pp/"
const EVID := "res://evidence"

const C_GRASS := Color("7AA063")
const C_GRASS_D := Color("4A7355")
const C_DIRT := Color("A98A61")
const C_STONE := Color("96A1A4")
const C_WOOD := Color("9C7A5B")
const C_WATER := Color("7FAFB4")
const C_CREAM := Color("F5E9D2")

var _sun: DirectionalLight3D
var _veg_nodes: Array = []
var _anim_players: Array = []
var _npcs: Dictionary = {}
var _stats := {"scene": {}, "instances": [], "lint": {}}
var _placed_types: Dictionary = {}
var _npc_origins: Dictionary = {}
var _action_mode := false
var _time := 0.0

func _ready() -> void:
	_build_environment()
	var args := OS.get_cmdline_user_args()
	_build_scene()
	_play_anims()
	_collect_stats()
	if "--perf" in args:
		_perf_run()
	else:
		_shots("--closer" in args)

# ---------- 基础 ----------
func _vc_material() -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = Color.WHITE
	m.vertex_color_use_as_albedo = true
	m.vertex_color_is_srgb = true
	m.roughness = 0.85
	m.metallic = 0.0
	m.metallic_specular = 0.25
	return m

func _plain(color: Color, rough := 0.85) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = color
	m.roughness = rough
	m.metallic = 0.0
	m.metallic_specular = 0.25
	return m

func _meshes(n: Node) -> Array:
	var out := []
	if n is MeshInstance3D:
		out.append(n)
	for c in n.get_children():
		out.append_array(_meshes(c))
	return out

func _place(dir: String, fname: String, pos: Vector3, ry := 0.0, scale := 1.0, vc := true, group := "") -> Node3D:
	var packed: PackedScene = load(dir + fname)
	if packed == null:
		push_error("MISSING " + dir + fname)
		return Node3D.new()
	var inst: Node3D = packed.instantiate()
	add_child(inst)
	if vc:
		for mi in _meshes(inst):
			mi.material_override = _vc_material()
	inst.position = pos
	inst.rotation_degrees.y = ry
	inst.scale = Vector3(scale, scale, scale)
	if not group.is_empty():
		inst.add_to_group(group)
	_placed_types[fname] = int(_placed_types.get(fname, 0)) + 1
	_stats["instances"].append({"file": fname, "pos": [pos.x, pos.y, pos.z]})
	return inst

func _plane(size: Vector2, color: Color, pos: Vector3, y := 0.0) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	var pm := PlaneMesh.new()
	pm.size = size
	mi.mesh = pm
	mi.material_override = _plain(color, 0.9)
	mi.position = Vector3(pos.x, y, pos.z)
	add_child(mi)
	return mi

func _patch(pos: Vector3, radius: float, color: Color) -> void:
	var mi := MeshInstance3D.new()
	var cm := CylinderMesh.new()
	cm.top_radius = radius
	cm.bottom_radius = radius * 0.92
	cm.height = 0.012
	cm.radial_segments = 14
	mi.mesh = cm
	mi.material_override = _plain(color, 0.92)
	mi.position = Vector3(pos.x, -0.014, pos.z)
	add_child(mi)

func _build_environment() -> void:
	_sun = DirectionalLight3D.new()
	_sun.rotation_degrees = Vector3(-38, -38, 0)
	_sun.light_color = Color(1.0, 0.96, 0.88)
	_sun.light_energy = 0.85
	_sun.shadow_enabled = true
	add_child(_sun)
	var fill := DirectionalLight3D.new()
	fill.rotation_degrees = Vector3(-20, 145, 0)
	fill.light_color = Color(0.86, 0.90, 1.0)
	fill.light_energy = 0.22
	fill.shadow_enabled = false
	add_child(fill)
	var env := WorldEnvironment.new()
	var e := Environment.new()
	e.background_mode = Environment.BG_COLOR
	e.background_color = Color(0.78, 0.87, 0.93)
	e.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	e.ambient_light_color = Color(0.72, 0.78, 0.86)
	e.ambient_light_energy = 0.35
	env.environment = e
	add_child(env)

# ---------- 场景 ----------
func _build_scene() -> void:
	_plane(Vector2(80, 80), C_GRASS.darkened(0.04), Vector3.ZERO, -0.02)
	# 土路：南入口 → 中心广场 → 住宅/商店分叉
	_plane(Vector2(3.2, 22), C_DIRT, Vector3(0, 0, 10), -0.008)
	_plane(Vector2(18, 3.0), C_DIRT, Vector3(0, 0, -1.5), -0.007)
	_plane(Vector2(3.0, 10), C_DIRT, Vector3(-8, 0, -5.5), -0.006)
	_plane(Vector2(3.0, 10), C_DIRT, Vector3(7, 0, -5.5), -0.006)
	# 草地色块（低对比，避免大片单色）
	for item in [[-14, -12, 4.5], [12, 8, 5.2], [-3, 13, 4.0], [16, -6, 3.8], [-20, 8, 4.6], [3, -12, 3.4]]:
		_patch(Vector3(item[0], 0, item[1]), item[2], C_GRASS.darkened(0.035 + (item[0] % 3) * 0.01))
	# 主路石板点缀 + 中心广场（同类 MultiMesh 合批）
	var slabs := [[0, 0.005, 1.2, 0, 1]]
	for i in range(11):
		slabs.append([(i % 2) * 0.55 - 0.27, 0.005, 2.5 + i * 1.55, (i * 37) % 180, 1])
	_multi_place(NATURE, "slab-path-stone-e526f7.glb", slabs)
	var rounds := []
	for i in range(7):
		var a := i * TAU / 7
		rounds.append([cos(a) * 2.7, 0.0, 1.2 + sin(a) * 2.7, (i * 47) % 180, 1])
	_multi_place(NATURE, "round-path-stone-4130f3.glb", rounds)

	# 主住宅（院落：围栏+门）
	_place(CUSTOM, "custom_house.glb", Vector3(-8.5, 0, -6.5), 0, 1.0)
	_multi_place(NATURE, "wooden-fence-section-5f04b7.glb",
		[[-12.8, 0, -10.4, 0, 1], [-12.8, 0, -2.8, 0, 1], [-4.2, 0, -10.4, 0, 1], [-4.2, 0, -2.8, 0, 1]])
	_place(NATURE, "wooden-fence-gate-a8735f.glb", Vector3(-8.5, 0, -2.8), 0)
	_place(NATURE, "lantern-post-f47665.glb", Vector3(-4.1, 0, -2.4), 0)
	# 小桃花树点缀（秋色树总量控制）
	_place(NATURE, "maple-tree-65fa12.glb", Vector3(-12.5, 0, -8.8), 20)

	# 商店（敞开售货台、幌子、货物）
	_place(CUSTOM, "custom_shop.glb", Vector3(7.5, 0, -6.5), 0, 1.0)
	_place(NATURE, "wooden-barrel-ab50ca.glb", Vector3(3.9, 0, -3.3), 10)
	_place(NATURE, "lantern-post-f47665.glb", Vector3(11.5, 0, -2.5), 0)
	_place(NATURE, "birdhouse-post-66d6c1.glb", Vector3(12.5, 0, -8.0), 15)
	_place(PP, "pp_gYYC0gYMnw.glb", Vector3(12.5, 1.72, -8.0), -90, 1.0, false)

	# 池塘 + 小桥（西侧）
	var water := _place(NATURE, "water-blob-f266b8.glb", Vector3(-15, 0, 7), 15, 2.0)
	_water_mat(water)
	for p in [Vector3(-14.0, 0.02, 5.3), Vector3(-16.2, 0.02, 8.1), Vector3(-14.8, 0.02, 8.8), Vector3(-17.2, 0.02, 6.2)]:
		_place(NATURE, "lily-pad-86edbb.glb", p, randf() * 90, 1.0, true, "pond")
	_place(PP, "pp_2KHEgw1ztVI.glb", Vector3(-15.6, 0.03, 6.7), 160, 1.35, false, "pond")
	_place(PP, "pp_2KHEgw1ztVI.glb", Vector3(-13.6, 0.03, 8.0), 40, 1.2, false, "pond")
	_place(NATURE, "log-plank-bridge-a5f74f.glb", Vector3(-10.2, 0, 7.2), 90, 1.1)
	var reeds := []
	for i in range(7):
		reeds.append([-18.6 + (i % 2) * 0.7, 0, 2.6 + i * 1.5, (i * 53) % 180, 1])
	_multi_place(NATURE, "cattail-reed-6abbb3.glb", reeds)
	_place(PP, "pp_5gZfOZIW92k.glb", Vector3(-11.8, 0, 3.4), -20, 1.0, false, "stone_lamp")
	_place(NATURE, "large-boulder-a29b99.glb", Vector3(-19.0, 0, 10.5), 20)
	var shore := []
	for i in range(9):
		var a := i * TAU / 9
		var r := 4.7 + (i % 3) * 0.25
		shore.append([-15.0 + cos(a) * r, 0, 7.0 + sin(a) * r, (i * 41) % 180, 1])
	_multi_place(NATURE, "small-rock-db33a7.glb", shore)

	# 树木与灌木（层次：高树外圈、灌木内圈）
	for spec in [
		["broadleaf-oak-997c22.glb", [[-22, 0, -4, 0, 1], [18, 0, 4, 120, 1], [-6, 0, 16, 200, 1]]],
		["tall-pine-tree-ab4108.glb", [[-20, 0, -14, 0, 1], [19, 0, -14, 160, 1]]],
		["young-pine-0d7695.glb", [[22, 0, -2, 40, 1], [-24, 0, 3, 90, 1]]],
		["birch-tree-181b33.glb", [[3, 0, 15, 30, 1], [-3, 0, -14, 0, 1], [15, 0, 12, 150, 1]]],
		["round-bush-cd2ac0.glb", [[-11, 0, 1, 12, 1], [4.5, 0, 3, 80, 1], [11, 0, 2, 140, 1],
			[-6, 0, 11, 40, 1], [-12, 0, -2, 100, 1], [12, 0, -4.5, 20, 1],
			[-8, 0, 11.5, 160, 1], [6, 0, 9.5, 70, 1]]],
	]:
		_multi_place(NATURE, spec[0], spec[1])
	_place(NATURE, "stone-well-2b4717.glb", Vector3(1.5, 0, -6.5), 25)
	_multi_place(NATURE, "wooden-bench-02e2c8.glb",
		[[-8.6, 0, 10.3, 25, 1], [3.6, 0, -2.2, -35, 1], [-9.8, 0, -2.0, 20, 1]])
	_multi_place(CUSTOM, "prop_flowerpot.glb",
		[[-10.9, 0, -3.2, 0, 1.1], [-6.1, 0, -3.2, 20, 0.9], [3.2, 0, -6.0, 0, 1], [10.6, 0, -2.2, 0, 0.9]])
	_multi_place(NATURE, "lantern-post-f47665.glb",
		[[-4.1, 0, -2.4, 0, 1], [11.5, 0, -2.5, 0, 1], [-2.2, 0, 3.2, 0, 1], [2.2, 0, 8.5, 0, 1]])
	_multi_place(CUSTOM, "prop_crate.glb", [[-11.3, 0, -5.0, 15, 1], [11.2, 0, -3.2, -20, 1]])
	_place(NATURE, "wooden-hand-cart-3ae5b5.glb", Vector3(12.5, 0, -1.5), -35)
	_place(NATURE, "open-woodshed-050a0a.glb", Vector3(14.5, 0, -11.0), -15)
	_multi_place(NATURE, "medium-rock-e08405.glb",
		[[-5.5, 0, 5.5, 12, 1], [6.0, 0, 6.5, 98, 1], [3.0, 0, -10.0, 55, 1]])

	# 植被 MultiMesh
	_veg_mm("grass-tuft-a40a08.glb", 125, Vector3(0, 0, 4), 44, 36, 0.28)
	_veg_mm("wildflower-68d3a1.glb", 42, Vector3(3, 0, 10), 28, 20, 0.38)
	_veg_mm("fern-plant-1559b8.glb", 24, Vector3(-17, 0, -6), 18, 16, 0.42)

	# 动物 NPC（面部朝 +Z 游戏主镜头）
	var rabbit := _place(CUSTOM, "npc_rabbit.glb", Vector3(-3.2, 0, 2.2), 0, 1.0, true, "npc")
	var fox := _place(CUSTOM, "npc_fox.glb", Vector3(5.2, 0, -3.5), -18, 1.0, true, "npc")
	var calf := _place(CUSTOM, "npc_calf.glb", Vector3(8.5, 0, 4.5), 0, 1.0, true, "npc")
	_npcs = {"rabbit": rabbit, "fox": fox, "calf": calf}
	for k in _npcs.keys():
		_npc_origins[k] = (_npcs[k] as Node3D).position
	_place(PP, "pp_1YE8U35HXsI.glb", Vector3(-1.5, 0, -4.5), 30, 1.0, false, "npc")

func _water_mat(root: Node) -> void:
	var m := StandardMaterial3D.new()
	m.albedo_color = C_WATER
	m.roughness = 0.15
	m.metallic = 0.0
	m.metallic_specular = 0.25
	m.rim_enabled = true
	m.rim = 0.6
	m.rim_tint = 0.4
	for mi in _meshes(root):
		mi.material_override = m

func _mm_place(fname: String, transforms: Array[Transform3D]) -> void:
	var packed: PackedScene = load(NATURE + fname)
	var src: Node3D = packed.instantiate()
	add_child(src)
	var mesh: Mesh = null
	for mi in _meshes(src):
		if mi.mesh:
			mesh = mi.mesh
			break
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.mesh = mesh
	mm.instance_count = transforms.size()
	for i in range(transforms.size()):
		mm.set_instance_transform(i, transforms[i])
	var holder := MultiMeshInstance3D.new()
	holder.multimesh = mm
	add_child(holder)
	holder.material_override = _vc_material()
	holder.add_to_group("vegetation")
	_veg_nodes.append(holder)
	_placed_types[fname] = int(_placed_types.get(fname, 0)) + transforms.size()
	src.queue_free()

func _multi_place(dir: String, fname: String, specs: Array) -> void:
	var transforms: Array[Transform3D] = []
	for s in specs:
		var t := Transform3D()
		t = t.rotated(Vector3.UP, deg_to_rad(s[3]))
		t = t.scaled(Vector3(s[4], s[4], s[4]))
		t.origin = Vector3(s[0], s[1], s[2])
		transforms.append(t)
	_mm_place_dir(dir, fname, transforms)

func _mm_place_dir(dir: String, fname: String, transforms: Array[Transform3D]) -> void:
	var packed: PackedScene = load(dir + fname)
	var src: Node3D = packed.instantiate()
	add_child(src)
	var mesh: Mesh = null
	for mi in _meshes(src):
		if mi.mesh:
			mesh = mi.mesh
			break
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_3D
	mm.mesh = mesh
	mm.instance_count = transforms.size()
	for i in range(transforms.size()):
		mm.set_instance_transform(i, transforms[i])
	var holder := MultiMeshInstance3D.new()
	holder.multimesh = mm
	add_child(holder)
	holder.material_override = _vc_material()
	holder.add_to_group("batch")
	_placed_types[fname] = int(_placed_types.get(fname, 0)) + transforms.size()
	_stats["instances"].append({"file": fname, "count": transforms.size(), "batch": true})
	src.queue_free()

func _mm_fence(pos: Vector3) -> void:
	var t := Transform3D()
	t = t.rotated(Vector3.UP, 0)
	t.origin = pos
	_mm_place("wooden-fence-section-5f04b7.glb", [t])

func _veg_mm(fname: String, count: int, center: Vector3, w: float, d: float, jitter: float) -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 20261122
	var tf: Array[Transform3D] = []
	for i in range(count):
		var t := Transform3D()
		t = t.rotated(Vector3.UP, rng.randf() * TAU)
		t.origin = Vector3(center.x + rng.randf_range(-w/2, w/2), 0, center.z + rng.randf_range(-d/2, d/2))
		tf.append(t)
	_mm_place(fname, tf)

func _play_anims() -> void:
	for n in get_children():
		for ap in _anim_players_in(n):
			_anim_players.append(ap)
			var names: PackedStringArray = ap.get_animation_list()
			var pick := ""
			for nm in names:
				if nm.contains("Idle"):
					pick = nm
					break
			if pick.is_empty() and names.size() > 0:
				pick = names[0]
			if not pick.is_empty():
				ap.play(pick)
				ap.get_animation(pick).loop_mode = Animation.LOOP_LINEAR

func _anim_players_in(n: Node) -> Array:
	var out := []
	if n is AnimationPlayer:
		out.append(n)
	for c in n.get_children():
		out.append_array(_anim_players_in(c))
	return out

func _process(delta: float) -> void:
	_time += delta
	var i := 0
	for k in _npcs.keys():
		var n: Node3D = _npcs[k]
		var origin: Vector3 = _npc_origins[k]
		n.position.y = origin.y + sin(_time * 2.6 + i * 1.7) * 0.012
		n.rotation_degrees.x = -12.0 if _action_mode else (sin(_time * 2.0 + i) * 2.5)
		i += 1

# ---------- 统计 ----------
func _mesh_tris(mesh: Mesh) -> int:
	var t := 0
	for s in range(mesh.get_surface_count()):
		var arr: Array = mesh.surface_get_arrays(s)
		var idx: PackedInt32Array = arr[Mesh.ARRAY_INDEX]
		var vtx: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
		t += (idx.size() if idx.size() > 0 else vtx.size()) / 3
	return t

func _collect_stats() -> void:
	var tris := 0
	var dc := 0
	var mats := {}
	for n in _countable_nodes(self):
		if n is MultiMeshInstance3D and n.multimesh and n.multimesh.mesh:
			tris += _mesh_tris(n.multimesh.mesh) * n.multimesh.instance_count
			dc += max(1, n.multimesh.mesh.get_surface_count())
			for s in range(n.multimesh.mesh.get_surface_count()):
				var mm: Material = n.multimesh.mesh.surface_get_material(s)
				if mm:
					mats[mm.get_instance_id()] = true
		elif n is MeshInstance3D and n.mesh:
			tris += _mesh_tris(n.mesh)
			dc += max(1, n.mesh.get_surface_count())
			for s in range(n.mesh.get_surface_count()):
				var m: Material = n.mesh.surface_get_material(s)
				if m:
					mats[m.get_instance_id()] = true
	var bones := 0
	var skeletons := 0
	for n in get_children():
		for sk in _by_class(n, "Skeleton3D"):
			skeletons += 1
			bones += sk.get_bone_count()
	var anims := 0
	for ap in _anim_players:
		anims += ap.get_animation_list().size()
	_stats["scene"] = {
		"title": "taohuayuan town sample",
		"model_types": _placed_types.size(),
		"placed_instances": _stats["instances"].size(),
		"static_tris": tris,
		"draw_calls_estimate": dc,
		"multimesh_groups": _veg_nodes.size(),
		"skeletons": skeletons,
		"bones": bones,
		"animation_players": _anim_players.size(),
		"animations": anims,
		"unique_materials": len(mats),
	}
	_stats["lint"] = {
		"stone_lamp": get_tree().get_nodes_in_group("stone_lamp").size(),
		"npc": get_tree().get_nodes_in_group("npc").size(),
		"autumn_trees": int(_placed_types.get("maple-tree-65fa12.glb", 0)),
	}
	var f := FileAccess.open(EVID + "/town_stats.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(_stats, "  "))
	f.close()
	print("TOWN_STATS ", JSON.stringify(_stats["scene"]))

func _countable_nodes(n: Node) -> Array:
	var out := []
	if n.is_queued_for_deletion():
		return out
	if n is MeshInstance3D or n is MultiMeshInstance3D:
		out.append(n)
	for c in n.get_children():
		out.append_array(_countable_nodes(c))
	return out

func _by_class(n: Node, cls: String) -> Array:
	var out := []
	if n.is_class(cls):
		out.append(n)
	for c in n.get_children():
		out.append_array(_by_class(c, cls))
	return out

# ---------- 镜头 ----------
func _cam(center: Vector3, dir: Vector3, dist: float, size: float) -> Camera3D:
	var c := Camera3D.new()
	c.projection = Camera3D.PROJECTION_ORTHOGONAL
	c.size = size
	add_child(c)
	c.global_position = center + dir * dist + Vector3(0, dist * 0.82, 0)
	c.look_at(center, Vector3.UP)
	return c

func _snap(c: Camera3D, path: String) -> void:
	c.make_current()
	await get_tree().process_frame
	await get_tree().process_frame
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png(path)
	print("SAVED ", path)
	c.queue_free()

func _shots(closer: bool) -> void:
	var c := _cam(Vector3(0, 1, 1), Vector3(0, 0, 1), 26, 28)
	await _snap(c, EVID + "/town_full.png")
	var dirs := {"s0": Vector3(0, 0, 1), "s90": Vector3(1, 0, 0), "s180": Vector3(0, 0, -1), "s270": Vector3(-1, 0, 0)}
	for k in dirs:
		var q := _cam(Vector3(0, 1, 1), dirs[k], 25, 27)
		await _snap(q, EVID + "/town_" + k + ".png")
	# 房屋正面（+Z 观察）/细节
	var h := _cam(Vector3(-8.5, 1.4, -6.5), Vector3(0, 0, 1), 11, 11)
	await _snap(h, EVID + "/house_front_a.png")
	h = _cam(Vector3(-8.5, 1.4, -6.5), Vector3(0, 0, -1), 11, 11)
	await _snap(h, EVID + "/house_front_b.png")
	var hd := _cam(Vector3(-9.6, 1.7, -5.0), Vector3(0, 0, 1), 6.5, 6.5)
	await _snap(hd, EVID + "/house_detail.png")
	var sh := _cam(Vector3(7.5, 1.4, -6.5), Vector3(0, 0, 1), 12, 12)
	await _snap(sh, EVID + "/shop_front.png")
	# 动物正面/侧面/动作
	for k in _npcs.keys():
		var p: Vector3 = _npcs[k].position
		var d := 3.0 if k == "calf" else (1.8 if k == "fox" else 1.2)
		var sz := 3.0 if k == "calf" else (1.8 if k == "fox" else 1.2)
		var a := _cam(p + Vector3(0, 0.5, 0), Vector3(0, 0, 1), d, sz)
		await _snap(a, EVID + "/npc_" + k + "_front.png")
		var s := _cam(p + Vector3(0, 0.5, 0), Vector3(1, 0, 0), d, sz)
		await _snap(s, EVID + "/npc_" + k + "_side.png")
	# 动作：节点级点头 + 呼吸（零蒙皮、gl_compatibility 稳定）
	_action_mode = true
	var act := _cam(Vector3(0, 1, 1), Vector3(0, 0, 1), 12, 13)
	await get_tree().create_timer(0.35).timeout
	await _snap(act, EVID + "/npc_action.png")
	_action_mode = false
	# 组合展示
	var combo := _cam(Vector3(-4, 1, 7), Vector3(0, 0, 1), 11, 12)
	await _snap(combo, EVID + "/combo_pond_path.png")
	var combo2 := _cam(Vector3(5, 1, 0), Vector3(0, 0, 1), 11, 12)
	await _snap(combo2, EVID + "/combo_shop_furniture.png")
	if closer:
		var cl := _cam(Vector3(-8, 1.6, -2), Vector3(0, 0, 1), 7, 8)
		await _snap(cl, EVID + "/house_detail_extra.png")
	print("SHOTS_DONE")
	get_tree().quit(0)

func _perf_run() -> void:
	var csv := "group,sample,fps,frame_ms,vram_mb,objects\n"
	var groups := [
		["baseline", true, true], ["shadow_off", false, true],
		["anim_paused", true, false], ["veg_hidden", true, true],
	]
	for g in groups:
		_sun.shadow_enabled = g[1]
		for ap in _anim_players:
			ap.active = g[2]
		for v in _veg_nodes:
			v.visible = g[0] != "veg_hidden"
		for i in range(30):
			await get_tree().create_timer(0.5).timeout
			var fps := Performance.get_monitor(Performance.TIME_FPS)
			var vm := Performance.get_monitor(Performance.RENDER_VIDEO_MEM_USED) / 1048576.0
			var ob := Performance.get_monitor(Performance.RENDER_TOTAL_OBJECTS_IN_FRAME)
			csv += "%s,%d,%.0f,%.2f,%.1f,%d\n" % [g[0], i, fps, 1000.0/fps if fps > 0 else 0, vm, ob]
	var f := FileAccess.open(EVID + "/town_perf.csv", FileAccess.WRITE)
	f.store_string(csv)
	f.close()
	print("PERF_DONE")
	get_tree().quit(0)
