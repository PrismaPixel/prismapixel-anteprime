// Controllo dell'identità di marca · PrismaPixel
// Uso: node controlla-brand.mjs /tmp/lavoro/<slug> [/tmp/lavoro/<slug>/controlli]
//
// Nella cartella: index.html (la pagina del brand board) e i file SVG pubblicati (logo-*.svg, marchio-*.svg,
// pattern-*.svg, etichetta-*.svg / menu-*.svg per le applicazioni progettate). Salva da guardare con Read:
//   - <file>-prova.png per ogni logo: grande, a 64/32/16 px, su chiaro e su scuro, e a un colore (nero e bianco);
//   - <pattern>-prova.png: la tessera ripetuta 3×3, per vedere le giunture;
//   - pagina-390.png e pagina-1280.png.
// Segnala come ERRORE: SVG che non si apre, logo con <text> o <image> o link esterni (deve essere fatto di
// tracciati), logo vuoto, coppie di colori dichiarate senza contrasto AA, immagini rotte, font non caricati,
// scorrimento orizzontale della pagina. Come AVVISO: dettagli che spariscono a 16 px, SVG più grandi di 60 KB.
//
// Le coppie di colori da controllare stanno nella pagina in
// <script type="application/json" id="brand-dati">{"direzioni":[{"nome":"…","palette":[{"nome":"Calce","hex":"#F4EFE6"},…],
//   "coppie":[["#2B2A26","#F4EFE6","testo"],["#F4EFE6","#9A4A2E","logo"]]}]}</script>
// ("testo" vuole 4,5:1, "logo" e "grande" 3:1).
import { createRequire } from 'module';
import { mkdirSync, readdirSync, readFileSync, writeFileSync, existsSync } from 'fs';
import { pathToFileURL } from 'url';
import { join, resolve, basename } from 'path';
const { chromium } = createRequire(import.meta.url)('playwright');

const [dir, outArg] = process.argv.slice(2);
if (!dir) { console.error('Uso: node controlla-brand.mjs <cartella> [controlli]'); process.exit(1); }
const out = resolve(outArg || join(dir, 'controlli'));
mkdirSync(out, { recursive: true });
const errori = [], avvisi = [];
const svgFiles = readdirSync(dir).filter(f => f.endsWith('.svg')).sort();
const pezzi = svgFiles.filter(f => /^(etichetta|menu|scatola|pezzo)/.test(f)); // applicazioni progettate: niente prova a 16 px
const loghi = svgFiles.filter(f => !/^pattern/.test(f) && !pezzi.includes(f));
const pattern = svgFiles.filter(f => /^pattern/.test(f));

