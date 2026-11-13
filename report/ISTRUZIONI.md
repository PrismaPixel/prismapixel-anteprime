# Agente Report mensile · PrismaPixel

Istruzioni per l'agente che produce il deliverable `report_mensile`.

**Prima di tutto leggi `officina/CONTRATTO.md`**: ricezione del lavoro, pubblicazione dell'anteprima ed esito finale
seguono quel contratto. Qui sotto ci sono solo le regole del report.

Il lavoro nasce da solo il 2 di ogni mese per ogni cliente con un abbonamento attivo da almeno 20 giorni, e parte
solo dopo l'ok di Vincenzo su Telegram. Il report lo rivede Vincenzo prima che arrivi al cliente.

```
{ job_id, deliverable: "report_mensile", livello: "prima",
  brief: { mese: "2026-10", servizi: ["SEO, AEO & GEO", "Social & AI Content"], accessi: [{ fonte: "ga4", riferimento: "..." }] },
  profilo_cliente, n8n: { ... } }
```

Nessuno è presente mentre lavori: non fare domande, prendi la lettura più ragionevole e annotala in `note`.

## 1. Cosa deve fare il report

Il cliente paga ogni mese: il report gli dice, per **ogni servizio che paga**, cosa abbiamo fatto, cosa è cambiato e
cosa facciamo il mese prossimo. Deve potersi leggere in 3 minuti dal telefono.

Due regole prima di tutto:
- **Onestà sui numeri.** Se un numero è sceso, lo dici e spieghi cosa fai. Niente numeri gonfiati, niente
  percentuali su basi piccole ("+100%" da 2 a 4 visite si scrive "da 2 a 4").
- **Si confronta solo ciò che è misurato allo stesso modo.** Stesse ricerche, stessa zona, stesso strumento del mese
  prima. Se il metodo cambia, il confronto non si fa e lo dici.

## 2. Le tre fonti

### 2a. Il lavoro fatto (sempre, gratis)

Dall'Agent OS (`execute_sql` sul progetto `oshnvlkwuclxbbjdaupt`), con `<id>` = `contesto.cliente.id` e
`<inizio>`/`<fine>` = primo giorno del mese del report e primo giorno del mese dopo:

```sql
select deliverable, servizio, status, preview_url, created_at::date
  from draft_jobs where client_id = <id> and created_at >= '<inizio>' and created_at < '<fine>'
   and deliverable <> 'report_mensile' order by created_at;
select tipo, titolo, created_at::date from events
 where client_id = <id> and created_at >= '<inizio>' and created_at < '<fine>' order by created_at;
```

Dal contesto prendi anche: il **piano editoriale** (spazi coperti nel mese, `officina/PIANO-EDITORIALE.md`), le note di
Vincenzo, l'ecosistema e il **report del mese prima** (`cliente.lavori`, `deliverable = report_mensile`,
`risultato.misure`): è la base del confronto.

Scrivi il lavoro come lo capisce il cliente: "12 contenuti pubblicati su 12 previsti", "pagina Servizi riscritta",
"2 campagne attive". Mai nomi di agenti, strumenti o codici interni.

### 2b. Dati pubblici (sempre, con Manifold)

Regole di spesa come nell'audit: `max_credits` su ogni chiamata, `dry_run` per i costi nuovi, `NoData` non si
riprova. **Budget 25 crediti per report**, più 3 per ogni canale social oltre il primo (massimo 40). Vietati: `leads_*`, `submit_feedback` con dati del cliente.

