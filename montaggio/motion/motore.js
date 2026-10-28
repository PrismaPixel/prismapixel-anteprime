/* PrismaPixel · motore delle grafiche verticali (1080 × 1920)
 *
 * Ogni elemento animato dichiara i suoi tempi in SECONDI sul video montato:
 *   data-in="3.2"            quando entra (sulla parola che lo nomina, o un attimo prima)
 *   data-out="7.0"           quando esce (facoltativo: senza, resta fino all'uscita del gruppo)
 *   data-anim="sale"         come entra: sale | pop | maschera | scrivi | conta | disegna | cresce (data-asse x | y | giu) | evidenzia | lettere | scorri | appare
 *   data-dur="0.45"          durata dell'entrata (default 0.45 s)
 * Un gruppo (.grafica) ha data-in e data-out e data-box="x,y,w,h" (pixel del palco): il motore lo posiziona e lo
 * scala per stare nel riquadro. I figli senza data-in entrano con il gruppo.
 *
 * Il tempo non scorre da solo: window.seek(t) mette ogni elemento nello stato esatto del secondo t. Così il rendering
 * fotogramma per fotogramma è identico ogni volta (nessuna animazione CSS, nessun fotogramma perso).
 * window.riquadri(t) restituisce i riquadri dei testi visibili (per i controlli: niente testo sul corpo, niente testo
 * fuori dall'area utile). window.anteprima() fa partire il tempo vero, solo per guardare la pagina nel browser.
 */
