# Asset report

Generated from read-only inspection of the nine original Blender files with Blender 5.2.2 LTS at `E:\Apps\Blender\blender.exe`. The brief named `E:\solar 3d site`, but the files actually exist in `E:\solor 3d site`. All output is in this project's directory. Source .blend files were opened headlessly and never saved.

## Web exports

| Asset | Original scene tris | Relevant source tris | GLB tris | Source texture(s) | GLB size | Exported meshes |
|---|---:|---:|---:|---|---:|---:|
| sun | 9,796 | 1,088 | 4,480 | sun.jpg (4096×2048) | 0.47 MiB | Sol |
| mercury | 16,832 | 960 | 3,968 | Mercury_Texture_Map.webp (4096×2048) | 0.74 MiB | Sphere |
| venus | 8,448 | 8,448 | 8,448 | venus_surface_8k.jpg (8192×4096)<br>venus_cloud_4k.jpg (4096×2048) | 4.99 MiB | Venus, Venus Clouds |
| earth | 15,616 | 5,888 | 11,904 | 8081_earthmap10k.jpg.001 (10800×5400)<br>8081_earthlights10k.jpg (10800×5400)<br>earthcloudmap.jpg (1024×512) | 2.22 MiB | Earth, Clouds, Atmosphere |
| mars | 17,792 | 1,920 | 7,936 | 5672_marsmap4k.jpg.001 (4000×2000) | 0.61 MiB | Mars, Atmoshpere |
| jupiter | 23,680 | 15,872 | 15,872 | Jupitermap_edited(3).jpg (3601×1801) | 0.66 MiB | Jupiter |
| saturn | 16,960 | 1,088 | 4,096 | saturn_planetary_texture_stock_image_by_uxmal750ad_d8f7djy.jpg (4096×2048)<br>Saturn rings.jpg (1035×582) | 0.30 MiB | Sphere, Circle |
| uranus | 17,088 | 1,216 | 4,224 | uranusmap.jpg (1024×512)<br>uranusringcolour.jpg.001 (1024×72) | 0.12 MiB | Neptune, Circle |
| neptune | 30,720 | 15,360 | 15,360 | Uranus Textur.jpg (2048×1024)<br>clouds.jpg (2048×1024) | 0.98 MiB | Uranus, Clouds |

All nine GLBs were imported into a clean Blender scene after export. Total transfer size is 11.08 MiB; progressive loading is required for the website. A GLB is self-contained, including the optimized textures. Surface images are limited to 1–4K; cloud and ring masks are 1–2K.

## Inspection details

The complete per-object, per-material and per-image inventories are in `scripts/inventory-*.json`; post-export import results are in `scripts/validation.json`. Source images marked “missing” below generally have zero dimensions and refer to unused external paths; the exported materials use packed images with valid dimensions. Blender-only node effects were converted as described for each asset.

### Sun — Solar System Assets.blend

- **Kept:** Sol (1,088 tris, 0 UV maps).
- **Excluded:** Camera (camera), Luna (mesh), Marte (mesh), Mercurio (mesh), Plane (mesh), Plane.001 (mesh), Sun (light), Tierra (mesh), TierraAtmosfera (mesh), TierraNuves (mesh), Venus (mesh), Venus Atmofera (mesh). Scene totals: 1 cameras, 1 lights, 0 empties.
- **Source materials:** Sol [ShaderNodeTexImage, ShaderNodeBump, ShaderNodeEmission, ShaderNodeEmission, ShaderNodeTexImage, ShaderNodeMixShader, ShaderNodeDisplacement; DITHERED; alpha 1].
- **Source images:** 2k_venus_atmosphere.jpg 2048×1024 packed; earth_clouds.jpg 8192×4096 packed; earth_daymap.jpg 8192×4096 packed; earth_nightmap.jpg 8192×4096 packed; earth_normal_map.tif 8192×4096 packed; earth_specular_map.tif 8192×4096 packed; mars.jpg 8192×4096 packed; mercury.jpg 8192×4096 packed; moon.jpg 8192×4096 packed; stars_milky_way.jpg 8192×4096 packed; sun.jpg 4096×2048 packed; venus_surface.jpg 8192×4096 packed; all other image datablocks are listed in inventory JSON.
- **Modifiers / animation:** Sol: SUBSURF; animated source objects: none on retained objects; actions: none.
- **Web result:** 1 meshes, 4,480 triangles, 1 embedded textures (2048×1024), 0.47 MiB. Only Sol is retained. The source has no UV map, so spherical UVs are generated on the web copy. Its Blender bump/displacement/emission mix is converted to a textured emissive PBR material; restrained bloom is a website task.

