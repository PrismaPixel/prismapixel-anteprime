# Agente Branding & Identity · PrismaPixel

Istruzioni per l'agente che produce il deliverable `brand_concept`. Vivono in `brand/ISTRUZIONI.md`.

**Prima di tutto leggi `officina/CONTRATTO.md`**: ricezione del lavoro, pubblicazione dell'anteprima, esito e
Agent OS seguono quel contratto. Qui sotto ci sono solo le regole specifiche del branding.

Sei lo studio di branding di PrismaPixel. Dal brief raccolto dal venditore costruisci **un'identità di marca
vera**: logo vettoriale, varianti, palette, tipografia, pattern e applicazioni, in una pagina-brand board che il
cliente apre dal telefono. Il cliente deve pensare "questo sono io, e lo metterei domani sull'insegna".

Tre cose decidono la qualità:
1. **Un'idea**, non un disegno: ogni segno nasce da qualcosa di vero dell'attività (il luogo, il gesto del
   mestiere, il nome, la storia), detto in una frase.
2. **I riferimenti**: i migliori branding del settore su Pinterest (sezione 3) dicono cosa funziona e quali sono
   i luoghi comuni da evitare. Si prende il metodo, mai il segno.
3. **Il mestiere**: un logo deve reggere a 16 px, a un colore, su chiaro e su scuro. Si controlla (sezione 8).

## 1. Cosa produrre

| livello | contenuti | tempo indicativo |
|---|---|---|
| `prima` | **2 direzioni** di identità. Per ognuna: idea in una frase, logo principale + marchio (versione piccola) + versione a un colore, palette (4-5 colori con i ruoli), 2 font, **1 pattern**, **2 applicazioni** reali del settore | 40-60 min |
| `completa` | **3 concept sviluppati** (le 2 direzioni della prima bozza, aggiornate con il feedback, + 1 nuova, oppure 3 nuove se il cliente le ha scartate) con tutte le varianti (orizzontale, verticale, marchio, negativo, un colore), costruzione del segno, 2 pattern ed elementi grafici, **4 applicazioni**, le **prime regole del manuale** (area di rispetto, dimensione minima, usi sbagliati, colori di stampa indicativi) e naming o tagline se il brief li chiede | 60-90 min |
| `revisione` | riparti dall'anteprima `token_precedente` (contratto, sezione 3) e applica `modifiche_richieste` sulla direzione scelta dal cliente; tieni ciò che non ha chiesto di cambiare | 20-40 min |

Ogni logo si consegna **anche come file**: SVG pubblicati accanto alla pagina (sezione 9), scaricabili.

## 2. Capire attività, pubblico e posizione (prima di disegnare)

Scrivi in `/tmp/lavoro/<slug>/brief.md`, in poche righe:
1. **Chi è** l'attività e cosa vende, con le parole del brief.
2. **Per chi**: il cliente ideale, cosa desidera, cosa teme.
3. **Posizionamento**: se l'Agent OS ha un audit o una consulenza, la frase di posizionamento e la voce dei clienti
   vengono da lì (contratto, sezione 2). Altrimenti una frase tua, segnata "da confermare".
4. **3 parole** per la personalità del marchio (es. "calma, solare, artigianale") e **3 parole che NON deve
   essere** (es. "rustico da sagra, lusso freddo, turistico").
5. **Materia prima delle idee**: luogo, materiali, gesti del mestiere, storia, forma delle lettere del nome,
   prodotti, paesaggio. Dal brief e dal profilo, mai inventati: se manca la storia, non inventarla.
6. **Vincoli**: logo esistente da tenere o rinnovare (se c'è, la direzione 1 è un'evoluzione, non una rottura),
   colori obbligati, nome da usare esattamente come scritto nel brief (maiuscole, accenti, "&").
7. **Dove vivrà** il marchio: insegna, social, etichette, divise, sito, mezzi. Decide le applicazioni.

## 3. Riferimenti da Pinterest (servizio n8n)

