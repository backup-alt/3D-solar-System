# The Solar System

A scroll-driven, real-time 3D journey through the Sun and eight planets, built with raw Three.js, TypeScript, Vite and GSAP ScrollTrigger. The models were exported from the supplied Blender files, with the Sun isolated from `Solar System Assets.blend`.

## Run

```powershell
cd 'E:\solor 3d site\solar-system-web'
npm install
npm run dev
```

Open the local URL printed by Vite. Add `?debug=true` to show FPS, camera coordinates, chapter, loaded models and triangle count. Build with `npm run build`.

If this machine's `npm` command points to a missing global install, run npm directly:

```powershell
& 'C:\Program Files\nodejs\node.exe' 'C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js' install
& 'C:\Program Files\nodejs\node.exe' 'C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js' run dev
```

## Project map

- `public/models/`: nine self-contained optimized GLBs.
- `src/data/planets.ts`: all chapter facts and presentation scaling constants.
- `src/three/`: scene, camera, renderer, stars, lighting, loaders and orbital groups.
- `src/animation/`: delta-time loop and GSAP ScrollTrigger camera journey.
- `scripts/`: read-only Blender inspection, GLB export and validation scripts, plus JSON reports.
- `ASSET_REPORT.md`: source inspection and export decisions.

The website streams the Sun and Mercury first, then loads the other planet models progressively. Each mesh remains real-time geometry from the supplied Blender assets. The source `.blend` files are never modified by these scripts.

Planet dimensions and distances are presentation scale, not true astronomical scale. Factual chapter values use [NASA planet sizes and locations](https://science.nasa.gov/solar-system/planet-sizes-and-locations-in-our-solar-system/) and [NASA/JPL moon counts](https://ssd.jpl.nasa.gov/sats/discovery.html). Moon counts were checked September 2026 and can change after new discoveries.
