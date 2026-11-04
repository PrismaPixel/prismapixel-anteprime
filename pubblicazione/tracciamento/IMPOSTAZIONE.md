# Tracciamento, banner e Search Console · cosa si imposta

Serve all'agente di pubblicazione per scrivere la sezione "Misure" della scheda di Vincenzo, e a Vincenzo per farla.

**Di chi sono gli account.** GA4, GTM e il server di misura stanno negli **account di PrismaPixel**: una proprietà GA4
e un contenitore GTM per ogni sito, creati in automatico. Search Console resta del cliente (verifica sul suo dominio),
con PrismaPixel come utente. Il cliente resta **titolare** dei dati; PrismaPixel è **responsabile del trattamento**
(termini di servizio). Se il cliente se ne va: la proprietà GA4 si sposta nel suo account GA (Amministrazione →
Proprietà → Sposta proprietà), il contenitore GTM si esporta e si importa nel suo account, e il server di misura si
ricrea nel suo progetto Google Cloud. Mai password o token nei file o nella scheda.

## 1. Lato client (sempre, per ogni sito con tracciamento)

**Creazione automatica.** Il workflow n8n **"PrismaPixel · Crea tracciamento"** (`workflowId: "le5mfdOrvT4weNLD"`,
`executionMode: "production"`, `triggerNodeName: "Richiesta tracciamento"`, body `{"job_id": "<job della
pubblicazione>"}`) crea in un colpo solo, negli account di PrismaPixel: proprietà GA4, flusso web, conservazione 14
mesi ed eventi chiave; contenitore GTM con Tag Google, attivatori ed eventi GA4; lo pubblica e registra `gtm` e `ga4`
negli accessi del cliente. Risponde con `gtm`, `ga4`, `misurazione`, `pubblicato` ed `errori`. Se GTM e GA4 ci sono
già non crea niente. Dopo, nella scheda resta solo da collegare Search Console a GA4 e da provare con l'Anteprima.

**GA4**
- Proprietà nell'account di PrismaPixel (fuso Europe/Rome, valuta EUR), un flusso web per il dominio. Conservazione: 14 mesi.
- Eventi chiave: `generate_lead`; più `click_whatsapp` e `click_telefono` se il sito vende per contatto;
  `begin_checkout` e `purchase` per e-commerce e prenotazioni.
- Collegamenti: Search Console; Google Ads se ci sono annunci.
- In accessi: fonte `ga4`, riferimento = ID della proprietà (numeri).

