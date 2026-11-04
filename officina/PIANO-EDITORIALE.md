# Piano editoriale · PrismaPixel

Vale per **tutti gli agenti che producono contenuti social**: `carosello_social` (caroselli e post),
`script_video` (copioni da girare), `video_ai` (video generati) e `video_montaggio` (girato del cliente montato).
Si legge dopo `officina/CONTRATTO.md` e prima delle istruzioni del servizio.

**Regola**: nessun contenuto nasce da solo. Ogni carosello, post, copione o video occupa uno **spazio del piano
editoriale** del cliente: una rubrica, un obiettivo, un formato, una CTA. Il piano decide *di cosa* parlare e *perché*;
le istruzioni del servizio decidono *come* farlo.

## 1. Dove sta il piano

Il piano è un oggetto JSON salvato nel risultato del lavoro che l'ha creato o aggiornato
(`officina_fine.risultato.piano_editoriale`). All'inizio di ogni lavoro cercalo nel contesto dell'Agent OS:
`contesto.cliente.lavori[].risultato.piano_editoriale`, **il più recente**. Se la consulenza strategica (`roadmap`)
ha un calendario o delle rubriche, il piano parte da lì.

## 2. Creare, aggiornare o seguire

| situazione | cosa fai |
|---|---|
| il cliente non ha un piano | **lo crei** (sezione 3) prima di qualsiasi contenuto, e lo mostri nella pagina |
| il piano ha più di 90 giorni, oppure si entra in una nuova fase di `stagioni`, oppure obiettivo, offerta, pubblico o maturità dell'account sono cambiati, oppure `modifiche_richieste` lo tocca | **lo aggiorni**: tieni ciò che funziona, cambi rubriche o calendario |
| c'è un piano valido | **lo segui**: prendi i primi spazi `da_fare` del tuo formato e non lo rifai |
| `revisione` | non tocchi il piano: correggi solo i contenuti |

Il piano lo crea **il primo agente social** che lavora per il cliente, qualunque sia. Per la prima bozza basta il
**piano base**: rubriche, mix e le prime 2 settimane di calendario. La versione completa ha 4 settimane.

## 2b. Da cosa nasce (è su misura, non un modello)

Prima di scrivere il piano raccogli in `brief.md`, dal contesto dell'Agent OS e dal JSON del lavoro:
- **obiettivo** e **pubblico** (brief, `profilo_cliente`, audit);
- **esigenze social** in `profilo_cliente.social`, raccolte dal venditore: `lingue` del pubblico, `stagione_forte` e
  `stagione_bassa`, `da_mostrare` e `da_non_mostrare`, `volto` (chi può comparire), `momenti` (eventi, aperture,
  novità), `contenuti_al_mese`;
- **maturità dell'account** (sezione 3, mix): dai `contatti` del cliente e, se serve, con `instagram_get_profile` o
  `tiktok_get_profile` (1 credito, rientra nel budget della ricerca);
- **settore** e **offerta**: cosa vende, cosa si sceglie in anticipo e cosa d'impulso, quanto costa decidere.

Quello che manca non si inventa: nel piano va tra i campi `"da_confermare"`, e nella pagina diventa una domanda
semplice per il cliente ("In bassa stagione lavorate su prenotazione?").

## 3. Cosa contiene

