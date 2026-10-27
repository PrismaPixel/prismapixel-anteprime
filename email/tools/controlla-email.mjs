// Controllo delle email · PrismaPixel
// Uso: node controlla-email.mjs /tmp/lavoro/<slug>/index.html /tmp/lavoro/<slug>/controlli
// Per ogni <article class="email">:
// - oggetto (massimo 60 caratteri, meglio sotto i 45) e anteprima (40-110 caratteri) presenti;
// - HTML dell'email: niente <script> né fogli di stile esterni, larghezza massima 600 px, immagini con alt,
//   almeno un link (CTA), link per annullare l'iscrizione, testo di almeno 14 px;
// - salva l'email a 375 e a 600 px (da guardare con Read) e segnala lo scorrimento orizzontale.
// Poi salva la pagina a 390 e a 1280 px.
import { createRequire } from 'module';
import { mkdirSync, writeFileSync } from 'fs';
import { pathToFileURL } from 'url';
import { resolve } from 'path';
const { chromium } = createRequire(import.meta.url)('playwright');

const [file, out = './controlli'] = process.argv.slice(2);
if (!file) { console.error('Uso: node controlla-email.mjs index.html [cartella]'); process.exit(1); }
mkdirSync(out, { recursive: true });
const url = /^https?:/.test(file) ? file : pathToFileURL(resolve(file)).href;
const browser = await chromium.launch();
const problemi = [], avvisi = [];

const p = await browser.newPage({ viewport: { width: 1280, height: 900 } });
await p.goto(url, { waitUntil: 'networkidle' });
const emails = await p.evaluate(() => [...document.querySelectorAll('article.email')].map(e => ({
  oggetto: (e.querySelector('.oggetto') || {}).textContent?.trim() || '',
  anteprima: (e.querySelector('.anteprima') || {}).textContent?.trim() || '',
  html: (e.querySelector('template.html') || {}).innerHTML || '',
})));
if (!emails.length) problemi.push('nessuna <article class="email"> trovata');

for (let i = 0; i < emails.length; i++) {
  const e = emails[i], n = `email ${i + 1}`;
  if (!e.oggetto) problemi.push(`${n}: oggetto mancante`);
  else if (e.oggetto.length > 60) problemi.push(`${n}: oggetto di ${e.oggetto.length} caratteri (massimo 60)`);
  else if (e.oggetto.length > 45) avvisi.push(`${n}: oggetto di ${e.oggetto.length} caratteri, su telefono si taglia dopo circa 40`);
  if (e.anteprima.length < 40 || e.anteprima.length > 110) problemi.push(`${n}: anteprima di ${e.anteprima.length} caratteri (40-110)`);
  if (!e.html.trim()) { problemi.push(`${n}: HTML dell'email mancante`); continue; }
  if (/<script/i.test(e.html)) problemi.push(`${n}: contiene <script>`);
  if (/<link[^>]+stylesheet/i.test(e.html)) problemi.push(`${n}: foglio di stile esterno (i client email lo ignorano)`);
  if (!/iscrizion|disiscri|unsubscribe/i.test(e.html)) problemi.push(`${n}: manca il link per annullare l'iscrizione`);
  for (const w of [375, 600]) {
    const q = await browser.newPage({ viewport: { width: w, height: 800 } });
    await q.setContent(e.html, { waitUntil: 'networkidle' });
    const r = await q.evaluate(() => {
      const larga = document.documentElement.scrollWidth > window.innerWidth + 1;
      const troppoLarghe = [...document.querySelectorAll('table,div,img')].filter(el => el.getBoundingClientRect().width > 601).length;
      const senzaAlt = [...document.images].filter(im => !im.hasAttribute('alt')).length;
      const link = [...document.querySelectorAll('a[href]')].length;
      const piccoli = [...document.querySelectorAll('p,td,li,a,span,h1,h2,h3')].filter(el => el.textContent.trim() && el.children.length === 0 && parseFloat(getComputedStyle(el).fontSize) < 12).map(el => el.textContent.trim().slice(0, 30));
      const corpo = [...document.querySelectorAll('p,li')].filter(el => el.textContent.trim().length > 40 && parseFloat(getComputedStyle(el).fontSize) < 14).length;
      return { larga, troppoLarghe, senzaAlt, link, piccoli, corpo };
    });
    if (r.larga) problemi.push(`${n}: a ${w} px scorre in orizzontale`);
    if (w === 600 && r.troppoLarghe) problemi.push(`${n}: elementi più larghi di 600 px`);
    if (w === 375) {
      if (r.senzaAlt) problemi.push(`${n}: ${r.senzaAlt} immagini senza alt`);
      if (r.link < 2) problemi.push(`${n}: servono almeno la CTA e il link per annullare l'iscrizione`);
      if (r.corpo) problemi.push(`${n}: ${r.corpo} paragrafi sotto i 14 px`);
      if (r.piccoli.length) avvisi.push(`${n}: testo sotto i 12 px → ${r.piccoli.slice(0, 3).join(' | ')}`);
    }
    await q.screenshot({ path: `${out}/email${i + 1}-${w}.png`, fullPage: true });
    await q.close();
  }
}

for (const w of [390, 1280]) {
  const q = await browser.newPage({ viewport: { width: w, height: 844 } });
  await q.goto(url, { waitUntil: 'networkidle' });
  await q.waitForTimeout(400);
  if (await q.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1)) problemi.push(`pagina: a ${w} px scorre in orizzontale`);
  await q.screenshot({ path: `${out}/pagina-${w}.png`, fullPage: true });
}
await browser.close();
const testo = (problemi.length ? 'DA SISTEMARE:\n' + problemi.join('\n') : `OK · ${emails.length} email controllate`) + (avvisi.length ? '\nAVVISI:\n' + avvisi.join('\n') : '');
writeFileSync(`${out}/esito.txt`, testo);
console.log(testo);
process.exit(problemi.length ? 2 : 0);