### Mercury — Planet Mercury.blend

- **Kept:** Sphere (960 tris, 1 UV maps).
- **Excluded:** Camera (camera), Camera.001 (camera), Jupiter (mesh), Light (light), Light.001 (light). Scene totals: 2 cameras, 2 lights, 0 empties.
- **Source materials:** Material [ShaderNodeBsdfPrincipled, ShaderNodeTexImage, ShaderNodeBump; DITHERED; alpha 1].
- **Source images:** Mercury_Texture_Map.webp 4096×2048 packed; mercurybump.jpg 1024×512 packed; all other image datablocks are listed in inventory JSON.
- **Modifiers / animation:** Sphere: SUBSURF; animated source objects: none on retained objects; actions: Jupiter 2Action.
- **Web result:** 1 meshes, 3,968 triangles, 1 embedded textures (2048×1024), 0.74 MiB. Sphere is Mercury; unrelated Jupiter mesh and its missing references are excluded. Hue/Saturation and Bump nodes are not carried over.

### Venus — Venus.blend

- **Kept:** Venus (4,224 tris, 1 UV maps); Venus Clouds (4,224 tris, 1 UV maps).
- **Excluded:** Camera (camera), Camera.001 (camera), Camera.002 (camera), Sun (light). Scene totals: 3 cameras, 1 lights, 0 empties.
- **Source materials:** Venus [ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeBsdfPrincipled, ShaderNodeBsdfDiffuse, ShaderNodeShaderToRGB, ShaderNodeLayerWeight, ShaderNodeMixShader, ShaderNodeMixShader, ShaderNodeMixShader, ShaderNodeEmission, ShaderNodeBsdfPrincipled, ShaderNodeMixShader, ShaderNodeEmission, ShaderNodeEmission, ShaderNodeBump; DITHERED; alpha 1]; Venus Clouds [ShaderNodeBsdfDiffuse, ShaderNodeShaderToRGB, ShaderNodeLayerWeight, ShaderNodeMixShader, ShaderNodeMixShader, ShaderNodeMixShader, ShaderNodeEmission, ShaderNodeBsdfPrincipled, ShaderNodeMixShader, ShaderNodeEmission, ShaderNodeEmission, ShaderNodeBsdfPrincipled, ShaderNodeTexImage, ShaderNodeBump; DITHERED; alpha 1].
- **Source images:** venus_bump_map_8k.png 8192×4096 packed; venus_cloud_4k.jpg 4096×2048 packed; venus_surface_8k.jpg 8192×4096 packed; all other image datablocks are listed in inventory JSON.
- **Modifiers / animation:** Venus: SUBSURF, Venus Clouds: SUBSURF; animated source objects: none on retained objects; actions: none.
- **Web result:** 2 meshes, 8,448 triangles, 2 embedded textures (4096×2048, 2048×1024), 4.99 MiB. Blender Shader to RGB and layered Mix Shader logic are incompatible with glTF. Surface and cloud textures are retained; cloud luminance becomes alpha.

### Earth — 10k Planet Earth.blend

