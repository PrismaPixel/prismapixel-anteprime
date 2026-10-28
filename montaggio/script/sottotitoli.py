"""Scrive i sottotitoli parola per parola dentro la scena (HTML, stessi font e stesso motore delle grafiche).

  python3 sottotitoli.py --lavoro DIR

Legge DIR/piano.json → "righe": [{"testo": "zero commissioni", "accento": "zero", "in": 4.1, "out": 5.6}, ...]
(solo le frasi chiave, 1-6 parole, scelte dall'agente), DIR/parole_montate.json (tempi delle parole) e DIR/zone.json
(altezza di ogni riga, lontano dal volto). Ogni parola compare quando viene detta e resta fino alla fine della riga;
una riga di più di 3 parole si divide in due righe brevi, una dopo l'altra. I numeri restano interi ("149.000").
Inserisce il risultato in DIR/scena/scena.html tra <!-- SOTTOTITOLI --> e <!-- /SOTTOTITOLI -->.
"""
import argparse, html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comune import lavoro, leggi

norm = lambda w: re.sub(r"[^\wàèéìòù]", "", w.lower())


def tempi_parole(riga, parole):
    ws = riga["testo"].split()
    vicine = [p for p in parole if riga["in"] - 0.4 <= p["s"] <= riga["out"] + 0.2]
    out, j = [], 0
    for w in ws:
        t = None
        for k in range(j, len(vicine)):
            if norm(vicine[k]["w"]) == norm(w) or (len(norm(w)) > 3 and norm(vicine[k]["w"]).startswith(norm(w)[:4])):
                t = vicine[k]["s"]; j = k + 1; break
        out.append(t)
    # parole non trovate (testo riscritto, numeri in cifre): distribuite tra i tempi noti
    noti = [i for i, t in enumerate(out) if t is not None]
    for i, t in enumerate(out):
        if t is None:
            prima = max([k for k in noti if k < i], default=None)
            dopo = min([k for k in noti if k > i], default=None)
            a = out[prima] if prima is not None else riga["in"]
            b = out[dopo] if dopo is not None else max(a + 0.2, riga["out"] - 0.3)
            n0, n1 = (prima if prima is not None else -1), (dopo if dopo is not None else len(ws))
            out[i] = round(a + (b - a) * (i - n0) / (n1 - n0), 2)
    return list(zip(ws, [max(riga["in"], min(t, riga["out"] - 0.1)) for t in out]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lavoro")
    a = ap.parse_args()
    d = lavoro(a.lavoro)
    piano = leggi(os.path.join(d, "piano.json"), {})
    parole = leggi(os.path.join(d, "parole_montate.json"), [])
    zone = leggi(os.path.join(d, "zone.json"), {})
    ys = zone.get("sottotitoli", [])
    blocchi = []
    for n, r in enumerate(piano.get("righe", [])):
        y = ys[n]["y"] if n < len(ys) else 1300
        tw = tempi_parole(r, parole)
        # righe brevi: al massimo 3 parole, e ogni riga resta almeno 0,7 s (niente lampi di una parola)
        pezzi = []
        for w, t in tw:
            if pezzi and len(pezzi[-1]) < 3 and not (len(pezzi[-1]) >= 2 and t - pezzi[-1][0][1] >= 1.2):
                pezzi[-1].append((w, t))
            elif pezzi and t - pezzi[-1][0][1] < 0.7:
                pezzi[-1].append((w, t))
            else:
                pezzi.append([(w, t)])
        if len(pezzi) > 1 and len(pezzi[-1]) == 1 and len(pezzi[-2]) <= 3:
            pezzi[-2] += pezzi.pop()
        for k, pz in enumerate(pezzi):
            t_in = pz[0][1] - 0.02 if k else r["in"]
            t_out = pezzi[k + 1][0][1] - 0.02 if k + 1 < len(pezzi) else r["out"]
            acc = "" if piano.get("stile", "naturale") == "naturale" else norm(r.get("accento", ""))
            spans = ""
            for w, t in pz:
                cls = ' class="acc"' if acc and norm(w) == acc else ""
                spans += f'<span data-anim="appare" data-dur="0.06" data-in="{t:.2f}"{cls}>{html.escape(w)}</span>'
            blocchi.append(f'<div class="grafica sott" data-tipo="sottotitolo" data-in="{t_in:.2f}" data-out="{t_out:.2f}" data-dur="0.01" style="top:{y - 40}px">{spans}</div>')
    scena = os.path.join(d, "scena", "scena.html")
    if not os.path.exists(scena):
        raise SystemExit("✗ manca scena/scena.html (copiala da motion/scena-modello.html)")
    s = open(scena, encoding="utf-8").read()
    nuovo = "<!-- SOTTOTITOLI -->\n" + "\n".join(blocchi) + "\n<!-- /SOTTOTITOLI -->"
    if "<!-- SOTTOTITOLI -->" in s:
        s = re.sub(r"<!-- SOTTOTITOLI -->.*?<!-- /SOTTOTITOLI -->", lambda m: nuovo, s, flags=re.S)
    else:
        s = s.replace("</div><!-- /palco -->", nuovo + "\n</div><!-- /palco -->")
    open(scena, "w", encoding="utf-8").write(s)
    print(f"✓ {len(blocchi)} righe di sottotitoli nella scena")


if __name__ == "__main__":
    main()
