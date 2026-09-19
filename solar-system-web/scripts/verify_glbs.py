"""Import every exported GLB in Blender and record what survived glTF export."""
import bpy
import json
import os
import sys

folder = sys.argv[sys.argv.index("--") + 1]
results = {}
for filename in sorted(os.listdir(folder)):
    if not filename.endswith(".glb"):
        continue
    bpy.ops.wm.read_factory_settings(use_empty=True)
    path = os.path.join(folder, filename)
    result = bpy.ops.import_scene.gltf(filepath=path)
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    count = 0
    for obj in meshes:
        obj.data.calc_loop_triangles()
        count += len(obj.data.loop_triangles)
    materials = [m.name for m in bpy.data.materials]
    images = [{"name": image.name, "width": image.size[0], "height": image.size[1]} for image in bpy.data.images]
    results[filename] = {"imported": "FINISHED" in result, "objects": [o.name for o in bpy.data.objects], "meshes": len(meshes), "triangles": count, "materials": materials, "images": images, "bytes": os.path.getsize(path)}
    print("VERIFY_OK", filename, len(meshes), count, len(images))
with open(os.path.join(os.path.dirname(os.path.dirname(folder)), "scripts", "validation.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
