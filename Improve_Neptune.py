"""Run in Blender 4.x/5.x Text Editor with Neuptun Neu.blend open.
Creates a new scene, preserves original scenes, saves a uniquely named copy.
Procedural artistic approximation, not an observed or calibrated weather map.
Syntax checked only; Blender execution could not be verified in this environment.
"""
import bpy
import math
import os
from mathutils import Vector

if bpy.app.version < (4, 0, 0):
    raise RuntimeError('Please run this script in Blender 4.0 or newer.')
if not bpy.data.filepath:
    raise RuntimeError('Open your saved Neptune .blend first.')

source_path = bpy.data.filepath
original = bpy.context.scene
# The uploaded 2.79 file contains a planet object named Uranus.
source = next((o for o in original.objects if o.type == 'MESH' and o.name == 'Uranus'), None)
scene = bpy.data.scenes.new('Neptune • Realistic')
bpy.context.window.scene = scene

# Retain a copy of the original sphere when it is recognizably spherical.
usable = False
if source and len(source.data.vertices) > 100:
    coords = [v.co.copy() for v in source.data.vertices]
    center = sum(coords, Vector()) / len(coords)
    radii = [(c-center).length for c in coords]
    mean_radius = sum(radii) / len(radii)
    usable = mean_radius > 0 and min(radii) > mean_radius * 0.8 and max(radii) < mean_radius * 1.2
if usable:
    planet = bpy.data.objects.new('Neptune', source.data.copy())
    scene.collection.objects.link(planet)
    for v in planet.data.vertices:
        p = (v.co-center).normalized()
        v.co = (p.x, p.y, p.z * 0.9829)
    planet.data.update()
else:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=192, ring_count=96, radius=1)
    planet = bpy.context.object
    planet.name = 'Neptune'
    for v in planet.data.vertices:
        v.co.z *= 0.9829
for p in planet.data.polygons:
    p.use_smooth = True
planet.rotation_euler[1] = math.radians(-18)  # Presentation orientation, not orbital obliquity.
planet['description'] = 'Procedural visible-light approximation; cloud patterns are illustrative.'
planet.data.materials.clear()

mat = bpy.data.materials.new('Neptune • subtle blue-green cloud tops')
mat.use_nodes = True
planet.data.materials.append(mat)
n = mat.node_tree.nodes
l = mat.node_tree.links
n.clear()
def node(kind, name, x, y):
    a = n.new(kind); a.label = name; a.location = (x, y); return a
out = node('ShaderNodeOutputMaterial', 'Surface', 1100, 120)
bs = node('ShaderNodeBsdfPrincipled', 'Matte atmospheric cloud deck', 850, 120)
bs.inputs['Roughness'].default_value = 1
bs.inputs['Metallic'].default_value = 0
bs.inputs['Specular IOR Level'].default_value = 0.05
l.new(bs.outputs['BSDF'], out.inputs['Surface'])
tex = node('ShaderNodeTexCoord', 'Seamless spherical coordinates', -1100, 100)
scale = node('ShaderNodeVectorMath', 'Latitude-stretched turbulence', -870, 100)
scale.operation = 'MULTIPLY'
scale.inputs[1].default_value = (2, 2, 35)
l.new(tex.outputs['Generated'], scale.inputs[0])
noise = node('ShaderNodeTexNoise', 'Fine wind-sheared cloud bands', -650, 100)
noise.inputs['Scale'].default_value = 3
noise.inputs['Detail'].default_value = 5
noise.inputs['Roughness'].default_value = 0.65
l.new(scale.outputs['Vector'], noise.inputs['Vector'])
ramp = node('ShaderNodeValToRGB', 'Restrained natural colour palette', -400, 100)
ramp.color_ramp.elements[0].position = 0.18
ramp.color_ramp.elements[0].color = (0.23, 0.43, 0.50, 1)
ramp.color_ramp.elements[1].position = 0.82
ramp.color_ramp.elements[1].color = (0.35, 0.57, 0.62, 1)
l.new(noise.outputs['Fac'], ramp.inputs[0])
# Sparse pale high-altitude streaks; avoid terrain-like bump/displacement.
cloud = node('ShaderNodeTexNoise', 'Sparse methane-cloud streaks', -650, -210)
cloud.inputs['Scale'].default_value = 8
cloud.inputs['Detail'].default_value = 3
l.new(scale.outputs['Vector'], cloud.inputs['Vector'])
mask = node('ShaderNodeMapRange', 'Only brightest cloud features', -390, -200)
mask.clamp = True
mask.inputs['From Min'].default_value = 0.69
mask.inputs['From Max'].default_value = 0.82
mask.inputs['To Max'].default_value = 0.35
l.new(cloud.outputs['Fac'], mask.inputs['Value'])
mix = node('ShaderNodeMixRGB', 'Cloud-top colour', 400, 130)
mix.inputs[2].default_value = (0.67, 0.78, 0.80, 1)
l.new(mask.outputs['Result'], mix.inputs[0])
l.new(ramp.outputs['Color'], mix.inputs[1])
l.new(mix.outputs[0], bs.inputs['Base Color'])

