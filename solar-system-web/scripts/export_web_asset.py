"""Export one curated, web-sized GLB from a READ-ONLY source .blend.

Run: blender --background source.blend --python export_web_asset.py -- asset output.glb
No bpy save operation is performed. Texture changes exist only in this process.
"""
import bpy
import json
import math
import os
import sys
from array import array

ASSETS = {
    "sun": {"objects": ["Sol"], "surface": ("Sol", "sun.jpg", 2048)},
    "mercury": {"objects": ["Sphere"], "surface": ("Sphere", "Mercury_Texture_Map.webp", 2048)},
    "venus": {"objects": ["Venus", "Venus Clouds"], "surface": ("Venus", "venus_surface_8k.jpg", 4096), "cloud": ("Venus Clouds", "venus_cloud_4k.jpg", 2048)},
    "earth": {"objects": ["Earth", "Clouds", "Atmosphere"], "surface": ("Earth", "8081_earthmap10k.jpg.001", 4096), "night": ("8081_earthlights10k.jpg", 2048), "cloud": ("Clouds", "earthcloudmap.jpg", 1024, "earthcloudmaptrans.jpg"), "atmosphere": "Atmosphere"},
    "mars": {"objects": ["Mars", "Atmoshpere"], "surface": ("Mars", "5672_marsmap4k.jpg.001", 2048), "atmosphere": "Atmoshpere"},
    "jupiter": {"objects": ["Jupiter"], "surface": ("Jupiter", "Jupitermap_edited(3).jpg", 2048)},
    "saturn": {"objects": ["Sphere", "Circle"], "surface": ("Sphere", "saturn_planetary_texture_stock_image_by_uxmal750ad_d8f7djy.jpg", 2048), "ring": ("Circle", "Saturn rings.jpg", 1024)},
    "uranus": {"objects": ["Neptune", "Circle"], "surface": ("Neptune", "uranusmap.jpg", 1024), "ring": ("Circle", "uranusringcolour.jpg.001", 1024)},
    "neptune": {"objects": ["Uranus", "Clouds"], "surface": ("Uranus", "Uranus Textur.jpg", 2048), "cloud": ("Clouds", "clouds.jpg", 1024)},
}


def optimized_image(name, max_width, work_dir, alpha_from_luma=False, alpha_name=None):
    source = bpy.data.images.get(name)
    if not source or not source.size[0]:
        raise RuntimeError(f"Required packed texture unavailable: {name}")
    image = source.copy()
    image.name = "web_" + name
    width, height = image.size
    if width > max_width:
        image.scale(max_width, max(1, round(height * max_width / width)))
    if alpha_from_luma:
        # glTF expects the cloud/ring mask in the alpha channel of a color texture.
        # Most source shaders instead compute it from RGB through Blender-only nodes.
        import numpy as np
        rgba = np.array(image.pixels[:], dtype=np.float32).reshape((-1, 4))
        if alpha_name:
            alpha_img = bpy.data.images.get(alpha_name)
            if alpha_img and alpha_img.has_data:
                mask = alpha_img.copy()
                mask.scale(*image.size)
                mask_rgba = np.array(mask.pixels[:], dtype=np.float32).reshape((-1, 4))
                rgba[:, 3] = np.clip(mask_rgba[:, :3].mean(axis=1), 0, 1)
                bpy.data.images.remove(mask)
            else:
                rgba[:, 3] = np.clip(rgba[:, :3].mean(axis=1), 0, 1)
        else:
            rgba[:, 3] = np.clip(rgba[:, :3].mean(axis=1), 0, 1)
        derived = bpy.data.images.new("web_alpha_" + name, width=image.size[0], height=image.size[1], alpha=True)
        derived.pixels.foreach_set(rgba.ravel())
        bpy.data.images.remove(image)
        image = derived
        image.alpha_mode = "STRAIGHT"
        ext = "png"
        image.file_format = "PNG"
    else:
        ext = "jpg"
        image.file_format = "JPEG"
    path = os.path.join(work_dir, f"{len(os.listdir(work_dir)):02d}_{os.path.basename(name).split('.')[0]}.{ext}")
    image.filepath_raw = path
    image.save(quality=86) if ext == "jpg" else image.save()
    result = bpy.data.images.load(path, check_existing=False)
    result.name = "WEB_" + name
    bpy.data.images.remove(image)
    return result


