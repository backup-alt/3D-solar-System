export type PlanetId = 'mercury' | 'venus' | 'earth' | 'mars' | 'jupiter' | 'saturn' | 'uranus' | 'neptune';

export interface PlanetData {
  id: PlanetId;
  number: string;
  name: string;
  category: string;
  description: string;
  distance: string;
  diameter: string;
  day: string;
  year: string;
  moons: string;
  radius: number;
  orbitRadius: number;
  orbitYears: number;
  spinHours: number;
  axialTilt: number;
  orbitInclination: number;
  startAngle: number;
  accent: string;
}

// Presentation units deliberately compress both size and orbital distance.
// Radii preserve the obvious relative hierarchy, while every world remains legible.
// Physical facts below are separate from these visual scaling constants.
export const planets: PlanetData[] = [
  {id:'mercury', number:'01', name:'Mercury', category:'THE SWIFT PLANET', description:'A small, cratered world tracing the innermost path around the Sun.', distance:'57.9 million km', diameter:'4,879 km', day:'58.6 Earth days', year:'88 Earth days', moons:'0', radius:0.24, orbitRadius:4.2, orbitYears:0.241, spinHours:1407.6, axialTilt:0.03, orbitInclination:7.0, startAngle:0.8, accent:'#c6b4a2'},
  {id:'venus', number:'02', name:'Venus', category:'THE VEILED WORLD', description:'Wrapped in dense clouds, Venus holds the hottest surface in our planetary family.', distance:'108.2 million km', diameter:'12,104 km', day:'243 Earth days', year:'225 Earth days', moons:'0', radius:0.49, orbitRadius:5.5, orbitYears:0.615, spinHours:-5832.5, axialTilt:177.4, orbitInclination:3.4, startAngle:2.15, accent:'#e5bf8c'},
  {id:'earth', number:'03', name:'Earth', category:'THE LIVING PLANET', description:'An ocean world with a thin atmosphere and the only known life in the cosmos.', distance:'149.6 million km', diameter:'12,756 km', day:'23.9 hours', year:'365.25 days', moons:'1', radius:0.52, orbitRadius:6.9, orbitYears:1, spinHours:23.9, axialTilt:23.4, orbitInclination:0, startAngle:4.15, accent:'#91b8d6'},
  {id:'mars', number:'04', name:'Mars', category:'THE RED PLANET', description:'A rust-colored desert shaped by ancient water, immense volcanoes, and thin air.', distance:'227.9 million km', diameter:'6,792 km', day:'24.6 hours', year:'687 Earth days', moons:'2', radius:0.34, orbitRadius:8.2, orbitYears:1.881, spinHours:24.6, axialTilt:25.2, orbitInclination:1.85, startAngle:5.45, accent:'#ce846d'},
  {id:'jupiter', number:'05', name:'Jupiter', category:'THE GIANT', description:'A vast gas giant where cloud bands and immense storms encircle the largest planet.', distance:'778.6 million km', diameter:'142,984 km', day:'9.9 hours', year:'11.86 Earth years', moons:'115', radius:1.12, orbitRadius:10.3, orbitYears:11.86, spinHours:9.9, axialTilt:3.1, orbitInclination:1.3, startAngle:0.15, accent:'#d4aa86'},
  {id:'saturn', number:'06', name:'Saturn', category:'THE RINGED GIANT', description:'A world of pale storms surrounded by a breathtaking disk of icy rings.', distance:'1.43 billion km', diameter:'120,536 km', day:'10.7 hours', year:'29.45 Earth years', moons:'293', radius:0.94, orbitRadius:12.7, orbitYears:29.45, spinHours:10.7, axialTilt:26.7, orbitInclination:2.49, startAngle:2.7, accent:'#dac5a4'},
  {id:'uranus', number:'07', name:'Uranus', category:'THE SIDEWAYS PLANET', description:'An ice giant tipped almost onto its side, turning through the deep outer dark.', distance:'2.87 billion km', diameter:'51,118 km', day:'17.2 hours', year:'84 Earth years', moons:'29', radius:0.71, orbitRadius:15.1, orbitYears:84, spinHours:-17.2, axialTilt:97.8, orbitInclination:0.77, startAngle:4.55, accent:'#9ed3d7'},
  {id:'neptune', number:'08', name:'Neptune', category:'THE OUTER EDGE', description:'The most distant planet: a deep-blue world swept by supersonic winds.', distance:'4.5 billion km', diameter:'49,528 km', day:'16.1 hours', year:'164.8 Earth years', moons:'16', radius:0.68, orbitRadius:17.4, orbitYears:164.8, spinHours:16.1, axialTilt:28.3, orbitInclination:1.77, startAngle:5.65, accent:'#8ba7e8'},
];

export const planetById = Object.fromEntries(planets.map(planet => [planet.id, planet])) as Record<PlanetId, PlanetData>;
