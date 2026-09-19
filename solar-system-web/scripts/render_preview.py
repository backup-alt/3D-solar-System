"""Render imported GLBs for material QA, without touching source Blender files."""
import bpy
import math
import os
import sys
from mathutils import Vector

key, folder = sys.argv[sys.argv.index('--')+1:][:2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.join(folder, key + '.glb'))
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 16
scene.render.resolution_x = 640
scene.render.resolution_y = 640
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False
scene.world = bpy.data.worlds.new('Preview background')
scene.world.color = (0.015, 0.018, 0.026)
camera_data = bpy.data.cameras.new('Preview camera')
camera = bpy.data.objects.new('Preview camera', camera_data)
scene.collection.objects.link(camera)
camera.location = (0, -5.8 if key in ('saturn','uranus') else -4.3, 2.5 if key in ('saturn','uranus') else 1.3)
camera.rotation_euler = (Vector((0, 0, 0)) - camera.location).to_track_quat('-Z','Y').to_euler()
camera_data.type = 'ORTHO'
camera_data.ortho_scale = 6.2 if key in ('saturn','uranus') else 2.9
scene.camera = camera
light_data = bpy.data.lights.new('Preview sunlight','AREA')
light_data.energy = 450
light_data.shape = 'DISK'
light_data.size = 4
light = bpy.data.objects.new('Preview sunlight',light_data)
scene.collection.objects.link(light)
light.location = (-3,-4,4)
out = os.path.join(os.path.dirname(os.path.dirname(folder)),'scripts','previews',key+'.png')
os.makedirs(os.path.dirname(out),exist_ok=True)
scene.render.filepath = out
bpy.ops.render.render(write_still=True)
print('PREVIEW_OK',key,out)
