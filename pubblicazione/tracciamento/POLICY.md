# Privacy e cookie policy dei siti dei clienti: blocchi per gli strumenti che installiamo

Testi pronti, da adattare con i dati del cliente, per dire nelle sue pagine **quali strumenti usa il sito**. Non sono
una consulenza legale: il titolare è il cliente e il testo finale lo approva lui (o il suo consulente privacy).
Non si inventano dati: titolare, indirizzo, email e P.IVA vengono solo dal brief.

## 1. Quando usarli

- **Il sito ha pagine `privacy` e `cookie` fatte da noi** (il caso normale per i siti PrismaPixel): inserisci o aggiorna
  i blocchi della sezione 3 per **ogni strumento attivo sul sito**, e solo per quelli. Aggiorna la data in testa
  ("Ultimo aggiornamento: …"). Togli i blocchi degli strumenti che non ci sono più.
- **Il cliente ha già una policy sua** (iubenda, Cookiebot, consulente, gestionale): non toccarla. Metti nella scheda
  per Vincenzo il testo da aggiungere (sezione 3, solo gli strumenti nuovi) con la nota "da passare a chi gestisce la
  policy del cliente". Se è iubenda: elenco dei servizi da aggiungere con i nomi che iubenda usa ("Meta Pixel",
  "Conversions API di Meta", "Google Analytics 4", "Google Tag Manager").
- **Senza titolare nel brief** (nome o ragione sociale, indirizzo, email): bloccante "dati del titolare per la privacy
  da chiedere al cliente", con segnaposto chiaro.

## 2. Come capire quali strumenti ci sono

Dagli accessi del cliente e dal sito:
- `gtm` e `ga4` negli accessi → blocchi **Google Tag Manager** e **Google Analytics 4**;
- `meta_pixel` con nota "installato in GTM" → **Meta Pixel**;
- Pixel installato **e** sito con `moduli.js` → anche **Conversions API di Meta** (non per il settore sanitario: lì il
  server non manda niente, quindi niente blocco);
- `gtm_server` → **server di misura**;
- moduli del sito → **Resend** e **Supabase**; dominio su Cloudflare → **Cloudflare**;
- mappe o video incorporati → il blocco del fornitore (Google Maps, YouTube in modalità privacy avanzata) solo se
  presenti.

## 3. Blocchi

### Cookie policy · tabella (una riga per cookie, solo se lo strumento c'è)

| Cookie | Fornitore | Categoria | Durata | A cosa serve |
|---|---|---|---|---|
| `cc_cookie` | questo sito | tecnico | 6 mesi | ricorda le scelte fatte nel banner dei cookie |
| `_ga`, `_ga_<ID>` | Google Ireland (Google Analytics 4) | statistiche | 14 mesi | conta visite e pagine viste in forma aggregata |
| `_fbp` | Meta Platforms Ireland (Meta Pixel) | marketing | 90 giorni | misura le visite e le azioni sul sito dopo un annuncio su Facebook o Instagram |
| `_fbc` | Meta Platforms Ireland (Meta Pixel) | marketing | 90 giorni | ricorda che sei arrivato da un annuncio Meta |

Sotto la tabella: "I cookie di statistiche e marketing si attivano solo dopo il tuo consenso nel banner e puoi
cambiare idea in ogni momento dal link «Preferenze cookie» in fondo alla pagina."

### Privacy policy · Meta Pixel

> **Meta Pixel (Meta Platforms Ireland Ltd.).** Se accetti i cookie di marketing, il sito usa il Pixel di Meta per
> misurare quante visite, contatti e prenotazioni arrivano dalle inserzioni su Facebook e Instagram e per mostrare
> annunci a chi ha già visitato il sito. Dati trattati: identificativi dei cookie, indirizzo IP, browser, pagine viste e
> azioni sul sito (per esempio l'invio di un modulo, senza il suo contenuto). Base giuridica: consenso (art. 6.1.a
> GDPR), revocabile in ogni momento. Meta può trasferire i dati negli Stati Uniti sulla base del Data Privacy Framework
> UE-USA. Per i dati raccolti con il Pixel [ragione sociale del cliente] e Meta sono contitolari per la raccolta e la
> trasmissione: [link alle condizioni per i titolari del trattamento di Meta,
> https://www.facebook.com/legal/controller_addendum].

### Privacy policy · Conversions API di Meta

> **Conversions API di Meta.** Se hai accettato i cookie di marketing e invii un modulo del sito, comunichiamo a Meta
> anche dal nostro server che è avvenuto un contatto (o una richiesta di prenotazione), così il dato arriva anche se il
> browser blocca il Pixel. Inviamo: tipo di azione, pagina, indirizzo IP, browser, identificativi dei cookie di Meta e,
> se li hai scritti nel modulo, email e telefono in forma codificata (hash SHA-256, non leggibili). **Il contenuto del
> messaggio non viene mai condiviso.** Base giuridica: consenso; i dati restano sui nostri sistemi al massimo 30 giorni.
> Senza consenso non inviamo nulla.

### Privacy policy · Google Analytics 4 e Tag Manager

> **Google Analytics 4 e Google Tag Manager (Google Ireland Ltd.).** Se accetti i cookie di statistiche, misuriamo in
> forma aggregata le visite e l'uso delle pagine. Google Tag Manager serve solo a caricare gli strumenti che hai
> accettato. Base giuridica: consenso. I dati sono conservati 14 mesi; Google può trasferirli negli Stati Uniti sulla
> base del Data Privacy Framework UE-USA.

### Privacy policy · moduli e infrastruttura

> **Moduli di contatto.** I messaggi che invii arrivano via email a [email del cliente] tramite Resend (invio
> dei messaggi); Supabase tiene un registro anti-spam senza il contenuto dei messaggi; il sito è servito da
> Cloudflare. Base giuridica: rispondere alla tua richiesta (art. 6.1.b GDPR).

### Privacy policy · server di misura (solo con `gtm_server`)

> **Server di misura.** Le misurazioni passano da un nostro server in Europa (`misure.[dominio]`, Google Cloud,
> regione UE), che toglie i dati non necessari prima di inoltrarle a Google e Meta. Valgono le stesse scelte del
> banner dei cookie.

## 4. Controlli

- Ogni strumento attivo ha il suo blocco; nessun blocco per strumenti assenti.
- Il link "Preferenze cookie" nel piè di pagina riapre il banner.
- In `consenso.js` l'indirizzo della cookie policy è quello vero.
- Data di aggiornamento cambiata. Nella scheda: "policy aggiornata con: …" e "da far approvare al cliente".
