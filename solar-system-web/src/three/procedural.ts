import * as THREE from 'three';
import type { PlanetId } from '../data/planets';

function seededRandom(seed: number) {
  let state = seed >>> 0;
  return () => {
    state = (state * 1664525 + 1013904223) >>> 0;
    return state / 4294967296;
  };
}

function splotch(context: CanvasRenderingContext2D, width: number, x: number, y: number, radius: number, color: string, alpha: number) {
  for (const offset of [-width, 0, width]) {
    const gradient = context.createRadialGradient(x + offset, y, 0, x + offset, y, radius);
    gradient.addColorStop(0, `rgba(${color},${alpha})`);
    gradient.addColorStop(1, `rgba(${color},0)`);
    context.fillStyle = gradient;
    context.fillRect(x + offset - radius, y - radius, radius * 2, radius * 2);
  }
}

function createPlutoTexture() {
  const width = 1024;
  const height = 512;
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const context = canvas.getContext('2d')!;

  const base = context.createLinearGradient(0, 0, 0, height);
  base.addColorStop(0, '#8a7969');
  base.addColorStop(0.45, '#c9b7a3');
  base.addColorStop(1, '#837262');
  context.fillStyle = base;
  context.fillRect(0, 0, width, height);

  const random = seededRandom(1930);
  for (let i = 0; i < 240; i++) {
    const tone = random();
    const color = tone < 0.45 ? '116, 92, 74' : tone < 0.8 ? '214, 198, 176' : '84, 64, 51';
    splotch(context, width, random() * width, random() * height, 8 + random() * 72, color, 0.05 + random() * 0.12);
  }

  for (let i = 0; i < 55; i++) {
    const x = random() * width;
    const y = random() * height;
    const radius = 3 + random() * 16;
    context.strokeStyle = `rgba(78, 58, 46, ${0.18 + random() * 0.2})`;
    context.lineWidth = 1 + random() * 2;
    context.beginPath();
    context.arc(x, y, radius, 0, Math.PI * 2);
    context.stroke();
  }

  context.save();
  context.translate(width * 0.54, height * 0.47);
  context.rotate(-0.12);
  context.fillStyle = 'rgba(240, 229, 210, 0.88)';
  context.beginPath();
  context.moveTo(0, 92);
  context.bezierCurveTo(-138, -4, -58, -104, 0, -34);
  context.bezierCurveTo(58, -104, 138, -4, 0, 92);
  context.closePath();
  context.fill();
  context.restore();

  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.anisotropy = 8;
  texture.wrapS = THREE.RepeatWrapping;
  texture.needsUpdate = true;
  return texture;
}

export function createProceduralPlanet(id: PlanetId): THREE.Mesh {
  if (id !== 'pluto') throw new Error(`No procedural model defined for ${id}.`);

  const geometry = new THREE.SphereGeometry(1, 96, 64);
  const material = new THREE.MeshStandardMaterial({
    map: createPlutoTexture(),
    roughness: 0.95,
    metalness: 0,
  });
  const mesh = new THREE.Mesh(geometry, material);
  mesh.name = 'Pluto procedural surface';
  return mesh;
}
