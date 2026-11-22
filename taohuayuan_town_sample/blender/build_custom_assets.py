"""Build cute round low-poly custom assets for Taohuayuan town sample.
Blender 4.5 headless: blender -b -t 2 --python build_custom_assets.py
Output: ../assets/models/custom/*.glb  + asset_report.json
"""
import bpy, json, math, os
from mathutils import Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "assets", "models", "custom")
os.makedirs(OUT, exist_ok=True)

P = {
    "cream": "#EBD7B4", "bark_white": "#E6E1D6", "dirt": "#A98A61",
    "wood": "#9C7A5B", "wood_dark": "#7A5A3E", "stone": "#96A1A4",
    "stone_dark": "#6E7A7D", "green": "#7AA063", "green_dark": "#4A7355",
    "green_soft": "#A8C577", "flower": "#F0B9C4", "water": "#7FAFB4",
    "tile": "#5D707F", "tile_dark": "#485866", "tile_light": "#7A8D9B",
    "eye": "#3E5148",
}

def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)

def vcol(obj, color):
    m = obj.data
    for a in list(m.color_attributes):
        m.color_attributes.remove(a)
    ca = m.color_attributes.new(name="Col", type="BYTE_COLOR", domain="CORNER")
    c = rgb(P.get(color, color))
    flat = [x for _ in range(len(m.loops)) for x in c]
    ca.data.foreach_set("color", flat)
    m.color_attributes.active_color = ca