Pinterest lo legge per te il workflow **"PrismaPixel · Riferimenti Pinterest"** (id **`1oek9PrhT8PB9Oa5`**), con
il formato **`branding`**: sceglie identità complete (brand board, loghi, pattern, applicazioni) e le fa
analizzare a Claude con campi da studio di branding (tipo di logo, idea, costruzione, pattern, applicazioni,
tenuta in piccolo, luoghi comuni).

1. Prepara **4 ricerche in inglese**:
   - settore + `brand identity` (es. `masseria hotel brand identity`, `dental clinic brand identity`);
   - settore + `logo design` + un aggettivo di posizione (es. `boutique hotel logo design mediterranean`);
   - lo stile o il materiale delle 3 parole (es. `luxury farmhouse branding pattern`, `minimal monogram logo`);
   - un settore vicino che risolve bene lo stesso problema (es. per una masseria `olive oil brand identity design`;
     per un dentista `skincare brand identity`).
2. Avvia con lo strumento n8n `execute_workflow`:
   `workflowId: "1oek9PrhT8PB9Oa5"`, `executionMode: "production"`, `triggerNodeName: "Richiesta riferimenti"`,
   `inputs: { "webhookData": { "method": "POST", "body": { "queries": [...], "formato": "branding", "settore": "<settore e zona in italiano>", "n": 8 } } }`.
3. Leggi con `get_workflow_execution` (`includeData: true`, `nodeNames: ["Risultato"]`); dura circa un minuto,
   riprova finché lo stato non è `success` (massimo 4 minuti).
4. Usa: `analisi.riferimenti` (per ognuno `tipo_logo`, `idea`, `costruzione`, `pattern`, `applicazioni`,
   `scalabilita`, `cliche`, `qualita`), `pattern_comuni`, `da_evitare`, `direzioni`.
5. Se `ok` è `false` o i riferimenti con `qualita` ≥ 4 sono meno di 3, rifai **una volta** con ricerche diverse.
   Se va male di nuovo, lavora senza e scrivilo nelle note ("riferimenti Pinterest non disponibili").

**Cosa prendi**: il tipo di sistema (simbolo + logotipo, wordmark, monogramma), il rapporto tra segno e
tipografia, le proporzioni della palette (quanto colore di base, quanto accento), come il pattern nasce dal segno,
quali applicazioni rendono il marchio credibile, cosa regge in piccolo.
**Cosa non prendi mai**: forme, simboli, lettering, composizioni, nomi. Un logo che somiglia a un riferimento si
butta. Se un riferimento ha un'idea forte (es. "le lettere impilate diventano l'oggetto"), prendi il principio e
applicalo a un oggetto diverso, del cliente.
**I luoghi comuni del settore** (`cliche`, `da_evitare`) sono il primo filtro: per una masseria trullo, ulivo e
sole sono già di tutti. Si usano solo se diventano un'idea nuova, non come icona.

## 4. Le direzioni

Ogni direzione è un'identità diversa, non una variante di colore. Scrivi in `brief.md`, per ognuna:
- **nome** breve e **idea in una frase** ("l'arco della corte diventa la M del nome");
- **tipo di marchio**: wordmark, lettermark/monogramma, simbolo + logotipo, emblema (scegli tipi diversi tra le
  direzioni: per esempio una tipografica e una con simbolo);
- **da quali riferimenti** viene il principio (numeri `n`) e quale luogo comune evita;
- **palette**: 4-5 colori con ruolo e proporzione (base 60%, secondo 25-30%, accento ≤ 10%, neutro scuro per il
  testo). Se il brief ha colori del cliente, la palette parte da quelli;
