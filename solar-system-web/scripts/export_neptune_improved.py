"""Export the improved Neptune from Neptune_Improved_02.blend as a web GLB.

The improved Neptune uses a fully procedural material (noise bands, color
ramp, cloud streaks), which glTF cannot read. This script bakes that shader
into an equirectangular texture with Cycles, applies a textured PBR material,
normalizes coordinates and exports a self-contained GLB.

Run: blender --background Neptune_Improved_02.blend --python export_neptune_improved.py -- output.glb
No bpy save operation is performed. Only objects created in this process exist
in memory; the source .blend is never written.
"""
import bpy
import json
import math
import os
import sys

from mathutils import Vector


def spherical_uv(obj):
    """Deterministic equirectangular UVs from object-space vertex positions."""
    mesh = obj.data
    if mesh.uv_layers:
        old = mesh.uv_layers[0]
        mesh.uv_layers.remove(old)
    uv = mesh.uv_layers.new(name="Web spherical UV")
    points = [v.co for v in mesh.vertices]
    center = sum(points, Vector()) / len(points)
    for face in mesh.polygons:
        mapped = []
        for loop_index in face.loop_indices:
            vertex = mesh.vertices[mesh.loops[loop_index].vertex_index].co - center
            length = max(vertex.length, 1e-9)
            u = 0.5 + math.atan2(vertex.y, vertex.x) / (2 * math.pi)
            v = 0.5 + math.asin(max(-1, min(1, vertex.z / length))) / math.pi
            mapped.append((loop_index, u, v))
        if max(u for _, u, _ in mapped) - min(u for _, u, _ in mapped) > 0.5:
            mapped = [(i, u + 1 if u < 0.5 else u, v) for i, u, v in mapped]
        for loop_index, u, v in mapped:
            uv.data[loop_index].uv = (u, v)


def bake_procedural_surface(obj, width, height, work_dir):
    """Bake the object's procedural material into an equirect image via Cycles.

    The source shader is repointed so its computed color feeds an Emission
    node; baking type EMIT ignores lighting and captures the albedo exactly.
    """
    engine = bpy.context.scene.render.engine
    bpy.context.scene.render.engine = "CYCLES"
    bake_image = bpy.data.images.new("WEB_neptune_bake", width, height, alpha=False)

    base = obj.data.materials[0]
    mat = base.copy()
    mat.name = "WEB_BAKE_neptune"
    tree = mat.node_tree
    nodes = tree.nodes
    links = tree.links
    principled = next(n for n in nodes if n.bl_idname == "ShaderNodeBsdfPrincipled")
    output = next(n for n in nodes if n.bl_idname == "ShaderNodeOutputMaterial")
    feed = principled.inputs["Base Color"].links[0]

    emission = nodes.new("ShaderNodeEmission")
    emission.location = principled.location
    links.new(feed.from_socket, emission.inputs["Color"])
    nodes.remove(principled)
    # Removing the Principled node already detached the surface link.
    links.new(emission.outputs["Emission"], output.inputs["Surface"])

    img_node = nodes.new("ShaderNodeTexImage")
    img_node.image = bake_image
    nodes.active = img_node

    obj.data.materials.clear()
    obj.data.materials.append(mat)
    for o in list(bpy.data.objects):
        o.select_set(False)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.context.scene.cycles.samples = 16
    bpy.ops.object.bake(type="EMIT", pass_filter={"COLOR"}, margin=8, use_clear=True)

    path = os.path.join(work_dir, "00_neptune_baked.jpg")
    bake_image.file_format = "JPEG"
    bake_image.filepath_raw = path
    bake_image.save(quality=90)
    baked = bpy.data.images.load(path, check_existing=False)
    baked.name = "WEB_neptune"
    bpy.data.images.remove(bake_image)
    bpy.context.scene.render.engine = engine
    return baked


def pbr_material(name, image):
    material = bpy.data.materials.new("WEB_" + name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = image
    material.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    material.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    bsdf.inputs["Roughness"].default_value = 0.78
    return material


def main():
    args = sys.argv[sys.argv.index("--") + 1:]
    output = args[0]
    keep = ["Neptune"]
    missing = [name for name in keep if name not in bpy.data.objects]
    if missing:
        raise RuntimeError(f"Missing required objects: {missing}")
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(output)))
    work_dir = os.path.join(project_dir, "scripts", "optimized-textures", "neptune")
    os.makedirs(work_dir, exist_ok=True)

    # Delete unrelated scene objects only in memory; original .blend stays intact.
    for obj in list(bpy.data.objects):
        if obj.name not in keep:
            bpy.data.objects.remove(obj, do_unlink=True)
    obj = bpy.data.objects["Neptune"]
    for mod in list(obj.modifiers):
        obj.modifiers.remove(mod)

    spherical_uv(obj)
    for face in obj.data.polygons:
        face.use_smooth = True
    obj.data.update()

    baked = bake_procedural_surface(obj, 2048, 1024, work_dir)
    set_material = obj.data.materials
    set_material.clear()
    set_material.append(pbr_material("neptune_surface", baked))

    # Normalize coordinates so the web sphere has diameter about 2, matching
    # the rest of the pipeline and the presentation scale in Three.js.
    bpy.context.view_layer.update()
    corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    lo = Vector(tuple(min(c[i] for c in corners) for i in range(3)))
    hi = Vector(tuple(max(c[i] for c in corners) for i in range(3)))
    center = (lo + hi) / 2
    diameter = max(hi - lo)
    root = bpy.data.objects.new("NEPTUNE_ROOT", None)
    bpy.context.collection.objects.link(root)
    world = obj.matrix_world.copy()
    obj.parent = root
    obj.matrix_world = world
    root.location = -center / diameter * 2
    root.scale = (2 / diameter,) * 3

    for o in bpy.data.objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.gltf(filepath=output, export_format="GLB", use_selection=True, export_apply=True, export_yup=True, export_cameras=False, export_lights=False)
    payload = {
        "asset": "neptune",
        "source": bpy.data.filepath,
        "objects": keep,
        "triangle_count": len(obj.data.loop_triangles),
        "diameter_before_normalization": diameter,
        "textures": [f for f in os.listdir(work_dir)],
        "glb_bytes": os.path.getsize(output),
    }
    with open(os.path.join(project_dir, "scripts", "export-neptune.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print("EXPORT_OK", output, os.path.getsize(output))


main()