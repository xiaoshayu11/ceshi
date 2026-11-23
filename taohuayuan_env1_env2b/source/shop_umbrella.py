# 桃花源物语 — ENV-2② 镇商业建筑样板：杂货铺「伞盖顶」
# Gemini 协作产出（模式 D，2026-11-23），WorkBuddy 审查整合版：
#   - tag_of 改为仅 Wall_* 入碰撞组，Base_/Timber_/Door_/Step_/Decor_ 全部归 Decor
#     （石基/柱/门框/窗框不挡玩家，沿用 CuteShop「装饰零碰撞」口径）
#   - 窗玻璃改 Decor_ 前缀，避免薄片进入 Wall_All 碰撞
#   - bevel 段数 2→1、伞骨 16→10，控制三角面预算 ≤8000
# 用法: blender --background --python asset_lab/commercial/shop_umbrella.py
import bpy, bmesh, math, os
from mathutils import Vector

OUT_DIR = 'C:/Users/小鲨鱼/WorkBuddy/2026-11-20-13-28-35/asset_lab/commercial/'


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for m in list(bpy.data.meshes):
        bpy.data.meshes.remove(m)
    for m in list(bpy.data.materials):
        bpy.data.materials.remove(m)


def _srgb_to_linear(c):
    """glTF 导出会把 Base Color 由线性编码成 sRGB；这里先把目标 Godot
    观感色反解为线性，确保导入 Godot 后的 albedo 与 MODEL-1 口径一致。"""
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def mat(name, rgb, rough=0.8):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (
            _srgb_to_linear(rgb[0]), _srgb_to_linear(rgb[1]),
            _srgb_to_linear(rgb[2]), 1.0)
        bsdf.inputs["Roughness"].default_value = rough
    return m


def _apply_bevel(obj, width):
    if width <= 0:
        return
    mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod.width = width
    mod.segments = 1                      # 预算：每段 1 即可保留圆润观感
    mod.limit_method = 'ANGLE'
    mod.angle_limit = math.radians(35)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)


def _clamp_ground(obj):
    """任何顶点不低于 z=0（贴地不穿地）。"""
    mw = obj.matrix_world
    mwi = mw.inverted()
    for v in obj.data.vertices:
        wv = mw @ v.co
        if wv.z < 0.0:
            wv.z = 0.0
            v.co = mwi @ wv


def box(name, loc, size, material, rot=(0, 0, 0), bevel_w=0.03):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=size, verts=bm.verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = rot
    obj.data.materials.append(material)
    _apply_bevel(obj, bevel_w)
    bpy.context.view_layer.update()
    _clamp_ground(obj)
    return obj


def cyl(name, loc, radius, depth, material, verts=12, rot=(0, 0, 0), bevel_w=0.02):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=verts,
                          radius1=radius, radius2=radius, depth=depth)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = rot
    obj.data.materials.append(material)
    _apply_bevel(obj, bevel_w)
    bpy.context.view_layer.update()
    _clamp_ground(obj)
    return obj


