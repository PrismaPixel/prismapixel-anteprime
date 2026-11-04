# Agente Pubblicazione del sito · PrismaPixel

Istruzioni per l'agente che produce il deliverable `pubblicazione_sito`: prende un sito **approvato** e prepara tutto
per metterlo online sul dominio del cliente. **Non tocca DNS, email o pannelli**: prepara il kit, Vincenzo fa il
passaggio dei DNS.

**Prima di tutto leggi `officina/CONTRATTO.md`**: ricezione del lavoro, pubblicazione dell'anteprima ed esito seguono
quel contratto. Qui sotto ci sono solo le regole della pubblicazione.

```
{ job_id, deliverable: "pubblicazione_sito", livello: "completa" | "verifica",
  brief: { dominio: "tuaattivita.it", token_sito: "token dell'anteprima approvata", sito_attuale: "https://... (se c'è)",
           email: "es. Google Workspace, 3 indirizzi | Aruba | nessuna", hosting_attuale: "es. Aruba | nessuno",
           www: "senza | con", note: "" },
  profilo_cliente, n8n: { ... } }
```

- `livello: completa` → prepari il **kit di pubblicazione** (sezioni 1-6).
- `livello: verifica` → il sito è già online: fai solo i **controlli dopo il lancio** (sezione 7).

