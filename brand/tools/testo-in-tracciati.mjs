// Testo → tracciati SVG, per loghi che non dipendono da nessun font installato.
//
//   node testo-in-tracciati.mjs --font fraunces --peso 600 [--stile normal|italic] --testo "Masseria Lume"
//        [--corpo 200] [--spaziatura 0.04] [--maiuscolo] [--out logotipo.svg]
//
// Il font arriva da npm (@fontsource/<font>, licenze aperte: OFL o Apache): lo script lo installa da solo in
// /tmp/officina-font. --spaziatura è in em (0.04 = +4%). Stampa un SVG con un solo <path> per lettera
// (id "l0", "l1"... per ritoccarle a mano: legature, tagli, contrografismi) e il viewBox stretto sull'inchiostro.
// Con --json stampa invece {viewBox, larghezza, altezza, lettere:[{car, d, x, avanzamento}]} per comporre a mano.
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';

const a = process.argv.slice(2);
const arg = (k, d) => { const i = a.indexOf('--' + k); return i >= 0 ? (a[i + 1] && !a[i + 1].startsWith('--') ? a[i + 1] : true) : d; };
const font = String(arg('font', '')).toLowerCase().trim().replace(/\s+/g, '-');
const peso = String(arg('peso', '400'));
const stile = String(arg('stile', 'normal'));
let testo = String(arg('testo', ''));
const corpo = Number(arg('corpo', 200));
const spaziatura = Number(arg('spaziatura', 0));
if (!font || !testo) { console.error('uso: --font <nome-fontsource> --peso 600 --testo "Nome"'); process.exit(1); }
if (arg('maiuscolo', false)) testo = testo.toUpperCase();

const DIR = '/tmp/officina-font';
mkdirSync(DIR, { recursive: true });
if (!existsSync(path.join(DIR, 'package.json'))) writeFileSync(path.join(DIR, 'package.json'), '{"name":"officina-font","private":true}');
const pacchetto = `@fontsource/${font}`;
if (!existsSync(path.join(DIR, 'node_modules', pacchetto))) {
  try { execFileSync('npm', ['i', '--silent', '--no-audit', '--no-fund', pacchetto], { cwd: DIR, stdio: 'pipe' }); }
  catch (e) { console.error(`✗ font "${font}" non trovato su npm (@fontsource/${font}): scegli un altro font Google`); process.exit(2); }
}
if (!existsSync(path.join(DIR, 'node_modules', 'opentype.js'))) execFileSync('npm', ['i', '--silent', '--no-audit', '--no-fund', 'opentype.js@1.3.4'], { cwd: DIR, stdio: 'pipe' });
const req = createRequire(path.join(DIR, 'package.json'));
const opentype = req('opentype.js');

// Il file .woff (WOFF 1) del sottoinsieme latino; se manca il "latin-ext" serve per lettere come ő ł
const cartella = path.join(DIR, 'node_modules', pacchetto, 'files');
const cerca = sub => path.join(cartella, `${font}-${sub}-${peso}-${stile}.woff`);
const file = [cerca('latin'), cerca('latin-ext')].find(existsSync);
if (!file) { console.error(`✗ ${font} non ha il peso ${peso} ${stile}: guarda ${cartella}`); process.exit(3); }
const buf = readFileSync(file);
const f = opentype.parse(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));

const scala = corpo / f.unitsPerEm;
const lettere = [];
let x = 0;
const glifi = f.stringToGlyphs(testo);
glifi.forEach((g, i) => {
  const car = testo[i] || '';
  const p = g.getPath(x, corpo, corpo);
  const bb = p.getBoundingBox();
  lettere.push({ car, d: p.toPathData(1), x: +x.toFixed(2), avanzamento: +(g.advanceWidth * scala).toFixed(2), bb });
  const kern = i < glifi.length - 1 ? f.getKerningValue(g, glifi[i + 1]) * scala : 0;
  x += g.advanceWidth * scala + kern + spaziatura * corpo;
});
// viewBox stretto sull'inchiostro reale
let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
lettere.forEach(l => {
  if (!l.d) return;
  x0 = Math.min(x0, l.bb.x1); y0 = Math.min(y0, l.bb.y1); x1 = Math.max(x1, l.bb.x2); y1 = Math.max(y1, l.bb.y2);
  delete l.bb;
});
const vb = [x0, y0, x1 - x0, y1 - y0].map(v => +v.toFixed(2));
if (arg('json', false)) {
  console.log(JSON.stringify({ font, peso, stile, corpo, viewBox: vb.join(' '), larghezza: vb[2], altezza: vb[3], ascendente: +(f.ascender * scala).toFixed(2), linea_base: corpo, lettere }, null, 1));
} else {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb.join(' ')}" width="${vb[2]}" height="${vb[3]}">\n` +
    `<!-- ${testo} · ${font} ${peso} ${stile} · tracciati, nessun font richiesto -->\n<g fill="currentColor">\n` +
    lettere.filter(l => l.d).map((l, i) => `  <path id="l${i}" data-car="${l.car.replace(/"/g, '&quot;')}" d="${l.d}"/>`).join('\n') + '\n</g>\n</svg>\n';
  const out = arg('out', '');
  if (out && out !== true) { writeFileSync(out, svg); console.log(`✓ ${out} · ${vb[2]}×${vb[3]}`); } else process.stdout.write(svg);
}
