import * as THREE from 'three';
import { qualitySettings } from '../utils/responsive';

export function createRenderer(canvas: HTMLCanvasElement) {
  // The renderer turns Scene + Camera into pixels; the DPR cap limits GPU cost.
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, powerPreference: 'high-performance' });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;
  renderer.setClearColor(0x05070c, 1);
  renderer.setPixelRatio(qualitySettings().pixelRatio);
  renderer.setSize(window.innerWidth, window.innerHeight, false);
  return renderer;
}
