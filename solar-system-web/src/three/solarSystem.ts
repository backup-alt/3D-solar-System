import * as THREE from 'three';
import { planets, type PlanetData, type PlanetId } from '../data/planets';
import { loadModel, type ModelId } from './loaders';
import { isMobile, isTablet } from '../utils/responsive';

interface World {
  data: PlanetData;
  orbitPlane: THREE.Group;
  orbitPivot: THREE.Group;
  axialGroup: THREE.Group;
  modelGroup: THREE.Group;
  cloud: THREE.Object3D | null;
  orbitLine: THREE.Line;
}

const worlds = new Map<PlanetId, World>();
const sunGroup = new THREE.Group();
const tmp = new THREE.Vector3();

function orbitLine(radius: number, color: string) {
  const vertices: number[] = [];
  for (let i = 0; i <= 192; i++) {
    const theta = i / 192 * Math.PI * 2;
    vertices.push(Math.cos(theta)*radius, 0, Math.sin(theta)*radius);
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
  const line = new THREE.Line(geometry, new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0.095, depthWrite: false }));
  line.name = 'Presentation orbit';
  return line;
}

function sunHalo() {
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = 128;
  const context = canvas.getContext('2d')!;
  const gradient = context.createRadialGradient(64,64,23,64,64,64);
  gradient.addColorStop(0, 'rgba(255,169,65,0.27)');
  gradient.addColorStop(0.45, 'rgba(255,135,38,0.10)');
  gradient.addColorStop(1, 'rgba(255,110,25,0)');
  context.fillStyle = gradient;
  context.fillRect(0,0,128,128);
  const texture = new THREE.CanvasTexture(canvas);
  const sprite = new THREE.Sprite(new THREE.SpriteMaterial({map:texture, transparent:true, blending:THREE.AdditiveBlending, depthWrite:false, toneMapped:false}));
  sprite.scale.set(9.2, 9.2, 1);
  sprite.name = 'Sun glow';
  return sprite;
}

function optimizeMaterial(model: THREE.Object3D) {
  model.traverse(object => {
    if (!(object instanceof THREE.Mesh)) return;
    object.castShadow = false;
    object.receiveShadow = false;
    const materials = Array.isArray(object.material) ? object.material : [object.material];
    for (const material of materials) {
      if (material instanceof THREE.MeshStandardMaterial) {
        material.roughness = Math.max(material.roughness, 0.72);
        material.needsUpdate = true;
      }
    }
  });
}

export function createSolarSystem(scene: THREE.Scene) {
  sunGroup.name = 'Sun';
  scene.add(sunGroup);
  sunGroup.add(sunHalo());
  // An orbital pivot is a Group whose rotation moves its child planet around
  // the Sun. A second Group applies the small orbital-plane inclination.
  for (const data of planets) {
    const orbitPlane = new THREE.Group();
    orbitPlane.rotation.x = THREE.MathUtils.degToRad(data.orbitInclination * 0.32);
    const orbitPivot = new THREE.Group();
    orbitPivot.rotation.y = data.startAngle;
    const axialGroup = new THREE.Group();
    axialGroup.position.x = data.orbitRadius;
    axialGroup.rotation.z = THREE.MathUtils.degToRad(data.axialTilt);
    const modelGroup = new THREE.Group();
    modelGroup.name = `${data.name} presentation scale`;
    modelGroup.scale.setScalar(data.radius);
    axialGroup.add(modelGroup);
    orbitPivot.add(axialGroup);
    orbitPlane.add(orbitPivot);
    const line = orbitLine(data.orbitRadius, data.accent);
    orbitPlane.add(line);
    scene.add(orbitPlane);
    worlds.set(data.id, {data, orbitPlane, orbitPivot, axialGroup, modelGroup, cloud:null, orbitLine:line});
  }
  updateOrbitLayout();
}

export function updateOrbitLayout() {
  // Smaller screens compress *distances*, while the planet sizes stay legible.
  // Mercury's minimum offset keeps it outside the Sun on narrow viewports.
  for (const world of worlds.values()) {
    const radius = isMobile() ? 3.55 + (world.data.orbitRadius - 4.2) * 0.43
      : isTablet() ? 4.0 + (world.data.orbitRadius - 4.2) * 0.72
      : world.data.orbitRadius;
    world.axialGroup.position.x = radius;
    world.orbitLine.scale.setScalar(radius / world.data.orbitRadius);
  }
}

export async function attachModel(id: ModelId) {
  const model = await loadModel(id);
  optimizeMaterial(model);
  if (id === 'sun') {
    model.scale.setScalar(2.8);
    sunGroup.add(model);
    return;
  }
  const world = worlds.get(id)!;
  world.modelGroup.add(model);
  if (id === 'earth') {
    world.cloud = model.getObjectByName('Clouds') || model.getObjectByName('Clouds_1') || null;
  }
}

export function updateSolarSystem(deltaSeconds: number, reducedMotion: boolean, journeyProgress: number) {
  const motion = reducedMotion ? 0.18 : 1;
  sunGroup.rotation.y += deltaSeconds * 0.018 * motion;
  sunGroup.visible = journeyProgress < 0.9;
  const orbitOpacity = Math.max(0, 1 - (journeyProgress - 0.35) / 0.75);
  const nearestChapter = Math.round(journeyProgress);
  const betweenChapters = Math.abs(journeyProgress - nearestChapter) > 0.18;
  let index = 0;
  for (const world of worlds.values()) {
    const chapterNumber = index + 1;
    world.modelGroup.visible = journeyProgress < 0.6 || (betweenChapters
      ? chapterNumber === Math.floor(journeyProgress) || chapterNumber === Math.ceil(journeyProgress)
      : chapterNumber === nearestChapter);
    index++;
    world.orbitLine.visible = orbitOpacity > 0.02;
    (world.orbitLine.material as THREE.LineBasicMaterial).opacity = 0.095 * orbitOpacity;
    // Speeds use orbital-year ratios as inspiration, compressed so outer worlds
    // still move visibly. Delta time makes speed independent of refresh rate.
    const orbitSpeed = 0.075 / Math.sqrt(world.data.orbitYears);
    world.orbitPivot.rotation.y += deltaSeconds * orbitSpeed * motion;
    const spinDirection = Math.sign(world.data.spinHours);
    const spinSpeed = 0.1 + 0.25 / Math.sqrt(Math.abs(world.data.spinHours) / 24);
    world.modelGroup.rotation.y += deltaSeconds * spinDirection * spinSpeed * motion;
    if (world.cloud) world.cloud.rotation.y += deltaSeconds * 0.014 * motion;
  }
}

export function worldPosition(id: PlanetId, target = new THREE.Vector3()) {
  const world = worlds.get(id)!;
  world.axialGroup.getWorldPosition(target);
  return target;
}

export function getWorld(id: PlanetId) { return worlds.get(id); }
export function allWorlds() { return [...worlds.values()]; }