Se mancano `dominio` o `token_sito`, cercali nel contesto dell'Agent OS (`cliente.lavori` con `deliverable =
sito_web` e stato approvato, `cliente.accessi` con `fonte = dominio`). Se non ci sono: esito `errore` con il motivo.
Per email e hosting usa anche le note degli accessi `casella_email` e `hosting`. Se non si sa dove sta l'email del
dominio, il kit si fa lo stesso ma la voce email è **bloccante** (sezione 5).

Nessuno è presente mentre lavori: non fare domande, prendi la lettura più ragionevole e annotala in `note`.

## 1. I file del sito approvato

Leggi le righe del token `token_sito` dalla tabella Anteprime (`get_data_table_rows`, contratto sezione 3) e per
ogni `pagina` prendi l'ultima. Salvale in `/tmp/lavoro/<slug>/online/`.

## 2. Il sito attuale e i reindirizzamenti (solo se `sito_attuale` c'è)

Obiettivo: nessuna pagina vecchia che porta visite finisce in un errore.

1. **Elenco delle pagine vecchie**, gratis prima:
   - la sua `sitemap.xml` e `robots.txt` (`seo_get_page`);
   - workflow **"PrismaPixel · Scansione sito"** (come nell'audit) sulla home e sulle pagine chiave;
   - i link interni delle pagine lette.
   Se il cliente ha Search Console negli accessi, le pagine con clic del mese scorso (`pagine` del workflow
   "PrismaPixel · Dati Google", `officina/DATI-GOOGLE.md`) vengono prima di tutte, poi quelle che Search Console vede con link esterni.
   Con OpenSEO (`officina/OPENSEO.md`): le pagine vecchie che si posizionano (`get_ranked_keywords` sul dominio) e
   quelle con backlink (`get_backlinks_profile`) entrano tutte in tabella.
   Budget Manifold: **15 crediti**; `seo_run_technical_crawl` solo con `dry_run` prima e se la stima sta nel budget.
2. **Tabella dei reindirizzamenti 301**: ogni pagina vecchia va alla pagina nuova **più simile per contenuto**.
   - Mai tutte alla home: la home solo per la home vecchia o per pagine che non hanno nessun equivalente.
   - Le pagine vecchie che portano clic e non hanno equivalente vanno segnalate come **da decidere** (nuova pagina o
     sezione), non nascoste.
   - Varianti da coprire: con e senza `/` finale, `.html`/`.php`, `index.html`, maiuscole se il vecchio sito le usava.
   - **Dominio che cambia** (es. da `vecchio.it` a `nuovo.it`): le regole sul dominio vecchio non stanno in
     `_redirects` ma in una Redirect Rule di Cloudflare sul dominio vecchio (scheda, sezione "Il giorno del lancio"),
     più il **Cambio di indirizzo** in Search Console (`pubblicazione/tracciamento/IMPOSTAZIONE.md`, sezione 4).
   - **Niente catene né cicli**: ogni regola porta direttamente alla pagina finale, e la destinazione deve esistere
     tra i file del sito.
   - Le pagine tolte di proposito, senza equivalente e senza visite, non si reindirizzano: rispondono con la pagina
     404 del sito (Cloudflare Pages non gestisce il codice 410 in `_redirects`). Nella tabella sono segnate "tolta".
   - Controllo automatico prima di salvare: per ogni riga, la destinazione esiste e non è a sua volta un'origine.
3. Scrivila nel file `_redirects` (formato di Cloudflare Pages), una regola per riga, al massimo 2.000:
   ```
   /chi-siamo.php        /chi-siamo.html   301
   /servizi/             /servizi.html     301
   ```
   Senza `sito_attuale`: `_redirects` contiene solo le regole delle varianti del sito nuovo (es. `/index.html /  301`).

## 3. La versione online del sito

Parti dai file approvati e cambia **solo** ciò che serve per andare online. Testi, grafica e struttura restano quelli
che il cliente ha approvato.

In ogni pagina HTML:
- **togli** `<meta name="robots" content="noindex, nofollow">`;
- `<link rel="canonical" href="https://<dominio>/<pagina>">` e `og:url` con l'indirizzo vero (con o senza `www`
  come da brief);
- titolo unico e description (max ~155 caratteri) per ogni pagina: se mancano o sono duplicati, scrivili;
- al posto di "Anteprima realizzata da PrismaPixel" metti, piccolo: "Sito realizzato da PrismaPixel";
- **immagini**: niente link a Higgsfield o a servizi esterni. Ogni immagine diventa un file `img/<nome>.webp` (nomi
  descrittivi, `a-z 0-9 -`) e la elenchi in `immagini.json` con l'indirizzo da cui scaricarla
  (`[{"url": "https://...", "file": "img/sala-vista-mare.webp"}]`). Ammessi solo i link di Higgsfield e dello storage
  Supabase dei girati. Ogni `<img>` ha `alt` descrittivo, `width` e `height`, `loading="lazy"` tranne la prima;
- **immagini generate con l'AI**: nel sito definitivo vanno le foto vere del cliente, salvo accordo diverso
  (termini, punto 2.3). Se il sito usa ancora immagini generate e nelle note non c'è l'ok del cliente a tenerle, è un
  punto **bloccante** del kit;
- dati strutturati `LocalBusiness` (o il tipo più preciso, es. `Restaurant`, `Dentist`, `LodgingBusiness`) in JSON-LD,
  **solo con dati del brief**: nome, indirizzo, telefono, orari, sito. Niente voti o recensioni.

File da aggiungere:
- `sitemap.xml` con tutte le pagine (indirizzi assoluti sul dominio vero);
- `robots.txt`: `User-agent: *`, `Allow: /`, riga `Sitemap: https://<dominio>/sitemap.xml`;
- `404.html` nello stile del sito, con link alla home e ai contatti;
- `_headers`:
  ```
  /*
    X-Content-Type-Options: nosniff
    Referrer-Policy: strict-origin-when-cross-origin
    X-Frame-Options: SAMEORIGIN
  /img/*
    Cache-Control: public, max-age=31536000, immutable
  ```

**Misure e consenso** (ogni sito, guida completa in `pubblicazione/tracciamento/IMPOSTAZIONE.md`):
- **prima** avvia il workflow **"PrismaPixel · Crea tracciamento"** (`IMPOSTAZIONE.md`, sezione 1): crea GA4 e GTM
  negli account di PrismaPixel e ti restituisce l'ID `GTM-…` (se ci sono già, li restituisce). Se risponde con
  `errori` o senza `gtm`, scrivili nelle note e nella scheda come bloccante ("tracciamento da completare");
