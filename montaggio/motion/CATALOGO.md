# Catalogo dei componenti verticali (1080 × 1920)

Il codice di ogni componente è in `componenti.html`: aprila con `?anteprima` per vederli girare tutti. Qui c'è
**quando** usarli, con le frasi che lo fanno capire (l'idea del catalogo a "parole dette" viene dal repository
YouTube AI Motion Graphics di TEIN AI, licenza MIT, vedi `../tein/`).

Regola d'oro: **una grafica solo quando aggiunge qualcosa che la voce da sola non fa vedere** (un numero, un
confronto, dei passi, la frase da ricordare). Un video da 30-45 s ne ha **2-4**, mai una per frase.

| # | tipo (`data-tipo`) | quando si dice… | cosa mostra | nota |
|---|---|---|---|---|
| 1 | `numero` | "il 38 percento", "3 volte tanto", una cifra sola | numero grande che conta, più cosa misura | il numero è quello detto, scritto come lo dice |
| 2 | `passi` | "primo… poi… infine", "in tre passaggi" | passi numerati che entrano uno alla volta | massimo 4 passi, 4 parole ciascuno |
| 3 | `prima-dopo` | "prima ci mettevo… adesso…" | due schede, la seconda evidenziata | solo cose vere e verificabili |
| 4 | `confronto` | "X contro Y", "invece di…" | due schede che entrano di lato, bollino sul vincitore | niente marchi dei concorrenti |
| 5 | `prezzo` | "costa…", "a partire da…" | cifra grande e 3 cose incluse | solo prezzi veri del cliente |
| 6 | `imbuto` | "di tutti questi, solo…", numeri che scendono | tre livelli che si restringono | |
| 7 | `linea-tempo` | "nel 2019… poi… oggi", la storia | tappe su una linea che cresce | |
| 8 | `barre` | "da dove arrivano", confronto di quantità | barre che crescono, la prima in colore | dati veri, con la fonte nelle note |
| 9 | `frase` | la frase da ricordare, la chiusura dell'idea | frase grande con una parola evidenziata | una per video |
| 10 | `svela` | titolo del video, nome di un luogo o di un piatto | titolo che si svela, senza scheda, sul girato | serve uno sfondo calmo dietro |
| 11 | `telefono` | "ti arriva un messaggio", "prenoti dal telefono" | telefono con notifiche | usa `data-larghezza="600"` |
| 12 | `elenco` | "cosa c'è dentro", "incluso…" | voci con spunta (✕ per ciò che manca) | massimo 4 voci |
| 13 | `capitolo` | chi parla (prima volta), "parte due" | sottopancia con numero o ruolo | in basso, sopra la zona della didascalia |
| 14 | `luogo` | "siamo a…", "a 10 minuti da…" | percorso disegnato, puntina, nome del luogo | distanze vere |
| 15 | `finale` | l'invito alla fine | frase che entra lettera per lettera + pulsante | il pulsante dice l'azione vera (dove si prenota) |

## Animazioni disponibili (`data-anim`)
`sale` (default) · `pop` · `maschera` · `scrivi` · `lettere` · `conta` (`data-da`, `data-a`, `data-prima`,
`data-dopo`, `data-decimali`) · `disegna` (SVG) · `cresce` (`data-asse` x | y | giu) · `evidenzia` · `scorri` ·
`appare`. Tempi sempre in secondi sul video montato: `data-in`, `data-out`, `data-dur`.

## Tre impaginazioni
- **Volto pieno** (la normale): il girato a tutto schermo, la grafica nello spazio libero accanto alla persona
  (`zone.py` sceglie sopra, sotto, a sinistra o a destra).
- **Senza volto**: riprese di luogo, prodotto o lavoro, o clip del video AI, con voce fuori campo o solo testo:
  la grafica può usare tutta l'area utile.
- **Diviso**: quando la persona occupa tutto (primo piano stretto) e la grafica deve essere grande: il video scende di
  700 px e la grafica usa la parte alta (`componi.py`, colore `--fondo`).

## Misure fisse
- Area utile **x 90-940, y 250-1470** (fuori: nome profilo in alto, didascalia e audio in basso, pulsanti a destra).
- Testo mai sotto **40 px** dopo la scala; titoli da 72 px in su; massimo 6 parole per riga.
- Sottotitoli: banda **y ≈ 1300**, spostati in alto se lì c'è un volto.
- Una grafica resta almeno **2 s + 0,35 s per parola**; entra sulla parola che la nomina o un attimo prima; entra ed
  esce una volta sola; mai due grafiche insieme (i sottotitoli non contano).
