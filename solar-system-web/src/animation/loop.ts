import * as THREE from 'three';
import { updateSolarSystem } from '../three/solarSystem';
import { updateCamera } from './cameraJourney';
import { isReducedMotion } from '../utils/responsive';
import type { JourneyState } from './scroll';

export function startLoop(scene: THREE.Scene, camera: THREE.PerspectiveCamera, renderer: THREE.WebGLRenderer, state: JourneyState, onFrame?: (fps: number, target: THREE.Vector3) => void) {
  const clock = new THREE.Clock();
  const cameraTarget = new THREE.Vector3();
  let lastDebug = 0;
  let frameId = 0;
  const animate = () => {
    frameId = requestAnimationFrame(animate);
    if (document.hidden) { clock.getDelta(); return; }
    // Delta time keeps rotation and orbit motion independent of monitor Hz.
    const delta = Math.min(clock.getDelta(), 0.05);
    updateSolarSystem(delta, isReducedMotion(), state.progress);
    scene.updateMatrixWorld(true);
    updateCamera(camera, state, cameraTarget);
    renderer.render(scene, camera);
    if (onFrame && clock.elapsedTime - lastDebug > 0.25) {
      onFrame(delta > 0 ? Math.round(1 / delta) : 0, cameraTarget);
      lastDebug = clock.elapsedTime;
    }
  };
  animate();
  return () => cancelAnimationFrame(frameId);
}
