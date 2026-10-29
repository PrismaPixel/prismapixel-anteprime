# Skill Omnedia Captions: provenienza e modifiche

`omnedia-captions/` è la skill **Omnedia Captions** 1.0.0 da https://github.com/omnedia/skills/tree/master/video/captions
(commit `29bf6748a7d0696210bfd950ce2f46a0aa054b39`), licenza **MIT** (`omnedia-captions/LICENSE`, © 2026 Omnedia).
La usiamo per le didascalie dei video verticali, tramite `../script/didascalie.py`.

## Cosa abbiamo tolto
- Gli stili **Brunson Red Script** e **Vermilion Brush Editorial**, con i loro font (Brunson: solo uso personale;
  Brush Script MT: Monotype, nessuna licenza di ridistribuzione) e i test/gallerie collegati: la loro stessa nota dice
  che l'uso commerciale non è stabilito. Il codice dei due stili resta (MIT), ma senza font e fuori dal catalogo non si
  possono scegliere. Restano quattro stili con font liberi: Active Word Highlight (Inter, OFL), Yellow Authority
  (Poppins e Montserrat, OFL), Editorial Kinetic (Poppins, Libre Baskerville OFL, Lazy Dog pubblico dominio),
  Montserrat Difference (OFL).

## Cosa abbiamo cambiato (segnato con "PrismaPixel" nel codice)
1. `assets/caption-code/render.mjs` e `assets/caption-code/yellow-plan.mjs`: usano il browser indicato in
   `REMOTION_BROWSER_EXECUTABLE` (il Chromium già installato), perché l'ambiente non raggiunge `remotion.media` da cui
   Remotion scarica il suo. Senza la variabile si comportano come l'originale.
2. `assets/caption-code/src/CaptionOverlay.tsx` (Active Word Highlight): opzioni `leftRatio` e `widthRatio` per i
   margini; di base 8% e 84% come l'originale. Ci servono per stare nell'area utile delle app (x 90-940).
3. `assets/caption-code/src/editorial.mjs` (Editorial Kinetic): opzioni `widthRatio` e `centerXRatio`, stesso motivo;
   di base 84% e centro come l'originale.

## Come la usiamo rispetto alle sue istruzioni
- La skill chiede il **plugin Remotion di Codex**. Qui non c'è Codex: l'agente legge le istruzioni ufficiali di
  Remotion (https://github.com/remotion-dev/skills, scaricate da `prepara.py`) e crea il progetto con il comando che
  quelle istruzioni indicano (`npx create-video@latest --yes --blank --no-tailwind`, poi `npm i`). Il controllo della
  skill (`doctor`, `prepare`) riceve il percorso di quelle istruzioni.
- I **tempi** delle parole vengono dalla nostra trascrizione (Parakeet, un tempo per parola) dopo i tagli: sono già
  tempi per parola, quindi non serve l'allineamento con Whisper della skill.
- La skill consegna solo il MOV trasparente e dice di non fare controlli dopo il render. Noi il MOV lo mettiamo sopra
  il video (`componi.py`) e **controlliamo il video finito** (`controlla.py`: didascalie complete, dentro l'area utile,
  mai sul volto), perché il cliente riceve il video montato, non un livello da montare.
- Yellow Authority di solito sceglie solo le frasi utili; su richiesta di Vincenzo le didascalie sono **complete**
  (la skill lo prevede: "keep a verbatim display when the user explicitly requests full subtitles").
- Remotion è gratuito per aziende fino a 3 persone (https://www.remotion.pro/license): oltre serve la licenza.
