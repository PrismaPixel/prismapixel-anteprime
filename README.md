# prismapixel-anteprime

Istruzioni, modelli e skill degli agenti di PrismaPixel. **Le anteprime per i clienti non si pubblicano qui**:
gli agenti le salvano nel servizio Anteprime su n8n (vedi `officina/CONTRATTO.md`).

- `officina/CONTRATTO.md` · contratto comune: lavoro in arrivo, pubblicazione, esito.
- `siti/` · Agente Siti Web & E-commerce: `siti/ISTRUZIONI.md`, skill di design in `siti/skills/`, demo in `siti/corte-dei-fichi-demo/`.
- `audit/` · Agente Audit digitale e strategia: `audit/ISTRUZIONI.md`, modello in `audit/_modello/`.
- `social/` · Agente Caroselli e Post (`carosello_social`): `social/ISTRUZIONI.md`, skill Kallaway in `social/skills/`, visore dell'anteprima (senza stile) in `social/_modello/`, controllo slide in `social/tools/`. Il design nasce solo dai riferimenti Pinterest (workflow n8n "PrismaPixel · Riferimenti Pinterest"), nessuno stile predefinito.
- `video/` · Agente Script video (`script_video`): `video/ISTRUZIONI.md`, skill WATCH (MIT) in `video/skills/`, visore in `video/_modello/`. Video con o senza faccia: copione, testi a schermo, storyboard 9:16 disegnato in HTML/SVG (senza immagini generate), formato "Racconto di scoperta" per i video sull'offerta, e didascalia.
- `email/` · Agente Email marketing (`sequenza_email`): `email/ISTRUZIONI.md`, visore casella di posta in `email/_modello/`, controllo email in `email/tools/`. Parte dal posizionamento e dalla voce dei clienti dell'audit, oppure dal brief.
- `ads/` · Agente Ads (`annunci_ads`): `ads/ISTRUZIONI.md`, visore del feed Meta e della strategia in `ads/_modello/`. Annunci indiretti (metodo Indirect Ads di Nu Reach, riassunto con parole nostre) e diretti come grafiche (riferimenti Pinterest formato "annuncio" + 5 principi degli annunci statici), immagini Higgsfield, piano dei test.
- `landing/` · Agente Landing page per le ads (`landing_page`): `landing/ISTRUZIONI.md`. Advertorial per gli indiretti e landing d'offerta per i diretti, con le stesse skill e gli stessi controlli dell'agente siti.
- `strategia/` · Agente Consulenza strategica (`roadmap`): `strategia/ISTRUZIONI.md`, skill Hormozi (MIT) in `strategia/skills/hormozi/`, modello in `strategia/_modello/`. Diagnosi dell'offerta con l'equazione del valore, offerta proposta, obiezioni, livelli e prezzi, angoli, priorità e roadmap 30-60-90.
- Servizi n8n per gli agenti: "PrismaPixel · Riferimenti Pinterest" (`1oek9PrhT8PB9Oa5`) e "PrismaPixel · Scansione sito" (`wpWXlrLMafvO1viE`, strumenti davvero presenti su un sito, anche caricati da JavaScript).
- `prove/` · banco di prova: i 4 clienti di test e i criteri per attivare un agente.
