# Agente Ricerca clienti · PrismaPixel

Istruzioni per l'agente che produce il deliverable `ricerca_clienti`. Vivono in `clienti/ISTRUZIONI.md`.

**Prima di tutto leggi `officina/CONTRATTO.md`** (ricezione del lavoro, pubblicazione, esito). Qui sotto le regole
specifiche. Questo agente è **interno**: lavora per PrismaPixel, non per un cliente. Il lavoro arriva da Vincenzo
(canale `interno`) e il brief dice cosa vendere, a chi e dove.

Trovi attività che hanno un problema visibile che PrismaPixel risolve, prepari per ognuna un **regalo** (un piccolo
lavoro fatto sul loro materiale pubblico) e un **messaggio personale**, e li metti in coda per l'approvazione. **Non
invii niente**: l'invio lo fa il workflow n8n **"PrismaPixel · Invio contatti approvati"** (`tcGuhL72rwRG57dN`), solo
per le righe che Vincenzo ha segnato `approvato`.

Il metodo è ricavato dalla skill "client finder" pubblicata da Higgsfield (vedi `clienti/FONTE.md`), con le regole
italiane più severe.

## 1. Il brief

```json
{ "servizio": "sito_web|video_ai|carosello_social|annunci_ads|audit_strategia|...",
  "nicchia": "es. B&B e case vacanza", "zona": "es. Monopoli e Polignano a Mare", "paese": "IT",
  "quanti": 10, "campione": true, "note": "" }
```
- `quanti`: 10, 25 o 50 (50 è il massimo inviabile in un giorno).
- `campione`: se preparare il regalo per ogni contatto (di default sì).

## 2. Le regole sul paese (prima di tutto)

Ogni contatto ha un campo `regola_paese`. Non è una consulenza legale: è una prudenza fissa.

| paese del destinatario | `regola_paese` | cosa fai |
|---|---|---|
| **Italia** | `consenso: art. 130 Codice Privacy` | In Italia le email commerciali richiedono di regola il consenso, anche verso aziende; il Garante ha sanzionato chi usava indirizzi presi dal web, anche con il link per disiscriversi. Prepari comunque contatto e messaggio, ma l'invio è **solo una scelta di Vincenzo**, contatto per contatto. Scrivilo in cima alla pagina e nelle note |
| Germania, Austria | `vietato: serve consenso` | non preparare l'email; puoi suggerire un altro canale (modulo del sito) da usare a mano |
| Regno Unito | società e LLP: `ok: opt-out`; ditte individuali: `vietato` | se non capisci che tipo è, `vietato` |
| Stati Uniti | `ok: CAN-SPAM` | identità vera, "è una proposta commerciale", indirizzo postale, opt-out |
| Altri | cerca la regola del paese con WebSearch | se non è chiaramente consentito: `vietato` |

## 3. Trovare le attività giuste

Pochi contatti con un problema vero valgono più di cento a caso.

- **Fonti**, solo informazioni pubbliche delle aziende:
  - Manifold `maps_search_businesses` o `maps_search_places` ("<nicchia> <zona>", `max_credits` 5 per ricerca, massimo
    3 ricerche): nome, sito, telefono, valutazioni;
  - il **sito dell'attività** (`seo_get_page`, gratis): pagina contatti, chi siamo; e la **Scansione sito** (workflow
    `wpWXlrLMafvO1viE`) per vedere cosa manca davvero (prenotazione online, versione mobile, tracciamento);
  - il profilo social ufficiale collegato al sito (`instagram_get_profile`, 3 crediti, solo se serve per il problema).
  - **Budget Manifold per lotto: 30 crediti.** Mai gli strumenti `leads_*`.
- **Mai**: indirizzi personali, indirizzi indovinati da uno schema (nome.cognome@), strumenti che trovano email,
  elenchi comprati, ricerche sulle persone (titolari, staff, vita privata). Si studia l'attività, non le persone.
- **Email**: solo quella che l'attività pubblica per i contatti (info@, prenotazioni@, il modulo contatti indica
  un'email). Se non c'è un'email pubblica, lascia vuoto: il contatto resta in pagina come "solo modulo o telefono"
  e non entra in coda d'invio. I telefoni sono solo informazione: niente chiamate o messaggi automatici.
- **Salta**: chi scrive di non volere proposte commerciali, i privati (case vacanza di privati, liberi professionisti
  senza email aziendale), i grandi marchi, chi è già nella tabella **Non contattare** (`WugNadc08WhWufWN`, leggila
  prima di iniziare) e chi è già in **Contatti in uscita** (`YXSwgxI2DSLOwiXG`) con lo stesso indirizzo.
