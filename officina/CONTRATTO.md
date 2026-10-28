# Officina PrismaPixel · contratto comune degli agenti

Questo file vale per **tutti** gli agenti. Le istruzioni del singolo servizio (`<cartella>/ISTRUZIONI.md`) dicono
*cosa* produrre; questo file dice *come si riceve un lavoro, come si pubblica e come si avvisa*. Se un file di
servizio dice qualcosa di diverso su pubblicazione o avviso, vale questo contratto.

Lavori da solo: nessuno risponde alle domande. Decidi, e scrivi le decisioni nelle note dell'esito.

## 1. Il lavoro che ricevi

Il messaggio di avvio contiene un JSON:

```json
{
  "job_id": "pp-20261026-ab12",
  "sessione": "id della conversazione",
  "canale": "demo|whatsapp|instagram|facebook|telegram|linkedin|prova",
  "deliverable": "sito_web",
  "livello": "completa|revisione|prima",
  "brief": { "attivita": "", "settore": "", "area": "", "offerta": "", "pubblico": "", "obiettivo": "", "tono": "", "stile_visivo": "", "materiali_cliente": "", "note": "" },
  "modifiche_richieste": "solo per revisione",
  "token_precedente": "solo per revisione: token dell'anteprima da rivedere",
  "profilo_cliente": { "...": "quello che il venditore ha capito del cliente, compresa la mappa digitale 'ecosistema'" },
  "n8n": { "data_table_id": "9wrhA9G6HrcvjpTj", "project_id": "KSisbb8i7nHhzFqw" }
}
```

- Se il JSON manca o non si legge: esito `errore` con note "JSON del lavoro mancante o illeggibile" (sezione 4) e fermati.
- `deliverable` decide le istruzioni da seguire (tabella in sezione 5). Deliverable sconosciuto o senza
  istruzioni: esito `errore` con note "deliverable non ancora disponibile: <nome>" e fermati.
- `canale: prova` = lavoro del banco di prova: comportati esattamente come con un cliente vero.

## 2. Dove lavori

1. Segna l'ora di inizio.
2. Clona il repository delle istruzioni (pubblico, solo lettura):
   `git clone --depth 1 https://github.com/PrismaPixel/prismapixel-anteprime.git /tmp/officina`
   Non serve fare push: il repository contiene solo istruzioni, modelli e skill. **Non pubblicare niente su GitHub.**
3. Cartella di lavoro: `/tmp/lavoro/<slug>/`, con `slug` = nome dell'attività in minuscolo con trattini
   (solo `a-z`, `0-9`, `-`, massimo 40 caratteri).
4. Leggi per intero le istruzioni del servizio e le skill che indicano, dal clone.
5. **Registra il lavoro nell'Agent OS** (sezione 4b, inizio) e leggi il contesto che ti restituisce: memoria del
   cliente, note di Vincenzo, lavori già fatti e il risultato del lavoro precedente se è un passaggio di testimone.
   Usalo: non contraddire ciò che è già stato scoperto o deciso.
   Se il contesto contiene un **posizionamento** e una **voce dei clienti** (dall'audit), i contenuti partono da lì:
   la stessa promessa di fondo e le parole dei clienti. Non inventarne un'altra.
   Se contiene una **consulenza strategica** (`deliverable = roadmap`), usa anche `risultato.offerta_proposta`,
   `obiezioni` e `angoli`: l'offerta da promuovere, i dubbi da sciogliere e gli angoli da testare. Sono proposte: se
   le note dicono che il cliente non le ha ancora confermate, segnalo anche tu come "da confermare".

## 3. Pubblicare l'anteprima (servizio Anteprime su n8n)

Le anteprime non vanno su GitHub: si salvano nella tabella n8n **"PrismaPixel · Anteprime"** e n8n le mostra a un
link privato.

- Tabella: `dataTableId` **`kXLpCtTmis3WME7A`**, `projectId` **`KSisbb8i7nHhzFqw`**.
- **Token** dell'anteprima: `<slug>-<6 caratteri casuali a-z0-9>` (es. `trattoria-da-nino-k3x9q2`). Solo
  `a-z`, `0-9`, `-`, tra 6 e 80 caratteri. Generalo una volta, con un generatore casuale vero
  (`tr -dc a-z0-9 </dev/urandom | head -c6`). Un nuovo lavoro, anche una revisione, ha sempre un token nuovo.
- **Ogni file è una riga** con lo strumento n8n `add_data_table_rows`:

  | colonna | valore |
  |---|---|
  | token | il token |
  | pagina | nome del file: `index.html`, `camere.html`, `stile.css`, `script.js` |
  | html | il contenuto completo del file (anche per CSS e JS) |
  | job_id | dal JSON |
  | deliverable | dal JSON |
  | titolo | nome dell'attività |

- **Una riga per chiamata** (le pagine sono grandi). Limite pratico verificato: 400 KB per file.
- Nomi dei file: solo `[a-z0-9-]+\.(html|css|js|svg|json|txt)`, **niente sottocartelle**. La pagina principale
  si chiama sempre `index.html`.
- Link tra le pagine **relativi** (`camere.html`, `stile.css`). Mai link che iniziano con `/`.
- **Immagini**: niente file immagine nella tabella. Usa i link diretti di Higgsfield (versione `_min.webp`) o
  immagini SVG scritte nel codice. Font da Google Fonts.
- Per correggere un file già salvato basta salvarne una nuova riga con lo stesso token e lo stesso nome:
  vale l'ultima.
- **Link dell'anteprima** (quello da mettere nell'esito):
  `https://integrazioni.app.n8n.cloud/webhook/30f9ffb0-81c6-47ee-b2da-e35b2d3982c2/anteprima/<token>/index.html`
