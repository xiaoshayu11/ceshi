# process_glb.py — 《桃花源物语》GLB 资源批处理（Blender 4.x）
# 依据 Gemini 双 AI 协作 v2.0 模式 D：Gemini 提供脚本设计（在 hue 像素处理处被 2600 token 截断），
# WorkBuddy 审查后补全了 adjust_image_hsv / process_objects / main 的收尾实现，并对
# 像素循环性能、材质清理做了小改。执行：
#   blender --background --python process_glb.py -- --src <in_dir> --dst <out_dir> --scale 1.0 --sat 1.1 --val 1.03
import bpy
import os
import sys
import argparse
import colorsys


def parse_args():
    """解析 -- 之后的命令行参数"""
    argv = sys.argv
    argv = argv[argv.index("--") + 1:] if "--" in argv else []
    p = argparse.ArgumentParser(description="桃花源物语 GLB 批处理")
    p.add_argument("--src", required=True)
    p.add_argument("--dst", required=True)
    p.add_argument("--scale", type=float, default=1.0, help="统一缩放")
    p.add_argument("--hue_shift", type=float, default=0.0, help="色相偏移 -0.5~0.5")
    p.add_argument("--sat", type=float, default=1.0, help="饱和度乘数")
    p.add_argument("--val", type=float, default=1.0, help="明度乘数")
    p.add_argument("--apply_to", default="", help="逗号分隔材质名过滤，缺省全部")
    p.add_argument("--drop_ground", default="", help="逗号分隔对象名关键字，匹配者删除（如包内自带地板）")
    return p.parse_args(argv)


def adjust_color_hsv(rgba, h_shift, s_mult, v_mult):
    r, g, b, a = rgba
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h = (h + h_shift) % 1.0
    s = max(0.0, min(1.0, s * s_mult))
    v = max(0.0, min(1.0, v * v_mult))
    nr, ng, nb = colorsys.hsv_to_rgb(h, s, v)
    return (nr, ng, nb, a)


def process_materials(args):
    """按参数暖化/饱和化 Principled BSDF 底色或贴图像素"""
    if args.hue_shift == 0.0 and args.sat == 1.0 and args.val == 1.0:
        return
    flt = [n.strip().lower() for n in args.apply_to.split(",") if n.strip()]
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        if flt and not any(f in mat.name.lower() for f in flt):
            continue
        nodes = mat.node_tree.nodes
        bsdf = next((n for n in nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if not bsdf:
            continue
        bc = bsdf.inputs.get("Base Color")
        if not bc:
            continue
        if bc.is_linked:
            from_node = bc.links[0].from_node
            if from_node.type == 'TEX_IMAGE' and from_node.image:
                img = from_node.image
                if img.get("_hsv_done"):
                    continue
                px = list(img.pixels)
                # 逐像素 HSV 调整（stride 4）
                for i in range(0, len(px), 4):
                    px[i:i + 4] = adjust_color_hsv(px[i:i + 4], args.hue_shift, args.sat, args.val)
                img.pixels = px
                img.pack()
                img["_hsv_done"] = True
        else:
            bc.default_value = adjust_color_hsv(tuple(bc.default_value), args.hue_shift, args.sat, args.val)


def process_objects(args):
    """落地 + 统一缩放 + 删除指定对象"""
    from mathutils import Vector
    if args.drop_ground:
        keys = [k for k in args.drop_ground.split(",") if k]
        for ob in list(bpy.data.objects):
            if any(k in ob.name.lower() for k in keys):
                bpy.data.objects.remove(ob, do_unlink=True)
    # 应用旋转与缩放，保证 Godot 侧尺寸/朝向稳定
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if args.scale != 1.0:
        bpy.ops.object.select_all(action='SELECT')
        bpy.context.scene.objects.active = None
        for ob in bpy.data.objects:
            if ob.parent is None:
                ob.scale = (args.scale, args.scale, args.scale)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    # 落地：整体 min z 归 0
    bpy.context.view_layer.update()
    minz = 1e9
    for ob in bpy.data.objects:
        if ob.type == 'MESH':
            for c in ob.bound_box:
                minz = min(minz, (ob.matrix_world @ Vector(c)).z)
    if minz < 1e9 and abs(minz) > 1e-4:
        roots = [ob for ob in bpy.data.objects if ob.parent is None]
        for ob in roots:
            ob.location.z += -minz
        bpy.context.view_layer.update()


def main():
    args = parse_args()
    os.makedirs(args.dst, exist_ok=True)
    files = sorted(f for f in os.listdir(args.src) if f.lower().endswith(".glb"))
    print(f"[proc] {len(files)} 个 GLB 待处理")
    for fn in files:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=os.path.join(args.src, fn))
        process_materials(args)
        process_objects(args)
        out = os.path.join(args.dst, fn)
        bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', export_yup=True)
        print(f"[proc] 完成 {fn} -> {out}")
    print("[proc] 全部完成")


main()
