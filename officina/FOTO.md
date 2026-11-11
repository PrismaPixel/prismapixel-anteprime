# Foto del cliente · come le usano gli agenti

Vale per caroselli e post (`carosello_social`), annunci (`annunci_ads`), landing (`landing_page`), siti (`sito_web`) e
video AI (`video_ai`).

**Video AI (`video_ai`)**: le foto vere del cliente vengono **prima** di quelle generate (luogo e prodotto partono
da quelle; il prodotto resta identico), secondo l'ordine di scelta qui sotto.

**Regola per caroselli, post, annunci, siti e landing:** le immagini le genera sempre Higgsfield seguendo la
reference (il pin, i riferimenti degli annunci, il sito modello), anche se il cliente ha già foto, e
il cliente le rifà uguali con la lista scatti (`social/ISTRUZIONI.md`, sezione 6;
`ads/ISTRUZIONI.md`, sezione 5; `siti/ISTRUZIONI.md`, sezione 4, che vale anche per le landing). Le foto che il cliente ha già servono come **riferimento del soggetto**
(com'è fatto il suo prodotto, il suo locale); quando arrivano quelle rifatte, sostituiscono le generate. Negli annunci
le immagini generate restano proposte: su Meta vanno solo quelli con le foto vere del cliente. Il servizio qui sotto
(elenco, importa, migliorare) resta per leggere le foto del cliente e per mettere al loro posto quelle rifatte;
l'ordine di scelta che segue vale per il video AI e dove un'istruzione lo richiama esplicitamente.

## Ordine di scelta

1. **Foto del cliente** (`origine`: `cliente`, `drive`, `dropbox`): caricate da lui con il link personale.
2. **Foto dei canali del cliente** (`sito`, `instagram`, `facebook`, `google_business`): sono sue. Solo dal suo sito,
   dai suoi profili e dalle foto che **lui** ha caricato sulla sua scheda Google. Mai le foto dei clienti nelle
   recensioni, mai foto di concorrenti o di altri siti.
3. **Foto d'archivio** (`archivio`, Pexels e Unsplash, uso commerciale libero): solo per ambientazioni generiche
   (mare, città, ingredienti, mani al lavoro). Mai presentate come il locale, il prodotto o il team del cliente.
4. **Immagini generate con Higgsfield**: solo se le prime tre non bastano, dichiarate come "immagini d'esempio" nelle note.

Se le foto del cliente mancano o sono poche, scrivilo nelle note dell'esito con il link per caricarle
(`richiesta.link` nell'elenco); se il link non c'è ancora, scrivi "chiedere le foto: modulo «Richiedi foto»".

## Servizio n8n «PrismaPixel · Foto del cliente»

Si chiama con lo strumento n8n `execute_workflow` (workflow `ptCXpEMzTaJiQ7uP`, trigger `Officina · foto`,
`webhookData.body`), poi si legge l'esito con `get_workflow_execution` (nodo `Rispondi esito` o `Rispondi elenco`).
Vale solo per un `job_id` aperto degli ultimi 45 giorni.

| azione | body | risposta |
|---|---|---|
| `elenco` | `{azione, job_id}` | `foto[]` con `id`, `origine`, `url` (link firmato valido 180 giorni, usalo anche nelle anteprime), `larghezza`, `altezza`, `scheda`, `autore`, `licenza` |
| `importa` | `{azione, job_id, url, origine, fonte_url?, autore?, licenza?, deriva_da?, modifica?, download_location?}` | `{ok, id}` della nuova foto |
| `archivio` | `{azione, job_id, query, orientamento?}` (`portrait`, `landscape`, `square`; query in inglese) | `risultati[]` con `anteprima`, `scarica`, `autore`, `pagina`, `licenza`, `download_location` |

Per l'elenco va bene anche l'SQL: `select foto_per_lavoro('<job_id>');`

La **scheda** di ogni foto la prepara Claude entro 15 minuti dal caricamento: `soggetto`, `tipo`, `qualita` (1-5),
`problemi`, `persone_riconoscibili`, `adatta` (carosello, post, annuncio, sfondo con testo), `formati`, `migliorie`,
`nota`. Scegli con la scheda; guarda la foto (link `url`) prima di usarla in un contenuto.

### Importare dai canali del cliente

- **Sito**: le immagini della pagina (servizio "Scansione sito" o l'HTML), solo quelle di contenuto: niente icone,
  loghi di terzi, banner di cookie. `origine: "sito"`, `fonte_url` = pagina.
- **Instagram / Facebook**: dal profilo del cliente (Manifold `instagram_get_posts`, `facebook_get_posts`, se
  disponibili). `origine: "instagram"` o `"facebook"`, `fonte_url` = link del post. Mai foto dove il cliente è solo
  taggato da altri.
- **Archivio**: dopo `archivio`, importa solo le foto scelte con `origine: "archivio"`, `autore`, `licenza`,
  `fonte_url` = `pagina` e, per Unsplash, `download_location` (lo chiede la loro licenza). Nelle note dell'esito
  scrivi "foto d'archivio: <autore> su <Pexels|Unsplash>".

## Migliorare con Higgsfield (senza falsare)

Solo se la scheda indica `migliorie` o qualità 2-3:

1. `media_import_url` con l'`url` della foto (il link firmato funziona) → `media_id`.
2. Lo strumento giusto, con `max_credits`:
   - `aumenta_risoluzione` → `upscale_image`;
   - `allarga_inquadratura` (4:5, 9:16) → `outpaint_image`;
   - `togli_sfondo` (prodotti) → `remove_background`;
   - `luce` → generazione da immagine con istruzione "stessa foto, stessa scena, solo luce ed esposizione corrette".
3. Salva il risultato: `importa` con `url` del risultato Higgsfield, `origine: "higgsfield"`, `deriva_da` = id della
   foto di partenza, `modifica` = cosa hai fatto ("aumentata la risoluzione 2x", "allargata a 4:5").

**Mai** cambiare ciò che la foto mostra: niente piatti diversi, prodotti diversi, locali più grandi, persone
aggiunte o tolte, scritte o loghi nuovi. Il cliente deve riconoscere le sue cose. Una foto con persone
riconoscibili si migliora solo nella luce e nella risoluzione.

Budget: rientra nei crediti Higgsfield del servizio (vedi le istruzioni del deliverable). Nelle note scrivi quante
foto hai migliorato e con cosa.

## Note dell'esito

Aggiungi una riga: `foto: <N> del cliente, <N> dai suoi canali, <N> d'archivio, <N> migliorate, <N> generate`.
