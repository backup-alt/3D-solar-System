import * as THREE from 'three';
import './style.css';
import { planets } from './data/planets';
import { createRenderer } from './three/renderer';
import { createCamera } from './three/camera';
import { createStars } from './three/stars';
import { addLighting } from './three/lighting';
import { attachModel, createSolarSystem, updateOrbitLayout } from './three/solarSystem';
import { loadOpening, modelFailures } from './three/loaders';
import { createScrollJourney } from './animation/scroll';
import { startLoop } from './animation/loop';
import { createDebug } from './utils/debug';
import { qualitySettings } from './utils/responsive';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

const app = document.querySelector<HTMLDivElement>('#app')!;
const fact = (label: string, value: string) => `<div class="fact"><dt>${label}</dt><dd>${value}</dd></div>`;

app.innerHTML = `
  <div class="loader" id="loader" role="status" aria-live="polite">
    <div class="loader__inner"><span class="eyebrow">AN INTERACTIVE JOURNEY</span><strong>THE SOLAR SYSTEM</strong><span id="loader-message">Loading worlds… 0 / 2</span><div class="loader__track"><i id="loader-fill"></i></div></div>
  </div>
  <canvas class="space-canvas" id="space-canvas" aria-label="Real-time 3D Solar System"></canvas>
  <div class="grain" aria-hidden="true"></div>
  <div class="vignette" aria-hidden="true"></div>
  <header class="nav">
    <a class="nav__brand" href="#hero" aria-label="Return to Solar System overview"><span class="nav__symbol">✳</span><span>SOLAR<br>SYSTEM</span></a>
    <div class="nav__center"><span>AN INTERPLANETARY JOURNEY</span><span class="nav__line"></span><span class="nav__position">OVERVIEW</span></div>
    <button class="nav__menu" id="menu-button" type="button" aria-expanded="false" aria-controls="planet-menu">EXPLORE <span class="nav__menu-icon"><i></i><i></i></span></button>
  </header>
  <nav class="planet-menu" id="planet-menu" aria-label="Planet chapters" hidden><span class="planet-menu__label">CHOOSE A DESTINATION</span>${planets.map(p => `<a href="#${p.id}"><span>${p.number}</span>${p.name}</a>`).join('')}</nav>
  <div class="edge-index" aria-hidden="true"><span>01</span><div class="edge-index__track"><i></i></div><span>08</span></div>
  <main class="story">
    <section class="hero" id="hero" aria-labelledby="hero-title">
      <div class="hero__topline"><span>EST. 4.6 BILLION YEARS AGO</span><span>01 STAR &nbsp;·&nbsp; 08 PLANETS</span></div>
      <div class="hero__content"><p class="eyebrow hero__eyebrow">A JOURNEY BEYOND OUR WORLD</p><h1 id="hero-title">THE SOLAR<br><em>SYSTEM</em></h1><p class="hero__subtitle">Eight worlds. One star.<br>A universe of stories in between.</p></div>
      <div class="hero__bottom"><div class="scroll-hint"><span class="scroll-hint__line"></span><span>SCROLL TO EXPLORE</span></div><span>DRAG THROUGH SPACE BY SCROLLING</span><span class="hero__coordinate">SOL SYSTEM / MILKY WAY</span></div>
    </section>
    ${planets.map((p, index) => `
      <section class="chapter chapter--${p.id} ${index % 2 ? 'chapter--right' : 'chapter--left'}" id="${p.id}" aria-labelledby="heading-${p.id}" style="--accent:${p.accent}">
        <div class="chapter__content">
          <div class="chapter__kicker"><span class="chapter__dash"></span><span>CHAPTER ${p.number} / 08</span><span class="chapter__category">${p.category}</span></div>
          <h2 id="heading-${p.id}">${p.name.toUpperCase()}</h2>
          <p class="chapter__description">${p.description}</p>
          <dl class="facts">${fact('DISTANCE FROM SUN',p.distance)}${fact('DIAMETER',p.diameter)}${fact('LENGTH OF DAY',p.day)}${fact('LENGTH OF YEAR',p.year)}${fact('KNOWN MOONS',p.moons)}</dl>
          <div class="chapter__next">${index < planets.length-1 ? `NEXT WORLD <span>${planets[index+1].name.toUpperCase()}</span><b aria-hidden="true">↘</b>` : 'END OF THE PLANETARY JOURNEY'}</div>
        </div>
        <span class="chapter__watermark" aria-hidden="true">${p.number}</span>
        ${index === planets.length-1 ? `<footer class="story-footer"><span>BEYOND NEPTUNE, THE JOURNEY CONTINUES.</span><a href="#hero">RETURN TO THE SUN ↑</a><a href="https://science.nasa.gov/solar-system/planet-sizes-and-locations-in-our-solar-system/" target="_blank" rel="noreferrer">PLANET FACTS: NASA ↗</a><a href="https://ssd.jpl.nasa.gov/sats/discovery.html" target="_blank" rel="noreferrer">MOON COUNTS: NASA/JPL ↗</a></footer>` : ''}
      </section>`).join('')}
  </main>
  <div class="model-warning" id="model-warning" hidden></div>
`;