def mat_vc(name="M_VC_Town"):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Roughness"].default_value = 0.82
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Specular IOR Level"].default_value = 0.25
    vc = nt.nodes.new("ShaderNodeVertexColor")
    vc.layer_name = "Col"
    nt.links.new(vc.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m

VC = mat_vc()

def finish(obj, color, bevel=0.0, smooth=True):
    if bevel > 0:
        mod = obj.modifiers.new("bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 1
        mod.profile = 0.5
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
    if smooth:
        for p in obj.data.polygons:
            p.use_smooth = True
    vcol(obj, color)
    if VC.name not in [s.material.name for s in obj.material_slots if s.material]:
        obj.data.materials.append(VC)
    return obj

def box(name, loc, dim, color, bevel=0.04, rot=(0,0,0), smooth=True):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = dim
    o.rotation_euler = rot
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish(o, color, bevel, smooth)

def sphere(name, loc, radius, color, subs=1, scale=None, smooth=True):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subs, radius=radius, location=loc)
    o = bpy.context.object
    o.name = name
    if scale:
        o.scale = scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish(o, color, 0.0, smooth)

def cyl(name, loc, radius, depth, color, verts=8, rot=(0,0,0), bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    return finish(o, color, bevel, True)

def join(objs, name):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    objs[0].name = name
    return objs[0]

def clear():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

def roof_panels(group, width, depth, ridge_z, eave_z, overhang=0.34, slope_step=0.42):
    """Thin blue-grey tiled gable roof: 2 shell panels + ridges + eave caps."""
    run = depth / 2 + overhang
    rise = ridge_z - eave_z
    ang = math.atan2(rise, run) * 0.46
    slen = math.hypot(run, rise) + 0.16
    for side in (-1, 1):
        yc = side * run / 2
        zc = (ridge_z + eave_z) / 2
        panel = box("roof_shell_%s" % side, (0, yc, zc), (width + 0.55, slen, 0.13), "tile_dark", 0.045,
                    (side * ang, 0, 0), False)
        group.append(panel)
        n = max(5, int((width + 0.3) / slope_step))
        for i in range(n):
            x = -width / 2 - 0.12 + (i + 0.5) * (width + 0.24) / n
            r = box("tile_ridge_%s_%d" % (side, i), (x, yc, zc + 0.075), (0.085, slen - 0.05, 0.075),
                    "tile" if i % 3 else "tile_light", 0.035, (side * ang, 0, 0), True)
            group.append(r)
        # eave wave caps
        m = max(4, int(width / 0.95))
        for i in range(m):
            x = -width / 2 - 0.1 + (i + 0.5) * (width + 0.2) / m
            cap = sphere("eave_cap_%s_%d" % (side, i), (x, side * run, eave_z - 0.015), 0.065,
                         "tile_light", 1, (1.0, 0.75, 0.55))
            group.append(cap)
    ridge = cyl("ridge", (0, 0, ridge_z + 0.01), 0.11, width + 0.7, "tile_light", 10, (0, math.pi/2, 0), 0.03)
    group.append(ridge)
    for sx in (-1, 1):
        group.append(sphere("ridge_end_%s" % sx, (sx * (width/2 + 0.35), 0, ridge_z + 0.01), 0.135,
                            "tile_light", 1, (0.8, 1.0, 0.8)))

def window_front(group, x, z, w=0.72, h=0.72, y=-2.27):
    group.append(box("win_glow", (x, y, z), (w, 0.07, h), "cream", 0.03))
    for dx in (-w/2, w/2):
        group.append(box("win_frame_v", (x+dx, y-0.05, z), (0.10, 0.11, h+0.12), "wood", 0.035))
    for dz in (-h/2, h/2):
        group.append(box("win_frame_h", (x, y-0.05, z+dz), (w+0.12, 0.11, 0.10), "wood", 0.035))
    # minimal chinese lattice: two cross bars only
    group.append(box("lattice_v", (x, y-0.10, z), (0.055, 0.06, h-0.08), "wood_dark", 0.02))
    group.append(box("lattice_h", (x, y-0.10, z), (w-0.08, 0.06, 0.055), "wood_dark", 0.02))


def window_back(group, x, z, w=0.78, h=0.72, y=2.32):
    group.append(box("win_glow_back", (x, y, z), (w, 0.07, h), "cream", 0.03))
    for dx in (-w/2, w/2):
        group.append(box("win_frame_back_v", (x+dx, y+0.05, z), (0.10, 0.11, h+0.12), "wood", 0.035))
    for dz in (-h/2, h/2):
        group.append(box("win_frame_back_h", (x, y+0.05, z+dz), (w+0.12, 0.11, 0.10), "wood", 0.035))
    group.append(box("lattice_back", (x, y+0.09, z), (0.055, 0.06, h-0.10), "wood_dark", 0.02))

def lantern(group, x, y, z, s=1.0):
    group.append(sphere("lantern_body", (x, y, z), 0.19*s, "cream", 1, (1.0, 1.0, 0.78)))
    group.append(cyl("lantern_top", (x, y, z+0.15*s), 0.10*s, 0.05*s, "wood_dark", 8))
    group.append(cyl("lantern_bottom", (x, y, z-0.15*s), 0.10*s, 0.05*s, "wood_dark", 8))
    group.append(box("lantern_tassel", (x, y, z-0.24*s), (0.025*s, 0.025*s, 0.16*s), "flower", 0.01))

def build_house():
    clear(); g = []
    cream = box("walls", (0, 0, 1.45), (5.5, 4.5, 2.5), "cream", 0.22)
    g.append(cream)
    # rounded stone plinth
    for x in (-2.55, 2.55):
        g.append(box("plinth_side", (x, 0, 0.18), (0.36, 4.65, 0.36), "stone", 0.14))
    for y in (-2.18, 2.18):
        g.append(box("plinth_front", (0, y, 0.18), (5.2, 0.36, 0.36), "stone", 0.14))
    # door + porch
    g.append(box("door", (-0.7, -2.30, 1.10), (1.02, 0.14, 1.92), "wood_dark", 0.14))
    g.append(box("door_inner", (-0.7, -2.39, 1.16), (0.80, 0.06, 1.58), "wood", 0.12))
    g.append(sphere("door_knob", (-0.34, -2.47, 1.13), 0.055, "stone_dark", 1))
    for x in (-1.42, 0.02):
        g.append(cyl("porch_post", (x, -2.92, 1.20), 0.095, 2.30, "wood", 8, bevel=0.025))
    g.append(box("porch_beam", (-0.7, -2.92, 2.35), (1.7, 0.18, 0.16), "wood_dark", 0.05))
    g.append(box("porch_step", (-0.7, -2.75, 0.10), (1.65, 0.62, 0.18), "stone", 0.06))
    # windows
    window_front(g, 1.45, 1.52, 0.86, 0.82)
    g.append(box("side_window", (2.80, 0.55, 1.50), (0.08, 1.0, 0.78), "cream", 0.03))
    g.append(box("side_frame", (2.86, 0.55, 1.50), (0.06, 1.12, 0.90), "wood", 0.04))
    g.append(box("side_window2", (-2.80, 0.55, 1.50), (0.08, 1.0, 0.78), "cream", 0.03))
    g.append(box("side_frame2", (-2.86, 0.55, 1.50), (0.06, 1.12, 0.90), "wood", 0.04))
    window_back(g, -0.7, 1.55)
    window_back(g, 1.45, 1.55)
    g.append(box("back_door", (2.05, 2.37, 1.05), (0.85, 0.12, 1.80), "wood_dark", 0.10))
    # roof
    roof_panels(g, 5.5, 4.5, 3.72, 2.52)
    # small round window on front wall + chimney (roof stays light)
    g.append(sphere("round_window", (-1.65, -2.38, 1.85), 0.26, "water", 1, (1, 0.25, 1)))
    g.append(cyl("round_frame", (-1.65, -2.42, 1.85), 0.31, 0.06, "wood", 12, (math.pi/2, 0, 0)))
    g.append(box("chimney", (1.85, 0.9, 3.28), (0.45, 0.45, 0.62), "stone", 0.07))
    # lanterns + tiny blossom accents
    lantern(g, -1.55, -2.84, 2.05, 0.9)
    lantern(g, 1.55, -2.50, 2.05, 0.75)
    for i in range(6):
        x = 2.20 + 0.11 * (i % 3)
        y = -1.85 + 0.12 * i
        z = 0.45 + 0.06 * (i % 4)
        g.append(sphere("blossom_%d" % i, (x, y, z), 0.055, "flower", 1, (1, 1, 0.5)))
    obj = join(g, "custom_house")
    bpy.ops.object.select_all(action="DESELECT"); obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "custom_house.glb"), export_format="GLB",
                              use_selection=True, export_apply=True, export_materials="EXPORT",
                              export_yup=True, export_animations=False)
    return obj

