# 3D Solar System

🌐 **Access the website here:**
https://backup-alt.github.io/3D-solar-System/

A scroll-driven, real-time 3D journey through the Sun and the eight planets, built with Three.js, TypeScript, Vite and GSAP. The models are original 3D assets exported from Blender.

have fun! 🚀

---

## The Eight Worlds

A quick-reference table, followed by a short profile of each planet.

| # | Planet | Type | Distance from Sun | Diameter | Day length | Year length | Moons |
|---|--------|------|-------------------|----------|------------|-------------|-------|
| 01 | Mercury | The Swift Planet | 57.9 million km | 4,879 km | 58.6 Earth days | 88 Earth days | 0 |
| 02 | Venus | The Veiled World | 108.2 million km | 12,104 km | 243 Earth days | 225 Earth days | 0 |
| 03 | Earth | The Living Planet | 149.6 million km | 12,756 km | 23.9 hours | 365.25 days | 1 |
| 04 | Mars | The Red Planet | 227.9 million km | 6,792 km | 24.6 hours | 687 Earth days | 2 |
| 05 | Jupiter | The Giant | 778.6 million km | 142,984 km | 9.9 hours | 11.86 Earth years | 115 |
| 06 | Saturn | The Ringed Giant | 1.43 billion km | 120,536 km | 10.7 hours | 29.45 Earth years | 293 |
| 07 | Uranus | The Sideways Planet | 2.87 billion km | 51,118 km | 17.2 hours | 84 Earth years | 29 |
| 08 | Neptune | The Outer Edge | 4.5 billion km | 49,528 km | 16.1 hours | 164.8 Earth years | 16 |

### 01 · Mercury — The Swift Planet
A small, cratered world tracing the innermost path around the Sun. It races through its year in just 88 Earth days while taking nearly 59 Earth days to complete a single rotation.

- **Distance from Sun:** 57.9 million km
- **Diameter:** 4,879 km
- **Day length:** 58.6 Earth days
- **Year length:** 88 Earth days
- **Moons:** 0

### 02 · Venus — The Veiled World
Wrapped in dense clouds, Venus holds the hottest surface in our planetary family. Its thick atmosphere traps heat and it spins backwards, so a single day lasts longer than its year.

- **Distance from Sun:** 108.2 million km
- **Diameter:** 12,104 km
- **Day length:** 243 Earth days
- **Year length:** 225 Earth days
- **Moons:** 0

### 03 · Earth — The Living Planet
An ocean world with a thin atmosphere and the only known life in the cosmos. Its 23.4° axial tilt gives us the seasons.

- **Distance from Sun:** 149.6 million km
- **Diameter:** 12,756 km
- **Day length:** 23.9 hours
- **Year length:** 365.25 days
- **Moons:** 1

### 04 · Mars — The Red Planet
A rust-colored desert shaped by ancient water, immense volcanoes, and thin air. Home to Olympus Mons, the tallest volcano in the Solar System.

- **Distance from Sun:** 227.9 million km
- **Diameter:** 6,792 km
- **Day length:** 24.6 hours
- **Year length:** 687 Earth days
- **Moons:** 2

### 05 · Jupiter — The Giant
A vast gas giant where cloud bands and immense storms encircle the largest planet. The Great Red Spot is a storm wider than Earth.

- **Distance from Sun:** 778.6 million km
- **Diameter:** 142,984 km
- **Day length:** 9.9 hours
- **Year length:** 11.86 Earth years
- **Moons:** 115

### 06 · Saturn — The Ringed Giant
A world of pale storms surrounded by a breathtaking disk of icy rings. It is the least dense planet, light enough to float in water.

- **Distance from Sun:** 1.43 billion km
- **Diameter:** 120,536 km
- **Day length:** 10.7 hours
- **Year length:** 29.45 Earth years
- **Moons:** 293

### 07 · Uranus — The Sideways Planet
An ice giant tipped almost onto its side, turning through the deep outer dark. Its extreme 97.8° tilt makes it roll along its orbit.

- **Distance from Sun:** 2.87 billion km
- **Diameter:** 51,118 km
- **Day length:** 17.2 hours
- **Year length:** 84 Earth years
- **Moons:** 29

### 08 · Neptune — The Outer Edge
The most distant planet: a deep-blue world swept by supersonic winds, the fastest in the Solar System.

- **Distance from Sun:** 4.5 billion km
- **Diameter:** 49,528 km
- **Day length:** 16.1 hours
- **Year length:** 164.8 Earth years
- **Moons:** 16

---

## Project structure

- `solar-system-web/src/data/planets.ts` — all planet facts and presentation scaling constants.
- `solar-system-web/src/three/` — scene, camera, renderer, stars, lighting, loaders and orbital groups.
- `solar-system-web/src/animation/` — delta-time loop and GSAP ScrollTrigger camera journey.
- `solar-system-web/public/models/` — optimized GLB models for the Sun and planets.
- `solar-system-web/scripts/` — Blender inspection, GLB export and validation scripts.

## Run locally

```bash
cd solar-system-web
npm install
npm run dev
```

Add `?debug=true` to the URL to show FPS, camera coordinates, chapter, loaded models and triangle count. Build with `npm run build`.

> Planet sizes and distances in the 3D scene are presentation scale, not true astronomical scale. Factual values use [NASA planet sizes and locations](https://science.nasa.gov/solar-system/planet-sizes-and-locations-in-our-solar-system/) and [NASA/JPL moon counts](https://ssd.jpl.nasa.gov/sats/discovery.html). Moon counts were checked September 2026 and can change after new discoveries.
