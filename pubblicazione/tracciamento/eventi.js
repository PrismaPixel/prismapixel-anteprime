// PrismaPixel · eventi per GTM (dataLayer). Nomi standard di GA4 dove esistono.
// I dati personali (email, telefono, testo dei moduli) non vanno mai nel dataLayer.
(function () {
  function invia(evento, extra) { window.dataLayer = window.dataLayer || []; window.dataLayer.push(Object.assign({ event: evento }, extra || {})); }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a, button');
    if (!a) return;
    var h = a.getAttribute('href') || '';
    if (/^tel:/i.test(h)) invia('click_telefono', { posizione: a.dataset.posizione || '' });
    else if (/wa\.me|api\.whatsapp\.com/i.test(h)) invia('click_whatsapp', { posizione: a.dataset.posizione || '' });
    else if (/^mailto:/i.test(h)) invia('click_email', { posizione: a.dataset.posizione || '' });
    if (a.dataset.evento) invia(a.dataset.evento, { voce: a.dataset.voce || '', valore: Number(a.dataset.valore || 0) || undefined, valuta: a.dataset.valore ? 'EUR' : undefined });
  }, true);
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f || f.tagName !== 'FORM' || f.hasAttribute('data-no-evento')) return;
    var modulo = f.id || f.getAttribute('name') || 'modulo';
    // Stesso identificativo per il Pixel (browser) e la Conversions API (moduli.js → server): Meta conta l'evento una volta sola
    var id = 'pp-' + Date.now() + '-' + Math.random().toString(36).slice(2, 10);
    f.dataset.eventId = id;
    invia(f.dataset.evento || 'generate_lead', { modulo: modulo, event_id: id });
    // Le richieste di prenotazione contano anche come prenotazione (Pixel di Meta: Schedule)
    if ((f.dataset.modulo || '') === 'prenotazione') invia('prenotazione', { modulo: modulo, event_id: id + '-s' });
  }, true);

  // Codice di prova di Meta (Gestione eventi → Test eventi): apri il sito con ?pp_test=TEST12345
  try {
    var t = new URLSearchParams(location.search).get('pp_test');
    if (t && /^TEST[0-9]{3,10}$/.test(t)) sessionStorage.setItem('pp_test', t);
  } catch (e) { /* niente */ }

  // Acquisto confermato (pagina di conferma dell'ordine):
  // <div data-acquisto data-ordine="1234" data-valore="89.90" data-valuta="EUR" data-email="…" hidden></div>
  // Evento "purchase" per GA4 e Pixel (event_id pp-ord-<ordine>) e, solo con il consenso marketing, lo stesso
  // acquisto alla Conversions API dal server (funzione Supabase "acquisto"). Email e telefono non vanno nel dataLayer.
  var URL_ACQUISTO = 'https://oshnvlkwuclxbbjdaupt.supabase.co/functions/v1/acquisto';
  function biscotto(nome) { var m = document.cookie.match(new RegExp('(?:^|; )' + nome + '=([^;]*)')); return m ? decodeURIComponent(m[1]) : ''; }
  function marketing() { try { return !!(window.CookieConsent && CookieConsent.acceptedCategory('marketing')); } catch (e) { return false; } }
  function acquisto() {
    var el = document.querySelector('[data-acquisto]');
    if (!el) return;
    var ordine = String(el.dataset.ordine || '').replace(/[^A-Za-z0-9_-]/g, '').slice(0, 60);
    var valore = Number(String(el.dataset.valore || '').replace(',', '.'));
    if (!ordine || !(valore > 0)) return;
    var valuta = (el.dataset.valuta || 'EUR').toUpperCase();
    var chiave = 'pp_ordine_' + ordine;
    try { if (!sessionStorage.getItem(chiave + '_dl')) { sessionStorage.setItem(chiave + '_dl', '1'); invia('purchase', { event_id: 'pp-ord-' + ordine, valore: valore, valuta: valuta, transaction_id: ordine }); } }
    catch (e) { invia('purchase', { event_id: 'pp-ord-' + ordine, valore: valore, valuta: valuta, transaction_id: ordine }); }
    function server() {
      if (!marketing()) return;
      try { if (sessionStorage.getItem(chiave + '_capi')) return; sessionStorage.setItem(chiave + '_capi', '1'); } catch (e) { /* niente */ }
      var clid = new URLSearchParams(location.search).get('fbclid');
      var test = ''; try { test = sessionStorage.getItem('pp_test') || ''; } catch (e) { test = ''; }
      fetch(URL_ACQUISTO, { method: 'POST', headers: { 'Content-Type': 'application/json' }, keepalive: true,
        body: JSON.stringify({ consenso_marketing: true, ordine: ordine, valore: valore, valuta: valuta, url: location.href,
          email: el.dataset.email || '', telefono: el.dataset.telefono || '', fbp: biscotto('_fbp'),
          fbc: biscotto('_fbc') || (clid ? 'fb.1.' + Date.now() + '.' + clid : ''), test_code: test }) }).catch(function () {});
    }
    server();
    window.addEventListener('cc:onConsent', server);
    window.addEventListener('cc:onChange', server);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', acquisto); else acquisto();
})();
