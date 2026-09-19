import { LoadingManager, Group } from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import type { PlanetId } from '../data/planets';

export type ModelId = PlanetId | 'sun';

// LoadingManager tracks network fetches; the promise cache prevents duplicate GLB downloads.
const manager = new LoadingManager();
const loader = new GLTFLoader(manager);
const promises = new Map<ModelId, Promise<Group>>();
const loaded = new Set<ModelId>();
const failures = new Map<ModelId, string>();

export function loadModel(id: ModelId): Promise<Group> {
  if (promises.has(id)) return promises.get(id)!;
  const promise = new Promise<Group>((resolve, reject) => {
    loader.load(`/models/${id}.glb`, gltf => {
      loaded.add(id);
      resolve(gltf.scene);
    }, undefined, error => {
      const message = error instanceof Error ? error.message : String(error);
      failures.set(id, message);
      reject(new Error(`Could not load ${id}.glb: ${message}`));
    });
  });
  promises.set(id, promise);
  return promise;
}

export const loadedModelNames = () => [...loaded];
export const modelFailures = () => new Map(failures);

export async function loadOpening(onProgress: (completed: number, total: number) => void) {
  const priority: ModelId[] = ['sun', 'mercury'];
  let complete = 0;
  await Promise.all(priority.map(id => loadModel(id).finally(() => onProgress(++complete, priority.length))));
}
