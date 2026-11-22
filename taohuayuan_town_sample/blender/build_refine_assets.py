"""第二轮视觉精修：定制池塘（顶点色深浅水）+ 重做小牛/统一NPC面部。
Blender 4.5 headless: blender -b -t 2 --python build_refine_assets.py
输出覆盖 ../project/assets/models/custom/{custom_pond,npc_calf,npc_rabbit,npc_fox}.glb
"""
import bpy, json, math, os
from mathutils import Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "project", "assets", "models", "custom")
os.makedirs(OUT, exist_ok=True)

P = {
    "cream": "#EBD7B4", "bark_white": "#E6E1D6", "dirt": "#A98A61",
    "wood": "#9C7A5B", "wood_dark": "#7A5A3E", "stone": "#96A1A4",
    "stone_dark": "#6E7A7D", "green": "#7AA063", "green_dark": "#4A7355",
    "green_soft": "#A8C577", "flower": "#F0B9C4", "water": "#7FAFB4",
    "tile": "#5D707F", "tile_dark": "#485866", "tile_light": "#7A8D9B",
    "eye": "#3E5148",
    # 精修新增色
    "water_shallow": "#6FB2B7", "water_mid": "#4A8F97", "water_deep": "#2E6872",
    "lily_green": "#6FA47A", "lily_light": "#8FC49A",
    "calf_cream": "#E9DDC6", "calf_patch": "#9FBE96",
    "muzzle": "#EFB5B2", "blush": "#E39A97", "horn": "#DCC18E",
}
def rgb(h):
    h = P.get(h, h).lstrip("#")
    return tuple(int(h[i:i+2],16)/255.0 for i in (0,2,4)) + (1.0,)

def mat_vc(name="M_VC_Town"):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Roughness"].default_value = 0.82
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Specular IOR Level"].default_value = 0.25
    vc = nt.nodes.new("ShaderNodeVertexColor"); vc.layer_name = "Col"
    nt.links.new(vc.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m
VC = mat_vc()

def finish(obj, color, smooth=True):
    m = obj.data
    for a in list(m.color_attributes): m.color_attributes.remove(a)
    ca = m.color_attributes.new(name="Col", type="BYTE_COLOR", domain="CORNER")
    c = rgb(color)
    ca.data.foreach_set("color", [x for _ in range(len(m.loops)) for x in c])
    m.color_attributes.active_color = ca
    if smooth:
        for p in m.polygons: p.use_smooth = True
    if VC.name not in [s.material.name for s in obj.material_slots if s.material]:
        m.materials.append(VC)
    return obj

def sphere(name, loc, radius, color, subs=1, scale=None, smooth=True):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subs, radius=radius, location=loc)
    o = bpy.context.object; o.name = name
    if scale:
        o.scale = scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish(o, color, smooth)

def cyl(name, loc, r_top, r_bot, depth, color, verts=10, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r_bot, radius2=r_top,
                                    depth=depth, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    return finish(o, color, True)

def clear():
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)

def join(objs, name):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join(); objs[0].name = name
    return objs[0]

def export(obj, fname):
    bpy.ops.object.select_all(action="DESELECT"); obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, fname), export_format="GLB",
                              use_selection=True, export_apply=True, export_materials="EXPORT",
                              export_yup=True, export_animations=False)
    return sum(len(p.vertices)-2 for p in obj.data.polygons)

