"""Sceglie DOVE mettere ogni grafica, lontano dal corpo e dal volto (i sottotitoli li sistema sottotitoli.py).

  python3 zone.py --lavoro DIR

Legge DIR/piano.json (le grafiche approvate) e DIR/persona.json (se manca: video senza persone, si usa tutta l'area).
piano.json:
  {"grafiche": [{"id": "g1", "tipo": "numero", "in": 3.2, "out": 6.4, "altezza_min": 420}, ...,
                 {"id": "g4", "tipo": "barre", "in": 20, "out": 26, "diviso": true, "motivo_diviso": "concetto_complesso"}]}
Il video resta SEMPRE a tutto schermo: niente riquadri divisi o rimpiccioliti. Per ogni grafica unisce i riquadri
delle persone nell'intervallo (con 40 px d'aria) e cerca, dentro l'area utile (x 90-940, y 250-1470: fuori ci sono
nome profilo, didascalia e pulsanti dell'app), lo spazio libero più grande tra sopra, sotto, a sinistra, a destra:
  1. con la grafica a grandezza normale; 2. con la grafica compatta; 3. sopra il corpo ma mai sul volto.
Se non c'è spazio nemmeno così, la grafica va rivista ("da_rivedere": spostarla, farne un sottotitolo o toglierla).
Unica eccezione, il layout "diviso" (il video scende di 700 px e la grafica usa la parte alta, lo fa componi.py): solo
se in piano.json la grafica ha "diviso": true e "motivo_diviso": "intervista" | "concetto_complesso" | "format".
Scrive DIR/zone.json: {"g1": {"box": [x, y, w, h], "posto": "sopra", "diviso": false, "avviso": ""}, ...} — box è il
valore di data-box nella scena. Le grafiche stanno sopra y 1270: sotto ci sono le didascalie (didascalie.py), salvo
"didascalie": {"stile": "nessuno"}. Con lo stile naturale (nessuna grafica) zone.py si può saltare.
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comune import UTILE, MARGINE_PERSONA, lavoro, leggi, scrivi

DIVISO_AMMESSO = {"intervista", "concetto_complesso", "format"}
X0, Y0, X1, Y1 = UTILE["x"], UTILE["y"], UTILE["x"] + UTILE["w"], UTILE["y"] + UTILE["h"]
BANDA_DIDASCALIE = 1270   # sotto questa altezza ci sono le didascalie (didascalie.py): le grafiche restano sopra


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
    global Y1
    if (piano.get("didascalie") or {}).get("stile") != "nessuno":
        Y1 = BANDA_DIDASCALIE      # la banda bassa è delle didascalie
    out = {}
    for g in piano.get("grafiche", []):
        u = unione(camp, g["in"], g["out"])
        hmin, wmin = g.get("altezza_min", 380), g.get("larghezza_min", 560)
        motivo = str(g.get("motivo_diviso", "")).strip()
        if g.get("diviso") and motivo in DIVISO_AMMESSO:
            # eccezione dichiarata nel piano: intervista, concetto complesso, format
            out[g["id"]] = {"box": [X0, Y0, X1 - X0, 640], "posto": "diviso", "diviso": True,
                            "avviso": f"layout diviso per scelta ({motivo})"}
            continue
        scelta = None
        # 1. spazio libero accanto al corpo, grandezza normale; 2. stesso spazio con la grafica compatta;
        # 3. sopra il corpo ma lontano dal volto (il volto non si copre mai)
        for nome, unione_, (hm, wm) in (("normale", u, (hmin, wmin)), ("compatta", u, (240, 420)),
                                        ("sul corpo", unione(camp, g["in"], g["out"], "volti"), (240, 420))):
            buoni = [(n, b) for n, b in spazi(unione_) if b[3] >= hm and b[2] >= wm]
            if buoni:
                n, b = max(buoni, key=lambda x: x[1][2] * x[1][3])
                scelta = (nome, n, b)
                break
        if scelta:
            nome, n, b = scelta
            h = min(b[3], g.get("altezza_max", 900 if nome == "normale" else 520))
            y = b[1] if n != "sotto" else b[1] + b[3] - h
            avviso = "" if nome == "normale" else ("grafica compatta: poco spazio accanto alla persona" if nome == "compatta"
                                                     else "la grafica passa sopra il corpo (non sul volto): guarda il foglio")
            out[g["id"]] = {"box": [int(b[0]), int(y), int(b[2]), int(h)], "posto": n, "diviso": False, "avviso": avviso}
        else:
            out[g["id"]] = {"box": [], "posto": "nessuno", "diviso": False, "da_rivedere": True,
                            "avviso": "nessuno spazio senza coprire il volto: sposta la grafica in un momento con più spazio, "
                                      "trasformala in sottotitolo o toglila (il video non si divide, salvo i casi ammessi)"}
    scrivi(os.path.join(d, "zone.json"), out)
    for k, v in out.items():
        print(f"• {k}: {v['posto']} {v['box']} {v['avviso']}")


if __name__ == "__main__":
    main()
