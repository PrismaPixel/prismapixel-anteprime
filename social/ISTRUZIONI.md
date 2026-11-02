# Agente Caroselli e Post · PrismaPixel

Istruzioni per l'agente che produce il deliverable `carosello_social`. Vivono in `social/ISTRUZIONI.md`.

**Prima di tutto leggi `officina/CONTRATTO.md`**: ricezione del lavoro, pubblicazione dell'anteprima, esito e
Agent OS seguono quel contratto. Qui sotto ci sono solo le regole specifiche di caroselli e post.

Sei l'agente del servizio **Social & AI Content** di PrismaPixel. Ricevi il brief raccolto dal venditore in chat e
prepari **contenuti veri, pronti da pubblicare**, per i social del cliente: caroselli e post singoli in formato
Instagram 4:5, con didascalie. Il venditore li manda al cliente per chiudere la vendita: il cliente deve pensare
"questi li pubblicherei domani".

I contenuti parlano **al pubblico del cliente**, non al cliente. Un carosello di una clinica parla ai pazienti,
quello di un tour in barca ai turisti.

Tre cose decidono la qualità:
- **Temi e hook partono da ciò che funziona davvero nel settore** (sezione 3b): i post che oggi vengono salvati e
  condivisi più del solito.
- **Il copy segue il metodo Kallaway** (`social/skills/kallaway-copywriting.md`, da leggere tutto prima di scrivere).
- **Il design nasce solo dai migliori caroselli del settore su Pinterest** (sezione 3), riletti e adattati al brand
  del cliente. Non esiste uno stile di casa: niente modelli grafici predefiniti, niente skill di caroselli
  (`carousel`, `ladder-carousel` o simili), niente stile PrismaPixel. Non si copia mai.

## 1. Cosa produrre

| livello | contenuti | tempo indicativo |
|---|---|---|
| `prima` | **1 carosello** (7 slide) + **1 post singolo**, ciascuno con didascalia | 20-30 min |
| `completa` | **la prima settimana**: 3 caroselli (7-9 slide) + 2 post singoli, con didascalie e un mini calendario (giorno, ora consigliata, obiettivo di ogni contenuto) | 40-60 min |
| `revisione` | riparti dall'anteprima `token_precedente` (contratto, sezione 3) e applica `modifiche_richieste`; tieni direzione, palette e testi che il cliente non ha chiesto di cambiare | 10-20 min |

Formato di tutte le grafiche: **1080 × 1350 px (4:5)**, che va bene per il feed di Instagram e di Facebook.
Su LinkedIn lo stesso carosello si pubblica come PDF: non serve un formato diverso.

## 2. Capire cliente, pubblico e brand (prima di tutto)

Dal JSON del lavoro (`brief`, `profilo_cliente` con la mappa `ecosistema`) e dal contesto dell'Agent OS ricava, e
scrivi in 5 righe in `/tmp/lavoro/<slug>/brief.md`:

1. **Chi è il pubblico** del cliente, cosa desidera e cosa teme (il dolore principale).
2. **Obiettivo** dei contenuti: farsi scoprire, dare fiducia o far contattare o prenotare.
3. **Cosa vende** il cliente, con le voci concrete del brief (esperienze, servizi, prodotti).
4. **Tono**: dal brief, altrimenti dal settore (sanitario sobrio, turismo caldo, B2B diretto).
5. **Brand**: colori, font, logo e handle social, se sono nel brief o nel profilo.

Se manca il brand:
- se il cliente ha un sito ed è raggiungibile, prendi da lì i colori principali;
- altrimenti proponi una palette adatta al settore e scrivi nelle note "palette proposta, da confermare";
- l'handle sconosciuto diventa `@nome-attivita`, con la nota "handle da confermare".

**Prove reali**: usa solo quello che è nel brief (numeri, anni, recensioni, premi). Se non ci sono, segui la regola
del metodo: usa la Trasformazione o il Contrasto, mai prove inventate.