# ---------------- 池塘：单网格三圈顶点色（浅→深），不规则岸线 ----------------
def build_pond():
    clear()
    N = 32
    rings = [(1.00, "water_shallow", -0.012), (0.74, "water_mid", 0.002), (0.38, "water_deep", 0.010)]
    base = 3.55
    verts, cols, uvs, faces = [], [], [], []
    def wob(a):
        return 1.0 + 0.13*math.sin(3*a + 0.4) + 0.075*math.sin(5*a + 1.1) + 0.03*math.sin(9*a + 0.2)
    for rf, col, h in rings:
        for i in range(N):
            a = i * math.tau / N
            r = base * rf * wob(a)
            x, y = math.cos(a)*r, math.sin(a)*r
            verts.append((x, y, h)); uvs.append((x/(base*2)+0.5, y/(base*2)+0.5)); cols.append(rgb(col))
    verts.append((0, 0, 0.014)); uvs.append((0.5, 0.5)); cols.append(rgb("water_deep"))
    ci = len(verts)-1
    for ri in range(len(rings)-1):
        for i in range(N):
            a = ri*N+i; b = ri*N+(i+1)%N; c = (ri+1)*N+i; d = (ri+1)*N+(i+1)%N
            faces.append((a, c, d)); faces.append((a, d, b))
    for i in range(N):
        faces.append((2*N+i, ci, 2*N+(i+1)%N))
    mesh = bpy.data.meshes.new("pond_mesh"); mesh.from_pydata(verts, [], faces); mesh.update()
    mesh.flip_normals()  # 绕序修正：法线朝上，避免 Godot 背面剔除
    obj = bpy.data.objects.new("custom_pond", mesh); bpy.context.collection.objects.link(obj)
    uv = mesh.uv_layers.new(name="UVMap")
    for li, lp in enumerate(mesh.loops): uv.data[li].uv = uvs[lp.vertex_index]
    for a in list(mesh.color_attributes): mesh.color_attributes.remove(a)
    ca = mesh.color_attributes.new(name="Col", type="BYTE_COLOR", domain="CORNER")
    for li, lp in enumerate(mesh.loops): ca.data[li].color = cols[lp.vertex_index]
    mesh.color_attributes.active_color = ca
    for p in mesh.polygons: p.use_smooth = True
    mesh.materials.append(VC)
    tris = export(obj, "custom_pond.glb")
    return {"file": "custom_pond.glb", "tris": tris, "type": "pond"}

# ---------------- NPC 面部统一：兔/狐微调 + 小牛重做 ----------------
def eyes(group, cx, cy, cz, r, hl, blush_r, bx, by, bz, eye_col="eye"):
    """统一眼睛风格：压扁大眼 + 左上高光 + 眼下外侧粉腮红。"""
    for x in (-cx, cx):
        group.append(sphere("eye", (x, cy, cz), r, eye_col, 1, (1.0, 0.42, 1.05)))
        group.append(sphere("eye_hl", (x-r*0.30, cy-r*0.30, cz+r*0.32), hl, "cream", 1, (1.0, 0.35, 1.0)))
        group.append(sphere("blush", (x*bx, by, bz), blush_r, "blush", 1, (1.2, 0.28, 0.8)))

def build_rabbit():
    clear(); g = []
    g.append(sphere("body", (0, 0, 0.115), 0.125, "cream", 2, (0.86, 1.1, 0.92)))
    g.append(sphere("tail", (0, 0.14, 0.13), 0.045, "cream", 1))
    for x in (-0.075, 0.075):
        g.append(sphere("foot", (x, -0.055, 0.035), 0.042, "cream", 1, (0.9, 1.2, 0.65)))
    g.append(sphere("head", (0, -0.085, 0.258), 0.112, "cream", 2, (1.0, 0.95, 1.0)))
    g.append(sphere("nose", (0, -0.230, 0.240), 0.024, "flower", 1))
    eyes(g, 0.033, -0.224, 0.282, 0.023, 0.008, 0.019, 1.85, -0.214, 0.246)
    for x in (-0.045, 0.045):
        g.append(sphere("ear", (x, -0.055, 0.415), 0.045, "cream", 1, (0.62, 0.42, 1.85)))
        g.append(sphere("ear_inner", (x, -0.075, 0.425), 0.030, "flower", 1, (0.52, 0.28, 1.55)))
    obj = join(g, "npc_rabbit")
    return {"file": "npc_rabbit.glb", "tris": export(obj, "npc_rabbit.glb"), "type": "npc"}

