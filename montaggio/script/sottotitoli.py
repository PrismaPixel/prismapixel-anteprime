"""Sottotitoli COMPLETI: tutto il parlato, a blocchi brevi, nello stile scelto. Li scrive dentro la scena (HTML, stessi
font e stesso motore delle grafiche).

  python3 sottotitoli.py --lavoro DIR

Legge DIR/parole_montate.json (ogni parola detta, con i tempi sul video montato), DIR/piano.json, DIR/persona.json
(volti) e DIR/zone.json (riquadri delle grafiche, se ci sono). Nel piano:
  "sottotitoli": {"preset": "pulito" | "evidenziato" | "parola" | "nessuno",
                  "accenti": ["38%", "grotte"],                 (solo evidenziato e parola: parole in colore)
                  "correzioni": [{"da": "polignano", "a": "Polignano"}],  (errori di trascrizione, mai cambiare il senso)
                  "y": 1400}                                     (facoltativo: altezza della riga, centro del testo)
Senza "preset" decide lo stile del video: naturale e leggero → pulito, grafico → evidenziato.

I tre preset vengono dai video più visti della nicchia (turismo in Puglia e Salento, giri in barca, creator; vedi
SOTTOTITOLI.md):
  pulito       frase in minuscolo come detta, bianca con ombra morbida, 48 px, fino a 5 parole (30 caratteri) su una
               riga, il blocco compare intero e resta fermo. Il più usato nei video naturali e nei tour in barca.
  evidenziato  MAIUSCOLO 58 px con bordo scuro, 1-3 parole (20 caratteri); la parola che si sta dicendo è nel colore
               d'accento (karaoke), più le parole in "accenti". Lo stile dei creator che parlano in camera.
  parola       MAIUSCOLO 76 px, 1-2 parole (14 caratteri) che entrano con un piccolo pop; accento solo su "accenti" e
               numeri. Per video veloci ed energici (cibo, liste, ritmo alto).
I blocchi si chiudono su punteggiatura, pause oltre 0,35 s e limiti di parole/caratteri; mai un blocco di una parola
sola se si può evitare (tranne il preset parola). Ogni parola detta compare: i sottotitoli sono completi.
Altezza: quella del preset (pulito 1400, evidenziato 1270, parola 1250); se lì c'è un volto o una grafica, il blocco
sale o scende (1100, 1500 → 420) restando nell'area utile. Scrive anche DIR/sottotitoli.json per controlla.py.
"""
import argparse, html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comune import UTILE, lavoro, leggi, scrivi
from zone import unione

norm = lambda w: re.sub(r"[^\wàèéìòùáíóú%€$]", "", w.lower())

PRESET = {
    #             parole, caratteri, altezza (centro), corpo px, pausa che chiude il blocco
    "pulito":      dict(parole=5, car=30, y=1400, px=48, pausa=0.35),
    "evidenziato": dict(parole=3, car=20, y=1270, px=58, pausa=0.35),
    "parola":      dict(parole=2, car=14, y=1250, px=76, pausa=0.30),
}
FINE_FRASE = re.compile(r"[.!?…]$")
VIRGOLA = re.compile(r"[,;:]$")
Y_MIN, Y_MAX = UTILE["y"] + 40, UTILE["y"] + UTILE["h"] - 40


def pulisci(w, preset):
    w = w.strip()
    if preset == "pulito":
        return re.sub(r"[.,;:]+$", "", w)          # si tengono ? e !
    return re.sub(r"[.,;:…]+$", "", w)


def span(w, classi, extra=""):
    c = f' class="{" ".join(classi)}"' if classi else ""
    return f"<span{c}{extra}>{html.escape(w)}</span>"