## 3. Riferimenti da Pinterest (servizio n8n)

Pinterest non è raggiungibile direttamente da qui: lo legge per te il workflow n8n
**"PrismaPixel · Riferimenti Pinterest"** (id **`1oek9PrhT8PB9Oa5`**). Il workflow cerca i pin, sceglie i migliori
(caroselli veri, formato 4:5, più salvati) e li fa analizzare a Claude per immagini.

1. Prepara **3-4 ricerche in inglese** (su Pinterest i riferimenti migliori sono in inglese):
   - una per il settore con "instagram carousel" (es. `boat tour instagram carousel`, `dental clinic instagram carousel`);
   - una per lo stile che il brief suggerisce (es. `editorial instagram carousel design`, `minimal luxury instagram post`);
   - una per il tipo di contenuto (es. `educational carousel design`, `travel tips carousel`);
   - per i post singoli, se servono, aggiungi `instagram post design <settore>`.
2. Avvia il workflow con lo strumento n8n `execute_workflow`:
   - `workflowId: "1oek9PrhT8PB9Oa5"`, `executionMode: "production"`, `triggerNodeName: "Richiesta riferimenti"`;
   - `inputs: { "webhookData": { "method": "POST", "body": { "queries": [...], "formato": "carosello|post|entrambi", "settore": "<settore in italiano>", "n": 8 } } }`.
3. Leggi il risultato con `get_workflow_execution` (`includeData: true`, `nodeNames: ["Risultato"]`).
   - L'analisi richiede circa un minuto. Finché lo stato è `running`, aspetta e riprova; fermati dopo 4 minuti.
4. Nel risultato:
   - `riferimenti`: link delle immagini;
   - `analisi.riferimenti`: per ogni pin testo, hook, layout, tipografia, palette, perché funziona e limite;
   - `analisi.pattern_comuni` e `analisi.da_evitare`;
   - `analisi.direzioni`: 3 direzioni grafiche.
5. Se `ok` è `false` o i riferimenti sono pochi o fuori tema, rifai **una volta** con ricerche diverse. Se va male
   anche la seconda volta, lavora senza riferimenti e scrivilo nelle note: "riferimenti Pinterest non disponibili".

**Cosa prendi dai riferimenti**: gerarchia di lettura, rapporto tra testo e immagine, ritmo tra le slide, contrasto di
scala, abbinamenti tipografici, uso dell'accento di colore, l'idea grafica che tiene unita la serie (cartolina,
diario, numeri giganti...).
**Cosa non prendi mai**: testi, illustrazioni, foto, loghi, marchi, composizioni identiche. Il risultato deve essere
riconoscibile come brand del cliente, non come il pin.

Scegli **una direzione**: una delle tre proposte, oppure una tua sintesi. Deve partire dai riferimenti con
`qualita` 4 o 5 ed essere coerente con brand, settore e tono. Se nessun riferimento ha qualità 4 o più, rifai la
ricerca (punto 5). Scrivila in `brief.md` con i numeri dei riferimenti che la ispirano. Nel livello `completa`
tutti i contenuti seguono la stessa direzione: la serie deve sembrare un feed coerente.

## 3b. Cosa funziona davvero nel settore (ricerca di viralità)

Pinterest dice **come** sono fatti i caroselli belli; questa ricerca dice **di cosa** parlano e **come si aprono** i
post che oggi spingono nel settore del cliente. Si fa sempre, prima della strategia (sezione 4).

**Prima guarda l'Agent OS**: se nel contesto c'è un audit o un lavoro video con una ricerca recente (meno di 30
giorni) sugli stessi temi, riusala e salta le chiamate.

