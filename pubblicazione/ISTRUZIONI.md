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
   Se il cliente ha collegato Search Console (accesso `search_console`), le pagine con clic negli ultimi 3 mesi
   (`console_get_search_analytics`) vengono prima di tutte.
   Budget Manifold: **15 crediti**; `seo_run_technical_crawl` solo con `dry_run` prima e se la stima sta nel budget.
2. **Tabella dei reindirizzamenti 301**: ogni pagina vecchia va alla pagina nuova **più simile per contenuto**.
   - Mai tutte alla home: la home solo per la home vecchia o per pagine che non hanno nessun equivalente.
   - Le pagine vecchie che portano clic e non hanno equivalente vanno segnalate come **da decidere** (nuova pagina o
     sezione), non nascoste.
   - Varianti da coprire: con e senza `/` finale, `.html`/`.php`, `index.html`, maiuscole se il vecchio sito le usava.
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
  `_redirects`, `_headers`, `sitemap.xml`, `robots.txt`, `immagini.json`.
- Link dello zip da caricare su Cloudflare Pages (scarica anche le immagini di `immagini.json`):
  `https://integrazioni.app.n8n.cloud/webhook/689f7b2a-d224-412c-9500-db025a61d096/scarica-sito/<token>`
  Se puoi, provalo con `execute_workflow` sul workflow **"PrismaPixel · Scarica sito"**
  (`workflowId: "0xRQUDMFFsTnm80I"`, `executionMode: "production"`, `triggerNodeName: "Richiesta zip"`,
  `inputs: { "webhookData": { "method": "GET", "query": { "token": "<token>" } } }`) e controlla in
  `get_workflow_execution` che "Unisci file e immagini" non abbia `immagini_mancanti`.

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
5. **Subito dopo** (entro 1 ora): sito raggiungibile in HTTPS, 10 reindirizzamenti più importanti provati a mano,
   una mail di prova inviata e ricevuta dal cliente, Search Console verificata con record TXT e sitemap inviata,
   Google Analytics collegato se previsto.
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
- 10 reindirizzamenti della tabella portano alla pagina giusta;
- `sitemap.xml` e `robots.txt` raggiungibili;
- record `MX`, SPF e `_dmarc` presenti come da scheda (DNS pubblici);
- se c'è Search Console: pagine indicizzate e errori 404 delle ultime settimane (`console_get_search_analytics`,
  `console_inspect_url` su 2-3 pagine). I 404 trovati diventano nuove righe di `_redirects` in una revisione del kit.

Esito con una pagina breve: cosa funziona, cosa no, cosa fare.

## 8. Esito

Come da contratto, sezione 4, con `fonte = agente_pubblicazione_sito`:
- `preview_url`: il link della **scheda di pubblicazione** (token `-kit-`);
- `descrizione`: 2 righe per Vincenzo: pronto o no, e i bloccanti;
- `note`: `durata · crediti: manifold <N> · token kit / online`, link dello zip, reindirizzamenti creati e "da
  decidere", record DNS non letti, controlli non fatti.

In `officina_fine`:
- `risultato`: `{"dominio": "...", "token_online": "...", "zip": "...", "reindirizzamenti": N, "da_decidere": [...],
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
