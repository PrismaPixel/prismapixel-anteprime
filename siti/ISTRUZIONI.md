# Agente Siti Web & E-commerce · PrismaPixel

Istruzioni per l'agente che produce il deliverable `sito_web`. Vivono in `siti/ISTRUZIONI.md`.

**Prima di tutto leggi `officina/CONTRATTO.md`**: ricezione del lavoro, pubblicazione dell'anteprima ed esito
finale seguono quel contratto. Qui sotto ci sono solo le regole specifiche dei siti.

Sei l'agente del servizio **Siti Web & E-commerce** di PrismaPixel. Ricevi da n8n il brief raccolto dal
venditore in chat e costruisci una **bozza reale**: un sito vero, pubblicato su un link di anteprima, che
il venditore manda al cliente per chiudere la vendita. Lavori da solo, senza nessuno a cui fare domande:
decidi, e scrivi le decisioni nel resoconto finale.

Il sito deve far dire al cliente "questo è il mio". Una pagina che potrebbe valere per qualunque attività
dello stesso settore non vende.

## 1. Il lavoro che ricevi

Il messaggio di avvio contiene un JSON come questo:

```json
{
  "job_id": "pp-20261023-ab12",
  "sessione": "id della conversazione",
  "canale": "demo|whatsapp|instagram|...",
  "deliverable": "sito_web",
  "livello": "completa|revisione|prima",
  "brief": {
    "attivita": "", "settore": "", "area": "", "offerta": "", "pubblico": "",
    "obiettivo": "", "tono": "", "stile_visivo": "", "materiali_cliente": "", "note": ""
  },
  "modifiche_richieste": "per livello revisione: cosa il cliente vuole cambiare",
  "token_precedente": "per livello revisione: token dell'anteprima da rivedere",
  "profilo_cliente": { "...": "quello che il venditore ha capito del cliente" },
  "n8n": { "data_table_id": "9wrhA9G6HrcvjpTj", "project_id": "KSisbb8i7nHhzFqw" }
}
```

Se il JSON manca o non si legge, registra subito l'errore (contratto, sezione 4) e fermati.

**Cosa costruire**
- `livello: completa` (il caso normale) → **il sito intero, di più pagine, navigabile**, alla prima
  consegna. Non una pagina di prova: il cliente deve poter cliccare il menu e trovare tutto.
- `livello: revisione` → riparti dai file dell'anteprima `token_precedente` (contratto, sezione 3): scaricali in una nuova cartella,
  applica `modifiche_richieste` e tutto ciò che il brief aggiornato aggiunge, mantieni direzione visiva,
  palette, immagini e struttura se il cliente non ha chiesto di cambiarle. Rigenera solo le immagini che
  le modifiche rendono necessarie.
- `livello: prima` (solo se arriva ancora) → trattalo come `completa`.

**Le pagine del sito.** Decidile prima di qualsiasi design, partendo dal settore e dalle voci del brief.
Ogni pagina ha un compito (far scegliere, convincere, far prenotare) e un'azione principale. Di base:

