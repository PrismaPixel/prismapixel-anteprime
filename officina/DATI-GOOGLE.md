# Dati Google del cliente (GA4 e Search Console) · PrismaPixel

GA4 e Search Console dei clienti stanno negli **account Google di PrismaPixel**
(`pubblicazione/tracciamento/IMPOSTAZIONE.md`). Gli agenti li leggono **solo** con il workflow n8n
**"PrismaPixel · Dati Google"**, mai con Manifold (`console_*`, `analytics_*`) né con altri strumenti.

## Come si chiama

`execute_workflow`: `workflowId: "V1bQYaTGn2EVMIYJ"`, `executionMode: "production"`,
`triggerNodeName: "Richiesta dati Google"`,
`inputs: { "webhookData": { "method": "POST", "body": { "job_id": "<job_id del lavoro>" } } }`.

- Passi solo il `job_id`: le proprietà le prende il workflow dagli accessi del cliente (`ga4`, `search_console`).
  Risponde per un lavoro aperto degli ultimi 15 giorni: `report_mensile`, `audit_strategia`, `roadmap`,
  `piano_seo`, `pubblicazione_sito`.
- Periodo: per il report il mese del brief (`brief.mese`), per gli altri lavori l'ultimo mese intero; sempre con il
  mese prima per il confronto.
- Il risultato **non sta nell'esecuzione** (non viene salvata): attendi 10-30 secondi e leggilo con `execute_sql`:
  `select dati from misure_google where job_ref = '<job_id>' order by id desc limit 1;`

## Cosa c'è in `dati`

```json
{"periodo": {"mese": "2026-10", "inizio": "2026-10-01", "fine": "2026-10-31", "prima": "2026-09"}, "dati_parziali": false,
 "ga4": {"proprieta": "123", "errore": null,
         "mese": {"visite": 0, "utenti": 0, "nuovi_utenti": 0, "visite_coinvolte": 0, "conversioni": 0, "pagine_viste": 0},
         "prima": {}, "variazione_pct": {},
         "canali": [{"canale": "Organic Search", "visite": 0, "conversioni": 0}],
         "eventi": {"generate_lead": {"mese": 0, "prima": 0}, "click_whatsapp": {}, "click_telefono": {}},
         "pagine_di_arrivo": [{"pagina": "/", "visite": 0, "conversioni": 0}],
         "dispositivi": [{"dispositivo": "mobile", "visite": 0}]},
 "search_console": {"proprieta": "sc-domain:esempio.it", "errore": null,
         "mese": {"clic": 0, "impressioni": 0, "ctr_pct": 0, "posizione": 0}, "prima": {}, "variazione_pct": {},
         "ricerche": [{"ricerca": "...", "clic": 0, "impressioni": 0, "posizione": 0}],
         "pagine": [{"pagina": "https://...", "clic": 0, "impressioni": 0, "posizione": 0}]}}
```

- `conversioni` = eventi chiave di GA4 (contatti, WhatsApp, telefono, acquisti). `eventi` dice quali.
- `errore: "non collegato"`: il cliente non ha quella fonte negli accessi. Nel report: "Google Analytics / Search
  Console da collegare".
- Altro `errore` (permessi, proprietà non trovata): nelle note "accesso <fonte> non raggiungibile: <errore>", senza
  inventare numeri.
- `dati_parziali: true`: il mese è finito da meno di 3 giorni, Search Console non ha ancora tutti i dati. Scrivilo.
- Primo mese di misura (mese prima a zero): niente percentuali, "punto di partenza".
- Sono dati privati del cliente: nel report sì, mai su GitHub.
