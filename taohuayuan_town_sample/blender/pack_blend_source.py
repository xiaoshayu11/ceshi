"""Pack the final exported GLBs into one editable Blender source file."""
import bpy, os, glob
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GLBS = sorted(glob.glob(os.path.join(ROOT, "project", "assets", "models", "custom", "*.glb")))
bpy.ops.wm.read_factory_settings(use_empty=True)
for p in GLBS:
    bpy.ops.import_scene.gltf(filepath=p)
    name = os.path.splitext(os.path.basename(p))[0]
    # move imported roots apart for inspection
    for o in bpy.context.selected_objects:
        o.location.x += (len(name) % 7) * 1.5
out = os.path.join(ROOT, "blender", "town_sample_custom_assets.blend")
bpy.ops.wm.save_as_mainfile(filepath=out)
print("BLEND_PACKED", out, len(GLBS))
