import * as THREE from 'three';
import { qualitySettings } from '../utils/responsive';

export function createStars() {
  const count = qualitySettings().starCount;
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  let seed = 7482;
  const random = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296);
  for (let i = 0; i < count; i++) {
    const theta = random() * Math.PI * 2;
    const phi = Math.acos(2 * random() - 1);
    const distance = 85 + random() * 100;
    positions[i*3] = Math.sin(phi) * Math.cos(theta) * distance;
    positions[i*3+1] = Math.cos(phi) * distance;
    positions[i*3+2] = Math.sin(phi) * Math.sin(theta) * distance;
    const brightness = 0.24 + Math.pow(random(), 6) * 0.63;
    colors[i*3] = brightness * (0.89 + random()*0.11);
    colors[i*3+1] = brightness * (0.92 + random()*0.08);
    colors[i*3+2] = brightness;
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  const material = new THREE.PointsMaterial({ size: 0.095, sizeAttenuation: true, vertexColors: true, depthWrite: false, transparent: true, opacity: 0.85 });
  const points = new THREE.Points(geometry, material);
  points.name = 'Procedural star field';
  return points;
}