```json
{
  "versione": "AAAA-MM-GG",
  "obiettivo": "prenotazioni | contatti | vendite online | notorietà",
  "pubblico": "chi è, cosa desidera, cosa teme (una riga ciascuno)",
  "promessa": "la frase di posizionamento (dall'audit se c'è, altrimenti 'da confermare')",
  "maturita": "nuovo | in crescita | affermato",
  "lingue": [{"lingua": "it", "quota": 60}, {"lingua": "fr", "quota": 40}],
  "stagioni": [{"periodo": "nov-mar", "fase": "bassa", "pubblico": "chi sogna e prenota da casa", "focus": "..."}],
  "canali": [
    {"canale": "instagram", "modo": "principale", "frequenza": "3 a settimana", "formati": ["carosello", "post", "reel", "storia"]},
    {"canale": "facebook", "modo": "stesso", "da": "instagram"},
    {"canale": "linkedin", "modo": "adattato", "da": "instagram", "pubblico": "solo se diverso da quello del piano"},
    {"canale": "tiktok", "modo": "dedicato", "frequenza": "2 a settimana", "formati": ["video", "carosello_foto"]}
  ],
  "rubriche": [
    {"nome": "Da salvare", "scopo": "scoperta", "quota": 40, "formati": ["carosello", "reel"], "temi": ["..."]}
  ],
  "calendario": [
    {"settimana": 1, "giorno": "mar", "canale": "instagram", "formato": "carosello", "rubrica": "Da salvare",
     "tema": "...", "obiettivo": "scoperta", "lingua": "it", "cta": "salva e manda a chi viene con te", "stato": "da_fare", "fatto_da": "",
     "adattamenti": [{"canale": "linkedin", "stato": "da_fare"}, {"canale": "instagram", "formato": "storia", "stato": "da_fare"}]}
  ],
  "regole": {"tono": "...", "cta_ammesse": ["..."], "da_non_dire": ["..."], "da_non_mostrare": ["..."], "volto": "..."},
  "da_confermare": ["..."],
  "hook": ["schemi di hook che valgono per questo cliente"],
  "vincitori": [],
  "riprese_quota": 0.25,
  "ricerca": null,
  "misure": {"scoperta": "salvataggi e condivisioni", "fiducia": "commenti e visite al profilo", "contatto": "DM e clic sul link"}
}
```

**Rubriche** (3-4): si costruiscono dal **settore**, dall'**offerta** e dall'**obiettivo** del cliente, non da un elenco
fisso. Chiediti: cosa cerca questo pubblico prima di comprare? cosa lo fa fidare? cosa lo blocca? Esempi di come cambiano:
- tour ed esperienze: "La rotta" (luoghi e itinerari da salvare), "A bordo" (persone e momenti), "Prima di partire"
  (meteo, mal di mare, cosa portare);
- studio dentistico: "Domande che ti fai" (dubbi veri, linguaggio sobrio), "Lo studio" (persone, strumenti, come si
  lavora), "Il percorso" (cosa succede alla prima visita);
- ristorante: "Il piatto" (cosa e perché), "La cucina" (chi lo fa), "Stasera da noi" (serate, novità, prenotazione);
- e-commerce: "Come si usa", "Scelto per te" (guide alla scelta), "Chi lo compra" (recensioni vere, solo dal brief).

**Controllo** (non è un modello, è una verifica): insieme le rubriche devono coprire **scoperta** (contenuti utili anche
a chi non compra), **fiducia** (persone, lavoro, prove vere) e **contatto** (offerta, dubbi, CTA chiara). Se una delle
tre manca, aggiungi o cambia una rubrica. Ogni rubrica rispetta `da_non_mostrare` e `volto`: se il cliente non vuole
comparire, niente rubriche con la faccia.

**Mix degli obiettivi**, in base a obiettivo del cliente e **maturità dell'account**:

| maturità | come la riconosci | scoperta | fiducia | contatto |
|---|---|---|---|---|
| nuovo | account assente o sotto 1.000 follower, pubblica poco | 55% | 30% | 15% |
| in crescita | 1.000-10.000 follower, pubblica ma con poche richieste | 40% | 35% | 25% |
| affermato | oltre 10.000 follower o molte interazioni, ma le richieste non seguono | 25% | 35% | 40% |

Se l'obiettivo è **contatti o vendite**, sposta 10 punti dalla scoperta al contatto (mai sotto il 20% di scoperta). Se
l'obiettivo è **notorietà**, fai il contrario. Scrivi nel piano il mix scelto e perché.