def sphere(name, loc, radius, scale_xyz, material, u_segs=12, v_segs=8):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=u_segs, v_segments=v_segs, radius=radius)
    bmesh.ops.scale(bm, vec=scale_xyz, verts=bm.verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    obj.data.materials.append(material)
    for p in obj.data.polygons:
        p.use_smooth = True
    bpy.context.view_layer.update()
    _clamp_ground(obj)
    return obj


def make_window(prefix, center, rot_z, m_wood, m_glass, w=1.1, h=1.1):
    ft, fd = 0.08, 0.28
    # 玻璃归 Decor：不参与碰撞
    box(f"Decor_{prefix}_Glass", center, (w - ft, 0.04, h - ft), m_glass,
        rot=(0, 0, rot_z), bevel_w=0.005)
    ca, sa = math.cos(rot_z), math.sin(rot_z)

    def offset(dx, dy, dz):
        return (center[0] + dx * ca - dy * sa, center[1] + dx * sa + dy * ca,
                center[2] + dz)

    box(f"Timber_{prefix}_Top", offset(0, 0, h / 2 - ft / 2),
        (w + 0.08, fd, ft), m_wood, rot=(0, 0, rot_z), bevel_w=0.015)
    box(f"Timber_{prefix}_Bot", offset(0, 0, -h / 2 + ft / 2),
        (w + 0.14, fd + 0.06, ft * 1.2), m_wood, rot=(0, 0, rot_z), bevel_w=0.02)
    box(f"Timber_{prefix}_L", offset(-w / 2 + ft / 2, 0, 0),
        (ft, fd, h - ft), m_wood, rot=(0, 0, rot_z), bevel_w=0.015)
    box(f"Timber_{prefix}_R", offset(w / 2 - ft / 2, 0, 0),
        (ft, fd, h - ft), m_wood, rot=(0, 0, rot_z), bevel_w=0.015)
    # 预算：十字细框（12 件）已移除——保留外框四边即可读清窗户造型。



def umbrella_roof(m_roof, m_under, m_wood, m_stone):
    """轻薄伞盖：32 环向 × 6 径向，屋面厚 0.12~0.16m，四向对称。"""
    segs, rings = 32, 6
    # 已验收反馈修正：原 rx/ry 3.15/2.65 + 檐口 3.12m 在正式镜头下压墙、
    # 招牌被遮。缩小外挑（墙半宽 2.46/1.96 → 外挑 0.49/0.49）并把檐口
    # 抬到 3.43m；顶高 4.05m 仍在预算内。
    rx, ry = 2.95, 2.45
    z_apex, z_drop, thick = 4.05, 0.62, 0.13

    mesh = bpy.data.meshes.new("Roof_Canopy_Mesh")
    obj = bpy.data.objects.new("Roof_Canopy", mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(m_roof)
    obj.data.materials.append(m_under)

    bm = bmesh.new()
    top_rings, bot_rings = [], []
    for r in range(rings + 1):
        t = r / rings
        curve = (t ** 1.35) * (1.0 - 0.12 * (t ** 3)) / 0.88
        z_t = z_apex - z_drop * curve
        th = thick * (1.0 - 0.25 * t)
        z_b = z_t - th
        rad_t = max(0.04, t) if r > 0 else 0.001
        tr, br = [], []
        for s in range(segs):
            ang = 2.0 * math.pi * s / segs
            wave = 0.025 * math.cos(ang * 8) * (t ** 2)
            x, y = rx * rad_t * math.cos(ang), ry * rad_t * math.sin(ang)
            tr.append(bm.verts.new((x, y, z_t + wave)))
            br.append(bm.verts.new((x * 0.992, y * 0.992, z_b + wave)))
        top_rings.append(tr)
        bot_rings.append(br)

    for r in range(rings):
        for s in range(segs):
            sn = (s + 1) % segs
            ft = bm.faces.new((top_rings[r][s], top_rings[r + 1][s],
                               top_rings[r + 1][sn], top_rings[r][sn]))
            ft.material_index = 0
            ft.smooth = True
            fb = bm.faces.new((bot_rings[r][sn], bot_rings[r + 1][sn],
                               bot_rings[r + 1][s], bot_rings[r][s]))
            fb.material_index = 1
            fb.smooth = True
    for s in range(segs):
        sn = (s + 1) % segs
        fr = bm.faces.new((top_rings[rings][s], bot_rings[rings][s],
                           bot_rings[rings][sn], top_rings[rings][sn]))
        fr.material_index = 0
        fr.smooth = True
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()

    # 10 根放射伞骨（预算：原 16 根削到 10）
    for i in range(10):
        ang = 2.0 * math.pi * i / 10
        p0 = Vector((0, 0, z_apex - thick * 0.8))
        p1 = Vector((rx * 0.94 * math.cos(ang), ry * 0.94 * math.sin(ang),
                     z_apex - z_drop - thick * 0.5))
        vec = p1 - p0
        yaw = math.atan2(vec.y, vec.x)
        pitch = -math.asin(vec.z / vec.length)
        box(f"Roof_Rib_{i}", (p0 + p1) * 0.5, (vec.length, 0.055, 0.065),
            m_wood, rot=(0, pitch, yaw), bevel_w=0.01)

    cyl("Roof_Finial_Base", (0, 0, z_apex + 0.03), 0.26, 0.08, m_wood,
        verts=16, bevel_w=0.02)
    sphere("Roof_Finial_Knob", (0, 0, z_apex + 0.11), 0.12, (1, 1, 0.85),
           m_roof, u_segs=12, v_segs=8)

    # 4 根暖木檐柱（Decor 组，零碰撞，不阻碍绕行）
    idx = 0
    for px in (-2.68, 2.68):
        for py in (-2.18, 2.18):
            idx += 1
            cyl(f"Base_PillarStone_{idx}", (px, py, 0.12), 0.17, 0.24,
                m_stone, verts=12, bevel_w=0.03)
            cyl(f"Timber_Pillar_{idx}", (px, py, 1.77), 0.11, 3.30,
                m_wood, verts=12, bevel_w=0.015)
            box(f"Roof_PillarCap_{idx}", (px, py, 3.36), (0.30, 0.30, 0.10),
                m_wood, bevel_w=0.02)
            sx, sy = (-1 if px > 0 else 1), (-1 if py > 0 else 1)
            box(f"Roof_Brace_{idx}", (px + sx * 0.18, py + sy * 0.18, 3.10),
                (0.48, 0.07, 0.08), m_wood,
                rot=(0, math.radians(-35), math.atan2(sy, sx)), bevel_w=0.015)


def build_shop():
    # 色板口径 = 期望 Godot 最终 albedo（mat() 内反解为线性再导出）
    m_wall = mat("Mat_Wall", (0.955, 0.93, 0.85), 0.85)
    m_wood = mat("Mat_Wood", (0.62, 0.50, 0.38), 0.75)
    m_roof = mat("Mat_Roof", (0.51, 0.53, 0.56), 0.70)
    m_under = mat("Mat_Under", (0.64, 0.72, 0.74), 0.80)
    m_stone = mat("Mat_Stone", (0.82, 0.80, 0.72), 0.85)
    m_red = mat("Mat_Red", (0.78, 0.24, 0.20), 0.60)
    m_glass = mat("Mat_Glass", (0.72, 0.84, 0.86), 0.25)

    # 石基/台阶（Decor，不挡路）
    box("Base_Floor", (0, 0, 0.05), (5.10, 4.10, 0.10), m_stone, bevel_w=0.02)
    box("Base_Curb_FL", (-1.75, -1.96, 0.13), (1.86, 0.36, 0.26), m_stone, bevel_w=0.03)
    box("Base_Curb_FR", (1.75, -1.96, 0.13), (1.86, 0.36, 0.26), m_stone, bevel_w=0.03)
    box("Base_Curb_Back", (0, 1.96, 0.13), (5.36, 0.36, 0.26), m_stone, bevel_w=0.03)
    box("Base_Curb_L", (-2.46, 0, 0.13), (0.36, 3.60, 0.26), m_stone, bevel_w=0.03)
    box("Base_Curb_R", (2.46, 0, 0.13), (0.36, 3.60, 0.26), m_stone, bevel_w=0.03)
    box("Step_Stone_1", (0, -2.18, 0.05), (1.92, 0.44, 0.10), m_stone, bevel_w=0.025)
    box("Step_Stone_2", (0, -1.96, 0.06), (1.68, 0.34, 0.12), m_stone, bevel_w=0.02)

    # 墙体：仅 Wall_* 参与碰撞；正面门洞 X∈[-0.8,0.8] / Z∈[0.26,2.2] 真实留空
    box("Wall_Front_L", (-1.70, -1.96, 1.63), (1.80, 0.22, 2.74), m_wall, bevel_w=0.03)
    box("Wall_Front_R", (1.70, -1.96, 1.63), (1.80, 0.22, 2.74), m_wall, bevel_w=0.03)
    box("Wall_Front_Top", (0, -1.96, 2.60), (1.66, 0.22, 0.80), m_wall, bevel_w=0.03)
    box("Wall_Back", (0, 1.96, 1.63), (5.10, 0.22, 2.74), m_wall, bevel_w=0.03)
    box("Wall_Left", (-2.46, 0, 1.63), (0.22, 3.74, 2.74), m_wall, bevel_w=0.03)
    box("Wall_Right", (2.46, 0, 1.63), (0.22, 3.74, 2.74), m_wall, bevel_w=0.03)

    for ix, cx in enumerate((-2.46, 2.46)):
        for iy, cy in enumerate((-1.96, 1.96)):
            box(f"Timber_Corner_{ix}_{iy}", (cx, cy, 1.63),
                (0.28, 0.28, 2.76), m_wood, bevel_w=0.04)
    box("Timber_Beam_F", (0, -1.96, 2.98), (5.24, 0.28, 0.14), m_wood, bevel_w=0.025)
    box("Timber_Beam_B", (0, 1.96, 2.98), (5.24, 0.28, 0.14), m_wood, bevel_w=0.025)
    box("Timber_Beam_L", (-2.46, 0, 2.98), (0.28, 4.18, 0.14), m_wood, bevel_w=0.025)
    box("Timber_Beam_R", (2.46, 0, 2.98), (0.28, 4.18, 0.14), m_wood, bevel_w=0.025)

    box("Door_Jamb_L", (-0.85, -1.96, 1.15), (0.10, 0.30, 2.30), m_wood, bevel_w=0.02)
    box("Door_Jamb_R", (0.85, -1.96, 1.15), (0.10, 0.30, 2.30), m_wood, bevel_w=0.02)
    box("Door_Lintel", (0, -1.96, 2.26), (1.96, 0.32, 0.12), m_wood, bevel_w=0.025)
    box("Door_Bracket_L", (-0.72, -1.96, 2.12), (0.18, 0.24, 0.16), m_wood, bevel_w=0.03)
    box("Door_Bracket_R", (0.72, -1.96, 2.12), (0.18, 0.24, 0.16), m_wood, bevel_w=0.03)

    make_window("Win_FL", (-1.68, -1.96, 1.55), 0.0, m_wood, m_glass, 0.88, 0.92)
    make_window("Win_FR", (1.68, -1.96, 1.55), 0.0, m_wood, m_glass, 0.88, 0.92)
    make_window("Win_Left", (-2.46, 0, 1.60), math.pi / 2, m_wood, m_glass, 1.35, 1.15)
    make_window("Win_Right", (2.46, 0, 1.60), math.pi / 2, m_wood, m_glass, 1.35, 1.15)
    make_window("Win_Back_L", (-1.15, 1.96, 1.60), 0.0, m_wood, m_glass, 1.15, 1.10)
    make_window("Win_Back_R", (1.15, 1.96, 1.60), 0.0, m_wood, m_glass, 1.15, 1.10)
    box("Timber_Back_Waist", (0, 2.08, 0.92), (4.80, 0.06, 0.08), m_wood, bevel_w=0.015)

    umbrella_roof(m_roof, m_under, m_wood, m_stone)

    # 装饰：木招牌（文字由 Godot 侧 Label3D 补）+ 一对小红灯笼 + 柜台/货物 + 背面货架
    box("Decor_Sign_Board", (0, -2.18, 2.66), (1.52, 0.08, 0.42), m_wood, bevel_w=0.025)
    box("Decor_Sign_TrimT", (0, -2.18, 2.88), (1.60, 0.11, 0.05), m_wood, bevel_w=0.015)
    box("Decor_Sign_TrimB", (0, -2.18, 2.44), (1.60, 0.11, 0.05), m_wood, bevel_w=0.015)
    box("Decor_Sign_HangerL", (-0.55, -2.12, 2.94), (0.06, 0.18, 0.14), m_wood, bevel_w=0.01)
    box("Decor_Sign_HangerR", (0.55, -2.12, 2.94), (0.06, 0.18, 0.14), m_wood, bevel_w=0.01)
    for side, lx in (("L", -1.12), ("R", 1.12)):
        ly = -2.18
        box(f"Decor_Lantern_Arm_{side}", (lx, -2.08, 2.48), (0.06, 0.28, 0.06), m_wood, bevel_w=0.01)
        cyl(f"Decor_Lantern_Cord_{side}", (lx, ly, 2.38), 0.015, 0.18, m_wood, verts=8, bevel_w=0)
        sphere(f"Decor_Lantern_Body_{side}", (lx, ly, 2.18), 0.18, (1, 1, 1.12), m_red, 12, 8)
        cyl(f"Decor_Lantern_CapT_{side}", (lx, ly, 2.36), 0.09, 0.04, m_wood, verts=12, bevel_w=0.008)
        cyl(f"Decor_Lantern_CapB_{side}", (lx, ly, 2.00), 0.08, 0.04, m_wood, verts=12, bevel_w=0.008)
        cyl(f"Decor_Lantern_Tassel_{side}", (lx, ly, 1.90), 0.025, 0.16, m_red, verts=8, bevel_w=0.005)

    box("Decor_Counter_Top", (-1.68, -2.26, 0.72), (1.16, 0.42, 0.06), m_wood, bevel_w=0.02)
    box("Decor_Counter_LegL", (-2.16, -2.26, 0.36), (0.08, 0.36, 0.72), m_wood, bevel_w=0.015)
    box("Decor_Counter_LegR", (-1.20, -2.26, 0.36), (0.08, 0.36, 0.72), m_wood, bevel_w=0.015)
    box("Decor_Counter_Shelf", (-1.68, -2.26, 0.28), (1.04, 0.34, 0.05), m_wood, bevel_w=0.01)
    sphere("Decor_Jar_1", (-1.90, -2.26, 0.87), 0.13, (1, 1, 1.15), m_stone, 12, 8)
    cyl("Decor_Jar_Lid_1", (-1.90, -2.26, 1.02), 0.08, 0.04, m_red, verts=10, bevel_w=0.01)
    sphere("Decor_Jar_2", (-1.52, -2.24, 0.85), 0.11, (1, 1, 1.10), m_stone, 12, 8)
    cyl("Decor_Jar_Lid_2", (-1.52, -2.24, 0.98), 0.07, 0.03, m_wood, verts=10, bevel_w=0.008)
    box("Decor_Crate_1", (1.52, -2.26, 0.22), (0.46, 0.42, 0.44), m_wood, rot=(0, 0, 0.08), bevel_w=0.02)
    box("Decor_Crate_2", (1.56, -2.24, 0.58), (0.36, 0.34, 0.30), m_wood, rot=(0, 0, -0.12), bevel_w=0.02)
    cyl("Decor_Barrel_F", (2.06, -2.24, 0.28), 0.20, 0.56, m_wood, verts=12, bevel_w=0.025)
    box("Decor_BackRack_PostL", (-0.36, 2.24, 0.55), (0.07, 0.36, 1.10), m_wood, bevel_w=0.015)
    box("Decor_BackRack_PostR", (0.36, 2.24, 0.55), (0.07, 0.36, 1.10), m_wood, bevel_w=0.015)
    box("Decor_BackRack_Board1", (0, 2.24, 0.35), (0.86, 0.38, 0.05), m_wood, bevel_w=0.015)
    box("Decor_BackRack_Board2", (0, 2.24, 0.85), (0.86, 0.38, 0.05), m_wood, bevel_w=0.015)
    sphere("Decor_BackJar", (0, 2.24, 1.02), 0.14, (1, 1, 1.1), m_stone, 12, 8)


def tag_of(name):
    """仅真实墙体进碰撞；柱/台阶/门框/窗框/装饰零碰撞（同 CuteShop 口径）。"""
    if name.startswith("Roof_"):
        return "Roof"
    if name.startswith("Wall_"):
        return "Wall"
    return "Decor"


def join_by_tag(tag):
    objs = [o for o in bpy.context.scene.objects
            if o.type == 'MESH' and tag_of(o.name) == tag]
    if not objs:
        return None
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    merged = bpy.context.view_layer.objects.active
    merged.name = f"{tag}_All"
    merged.data.name = f"{tag}_All_Mesh"
    # 烘变换：GLB 节点 identity，Godot AABB/碰撞简单
    merged.data.transform(merged.matrix_world)
    merged.matrix_world.identity()
    _clamp_ground(merged)
    return merged


def main():
    clear_scene()
    build_shop()
    for tag in ("Wall", "Roof", "Decor"):
        join_by_tag(tag)

    os.makedirs(OUT_DIR, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, "shop_umbrella.blend"))
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT_DIR, "shop_umbrella.glb"),
                              export_format='GLB', export_apply=True)

    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    per_group = {o.name: sum(len(p.vertices) - 2 for p in o.data.polygons)
                 for o in meshes}
    total_tris = sum(per_group.values())
    print(f"[STATS] tris={total_tris} objects={len(meshes)} materials={len(bpy.data.materials)}")
    print(f"[STATS] groups={per_group}")
    assert total_tris <= 8000, f"Triangle count {total_tris} exceeds 8000"
    assert len(meshes) == 3, f"Expected 3 merged meshes, got {len(meshes)}"


if __name__ == '__main__':
    main()