def build_fox():
    clear(); g = []
    g.append(sphere("body", (0, 0, 0.255), 0.215, "wood", 2, (0.78, 1.45, 0.82)))
    g.append(sphere("chest", (0, -0.20, 0.235), 0.13, "cream", 1, (0.85, 0.55, 1.0)))
    for x in (-0.14, 0.14):
        for y in (-0.19, 0.18):
            g.append(sphere("leg", (x, y, 0.085), 0.06, "wood_dark", 1, (0.8, 0.8, 1.35)))
    tail = sphere("tail", (0, 0.36, 0.30), 0.16, "wood", 2, (1.0, 1.55, 0.95))
    tail.rotation_euler.x = -0.28; g.append(tail)
    g.append(sphere("tail_tip", (0, 0.54, 0.36), 0.10, "cream", 1))
    g.append(sphere("head", (0, -0.34, 0.485), 0.155, "wood", 2, (1.0, 0.92, 0.96)))
    g.append(sphere("muzzle", (0, -0.475, 0.445), 0.078, "cream", 1, (1.0, 1.1, 0.7)))
    g.append(sphere("nose", (0, -0.535, 0.452), 0.024, "wood_dark", 1))
    eyes(g, 0.058, -0.470, 0.518, 0.026, 0.009, 0.026, 1.75, -0.452, 0.480)
    for x in (-0.085, 0.085):
        g.append(sphere("ear", (x, -0.32, 0.685), 0.075, "wood", 1, (0.75, 0.45, 1.25)))
        g.append(sphere("ear_inner", (x, -0.348, 0.689), 0.046, "flower", 1, (0.65, 0.3, 1.2)))
    obj = join(g, "npc_fox")
    return {"file": "npc_fox.glb", "tris": export(obj, "npc_fox.glb"), "type": "npc"}

def build_calf():
    """Gemini 方案：二头身团子，头大身圆腿短粗。脚底原点，Blender -Y 朝前。"""
    clear(); g = []
    # 身体：短胖圆团（原为细长胶囊）
    g.append(sphere("body", (0, 0.05, 0.52), 0.45, "calf_cream", 2, (0.92, 1.05, 0.88)))
    # 四肢：短粗象腿，上细下粗
    for x in (-0.20, 0.20):
        for y in (-0.22, 0.22):
            g.append(cyl("leg", (x, y, 0.14), 0.095, 0.115, 0.28, "calf_cream", 10))
            g.append(sphere("hoof", (x, y, 0.035), 0.10, "stone_dark", 1, (1.0, 1.0, 0.42)))
    # 斑块：柔和抹茶绿，不再廉价绿点
    g.append(sphere("patch", (0.20, 0.22, 0.68), 0.19, "calf_patch", 1, (1.0, 1.05, 0.45)))
    g.append(sphere("patch2", (-0.24, 0.16, 0.50), 0.12, "calf_patch", 1, (0.9, 0.9, 0.4)))
    g.append(sphere("tail", (0, 0.50, 0.60), 0.055, "calf_cream", 1, (0.7, 1.5, 0.7)))
    # 头：显著放大
    g.append(sphere("head", (0, -0.36, 0.78), 0.38, "calf_cream", 2, (1.08, 0.92, 0.98)))
    # 口鼻：宽厚粉吻覆盖下半脸
    g.append(sphere("muzzle", (0, -0.66, 0.70), 0.20, "muzzle", 1, (1.35, 0.65, 0.78)))
    for x in (-0.085, 0.085):
        g.append(sphere("nostril", (x, -0.785, 0.73), 0.026, "wood_dark", 1, (0.8, 0.5, 1.1)))
    # 统一眼睛风格：大眼+高光+腮红
    eyes(g, 0.17, -0.645, 0.86, 0.072, 0.022, 0.058, 1.62, -0.605, 0.765)
    # 圆钝小角 + 荷叶耳
    for x in (-0.16, 0.16):
        g.append(cyl("horn", (x, -0.31, 1.10), 0.020, 0.055, 0.11, "horn", 8))
        g.append(sphere("ear", (x*2.35, -0.33, 0.88), 0.115, "calf_cream", 1, (1.45, 0.42, 0.68)))
        g.append(sphere("ear_inner", (x*2.35, -0.37, 0.885), 0.070, "flower", 1, (1.25, 0.35, 0.55)))
    obj = join(g, "npc_calf")
    return {"file": "npc_calf.glb", "tris": export(obj, "npc_calf.glb"), "type": "npc"}

if __name__ == "__main__":
    report = {"assets": [build_pond(), build_rabbit(), build_fox(), build_calf()]}
    with open(os.path.join(ROOT, "blender", "refine_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print("REFINE_ASSETS_DONE", json.dumps(report, ensure_ascii=False))