**Frequenza**: realistica rispetto al tempo del cliente (`ecosistema.aree.team_tempo`): meglio 3 contenuti a settimana
tenuti che 7 promessi. Un video da girare vale come un contenuto e richiede tempo al cliente: non più di 2 a settimana se
li gira lui.

**Lingue**: se il pubblico parla più lingue (`profilo_cliente.social.lingue`, oppure la clientela del brief), il piano
decide la lingua di ogni spazio con le quote del pubblico: un contenuto si fa in una lingua sola, oppure con la
didascalia nella seconda lingua. Mai le lingue mescolate dentro la stessa slide. Se il pubblico straniero è il più
importante, i contenuti di scoperta e di contatto vanno soprattutto nella sua lingua.

**Stagioni** (per le attività che hanno una stagione: turismo, ristorazione, eventi, scuole, regali, sport):
- dividi l'anno in fasi dalle informazioni del cliente (`stagione_forte`, `stagione_bassa`) e scrivile in `stagioni`;
- **in bassa stagione** si parla a chi sogna e prepara: più scoperta e contenuti da salvare, la CTA porta a
  prenotare in anticipo o a seguire l'account; si preparano i contenuti per l'alta;
- **a ridosso dell'alta** (4-6 settimane prima) cresce la fiducia: persone, cosa aspettarsi, dubbi;
- **in alta stagione** si parla a chi è già lì o sta per decidere: più contatto, CTA immediate (scrivici, prenota),
  contenuti veloci da girare sul posto;
- il calendario usa la fase in cui cade e la scrive nello spazio; i `momenti` del cliente (eventi, aperture,
  novità) entrano nel calendario nella settimana giusta, e solo quelli veri.

**Canali e adattamenti.** Nel piano entrano solo i canali che il cliente usa davvero o vuole aprire (brief,
`profilo_cliente.social`, `ecosistema.aree.social`). Ogni canale ha un `modo`:

| modo | cosa vuol dire | quando |
|---|---|---|
| `principale` | il canale su cui nascono i contenuti; uno solo per piano | di solito Instagram; LinkedIn per uno studio B2B, TikTok se il cliente punta solo lì |
| `stesso` (`da`: canale) | si pubblica lo stesso contenuto del canale indicato, con la sua didascalia | Facebook che riprende Instagram |
| `adattato` (`da`: canale) | si aggiunge una versione ricavata dallo stesso contenuto: stessa idea, stesso hook, stessa direzione grafica, ma formato, lunghezza e didascalia di quel canale | il caso normale per ogni canale in più |
| `dedicato` | il canale ha contenuti propri, nati nel suo formato, che **sostituiscono** il principale su quel canale e hanno i loro spazi nel calendario | pubblico diverso su quel canale (clienti su Instagram, aziende su LinkedIn), oppure un canale che vive di formati suoi (TikTok, Pinterest) |

- Il `modo` lo **proponi tu** quando crei o aggiorni il piano, partendo da dove sta il pubblico e dal tempo del
  cliente (`team_tempo`), e lo scrivi tra i `da_confermare` ("LinkedIn: adattato da Instagram o contenuti
  dedicati?"). Vincenzo o il cliente lo cambiano con una revisione del piano o nel brief ("solo Instagram",
  "su LinkedIn contenuti dedicati"): da quel momento vale per tutti gli agenti.
- Un canale che non è nel piano non riceve niente: niente adattamenti "per sicurezza".
- Gli spazi del canale principale hanno `adattamenti`: un elemento per ogni canale `adattato` (e per la **storia**
  di Instagram, se `storia` è tra i formati: rimanda al contenuto del feed). I canali `dedicato` hanno spazi propri
  nel calendario, con il loro `canale`. I canali `stesso` non hanno niente da fare: si pubblica lo stesso file.
- Il **mix** (scoperta, fiducia, contatto) vale sul canale principale e su ogni canale `dedicato`, ciascuno per conto
  suo. Gli adattamenti seguono l'obiettivo dello spazio da cui nascono.

