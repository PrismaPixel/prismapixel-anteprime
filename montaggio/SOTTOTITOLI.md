# Da dove vengono le didascalie (sottotitoli)

Ricerca del 29 ottobre 2026 sui video verticali più visti della nicchia (turismo in Puglia e Salento, giri in barca,
creator di viaggio e cibo). Le classifiche vengono da TikTok (ricerca per popolarità, ultimo anno); i fotogrammi
sono stati guardati sugli stessi video o sulle copie che i creator pubblicano su YouTube Shorts (TikTok senza accesso
non mostra i video). Si è guardato solo il **metodo** (posizione, grandezza, quante parole, colori): nessun font,
grafica o testo copiato.

| video (visualizzazioni) | parlato | sottotitoli |
|---|---|---|
| 24 ore in Puglia, cibo (1,2 Mln) | no, solo musica | nessuno; solo un titolo elegante all'inizio |
| 3 posti da vedere in Puglia (580 K) | sì, in camera | solo titoli dei posti, scritta a mano con bordo |
| Tre spiagge nel Salento (185 K) | voce fuori campo | **completi**, 1-3 parole, MAIUSCOLO con bordo, parola in giallo, a ⅔ dello schermo; nome del posto in alto con la puntina |
| 5 spiagge sulla costa ionica (176 K) | in camera e fuori campo | **completi**, 1-3 parole, minuscolo corsivo piccolo, bianco, a ¾ dello schermo |
| Centro storico di Lecce, cibo (151 K) | in camera, ritmo alto | **completi**, 1-2 parole grandi, MAIUSCOLO, una parola in giallo; titolo-gancio in alto |
| 3 spiagge segrete in Salento (114 K) | in camera | **completi**, 2-4 parole piccole in alto, nel cielo sopra la testa |
| Escursioni in barca a Leuca (91 K) | voce fuori campo | **completi**, frase intera piccola in minuscolo (1-2 righe), bianca, a ¾ dello schermo |
| Posto pazzesco in Salento (87 K) | voce fuori campo | **completi**, frase piccola minuscola; titolo-gancio in un riquadro bianco nei primi 3 s |
| Salento senza caos (47 K) | in camera | **completi**, 2-3 parole MAIUSCOLO, la parola detta in giallo (karaoke), a ⅔ dello schermo |

Cosa se ne ricava:
1. **Chi parla mette i sottotitoli completi** (7 video su 7 con voce). Solo i video di sola musica non li hanno.
2. Due famiglie: **frase piccola e pulita** in minuscolo (tour in barca, racconti calmi, voce fuori campo) e
   **MAIUSCOLO con bordo e una parola in giallo** (creator in camera, liste, consigli). Una terza, più rara, per i
   video a ritmo alto: **1-2 parole grandi**.
3. Mai più di una riga; blocchi brevi che cambiano con la voce; nessun riquadro dietro il testo (solo ombra o bordo).
4. Posizione tra ⅔ e ¾ dello schermo, sotto il volto e sopra la didascalia dell'app; in alto solo se in basso c'è
   la persona.
5. Il giallo è l'unico colore usato per la parola evidenziata: si legge su mare, cielo e sabbia.
6. Quasi tutti hanno un **titolo-gancio** nei primi 2-3 secondi, separato dai sottotitoli.

Come si traduce negli stili della skill **Omnedia Captions** (`didascalie/`, usata da `script/didascalie.py`):
| famiglia vista nella nicchia | stile della skill | quando |
|---|---|---|
| frase piccola e pulita, nessun colore | `active-word-highlight` tutto bianco | stile video `naturale` |
| parola detta in giallo (karaoke) | `active-word-highlight` con il giallo | stile video `leggero` |
| maiuscolo, giallo sui punti chiave, titoli dei posti | `yellow-authority` con il piano dell'agente | stile video `grafico` |
| titolo elegante (video di cibo e lusso) | `editorial-kinetic` | format di brand |
Posizione: tra ⅔ e ¾ dello schermo come nella nicchia, ma con il fondo del blocco a y 1459 (sopra la didascalia
dell'app) e dentro x 110-910; sale da solo se lì c'è un volto. `script/sottotitoli.py` con i suoi tre preset HTML
(`pulito`, `evidenziato`, `parola`) resta come riserva se Remotion non si può usare.
Da rifare ogni tanto: gli stili cambiano. Bastano 6-8 video con voce, guardati in 8 fotogrammi ciascuno.
