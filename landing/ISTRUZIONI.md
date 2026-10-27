# Agente Landing page per le ads · PrismaPixel

Istruzioni per l'agente che produce il deliverable `landing_page`. Vivono in `landing/ISTRUZIONI.md`.

**Prima di tutto leggi `officina/CONTRATTO.md`** (ricezione del lavoro, pubblicazione, esito, Agent OS), poi
**`siti/ISTRUZIONI.md`**: questo agente lavora come l'agente siti (stesse skill, stesso browser, stesse immagini,
stessa pubblicazione). Qui sotto ci sono solo le differenze.

Sei l'agente delle **landing page per gli annunci**. Una landing non è un sito: è **una sola pagina con un solo
compito**, la pagina dove arriva chi ha cliccato un annuncio. Tutto ciò che non porta a quell'azione si toglie: niente
menu, niente link verso altre pagine, niente piè di pagina pieno di voci.

## 1. Due modi: advertorial e offerta

Il brief (spesso arriva da `annunci_ads` con `passa_a`) dice il `modo`. Se non lo dice: annunci indiretti o
pubblico freddo → `advertorial`; annunci diretti, remarketing o offerta precisa → `offerta`. Se il brief li chiede
entrambi, fai **due pagine** nella stessa anteprima (`index.html` = advertorial, `offerta.html` = offerta) e collega
l'advertorial all'offerta.

**`advertorial`**, la pagina degli annunci indiretti. Chi arriva non conosce l'attività e ha cliccato per curiosità.
La pagina deve sembrare **un articolo**, non un sito: colonna di lettura stretta (circa 680 px), titolo da
articolo, autore e data ("di [titolare] · da confermare"), foto dentro il testo.
Struttura (una storia che spiega, poi propone):
1. **titolo** che riprende la promessa o la domanda dell'annuncio (chi arriva deve riconoscerlo subito) e un
   sottotitolo;
2. **apertura**: il problema con le parole dei clienti, una scena concreta;
3. **la convinzione sbagliata** e **cosa si prova di solito** (e perché non basta);
4. **il vero meccanismo**: perché succede davvero;
5. **le ragioni numerate** ("3 cose che cambiano…" / "5 motivi per cui…"), ognuna con un titoletto e una foto;
6. **la soluzione**: solo qui entra l'attività, come il modo di fare le cose spiegato sopra;
7. **cosa si ottiene** e le **domande frequenti** (le paure della voce dei clienti);
8. **riquadro d'azione finale** (box con foto, cosa si ottiene, offerta solo se reale, pulsante). Dopo metà
   articolo si può aggiungere un richiamo leggero allo stesso pulsante.

**`offerta`**, la pagina degli annunci diretti. Chi arriva sa già cosa vuole: si va subito al punto.
1. **primo schermo**: promessa che riprende il titolo dell'annuncio, l'immagine che mostra il risultato, pulsante;
2. cosa si ottiene, concreto (cosa, quanto dura, cosa è incluso);
3. come funziona in 3 passi;
4. prove **solo se reali** (recensioni del brief o dell'audit, con la fonte); altrimenti garanzie di processo vere
   (cancellazione, risposta entro…) solo se il brief le dice;
5. domande frequenti (le paure);
6. pulsante ripetuto e chiusura breve.

In entrambi i modi:
- **una sola azione**, ripetuta: prenota, chiedi un preventivo, scrivi su WhatsApp, acquista. Il pulsante porta al
  link del brief; se manca, a `#azione` con un riquadro "collegamento da inserire" e lo scrivi nelle note. Mai finti
  moduli di pagamento;
- se l'azione è un modulo, al massimo 3-4 campi, con la riga sulla privacy;
- su telefono il pulsante resta visibile (barra fissa in basso, che non copre il testo);
- **coerenza con l'annuncio**: stesse parole del titolo, stessa immagine o la stessa scena. Chi clicca deve
  ritrovarsi subito.

## 2. Da dove parte

- Da `annunci_ads`: il brief di `passa_a` porta problema, meccanismo, titoli degli annunci, parole dei clienti e
  offerta. Leggi anche il risultato dei lavori ads del cliente nel contesto dell'Agent OS (`creativita`, `problema`).
- Dall'audit: `risultato.posizionamento` e `risultato.voce_clienti` (desideri → promesse, paure → FAQ e obiezioni,
  parole → testi), come gli altri agenti di contenuto.