**Calendario**: ogni spazio ha settimana, giorno, canale, formato, rubrica, tema, obiettivo e CTA. Alterna le rubriche e
non mettere due contenuti di contatto di fila. Mai date di eventi, offerte o prezzi che non sono nel brief.

## 4. Come lo usa ogni agente

- **`carosello_social`**: prende gli spazi con formato carosello, post, carosello foto o pin, e i loro
  `adattamenti`. `prima` = i primi 2 spazi del canale principale e **al massimo un adattamento d'esempio**;
  `completa` = tutti gli spazi della settimana 1, con i loro adattamenti e gli spazi dei canali `dedicato`.
- **`script_video`**: prende gli spazi reel o video. Il copione segue rubrica, obiettivo e CTA dello spazio.
- **`video_ai`**: prende gli spazi video che si possono generare (prodotto, luogo, spot). Se i video servono per gli
  annunci, il piano non li vincola: lo scrivi nelle note.
- **Video e canali**: un video verticale 9:16 vale per Reel, TikTok e Shorts. Per i canali `stesso` o `adattato` si
  usa lo stesso video con didascalia, hashtag e copertina di quel canale (un adattamento del video = una didascalia
  in più, non un video nuovo); per un canale `dedicato` il video nasce per quel canale (ritmo, durata, suoni di
  tendenza di quella piattaforma).
- **`video_montaggio`**: il girato c'è già. Abbina ogni video allo spazio più vicino (rubrica, obiettivo) e scrivi
  didascalia e CTA di quello spazio; se nessuno spazio è vicino, scrivilo nelle note.

**Spazi "Ripresa"** (sezione 4b): l'agente del formato dello spazio riceve il vincitore (link, hook, tema) e ne fa
la versione indicata nello spazio. Guarda l'originale (link o copertina) per capire cosa ha funzionato e lo rifà con
la direzione grafica attuale: mai lo stesso testo e la stessa grafica. Nella `ripresa` del vincitore scrive lo spazio
e la versione fatta.

Per ogni contenuto:
- nel `brief.md` (o `base.md`) e nelle note scrivi **lo spazio occupato** (settimana, giorno, rubrica, obiettivo);
- la CTA è quella dello spazio, scritta in modo naturale;
- alla fine segna lo spazio `"stato": "fatto"` con `"fatto_da": "<job_id>"` e salva il piano aggiornato in
  `officina_fine.risultato.piano_editoriale`. Se l'hai creato o aggiornato, mandalo anche nell'ecosistema:
  `ecosistema.aree.social = {"stato": "base", "nota": "piano editoriale del AAAA-MM-GG: N rubriche, N contenuti a settimana"}`.