// 1. Controlli sul testo degli SVG
for (const f of svgFiles) {
  const s = readFileSync(join(dir, f), 'utf8');
  const kb = Buffer.byteLength(s) / 1024;
  if (!/^\s*(<\?xml[^>]*>\s*)?(<!--[\s\S]*?-->\s*)*<svg[\s>]/.test(s)) errori.push(`${f}: non comincia con <svg>`);
  if (!/viewBox=/.test(s)) errori.push(`${f}: manca viewBox (non si ridimensiona bene)`);
  if (/<text[\s>]/.test(s) && !/^pattern/.test(f)) errori.push(`${f}: contiene <text>: converti le scritte in tracciati (testo-in-tracciati.mjs)`);
  if (/<image[\s>]/.test(s)) errori.push(`${f}: contiene un'immagine raster: il logo deve essere vettoriale`);
  if (/(href|src)=["']https?:/.test(s) || /@import|url\(\s*["']?https?:/.test(s)) errori.push(`${f}: richiama file esterni`);
  if (/<script/i.test(s)) errori.push(`${f}: contiene script`);
  if (kb > 60) avvisi.push(`${f}: ${kb.toFixed(0)} KB, semplifica i tracciati`);
}

const browser = await chromium.launch();
const p = await browser.newPage({ viewport: { width: 1400, height: 900 } });

// 2. Prove dei loghi: grande, piccolo, chiaro/scuro, un colore
for (const f of loghi) {
  const s = readFileSync(join(dir, f), 'utf8');
  const uri = 'data:image/svg+xml;base64,' + Buffer.from(s).toString('base64');
  const html = `<!doctype html><html><body style="margin:0;font:12px system-ui;background:#fff">
  <style>.r{display:flex;align-items:center;gap:28px;padding:22px}.k{width:520px;height:300px;display:flex;align-items:center;justify-content:center}
  img{display:block;object-fit:contain}.c{background:#f2f1ee}.s{background:#1d1d1b}.mono{filter:brightness(0)}.inv{filter:brightness(0) invert(1)}
  .l{color:#888;width:70px}</style>
  <div class="r c"><div class="k"><img src="${uri}" style="max-width:460px;max-height:260px"></div>
    <img src="${uri}" style="height:64px"><img src="${uri}" style="height:32px"><img src="${uri}" style="height:16px"></div>
  <div class="r s"><div class="k"><img class="inv" src="${uri}" style="max-width:460px;max-height:260px"></div>
    <img class="inv" src="${uri}" style="height:64px"><img class="inv" src="${uri}" style="height:32px"><img class="inv" src="${uri}" style="height:16px"></div>
  <div class="r"><div class="l">un colore</div><img class="mono" src="${uri}" style="height:120px"><img class="mono" src="${uri}" style="height:24px"></div>
  </body></html>`;
  await p.setContent(html, { waitUntil: 'load' });
  const ok = await p.evaluate(() => [...document.images].every(i => i.complete && i.naturalWidth > 0));
  if (!ok) { errori.push(`${f}: il browser non riesce ad aprirlo`); continue; }
  // inchiostro: il logo grande deve occupare spazio vero; a 16 px deve restare qualcosa di leggibile
  const ink = await p.evaluate(async () => {
    const misura = (img, w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d');
      g.fillStyle = '#fff'; g.fillRect(0, 0, w, h); const r = Math.min(w / img.naturalWidth, h / img.naturalHeight);
      g.drawImage(img, 0, 0, img.naturalWidth * r, img.naturalHeight * r); const d = g.getImageData(0, 0, w, h).data; let n = 0;
      for (let k = 0; k < d.length; k += 4) if (d[k] + d[k + 1] + d[k + 2] < 600) n++; return n / (w * h); };
    const img = document.images[0];
    return { grande: misura(img, 460, 260), piccolo: misura(img, 48, 16) };
  });
  if (ink.grande < 0.01) errori.push(`${f}: sembra vuoto o troppo chiaro su bianco`);
  if (ink.piccolo < 0.04) avvisi.push(`${f}: a 16 px resta poco: prepara una versione semplificata (marchio) per le misure piccole`);
  await p.setViewportSize({ width: 1400, height: 900 });
  await p.screenshot({ path: join(out, basename(f, '.svg') + '-prova.png'), fullPage: true });
}

// 2b. Applicazioni progettate (etichette, menu…): a misura di lettura
for (const f of pezzi) {
  const s = readFileSync(join(dir, f), 'utf8');
  const uri = 'data:image/svg+xml;base64,' + Buffer.from(s).toString('base64');
  await p.setContent(`<!doctype html><body style="margin:0;background:#bbb;padding:20px"><img src="${uri}" style="width:700px;display:block"></body>`, { waitUntil: 'load' });
  await p.screenshot({ path: join(out, basename(f, '.svg') + '-prova.png'), fullPage: true });
}

// 3. Pattern: tessera ripetuta 3×3
for (const f of pattern) {
  const s = readFileSync(join(dir, f), 'utf8');
  const uri = 'data:image/svg+xml;base64,' + Buffer.from(s).toString('base64');
  await p.setContent(`<!doctype html><body style="margin:0"><div style="width:900px;height:900px;background:url('${uri}');background-size:300px auto;outline:1px solid #ccc"></div></body>`, { waitUntil: 'load' });
  await p.waitForTimeout(150);
  await p.screenshot({ path: join(out, basename(f, '.svg') + '-prova.png'), clip: { x: 0, y: 0, width: 900, height: 900 } });
}

// 4. Pagina: telefono e computer, contrasti dichiarati
const pagina = join(dir, 'index.html');
if (!existsSync(pagina)) errori.push('manca index.html');
else {
  const url = pathToFileURL(resolve(pagina)).href;
  for (const w of [390, 1280]) {
    await p.setViewportSize({ width: w, height: 900 });
    await p.goto(url, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    // tutte le direzioni una sotto l'altra, così lo screenshot le mostra tutte
    await p.addStyleTag({ content: '.dir{display:block!important}.scelta{position:static!important}' });
    await p.waitForTimeout(300);
    const st = await p.evaluate(() => ({
      orizz: document.documentElement.scrollWidth > window.innerWidth + 1,
      rotte: [...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.src.slice(0, 90)),
      font: [...document.fonts].filter(f => f.status === 'error').map(f => f.family),
      dati: (() => { try { return JSON.parse(document.getElementById('brand-dati').textContent); } catch (_) { return null; } })(),
    }));
    if (st.orizz) errori.push(`pagina a ${w} px: scorre di lato`);
    st.rotte.forEach(u => errori.push(`immagine rotta: ${u}`));
    st.font.forEach(f => errori.push(`font non caricato: ${f}`));
    if (w === 390) {
      if (!st.dati) avvisi.push('manca <script id="brand-dati"> con palette e coppie: contrasti non controllati');
      else {
        const lum = h => { const c = h.replace('#', '').match(/../g).map(x => parseInt(x, 16) / 255).map(v => v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; };
        const cr = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((m, n) => n - m); return (x + 0.05) / (y + 0.05); };
        (st.dati.direzioni || []).forEach(d => (d.coppie || []).forEach(([a, b, uso]) => {
          if (!/^#[0-9a-f]{6}$/i.test(a) || !/^#[0-9a-f]{6}$/i.test(b)) { errori.push(`${d.nome}: colore non valido in ${a}/${b}`); return; }
          const v = cr(a, b), min = uso === 'testo' ? 4.5 : 3;
          if (v < min) errori.push(`${d.nome}: ${a} su ${b} (${uso}) contrasto ${v.toFixed(2)}, serve ${min}`);
        }));
      }
    }
    await p.screenshot({ path: join(out, `pagina-${w}.png`), fullPage: true });
  }
}
await browser.close();
const tuttiPng = [...loghi, ...pezzi];
const rapporto = [`ERRORI: ${errori.length ? '' : 'nessuno'}`, ...errori.map(e => '  ✗ ' + e), `AVVISI: ${avvisi.length ? '' : 'nessuno'}`, ...avvisi.map(a => '  ! ' + a),
  `Guarda con Read: ${tuttiPng.map(f => basename(f, '.svg') + '-prova.png').concat(pattern.map(f => basename(f, '.svg') + '-prova.png'), ['pagina-390.png', 'pagina-1280.png']).join(', ')}`];
writeFileSync(join(out, 'rapporto.txt'), rapporto.join('\n') + '\n');
console.log(rapporto.join('\n'));
console.log(errori.length ? 'ESITO: DA CORREGGERE' : 'ESITO: OK');
process.exit(errori.length ? 1 : 0);