(function () {
  const USCITA = 0.3; // dissolvenza d'uscita (s)
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const ease = {
    out: p => 1 - Math.pow(1 - p, 3),
    back: p => { const c = 1.6; return 1 + (c + 1) * Math.pow(p - 1, 3) + c * Math.pow(p - 1, 2); },
    inout: p => (p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2),
  };
  const num = (el, k, d) => { const v = parseFloat(el.dataset[k]); return Number.isFinite(v) ? v : d; };
  const gruppoDi = el => el.closest('.grafica');

  function prepara() {
    // posiziona e scala i gruppi nel loro riquadro
    document.querySelectorAll('.grafica').forEach(g => {
      const box = String(g.dataset.box || '').split(',').map(Number);
      if (box.length === 4 && box.every(Number.isFinite)) {
        const [x, y, w, h] = box;
        g.style.position = 'absolute'; g.style.left = x + 'px'; g.style.top = y + 'px'; g.style.width = w + 'px';
        g.style.transformOrigin = 'top left';
        const base = num(g, 'larghezza', 900); // larghezza di disegno del componente
        const sc = w / base; g.style.width = base + 'px'; g.style.setProperty('--scala', sc);
        g.style.transform = `scale(${sc})`;
        // se dopo la scala il componente è più alto del riquadro, riduce ancora
        const altezza = g.scrollHeight * sc;
        if (altezza > h) { const s2 = sc * h / altezza; g.style.transform = `scale(${s2})`; g.style.setProperty('--scala', s2); }
      }
    });
    // testo da scrivere lettera per lettera: lo spezza una volta sola
    document.querySelectorAll('[data-anim="scrivi"],[data-anim="lettere"]').forEach(el => {
      if (el.dataset.pronto) return; el.dataset.pronto = 1;
      const t = el.textContent; el.textContent = '';
      // lettere dentro parole che non si spezzano a fine riga
      t.split(/(\s+)/).forEach(pz => {
        if (!pz) return;
        if (/^\s+$/.test(pz)) { el.appendChild(document.createTextNode(' ')); return; }
        const w = document.createElement('span'); w.style.whiteSpace = 'nowrap'; w.style.display = 'inline-block';
        [...pz].forEach(c => { const s = document.createElement('span'); s.className = 'lt'; s.textContent = c; w.appendChild(s); });
        el.appendChild(w);
      });
    });
    document.querySelectorAll('[data-anim="disegna"]').forEach(el => {
      el.querySelectorAll('path,line,polyline,circle,rect').forEach(p => {
        try { const L = p.getTotalLength(); p.style.strokeDasharray = L; p.dataset.l = L; } catch (_) {}
      });
    });
    document.querySelectorAll('[data-anim="conta"]').forEach(el => { if (!el.dataset.a) el.dataset.a = el.textContent.replace(/[^\d.,-]/g, ''); });
  }

  const formatta = (v, el) => {
    const dec = num(el, 'decimali', 0);
    const s = v.toLocaleString('it-IT', { minimumFractionDigits: dec, maximumFractionDigits: dec });
    return (el.dataset.prima || '') + s + (el.dataset.dopo || '');
  };

  function stato(el, t) {
    const g = gruppoDi(el);
    const tin = num(el, 'in', g ? num(g, 'in', 0) : 0);
    const tout = num(el, 'out', g && g !== el ? num(g, 'out', 1e9) : 1e9);
    const dur = num(el, 'dur', el.classList.contains('grafica') ? 0.35 : 0.45);
    const p = clamp((t - tin) / dur, 0, 1);
    const q = clamp((tout - t) / USCITA, 0, 1); // 1 = visibile, 0 = uscito
    return { tin, tout, p, q, visibile: t >= tin && t < tout };
  }

  function applica(el, t) {
    const { p, q, visibile, tin } = stato(el, t);
    const anim = el.dataset.anim || (el.classList.contains('grafica') ? 'appare' : 'sale');
    el.style.visibility = visibile ? 'visible' : 'hidden';
    if (!visibile) return;
    const e = ease.out(p);
    let op = Math.min(e, q), tr = '';
    switch (anim) {
      case 'appare': op = Math.min(p, q); break;
      case 'sale': tr = `translateY(${(1 - e) * 40}px)`; break;
      case 'pop': tr = `scale(${0.6 + 0.4 * ease.back(p)})`; op = Math.min(clamp(p * 3, 0, 1), q); break;
      case 'maschera': el.style.clipPath = `inset(0 0 ${(1 - ease.inout(p)) * 100}% 0)`; tr = `translateY(${(1 - e) * 30}px)`; op = q; break;
      case 'scrivi': case 'lettere': {
        const lt = el.querySelectorAll('.lt'); const n = lt.length;
        const quante = Math.ceil(n * p);
        lt.forEach((s, i) => {
          if (anim === 'scrivi') s.style.opacity = i < quante ? 1 : 0;
          else { const pi = clamp(p * n * 0.5 - i * 0.5 + 0.5, 0, 1); s.style.opacity = pi; s.style.display = 'inline-block'; s.style.transform = `translateY(${(1 - ease.out(pi)) * 30}px)`; }
        });
        op = q; break;
      }
      case 'conta': {
        const da = num(el, 'da', 0), a = parseFloat(String(el.dataset.a).replace(/\./g, '').replace(',', '.'));
        el.textContent = formatta(da + (a - da) * ease.out(clamp((t - tin) / num(el, 'dur', 1.2), 0, 1)), el);
        op = Math.min(clamp(p * 4, 0, 1), q); break;
      }
      case 'disegna': {
        const pd = ease.inout(clamp((t - tin) / num(el, 'dur', 0.9), 0, 1));
        el.querySelectorAll('[data-l]').forEach(s => { s.style.strokeDashoffset = s.dataset.l * (1 - pd); });
        op = q; break;
      }
      case 'cresce': {
        const asse = el.dataset.asse || 'y';
        el.style.transformOrigin = asse === 'y' ? 'bottom' : asse === 'giu' ? 'top' : 'left';
        tr = asse === 'x' ? `scaleX(${e})` : `scaleY(${e})`; op = q; break;
      }
      case 'evidenzia': el.style.backgroundSize = `${e * 100}% 100%`; op = q; break;
      case 'scorri': tr = `translateX(${(1 - e) * -60}px)`; break;
    }
    el.style.opacity = op;
    if (el.classList.contains('grafica')) { const sc = el.style.getPropertyValue('--scala'); el.style.transform = (sc ? `scale(${sc}) ` : '') + tr; }
    else el.style.transform = tr;
  }

  window.seek = function (t) {
    document.querySelectorAll('.grafica').forEach(g => applica(g, t));
    document.querySelectorAll('.grafica [data-in], .grafica [data-anim]').forEach(el => applica(el, t));
  };

  // tempi dei gruppi: per il rendering (salta i fotogrammi vuoti) e per i controlli
  window.tempi = () => [...document.querySelectorAll('.grafica')].map(g => ({
    id: g.id || '', tipo: g.dataset.tipo || '', in: num(g, 'in', 0), out: num(g, 'out', 0),
    parole: (g.innerText || '').trim().split(/\s+/).filter(Boolean).length,
  }));

  // riquadri dei testi visibili al secondo t (coordinate del palco)
  window.riquadri = function (t) {
    window.seek(t);
    const out = [];
    document.querySelectorAll('.grafica').forEach(g => {
      if (getComputedStyle(g).visibility === 'hidden' || parseFloat(g.style.opacity || 1) < 0.05) return;
      const r = g.getBoundingClientRect();
      out.push({ id: g.id || '', tipo: g.dataset.tipo || '', x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) });
    });
    return out;
  };

  window.anteprima = function (velocita = 1) {
    const t0 = performance.now();
    const fine = Math.max(1, ...window.tempi().map(x => x.out)) + 1;
    const giro = () => { window.seek(((performance.now() - t0) / 1000 * velocita) % fine); requestAnimationFrame(giro); };
    requestAnimationFrame(giro);
  };

  window.palcoPronto = (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => { prepara(); window.seek(0); return true; });
})();
