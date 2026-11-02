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
riprova. **Budget 25 crediti per report.** Vietati: `leads_*`, `submit_feedback` con dati del cliente.

| servizio pagato | cosa misuri | strumento | crediti |
|---|---|---|---|
| SEO, AEO & GEO | posizione su 3-5 ricerche fisse (le stesse ogni mese: quelle del piano SEO o del primo report) | `seo_get_position` | 1-2 ciascuna |
| SEO, AEO & GEO | scheda Google: voto e numero di recensioni | `maps_get_place` | 2 |
| SEO, AEO & GEO | risposte delle AI a 1 domanda fissa, **solo a marzo, giugno, settembre e dicembre** (o ogni mese al livello 3) | `aeo_run_ai_answers` + `get_task` | ≤ 15 |
| Social & AI Content, Video AI, Montaggio | follower, contenuti pubblicati nel mese, i 3 contenuti migliori del mese per interazioni | `instagram_get_profile`, `instagram_get_posts` (e TikTok o Facebook se sono nel piano) | 1-3 ciascuno |
| Gestione ADS | annunci attivi del cliente nella libreria pubblica | `ads_get_advertiser_ads` | 2 |
| Siti Web & E-commerce | il sito risponde, titolo e descrizione delle pagine chiave, strumenti presenti | workflow **"PrismaPixel · Scansione sito"** (come nell'audit) + `seo_get_page` | gratis |
| Email Marketing, Automazioni, Consulenza | niente dati pubblici: solo lavoro fatto e dati privati | — | — |

Se il budget non basta, l'ordine è: SEO (posizioni) → social → scheda Google → ADS → AI.

### 2c. Dati privati (solo se il cliente li ha collegati)

`brief.accessi` elenca le fonti che il cliente ci ha dato in sola lettura (tabella `accessi_cliente`). **Usi solo
quelle**, e solo per questo cliente:

| fonte | cosa leggi | come |
|---|---|---|
| `search_console` | clic, impressioni e posizione media delle ricerche, confronto col mese prima | `console_get_search_analytics` sulla proprietà in `riferimento` |
| `ga4` | visite, da dove arrivano, contatti o acquisti (conversioni) | `analytics_get_report` sulla proprietà in `riferimento` |
| `meta` | spesa, persone raggiunte, clic e risultati (conversazioni, contatti, acquisti, prenotazioni) del mese, totali e per campagna | workflow n8n **"PrismaPixel · Dati Meta Ads"** (sotto) |
| `google_ads`, `email`, `ecommerce`, `altro` | — | non c'è ancora un lettore automatico: scrivi "dati di <fonte> da collegare" nelle note |

**Dati Meta Ads.** Avvia con `execute_workflow`: `workflowId: "SNyf2JhKdBX3H1Cl"`, `executionMode: "production"`,
`triggerNodeName: "Richiesta dati Meta"`, `inputs: { "webhookData": { "method": "POST", "body": { "job_id": "<job_id del report>" } } }`.
Leggi il risultato con `get_workflow_execution` (`includeData: true`, `nodeNames: ["Riepilogo", "Non disponibile"]`).
- Passi solo il `job_id`: l'account pubblicitario lo prende il workflow dagli accessi del cliente, e risponde solo per
  un report mensile aperto.
- `ok: false` o `errore` su un conto: scrivi nelle note il motivo ("accesso Meta non ancora dato", "permessi
  insufficienti") e fai il blocco ADS con lavoro fatto e dati pubblici.
- La spesa è nella valuta dell'account. Nel report mostra spesa, risultati e costo per risultato (spesa ÷ risultati,
  calcolato da te); clic e CTR solo se aiutano a spiegare. Per il pubblico dei social organici restano i dati pubblici
  di 2b.

Se la proprietà indicata non compare tra quelle collegate (`console_list_properties`, `analytics_list_properties`),
non cercarne altre: scrivi nelle note "accesso <fonte> non raggiungibile". Se non ci sono accessi, il report si fa lo
stesso con 2a e 2b, e chiude con una riga gentile: "Se ci colleghi Google Analytics e Search Console, dal prossimo mese
vedi anche visite e contatti".

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
    si confronta allo stesso modo. Esempio: `{"seo": {"metodo": {"zona": "Bari", "dispositivo": "mobile"}, "posizioni": {"pizzeria bari centro": 7}}, "instagram": {"follower": 1840, "contenuti": 12}}`;
  - `fatti`: 1-3 risultati verificati del mese (`tipo: "risultato"`), ad esempio "In ottobre è passato dal 12° al 7°
    posto per «pizzeria bari centro»";
  - `ecosistema`: aggiorna le aree dei servizi seguiti, con quello che hai verificato;
  - `passa_a`: solo se il report fa emergere un lavoro nuovo da proporre (es. un servizio che risolve un problema
    visto nei numeri), mai per i lavori già compresi nell'abbonamento.
- Il report arriva al cliente **solo dopo l'ok di Vincenzo**: non mandarlo tu e non scrivere al cliente.