def build_shop():
    clear(); g = []
    # open-front shop: back + side walls, counter, awning
    g.append(box("shop_back", (0, 1.9, 1.45), (6.8, 0.40, 2.5), "cream", 0.20))
    for x in (-3.2, 3.2):
        g.append(box("shop_side", (x, 0, 1.45), (0.40, 4.2, 2.5), "cream", 0.20))
    for x in (-3.2, 3.2):
        g.append(box("plinth", (x, 0, 0.18), (0.48, 4.4, 0.36), "stone", 0.14))
    g.append(box("back_plinth", (0, 1.9, 0.18), (6.4, 0.44, 0.36), "stone", 0.14))
    # counter + goods
    g.append(box("counter", (0, -1.45, 0.68), (5.3, 0.78, 0.30), "wood", 0.10))
    for x in (-2.0, 0, 2.0):
        g.append(box("counter_leg", (x, -1.45, 0.34), (0.22, 0.60, 0.65), "wood_dark", 0.06))
    for i, x in enumerate((-2.15, -1.55, 1.35, 2.05)):
        g.append(sphere("jar_%d" % i, (x, -1.42, 0.98), 0.21, "stone_dark" if i % 2 else "cream", 1, (1, 1, 1.25)))
        g.append(cyl("jar_lid_%d" % i, (x, -1.42, 1.22), 0.14, 0.06, "wood", 8))
    for i, x in enumerate((-0.9, -0.4, 0.4, 0.9)):
        g.append(sphere("fruit_%d" % i, (x, -1.50, 0.92 + (i%2)*0.12), 0.11, "flower", 1))
    # awning stripes
    for i in range(8):
        x = -2.97 + i * 0.85
        g.append(box("awning_%d" % i, (x, -2.42, 2.52), (0.83, 1.30, 0.09),
                     "cream" if i % 2 == 0 else "tile", 0.02, (math.radians(-11), 0, 0), False))
    g.append(box("awning_bar", (0, -3.00, 2.36), (6.9, 0.11, 0.11), "wood_dark", 0.04))
    for x in (-3.25, 3.25):
        g.append(cyl("awning_post", (x, -2.98, 1.23), 0.10, 2.45, "wood", 8, bevel=0.02))
    # signboard (gourd-like wooden sign)
    g.append(sphere("sign", (2.45, -2.98, 2.02), 0.30, "wood", 1, (0.85, 0.35, 1.15)))
    g.append(box("sign_hang", (2.45, -2.98, 2.38), (0.05, 0.05, 0.42), "wood_dark", 0.01))
    window_back(g, -1.6, 1.55, 0.9, 0.8)
    window_back(g, 1.6, 1.55, 0.9, 0.8)
    g.append(box("side_window_shop", (3.28, 0.6, 1.5), (0.08, 1.1, 0.8), "cream", 0.03))
    g.append(box("side_frame_shop", (3.34, 0.6, 1.5), (0.06, 1.22, 0.92), "wood", 0.04))
    # roof
    roof_panels(g, 6.8, 4.2, 3.95, 2.62)
    lantern(g, -2.6, -2.95, 2.15, 1.0)
    lantern(g, 2.0, -1.62, 2.10, 0.8)
    obj = join(g, "custom_shop")
    bpy.ops.object.select_all(action="DESELECT"); obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "custom_shop.glb"), export_format="GLB",
                              use_selection=True, export_apply=True, export_materials="EXPORT",
                              export_yup=True, export_animations=False)
    return obj