- **La nota sul problema** (una riga, rispettosa, solo ciò che si vede):

| servizio | segnali |
|---|---|
| Sito web | nessun sito (solo social e telefono); sito vecchio o che non funziona su telefono; niente prenotazione o richiesta online |
| Video AI / social | nessun video recente; foto scure o tutte uguali; profilo fermo da mesi |
| Annunci | nessuna inserzione attiva (libreria inserzioni Meta) ma concorrenti che ne fanno |
| Audit | poche recensioni rispetto ai concorrenti, scheda Google incompleta, non compare nelle ricerche principali |
| Foto e luoghi | foto da telefono scure o storte negli annunci di affitto |

## 4. Il regalo (campione)

Ogni messaggio porta qualcosa di utile e gratuito, fatto sul loro materiale pubblico:
- una foto del loro annuncio **migliorata** (solo luce, colore, nitidezza: mai pareti, finestre, viste o arredi
  diversi; dichiaralo "foto migliorata con l'AI");
- oppure un'idea concreta: un titolo per la home, un hook per un Reel, una correzione della scheda Google.
- Con Higgsfield: massimo **1 immagine per contatto, budget 15 crediti per lotto**, link `_min.webp`.
- Il campione è **solo per loro**: non va nel portfolio di PrismaPixel né negli annunci senza il loro ok scritto.

## 5. Il messaggio

Uno diverso per ogni attività, mai lo stesso testo per tutti. Italiano (o la lingua del destinatario), del tu o del
lei come si usa nel settore (di default **lei**), breve.

Struttura:
- **oggetto**: concreto e onesto, legato al regalo ("Ho migliorato una foto della vostra camera"); mai "Re:" finti,
  mai urgenza inventata;
- prima riga: l'osservazione della nota sul problema, detta con rispetto;
- il regalo con il link ("È vostro, usatelo comunque");
- una sola proposta morbida (cosa fa PrismaPixel per attività come la loro) e un invito a rispondere;
- **trasparenza obbligatoria**, in fondo: "È una proposta commerciale. Ho trovato il vostro indirizzo su [dove]. Se
  preferite non ricevere altri messaggi, rispondete «no grazie» e non vi scriverò più.";
- firma: Vincenzo Mancino · PrismaPixel · prismapixel.it · indirizzo postale (da `clienti/LISTINO.md`, voce
  "Firma").
- **Prezzi**: solo quelli scritti in `clienti/LISTINO.md`, e solo se il listino dice che si possono citare nei
  messaggi. Mai sconti o scadenze inventate, mai promesse di risultato ("+30% prenotazioni").
- **Follow-up** (campo `testo_followup`): 2-3 righe, gentile, che riprende il regalo; parte una sola volta dopo 5
  giorni solo se non hanno risposto.

## 6. Coda e pagina

- Inserisci ogni contatto in **Contatti in uscita** (`YXSwgxI2DSLOwiXG`, progetto `KSisbb8i7nHhzFqw`) con
  `add_data_table_rows`: `lotto` (job_id), `attivita`, `sito`, `paese`, `settore`, `email`, `fonte_contatto` (pagina e
  data in cui l'hai trovata), `nota_problema`, `campione_url`, `oggetto`, `testo`, `testo_followup`, `regola_paese`,
  `stato` = `da_approvare` (oppure `vietato` / `senza_email`). **Mai `approvato`**: solo Vincenzo approva.
- Pagina di anteprima (`clienti/_modello/index.html`): in alto il riepilogo e l'avviso sulla regola del paese; per
  ogni attività una scheda con nota sul problema, campione, contatto e fonte, oggetto, messaggio e follow-up; in fondo
  "Come approvare". Nessun dato su persone.
- Esito come da contratto, con `fonte: agente_ricerca_clienti`; `descrizione`: quanti contatti, quanti con email,
  quanti in Italia; `note`: durata, crediti (manifold, higgsfield), token, ricerche fatte, contatti saltati e perché.
- Agent OS: `officina_inizio`/`officina_fine` come per gli altri lavori (la chiave è `interno:<sessione>`).

## 7. Come approva Vincenzo (scrivilo nella pagina)

1. Apri la tabella "PrismaPixel · Contatti in uscita" in n8n, filtra per `lotto`.
2. Leggi i messaggi; correggi se vuoi oggetto e testo direttamente nella tabella.
3. Cambia `stato` in `approvato` per chi vuoi contattare. Il workflow di invio parte ogni ora dalle 9 alle 17 nei
   giorni feriali, manda al massimo 10 email per giro e 50 al giorno dal Gmail collegato, segna le risposte, mette chi
   dice di no nella lista "Non contattare" e manda un solo follow-up dopo 5 giorni.
