# recolor_mats.py — 按材质名重配色 GLB（WorkBuddy 实现；基于 inspect_mats 检查结果）
# 用法: blender --background --python recolor_mats.py -- <in.glb> <out.glb> Leaves=6FAE4E DarkGrey=C96846 ...
import bpy, sys, os

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
src, dst = argv[0], argv[1]
mapping = {}
for a in argv[2:]:
    name, hexcol = a.split("=", 1)
    mapping[name.lower()] = hexcol

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)

done = []
for mat in bpy.data.materials:
    key = None
    for m in mapping:
        if m in mat.name.lower():
            key = m
            break
    if key is None or not mat.use_nodes:
        continue
    b = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if not b:
        continue
    bc = b.inputs.get("Base Color")
    c = bc.default_value
    h = mapping[key]
    bc.default_value = (int(h[0:2], 16)/255.0, int(h[2:4], 16)/255.0,
                        int(h[4:6], 16)/255.0, c[3] if len(c) > 3 else 1.0)
    # 平色低模：微调粗糙度到哑光，风格更接近目标
    b.inputs.get("Roughness").default_value = 0.9
    done.append(mat.name)

bpy.ops.export_scene.gltf(filepath=dst, export_format='GLB', export_yup=True)
print(f"[recolor] {os.path.basename(src)} -> {os.path.basename(dst)} 改材质: {done}")