**GTM web** (un contenitore per sito nell'account GTM di PrismaPixel, in accessi fonte `gtm`, riferimento `GTM-XXXXXXX`)
- Il sito ha già: consenso negato all'avvio (Consent Mode v2), banner, eventi nel dataLayer (`pubblicazione/tracciamento/`).
- Nel contenitore:
  1. **Tag Google** (Google tag) con l'ID di misurazione GA4 (`G-…`), attivazione "Initialization - All Pages".
     Se c'è il lato server: parametro `server_container_url` = `https://misure.<dominio>`.
  2. **Eventi GA4**, uno per evento del dataLayer: `generate_lead`, `click_whatsapp`, `click_telefono`,
     `click_email`, `begin_checkout`, `purchase` (attivatore: evento personalizzato con lo stesso nome).
  3. Pixel di Meta e tag di Google Ads **solo se ci sono annunci**, con controllo del consenso `ad_storage`.
  4. Impostazioni del contenitore → **Panoramica del consenso** attiva; i tag Google usano il consenso integrato,
     gli altri richiedono `ad_storage` o `analytics_storage`.
- Prova con **Anteprima** (Tag Assistant): senza consenso nessun cookie `_ga`; dopo "Accetta tutti" gli eventi arrivano
  in GA4 → Rapporti in tempo reale.

## 2. Lato server (solo per clienti con annunci attivi o e-commerce)

- **Perché**: le conversioni arrivano ad annunci e GA4 anche con blocchi del browser e cookie brevi di Safari; i dati
  passano da un dominio del cliente (`misure.<dominio>`).
- **Costo**: Google Cloud Run a consumo, da pochi euro a circa 100-120 €/mese con le istanze sempre accese consigliate
  da Google per i siti con tanto traffico. Lo paga PrismaPixel e lo **riaddebita** al cliente nel canone (va detto
  prima). Un servizio Cloud Run per cliente, con l'etichetta `cliente=<slug>`, così i costi si leggono per cliente.
- **Passi**:
  1. Progetto Google Cloud **di PrismaPixel** (uno per tutti i server di misura), con la fatturazione di PrismaPixel.
  2. GTM → nuovo contenitore **Server** → "Effettua il provisioning automatico del server di tagging" (crea il servizio
     su Cloud Run nel progetto del cliente). Regione: `europe-west1` (o la più vicina in UE).
  3. Dominio: su Cloud Run → **Gestisci domini personalizzati** → `misure.<dominio>`; il record DNS che Google indica
     (di solito CNAME verso `ghs.googlehosted.com`) va su Cloudflare **senza proxy (nuvola grigia)**.
  4. Nel contenitore server: client GA4 (già presente) e tag GA4; per Meta il tag Conversions API dalla galleria dei
     modelli, con il token di Meta salvato **solo dentro GTM server**.
  5. Nel contenitore web: `server_container_url` nel Tag Google (sezione 1).
  6. Prova: in GTM server → Anteprima, gli eventi del sito arrivano dal dominio `misure.`.
- In accessi: fonte `gtm_server`, riferimento = `https://misure.<dominio>`.

## 3. Banner dei cookie

- Libreria open source **vanilla-cookieconsent 3.1.0**, servita dal sito stesso (file `cookieconsent.umd.js` e `cookieconsent.css` nella cartella principale), configurata in
  `consenso.js`: rifiuta e accetta con lo stesso peso, tre categorie, pulsante "Preferenze cookie" nel piè di pagina.
- Non è una CMP certificata da Google: per Consent Mode va bene; se il cliente fa annunci Google con pubblico nello
  Spazio economico europeo e Google chiede una CMP certificata, si passa a una CMP certificata (Iubenda, Cookiebot) a
  carico del cliente.
- La **cookie policy** del cliente deve elencare GA4 (e Meta/Google Ads se presenti) e il server di misura: è un
  bloccante della scheda se manca.

## 4. Search Console e reindirizzamenti su Cloudflare

- Proprietà **di dominio** (`<dominio>`, tutte le varianti), verificata con record **TXT** su Cloudflare.
  Il cliente è proprietario; PrismaPixel utente con accesso completo. In accessi: fonte `search_console`.
- Subito dopo il lancio: invia `sitemap.xml`; collega GA4.
- **Reindirizzamenti**:
  - stesso dominio (restyling): bastano le regole `_redirects` del sito su Cloudflare Pages;
  - **dominio che cambia** (vecchio → nuovo): sul dominio vecchio, in Cloudflare, una **Redirect Rule** (o Bulk
    Redirects se le regole sono tante) che porta ogni indirizzo vecchio al nuovo con 301 mantenendo il percorso; poi in
    Search Console, sulla proprietà vecchia, **Cambio di indirizzo** verso la nuova. Il dominio vecchio resta attivo
    almeno 12 mesi.
  - dopo 2-7 giorni (livello `verifica`): pagine con errore 404 e "Pagina con reindirizzamento" nel rapporto
    Indicizzazione → nuove righe in `_redirects`.

## 5. Modificare i siti con Replit

Ogni sito pubblicato ha anche un **progetto Replit** con gli stessi file: lì Vincenzo (o l'Agente di Replit) fa le
modifiche, e il progetto **pubblica su Cloudflare Pages** con un comando. Cloudflare resta l'hosting (DNS,
reindirizzamenti, HTTPS); Replit è l'officina.
- Una volta sola su Replit: nei **Secrets dell'account** `CLOUDFLARE_API_TOKEN` (token Cloudflare con permesso
  "Cloudflare Pages: Edit" sull'account di PrismaPixel) e `CLOUDFLARE_ACCOUNT_ID`.
- Nel progetto: cartella `site/` con il sito, `package.json` con `wrangler` a versione fissa e lo script
  `"pubblica": "wrangler pages deploy site --project-name <slug> --branch main"`, una pagina README breve.
- Per pubblicare una modifica: nel progetto, Shell → `npm run pubblica`. La versione precedente resta su Cloudflare
  (Deployments) e si ripristina con un clic.