| servizio pagato | cosa misuri | strumento | crediti |
|---|---|---|---|
| SEO, AEO & GEO (con OpenSEO, `officina/OPENSEO.md`) | **storico del monitoraggio** del progetto del cliente (`get_rank_history`), visibilità nelle AI (`get_ai_visibility_trend`), Search Console e Analytics dal progetto se collegati; griglia su Maps (`get_local_rank_grid`) ogni 3 mesi | 0-100 crediti OpenSEO |
| SEO, AEO & GEO (senza OpenSEO) | posizione delle **ricerche monitorate** del piano SEO (`piano_seo.risultato.ricerche_monitorate`; se non c'è, 3-5 ricerche fisse scelte al primo report): prima Search Console se collegata (gratis), poi **una sola** chiamata `seo_get_ranked_keywords` sul dominio (`location: "Italy"`, `language: "it"`, `limit: 100`) da cui leggi le posizioni di tutte; `seo_get_position` solo per 1-2 ricerche importanti che non compaiono | 10 + 6 ciascuna |
| SEO, AEO & GEO | scheda Google: voto e numero di recensioni | `maps_get_place` | 2 |
| SEO, AEO & GEO | risposte delle AI a 1 domanda fissa, **solo a marzo, giugno, settembre e dicembre** (o ogni mese al livello 3) | `aeo_run_ai_answers` + `get_task` | ≤ 15 |
| Social & AI Content, Video AI, Montaggio | per **ogni canale `principale` o `dedicato` del piano** (Instagram, Facebook, TikTok, YouTube, LinkedIn): follower, contenuti del mese, mediana e migliori del mese con la misura della piattaforma; dei canali `stesso`/`adattato` solo quanti contenuti sono usciti | `officina/SOCIAL-MISURE.md` (insights privati prima, se collegati: 2c) | 2-4 a canale |
| Gestione ADS | annunci attivi del cliente nella libreria pubblica | `ads_get_advertiser_ads` | 2 |
| Siti Web & E-commerce | il sito risponde, titolo e descrizione delle pagine chiave, strumenti presenti | workflow **"PrismaPixel · Scansione sito"** (come nell'audit) + `seo_get_page` | gratis |
| Email Marketing, Automazioni, Consulenza | niente dati pubblici: solo lavoro fatto e dati privati | — | — |

Se il budget non basta, l'ordine è: SEO (posizioni) → social → scheda Google → ADS → AI.

### 2c. Dati privati (solo se il cliente li ha collegati)

`brief.accessi` elenca le fonti che il cliente ci ha dato in sola lettura (tabella `accessi_cliente`). **Usi solo
quelle**, e solo per questo cliente:

| fonte | cosa leggi | come |
|---|---|---|
| `search_console` | clic, impressioni, CTR e posizione media, ricerche e pagine principali, confronto col mese prima | workflow n8n **"PrismaPixel · Dati Google"** (`officina/DATI-GOOGLE.md`) |
| `ga4` | visite, utenti, da dove arrivano (canali), conversioni ed eventi (contatti, WhatsApp, telefono, acquisti), pagine di arrivo, dispositivi | stesso workflow, una sola chiamata per tutte e due le fonti |
| `meta` | spesa, persone raggiunte, clic e risultati (conversazioni, contatti, acquisti, prenotazioni) del mese, totali e per campagna | workflow n8n **"PrismaPixel · Dati Meta Ads"** (sotto) |
| `instagram`, `facebook_pagina` | i contenuti del mese con **copertura, salvataggi e condivisioni veri** (Instagram) o reazioni, commenti e condivisioni (pagina), la mediana dei 12 mesi e i **migliori del mese** (almeno il doppio della mediana) | workflow n8n **"PrismaPixel · Insights social"** (sotto). Se c'è, **sostituisce** la riga social della fonte 2b per quel canale |
| `google_ads`, `email`, `ecommerce`, `altro` | — | non c'è ancora un lettore automatico: scrivi "dati di <fonte> da collegare" nelle note |

**Dati Meta Ads.** Avvia con `execute_workflow`: `workflowId: "SNyf2JhKdBX3H1Cl"`, `executionMode: "production"`,
`triggerNodeName: "Richiesta dati Meta"`, `inputs: { "webhookData": { "method": "POST", "body": { "job_id": "<job_id del report>" } } }`.
Leggi il risultato con `get_workflow_execution` (`includeData: true`, `nodeNames: ["Riepilogo", "Non disponibile"]`).
- Passi solo il `job_id`: l'account pubblicitario lo prende il workflow dagli accessi del cliente, e risponde solo per
  un report mensile aperto.
- `ok: false` o `errore` su un conto: scrivi nelle note il motivo ("accesso Meta non ancora dato", "permessi
  insufficienti") e fai il blocco ADS con lavoro fatto e dati pubblici.
- `senza_inserzioni: true`: nel mese non è girata nessuna inserzione. Scrivilo così ("questo mese le campagne erano
  ferme"), non come risultati a zero.
- La spesa è nella valuta dell'account. Nel report mostra spesa, risultati e costo per risultato (spesa ÷ risultati,
  calcolato da te); clic e CTR solo se aiutano a spiegare. Per il pubblico dei social organici restano i dati pubblici
  di 2b.

**Insights social.** Avvia con `execute_workflow`: `workflowId: "UAvE9NVsNXxnaW42"`, `executionMode: "production"`,
`triggerNodeName: "Richiesta insights social"`, `inputs: { "webhookData": { "method": "POST", "body": { "job_id": "<job_id del report>" } } }`.
Il risultato **non sta nell'esecuzione** (non viene salvata): attendi 10-60 secondi e leggilo con `execute_sql`:
`select dati from insights_social where job_ref = '<job_id>' order by id desc limit 1;`
- Per canale hai `metrica` (salvataggi + condivisioni se Meta dà gli insights, altrimenti like + commenti), `mediana`
  dei 12 mesi, `migliori` del mese (con `resa` = volte la mediana), `contenuti` del mese ed eventuale `errore`.
- `errore` con "permission" o "does not exist": nelle note "insights <canale> non raggiungibili: controllare
  l'accesso partner e l'utente di sistema" e usa i dati pubblici di 2b per quel canale.
- Copia `migliori` in `risultato.misure.<canale>.migliori` (sezione 5) con la stessa `resa`: li riprende il piano
  editoriale. Copertura e salvataggi sono dati privati: nel report sì, mai su GitHub.

**Dati Google.** GA4 e Search Console si leggono **solo** con il workflow "PrismaPixel · Dati Google" (mai Manifold
`console_*`/`analytics_*`): chiamata, lettura da `misure_google` e significato dei campi in `officina/DATI-GOOGLE.md`.
Nei **Numeri** del blocco SEO usa clic e impressioni di Search Console (più 1-2 ricerche dalla lista `ricerche`);
nel blocco Siti/ADS visite e conversioni di GA4, con il canale che porta più contatti. Se il workflow risponde
`errore` per una fonte, non cercare altre proprietà: scrivi nelle note "accesso <fonte> non raggiungibile". Se non ci sono accessi, il report si fa lo
stesso con 2a e 2b, e chiude con una riga gentile: "Se ci colleghi Google Analytics e Search Console, dal prossimo mese
vedi anche visite e contatti".

### 2d. I conti degli annunci (solo per chi paga Gestione ADS)

Servono a dire al cliente se gli annunci **rendono**, non solo quanto costano. Si costruiscono con tre fonti: i
**dati Meta** del mese (sopra), i **numeri che il cliente ci ha dato** (clienti nuovi, quanti dagli annunci, quanto
hanno speso) e i **numeri della consulenza strategica** (valore di un cliente, costo sostenibile, tetti).

1. Leggi tutto con `execute_sql`: `select numeri_per_lavoro('<job_id del report>');`. Ottieni:
   - `questo_mese`: la riga del mese (con `clienti_nuovi`, `clienti_da_annunci`, `ricavo_nuovi` se il cliente li ha
     inviati: `dichiarati: true`);
   - `consulenza`: i `numeri` dell'ultima consulenza (`ltv`/LTGP, `cac_sostenibile`, `tetto_costo_contatto`, …) e la
     data;
   - `storico`: i mesi precedenti (massimo 12), per il confronto e per aggiornare i tetti;
   - `link_cliente`: il link personale per inviare i numeri, se **non** li ha ancora mandati.
   I numeri li chiede Vincenzo al cliente il 1° del mese (workflow "Numeri del cliente"): non scrivere tu al cliente.
2. **Calcola in Python** (mai a mente), solo con i numeri che ci sono:
   - **contatti del mese** = risultati Meta che sono contatti veri (conversazioni avviate, contatti, contatti dal sito,
     prenotazioni, registrazioni), senza contare due volte lo stesso tipo (`lead` e `contatti dal sito` sono spesso lo
     stesso contatto: prendi il maggiore);
   - **costo per contatto** = spesa ÷ contatti;
   - **costo per cliente dagli annunci** (CAC degli annunci) = spesa ÷ `clienti_da_annunci`; se il cliente non sa
     quanti arrivano dagli annunci, non calcolarlo e scrivilo;
   - **scontrino medio dei clienti nuovi** = `ricavo_nuovi` ÷ `clienti_nuovi`;
   - **contatti che diventano clienti** = `clienti_da_annunci` ÷ contatti;
   - **rapporto valore:costo** = LTGP della consulenza ÷ CAC degli annunci (riferimento: almeno 3 a 1);
   - **ROAS di Meta** = `valore_acquisti` ÷ spesa, solo se Meta lo dà (e-commerce con Pixel).
3. **Confronta con le soglie** della consulenza (o, se ci sono almeno 3 mesi di dati veri, con le soglie aggiornate
   sotto): costo per contatto contro `tetto_costo_contatto`, CAC degli annunci contro `cac_sostenibile`. Ogni
   confronto dice da dove viene la soglia ("dalla consulenza di settembre, su stime del cliente").
4. **Diagnosi**, con le parole della consulenza: contatti buoni ma pochi clienti → il problema è la **vendita**, non
   l'annuncio; CAC nella norma ma margini bassi → la leva è il **modello** (prezzo, offerte aggiuntive, ritorni);
   pochi contatti o troppo cari → è l'**acquisizione** (creatività, pubblico, offerta). Una sola diagnosi, quella
   che i numeri sostengono.
5. **Soglie aggiornate**: se nello `storico` più questo mese ci sono almeno **3 mesi** con contatti e
   `clienti_da_annunci`, ricalcola il tetto per contatto con la percentuale vera di contatti che diventano clienti
   (`cac_sostenibile` × clienti dagli annunci ÷ contatti, sui 3 mesi) e salvalo: da quel momento vale quello, non la
   stima della consulenza. Scrivilo nelle note per Vincenzo.
6. **Salva** sempre la riga del mese: `select numeri_salva('<job_id>', '{"spesa_ads": …, "contatti": …,
   "acquisti_meta": …, "valore_acquisti_meta": …, "costo_contatto": …, "cac_annunci": …, "scontrino_medio": …,
   "roas": …, "ltgp": …, "rapporto": …, "cac_sostenibile": …, "tetto_costo_contatto": …, "fonte": {"tetti":
   "consulenza|ricalcolati su 3 mesi"}}');`. Metti solo i numeri che hai davvero (niente zeri al posto dei vuoti). I
   numeri dichiarati dal cliente non si toccano.

**Nella pagina**, dentro il blocco Gestione ADS, una parte **"I conti degli annunci"**: al massimo 4 numeri (costo per
contatto, costo per cliente dagli annunci, scontrino medio, rapporto valore:costo), ognuno con la soglia accanto
("sotto il tetto di 12 €": meglio/peggio con parola e colore) e il mese prima; poi "Cosa vuol dire" con la diagnosi
e la decisione del mese prossimo (spegnere, scalare, cambiare offerta, lavorare sulla vendita). Senza dati del
cliente mostra solo spesa, contatti e costo per contatto, e in **"Cosa ci serve da te"** scrivi: "Quanti clienti
nuovi hai avuto a <mese>, e quanti dagli annunci? Ci vuole un minuto: <link_cliente>". Niente gergo: CAC diventa
"quanto ci costa un cliente nuovo", LTGP "quanto ti fa guadagnare un cliente nel tempo".

## 3. Struttura della pagina

1. **Il mese in breve**: 3 frasi. La cosa più importante fatta, il risultato più chiaro, la priorità del mese
   prossimo.
2. **Un blocco per ogni servizio pagato**, sempre nello stesso ordine:
   - **Fatto**: 2-5 punti (dalla fonte 2a);
   - **Numeri**: massimo 4, ognuno con il valore di questo mese, quello del mese prima e la fonte in piccolo
     ("Google, ricerca da cellulare a Bari"). Primo mese: niente confronto, scrivi "punto di partenza";
   - **Cosa vuol dire**: 1-2 frasi semplici;
   - **Il mese prossimo**: 2-3 azioni concrete, dal piano (piano editoriale, piano SEO, priorità dell'audit).
3. **Cosa ci serve da te**: solo se c'è qualcosa (foto, ok a un testo, un accesso). Al massimo 3 punti.
4. Chiusura breve: "Per qualsiasi dubbio scrivici in chat". Nessuna firma.

Regole di scrittura: quelle del contratto, sezione 6. In più:
- Mai garanzie ("il mese prossimo sarai primo su Google"). Le azioni sì, i risultati promessi no.
- Niente gergo: "posizione media" diventa "in media compari al 7° posto"; "impression" diventa "volte in cui sei
  apparso nelle ricerche".
- Dati di persone mai: niente nomi di chi ha commentato o comprato, niente email.
- Prezzi e canoni non si scrivono nel report.

## 4. Grafica

Il report usa **l'identità del cliente**, non uno stile nuovo: logo, palette e font del branding scelto
(`contesto.cliente.ecosistema`, area `branding`, o il sito fatto da noi). Se non c'è un branding, usa i colori del
suo sito o del profilo social, sobri.

- Un solo file `index.html`, niente immagini o script esterni; font Google solo se sono quelli del brand.
- Numeri grandi e leggibili, frecce su e giù in SVG con il colore di stato (meglio / peggio / uguale) **e** la parola
  scritta: il colore non basta mai da solo.
- Grafici solo se servono (es. le posizioni di 3 ricerche negli ultimi mesi): SVG scritto nel codice, al massimo 1 per
  servizio.
- Testo almeno 16 px, contrasto AA, a 375 px niente scorrimento orizzontale e tabelle al massimo di 3 colonne.

## 5. Pubblicazione ed esito

- Pubblica con il servizio Anteprime come da **contratto, sezione 3**. Il report contiene dati del cliente: **mai su
  GitHub**.
- Esito come da **contratto, sezione 4**, con `fonte = agente_report_mensile`:
  - `descrizione`: per Vincenzo, 2 righe: la notizia migliore e quella da gestire;
  - `note`: `durata · crediti: manifold <N> · token`, poi fonti usate, accessi mancanti o non raggiungibili,
    numeri da verificare.
- In `officina_fine`:
  - `risultato`: `{"mese": "2026-10", "misure": {...}, "fatto": {...}, "prossimo_mese": {...}}`. In `misure` salva
    **tutto quello che hai misurato con il metodo** (ricerche usate, zona, dispositivo, proprietà), così il mese dopo
    si confronta allo stesso modo. Esempio: `{"seo": {"metodo": {"zona": "Bari", "dispositivo": "mobile"}, "posizioni": {"pizzeria bari centro": 7}}, "instagram": {"follower": 1840, "contenuti": 12, "mediana": {"salvataggi_condivisioni": 9}, "migliori": [{"url": "...", "formato": "carosello", "tema": "...", "hook": "...", "resa": 2.6, "data": "AAAA-MM-GG"}]}}`.
    In `migliori` vanno i contenuti del mese che hanno reso almeno il doppio della mediana del cliente: diventano i
    vincitori del piano editoriale (`officina/PIANO-EDITORIALE.md`, sezione 4b). Se nel mese sono uscite delle
    **riprese**, scrivi la loro resa in `"riprese": [{"url": "...", "vincitore": "<url originale>", "resa": 1.2}]`;
  - in `misure.annunci` copia i conti del mese (gli stessi salvati con `numeri_salva`);
  - `fatti`: 1-3 risultati verificati del mese (`tipo: "risultato"`), ad esempio "In ottobre è passato dal 12° al 7°
    posto per «pizzeria bari centro»";
  - `ecosistema`: aggiorna le aree dei servizi seguiti, con quello che hai verificato;
  - `passa_a`: solo se il report fa emergere un lavoro nuovo da proporre (es. un servizio che risolve un problema
    visto nei numeri), mai per i lavori già compresi nell'abbonamento.
- Il report arriva al cliente **solo dopo l'ok di Vincenzo**: non mandarlo tu e non scrivere al cliente.
