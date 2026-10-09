// Calcula altura/azimut con el código de index.html para comparar con astropy (tools/check_astropy.py)
import fs from 'fs';
const html = fs.readFileSync(new URL('../index.html', import.meta.url), 'utf8');
const src = html.match(/<script id="astro">([\s\S]*?)<\/script>/)[1];
const Astro = new Function(src + '; return Astro;')();
const data = html.match(/const STARS=(\[.*?\]);/s)[1];
const STARS = JSON.parse(data);
const D2R = Math.PI / 180, R2D = 180 / Math.PI;
const lat = -33.0422, lon = -71.3733;
const dates = ['2026-10-09T23:30:00Z', '2026-10-10T03:00:00Z', '2026-06-21T04:00:00Z', '2025-01-15T02:00:00Z', '2027-03-01T08:00:00Z', '2030-12-24T01:00:00Z'];
const names = ['Sirius', 'Canopus', 'Acrux', 'Antares', 'Rigel', 'Achernar', 'Fomalhaut', 'Vega', 'Arcturus'];
const out = [];
for (const ds of dates) {
  const date = new Date(ds), T = Astro.centuries(date), P = Astro.precessionMatrix(T);
  const lst = Astro.gmst(date) + lon, HM = Astro.horizonMatrix(lst, lat);
  const aa = v => { const h = Astro.mulMV(HM, v); return [Math.asin(h[2]) * R2D, Astro.n360(Math.atan2(h[0], h[1]) * R2D)]; };
  const r = { date: ds, bodies: {}, stars: {} };
  r.bodies.sun = aa(Astro.sun(T).vec);
  const m = Astro.moon(T), er = m.dist / 6378.14, la = lat * D2R, th = lst * D2R;
  const mv = [m.vec[0] * er - Math.cos(la) * Math.cos(th), m.vec[1] * er - Math.cos(la) * Math.sin(th), m.vec[2] * er - Math.sin(la)], ml = Math.hypot(...mv);
  r.bodies.moon = aa(mv.map(x => x / ml));
  r.moonDist = m.dist;
  for (const p of ['mercurio', 'venus', 'marte', 'jupiter', 'saturno']) { const pl = Astro.planet(p, T); r.bodies[p] = aa(Astro.mulMV(P, pl.vec)); r[p + 'Mag'] = pl.mag; }
  for (const n of names) { const s = STARS.find(s => s[6] === n); r.stars[n] = { ra: s[0], dec: s[1], aa: aa(Astro.mulMV(P, Astro.radecToVec(s[0], s[1]))) }; }
  out.push(r);
}
console.log(JSON.stringify(out));
