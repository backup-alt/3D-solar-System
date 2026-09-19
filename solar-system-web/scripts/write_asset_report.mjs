import fs from 'node:fs';
import path from 'node:path';

const project = path.resolve(import.meta.dirname, '..');
const inventory = key => JSON.parse(fs.readFileSync(path.join(project, 'scripts', `inventory-${key}.json`), 'utf8'));
const validation = JSON.parse(fs.readFileSync(path.join(project, 'scripts', 'validation.json'), 'utf8'));
const specs = [
  ['sun', ['Sol'], ['sun.jpg'], 'Only Sol is retained. The source has no UV map, so spherical UVs are generated on the web copy. Its Blender bump/displacement/emission mix is converted to a textured emissive PBR material; restrained bloom is a website task.'],
  ['mercury', ['Sphere'], ['Mercury_Texture_Map.webp'], 'Sphere is Mercury; unrelated Jupiter mesh and its missing references are excluded. Hue/Saturation and Bump nodes are not carried over.'],
  ['venus', ['Venus', 'Venus Clouds'], ['venus_surface_8k.jpg', 'venus_cloud_4k.jpg'], 'Blender Shader to RGB and layered Mix Shader logic are incompatible with glTF. Surface and cloud textures are retained; cloud luminance becomes alpha.'],
  ['earth', ['Earth', 'Clouds', 'Atmosphere'], ['8081_earthmap10k.jpg.001', '8081_earthlights10k.jpg', 'earthcloudmap.jpg'], 'Duplicate Earth/layers, Moon, aurorae, helper Sun and scene objects are excluded. Night lights are an emissive map; cloud transparency mask is baked to PNG alpha; atmosphere becomes a subtle transparent material. Procedural cloud noise, aurorae and bump/specular node networks are not baked.'],
  ['mars', ['Mars', 'Atmoshpere'], ['5672_marsmap4k.jpg.001'], 'Unrelated Jupiter mesh is excluded. Surface color map is retained; Bump/Hue nodes are replaced by a web PBR material and atmosphere by subtle transparent material.'],
  ['jupiter', ['Jupiter'], ['Jupitermap_edited(3).jpg'], 'Unrelated Earth, clouds, atmosphere, Moon, helper and cameras/lights are excluded. Hue/Bump shader nodes are replaced by textured PBR.'],
  ['saturn', ['Sphere', 'Circle'], ['saturn_planetary_texture_stock_image_by_uxmal750ad_d8f7djy.jpg', 'Saturn rings.jpg'], 'Sphere and Circle are Saturn and its rings. Ring luminance is baked into PNG alpha; ring geometry is retained. Unrelated Jupiter mesh is excluded.'],
  ['uranus', ['Neptune', 'Circle'], ['uranusmap.jpg', 'uranusringcolour.jpg.001'], 'Object named Neptune is actually the Uranus surface, based on its Uranus material and texture. Circle is its ring. Ring texture luminance becomes alpha; unrelated Jupiter mesh is excluded.'],
  ['neptune', ['Neptune'], [], 'The improved Neptune retains only the upgraded procedural surface from Neptune_Improved_02.blend. Its noise/color-ramp cloud deck is procedural, so the shader output is baked to a 2048×1024 equirectangular texture with Cycles before export; the result is a single textured PBR mesh.'],
];
const rows = [];
let md = `# Asset report\n\nGenerated from read-only inspection of the nine original Blender files with Blender 5.2.2 LTS at \`E:\\Apps\\Blender\\blender.exe\`. The brief named \`E:\\solar 3d site\`, but the files actually exist in \`E:\\solor 3d site\`. All output is in this project's directory. Source .blend files were opened headlessly and never saved.\n\n## Web exports\n\n| Asset | Original scene tris | Relevant source tris | GLB tris | Source texture(s) | GLB size | Exported meshes |\n|---|---:|---:|---:|---|---:|---:|\n`;
for (const [key, selected, textures] of specs) {
  const data = inventory(key);
  const glb = validation[`${key}.glb`];
  const relevant = data.objects.filter(o => selected.includes(o.name)).reduce((sum, o) => sum + (o.triangles || 0), 0);
  const sourceTextures = textures.length
    ? textures.map(name => {
        const image = data.images.find(i => i.name === name);
        return `${name} (${image?.width || '?'}×${image?.height || '?'})`;
      }).join('<br>')
    : 'procedural → baked';
  rows.push({key, data, glb, selected});
  md += `| ${key} | ${data.totals.triangles.toLocaleString()} | ${relevant.toLocaleString()} | ${glb.triangles.toLocaleString()} | ${sourceTextures} | ${(glb.bytes/1048576).toFixed(2)} MiB | ${selected.join(', ')} |\n`;
}
md += `\nAll nine GLBs were imported into a clean Blender scene after export. Total transfer size is ${(rows.reduce((sum, row) => sum + row.glb.bytes, 0)/1048576).toFixed(2)} MiB; progressive loading is required for the website. A GLB is self-contained, including the optimized textures. Surface images are limited to 1–4K; cloud and ring masks are 1–2K.\n\n## Inspection details\n\nThe complete per-object, per-material and per-image inventories are in \`scripts/inventory-*.json\`; post-export import results are in \`scripts/validation.json\`. Source images marked “missing” below generally have zero dimensions and refer to unused external paths; the exported materials use packed images with valid dimensions. Blender-only node effects were converted as described for each asset.\n\n`;
for (const [key, selected, _textures, note] of specs) {
  const {data, glb} = rows.find(row => row.key === key);
  const source = path.basename(data.source);
  const other = data.objects.filter(o => !selected.includes(o.name));
  const selectedRecords = data.objects.filter(o => selected.includes(o.name));
  const images = data.images.filter(i => i.width && i.height && i.name !== 'Viewer Node' && !i.name.startsWith('Viewer Node'));
  const modText = selectedRecords.flatMap(o => o.modifiers.map(m => `${o.name}: ${m.type}`)).join(', ') || 'none';
  const animation = data.objects.filter(o => o.animation).map(o => o.name).join(', ') || 'none on retained objects';
  const materials = selectedRecords.flatMap(o => o.materials).filter(Boolean);
  const relevantMaterials = data.materials.filter(m => materials.includes(m.name));
  const sourceImages = images.map(i => `${i.name} ${i.width}×${i.height}${i.packed ? ' packed' : i.exists ? ' external' : ' missing'}`).join('; ');
  const converted = glb.images.map(i => `${i.width}×${i.height}`).join(', ');
  md += `### ${key[0].toUpperCase()+key.slice(1)} — ${source}\n\n`;
  md += `- **Kept:** ${selectedRecords.map(o => `${o.name} (${o.triangles?.toLocaleString() || 0} tris, ${o.uv_maps?.length || 0} UV maps)`).join('; ')}.\n`;
  md += `- **Excluded:** ${other.map(o => `${o.name} (${o.type.toLowerCase()})`).join(', ') || 'none'}. Scene totals: ${data.totals.cameras} cameras, ${data.totals.lights} lights, ${data.totals.empties} empties.\n`;
  md += `- **Source materials:** ${relevantMaterials.map(m => `${m.name} [${m.node_types.filter(n => /TexImage|Emission|Transparent|MixShader|Bump|ShaderToRGB|Displacement|LayerWeight|BsdfPrincipled|BsdfDiffuse/.test(n)).join(', ') || 'simple'}; ${m.blend_method}; alpha ${m.alpha}]`).join('; ')}.\n`;
  md += `- **Source images:** ${sourceImages || 'none'}; all other image datablocks are listed in inventory JSON.\n`;
  md += `- **Modifiers / animation:** ${modText}; animated source objects: ${animation}; actions: ${data.actions.join(', ') || 'none'}.\n`;
  md += `- **Web result:** ${glb.meshes} meshes, ${glb.triangles.toLocaleString()} triangles, ${glb.images.length} embedded textures (${converted}), ${(glb.bytes/1048576).toFixed(2)} MiB. ${note}\n\n`;
}
md += `## Compatibility and limitations\n\n- The original packed color maps are retained at reduced resolution. Existing UVs survive glTF export; spherical UVs were generated for the Sun because that source mesh used Blender Generated coordinates, and for the improved Neptune the procedural shader was baked to an equirectangular texture. Normal/bump, procedural noise, ColorRamp, Shader to RGB, Layer Weight and Blender displacement networks cannot round-trip as-is unless baked; the material conversions are stated above.\n- Transparent clouds and rings use alpha generated from their supplied images. Saturn's ring mesh and Earth's clouds/atmosphere are retained. The Sun uses its actual \`Sol\` mesh and sun texture, not objects from the composite system file.\n- The source files have a number of unused broken external image references (zero-sized datablocks). The web exports use available packed images; the import check found all expected embedded textures.\n- All source meshes were inspected before export. Subdivision was capped at one viewport level where it improved rounded silhouettes; unrelated geometry and cameras/lights were removed. The model assets were rendered after import for material QA; final on-screen lighting and appearance still need browser visual QA in later milestones.\n`;
fs.writeFileSync(path.join(project, 'ASSET_REPORT.md'), md);
console.log(`Wrote ASSET_REPORT.md (${md.length} chars)`);
