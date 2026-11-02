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
| il piano ha più di 90 giorni, oppure obiettivo, offerta o pubblico sono cambiati, oppure `modifiche_richieste` lo tocca | **lo aggiorni**: tieni ciò che funziona, cambi rubriche o calendario |
| c'è un piano valido | **lo segui**: prendi i primi spazi `da_fare` del tuo formato e non lo rifai |
| `revisione` | non tocchi il piano: correggi solo i contenuti |

Il piano lo crea **il primo agente social** che lavora per il cliente, qualunque sia. Per la prima bozza basta il
**piano base**: rubriche, mix e le prime 2 settimane di calendario. La versione completa ha 4 settimane.

## 3. Cosa contiene

```json
{
  "versione": "AAAA-MM-GG",
  "obiettivo": "prenotazioni | contatti | vendite online | notorietà",
  "pubblico": "chi è, cosa desidera, cosa teme (una riga ciascuno)",
  "promessa": "la frase di posizionamento (dall'audit se c'è, altrimenti 'da confermare')",
  "canali": [{"canale": "instagram", "frequenza": "3 a settimana", "formati": ["carosello", "reel"]}],
  "rubriche": [
    {"nome": "Da salvare", "scopo": "scoperta", "quota": 40, "formati": ["carosello", "reel"], "temi": ["..."]}
  ],
  "calendario": [
    {"settimana": 1, "giorno": "mar", "canale": "instagram", "formato": "carosello", "rubrica": "Da salvare",
     "tema": "...", "obiettivo": "scoperta", "cta": "salva e manda a chi viene con te", "stato": "da_fare", "fatto_da": ""}
  ],
  "regole": {"tono": "...", "cta_ammesse": ["..."], "da_non_dire": ["..."]},
  "hook": ["schemi di hook che valgono per questo cliente"],
  "ricerca": null,
  "misure": {"scoperta": "salvataggi e condivisioni", "fiducia": "commenti e visite al profilo", "contatto": "DM e clic sul link"}
}
```

**Rubriche** (3-4, con nomi adatti al cliente). Il punto di partenza è questo, da adattare:
1. **Da salvare** (scoperta): guide, liste, itinerari, errori da evitare. Contenuti utili anche a chi non compra.
2. **Dietro le quinte e persone** (fiducia): chi lavora, come si fa, il luogo. Con la faccia se il cliente ci sta.
3. **Prova** (fiducia): cosa succede davvero, recensioni e numeri **solo se sono nel brief**.
4. **Offerta e dubbi** (contatto): come funziona, cosa include, le obiezioni vere del pubblico (dall'audit, dalla chat,
   dai commenti), con una CTA chiara.

**Mix degli obiettivi**: di base 40% scoperta, 35% fiducia, 25% contatto. Se l'obiettivo del cliente è il contatto o la
vendita, 30 / 30 / 40.

**Frequenza**: realistica rispetto al tempo del cliente (`ecosistema.aree.team_tempo`): meglio 3 contenuti a settimana
tenuti che 7 promessi. Un video da girare vale come un contenuto e richiede tempo al cliente: non più di 2 a settimana se
li gira lui.

**Calendario**: ogni spazio ha settimana, giorno, canale, formato, rubrica, tema, obiettivo e CTA. Alterna le rubriche e
non mettere due contenuti di contatto di fila. Mai date di eventi, offerte o prezzi che non sono nel brief.

## 4. Come lo usa ogni agente

- **`carosello_social`**: prende gli spazi con formato carosello o post. `prima` = i primi 2 spazi di quel formato;
  `completa` = tutti quelli della settimana 1.
- **`script_video`**: prende gli spazi reel o video. Il copione segue rubrica, obiettivo e CTA dello spazio.
- **`video_ai`**: prende gli spazi video che si possono generare (prodotto, luogo, spot). Se i video servono per gli
  annunci, il piano non li vincola: lo scrivi nelle note.
- **`video_montaggio`**: il girato c'è già. Abbina ogni video allo spazio più vicino (rubrica, obiettivo) e scrivi
  didascalia e CTA di quello spazio; se nessuno spazio è vicino, scrivilo nelle note.

Per ogni contenuto:
- nel `brief.md` (o `base.md`) e nelle note scrivi **lo spazio occupato** (settimana, giorno, rubrica, obiettivo);
- la CTA è quella dello spazio, scritta in modo naturale;
- alla fine segna lo spazio `"stato": "fatto"` con `"fatto_da": "<job_id>"` e salva il piano aggiornato in
  `officina_fine.risultato.piano_editoriale`. Se l'hai creato o aggiornato, mandalo anche nell'ecosistema:
  `ecosistema.aree.social = {"stato": "base", "nota": "piano editoriale del AAAA-MM-GG: N rubriche, N contenuti a settimana"}`.

**Nella pagina del cliente**, quando crei o aggiorni il piano: una sezione **"Il tuo piano editoriale"** con le
rubriche (nome, a cosa servono, quanto spesso) e il calendario delle settimane, con i contenuti di questa anteprima
evidenziati. Parole semplici, niente sigle.

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
3. Se il cliente ha già un account con dei post, guarda anche i suoi migliori (`instagram_get_posts` o
   `tiktok_get_videos`, 1 chiamata): quello che funziona per lui conta più degli altri.

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