def blocchi(parole, preset):
    p = PRESET[preset]
    out, cur = [], []
    for i, x in enumerate(parole):
        if cur:
            prec = cur[-1]
            testo = " ".join(c["w"] for c in cur + [x])
            chiudi = (len(cur) >= p["parole"] or len(testo) > p["car"]
                      or x["s"] - prec.get("e", prec["s"]) > p["pausa"]
                      or FINE_FRASE.search(prec["w"]) or (VIRGOLA.search(prec["w"]) and len(cur) >= 2))
            if chiudi:
                out.append(cur)
                cur = []
        cur.append(x)
    if cur:
        out.append(cur)
    if preset != "parola":
        # niente blocchi di una parola sola: si unisce al vicino se c'è posto e la pausa è breve
        unito = []
        for b in out:
            if unito and len(b) == 1 and len(unito[-1]) < p["parole"] + 1 \
                    and len(" ".join(c["w"] for c in unito[-1] + b)) <= p["car"] + 6 \
                    and b[0]["s"] - unito[-1][-1].get("e", unito[-1][-1]["s"]) <= 0.6:
                unito[-1] = unito[-1] + b
            else:
                unito.append(b)
        out = unito
        if len(out) > 1 and len(out[0]) == 1 and len(out[1]) < p["parole"] + 1:   # una parola sola in apertura
            out[1] = out[0] + out[1]
            out = out[1:]
    return out


def tempi_blocchi(bl):
    t = []
    for k, b in enumerate(bl):
        t_in = max(0.0, b[0]["s"] - 0.04)
        fine_parlato = b[-1].get("e", b[-1]["s"] + 0.3) + 0.25
        t_out = fine_parlato
        if k + 1 < len(bl):
            nxt = bl[k + 1][0]["s"] - 0.04
            t_out = nxt if nxt - fine_parlato < 0.6 else fine_parlato   # pausa lunga: lo schermo resta pulito
            t_out = min(t_out, nxt)
        if t_out - t_in < 0.5:                                         # mai un lampo
            lim = bl[k + 1][0]["s"] - 0.04 if k + 1 < len(bl) else t_in + 0.5
            t_out = max(t_out, min(t_in + 0.5, lim))
        t.append((round(t_in, 2), round(t_out, 2)))
    return t