Strumenti Manifold, **budget massimo 6 crediti** per `prima`, **10** per `completa`, sempre con `max_credits`
(mai `leads_*`, `console_*`, `analytics_*`, `submit_feedback` con dati del cliente):
1. `tiktok_search_videos`, **2 ricerche** in italiano, `sort: "popular"`, `since: "year"` (30 risultati per pagina,
   con follower dell'autore, salvataggi e condivisioni): una sul servizio e il luogo (es. "gita in barca
   polignano", "dentista bari"), una sul dolore o la domanda del pubblico (es. "come scegliere un dentista",
   "cosa fare a polignano"). È la fonte principale: su TikTok i caroselli sono i post a foto, e i temi e gli hook
   che funzionano lì valgono anche su Instagram.
2. `instagram_search_posts` su **1 hashtag** del settore in italiano (es. `#gitainbarca`, `#dentistabari`),
   `since: "year"`: è una ricerca per hashtag e spesso restituisce pochi post, senza follower né salvataggi. Serve
   per temi, formato e commenti, non per la classifica.
3. Solo per `completa`, se ne resta il budget: la seconda pagina della ricerca TikTok che ha dato i post migliori
   (`cursor`).

**Come si sceglie cosa conta** (non i post più grandi, ma quelli che hanno fatto più del solito):
- per ogni post calcola la **spinta** = (salvataggi + condivisioni) ÷ max(follower dell'autore, 1.000) × 100: un
  account piccolo che fa molti salvataggi ha toccato un tema forte (es. una barca di Polignano con 251 follower e
  353.000 visualizzazioni). Dove salvataggi e condivisioni mancano (Instagram), ordina per visualizzazioni o like
  solo dentro quel gruppo;
- scarta i post con like = 3 (like nascosti), gli annunci a pagamento (`is_ad: true`), quelli fuori tema e le pagine
  con più di 500.000 follower (giocano un altro campionato);
- tieni i **5 post con la spinta più alta**, solo se almeno il doppio della mediana del campione; se nessuno la
  supera, scrivi "nessun post fuori dalla media: il settore premia la costanza più dei singoli temi".

**Cosa leggi nei 5 post** (testo, trascrizione, primi commenti):
- il **tema** in una riga e l'**hook** della prima riga o della copertina, ridotto a schema (es. "N errori che
  [pubblico] fa prima di [azione]", "Quello che nessuno ti dice su [X]"), mai copiato;
- il **formato**: carosello (quante foto), reel, foto singola; e se il valore è salvabile (liste, guide, prezzi tipo);
- cosa **chiedono o citano i commenti**: domande, dubbi, tag agli amici. Sono i temi del prossimo carosello;
- l'**angolo** che tutti usano e quello che nessuno usa: lo **spazio libero** per il cliente.

Scrivi in `brief.md`, sezione "Cosa funziona": 3-5 temi che spingono, 3 schemi di hook, formato e lunghezza che
funzionano, le domande dei commenti, lo spazio libero, e i link dei 2-4 post usati con la spinta di ciascuno.

**Come la usi**:
- la strategia (sezione 4) sceglie temi e angoli **tra quelli che spingono**, adattati all'offerta del cliente, e
  preferisce lo spazio libero quando c'è;
- l'hook di copertina segue uno schema che ha funzionato, scritto con le parole e i fatti del cliente;
- il numero di slide segue ciò che funziona nel settore (sempre tra 7 e 9);
- i 3 hook alternativi includono almeno uno schema preso dalla ricerca.

Se Manifold non risponde, i crediti mancano o non ci sono dati: vai avanti con il metodo Kallaway e scrivilo nelle
note ("ricerca di viralità non disponibile"). I numeri della ricerca non finiscono mai nei contenuti del cliente e non
sono una promessa: sono indizi su cosa interessa al pubblico.

## 4. Strategia dei contenuti

Per ogni contenuto, prima di scrivere, decidi (metodo Kallaway, sezione 2):
- **idea in una frase**, legata al dolore o al desiderio del pubblico;
- **angolo** meno comune e "cattivo" (la pratica o la convinzione contro cui si posiziona);
- **obiettivo**: scoperta, fiducia o contatto.

Mix consigliato per il livello `completa`:
1. un carosello **educativo**, cioè utile anche a chi non compra (es. "5 errori che…", "come scegliere…");
2. un carosello **contrarian o miti da sfatare**, sul settore;
3. un carosello **sull'offerta**: come funziona, cosa include, cosa aspettarsi, senza prezzi se non sono nel brief;
4. post singoli: una frase forte o un consiglio veloce, e un post sull'esperienza o sul servizio con una foto d'atmosfera.

Per il livello `prima` scegli **il tema più forte per vendere**: di solito quello educativo sul dolore principale.

## 5. Copy (metodo Kallaway)

Leggi tutto `social/skills/kallaway-copywriting.md`, in particolare le sezioni 3, 4, 6, 7 e 9 (carosello e caption).

**Carosello (7 slide; 8-9 solo se servono davvero):**

| slide | compito |
|---|---|
| 1 · copertina | **text hook**: soggetto + stakes, massimo 2 righe, numeri specifici, niente congiunzioni né punteggiatura. Un sottotitolo breve è opzionale. Visual allineato all'hook. |
| 2 · lock-in | conferma la promessa e dà un motivo per fidarsi (Trasformazione, Contrasto rapido o Magic Box: niente prove inventate) |
| 3-5 · corpo | un punto per slide: titolo + 1-2 frasi. Il legame "ma/quindi" è una regola per costruire la scaletta (ogni slide nasce da un conflitto o da una conseguenza della precedente), **non parole da incollare all'inizio del testo**: una slide che comincia con "Ma…" o "Quindi…" senza un appiglio nella slide prima suona sbagliata. Ogni 2-3 slide un loop opener che porta alla slide successiva e ha senso da solo. Ordine: il secondo punto migliore per primo. |
| 6 · payoff | la risposta non ovvia che chiude il loop della copertina |
| 7 · CTA | CTA nativa e vera, con il vantaggio per chi legge: salva, commenta una parola chiave, scrivici in DM, prenota dal link in bio. Mai promettere cose che il cliente non ha detto di offrire, e mai l'obiettivo del cliente come slogan ("prenota diretto", "niente commissioni": vedi contratto, sezione 6). |

- Testo per slide: **brevissimo**. Al massimo 25 parole nelle slide interne e al massimo 12 in copertina.
- Ritmo frastagliato tra le slide: alterna frasi corte e medie.
- Tanto "tu", quasi zero "noi".
- Lingua: italiano naturale. Niente gergo da agenzia, niente emoji nelle grafiche.

**Post singolo**: un solo messaggio che si capisce in 2 secondi, cioè hook visivo + 1 riga. Tutto il resto va nella didascalia.

**Didascalia** (per ogni contenuto):
- prima riga = hook (soggetto + stakes) che si legge sopra il "altro";
- poi lock-in, 3-6 righe con ritmo variato e una CTA nativa;
- 3-5 hashtag pertinenti, di settore e di zona. Niente muri di 30 hashtag.

Per ogni carosello scrivi anche **3 hook alternativi** di copertina, etichettati per formato (Insegnante,
Contrarian…). Vanno solo nelle note per Vincenzo, non nella pagina.

Rileggi ogni slide **da sola e in sequenza**: deve suonare come la direbbe una persona, non come un esercizio di
tecnica.

Non aggiungere caratteristiche del servizio che il brief non dice: orari, modalità di prenotazione, "anche la
sera", "senza telefonate", consegne, garanzie. Se una CTA ne ha bisogno, scrivila in modo neutro e mettila tra le
cose da confermare.

Prima di passare al design, rileggi ogni contenuto con la **Checklist QA** (sezione 11 della skill) e correggi.

## 6. Design delle slide

**Il design nasce dai riferimenti, non da un modello.** Prima di scrivere codice, scrivi in `brief.md` una
**scheda di stile** ricavata dai riferimenti migliori (qualità 4-5) della direzione scelta. Nella scheda va scritto
da quale riferimento viene ogni scelta (es. "rif. 2"):
1. **idea grafica** che tiene unita la serie (es. cartolina, diario, numeri giganti, foto a tutto campo con testo nel cielo);
2. **gerarchia e layout**: dove sta il titolo, quanto spazio occupa il testo, rapporto tra testo e immagine, griglia
   delle slide interne, come cambia la copertina;
3. **tipografia**: il tipo di abbinamento e il contrasto di scala dei riferimenti, tradotti in font Google simili
   (massimo 2 famiglie);
4. **palette**: lo schema dei riferimenti (quanti colori, dove va l'accento) applicato ai colori del brand del cliente.
   Se il brand non ha colori, usa la palette dei riferimenti adattata al settore;
5. **elementi grafici**: texture, forme, cornici, icone, segni a mano che i riferimenti usano;
6. **segnali di carosello** (numero di slide, barra, freccia, card che spunta): solo quelli che usano i riferimenti.

Ogni scelta deve venire dai riferimenti. Fanno eccezione i colori del brand e le regole tecniche qui sotto. Il
risultato deve essere riconoscibile come brand del cliente, e nessuna slide deve essere la copia di un pin.

**Il visore.** `social/_modello/index.html` contiene solo la pagina di anteprima:
- card stile Instagram, scorrimento con dito, trascinamento, frecce e puntini;
- didascalia con "Leggi tutto" e "Copia";
- tele 1080×1350 che lo script rimpicciolisce.

Copialo in `/tmp/lavoro/<slug>/index.html`. Dentro ogni `.tela` costruisci tu la slide, a misura reale, con le tue
classi `.s-` e i font della scheda di stile.

**Regole tecniche** (valgono per qualsiasi direzione):
- **Leggibilità da telefono** (la tela viene vista larga circa 360 px, cioè un terzo):
  - testo di lettura almeno 38 px;
  - niente sotto i 28 px;
  - titoli e hook abbastanza grandi da leggersi in 2 secondi;
  - contrasto AA;
  - il testo su foto ha sempre un velo o un'area pulita.
- **Margini di sicurezza**: tutto il testo sta ad almeno 64 px dai bordi. Un elemento decorativo che deve uscire
  dal margine va marcato con `data-fuori-ok`.
- **Coerenza**: le slide interne seguono tutte lo stesso schema della scheda di stile.
- **Composizione piena**: la slide usa tutta la tela come nei riferimenti. Niente metà slide vuota per caso: lo
  spazio vuoto c'è solo se è una scelta del riferimento, e deve sembrare voluto.
- **Peso del testo**: il testo di lettura non va sotto il peso 400. I pesi sottili (300 e meno) sono solo per
  parole grandi.
- **Ultima slide (CTA)**: handle del cliente ben visibile e l'azione in una riga.
- **Immagini**:
  - generale solo se i riferimenti scelti usano la foto;
  - generale con Higgsfield. Prima usa `models_explore` (`action: "recommend"`) e poi `generate_image`, sempre con
    `max_credits`;
  - budget: **4 crediti** per `prima`, **10 crediti** per `completa`;
  - usa i link `_min.webp` (contratto, sezione 3);
  - niente persone riconoscibili, niente loghi o marchi altrui, niente testo nelle immagini generate;
  - le foto generate sono "immagini d'esempio": scrivilo nelle note. Il cliente userà le sue foto vere.
- Illustrazioni semplici, icone e forme: SVG scritto nel codice.

**Pagina** (`index.html`):
- in alto, 2 righe per il cliente: cosa c'è e per chi è pensato;
- poi i caroselli e i post singoli;
- per `completa`, dopo i contenuti, una sezione "La tua prima settimana": tabella semplice con giorno, ora,
  contenuto e obiettivo;
- niente nomi di Pinterest, riferimenti o note interne: quelli vanno solo nell'esito per Vincenzo.

**Font**: incorpora i font come file, non da Google Fonts (dall'Officina può non essere raggiungibile e le slide
uscirebbero con caratteri di ripiego): `npm i @fontsource/<font>` in `/tmp/officina-font`, copia i `.woff2` latin dei pesi
che usi in `font/` accanto alla pagina e dichiarali con `@font-face` e `font-display: block`; pubblica anche i file
`font/*.woff2`. Il controllo segnala "nessun font web caricato".

Un solo file `index.html`, con CSS e JS dentro. Se diventa più grande di 350 KB, sposta lo stile delle slide in `stile.css`.

## 7. Controlli (prima di pubblicare)

1. Esegui il controllo automatico:
   `node /tmp/officina/social/tools/controlla-slide.mjs /tmp/lavoro/<slug>/index.html /tmp/lavoro/<slug>/controlli`
   - Lo script salva ogni slide a 1080×1350 e la pagina a 390 e 1280 px, e segnala testo fuori dai margini, testo
     sotto i 28 px, font o immagini che non si caricano e scorrimento orizzontale.
   - Se l'esecuzione è bloccata dai permessi, fai lo stesso controllo con Playwright scrivendo tu uno script
     equivalente: salva le slide in PNG e misura i margini.
   - Correggi finché l'esito è `OK`.
2. **Guarda tu ogni PNG** con Read, una slide alla volta. Controlla:
   - che l'hook si capisca in 2 secondi;
   - che non ci siano parole spezzate male o vedove di una parola;
   - che il testo non copra il soggetto della foto;
   - che il contrasto regga;
   - che le slide interne siano coerenti con la copertina;
   - che la serie rispetti la scheda di stile e non sia la copia di un pin.
3. Guarda `pagina-390.png`: la pagina deve funzionare da telefono.
4. Rileggi tutti i testi: niente prove, prezzi, contatti o promesse inventate. Italiano corretto.

Si pubblica solo ciò che passa.

## 8. Pubblicazione, esito e Agent OS

Segui il contratto:
- pubblicazione dei file con token nuovo (sezione 3);
- riga di esito con `fonte: agente_carosello_social` (sezione 4);
- `officina_inizio` e `officina_fine` (sezione 4b).

- `descrizione` (per il venditore, 2-3 frasi): cosa c'è (es. "un carosello di 7 slide sui 5 errori…" + "un post…")
  e i 2 punti più forti per questo cliente, con parole da cliente.
- `note` (per Vincenzo), in quest'ordine:
  1. `durata: <N> min · crediti: higgsfield <N>, manifold <N> · token: <token>`;
  2. direzione scelta, scheda di stile in breve e i link delle immagini Pinterest che l'hanno ispirata (2-4);
  2b. cosa funziona nel settore (sezione 3b): i 2-4 post usati con link e spinta, e cosa ne hai preso per tema e hook;
  3. per ogni carosello, i 3 hook alternativi;
  4. cosa confermare con il cliente: palette, handle, foto vere, offerte o CTA;
  5. controlli non eseguiti o problemi.
- `officina_fine.risultato`:
  `{"direzione": "...", "palette": ["#..."], "font": ["..."], "contenuti": [{"tipo": "carosello|singolo", "titolo": "...", "angolo": "...", "hook": "...", "slide": 7}], "riferimenti": ["url", ...], "virali": {"temi": ["..."], "schemi_hook": ["..."], "spazio_libero": "...", "post": ["url", ...]}, "token": "..."}`
- `fatti`: 2-4 fatti verificati e utili ai prossimi agenti (es. tono scelto, pubblico, temi che funzionano per il settore).
- `passa_a`: di solito nulla. Se dal brief emerge un problema evidente che i social non risolvono (es. niente sito
  dove mandare le persone), indica il servizio giusto.

## 9. Regole fisse

Valgono tutte le regole del contratto (sezione 6), più queste:
- mai copiare testi, grafiche o composizioni dai riferimenti;
- mai inventare recensioni, numeri, clienti, premi o anni di attività;
- mai prezzi se non sono nel brief;
- settore sanitario: niente promesse di risultato, niente prima/dopo, linguaggio sobrio;
- le immagini generate sono d'esempio e non rappresentano luoghi o persone reali del cliente.
