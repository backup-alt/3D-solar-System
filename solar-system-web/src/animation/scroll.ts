import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { planets } from '../data/planets';
import { attachModel } from '../three/solarSystem';

gsap.registerPlugin(ScrollTrigger);

export interface JourneyState { progress: number; current: string; }

export function createScrollJourney() {
  const state: JourneyState = { progress: 0, current: 'overview' };
  const story = document.querySelector<HTMLElement>('.story')!;

  // ScrollTrigger writes a single camera progress value. The render loop then
  // combines it with each planet's live orbital position for continuous travel.
  gsap.to(state, {
    progress: planets.length,
    ease: 'none',
    onUpdate: () => {
      document.documentElement.style.setProperty('--journey-progress', String(state.progress / planets.length));
      const current = Math.min(planets.length - 1, Math.max(0, Math.round(state.progress) - 1));
      state.current = state.progress < 0.55 ? 'overview' : planets[current].id;
      const label = document.querySelector<HTMLElement>('.nav__position');
      if (label) label.textContent = state.progress < 0.55 ? 'OVERVIEW' : `${planets[current].number} / 08`;
    },
    scrollTrigger: { trigger: story, start: 'top top', end: 'bottom bottom', scrub: 1.1, invalidateOnRefresh: true },
  });

  gsap.to('.hero__content', {
    opacity: 0, y: -70, ease: 'none',
    scrollTrigger: { trigger: '#hero', start: 'top top', end: 'bottom 45%', scrub: true },
  });

  for (const [index, planet] of planets.entries()) {
    const section = document.getElementById(planet.id)!;
    ScrollTrigger.create({
      trigger: section,
      start: 'top 65%',
      end: 'bottom 35%',
      onEnter: () => activate(index),
      onEnterBack: () => activate(index),
      onLeave: () => section.classList.remove('is-active'),
      onLeaveBack: () => section.classList.remove('is-active'),
    });
    function activate(i: number) {
      state.current = planet.id;
      section.classList.add('is-active');
      // Ensure this world and its neighbors are ready before they enter frame.
      for (const neighbor of planets.slice(Math.max(0, i - 1), Math.min(planets.length, i + 3))) {
        attachModel(neighbor.id).catch(error => console.error(error));
      }
    }
  }
  return state;
}