def animal_part(kind):
    """Return (body_objects, head_objects, ear_pivots, spec)."""
    body, head, ears = [], [], []
    if kind == "rabbit":
        body.append(sphere("body", (0, 0, 0.115), 0.125, "cream", 2, (0.85, 1.1, 0.92)))
        body.append(sphere("tail", (0, 0.14, 0.13), 0.045, "cream", 1))
        for x in (-0.075, 0.075):
            body.append(sphere("foot", (x, -0.055, 0.035), 0.042, "cream", 1, (0.9, 1.2, 0.65)))
        head.append(sphere("head", (0, -0.085, 0.255), 0.105, "cream", 2, (1.0, 0.95, 1.0)))
        head.append(sphere("nose", (0, -0.226, 0.238), 0.022, "flower", 1))
        for x in (-0.032, 0.032):
            head.append(sphere("eye", (x, -0.222, 0.278), 0.020, "eye", 1, (1.0, 0.45, 1.15)))
            head.append(sphere("eye_hl", (x-0.007, -0.229, 0.287), 0.008, "cream", 1))
            head.append(sphere("blush", (x*1.9, -0.214, 0.245), 0.018, "flower", 1, (1.0, 0.35, 0.7)))
        for x in (-0.045, 0.045):
            head.append(sphere("ear", (x, -0.055, 0.415), 0.045, "cream", 1, (0.62, 0.42, 1.85)))
            head.append(sphere("ear_inner", (x, -0.075, 0.425), 0.030, "flower", 1, (0.52, 0.28, 1.55)))
        spec = {"height": 0.42, "head_z": 0.255, "eye": 0.014}
    elif kind == "fox":
        body.append(sphere("body", (0, 0, 0.255), 0.215, "wood", 2, (0.78, 1.45, 0.82)))
        body.append(sphere("chest", (0, -0.20, 0.235), 0.13, "cream", 1, (0.85, 0.55, 1.0)))
        for x in (-0.14, 0.14):
            for y in (-0.19, 0.18):
                body.append(sphere("leg", (x, y, 0.085), 0.06, "wood_dark", 1, (0.8, 0.8, 1.35)))
        tail = sphere("tail", (0, 0.36, 0.30), 0.16, "wood", 2, (1.0, 1.55, 0.95))
        tail.rotation_euler.x = -0.28
        body.append(tail)
        body.append(sphere("tail_tip", (0, 0.54, 0.36), 0.10, "cream", 1))
        head.append(sphere("head", (0, -0.34, 0.485), 0.145, "wood", 2, (1.0, 0.92, 0.96)))
        head.append(sphere("muzzle", (0, -0.465, 0.445), 0.072, "cream", 1, (1.0, 1.1, 0.7)))
        head.append(sphere("nose", (0, -0.525, 0.452), 0.022, "wood_dark", 1))
        for x in (-0.055, 0.055):
            head.append(sphere("eye", (x, -0.460, 0.515), 0.023, "eye", 1, (1.0, 0.45, 1.0)))
            head.append(sphere("eye_hl", (x-0.007, -0.468, 0.525), 0.008, "cream", 1))
            head.append(sphere("blush", (x*1.75, -0.452, 0.478), 0.025, "flower", 1, (1.0, 0.35, 0.7)))
        for x in (-0.085, 0.085):
            head.append(sphere("ear", (x, -0.32, 0.675), 0.072, "wood", 1, (0.75, 0.45, 1.25)))
            head.append(sphere("ear_inner", (x, -0.346, 0.679), 0.044, "flower", 1, (0.65, 0.3, 1.2)))
        spec = {"height": 0.58, "head_z": 0.485, "eye": 0.023}
    else:  # calf
        body.append(sphere("body", (0, 0, 0.88), 0.51, "cream", 2, (0.72, 1.42, 0.86)))
        for x in (-0.28, -0.10, 0.12, 0.30):
            pass
        for x in (-0.27, 0.27):
            for y in (-0.48, 0.45):
                body.append(cyl("leg", (x, y, 0.30), 0.105, 0.60, "cream", 8, bevel=0.04))
                body.append(sphere("hoof", (x, y, 0.055), 0.10, "stone_dark", 1, (1, 1, 0.55)))
        body.append(sphere("patch", (0.22, 0.30, 1.24), 0.15, "green_soft", 1, (1.0, 1.2, 0.35)))
        body.append(sphere("tail", (0, 0.75, 0.95), 0.06, "cream", 1, (0.7, 1.7, 0.7)))
        head.append(sphere("head", (0, -0.82, 1.03), 0.28, "cream", 2, (1.05, 0.86, 1.0)))
        head.append(sphere("muzzle", (0, -1.02, 0.91), 0.19, "flower", 1, (1.0, 0.85, 0.62)))
        for x in (-0.075, 0.075):
            head.append(sphere("nostril", (x, -1.18, 0.94), 0.025, "wood_dark", 1))
        for x in (-0.15, 0.15):
            head.append(sphere("eye", (x, -1.035, 1.115), 0.055, "eye", 1, (1.0, 0.42, 1.0)))
            head.append(sphere("eye_hl", (x-0.015, -1.043, 1.135), 0.018, "cream", 1))
            head.append(sphere("blush", (x*1.8, -1.025, 1.045), 0.045, "flower", 1, (1.0, 0.35, 0.7)))
        for x in (-0.20, 0.20):
            head.append(sphere("horn", (x, -0.74, 1.30), 0.055, "wood", 1, (0.75, 0.75, 1.2)))
            head.append(sphere("ear", (x*1.35, -0.79, 1.22), 0.085, "cream", 1, (1.3, 0.5, 0.65)))
            head.append(sphere("ear_inner", (x*1.35, -0.83, 1.22), 0.055, "flower", 1, (1.2, 0.35, 0.55)))
        spec = {"height": 1.38, "head_z": 1.03, "eye": 0.055}
    return body, head, ears, spec