def pbr_material(name, image, kind, emission_image=None):
    material = bpy.data.materials.new("WEB_" + name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = image
    tex.interpolation = "Linear"
    links = material.node_tree.links
    links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    bsdf.inputs["Roughness"].default_value = 0.9 if kind != "surface" else 0.78
    if kind == "sun":
        bsdf.inputs["Base Color"].default_value = (1, 0.55, 0.18, 1)
        links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
        bsdf.inputs["Emission Strength"].default_value = 1.0
    if emission_image:
        night_tex = nodes.new("ShaderNodeTexImage")
        night_tex.image = emission_image
        links.new(night_tex.outputs["Color"], bsdf.inputs["Emission Color"])
        bsdf.inputs["Emission Strength"].default_value = 0.45
    if kind in ("cloud", "ring"):
        links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
        material.surface_render_method = "BLENDED"
        material.use_nodes = True
        bsdf.inputs["Roughness"].default_value = 1.0
        if kind == "ring":
            material.use_backface_culling = False
    return material


def atmosphere_material(name, color):
    material = bpy.data.materials.new("WEB_" + name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Alpha"].default_value = 0.08
    bsdf.inputs["Roughness"].default_value = 1.0
    material.surface_render_method = "BLENDED"
    material.use_backface_culling = False
    material.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    return material


def set_material(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def ensure_spherical_uv(obj):
    """The Sun and Neptune use Generated coordinates, so add web UVs in memory."""
    mesh = obj.data
    if mesh.uv_layers:
        return
    from mathutils import Vector
    points = [v.co for v in mesh.vertices]
    center = sum(points, Vector()) / len(points)
    uv = mesh.uv_layers.new(name="Web spherical UV")
    for face in mesh.polygons:
        mapped = []
        for loop_index in face.loop_indices:
            vertex = mesh.vertices[mesh.loops[loop_index].vertex_index].co - center
            length = max(vertex.length, 1e-9)
            u = 0.5 + math.atan2(vertex.y, vertex.x) / (2 * math.pi)
            v = 0.5 + math.asin(max(-1, min(1, vertex.z / length))) / math.pi
            mapped.append((loop_index, u, v))
        if max(u for _,u,_ in mapped) - min(u for _,u,_ in mapped) > 0.5:
            mapped = [(i, u + 1 if u < 0.5 else u, v) for i,u,v in mapped]
        for loop_index, u, v in mapped:
            uv.data[loop_index].uv = (u, v)


def main():
    args = sys.argv[sys.argv.index("--") + 1:]
    key, output = args[:2]
    spec = ASSETS[key]
    missing = [name for name in spec["objects"] if name not in bpy.data.objects]
    if missing:
        raise RuntimeError(f"Missing required objects: {missing}")
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(output)))
    work_dir = os.path.join(project_dir, "scripts", "optimized-textures", key)
    os.makedirs(work_dir, exist_ok=True)

    # Delete unrelated scene objects only in memory; original .blend remains untouched.
    for obj in list(bpy.data.objects):
        if obj.name not in spec["objects"]:
            bpy.data.objects.remove(obj, do_unlink=True)
    for obj in bpy.data.objects:
        for mod in list(obj.modifiers):
            # The source spheres are smooth shaded. One level provides a rounded
            # silhouette without exporting high render-time subdivision levels.
            if mod.type == "SUBSURF" and obj.type == "MESH" and len(obj.data.polygons) <= 1200 and obj.name not in ("Circle",):
                mod.levels = 1
                mod.render_levels = 1
                mod.show_viewport = True
                mod.show_render = True
            else:
                obj.modifiers.remove(mod)
        if obj.type == "MESH":
            ensure_spherical_uv(obj)
            for face in obj.data.polygons:
                face.use_smooth = True

    surface_obj, surface_tex, surface_width = spec["surface"]
    surface_img = optimized_image(surface_tex, surface_width, work_dir)
    night_img = optimized_image(*spec["night"], work_dir) if "night" in spec else None
    set_material(bpy.data.objects[surface_obj], pbr_material(key + "_surface", surface_img, "sun" if key == "sun" else "surface", night_img))
    if "cloud" in spec:
        cloud_obj, cloud_tex, cloud_width, *alpha = spec["cloud"]
        cloud_img = optimized_image(cloud_tex, cloud_width, work_dir, True, alpha[0] if alpha else None)
        set_material(bpy.data.objects[cloud_obj], pbr_material(key + "_cloud", cloud_img, "cloud"))
    if "ring" in spec:
        ring_obj, ring_tex, ring_width = spec["ring"]
        ring_img = optimized_image(ring_tex, ring_width, work_dir, True)
        set_material(bpy.data.objects[ring_obj], pbr_material(key + "_ring", ring_img, "ring"))
    if "atmosphere" in spec:
        tint = (0.08, 0.3, 0.7) if key == "earth" else (0.4, 0.16, 0.09)
        set_material(bpy.data.objects[spec["atmosphere"]], atmosphere_material(key + "_atmosphere", tint))

    # Normalize imported coordinates. The Sun's source mesh is ~1391 Blender
    # units wide and translated -695 units; all chapter models become unit radius.
    from mathutils import Vector
    bpy.context.view_layer.update()
    # Use the planet surface as the unit sphere. Including wide ring meshes here
    # would make Saturn and Uranus look much smaller than their intended radii.
    surface = bpy.data.objects[surface_obj]
    corners = [surface.matrix_world @ Vector(corner) for corner in surface.bound_box]
    lo = Vector(tuple(min(c[i] for c in corners) for i in range(3)))
    hi = Vector(tuple(max(c[i] for c in corners) for i in range(3)))
    center = (lo + hi) / 2
    diameter = max(hi - lo)
    root = bpy.data.objects.new(key.upper() + "_ROOT", None)
    bpy.context.collection.objects.link(root)
    for obj in list(bpy.data.objects):
        if obj is root:
            continue
        world = obj.matrix_world.copy()
        obj.parent = root
        obj.matrix_world = world
    root.location = -center / diameter * 2
    root.scale = (2 / diameter,) * 3
    # The normalized group has diameter about 2, making it easy for Three.js
    # to apply presentation scale later.
    for obj in bpy.data.objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[surface_obj]
    bpy.ops.export_scene.gltf(filepath=output, export_format="GLB", use_selection=True, export_apply=True, export_yup=True, export_cameras=False, export_lights=False)
    with open(os.path.join(project_dir, "scripts", "export-" + key + ".json"), "w", encoding="utf-8") as f:
        json.dump({"asset": key, "source": bpy.data.filepath, "objects": spec["objects"], "triangle_count": sum(len(o.data.loop_triangles) for o in bpy.data.objects if o.type == "MESH"), "diameter_before_normalization": diameter, "textures": [f for f in os.listdir(work_dir)], "glb_bytes": os.path.getsize(output)}, f, indent=2)
    print("EXPORT_OK", key, os.path.getsize(output))


main()
