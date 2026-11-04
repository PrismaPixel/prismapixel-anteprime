// PrismaPixel · banner dei cookie (vanilla-cookieconsent v3, file locale) collegato a Google Consent Mode v2.
// Tre categorie: necessari (sempre attivi), statistiche (Google Analytics), marketing (pixel e annunci).
// Rifiutare costa un clic come accettare. Il testo cita il titolare e la cookie policy del sito.
(function () {
  var POLICY = '/cookie-policy.html'; // indirizzo della cookie policy del cliente
  function aggiorna() {
    var stat = CookieConsent.acceptedCategory('statistiche');
    var mkt = CookieConsent.acceptedCategory('marketing');
    gtag('consent', 'update', {
      analytics_storage: stat ? 'granted' : 'denied',
      ad_storage: mkt ? 'granted' : 'denied',
      ad_user_data: mkt ? 'granted' : 'denied',
      ad_personalization: mkt ? 'granted' : 'denied'
    });
    window.dataLayer.push({ event: 'consenso_aggiornato', consenso_statistiche: stat, consenso_marketing: mkt });
  }
  CookieConsent.run({
    guiOptions: { consentModal: { layout: 'box', position: 'bottom left', equalWeightButtons: true },
                  preferencesModal: { layout: 'box', equalWeightButtons: true } },
    categories: { necessari: { enabled: true, readOnly: true }, statistiche: {}, marketing: {} },
    onConsent: aggiorna, onChange: aggiorna,
    language: { default: 'it', translations: { it: {
      consentModal: {
        title: 'Usiamo i cookie',
        description: 'Usiamo cookie tecnici per far funzionare il sito e, solo se accetti, cookie per misurare le visite e per la pubblicità. Puoi cambiare idea quando vuoi da «Preferenze cookie» in fondo alla pagina. <a href="' + POLICY + '">Cookie policy</a>',
        acceptAllBtn: 'Accetta tutti', acceptNecessaryBtn: 'Rifiuta', showPreferencesBtn: 'Scegli'
      },
      preferencesModal: {
        title: 'Preferenze cookie', acceptAllBtn: 'Accetta tutti', acceptNecessaryBtn: 'Rifiuta tutti',
        savePreferencesBtn: 'Salva le scelte', closeIconLabel: 'Chiudi',
        sections: [
          { title: 'Necessari', description: 'Servono a far funzionare il sito e a ricordare le tue scelte. Non si possono disattivare.', linkedCategory: 'necessari' },
          { title: 'Statistiche', description: 'Ci dicono in forma aggregata quante persone visitano il sito e cosa cercano (Google Analytics).', linkedCategory: 'statistiche' },
          { title: 'Marketing', description: 'Servono a misurare gli annunci e a mostrarli alle persone giuste (per esempio Meta e Google Ads).', linkedCategory: 'marketing' },
          { title: 'Più informazioni', description: 'Leggi la <a href="' + POLICY + '">cookie policy</a>.' }
        ]
      }
    } } }
  });
})();