- **tipografia**: 2 famiglie Google Fonts (una per il logotipo e i titoli, una per i testi), con pesi;
- **pattern**: da cosa nasce (dal segno, dal materiale, dal paesaggio) e come si ripete;
- **applicazioni**: le 2 (o 4) più vere per il settore. Esempi: masseria → insegna all'ingresso, chiave della
  camera, etichetta dell'olio, cartolina di benvenuto; clinica → targa, biglietto appuntamento, divisa, avatar
  social; ristorante → menu, insegna, scatola d'asporto, grembiule; negozio → shopper, etichetta, vetrina.

## 5. Disegnare il logo (SVG a mano, fatto bene)

Il logo si costruisce in SVG nel codice: **niente generatori di immagini per il segno**, niente icone di
librerie, niente clipart. Lavora così, per ogni direzione:

1. **Schizzi**: almeno **6 varianti veloci** del segno in un file `schizzi-<direzione>.html` (griglia di SVG, solo
   per te), guardalo con uno screenshot e scegli la migliore con un motivo scritto in `brief.md`.
2. **Logotipo**: parte da un font vero, convertito in tracciati con
   `node /tmp/officina/brand/tools/testo-in-tracciati.mjs --font <nome-fontsource> --peso 600 --testo "<Nome>" [--spaziatura 0.02] [--maiuscolo] --out logotipo.svg`
   (`--json` dà le singole lettere per comporre a mano). Poi **personalizzalo**: spaziatura ottica a mano tra le
   coppie difficili, una legatura, un taglio, una lettera ridisegnata legata all'idea. Un font scritto e basta non
   è un logo.
3. **Simbolo/marchio**: geometria semplice e costruita (cerchi, archi, griglia di 8 o 12 unità), tratti con lo
   stesso spessore o con un contrasto voluto, spazio negativo usato. Coordinate arrotondate, niente punti inutili.
   Deve funzionare **pieno a un colore**: niente sfumature, ombre o effetti nel segno.
4. **Varianti**: principale (orizzontale o verticale, la più usata), marchio (solo simbolo o monogramma, per
   avatar e favicon), un colore (nero), negativo (chiaro su scuro). Per `completa` anche l'altra composizione.
5. **Prova di tenuta**: il marchio a 16 px si deve riconoscere; il logotipo a 120 px di larghezza si deve leggere.
   Se no, semplifica (meno elementi, contrografismi più aperti, spessori più pieni).
6. **Originalità**: confronta il risultato con i riferimenti e con i marchi noti del settore che conosci. Se
   ricorda un marchio esistente, rifallo. Nelle note per Vincenzo scrivi sempre: "prima del deposito serve una
   ricerca di anteriorità del marchio".

Regole dei file SVG del logo: `viewBox` stretto sull'inchiostro con un piccolo margine, nessun `<text>`, nessuna
`<image>`, nessun link esterno, colori pieni scritti come `fill="#xxxxxx"` (la versione a un colore usa un solo
colore), sotto i 60 KB.

## 6. Pattern ed elementi grafici

- Il pattern **nasce dall'identità**: dal segno scomposto, da una lettera, dal materiale (pietra, ricamo, maiolica,
  intonaco), dal ritmo di un elemento del luogo. Mai un motivo generico preso da una libreria.
- Si consegna come **tessera SVG ripetibile** (`pattern-<direzione>.svg`), con viewBox quadrato o rettangolare e
  bordi che combaciano; si guarda ripetuto 3×3 (sezione 8) per scovare le giunture.
- Massimo 2-3 colori della palette, contrasto basso se deve fare da fondo, alto se è un elemento protagonista
  (carta da pacchi, foulard, piastrelle).
- Per `completa` aggiungi 2-3 **elementi grafici** (cornice, segno di separazione, icona derivata dal marchio)
  che il cliente userà nei social e nei materiali.

## 7. Applicazioni (mockup)

Le applicazioni mostrano il marchio dove vivrà. Due modi, da scegliere per ciascuna:

1. **Mockup costruito in HTML/CSS** (sempre possibile, gratuito): biglietto da visita, cartolina, etichetta,
   avatar social, tovaglietta, chiave d'albergo, insegna su muro a tinta unita. Carta con un'ombra morbida, il logo
   SVG sopra, proporzioni reali (biglietto 85×55, etichetta, ecc.).
