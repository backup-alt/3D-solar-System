import * as THREE from 'three';
import { allWorlds } from '../three/solarSystem';
import { loadedModelNames } from '../three/loaders';
import type { JourneyState } from '../animation/scroll';

export function createDebug(renderer: THREE.WebGLRenderer, camera: THREE.PerspectiveCamera, state: JourneyState) {
  if (new URLSearchParams(location.search).get('debug') !== 'true') return undefined;
  const element = document.createElement('pre');
  element.className = 'debug-panel';
  document.body.appendChild(element);
  return (fps: number, target: THREE.Vector3) => {
    const dimensions = allWorlds().map(w => `${w.data.name}: radius ${w.data.radius}`).join('\n');
    element.textContent = `FPS ${fps}\nCHAPTER ${state.current}\nCAMERA ${camera.position.toArray().map(n => n.toFixed(2)).join(', ')}\nTARGET ${target.toArray().map(n => n.toFixed(2)).join(', ')}\nLOADED ${loadedModelNames().join(', ')}\nTRIANGLES ${renderer.info.render.triangles}\n${dimensions}`;
  };
}
