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
    if (f && f.tagName === 'FORM' && !f.hasAttribute('data-no-evento')) invia(f.dataset.evento || 'generate_lead', { modulo: f.id || f.getAttribute('name') || 'modulo' });
  }, true);
})();