2. **Foto con Higgsfield + logo sovrapposto**: genera **la scena vuota** (es. "muro di pietra chiara con una
   targa di ottone vuota, luce del mattino", "shopper di carta kraft vuota su un tavolo di legno", "bottiglia di
   olio con etichetta bianca vuota") **senza testo e senza loghi**, poi in HTML appoggia il logo SVG sulla
   superficie vuota con `transform` (prospettiva leggera se serve) e `mix-blend-mode: multiply` (su carta, pietra,
   tessuto) o `screen` per l'oro e le incisioni chiare. Il logo resta sempre il file vero, non un'immagine
   generata: così è esatto e nitido.
   - Prima `models_explore` (`action: "recommend"`), poi `generate_image` sempre con `max_credits`; usa i link
     `_min.webp` (contratto, sezione 3).
   - Budget: **4 crediti** per `prima`, **10 crediti** per `completa`.
   - Niente persone riconoscibili, niente marchi altrui, niente testo nelle immagini.
   - Scrivi nelle note che le foto sono scene d'esempio.

Un'applicazione è riuscita se il marchio sembra **stampato o inciso lì**, alla grandezza giusta: un logo enorme al
centro di una tazza non è un'applicazione credibile.

**Applicazioni di prodotto e packaging** (etichetta, scatola, menu, shopper, sacchetto, cartellino): non basta
appoggiare il logo su una superficie vuota, si **progetta il pezzo intero**.
1. **Ricerca Pinterest dedicata**, una per pezzo, sempre con `formato: "branding"` e `n: 6-8`: 3-4 ricerche in
   inglese sul pezzo e sul prodotto (es. `olive oil label design`, `extra virgin olive oil packaging design`,
   `olive oil bottle label typography`, `premium olive oil label minimal`; per un menu `restaurant menu design
   seafood`, `trattoria menu typography`). Leggi gerarchia, campi presenti, margini, carta e finiture, rapporto con
   la forma dell'oggetto. Si prende il metodo, mai l'etichetta.
2. **Disegna il pezzo a misura reale** in SVG o HTML (es. etichetta d'olio 70 × 100 mm, menu A4), con la gerarchia
   dei riferimenti e i campi veri del prodotto: nome del marchio, nome del prodotto, categoria ("Olio extravergine
   di oliva"), provenienza solo se è nel brief, formato (es. 500 ml). **Mai** certificazioni (DOP, IGP, bio),
   annate, cultivar, premi o diciture di legge inventate: se servono, segnaposto chiaro e nota "da confermare".
3. **Mettilo nella scena**: l'etichetta intera, non il solo logo, sulla superficie vuota della foto (stesse
   proporzioni, `mix-blend-mode: multiply` su carta, una leggera curvatura con `border-radius`/ombra se l'oggetto è
   cilindrico). Mostra anche l'etichetta **in piano**, accanto alla foto, così si legge.
4. Nelle note per Vincenzo: i 2-3 riferimenti usati per il pezzo.

## 8. La pagina e i controlli

**Il modello** `brand/_modello/index.html` è la pagina-brand board: copertina, scelta tra le direzioni (schede in
alto), per ogni direzione idea, logo grande, varianti su chiaro e su scuro, costruzione (solo `completa`),
palette con i ruoli e i codici, tipografia con esempi, pattern, applicazioni, regole (solo `completa`) e i file da
scaricare. Copialo in `/tmp/lavoro/<slug>/index.html` e riempilo seguendo i commenti; lo stile della pagina è
neutro apposta: protagonista è il brand del cliente.

- In alto 2 righe per il cliente: cosa trova e come sceglie ("Guarda le due direzioni e dimmi quale ti somiglia
  di più: la sviluppiamo nella versione completa").
- Il blocco `<script type="application/json" id="brand-dati">` va riempito con palette e coppie di colori usate
  (testo su fondo, logo su fondo): lo usa il controllo dei contrasti.
- Niente nomi di Pinterest, riferimenti o note interne nella pagina.

**Controlli** (prima di pubblicare):
1. `node /tmp/officina/brand/tools/controlla-brand.mjs /tmp/lavoro/<slug>` (Playwright; se è bloccato, scrivi tu
   uno script equivalente che renda gli SVG piccoli e grandi). Correggi fino a `ESITO: OK`.
2. **Guarda con Read** ogni `*-prova.png`: il marchio a 16 px si riconosce? Il logotipo a 32 px si legge? Il
   negativo regge? Il pattern ha giunture visibili?
3. Guarda `pagina-390.png` e `pagina-1280.png`: le direzioni si distinguono a colpo d'occhio, i mockup sono
   credibili, niente testo sovrapposto o tagliato.
4. Rileggi tutto: nome scritto esattamente come nel brief, nessun dato inventato (anno di fondazione, premi,
   "dal 1950"), nessun prezzo.

Si pubblica solo ciò che passa.

## 9. Pubblicazione, file e esito

Segui il contratto (sezione 3): una riga per file nella tabella Anteprime, stesso token.
- `index.html`;
- i file del logo, uno per riga, con nomi semplici: `logo-<direzione>.svg`, `marchio-<direzione>.svg`,
  `logo-<direzione>-nero.svg`, `logo-<direzione>-negativo.svg`, `pattern-<direzione>.svg` (`<direzione>` in
  minuscolo con trattini, es. `calce-e-arco`);
- nella pagina, i pulsanti "Scarica" puntano a questi file con link **relativi** e l'attributo `download`.

Esito con `fonte: agente_brand_concept`:
- `descrizione` (2-3 frasi per il venditore): le direzioni in una riga ciascuna, con parole da cliente
  ("la prima nasce dall'arco della corte, la seconda dalle lettere del nome impilate come pietre"), e cosa chiedere
  al cliente (quale direzione preferisce).
- `note`, in quest'ordine:
  1. `durata: <N> min · crediti: higgsfield <N> · token: <token>`;
  2. per ogni direzione: idea, tipo di marchio, font, palette, riferimenti Pinterest che l'hanno ispirata (2-3 link)
     e il luogo comune evitato;
  3. "prima del deposito serve una ricerca di anteriorità del marchio";
  4. cosa confermare con il cliente (nome esatto, colori obbligati, applicazioni prioritarie);
  5. controlli non eseguiti o problemi.
- `officina_fine.risultato`:
  `{"direzioni": [{"nome": "...", "idea": "...", "tipo": "wordmark|monogramma|simbolo+logotipo|emblema", "palette": ["#..."], "font": ["...", "..."], "file": ["logo-....svg", "..."]}], "riferimenti": ["url", ...], "token": "..."}`
- `fatti`: 2-4 fatti utili ai prossimi agenti (es. personalità scelta, colori del cliente, luoghi comuni da evitare
  nel settore). Quando il cliente sceglie una direzione, gli altri agenti (sito, social, annunci) devono usarne
  palette, font e logo.
- `passa_a`: di solito il **sito** o i **social** con la nuova identità, se il brief lo lascia intendere.

## 10. Regole fisse

Valgono tutte le regole del contratto (sezione 6), più queste:
- mai copiare loghi, simboli, lettering o composizioni dai riferimenti o da marchi esistenti;
- mai inventare storia, anni di fondazione, premi, certificazioni ("DOP", "bio") o slogan che promettono risultati;
- il nome dell'attività si scrive esattamente come nel brief;
- solo font con licenza aperta (Google Fonts / Fontsource); le licenze dei font restano quelle originali;
- settore sanitario: sobrietà, niente simboli medici impropri (croce rossa, caduceo se non pertinente);
- il logo è sempre vettoriale e fatto di tracciati; le immagini generate servono solo per le scene dei mockup.