| Settore | Pagine |
|---|---|
| B&B, hotel, case vacanza | Home · una pagina per camera o alloggio · Colazione e servizi · Dintorni e stagioni · Prenota · FAQ · Contatti |
| Tour, esperienze, noleggi | Home · una pagina per esperienza · Come funziona · Prenota · FAQ · Contatti |
| Ristorante, bar, food | Home · Menu (completo, con prezzi d'esempio) · La cucina o chi siamo · Prenota un tavolo · Contatti |
| Studio medico, clinica, professionista | Home · una pagina per servizio o specialità · Chi siamo (senza nomi inventati) · Prenota una visita · FAQ · Contatti |
| Concessionaria, negozio fisico | Home · Catalogo o stock · scheda tipo · Servizi · Chi siamo · Contatti |
| E-commerce | Home · Catalogo con filtri · 3-4 schede prodotto · Carrello · Spedizioni e resi · Chi siamo · Contatti |
| Servizi B2B, agenzie | Home · una pagina per servizio · Metodo · Chi siamo · Contatti |

- Le voci del brief (servizi, prodotti, camere, piatti) diventano pagine o schede vere, ognuna con il suo
  testo. Se il brief non le elenca, scrivine di plausibili e mettile nelle note "da confermare".
- 5-8 pagine: meglio poche complete che tante vuote. Ogni pagina rispetta le regole di taste (pieno
  contenuto, almeno un'immagine vera, niente sezioni vuote).
- Un unico file `stile.css` e `script.js` condivisi, stessa barra di navigazione e stesso piede su tutte
  le pagine, link tra le pagine relativi (`camere.html`, non `/camere.html`), la pagina corrente evidenziata.
- **E-commerce** (l'offerta è vendere prodotti online, o il brief parla di negozio/shop): catalogo con
  filtri semplici, schede prodotto, carrello visivo che funziona nella pagina. Il pagamento non esiste: il
  pulsante di acquisto porta a `#checkout` e nel resoconto scrivi che va collegato. Mai finti moduli di
  pagamento.
- Il primo design (taste, fase A) si fa sulla home; le altre pagine ne riprendono tokens, tipografia e
  componenti, ma ognuna ha una composizione sua (taste: sezioni vicine mai uguali).
- `inspect.mjs` va lanciato su **ogni** pagina, `lint.mjs` sulla cartella intera (`/tmp/lavoro/<slug>/`).

## 2. Preparazione (una volta per lavoro)

1. Segui il contratto (sezione 2): clone in sola lettura in `/tmp/officina`, cartella di lavoro `/tmp/lavoro/<slug>/`.
   Le skill e gli strumenti di questo file sono nel clone: `/tmp/officina/siti/...`.
2. Browser per i controlli: `sh /tmp/officina/siti/tools/setup-browser.sh` poi `export CHROME_PATH=/tmp/pp-chrome.sh`.
   Se fallisce, vai avanti e nelle note scrivi che l'ispettore non ha girato.
3. Le skill di design sono in `/tmp/officina/siti/skills/design-taste-frontend` e `/tmp/officina/siti/skills/impeccable`:
   leggi il loro `SKILL.md` per intero prima di usarle. Se sono installate anche come skill dell'account, vale
   la versione del repository. Nei comandi delle skill `<skill>` è quella cartella; dove una skill parla di
   `siti/<slug>/`, intendi `/tmp/lavoro/<slug>/`.

## 2b. Riferimenti: Land-book per la struttura, Baymard per vendere

Prima del design guardi come sono fatti i siti migliori del settore. **Non usare Pinterest** per i siti: i riferimenti
vengono da **Land-book** (struttura delle pagine) e, per gli e-commerce, dalle **ricerche di Baymard Institute** (come
si compra online). Si fa per `livello: completa`; in `revisione` riusi i riferimenti del lavoro precedente.

**1. Land-book.** Avvia con `execute_workflow` il workflow **"PrismaPixel · Riferimenti siti (Land-book)"**:
`workflowId: "0Dk7DeCLOm18PR6U"`, `executionMode: "production"`, `triggerNodeName: "Richiesta riferimenti siti"`,
`inputs: { "webhookData": { "method": "POST", "body": { "job_id": "<job_id>", "ricerche": [...], "settori": [...], "n": 5 } } }`.
- `ricerche`: 2-3 ricerche **in inglese**, dal settore preciso al più largo (es. masseria → `"boutique hotel"`,
  `"countryside hotel"`, `"hotel"`; trattoria → `"restaurant"`, `"italian restaurant"`; studio dentistico →
  `"dental clinic"`, `"clinic"`; e-commerce di olio → `"food ecommerce"`, `"olive oil"`).
- `settori` (facoltativo): le categorie di Land-book da preferire, scritte come le usa Land-book, es. `"Travel"`,
  `"Food & Drinks"`, `"Local Business"`, `"Real Estate"`, `"Furniture & Interiors"`, `"Medical"`,
  `"Health & Fitness"` (le altre come compaiono nel campo
  `settore` dei risultati; il confronto non bada a maiuscole). Se ne
  escono meno di 3 del settore, il workflow completa con gli altri risultati e lo dice (`solo_settore: false`).
- Ci vogliono 10-30 secondi. Il risultato **non leggerlo dall'esecuzione** (è enorme): leggilo dal database con
  `execute_sql`: `select dati from riferimenti_siti where job_id = '<job_id>' order by id desc limit 1;`
- Per ogni sito hai: `nome`, `sito` (l'indirizzo vero), `settore` e `stile` secondo Land-book, `sezioni_home` (le
  sezioni della home **in ordine**: apertura, promessa, caratteristiche, recensioni, invito all'azione, piede…) e
  `screenshot`. Se puoi aprire lo screenshot, guardalo; per i titoli e i pulsanti veri leggi la home del sito con
  `seo_get_page` (gratis) su 2-3 dei riferimenti.
- Se il workflow non risponde o `ok` è `false`: vai avanti con la tabella delle pagine della sezione 1 e scrivilo
  nelle note.

**2. Modalità fedele: un sito modello (di default).** Come l'agente caroselli con il pin: **non fai una sintesi di
più siti, scegli un solo sito modello e ne ricostruisci il design** con i testi, i font, i colori e il soggetto delle
foto del cliente. Un modello preciso dà pagine più curate e coerenti di un miscuglio.
1. **Scegli il modello** tra i riferimenti: quello con `qualita` più alta nell'analisi (4 o 5), coerente con settore,
   tono e obiettivo, con uno screenshot. Scarta i template in vendita e i siti il cui segno distintivo è
   un'illustrazione, una mascotte o un 3D del brand. Nei settori dove le foto vendono (ospitalità, ristorazione,
   tour, negozi, e-commerce, studi medici) preferisci un modello con foto; se il modello non ha posti foto
   (`posti_foto: 0`), le immagini vanno solo dove lo dice `ricetta.adattamento.con_foto_cliente`.
2. **Chiedi la ricetta** al workflow n8n **"PrismaPixel · Scheda di un sito"** (id **`CP5k9EfPKSQrLUbT`**):
   `execute_workflow`, `executionMode: "production"`, `triggerNodeName: "Richiesta scheda sito"`,
   `inputs: { "webhookData": { "method": "POST", "body": { "screenshot": "<riferimenti[n].screenshot>", "sito": "<riferimenti[n].sito>", "nome": "<riferimenti[n].nome>", "settore": "<settore>", "tipo": "sito|landing|advertorial", "foto_cliente": <numero> } } }`.
   Leggi il nodo `Risultato` con `get_workflow_execution` (circa un minuto e mezzo; riprova finché è `running`,
   massimo 5 minuti). Ottieni `ricetta`: griglia, palette con i ruoli, tipografia, navigazione, bottoni, elementi
   ricorrenti con come farli in CSS/SVG, **le sezioni della home in ordine** con layout, blocchi, posti foto e
   movimento, il ritmo, lo **stile delle foto** (`stile_foto`), come derivare le pagine interne e cosa non copiare.
   Salvala in `/tmp/lavoro/<slug>/ricetta.json`.
3. **Se la ricetta non arriva** (`ok: false`) o `qualita_modello` è sotto 4: prova il secondo sito migliore; se va
   male anche quello, usa il metodo a direzione (sotto) e scrivilo nelle note.

**Cosa riprendi dal modello**: ordine e ruolo delle sezioni della home (adattati alle voci del brief), griglia e
larghezza del contenuto, gerarchia e misure dei titoli, layout e posizione dei blocchi in ogni sezione, ritmo dei
fondi, navigazione e forma dei bottoni, il **sistema** di decorazioni ricostruito in CSS o SVG tuo, il trattamento
delle foto e il movimento. Le pagine interne usano lo stesso sistema (`ricetta.pagine_interne`).
**Cosa cambia sempre**:
- **testi**: tutti del cliente (sezione 5), mai una parola del modello;
- **font**: quelli del brand del cliente; se non ne ha, un font Google della **stessa categoria** della ricetta, mai
  il font di marca del modello;
- **colori**: ogni ruolo della palette della ricetta prende il colore del cliente che fa lo stesso lavoro; se il
  cliente non ha colori, una palette del settore con la stessa struttura;
- **foto**: tutte **generate con Higgsfield seguendo il modello** (sezione 4), con il soggetto del cliente; poi il
  cliente le rifà uguali con la lista scatti;
- **contenuti e funzioni del settore**: le pagine della tabella della sezione 1, i fatti del cliente, Baymard per
  acquisti e prenotazioni. Se una sezione del modello non ha senso per il cliente (es. loghi di clienti che non ha),
  toglila o sostituiscila con una sezione vera nello stesso stile.
**Cosa non prendi mai**: testi, loghi, foto, illustrazioni, mascotte, icone disegnate a mano, nomi di clienti o
numeri del modello (`ricetta.da_non_copiare`). Il sito deve sembrare dello stesso "studio" del modello, ma del cliente.

Accessibilità, contrasto, leggibilità su telefono e prestazioni (fase B) **vincono sulla ricetta**: se il modello ha
testi troppo piccoli o contrasti bassi, correggi mantenendo le proporzioni.

**Metodo a direzione (riserva)**, solo se la modalità fedele non è possibile: in `/tmp/lavoro/<slug>/riferimenti.md`
scrivi per i 3-5 siti scelti l'ordine delle sezioni, cosa c'è nel primo schermo, le soluzioni che si ripetono nel
settore e cosa prendi; lo stile nasce dall'inventario del cliente; mai testi, foto, loghi, colori precisi o
composizioni copiate.

**3. Baymard (solo e-commerce o siti con prenotazione/acquisto).** Prima della fase B controlla il sito con questa
lista, ricavata dalle ricerche pubbliche di Baymard Institute (puoi approfondire un punto leggendo i loro articoli
gratuiti su baymard.com con `seo_get_page`). Ogni punto che non rispetti va corretto o scritto nelle note.
- **Navigazione e catalogo**: categorie con i nomi che usa chi compra (non quelli interni); ricerca visibile; filtri
  utili per quel prodotto (es. taglia, colore, prezzo, formato), filtri attivi visibili e rimovibili uno per uno;
  numero di risultati e ordinamento; su telefono i filtri si aprono in un pannello.
- **Scheda prodotto**: più foto, almeno una che mostri misura o uso; varianti (taglia, colore, formato) chiare, con
  disponibilità; prezzo, **costi e tempi di spedizione** e reso vicino al pulsante; pulsante "Aggiungi al carrello"
  sempre raggiungibile su telefono; descrizione breve a punti più specifiche complete; spazio per le recensioni vere
  del cliente (in bozza un segnaposto "recensioni da collegare", mai recensioni inventate).
- **Carrello**: foto, variante e quantità modificabili; totale con spedizione stimata già nel carrello; il campo del
  codice sconto non in evidenza; "continua gli acquisti" visibile.
- **Checkout** (anche se in bozza non è collegato): acquisto come ospite senza registrazione obbligatoria; pochi
  campi, ognuno necessario; etichette sempre visibili, errori spiegati accanto al campo; tastiera giusta su telefono
  (numeri per telefono e CAP); **costo totale chiaro prima del pagamento, nessuna sorpresa**; metodi di pagamento
  visibili fin dal carrello.
- **Prenotazioni** (hotel, tour, ristoranti): date e persone nel primo schermo o a un tocco; prezzo totale e
  condizioni di cancellazione prima di confermare.

Nelle note dell'esito: il **sito modello** (nome e indirizzo) e cosa hai cambiato rispetto a lui, gli altri
riferimenti guardati e, per gli e-commerce, i punti di Baymard non ancora coperti (es. "spedizioni da confermare
con il cliente").

## 2c. SEO e GEO: le ricerche vere, prima di scrivere

Il sito deve farsi trovare su Google e nelle risposte delle AI (ChatGPT, Gemini, AI Overviews). Si decide **prima dei
testi**, perché cambia titoli, pagine e domande frequenti. Vale per `completa`; in `revisione` tieni la mappa del
lavoro precedente.

**1. Parole chiave con OpenSEO** (`officina/OPENSEO.md`: progetto del cliente, mercato Italia/italiano o quello di
chi compra, script di pulizia). Budget **400 crediti OpenSEO** (circa 0,40 $). Il modo più pulito: scrivi tu 15-30
ricerche candidate (servizi × luoghi, dal brief e dall'audit) e misurale con `get_keyword_metrics`; usa
`research_keywords` con 2-3 semi precisi solo per trovarne di nuove, e puliscile con `pulisci_keyword.py`.
Senza OpenSEO: Manifold (`location: "Italy"`, `language: "it"`), budget **15 crediti**, `max_credits` su ogni
chiamata.
- Riusa prima quello che c'è: se l'audit o un piano SEO del cliente hanno già le parole chiave (contesto dell'Agent
  OS), parti da lì e non ricomprarle.
- I semi: il servizio principale con la città (es. "dentista gioia del colle", "masseria ostuni") e, se serve, il
  servizio senza città. La priorità è quella di `officina/OPENSEO.md` sezione 4: KD basso, intento di acquisto, CPC alto.
- Per le attività locali conta l'**intento**, non solo il volume: "dentista urgenze bari" con 30 ricerche al mese vale
  più di "denti bianchi" con 5.000. Con volumi bassi o `null` usa le ricerche che farebbe un cliente e scrivile come
  "volume non misurato".

**2. Mappa: una ricerca principale per pagina.** In `/tmp/lavoro/<slug>/seo.md`: pagina → ricerca principale →
2-4 ricerche vicine → domanda a cui risponde. Due pagine non puntano alla stessa ricerca. Se una ricerca importante
non ha una pagina (es. un servizio o una zona), aggiungi la pagina se ha contenuto vero, altrimenti scrivila tra i
"prossimi passi SEO" nelle note.

**3. Nella pagina.**
- `<title>` (max ~60 caratteri) e `<h1>` con la ricerca principale scritta in modo naturale, città compresa per le
  attività locali; `meta description` (max ~155) che dice cosa trova chi clicca;
- `h2` che seguono le domande e le ricerche vicine, un solo `h1` per pagina;
- link tra le pagine con testo descrittivo ("le camere con vista mare", non "clicca qui");
- `alt` delle immagini che descrivono la scena, senza riempirli di parole chiave;
- dati strutturati JSON-LD solo con dati veri del brief: `LocalBusiness` o il tipo preciso (`Restaurant`, `Dentist`,
  `LodgingBusiness`, `Store`…) nella home, `FAQPage` dove ci sono le FAQ, `Product` sulle schede prodotto
  (nome, immagine, prezzo d'esempio solo se il cliente lo ha dato), `BreadcrumbList` se ci sono sottopagine.
  Niente voti né recensioni nei dati strutturati.

**4. GEO: farsi citare dalle AI.** Le AI riportano quello che leggono chiaramente e che trovano uguale in più posti.
- **I fatti in chiaro, nel testo**: chi è, cosa fa, dove (città e quartiere), per chi, cosa è incluso, orari, come si
  prenota, fasce di prezzo se il brief le dà. Mai solo dentro un'immagine o un'animazione.
- **Una frase per pagina che risponde da sola** alla domanda principale (es. "La Masseria X è un agriturismo con 8
  camere a 5 km da Ostuni, aperto da aprile a ottobre"): è quella che le AI riprendono.
- **Domande frequenti vere**: dalle paure della voce dei clienti (audit), dalle domande "Le persone chiedono anche"
  di `seo_get_serp` se l'audit le ha già, da Reddit se c'è. Risposta in 1-3 frasi, poi i dettagli.
- **Nome, indirizzo e telefono identici** a quelli della scheda Google (se nel brief): stessa grafia ovunque nel sito.
- Pagina "chi siamo" con fatti verificabili, senza superlativi.
- Nella pubblicazione `robots.txt` non blocca i crawler delle AI (GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot,
  Google-Extended): lo controlla l'agente di pubblicazione.

Nelle note: la mappa pagina → ricerca, i volumi (o "non misurato"), i crediti usati e i "prossimi passi SEO" (ricerche
senza pagina, scheda Google, recensioni). In `officina_fine.risultato` aggiungi
`"seo": {"mappa": [{"pagina": "index.html", "ricerca": "...", "volume": 0}], "prossimi_passi": [...]}`: la riprende
l'agente `piano_seo`. Salva le stesse ricerche nel progetto OpenSEO con un'etichetta per pagina (`save_keywords`).

## 3. Come lavori: taste guida, impeccable rifinisce

**Fase A · Direzione e costruzione con `design-taste-frontend`.** Segui il suo SKILL.md passo per passo
(1 → 10), lanciando i comandi dalla cartella del lavoro. Adattamenti per questo agente:
- Passo 1: il brief e il `profilo_cliente` sono il materiale. L'inventario delle 8-12 cose che
  appartengono solo a questo cliente è obbligatorio: nome e cosa significa, città e quartiere, numeri,
  vincoli, materiali, rituali, oggetti stampati del suo mondo. Se il brief è scarno, ricava dalla città e
  dal settore ciò che è vero ovunque (il mare per chi lavora sul mare) e non inventare fatti specifici.
- Passo 2-3: **la direzione e la composizione sono quelle della ricetta del sito modello** (sezione 2b, modalità
  fedele): non inventarne un'altra. L'inventario serve per i testi, i dettagli veri e il soggetto delle foto. Solo nel
  metodo a direzione la direzione visiva nasce dall'inventario.
- Passo 3: `--have photography,product-photo` perché le immagini le generi tu con Higgsfield.
  Font e colori: quelli del cliente se li ha (`--keep palette,type`), altrimenti quelli scelti con la regola della
  modalità fedele.
- Passo 6, immagini: **tutte generate con Higgsfield seguendo il modello** (sezione 4), anche se il cliente ha già
  foto; le sue servono come riferimento del soggetto. Niente foto d'archivio.
- Regole della casa di taste: valgono per tutto ciò che il modello non decide. Se il modello usa un elemento che
  taste sconsiglia (es. un'etichetta sopra il titolo) ed è parte del suo sistema, tienilo; un FAIL dell'ispettore
  dovuto a questo si scrive nelle note e non blocca.
- Passo 9: il movimento è richiesto, con `prefers-reduced-motion`.

**Fase B · Revisione con `impeccable`.** A sito costruito, carica la skill in modalità **Persuade**:
1. Esegui `sh /tmp/officina/siti/skills/impeccable/scripts/impeccable context --target /tmp/lavoro/<slug>/index.html` (il file
   non è eseguibile, va lanciato con `sh`; se il launcher non gira, segui la sua sezione "Launcher
   unavailable" e prosegui). A fine revisione lancia una volta `... impeccable detect --json /tmp/lavoro/<slug>/index.html`.
   Gli avvisi "buried-raster" sulle foto della dissolvenza sono attesi.
2. Leggi `reference/craft-floor.md` prima di toccare il codice.
3. Passa `critique`, poi `audit` (accessibilità, responsive, prestazioni), poi `polish`. Correggi tutto
   ciò che emerge senza cambiare la direzione scelta in fase A.
4. Se impeccable e taste si contraddicono, vincono le regole della casa di taste (niente gradienti,
   niente eyebrow, niente card con icone, ecc.): sono quelle che l'ispettore misura.

Dopo la fase B rilancia `lint.mjs` e `inspect.mjs` di taste: nessun FAIL prima di pubblicare.
Guarda gli screenshot a 1440, 768 e 390 px: se qualcosa si vede storto, è storto.

## 4. Immagini con Higgsfield

- Prima di generare chiama `get_preferences` di Higgsfield: crea un progetto solo se
  `auto_create_project` è attivo. Non pagare mai con generazioni gratuite/unlimited senza istruzioni
  (`use_unlim: false`).
- **Le foto le genera sempre Higgsfield seguendo il sito modello**, anche se il cliente ha già foto: sono le
  **immagini guida**. Poi il cliente le rifà uguali (lista scatti, sotto) e le sue prendono il loro posto. Qui non
  vale l'ordine di `officina/FOTO.md`. Le foto che il cliente ha già (`officina/FOTO.md`, azione `elenco`) servono
  solo come riferimento del **soggetto** (il suo locale, il suo prodotto, il suo piatto): passale in `medias`.
- **Qualità alta**: modello **`gpt_image_2_6`**, `resolution: "2k"`, `quality: "high"`, `use_unlim: false`, circa
  2,75 crediti a immagine (controlla con `get_cost: true`). `generate_image_batch` con una richiesta per posto foto,
  poi `jobs_wait`.
- **Ogni immagine nasce per un posto foto preciso** della ricetta (o della pagina interna costruita con lo stesso
  sistema): `aspect_ratio` = la proporzione del posto; soggetto = quello del cliente, mai quello del modello;
  stile = `ricetta.stile_foto.suffisso_prompt_en`, lo stesso per tutto il sito, così sembra un unico servizio
  fotografico; se il testo sta sopra la foto, scrivi nel prompt dove lasciare lo spazio vuoto. Ogni prompt finisce
  con `no text, no letters, no logos, no watermark`. **Mai** passare lo screenshot del modello a Higgsfield.
- Se un'immagine esce sbagliata (testo, mani o oggetti deformati, soggetto dove va il testo), riprova **una volta**
  con il prompt leggermente cambiato.
- Budget: **sito completo 8-12 immagini** (circa 22-33 crediti, tentativi compresi), **revisione 0-4**. Se i posti
  foto sono di più, riusa un'immagine con un ritaglio diverso. Se il saldo (`balance`) non basta, genera il minimo
  indispensabile (2-3) e scrivilo nelle note.
- **Lista scatti per il cliente**: una pagina in più, `foto-da-rifare.html`, salvata con lo stesso token ma **fuori
  dal menu**: per ogni immagine guida, l'immagine e accanto come rifarla uguale col telefono (cosa fotografare, da
  dove e quanto vicino, luce e ora, sfondo e oggetti, orientamento, dove lasciare spazio per il testo, 1-2 consigli
  pratici). Il link alla pagina va nella `descrizione` per il venditore e nelle note, con il link per caricare le
  foto (`officina/FOTO.md`). Quando il cliente carica le foto rifatte, un lavoro `revisione` le mette al posto di
  quelle generate senza cambiare il design.
- Onestà: un'immagine generata mostra il mondo del cliente, non viene spacciata per una sua foto reale
  di staff, clienti o recensioni. Persone sì, ma come atmosfera, mai con nomi o citazioni attribuite.
- Per un set coerente (lo stesso luogo in momenti diversi) genera prima l'immagine principale, poi le
  varianti passando il suo `job_id` in `medias` con ruolo `image_references`.
- Ogni risultato ha anche una versione `_min.webp` alla stessa risoluzione (nel campo `minUrl` di
  `show_generation_by_ids`, oppure aggiungendo `_min.webp` al posto di `.png`): usa quella, pesa molto meno.
- Nell'HTML usa **sempre il link Higgsfield `_min.webp` diretto** (le anteprime non ospitano file immagine),
  con `width`/`height` e `alt` in italiano. Puoi scaricare una copia in `/tmp/lavoro/<slug>/img/` solo per i
  controlli locali, se la rete lo permette.

## 5. Testi

**Metodo: `officina/COPYWRITING.md`**, da leggere per intero prima di scrivere: posizionamento, livello di
consapevolezza (la home di solito parla a chi conosce le soluzioni ma non il cliente; le pagine servizio, camera o
prodotto a chi sta decidendo), voce dei clienti, struttura, tre test dei titoli e controllo finale. Sotto, le regole
in più dei siti.

- Italiano naturale, il tono è quello del brief; di default sereno e professionale. Niente frasi da
  brochure ("a 360 gradi", "fare la differenza", "esperienza unica", "valorizzare").
- Il primo schermo dice cosa fa l'attività, dove, e porta all'azione del brief con un pulsante vero.
- Contenuti completi: servizi con descrizione, menu con piatti, camere, prodotti con nome e prezzo
  d'esempio. I dettagli che il brief non dà li scrivi come esempio plausibile e li elenchi nelle note
  come "da confermare con il cliente".
- **Mai inventare prove**: niente recensioni, citazioni, numeri di clienti, premi, loghi di partner,
  anni di attività. Niente dati di contatto inventati: telefono, email e indirizzo solo se nel brief,
  altrimenti segnaposto chiaro (es. "Telefono · da inserire") e pulsanti che puntano a `#contatti`.
- Settore sanitario: niente promesse di risultato, linguaggio sobrio.

## 6. Pubblicazione

Ogni sito è un insieme di file statici: `index.html` + altre pagine, `stile.css`, `script.js`.
Niente build, niente framework che richiedono compilazione: HTML, CSS e JavaScript puri, font da Google Fonts.

Obbligatorio in ogni pagina:
- Documento completo (`<!doctype html>`, `<html lang="it">`, `<head>` con charset) e
  `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- `figure { margin: 0; }` nel reset.
- `<meta name="robots" content="noindex, nofollow">`.
- Titolo, description e un'immagine Open Graph (la migliore del set, link Higgsfield).
- In fondo, piccolo: "Anteprima realizzata da PrismaPixel · prismapixel.it".
- Tutti i file nella stessa cartella, nomi solo `a-z 0-9 -` (es. `camera-vista-mare.html`), link relativi.

Poi pubblica con il servizio Anteprime come da **contratto, sezione 3**: una riga per file, token nuovo,
link `.../anteprima/<token>/index.html`.

## 7. Esito

Come da **contratto, sezione 4**, con `fonte = agente_sito_web`. Nelle note: direzione scelta, contenuti d'esempio
da confermare, cosa manca (checkout, contatti), controlli non eseguiti, crediti Higgsfield usati, durata, token.

## 8. Limiti

- Non pubblicare niente su GitHub e non modificare il repository: è pubblico e contiene solo istruzioni.
- Nelle anteprime solo i contenuti del sito, mai il brief, il profilo del cliente o le note per Vincenzo.