def build_animal(kind):
    clear()
    body, head, ears, spec = animal_part(kind)
    obj = join(body + head, "npc_%s" % kind)
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    # 单网格 + 单材质 + 顶点色；基础动作在 Godot 侧以节点级 idle/nod 实现，
    # 避免 glTF 父子空节点在 Godot 中的偏移，并保持零蒙皮开销。
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "npc_%s.glb" % kind), export_format="GLB",
                              use_selection=True, export_apply=True, export_materials="EXPORT",
                              export_yup=True, export_animations=False)
    tris = sum(len(p.vertices) - 2 for p in obj.data.polygons)
    return {"file": "npc_%s.glb" % kind, "tris": tris, "spec": spec}

def build_props():
    clear(); g = []
    # flower pot
    g.append(cyl("pot", (0, 0, 0.20), 0.22, 0.36, "wood", 10, bevel=0.04))
    g.append(cyl("pot_rim", (0, 0, 0.39), 0.26, 0.08, "wood_dark", 10, bevel=0.02))
    for i in range(5):
        a = i * math.tau / 5
        g.append(sphere("blossom", (0.11*math.cos(a), 0.11*math.sin(a), 0.55), 0.10, "flower", 1, (1,1,0.85)))
        g.append(box("stem", (0.06*math.cos(a), 0.06*math.sin(a), 0.46), (0.025,0.025,0.18), "green", 0.01))
    obj = join(g, "prop_flowerpot")
    bpy.ops.object.select_all(action="DESELECT"); obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "prop_flowerpot.glb"), export_format="GLB",
                              use_selection=True, export_apply=True, export_materials="EXPORT",
                              export_yup=True, export_animations=False)
    clear(); g = []
    # crate with rounded slats
    g.append(box("crate_body", (0,0,0.32), (0.72,0.62,0.62), "wood", 0.08))
    for z in (0.14, 0.32, 0.50):
        g.append(box("crate_slat", (0,-0.325,z), (0.68,0.05,0.055), "wood_dark", 0.02))
    obj = join(g, "prop_crate")
    bpy.ops.object.select_all(action="DESELECT"); obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "prop_crate.glb"), export_format="GLB",
                              use_selection=True, export_apply=True, export_materials="EXPORT",
                              export_yup=True, export_animations=False)

if __name__ == "__main__":
    report = {"assets": []}
    for fn in (build_house, build_shop, build_props):
        o = fn()
        if o:
            tris = sum(len(p.vertices) - 2 for p in o.data.polygons)
            report["assets"].append({"file": o.name + ".glb", "tris": tris})
    for kind in ("rabbit", "fox", "calf"):
        report["assets"].append(build_animal(kind))
    with open(os.path.join(ROOT, "blender", "asset_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print("CUSTOM_ASSETS_DONE", json.dumps(report, ensure_ascii=False))
