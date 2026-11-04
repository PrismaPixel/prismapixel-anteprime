# Misurare i social del cliente · PrismaPixel

Vale per **audit**, **report mensile** e **piano editoriale** (vincitori e riprese). Dice quali canali guardare, con
quali strumenti, con quale misura e quanto si spende. Dati privati (insights) prima di quelli pubblici; ogni canale si
confronta **solo con se stesso**, mai con un'altra piattaforma o con il settore.

## 1. Quali canali

1. **Trovali tutti**, prima di spendere: link nel sito (piede, contatti), `sameAs` dei dati strutturati (`seo_get_page`
   e `aeo_get_site_readiness` li danno gratis), brief, `profilo_cliente.contatti` e `profilo_cliente.social`,
   accessi del cliente (`accessi_cliente`).
2. Un profilo trovato solo per nome (ricerca) va confermato: stesso nome, stessa città o stesso sito nel profilo.
   Se non è sicuro, scrivi "profilo da confermare" e non misurarlo.
3. **Audit**: tutti i canali trovati. **Report**: i canali del piano con `modo` `principale` o `dedicato` (quelli
   `stesso` e `adattato` pubblicano contenuti ricavati: basta il numero di pubblicazioni). **Piano**: i vincitori si
   cercano sul canale principale e su ogni canale `dedicato`.
4. Un canale fermo da più di 90 giorni conta come "fermo": lo dici e non calcoli la mediana.

## 2. Strumenti e misura per piattaforma

| piattaforma | dati privati (se c'è l'accesso) | dati pubblici (Manifold) | **misura** per la mediana | crediti pubblici |
|---|---|---|---|---|
| Instagram | workflow "PrismaPixel · Insights social" (fonte `instagram`) | `instagram_get_profile`, `instagram_get_posts` (1 pagina = gli ultimi contenuti) | con insights: salvataggi + condivisioni; senza: like + commenti (con like nascosti: commenti; per i reel anche le visualizzazioni) | 1 + 1 |
| Facebook | stesso workflow (fonte `facebook_pagina`) | `facebook_get_profile`, `facebook_get_posts` | con accesso: condivisioni ×2 + commenti + reazioni ×0,5; senza: commenti + reazioni (Facebook non pubblica le condivisioni) | 1 + 1 |
| TikTok | — (i dati pubblici bastano) | `tiktok_get_profile`, `tiktok_get_videos` (`sort: "latest"` per la mediana; `"popular"` solo nell'audit per vedere i successi di sempre) | salvataggi + condivisioni | 1 + 1 |
| YouTube | — (accesso al canale da collegare in futuro) | `youtube_get_channel`, `youtube_get_videos` | visualizzazioni; per confrontare video di età diverse usa le visualizzazioni al giorno nei primi 30 giorni (o dalla pubblicazione, se ne ha meno). Shorts e video lunghi hanno mediane **separate** | 1 + 1 |
| LinkedIn (pagina aziendale) | — (l'API delle statistiche è riservata ai partner LinkedIn) | `linkedin_get_company` + `linkedin_get_company_posts` (senza numeri), poi `linkedin_get_post` sui **5 post più recenti** nell'audit e su quelli **del mese** nel report (al massimo 8) | like + commenti ×2 | 2 + 1 per post |

- `null` vuol dire "la piattaforma non lo pubblica", non zero: un contenuto con la misura `null` resta fuori dalla
  mediana. Se il fornitore non risponde (`ProviderUnavailable`), scrivi "dati di <canale> non disponibili" e non
  inventare: i vincitori del mese restano quelli già noti.
- **Mediana**: almeno 8 contenuti con la misura, negli ultimi 12 mesi (per LinkedIn, che ne legge meno: almeno 5, e
  scrivi "mediana su pochi post"). Con meno, niente mediana e niente vincitori: solo i numeri.
- **Resa** di un contenuto = misura ÷ mediana del suo canale (arrotondata a una cifra). **Vincitore** = resa ≥ 2.

## 3. Cosa si salva

Per ogni canale, nel risultato del lavoro (audit: `risultato.social.canali`; report: `risultato.misure.<canale>`):

```json
{"canale": "tiktok", "profilo": "@nome", "fonte": "insights|pubblici", "follower": 0, "stato": "attivo|fermo|da_confermare",
 "metrica": "salvataggi + condivisioni", "mediana": 0, "contenuti_12_mesi": 0, "contenuti_mese": 0,
 "migliori": [{"url": "...", "formato": "video|short|carosello|post|reel", "tema": "...", "hook": "...", "resa": 2.4, "data": "AAAA-MM-GG"}]}
```

`migliori`: massimo 5 per canale, resa ≥ 2. Sono i vincitori che il piano editoriale riprende
(`officina/PIANO-EDITORIALE.md`, sezione 4b).

## 4. Quanto si spende

Con i dati pubblici: **2-4 crediti per canale** (LinkedIn fino a 10). Ordine se il budget stringe: canale principale
→ canali `dedicato` → gli altri. I dati privati non costano crediti. Il numero di follower e i dati privati non vanno
mai su GitHub; nel report sì.
