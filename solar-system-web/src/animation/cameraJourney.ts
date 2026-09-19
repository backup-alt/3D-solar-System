import * as THREE from 'three';
import { planets, type PlanetId } from '../data/planets';
import { isMobile, isReducedMotion } from '../utils/responsive';
import { overviewPose } from '../three/camera';
import { worldPosition } from '../three/solarSystem';
import type { JourneyState } from './scroll';

const eyeA = new THREE.Vector3();
const eyeB = new THREE.Vector3();
const targetA = new THREE.Vector3();
const targetB = new THREE.Vector3();
const sunward = new THREE.Vector3();
const direction = new THREE.Vector3();
const tangent = new THREE.Vector3();
const innerOffset = new THREE.Vector3(0, 0.12, 0.08);
const tmp = new THREE.Vector3();
const chapterIds = planets.map(p => p.id);

function chapterPose(id: PlanetId, eye: THREE.Vector3, target: THREE.Vector3) {
  const data = planets.find(p => p.id === id)!;
  const index = chapterIds.indexOf(id);
  const position = worldPosition(id, tmp);
  sunward.copy(position).multiplyScalar(-1).normalize();
  if (index < 4) {
    // Near the Sun, approach from the side. A sunward camera path can pass
    // through the Sun on compressed mobile orbits and hide the planet.
    tangent.set(-position.z, 0, position.x).normalize();
    direction.copy(tangent).addScaledVector(sunward, 0.08).add(innerOffset).normalize();
  } else {
    direction.set(0.26, 0.15, 1).addScaledVector(sunward, 0.52).normalize();
  }
  const ring = id === 'saturn' || id === 'uranus';
  const distance = data.radius * (isMobile() ? ring ? 9.2 : 5.3 : ring ? 7.1 : 4.0);
  eye.copy(position).addScaledVector(direction, distance);
  if (index < 4 && eye.length() < 3.25) eye.setLength(3.25);
  target.copy(position);
  if (isMobile()) target.y -= data.radius * 0.65;
  else target.x += id === 'earth' ? data.radius * 0.45 : (index % 2 === 0 ? -1 : 1) * data.radius * 0.9;
}

function poseAt(index: number, eye: THREE.Vector3, target: THREE.Vector3) {
  if (index === 0) {
    const overview = overviewPose();
    eye.copy(overview.position);
    target.copy(overview.target);
    return;
  }
  chapterPose(chapterIds[index - 1], eye, target);
}

export function updateCamera(camera: THREE.PerspectiveCamera, state: JourneyState, targetOut: THREE.Vector3) {
  const progress = THREE.MathUtils.clamp(state.progress, 0, planets.length);
  const from = Math.min(Math.floor(progress), planets.length - 1);
  const to = Math.min(from + 1, planets.length);
  const fraction = progress - from;
  const smooth = fraction * fraction * (3 - 2 * fraction);
  poseAt(from, eyeA, targetA);
  poseAt(to, eyeB, targetB);
  camera.position.copy(eyeA).lerp(eyeB, smooth);
  targetOut.copy(targetA).lerp(targetB, smooth);
  if (!isReducedMotion()) {
    const arc = Math.sin(Math.PI * fraction);
    camera.position.y += arc * (from === 0 ? 2.8 : 1.2);
    camera.position.z += arc * (from === 0 ? 2.8 : 1.8);
  }
  camera.lookAt(targetOut);
}
