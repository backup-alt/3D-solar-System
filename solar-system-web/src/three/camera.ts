import * as THREE from 'three';
import { isMobile, isTablet } from '../utils/responsive';

export function overviewPose() {
  if (isMobile()) return { position: new THREE.Vector3(0, 17, 46), target: new THREE.Vector3(0, 0, 0) };
  if (isTablet()) return { position: new THREE.Vector3(0, 14, 38), target: new THREE.Vector3(0, 0, 0) };
  return { position: new THREE.Vector3(0, 12.5, 32), target: new THREE.Vector3(0, 0, 0) };
}

export function createCamera() {
  const camera = new THREE.PerspectiveCamera(isMobile() ? 48 : 42, window.innerWidth / window.innerHeight, 0.1, 350);
  const pose = overviewPose();
  camera.position.copy(pose.position);
  camera.lookAt(pose.target);
  return camera;
}