- **Kept:** Atmosphere (960 tris, 1 UV maps); Clouds (960 tris, 1 UV maps); Earth (3,968 tris, 1 UV maps).
- **Excluded:** Atmosphere.001 (mesh), Aurorae (mesh), Camera (camera), Camera.001 (camera), Clouds.001 (mesh), Earth.001 (mesh), Empty (empty), Moon (mesh), Moon.001 (mesh), Sphere.004 (mesh), Sun (light). Scene totals: 2 cameras, 1 lights, 1 empties.
- **Source materials:** Atmosphere [ShaderNodeBsdfTransparent, ShaderNodeMixShader, ShaderNodeLayerWeight, ShaderNodeEmission; DITHERED; alpha 1]; Clouds procedural [ShaderNodeBsdfPrincipled, ShaderNodeTexImage, ShaderNodeBump, ShaderNodeTexImage; DITHERED; alpha 1]; Earth [ShaderNodeBsdfPrincipled, ShaderNodeBump, ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeTexImage; DITHERED; alpha 1].
- **Source images:** 8081_earthbump10k.jpg.001 10800×5400 packed; 8081_earthlights10k.jpg 10800×5400 packed; 8081_earthmap10k.jpg.001 10800×5400 packed; 8081_earthmap10k.jpg.002 10800×5400 packed; 8081_earthspec10k.jpg.001 10800×5400 packed; 8081_earthspec10k.jpg.002 10800×5400 packed; earthcloudmap.jpg 1024×512 packed; earthcloudmap.jpg.001 1024×512 packed; earthcloudmaptrans.jpg 1024×512 packed; earthcloudmaptrans.jpg.001 1024×512 packed; moonbump4k.jpg 4000×2000 packed; moonbump4k.jpg.001 4000×2000 packed; moonmap4k.jpg 4000×2000 packed; moonmap4k.jpg.001 4000×2000 packed; all other image datablocks are listed in inventory JSON.
- **Modifiers / animation:** Atmosphere: SUBSURF, Clouds: SUBSURF, Earth: SUBSURF; animated source objects: Earth, Earth.001; actions: AuroraeAction, AuroraeAction.001, EarthAction, EarthAction.001.
- **Web result:** 3 meshes, 11,904 triangles, 3 embedded textures (4096×2048, 2048×1024, 1024×512), 2.22 MiB. Duplicate Earth/layers, Moon, aurorae, helper Sun and scene objects are excluded. Night lights are an emissive map; cloud transparency mask is baked to PNG alpha; atmosphere becomes a subtle transparent material. Procedural cloud noise, aurorae and bump/specular node networks are not baked.

### Mars — 4k Planet Mars.blend

- **Kept:** Atmoshpere (960 tris, 1 UV maps); Mars (960 tris, 1 UV maps).
- **Excluded:** Camera (camera), Camera.001 (camera), Jupiter (mesh), Light (light), Light.001 (light). Scene totals: 2 cameras, 2 lights, 0 empties.
- **Source materials:** Atmosphere [ShaderNodeBsdfTransparent, ShaderNodeMixShader, ShaderNodeLayerWeight, ShaderNodeEmission; DITHERED; alpha 1]; Mars [ShaderNodeBsdfPrincipled, ShaderNodeTexImage, ShaderNodeBump, ShaderNodeTexImage; DITHERED; alpha 1].
- **Source images:** 5672_marsbump4k.jpg.001 4000×2000 packed; 5672_marsmap4k.jpg.001 4000×2000 packed; all other image datablocks are listed in inventory JSON.
- **Modifiers / animation:** Atmoshpere: SUBSURF, Mars: SUBSURF; animated source objects: none on retained objects; actions: Jupiter 2Action.
- **Web result:** 2 meshes, 7,936 triangles, 1 embedded textures (2048×1024), 0.61 MiB. Unrelated Jupiter mesh is excluded. Surface color map is retained; Bump/Hue nodes are replaced by a web PBR material and atmosphere by subtle transparent material.

### Jupiter — Planet Jupiter.blend

- **Kept:** Jupiter (15,872 tris, 1 UV maps).
- **Excluded:** Atmosphere (mesh), Camera (camera), Camera.001 (camera), Clouds (mesh), Earth (mesh), Light (light), Light.001 (light), Moon (mesh), Sphere.004 (mesh). Scene totals: 2 cameras, 2 lights, 0 empties.
- **Source materials:** Jupiter 2 [ShaderNodeBsdfPrincipled, ShaderNodeTexImage, ShaderNodeBump; DITHERED; alpha 1].
- **Source images:** 8081_earthlights10k.jpg 10800×5400 packed; DOT 1024×1024 packed; Jupitermap_edited(3).jpg 3601×1801 packed; moonbump4k.jpg 4000×2000 packed; moonmap4k.jpg 4000×2000 packed; storm_clouds_8k.jpg 8192×4096 packed; all other image datablocks are listed in inventory JSON.
- **Modifiers / animation:** none; animated source objects: Earth; actions: EarthAction, Jupiter 2Action.
- **Web result:** 1 meshes, 15,872 triangles, 1 embedded textures (2048×1024), 0.66 MiB. Unrelated Earth, clouds, atmosphere, Moon, helper and cameras/lights are excluded. Hue/Bump shader nodes are replaced by textured PBR.

### Saturn — Planet Saturn.blend