const menuButton = document.querySelector<HTMLButtonElement>('#menu-button')!;
const menu = document.querySelector<HTMLElement>('#planet-menu')!;
const closeMenu = () => { menu.hidden = true; menuButton.setAttribute('aria-expanded','false'); };
menuButton.addEventListener('click', () => { const open = menu.hidden; menu.hidden = !open; menuButton.setAttribute('aria-expanded', String(open)); });
menu.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });

const canvas = document.querySelector<HTMLCanvasElement>('#space-canvas')!;
const scene = new THREE.Scene(); // Scene holds all Mesh, Group, light and star objects.
scene.background = new THREE.Color(0x05070c);
const camera = createCamera();
let renderer: THREE.WebGLRenderer;
try {
  renderer = createRenderer(canvas);
} catch (error) {
  const message = document.querySelector<HTMLElement>('#loader-message')!;
  message.textContent = 'This 3D experience needs a browser with WebGL enabled.';
  throw error;
}

scene.add(createStars());
addLighting(scene);
createSolarSystem(scene);
const journey = createScrollJourney();
const debug = createDebug(renderer, camera, journey);
startLoop(scene, camera, renderer, journey, debug);
// Sections are created by TypeScript, so a bookmarked #planet must scroll
// after the DOM and ScrollTrigger exist, rather than during HTML parsing.
requestAnimationFrame(() => {
  const target = document.getElementById(location.hash.slice(1));
  if (target) {
    target.scrollIntoView({ behavior: 'instant', block: 'start' });
    ScrollTrigger.refresh();
  }
});

window.addEventListener('resize', () => {
  updateOrbitLayout();
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.fov = window.innerWidth <= 700 ? 48 : 42;
  camera.updateProjectionMatrix();
  renderer.setPixelRatio(qualitySettings().pixelRatio);
  renderer.setSize(window.innerWidth, window.innerHeight, false);
  ScrollTrigger.refresh();
}, { passive: true });

const loaderEl = document.querySelector<HTMLElement>('#loader')!;
const loaderMessage = document.querySelector<HTMLElement>('#loader-message')!;
const loaderFill = document.querySelector<HTMLElement>('#loader-fill')!;
const warning = document.querySelector<HTMLElement>('#model-warning')!;

async function boot() {
  try {
    await loadOpening((completed, total) => {
      loaderMessage.textContent = `Loading worlds… ${completed} / ${total}`;
      loaderFill.style.transform = `scaleX(${completed / total})`;
    });
    await Promise.all([attachModel('sun'), attachModel('mercury')]);
    loaderEl.classList.add('is-loaded');
    setTimeout(() => loaderEl.remove(), 950);
    // The hero remains interactive while additional GLBs arrive progressively.
    for (const planet of planets.slice(1)) {
      try { await attachModel(planet.id); }
      catch (error) { console.error(error); }
    }
    if (modelFailures().size) {
      warning.hidden = false;
      warning.textContent = `Some worlds could not load: ${[...modelFailures().keys()].join(', ')}. Refresh to retry.`;
    }
  } catch (error) {
    console.error(error);
    loaderMessage.textContent = `A required model failed to load. ${error instanceof Error ? error.message : ''}`;
    loaderFill.style.background = '#d7907d';
  }
}
boot();