# Thin scattering volume: illuminated haze rather than a self-lit neon rim.
atmo = bpy.data.objects.new('Neptune • atmospheric haze', planet.data.copy())
scene.collection.objects.link(atmo)
atmo.rotation_euler = planet.rotation_euler.copy()
atmo.scale = (1.008,)*3
atmo.data.materials.clear()
haze = bpy.data.materials.new('Neptune • scattering atmosphere')
haze.use_nodes = True
hn = haze.node_tree.nodes; hl = haze.node_tree.links
hn.clear()
hout = hn.new('ShaderNodeOutputMaterial')
scatter = hn.new('ShaderNodeVolumeScatter')
scatter.inputs['Color'].default_value = (0.44, 0.68, 0.82, 1)
scatter.inputs['Density'].default_value = 0.35
scatter.inputs['Anisotropy'].default_value = 0.15
hl.new(scatter.outputs[0], hout.inputs['Volume'])
atmo.data.materials.append(haze)

world = bpy.data.worlds.new('Neptune • black space')
world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (0, 0, 0, 1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0
scene.world = world
ld = bpy.data.lights.new('Sun • directional illumination', 'SUN')
ld.energy = 2.5  # Exposure-normalized for presentation, not irradiance at Neptune.
ld.angle = math.radians(0.018)
sun = bpy.data.objects.new('Sun • directional illumination', ld)
scene.collection.objects.link(sun)
sun.rotation_euler = Vector((0.6, 0.85, -0.4)).to_track_quat('-Z', 'Y').to_euler()
camdata = bpy.data.cameras.new('Neptune portrait')
cam = bpy.data.objects.new('Neptune portrait', camdata)
scene.collection.objects.link(cam)
cam.location = (0, -6, 1)
cam.rotation_euler = (-cam.location).to_track_quat('-Z', 'Y').to_euler()
camdata.type = 'ORTHO'; camdata.ortho_scale = 2.65
scene.camera = cam
scene.render.engine = 'CYCLES'
scene.cycles.samples = 128
scene.cycles.use_denoising = True
scene.cycles.volume_bounces = 2
scene.render.resolution_x = 1600
scene.render.resolution_y = 1600
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.view_settings.view_transform = 'AgX'
scene.view_settings.exposure = 0
scene.render.film_transparent = False

bpy.ops.object.select_all(action='DESELECT')
planet.select_set(True)
bpy.context.view_layer.objects.active = planet
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.region_3d.view_perspective = 'CAMERA'
            area.spaces.active.shading.type = 'MATERIAL'

notes = bpy.data.texts.new('READ ME — Neptune improvement')
notes.write('New procedural Neptune scene. Original scenes retained.\n'
            'Matte blue-green cloud deck, restrained bands, thin scattering haze,\n'
            'smooth oblate sphere, directional sunlight, black background.\n'
            'Cloud distribution is illustrative, not an observed weather map.\n'
            'This is an artistic approximation, not calibrated radiative transfer.\n'
            'Press F12 to render. Procedural materials require baking for GLB export.\n')
folder = os.path.dirname(source_path)
output = os.path.join(folder, 'Neptune_Improved.blend')
i = 2
while os.path.exists(output):
    output = os.path.join(folder, 'Neptune_Improved_%02d.blend' % i)
    i += 1
scene.render.filepath = os.path.splitext(output)[0] + '.png'
bpy.ops.wm.save_as_mainfile(filepath=output)
print('Saved:', output)
