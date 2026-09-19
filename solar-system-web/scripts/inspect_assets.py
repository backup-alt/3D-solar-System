"""Read-only Blender inventory. Run once per source .blend in background mode."""
import bpy
import json
import os
import sys


def safe(value):
    try:
        return str(value)
    except Exception:
        return "<unavailable>"


def inspect():
    source = bpy.data.filepath
    objects = []
    for obj in bpy.data.objects:
        record = {
            "name": obj.name,
            "type": obj.type,
            "hidden_viewport": bool(obj.hide_viewport),
            "hidden_render": bool(obj.hide_render),
            "collections": [c.name for c in obj.users_collection],
            "parent": obj.parent.name if obj.parent else None,
            "children": [c.name for c in obj.children],
            "dimensions": [round(v, 4) for v in obj.dimensions],
            "location": [round(v, 4) for v in obj.location],
            "rotation_euler": [round(v, 4) for v in obj.rotation_euler],
            "scale": [round(v, 4) for v in obj.scale],
            "modifiers": [{"name": m.name, "type": m.type, "show_render": bool(m.show_render)} for m in obj.modifiers],
            "materials": [m.name if m else None for m in obj.data.materials] if hasattr(obj.data, "materials") else [],
            "animation": bool(obj.animation_data and (obj.animation_data.action or obj.animation_data.drivers or obj.animation_data.nla_tracks)),
        }
        if obj.type == "MESH":
            mesh = obj.data
            mesh.calc_loop_triangles()
            record.update(vertices=len(mesh.vertices), polygons=len(mesh.polygons), triangles=len(mesh.loop_triangles), uv_maps=[u.name for u in mesh.uv_layers])
        objects.append(record)

    materials = []
    for mat in bpy.data.materials:
        nodes = list(mat.node_tree.nodes) if mat.use_nodes and mat.node_tree else []
        materials.append({
            "name": mat.name,
            "blend_method": safe(getattr(mat, "surface_render_method", getattr(mat, "blend_method", "UNKNOWN"))),
            "alpha": round(mat.diffuse_color[3], 4),
            "node_types": [n.bl_idname for n in nodes],
            "image_nodes": [{"node": n.name, "image": n.image.name if n.image else None} for n in nodes if n.bl_idname == "ShaderNodeTexImage"],
            "emission_nodes": [n.name for n in nodes if "Emission" in n.bl_idname],
            "principled": any(n.bl_idname == "ShaderNodeBsdfPrincipled" for n in nodes),
        })

    images = []
    for img in bpy.data.images:
        path = bpy.path.abspath(img.filepath) if img.filepath else ""
        images.append({
            "name": img.name,
            "source": img.source,
            "file": img.filepath,
            "resolved_file": path,
            "exists": bool(path and os.path.exists(path)),
            "packed": bool(img.packed_file or img.packed_files),
            "width": img.size[0], "height": img.size[1],
            "channels": img.channels,
            "colorspace": img.colorspace_settings.name,
        })

    payload = {
        "source": source,
        "blender": bpy.app.version_string,
        "objects": objects,
        "materials": materials,
        "images": images,
        "totals": {"meshes": sum(o["type"] == "MESH" for o in objects), "triangles": sum(o.get("triangles", 0) for o in objects), "cameras": sum(o["type"] == "CAMERA" for o in objects), "lights": sum(o["type"] == "LIGHT" for o in objects), "empties": sum(o["type"] == "EMPTY" for o in objects)},
        "actions": [a.name for a in bpy.data.actions],
        "collections": [{"name": c.name, "objects": [o.name for o in c.objects]} for c in bpy.data.collections],
    }
    output = sys.argv[sys.argv.index("--") + 1]
    with open(output, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print("INSPECT_OK", output)


inspect()
