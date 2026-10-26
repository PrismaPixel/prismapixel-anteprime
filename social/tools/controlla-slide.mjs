// Controllo delle slide · PrismaPixel
// Uso: node controlla-slide.mjs /tmp/lavoro/<slug>/index.html /tmp/lavoro/<slug>/controlli
// - salva ogni tela a 1080x1350 come PNG (da guardare con Read, una per una)
// - salva la pagina a 390 px e a 1280 px
// - segnala testo che esce dalla tela o dai margini di sicurezza (64 px), font non caricati, immagini rotte,
//   testo sotto i 28 px nelle tele e scorrimento orizzontale della pagina
import { createRequire } from 'module';
import { mkdirSync, writeFileSync } from 'fs';
import { pathToFileURL } from 'url';
import { resolve } from 'path';
// require: trova Playwright anche quando è installato globalmente (NODE_PATH)
const { chromium } = createRequire(import.meta.url)('playwright');

const [file, out = './controlli'] = process.argv.slice(2);
if (!file) { console.error('Uso: node controlla-slide.mjs index.html [cartella]'); process.exit(1); }
mkdirSync(out, { recursive: true });
const url = /^https?:/.test(file) ? file : pathToFileURL(resolve(file)).href;
const browser = await chromium.launch();
const problemi = [];

// 1. Ogni tela a misura reale
const p = await browser.newPage({ viewport: { width: 1200, height: 1500 } });
await p.goto(url, { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
const info = await p.evaluate(() => {
  const SICUREZZA = 64;
  const ris = [];
  document.querySelectorAll('.tela').forEach((t, i) => {
    t.style.transform = 'none';
    t.closest('.cornice').style.cssText = 'width:1080px;height:1350px;flex:0 0 1080px;aspect-ratio:auto';
    const r = t.getBoundingClientRect();
    const fuori = [], piccoli = [];
    t.querySelectorAll('*').forEach(el => {
      if (!el.childNodes.length || ![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
      const b = el.getBoundingClientRect();
      if (!b.width || !b.height) return;
      const testo = el.textContent.trim().slice(0, 40);
      if (b.left < r.left + SICUREZZA - 1 || b.right > r.right - SICUREZZA + 1 || b.top < r.top + SICUREZZA - 1 || b.bottom > r.bottom - SICUREZZA + 1) {
        if (!el.closest('[data-fuori-ok]')) fuori.push(testo); // data-fuori-ok: elementi decorativi voluti oltre il margine
      }
      if (parseFloat(getComputedStyle(el).fontSize) < 28) piccoli.push(testo);
      if (el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).overflow !== 'visible') fuori.push('taglio: ' + testo);
    });
    const post = t.closest('.post');
    ris.push({ i, post: [...document.querySelectorAll('.post')].indexOf(post) + 1, slide: [...post.querySelectorAll('.tela')].indexOf(t) + 1, fuori, piccoli });
  });
  const immaginiRotte = [...document.images].filter(im => !im.complete || !im.naturalWidth).map(im => im.src.slice(0, 80));
  const fontMancanti = [...document.fonts].filter(f => f.status === 'error').map(f => f.family);
  return { ris, immaginiRotte, fontMancanti };
});
const tele = await p.$$('.tela');
for (let i = 0; i < tele.length; i++) {
  const r = info.ris[i];
  await tele[i].screenshot({ path: `${out}/post${r.post}-slide${String(r.slide).padStart(2, '0')}.png` });
  if (r.fuori.length) problemi.push(`post ${r.post} slide ${r.slide}: testo fuori dai margini di sicurezza → ${r.fuori.join(' | ')}`);
  if (r.piccoli.length) problemi.push(`post ${r.post} slide ${r.slide}: testo sotto 28 px → ${r.piccoli.join(' | ')}`);
}
if (info.immaginiRotte.length) problemi.push('immagini che non si caricano: ' + info.immaginiRotte.join(', '));
if (info.fontMancanti.length) problemi.push('font non caricati: ' + info.fontMancanti.join(', '));

// 2. Pagina a 390 px e a 1280 px
for (const w of [390, 1280]) {
  const q = await browser.newPage({ viewport: { width: w, height: 844 } });
  await q.goto(url, { waitUntil: 'networkidle' });
  await q.evaluate(() => document.fonts.ready);
  await q.waitForTimeout(300);
  const larga = await q.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  if (larga) problemi.push(`a ${w} px la pagina scorre in orizzontale`);
  await q.screenshot({ path: `${out}/pagina-${w}.png`, fullPage: true });
}
await browser.close();
writeFileSync(`${out}/esito.txt`, problemi.length ? problemi.join('\n') : 'OK');
console.log(problemi.length ? 'DA SISTEMARE:\n' + problemi.join('\n') : `OK · ${tele.length} tele controllate`);
process.exit(problemi.length ? 2 : 0);
