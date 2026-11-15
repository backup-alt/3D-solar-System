# 3D Solar System

🌐 **Access the website here:**
https://backup-alt.github.io/3D-solar-System/

A cinematic journey through the Solar System, rendered in real time with original 3D planet models. Scroll through eight worlds, each with its own scale, orbit, rotation, and story.

have fun! 🚀

---

## The Eight Worlds

| # | Planet | Type | Distance from Sun | Diameter | Day Length | Year Length | Moons |
|---|--------|------|-------------------|----------|------------|-------------|-------|
| 01 | [Mercury](#mercury) | The Swift Planet | 57.9 million km | 4,879 km | 58.6 Earth days | 88 Earth days | 0 |
| 02 | [Venus](#venus) | The Veiled World | 108.2 million km | 12,104 km | 243 Earth days | 225 Earth days | 0 |
| 03 | [Earth](#earth) | The Living Planet | 149.6 million km | 12,756 km | 23.9 hours | 365.25 days | 1 |
| 04 | [Mars](#mars) | The Red Planet | 227.9 million km | 6,792 km | 24.6 hours | 687 Earth days | 2 |
| 05 | [Jupiter](#jupiter) | The Giant | 778.6 million km | 142,984 km | 9.9 hours | 11.86 Earth years | 115 |
| 06 | [Saturn](#saturn) | The Ringed Giant | 1.43 billion km | 120,536 km | 10.7 hours | 29.45 Earth years | 293 |
| 07 | [Uranus](#uranus) | The Sideways Planet | 2.87 billion km | 51,118 km | 17.2 hours | 84 Earth years | 29 |
| 08 | [Neptune](#neptune) | The Outer Edge | 4.5 billion km | 49,528 km | 16.1 hours | 164.8 Earth years | 16 |

---

### Mercury
**The Swift Planet** — A small, cratered world tracing the innermost path around the Sun.

- Distance from Sun: 57.9 million km
- Diameter: 4,879 km
- Day length: 58.6 Earth days
- Year length: 88 Earth days
- Known moons: 0

### Venus
**The Veiled World** — Wrapped in dense clouds, Venus holds the hottest surface in our planetary family.

- Distance from Sun: 108.2 million km
- Diameter: 12,104 km
- Day length: 243 Earth days
- Year length: 225 Earth days
- Known moons: 0

### Earth
**The Living Planet** — An ocean world with a thin atmosphere and the only known life in the cosmos.

- Distance from Sun: 149.6 million km
- Diameter: 12,756 km
- Day length: 23.9 hours
- Year length: 365.25 days
- Known moons: 1

### Mars
**The Red Planet** — A rust-colored desert shaped by ancient water, immense volcanoes, and thin air.

- Distance from Sun: 227.9 million km
- Diameter: 6,792 km
- Day length: 24.6 hours
- Year length: 687 Earth days
- Known moons: 2

### Jupiter
**The Giant** — A vast gas giant where cloud bands and immense storms encircle the largest planet.

- Distance from Sun: 778.6 million km
- Diameter: 142,984 km
- Day length: 9.9 hours
- Year length: 11.86 Earth years
- Known moons: 115

### Saturn
**The Ringed Giant** — A world of pale storms surrounded by a breathtaking disk of icy rings.

- Distance from Sun: 1.43 billion km
- Diameter: 120,536 km
- Day length: 10.7 hours
- Year length: 29.45 Earth years
- Known moons: 293

### Uranus
**The Sideways Planet** — An ice giant tipped almost onto its side, turning through the deep outer dark.

- Distance from Sun: 2.87 billion km
- Diameter: 51,118 km
- Day length: 17.2 hours
- Year length: 84 Earth years
- Known moons: 29

### Neptune
**The Outer Edge** — The most distant planet: a deep-blue world swept by supersonic winds.

- Distance from Sun: 4.5 billion km
- Diameter: 49,528 km
- Day length: 16.1 hours
- Year length: 164.8 Earth years
- Known moons: 16

---

## Features

- Real-time 3D rendering with Three.js
- Original GLB models for the Sun and all eight planets
- Scroll-driven journey with per-planet chapters
- Accurate relative planet sizes and compressed orbital distances for legibility
- Responsive layout for desktop and mobile

## Tech Stack

- TypeScript
- Three.js
- GSAP
- Vite

## Running Locally

```bash
cd solar-system-web
npm install
npm run dev
```

Then open the local URL printed by Vite.

### Build

```bash
cd solar-system-web
npm run build
```

## Project Structure

```
solar-system-web/
├── index.html
├── public/models/      # GLB models for the Sun and planets
├── src/
│   ├── data/           # Planet facts and visual scaling constants
│   ├── three/          # Scene, loaders, lighting, solar system
│   └── animation/      # Scroll-driven motion
└── scripts/            # Export, inventory, and browser QA tooling
```

Planet facts live in `solar-system-web/src/data/planets.ts`.