**Nella pagina del cliente**, quando crei o aggiorni il piano: una sezione **"Il tuo piano editoriale"** con le
rubriche (nome, a cosa servono, quanto spesso), i canali con una riga ciascuno su cosa ci si pubblica ("Facebook:
gli stessi post di Instagram", "LinkedIn: versioni con più testo per le aziende") e il calendario delle settimane,
con i contenuti di questa anteprima evidenziati. Parole semplici, niente sigle.

**Il tuo feed**: chi produce caroselli o post mostra anche come appare il profilo del canale principale con i
contenuti del piano (`social/ISTRUZIONI.md`, sezione 6c): i contenuti di questa anteprima con le loro copertine
vere, gli altri spazi della settimana come riquadri "in arrivo" con il tema, nell'ordine di pubblicazione.

## 4b. I contenuti che funzionano tornano più volte (riprese)

Un contenuto che ha funzionato per **questo** cliente vale più di qualunque tendenza: si ripropone più volte, ogni
volta in una versione nuova, finché continua a funzionare.

**Chi è un vincitore**: un contenuto del cliente (fatto da lui o da noi) che ha reso **almeno il doppio della sua
mediana** sullo stesso canale, con la misura di quella piattaforma (`officina/SOCIAL-MISURE.md`: salvataggi +
condivisioni su TikTok e su Instagram con gli insights, visualizzazioni su YouTube, interazioni su Facebook e LinkedIn),
confrontato con i suoi contenuti degli ultimi 12 mesi, mai con il settore o con un altro canale. Servono almeno 8 contenuti per avere una mediana; con meno, nessun
vincitore. Deve parlare ancora di qualcosa che il cliente vende o fa: eventi passati e prodotti tolti non contano.

**Da dove arrivano**, in quest'ordine (prima i gratuiti):
0. se il cliente ci ha dato l'accesso (`accessi_cliente` con fonte `instagram` o `facebook_pagina`): il workflow
   **"PrismaPixel · Insights social"** (`workflowId: "UAvE9NVsNXxnaW42"`, body `{"job_id": "<job_id>"}`, risultato in
   `insights_social`, come in `report/ISTRUZIONI.md` sezione 2c). Dà salvataggi e condivisioni veri: vale più dei
   dati pubblici. Fuori dal report il periodo sono gli ultimi 90 giorni, la mediana sempre 12 mesi;
1. `contesto.cliente.lavori`: `audit_strategia` → `risultato.social.migliori`; `report_mensile` → `risultato.misure.<canale>.migliori` (i migliori del mese, anche quelli fatti da noi);
2. il piano stesso: `vincitori` (sotto);
3. se mancano o hanno più di 60 giorni: i dati pubblici del **canale principale e di ogni canale `dedicato`**, con strumenti e misura di `officina/SOCIAL-MISURE.md` (2-4 crediti a canale, budget della ricerca), anche quando la ricerca di viralità non si fa.

Ogni canale ha i **suoi** vincitori, misurati contro la sua mediana; le riprese di un canale `dedicato` stanno nei suoi spazi e nella sua quota.

Nel piano:
`"vincitori": [{"url": "...", "canale": "instagram", "formato": "carosello", "tema": "...", "hook": "...", "resa": 3.4, "data": "AAAA-MM-GG", "riprese": [{"spazio": "S3-gio", "versione": "reel con lo stesso hook", "resa": null}], "stato": "attivo|ritirato"}]`
(`resa` = volte la mediana del cliente).

**Il ciclo**:
- prima ripresa **3-4 settimane** dopo l'originale (o dalla creazione del piano), poi **ogni 4-6 settimane**;
- **ogni ripresa è una versione diversa**, mai lo stesso file: un altro formato (carosello → reel, reel → carosello,
  post → storia), un altro hook tra quelli alternativi, un angolo nuovo sullo stesso tema, dati o stagione aggiornati.
  L'idea che ha funzionato resta; cambia come si presenta;
- un vincitore resta `attivo` finché le riprese rendono almeno quanto la mediana del cliente; dopo **2 riprese di fila
  sotto la mediana** diventa `ritirato`. Il report mensile aggiorna la `resa` delle riprese;
- il report o l'agente che trova un vincitore nuovo lo aggiunge a `vincitori`;
- ogni volta che il calendario si allunga (settimane nuove) o il piano si aggiorna, gli spazi "Ripresa" si rimettono
  in calendario dai vincitori `attivi` e dalle date delle loro ultime riprese.

**Quanto spazio**: le riprese hanno la rubrica **"Ripresa"** nel calendario e occupano **fino a 1 contenuto su 4**
del canale principale (25%); gli altri 3 su 4 restano contenuti nuovi. Se i vincitori attivi sono pochi, le riprese
sono meno: mai inventare un vincitore per riempire la quota. In più ogni ripresa può avere i suoi `adattamenti`
(storie, altri canali) senza togliere spazio al feed.
- Vincenzo o il cliente possono cambiare la quota nel brief o con una revisione del piano (`"riprese_quota": 0.25`);
  `0` le spegne.
- **Mai nella bozza `prima`** (il cliente deve vedere contenuti nuovi): lì i vincitori guidano solo temi, formati e hook.
- Nel mix (scoperta, fiducia, contatto) la ripresa conta con l'obiettivo dello spazio che occupa.

**Anche quando non si ripropongono**, i vincitori guidano il piano: le rubriche e i formati che rendono di più per il
cliente prendono più spazio, e i loro schemi di hook entrano in `hook`.

## 5. Ricerca di viralità: inclusa nel piano, ma non sempre

La ricerca guarda cosa viene **salvato e condiviso più del solito** nel settore e nella zona del cliente. Serve a
scegliere i temi delle rubriche e gli schemi di hook. Non si fa a ogni contenuto.

**Si fa quando:**
- crei il piano o lo aggiorni dopo 90 giorni;
- uno spazio del calendario è della rubrica **"Tendenza"** (facoltativa, al massimo 1 contenuto su 6).

**Non si fa quando:**
- il piano ha già una `ricerca` con meno di 60 giorni, sullo stesso settore e zona: riusala;
- un altro cliente dello stesso settore e zona ha una ricerca con meno di 30 giorni: riusala (sono dati pubblici).
  Per trovarla:
  `select risultato->'piano_editoriale'->'ricerca' from draft_jobs where risultato->'piano_editoriale'->'ricerca'->>'settore' ilike '%<settore>%' and risultato->'piano_editoriale'->'ricerca'->>'zona' ilike '%<zona>%' order by ready_at desc limit 1;`
- è una `revisione`, un contenuto delle rubriche Prova o Offerta (nascono dal cliente, non dalle tendenze) o il montaggio
  di un girato già fatto.

**Settori con pochi dati** (B2B, professioni, nicchie locali): fai 1 ricerca di prova. Se escono meno di 10 post
pertinenti, fermati e scrivi nel piano `"ricerca": {"esito": "settore con pochi dati"}`: le rubriche partono dal
pubblico e dall'offerta.

**Come si fa** (Manifold, budget **4 crediti** per il piano base, **6** per il piano completo, sempre `max_credits`;
mai `leads_*`, `console_*`, `analytics_*`, `submit_feedback` con dati del cliente):
1. `tiktok_search_videos`, **2 ricerche** in italiano (o nella lingua del pubblico), `sort: "popular"`,
   `since: "year"`. La prima sul servizio e il luogo (es. "gita in barca polignano"), la seconda sulla domanda del
   pubblico (es. "cosa fare a polignano"). Danno 30 risultati per pagina, con follower, salvataggi e condivisioni.
   È la fonte principale.
2. `instagram_search_posts` su **1 hashtag** del settore, `since: "year"`: spesso pochi post, senza follower né
   salvataggi. Serve per temi e commenti, non per la classifica.
3. I post del cliente **non entrano in questa classifica**: si valutano contro la sua mediana e vanno in `vincitori`
   (sezione 4b), che usa la stessa chiamata se serve.

**Cosa conta**: per ogni post la **spinta** = (salvataggi + condivisioni) ÷ max(follower dell'autore, 1.000) × 100.
Scarta i like nascosti (= 3), gli annunci (`is_ad`), i post fuori tema e le pagine con più di 500.000 follower. Tieni
i **5 post con la spinta più alta**, solo se almeno il doppio della mediana. Da questi ricavi: temi, schemi di hook
(mai copiati), formato, cosa chiedono i commenti e **lo spazio libero** (l'angolo che nessuno usa).

**Regola d'incrocio**: un tema che spinge entra nel piano solo se si collega al pubblico o all'offerta del cliente. Se
non c'entra con quello che vende, vince il problema del cliente.

Nel piano:
`"ricerca": {"data": "AAAA-MM-GG", "settore": "...", "zona": "...", "temi": ["..."], "schemi_hook": ["..."], "spazio_libero": "...", "post": [{"url": "...", "spinta": 0}], "crediti": 0}`.
Nelle note per Vincenzo: i 2-4 post usati, con link e spinta, e cosa ne hai preso. I numeri della ricerca non vanno
mai nei contenuti e non sono una promessa di risultati.