- Revisione (`livello: revisione`): leggi i file del lavoro precedente con `get_data_table_rows` sulla stessa
  tabella, filtro `token = token_precedente`, prendi per ogni `pagina` l'ultima riga, applica le modifiche e
  salva tutto sotto il **nuovo** token.
- Ogni pagina HTML contiene `<meta name="robots" content="noindex, nofollow">`, viewport, titolo, description,
  immagine Open Graph e in fondo, piccolo: "Anteprima realizzata da PrismaPixel · prismapixel.it".
- Prima di salvare, controlla in locale (`/tmp/lavoro/<slug>/`) con i controlli del servizio: si pubblica solo
  ciò che passa.

## 4. L'esito (sempre, anche in caso di errore)

Alla fine scrivi **una riga** nella tabella delle bozze con `add_data_table_rows`: `dataTableId` e `projectId`
presi da `n8n` nel JSON (predefiniti `9wrhA9G6HrcvjpTj` e `KSisbb8i7nHhzFqw`).

| colonna | valore |
|---|---|
| job_id, sessione, canale, deliverable, livello | dal JSON |
| fonte | `agente_<deliverable>` (es. `agente_sito_web`, `agente_audit_strategia`): n8n legge solo le righe che iniziano con `agente_` |
| stato | `pronta` oppure `errore` |
| preview_url | il link dell'anteprima (vuoto se errore) |
| descrizione | 2-3 frasi per il venditore: cosa contiene e i 2 punti più forti per questo cliente, con parole da cliente |
| brief_json | il brief ricevuto, come stringa JSON |
| note | per Vincenzo, in quest'ordine: `durata: <N> min · crediti: <servizio> <N> · token: <token>`, poi direzione scelta, contenuti d'esempio da confermare, controlli non eseguiti, problemi |

Se qualcosa si rompe a metà, scrivi comunque l'esito `errore` con il motivo: un lavoro senza esito blocca il
venditore.

## 4b. Agent OS (database Supabase condiviso da tutti gli agenti)

Con lo strumento Supabase `execute_sql`, progetto **`oshnvlkwuclxbbjdaupt`**. Se Supabase non risponde, vai avanti
lo stesso e scrivilo nelle note dell'esito: l'Agent OS non deve mai bloccare un lavoro.

- **Inizio** (subito dopo aver letto il JSON): `select officina_inizio('<JSON del lavoro>'::jsonb);`
  Restituisce `contesto` con la scheda cliente (`cliente.memoria`, `cliente.note_vincenzo`, `cliente.lavori`) e
  `job.dal_lavoro_precedente`.
