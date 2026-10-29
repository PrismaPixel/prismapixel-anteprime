# Fonti dell'agente Montaggio video e motion

1. **Video Editor Starter Kit** (zip fornito da Vincenzo, ottobre 2026): skill per Claude Code che monta un video
   parlato un passaggio alla volta (trascrizione, taglio delle riprese doppie e delle pause, sottotitoli parola per
   parola, poche grafiche, controllo dei fotogrammi, regole che si riscrivono a ogni correzione).
   **Nessuna licenza indicata**: non copiamo file, testi o script. Abbiamo ripreso solo il metodo (l'ordine dei
   passaggi, le fermate per l'approvazione, il principio "una correzione riscrive una regola, non ne aggiunge una")
   e scritto da zero istruzioni e script in `montaggio/script/`.
2. **YouTube AI Motion Graphics** di TEIN AI (https://github.com/sirioberati/YouTube-AI-Motion-Graphics, commit
   `52b5b94`, 27/10/2026), **licenza MIT**: copiati in `montaggio/tein/` le 74 grafiche 16:9 (`boards/`), le tre skill
   (`explainer-board-brief`, `explainer-board-system`, `board-sync`), il file dei controlli e lo script di esportazione
   `tools/export.py`, con la licenza originale. Servono per i video YouTube 16:9 (livello `lungo`). Dal repository
   vengono anche le idee del catalogo "per frasi dette", del tempo fermato fotogramma per fotogramma e delle zone da
   tenere libere, applicate al formato verticale nei file nostri di `montaggio/motion/`.
3. **Modelli usati dagli script** (scaricati da `prepara.py` al momento del lavoro, non nel repository):
   - NVIDIA Parakeet TDT 0.6B v3 (CC-BY-4.0), convertito per sherpa-onnx da k2-fsa (Apache-2.0): trascrizione con i
     tempi delle parole in 25 lingue europee; Silero VAD (MIT);
   - YOLOX-S (Apache-2.0) e YuNet (MIT) dall'OpenCV Model Zoo: corpo e volto delle persone.
4. **Formato verticale**: misure e zone sicure nostre, le stesse dell'agente Video AI (margini 250 in alto, 450 in
   basso, 90 a sinistra, 140 a destra su 1080 × 1920).

## Didascalie: skill Omnedia Captions (MIT)
`didascalie/omnedia-captions/` è la skill https://github.com/omnedia/skills/tree/master/video/captions (commit
`29bf674`, © 2026 Omnedia, licenza MIT), usata su richiesta di Vincenzo per le didascalie dei verticali. Tolti i due
stili con font senza licenza commerciale (Brunson, Brush Script MT); tre piccole modifiche segnate "PrismaPixel" nel
codice: elenco e motivi in `didascalie/MODIFICHE.md`. I font rimasti sono OFL o di pubblico dominio (licenze nelle
cartelle `styles/*/fonts/`). Remotion (il motore) è gratuito fino a 3 persone in azienda: oltre serve la licenza.