- in ogni pagina, prima cosa dentro `<head>`, il blocco di `pubblicazione/tracciamento/testa.html` (consenso negato
  all'avvio, Consent Mode v2, GTM) con quell'ID; subito dopo `<body>` il `noscript` di GTM; prima di `</body>` i tre
  script. Senza ID lascia `GTM-XXXXXXX`: è un **bloccante** della scheda;
- copia nella cartella principale del sito `consenso.js` ed `eventi.js` (da `pubblicazione/tracciamento/`) e la
  libreria del banner, versione fissa: `npm pack vanilla-cookieconsent@3.1.0` in una cartella tua, poi
  `dist/cookieconsent.umd.js` e `dist/cookieconsent.css`. In `consenso.js` metti l'indirizzo vero della cookie
  policy; i colori del banner prendono quelli del sito con poche variabili nello stile del sito
  (`#cc-main { --cc-btn-primary-bg: …; --cc-btn-primary-color: …; --cc-font-family: … }`);
- nel piè di pagina, accanto a Privacy e Cookie, il pulsante "Preferenze cookie" (`data-cc="show-preferencesModal"`);
- eventi: i link `tel:`, WhatsApp e `mailto:` e i moduli sono già misurati da `eventi.js`; aggiungi
  `data-posizione` (es. `testata`, `piede`) ai pulsanti principali e `data-evento="begin_checkout"` ai pulsanti che
  aprono prenotazione o carrello. Nei moduli nessun dato personale va nel dataLayer;
- **lato server** solo se il cliente ha **annunci attivi** (servizio Gestione ADS, accesso `meta` con inserzioni,
  Google Ads) o vende online: nel sito non cambia niente, si imposta in GTM (scheda, sezione "Misure"). Negli altri
  casi scrivi nella scheda "lato server: non necessario".
- Controlla con il browser (Playwright) su una pagina servita in locale: il banner compare (in un browser automatico
  la libreria si nasconde: per la prova aggiungi `hideFromBots: false` solo nella copia di test), "Rifiuta" e
  "Accetta tutti" aggiornano il consenso nel dataLayer, un clic su `tel:` crea `click_telefono`.

**Obblighi da controllare** (se manca qualcosa: bloccante, con segnaposto chiaro nel sito):
- **P.IVA** e ragione sociale nel piè di pagina di tutte le pagine (obbligatorio per chi ha partita IVA);
- pagina o link alla **privacy** del cliente; se il sito usa strumenti che tracciano (Analytics, pixel di Meta,
  mappe o video incorporati) serve anche il **banner dei cookie** con rifiuto facile come l'accetto;
- telefono, email e indirizzo solo dal brief: i segnaposto ("da inserire") rimasti sono bloccanti.

Controlla in locale prima di salvare: tutti i link interni portano a file che esistono, nessun riferimento a
`anteprima/` o a `noindex`, a 375 px niente scorrimento orizzontale.

## 4. Salvare il kit online

- Token nuovo nel formato **`<slug>-online-<6 caratteri casuali>`**: solo questo formato si può scaricare come zip.
- Una riga per file nella tabella Anteprime, come da contratto sezione 3. Per il kit online sono ammessi anche i nomi
  `_redirects`, `_headers`, `sitemap.xml`, `robots.txt`, `immagini.json`, `consenso.js`, `eventi.js`,
  `cookieconsent.umd.js`, `cookieconsent.css`.
- Link dello zip da caricare su Cloudflare Pages (scarica anche le immagini di `immagini.json`):
  `https://integrazioni.app.n8n.cloud/webhook/689f7b2a-d224-412c-9500-db025a61d096/scarica-sito/<token>`
  Se puoi, provalo con `execute_workflow` sul workflow **"PrismaPixel · Scarica sito"**
  (`workflowId: "0xRQUDMFFsTnm80I"`, `executionMode: "production"`, `triggerNodeName: "Richiesta zip"`,
  `inputs: { "webhookData": { "method": "GET", "query": { "token": "<token>" } } }`) e controlla in
  `get_workflow_execution` che "Unisci file e immagini" non abbia `immagini_mancanti`.

## 4b. Il progetto Replit (per le modifiche future)

Ogni sito pubblicato ha un progetto Replit con gli stessi file: lì si fanno le modifiche, e da lì si pubblica su
Cloudflare Pages (`pubblicazione/tracciamento/IMPOSTAZIONE.md`, sezione 5). Solo per `livello: completa`.
- Con lo strumento Replit `create_app_from_prompt`, prompt (in inglese, preciso):
  "Create a static website project named `<slug>`. Download the zip from `<link dello zip>` and extract it into
  `site/` without changing any file. Serve `site/` as a static site for preview. Add `package.json` with `wrangler`
  pinned to an exact version and the script `\"pubblica\": \"wrangler pages deploy site --project-name <slug> --branch main\"`,
  which reads `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` from Replit Secrets. Add a short README in Italian:
  edit files in `site/`, then run `npm run pubblica`. Do not add frameworks, build steps or analytics."
- Controlla con `list_app_files` che in `site/` ci siano tutte le pagine e `_redirects`; con `read_app_file` che
  `index.html` sia identico a quello del kit. Non pubblicare l'app su Replit.
- Se lo strumento non c'è o non riesce: scrivi nella scheda "progetto Replit da creare" con il prompt qui sopra.

## 5. La scheda di pubblicazione per Vincenzo

Una pagina sola, privata (`noindex`), salvata con un altro token: **`<slug>-kit-<6 caratteri>`**. È la lista di
lavoro di Vincenzo, in ordine, con caselle da spuntare. Sobria, leggibile da telefono.

1. **In breve**: dominio, dove sta il dominio, dove sta l'email, numero di reindirizzamenti, punti bloccanti.
2. **Bloccanti** (in cima, in evidenza): cosa va sistemato prima di andare online e chi deve farlo.
3. **Una settimana prima**:
   - accesso Cloudflare come membro arrivato e dominio aggiunto su Cloudflare;
   - **controllare che Cloudflare abbia importato tutti i record attuali**, soprattutto `MX` e `TXT` delle email:
     elencali come devono essere (letti dai DNS pubblici attuali, sezione 6), così Vincenzo li confronta;
   - TTL a 5 minuti dove si può.
4. **Il giorno del lancio**:
   - Cloudflare Pages: nuovo progetto `<slug>` → **Carica i file** → lo zip (link sopra) → collegare il dominio
     (dominio senza e con `www`) dalla scheda "Domini personalizzati";
   - reindirizzamento `www` ↔ senza `www` come da brief (regola di reindirizzamento in Cloudflare);
   - solo dopo che i record sono verificati: il cliente cambia i **nameserver** (guida già mandata);
   - email: tabella dei record da avere (sezione 6).
4b. **Misure** (`pubblicazione/tracciamento/IMPOSTAZIONE.md`): GA4 e contenitore GTM del cliente con i tag e gli eventi
   elencati, prova con Anteprima di GTM; **lato server** su Cloud Run solo se indicato, con il costo da comunicare al
   cliente; `misure.<dominio>` su Cloudflare senza proxy; la cookie policy aggiornata con gli strumenti usati.
   Il progetto Replit (sezione 4b) con il comando per ripubblicare.
5. **Subito dopo** (entro 1 ora): sito raggiungibile in HTTPS, 10 reindirizzamenti più importanti provati a mano,
   una mail di prova inviata e ricevuta dal cliente, **Search Console**: Vincenzo avvia il workflow
   "PrismaPixel · Search Console" (`IMPOSTAZIONE.md`, sezione 4) appena la zona è attiva su Cloudflare, poi collega
   Search Console a GA4 (in GA4 → Amministrazione → Collegamenti a Search Console).
6. **Dopo** (in 2-7 giorni): link del sito aggiornato su scheda Google, Instagram, Facebook e portali; poi
   `pubblicazione_sito` con `livello: verifica`.
7. **La tabella dei reindirizzamenti** completa (vecchio → nuovo), con le pagine "da decidere" segnate.

Non mettere mai nella scheda password, codici o token di nessun servizio.

## 6. DNS ed email: cosa scrivere nella scheda

Leggi i record pubblici attuali del dominio con lo strumento che hai a disposizione (in un terminale `dig`, oppure un
servizio DNS-over-HTTPS come `https://dns.google/resolve?name=<dominio>&type=MX`): `NS`, `A`, `CNAME` di `www`,
`MX`, `TXT` (SPF, verifiche) e `_dmarc`. Se non riesci a leggerli, scrivi "da leggere in Cloudflare" e non inventarli.

| caso | cosa scrivi |
|---|---|
| sito | `CNAME` (o il record che Cloudflare Pages propone) per il dominio e per `www` verso `<progetto>.pages.dev`: lo crea Cloudflare quando colleghi il dominio a Pages |
| email che **resta dov'è** | i record `MX` e `TXT` attuali **devono restare uguali**: elencali uno per uno |
| email **nuova** o da spostare | `MX` del fornitore scelto; SPF (un solo record `v=spf1 ...` con il fornitore); **DKIM: da copiare dal pannello del fornitore** (non si inventa); DMARC di partenza `v=DMARC1; p=none; rua=mailto:<email del cliente>`, da alzare a `quarantine` dopo 4 settimane senza problemi |
| SPF già presente | non aggiungerne un secondo: unisci i fornitori in un solo record |
| vecchio hosting con la posta dentro | bloccante finché le caselle non sono migrate: **non si disdice il vecchio hosting** |

## 7. Livello `verifica` (dopo il lancio)

Controlli sul sito vero, gratis o quasi (budget **8 crediti** Manifold; con OpenSEO anche `run_site_audit` sul
dominio, `submit_indexnow_urls` con le pagine nuove e `inspect_urls` su 2-3 pagine, `officina/OPENSEO.md`):
- home e 3 pagine chiave rispondono, in HTTPS, senza `noindex` (`seo_get_page`);
- **tutti** i reindirizzamenti della tabella portano alla pagina giusta con un solo passaggio (controllo automatico con
  richieste HEAD dal tuo ambiente, oppure `seo_get_page` sui 10 più importanti se la rete non lo permette);
- il banner compare, prima del consenso non ci sono cookie `_ga` né di pubblicità; nella scheda di Vincenzo: "in GA4
  → Rapporti in tempo reale, dopo 'Accetta tutti', arrivano page_view e un clic su WhatsApp o telefono";
- `sitemap.xml` e `robots.txt` raggiungibili;
- record `MX`, SPF e `_dmarc` presenti come da scheda (DNS pubblici);
- se c'è Search Console: le pagine con impressioni del mese (workflow "PrismaPixel · Dati Google") e, nella scheda di
  Vincenzo, il rapporto Indicizzazione → "Non trovata (404)". I 404 trovati diventano nuove righe di `_redirects` in
  una revisione del kit.

Esito con una pagina breve: cosa funziona, cosa no, cosa fare.

## 8. Esito

Come da contratto, sezione 4, con `fonte = agente_pubblicazione_sito`:
- `preview_url`: il link della **scheda di pubblicazione** (token `-kit-`);
- `descrizione`: 2 righe per Vincenzo: pronto o no, e i bloccanti;
- `note`: `durata · crediti: manifold <N> · token kit / online`, link dello zip, reindirizzamenti creati e "da
  decidere", record DNS non letti, controlli non fatti.

In `officina_fine`:
- `risultato`: `{"dominio": "...", "token_online": "...", "zip": "...", "reindirizzamenti": N, "da_decidere": [...], "tracciamento": {"gtm": "GTM-…|da creare", "ga4": "…|da creare", "server": "sì|no", "banner": "vanilla-cookieconsent 3.1.0"}, "replit": "link del progetto|da creare",
  "bloccanti": [...], "email": {"fornitore": "...", "resta": true}}`;
- `ecosistema`: area `sito` → `"pronto da pubblicare"` (o `"online"` dopo la verifica riuscita);
- `fatti`: dove stanno dominio ed email, se verificato;
- `passa_a`: dopo il kit, niente (il lancio lo fa Vincenzo); dopo una verifica riuscita, `piano_seo` se il cliente
  ha la SEO nell'abbonamento.

## 9. Limiti

- Non modificare DNS, email, Cloudflare o pannelli del cliente, non scrivere al cliente, non pubblicare niente su
  GitHub.
- Il kit online contiene solo il sito: mai brief, profilo del cliente o note per Vincenzo.
- Se il sito approvato ha problemi che non sono della pubblicazione (testi da cambiare, sezioni mancanti), non
  rifarlo: segnalali come bloccanti e proponi in `passa_a` una revisione di `sito_web`.