- **Fine** (subito dopo l'esito nella tabella n8n): `select officina_fine('<JSON>'::jsonb);` con
  `{job_id, stato: "pronta"|"errore", preview_url, descrizione, note, crediti, risultato, fatti, passa_a}`:
  - `crediti`: numero intero dei crediti usati (Higgsfield o Manifold);
  - `risultato`: oggetto con ciò che serve ai prossimi agenti (es. audit: `{"priorita": [...], "piano_90_giorni": {...}}`; sito: `{"pagine": [...], "palette": [...], "token": "..."}`);
  - `fatti`: 2-5 fatti utili sul cliente, `[{"tipo": "problema|fatto|obiettivo|preferenza|risultato", "testo": "..."}]`, solo cose verificate;
  - `passa_a`: il lavoro successivo consigliato, `[{"deliverable": "sito_web", "brief": {...}}]` (l'audit indica sempre il servizio della priorità n°1; gli altri solo se ha senso). Il lavoro non parte da solo: aspetta l'approvazione di Vincenzo.
- Nell'SQL scrivi il JSON come stringa tra apici singoli, raddoppiando ogni apice interno (`l'orto` → `l''orto`).

## 5. Servizi e istruzioni

| deliverable | istruzioni | stato |
|---|---|---|
| `sito_web` | `siti/ISTRUZIONI.md` | attivo |
| `audit_strategia` | `audit/ISTRUZIONI.md` | attivo |
| `landing_page` | `landing/ISTRUZIONI.md` | attivo (in prova) |
| `carosello_social` | `social/ISTRUZIONI.md` | attivo (in prova) |
| `script_video` | `video/ISTRUZIONI.md` | attivo (in prova) |
| `video_ai` | `video-ai/ISTRUZIONI.md` | attivo (in prova) |
| `video_montaggio` | `montaggio/ISTRUZIONI.md` | attivo (in prova) |
| `ricerca_clienti` (interno) | `clienti/ISTRUZIONI.md` | attivo (in prova) |
| `piano_seo` | `seo/ISTRUZIONI.md` | da costruire |
| `annunci_ads` | `ads/ISTRUZIONI.md` | attivo (in prova) |
| `roadmap` | `strategia/ISTRUZIONI.md` | attivo (in prova) |
| `sequenza_email` | `email/ISTRUZIONI.md` | attivo (in prova) |
| `brand_concept` | `brand/ISTRUZIONI.md` | da costruire |
| `flusso_automazione` | `automazioni/ISTRUZIONI.md` | da costruire |
| `programma_formazione` | `formazione/ISTRUZIONI.md` | da costruire |

## 6. Regole fisse per tutti

- Italiano naturale, voce PrismaPixel: serena, entusiasta, professionale. Niente frasi da brochure, nessuna firma.
- **Mai inventare prove**: niente recensioni, citazioni, numeri di clienti, premi, loghi di partner, anni di attività.
- **Mai inventare contatti**: telefono, email e indirizzo solo se sono nel brief, altrimenti segnaposto chiaro
  ("Telefono · da inserire").
- Mai prezzi di PrismaPixel, mai garanzie di risultato (posizioni su Google, comparire nelle AI, fatturato).
- **Gli obiettivi del cliente non si dicono al pubblico.** Ciò che il brief chiama obiettivo (es. "prenotazioni
  dirette invece che da Booking", "riempire la sala d'inverno", "più richieste online") orienta la strategia e la
  scelta della CTA, ma non finisce mai nei testi: niente "prenota diretto", "senza intermediari", "niente commissioni"
  e simili, che sono vantaggi per l'attività e non per chi guarda. La CTA dice **cosa ottiene la persona** facendo quel
  gesto, con parole sue (es. "Scrivici: ti diciamo quale camera prende il tramonto"; "Mandaci le tue date, ti
  rispondiamo noi, non un call center").
- Ciò che non è confermato da dati o dal brief: "da verificare" o "da confermare con il cliente" nelle note.
- Settore sanitario: niente promesse di risultato, linguaggio sobrio.
- Il repository è pubblico: non scriverci mai niente. Brief, profilo e note vanno solo nelle tabelle n8n.
- Crediti: rispetta il budget del servizio e scrivi sempre nell'esito quanti ne hai usati.
