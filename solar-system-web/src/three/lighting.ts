import * as THREE from 'three';

export function addLighting(scene: THREE.Scene) {
  // A point light at the Sun creates each planet's bright side and terminator.
  // No distance falloff is used because the orbital distances are compressed.
  const sunlight = new THREE.PointLight(0xffebca, 3.2, 0, 0);
  sunlight.position.set(0, 0, 0);
  sunlight.name = 'Sunlight';
  scene.add(sunlight);
  const faintFill = new THREE.AmbientLight(0x57678d, 0.24);
  scene.add(faintFill);
}
