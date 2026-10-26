# Banco di prova degli agenti

Un agente si **attiva** (nel registro agenti dell'Agent OS) solo quando supera **tutti** i casi del suo servizio.
Le prove si lanciano con `canale: "prova"` e `sessione: "prova-<id caso>-<data>"`: l'agente lavora esattamente
come con un cliente vero.

## Casi
- Servizi creativi (sito, landing, carosello, annunci, email, brand): i 4 clienti di `clienti.json → creativi`.
- Audit e piano SEO: i 3 casi di `clienti.json → audit` (due attività vere di Vincenzo e un caso senza sito).
- Roadmap, automazioni, formazione: i 4 clienti creativi, con il profilo come contesto.

## Criteri (ogni caso)
| Area | Supera se |
|---|---|
| Consegna | esito scritto in tabella; con `pronta` il link apre da telefono, tutte le pagine e i link interni funzionano |
| Contenuto | completo per il servizio (es. sito: 5-8 pagine piene; audit: tutte le 7 sezioni con dati) |
| Personalizzazione | almeno 5 dettagli che valgono solo per quel cliente; nessun testo che andrebbe bene per chiunque |
| Regole | zero recensioni, contatti, prezzi PrismaPixel o garanzie inventati; dati non confermati segnati "da verificare" |
| Qualità tecnica | controlli del servizio senza errori bloccanti (sito: inspect/lint senza FAIL, 390 px senza scroll orizzontale) |
| Lingua | italiano naturale, niente frasi da brochure né gergo |
| Costi e tempi | entro il budget del servizio; durata annotata |
| Giudizio di Vincenzo | voto 4 o 5 su 5 ("lo manderei a un cliente così com'è") |

Il registro delle prove (data, caso, esito, voto, durata, crediti, problemi) sta nell'Agent OS.