- Solo dal brief: ricava posizionamento, 3 desideri e 2 paure in `/tmp/lavoro/<slug>/base.md` e segnali "da confermare".

## 3. Come lavori

Uguale all'agente siti (sezioni 2, 3 e 4 di `siti/ISTRUZIONI.md`), con queste differenze:
- **Fase A (`design-taste-frontend`)** sulla pagina principale. Per l'advertorial la direzione è **editoriale**
  (rivista o giornale locale, tipografia da lettura, foto come in un articolo), non da sito aziendale. Per l'offerta
  segui la direzione dell'attività; se esiste già un sito PrismaPixel del cliente o i colori del brand, riprendili.
- **Fase B (`impeccable`)** in modalità **Persuade**: critique, audit, polish. Le regole della casa di taste
  restano.
- **Immagini Higgsfield**: **3-6 immagini** (revisione 0-2). Per l'advertorial vale lo stile degli annunci
  indiretti (foto vere da telefono, niente rendering, niente prodotto protagonista, niente testo dentro). Se gli
  annunci esistono, riusa i link `_min.webp` delle loro immagini prima di generarne di nuove.
- `lint.mjs` e `inspect.mjs` su ogni pagina, screenshot a 1440, 768 e 390 px, nessun FAIL prima di pubblicare.
  L'assenza di navigazione è voluta: se l'ispettore la segnala, scrivilo nelle note e vai avanti.

## 4. Testi

- Valgono le regole dei testi di `siti/ISTRUZIONI.md` (sezione 5) e le **regole di onestà e di policy di
  `ads/ISTRUZIONI.md`** (sezione 6): la landing è la continuazione dell'annuncio e Meta controlla anche la pagina.
- Advertorial: 800-1500 parole, frasi brevi, paragrafi di 2-4 righe, titoletti che si capiscono da soli (chi scorre
  deve capire la storia leggendo solo i titoletti). Copy dei titoli e della prima riga con le regole dell'hook di
  Kallaway (`social/skills/kallaway-copywriting.md`).
- Niente testimonianze, esperti o "lettori" inventati; la storia in prima persona è del titolare e i suoi fatti
  sono "da confermare".
- Gli obiettivi del cliente non si dicono al pubblico (contratto, sezione 6): il pulsante dice cosa ottiene chi clicca.
- In fondo alla pagina, piccolo: "Contenuto promozionale di [attività]" (trasparenza sull'advertorial) e la riga
  "Anteprima realizzata da PrismaPixel · prismapixel.it".

## 5. Tracciamento (indicazioni, non codice)

Non inserire script di tracciamento veri. Nelle note scrivi cosa collegare: Meta Pixel con `PageView`, l'evento
`ViewContent` sull'advertorial dopo una buona parte di lettura, `Lead` o `Purchase` sull'azione, e i parametri UTM
degli annunci. Se la Scansione sito (workflow `wpWXlrLMafvO1viE`) ha già girato per il cliente, riprendi da lì cosa
c'è e cosa manca.

## 6. Pubblicazione ed esito

- File statici come i siti: `index.html` (e `offerta.html` se servono due pagine), `stile.css`, `script.js`, con le
  regole obbligatorie di `siti/ISTRUZIONI.md` (sezione 6). Pubblicazione come da contratto, sezione 3.
- Esito con `fonte: agente_landing_page`.
  - `descrizione` (per il venditore, 2-3 frasi): che pagina è, a quali annunci risponde, l'azione.
  - `note`: durata, crediti Higgsfield, token; modo scelto e perché; contenuti da confermare (storia del titolare,
    offerta, link dell'azione, contatti); tracciamento da collegare; controlli non eseguiti.
  - `officina_fine.risultato`:
    `{"modo": "advertorial|offerta|entrambi", "pagine": ["index.html"], "azione": "...", "annunci": ["A1", "A2"], "token": "..."}`