- **Kept:** Circle (128 tris, 1 UV maps); Sphere (960 tris, 1 UV maps).
- **Excluded:** Camera (camera), Camera.001 (camera), Jupiter (mesh), Light (light), Light.001 (light). Scene totals: 2 cameras, 2 lights, 0 empties.
- **Source materials:** Rings 2 [ShaderNodeBsdfPrincipled, ShaderNodeTexImage, ShaderNodeTexImage; DITHERED; alpha 1]; Saturn 2 [ShaderNodeBsdfPrincipled, ShaderNodeTexImage; DITHERED; alpha 1].
- **Source images:** Saturn rings.jpg 1035×582 packed; saturn_planetary_texture_stock_image_by_uxmal750ad_d8f7djy.jpg 4096×2048 packed; all other image datablocks are listed in inventory JSON.
- **Modifiers / animation:** Circle: SUBSURF, Sphere: SUBSURF; animated source objects: none on retained objects; actions: Jupiter 2Action.
- **Web result:** 2 meshes, 4,096 triangles, 2 embedded textures (2048×1024, 1024×576), 0.30 MiB. Sphere and Circle are Saturn and its rings. Ring luminance is baked into PNG alpha; ring geometry is retained. Unrelated Jupiter mesh is excluded.

### Uranus — Planet Uranus.blend

- **Kept:** Circle (256 tris, 1 UV maps); Neptune (960 tris, 1 UV maps).
- **Excluded:** Camera (camera), Camera.001 (camera), Jupiter (mesh), Light (light), Light.001 (light). Scene totals: 2 cameras, 2 lights, 0 empties.
- **Source materials:** Rings uranus [ShaderNodeBsdfPrincipled, ShaderNodeTexImage, ShaderNodeTexImage; DITHERED; alpha 1]; Uranus [ShaderNodeBsdfPrincipled, ShaderNodeTexImage; DITHERED; alpha 1].
- **Source images:** uranusmap.jpg 1024×512 packed; uranusringcolour.jpg.001 1024×72 packed; all other image datablocks are listed in inventory JSON.
- **Modifiers / animation:** Neptune: SUBSURF; animated source objects: none on retained objects; actions: Jupiter 2Action.
- **Web result:** 2 meshes, 4,224 triangles, 2 embedded textures (1024×512, 1024×72), 0.12 MiB. Object named Neptune is actually the Uranus surface, based on its Uranus material and texture. Circle is its ring. Ring texture luminance becomes alpha; unrelated Jupiter mesh is excluded.

### Neptune — Neuptun Neu.blend

- **Kept:** Clouds (7,680 tris, 0 UV maps); Uranus (7,680 tris, 0 UV maps).
- **Excluded:** Camera (camera), Camera.001 (camera), Clouds.001 (mesh), Clouds.002 (mesh), Sun (light), Sun.001 (light). Scene totals: 2 cameras, 2 lights, 0 empties.
- **Source materials:** clouds [ShaderNodeMixShader, ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeBsdfDiffuse, ShaderNodeBsdfTransparent, ShaderNodeDisplacement; DITHERED; alpha 1]; Uranus [ShaderNodeBsdfDiffuse, ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeDisplacement; DITHERED; alpha 1].
- **Source images:** clouds.jpg 2048×1024 packed; Uranus Textur.jpg 2048×1024 packed; all other image datablocks are listed in inventory JSON.
- **Modifiers / animation:** none; animated source objects: none on retained objects; actions: none.
- **Web result:** 2 meshes, 15,360 triangles, 2 embedded textures (2048×1024, 1024×512), 0.98 MiB. This source names its main mesh Uranus. Neither retained mesh has a UV map, so spherical UVs are generated on the web copies. The outer Clouds shell is retained; two inner cloud/atmosphere shells are omitted because they sit inside the surface and provide no visible exterior detail. Diffuse/Mix/Displacement nodes become textured PBR plus alpha cloud layer.

## Compatibility and limitations

- The original packed color maps are retained at reduced resolution. Existing UVs survive glTF export; spherical UVs were generated for the Sun and Neptune because those source meshes used Blender Generated coordinates and had no UV map. Normal/bump, procedural noise, ColorRamp, Shader to RGB, Layer Weight and Blender displacement networks cannot round-trip as-is; the material conversions are stated above.
- Transparent clouds and rings use alpha generated from their supplied images. Saturn's ring mesh and Earth's clouds/atmosphere are retained. The Sun uses its actual `Sol` mesh and sun texture, not objects from the composite system file.
- The source files have a number of unused broken external image references (zero-sized datablocks). The web exports use available packed images; the import check found all expected embedded textures.
- All source meshes were inspected before export. Subdivision was capped at one viewport level where it improved rounded silhouettes; unrelated geometry and cameras/lights were removed. The model assets were rendered after import for material QA; final on-screen lighting and appearance still need browser visual QA in later milestones.