def altezza(y0, px, t_in, t_out, camp, graf):
    f = unione(camp, t_in, t_out, "volti") if camp else None
    ostacoli = [(f[1], f[3])] if f else []
    ostacoli += [(z["box"][1], z["box"][1] + z["box"][3]) for gi, go, z in graf if gi < t_out and t_in < go]
    meta = px * 0.75
    for c in (y0, 1400, 1100, 1500, 950, 420):
        c = min(max(c, Y_MIN), Y_MAX)
        if all(c + meta <= a or c - meta >= b for a, b in ostacoli):
            return c, c != y0
    return y0, True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lavoro")
    a = ap.parse_args()
    d = lavoro(a.lavoro)
    piano = leggi(os.path.join(d, "piano.json"), {})
    parole = [dict(x) for x in leggi(os.path.join(d, "parole_montate.json"), []) if str(x.get("w", "")).strip()]
    zone = leggi(os.path.join(d, "zone.json"), {})
    camp = leggi(os.path.join(d, "persona.json"), [])
    cfg = piano.get("sottotitoli") if isinstance(piano.get("sottotitoli"), dict) else {}
    stile = piano.get("stile", "naturale")
    preset = cfg.get("preset") or ("evidenziato" if stile == "grafico" else "pulito")
    if preset not in PRESET and preset != "nessuno":
        raise SystemExit(f"✗ preset sconosciuto: {preset} (pulito, evidenziato, parola, nessuno)")

    # correzioni della trascrizione (nomi di luoghi, maiuscole): parola per parola, mai cambiare il senso
    corr = {norm(c["da"]): c["a"] for c in cfg.get("correzioni", []) if c.get("da")}
    for x in parole:
        if norm(x["w"]) in corr:
            x["w"] = corr[norm(x["w"])] + (x["w"][-1] if re.search(r"[.,;:!?]$", x["w"]) else "")

    righe, html_b = [], []
    if preset != "nessuno":
        p = PRESET[preset]
        y0 = int(cfg.get("y", p["y"]))
        accenti = {norm(w) for w in cfg.get("accenti", [])}
        graf = [(g["in"], g["out"], zone[g["id"]]) for g in piano.get("grafiche", []) if zone.get(g["id"], {}).get("box")]
        bl = blocchi(parole, preset)
        for b, (t_in, t_out) in zip(bl, tempi_blocchi(bl)):
            y, spostato = altezza(y0, p["px"], t_in, t_out, camp, graf)
            ws = [pulisci(x["w"], preset) for x in b]
            top = int(y - p["px"] * 0.6)
            righe.append({"in": t_in, "out": t_out, "y": y, "testo": " ".join(ws), "parole": len(ws),
                          "spostato": spostato, "preset": preset})
            stile_div = f"top:{top}px"
            if preset == "pulito":
                spans = " ".join(f"<span>{html.escape(w)}</span>" for w in ws)
                html_b.append(f'<div class="grafica sott pulito" data-tipo="sottotitolo" data-in="{t_in:.2f}" data-out="{t_out:.2f}" data-dur="0.01" style="{stile_div}">{spans}</div>')
            elif preset == "evidenziato":
                # karaoke: un livello per ogni parola detta, con quella parola in colore
                for k, x in enumerate(b):
                    a_in = t_in if k == 0 else round(x["s"] - 0.02, 2)
                    a_out = t_out if k == len(b) - 1 else round(b[k + 1]["s"] - 0.02, 2)
                    if a_out <= a_in:
                        continue
                    spans = " ".join(span(w, (["ora"] if j == k else []) + (["acc"] if norm(w) in accenti else []))
                                     for j, w in enumerate(ws))
                    html_b.append(f'<div class="grafica sott evidenziato" data-tipo="sottotitolo" data-in="{a_in:.2f}" data-out="{a_out:.2f}" data-dur="0.01" style="{stile_div}">{spans}</div>')
            else:
                # il pop è sulle parole, non sul blocco: il riquadro resta fermo dentro l'area utile
                spans = " ".join(span(w, ["acc"] if (norm(w) in accenti or re.search(r"[0-9]", w)) else [],
                                      f' data-anim="pop" data-in="{t_in:.2f}" data-dur="0.12"') for w in ws)
                html_b.append(f'<div class="grafica sott parola" data-tipo="sottotitolo" data-in="{t_in:.2f}" data-out="{t_out:.2f}" data-dur="0.01" style="{stile_div}">{spans}</div>')

    # copertura: ogni parola detta deve essere in un blocco
    dette = len(parole)
    mostrate = sum(r["parole"] for r in righe)
    scrivi(os.path.join(d, "sottotitoli.json"), {"preset": preset, "parole_dette": dette, "parole_mostrate": mostrate,
                                                 "blocchi": righe})
    scena = os.path.join(d, "scena", "scena.html")
    if not os.path.exists(scena):
        raise SystemExit("✗ manca scena/scena.html (copiala da motion/scena-modello.html)")
    s = open(scena, encoding="utf-8").read()
    nuovo = "<!-- SOTTOTITOLI -->\n" + "\n".join(html_b) + "\n<!-- /SOTTOTITOLI -->"
    if "<!-- SOTTOTITOLI -->" in s:
        s = re.sub(r"<!-- SOTTOTITOLI -->.*?<!-- /SOTTOTITOLI -->", lambda m: nuovo, s, flags=re.S)
    else:
        s = s.replace("</div><!-- /palco -->", nuovo + "\n</div><!-- /palco -->")
    open(scena, "w", encoding="utf-8").write(s)
    sp = sum(1 for r in righe if r["spostato"])
    print(f"✓ sottotitoli {preset}: {len(righe)} blocchi, {mostrate}/{dette} parole"
          + (f", {sp} spostati per non coprire volti o grafiche" if sp else ""))


if __name__ == "__main__":
    main()
