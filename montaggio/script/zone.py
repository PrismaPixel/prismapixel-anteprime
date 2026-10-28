"""Sceglie DOVE mettere ogni grafica e i sottotitoli, lontano dal corpo e dal volto.

  python3 zone.py --lavoro DIR

Legge DIR/piano.json (le grafiche approvate) e DIR/persona.json (se manca: video senza persone, si usa tutta l'area).
piano.json:
  {"grafiche": [{"id": "g1", "tipo": "numero", "in": 3.2, "out": 6.4, "altezza_min": 420}, ...],
   "sottotitoli": true}
Per ogni grafica unisce i riquadri delle persone nell'intervallo (con 40 px d'aria) e cerca, dentro l'area utile
(x 90-940, y 250-1470: fuori ci sono nome profilo, didascalia e pulsanti dell'app), lo spazio libero più grande tra:
sopra la persona, sotto, a sinistra, a destra. Se nessuno spazio è abbastanza grande (primo piano stretto), propone il
layout "diviso": il video scende di 700 px e la grafica usa la parte alta (lo fa componi.py).
Scrive DIR/zone.json: {"g1": {"box": [x, y, w, h], "posto": "sopra", "diviso": false, "avviso": ""}, ...,
"sottotitoli": [{"in": .., "out": .., "y": 1300}, ...]} — box è il valore di data-box nella scena.
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comune import UTILE, MARGINE_PERSONA, lavoro, leggi, scrivi

X0, Y0, X1, Y1 = UTILE["x"], UTILE["y"], UTILE["x"] + UTILE["w"], UTILE["y"] + UTILE["h"]


def principali(lst):
    """Le persone da non coprire: la più grande e chi è grande quasi come lei. Se sono tutte piccole (folla lontana),
    solo la più grande: coprire chi passa sullo sfondo va bene."""
    if not lst:
        return []
    mx = max(p["h"] for p in lst)
    if mx < 0.2 * 1920:
        return [max(lst, key=lambda p: p["h"])]
    return [p for p in lst if p["h"] >= 0.6 * mx]


def unione(campioni, t0, t1, chiave="persone"):
    rs = [p for c in campioni if t0 - 0.25 <= c["t"] <= t1 + 0.25 for p in (principali(c[chiave]) if chiave == "persone" else c[chiave])]
    if not rs:
        return None
    m = MARGINE_PERSONA
    return (min(r["x"] for r in rs) - m, min(r["y"] for r in rs) - m,
            max(r["x"] + r["w"] for r in rs) + m, max(r["y"] + r["h"] for r in rs) + m)


def spazi(u):
    if not u:
        return [("pieno", (X0, Y0, X1 - X0, Y1 - Y0))]
    ux0, uy0, ux1, uy1 = u
    c = []
    if uy0 - Y0 > 0: c.append(("sopra", (X0, Y0, X1 - X0, min(uy0, Y1) - Y0)))
    if Y1 - uy1 > 0: c.append(("sotto", (X0, max(uy1, Y0), X1 - X0, Y1 - max(uy1, Y0))))
    if ux0 - X0 > 0: c.append(("sinistra", (X0, Y0, min(ux0, X1) - X0, Y1 - Y0)))
    if X1 - ux1 > 0: c.append(("destra", (max(ux1, X0), Y0, X1 - max(ux1, X0), Y1 - Y0)))
    return [(n, b) for n, b in c if b[2] > 0 and b[3] > 0]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lavoro")
    a = ap.parse_args()
    d = lavoro(a.lavoro)
    piano = leggi(os.path.join(d, "piano.json"))
    if not piano:
        raise SystemExit("✗ manca piano.json (le grafiche approvate)")
    camp = leggi(os.path.join(d, "persona.json"), [])
    out = {}
    for g in piano.get("grafiche", []):
        u = unione(camp, g["in"], g["out"])
        hmin, wmin = g.get("altezza_min", 380), g.get("larghezza_min", 560)
        buoni = [(n, b) for n, b in spazi(u) if b[3] >= hmin and b[2] >= wmin]
        if buoni:
            n, b = max(buoni, key=lambda x: x[1][2] * x[1][3])
            # non serve tutta l'altezza: la scheda si appoggia vicino al bordo libero più lontano dalla persona
            h = min(b[3], g.get("altezza_max", 900))
            y = b[1] if n != "sotto" else b[1] + b[3] - h
            out[g["id"]] = {"box": [int(b[0]), int(y), int(b[2]), int(h)], "posto": n, "diviso": False, "avviso": ""}
        else:
            out[g["id"]] = {"box": [X0, Y0, X1 - X0, 640], "posto": "diviso", "diviso": True,
                            "avviso": "nessuno spazio libero accanto alla persona: layout diviso (video spostato in basso di 700 px)"}
    # sottotitoli: banda bassa (y 1300), salvo che lì ci sia un volto; poi in alto
    sott = []
    for r in piano.get("righe", []):
        f = unione(camp, r["in"], r["out"], "volti")
        y = 1300
        if f and f[1] < 1380 and f[3] > 1180:
            y = 1100 if f[1] > 1200 else 420
        sott.append({"in": r["in"], "out": r["out"], "y": y})
    out["sottotitoli"] = sott
    scrivi(os.path.join(d, "zone.json"), out)
    for k, v in out.items():
        if k != "sottotitoli":
            print(f"• {k}: {v['posto']} {v['box']} {v['avviso']}")


if __name__ == "__main__":
    main()
