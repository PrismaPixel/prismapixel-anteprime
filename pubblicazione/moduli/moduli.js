/* PrismaPixel · invio dei moduli del sito.
   Ogni <form data-modulo="contatto"> viene mandato alla funzione Supabase «modulo», che lo inoltra via Resend
   all'indirizzo aziendale del cliente (verificato da PrismaPixel). Nessuna chiave o password nel sito.
   Nel form: un campo nascosto anti-spam <input name="_hp" tabindex="-1" autocomplete="off" hidden>,
   un elemento [data-esito] per il messaggio, e campi con name leggibili (es. "Nome", "Email", "Messaggio"). */
(function () {
  var URL_FUNZIONE = 'https://oshnvlkwuclxbbjdaupt.supabase.co/functions/v1/modulo';
  var OK = 'Grazie! Abbiamo ricevuto il tuo messaggio e ti rispondiamo al più presto.';
  var KO = 'Non siamo riusciti a inviare il messaggio. Riprova tra poco oppure contattaci per telefono.';

  function biscotto(nome) {
    var m = document.cookie.match(new RegExp('(?:^|; )' + nome + '=([^;]*)'));
    return m ? decodeURIComponent(m[1]) : '';
  }

  function esito(form, testo, ok) {
    var el = form.querySelector('[data-esito]');
    if (!el) { el = document.createElement('p'); el.setAttribute('data-esito', ''); form.appendChild(el); }
    el.textContent = testo;
    el.setAttribute('role', ok ? 'status' : 'alert');
    el.className = 'modulo-esito ' + (ok ? 'modulo-ok' : 'modulo-errore');
  }

  document.addEventListener('submit', function (ev) {
    var form = ev.target;
    if (!(form instanceof HTMLFormElement) || !form.hasAttribute('data-modulo')) return;
    ev.preventDefault();
    var bottone = form.querySelector('[type="submit"]');
    if (bottone) bottone.disabled = true;
    var campi = {}; var hp = '';
    new FormData(form).forEach(function (v, k) {
      if (k === '_hp') { hp = String(v); return; }
      if (typeof v === 'string') campi[k] = v;
    });
    // Conversions API di Meta: solo con il consenso ai cookie di marketing (banner consenso.js)
    var mkt = false;
    try { mkt = !!(window.CookieConsent && CookieConsent.acceptedCategory('marketing')); } catch (e) { mkt = false; }
    var extra = { consenso_marketing: mkt, event_id: form.dataset.eventId || '' };
    if (mkt) {
      extra.url = location.href;
      extra.fbp = biscotto('_fbp');
      extra.fbc = biscotto('_fbc');
      var clid = new URLSearchParams(location.search).get('fbclid');
      if (!extra.fbc && clid) extra.fbc = 'fb.1.' + Date.now() + '.' + clid;
    }
    fetch(URL_FUNZIONE, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.assign({ tipo: form.getAttribute('data-modulo') || 'contatto', campi: campi, _hp: hp, pagina: location.pathname }, extra))
    }).then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok && j.ok, j: j }; }); })
      .then(function (x) {
        if (x.ok) { form.reset(); esito(form, OK, true); }
        else esito(form, (x.j && x.j.motivo) ? 'Invio non riuscito: ' + x.j.motivo + '.' : KO, false);
      })
      .catch(function () { esito(form, KO, false); })
      .then(function () { if (bottone) bottone.disabled = false; });
  });
})();
