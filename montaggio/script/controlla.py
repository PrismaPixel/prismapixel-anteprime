"""Controlla la bozza prima di mostrarla: fogli di fotogrammi da guardare + controlli automatici.

  python3 controlla.py --lavoro DIR [--video bozza.mp4] [--fotogramma 8.2]

1. Fogli: DIR/controllo/foglio_NN.jpg, 4 fotogrammi al secondo, 6 × 3 per foglio, con il secondo scritto sotto ogni
   riquadro. Vanno guardati TUTTI, in ordine.
2. Controlli automatici (DIR/controllo.txt), da riquadri.json, persona.json e piano.json:
   - testo sopra un volto (errore) o sopra il corpo (avviso);
   - testo fuori dall'area utile x 90-940, y 250-1470 (errore: lo coprono i pulsanti dell'app);
   - grafica troppo breve: meno di 2 s + 0,35 s per parola (è un lampo);
   - due grafiche nello stesso momento (sottotitoli esclusi);
   - due cambi di grafica a meno di 1,5 s (scatto);
   - durata del video diversa da quella del montato.
--fotogramma S salva un fotogramma a piena grandezza (DIR/controllo/f_S.png) per guardare da vicino un dubbio
prima di chiamarlo errore: i riquadri piccoli del foglio possono ingannare.
"""
import argparse, os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comune import UTILE, durata, esegui, lavoro, leggi
from zone import principali

X0, Y0, X1, Y1 = UTILE["x"], UTILE["y"], UTILE["x"] + UTILE["w"], UTILE["y"] + UTILE["h"]


def tocca(a, b, m=0):
    return not (a["x"] + a["w"] <= b["x"] - m or b["x"] + b["w"] <= a["x"] - m or a["y"] + a["h"] <= b["y"] - m or b["y"] + b["h"] <= a["y"] - m)


def font_file():
    try:
        return subprocess.run(["fc-match", "-f", "%{file}", "DejaVu Sans:bold"], capture_output=True, text=True).stdout.strip()
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lavoro")
    ap.add_argument("--video", default="bozza.mp4")
    ap.add_argument("--fotogramma", type=float)
    a = ap.parse_args()
    d = lavoro(a.lavoro)
    video = os.path.join(d, a.video)
    cart = os.path.join(d, "controllo")
    os.makedirs(cart, exist_ok=True)
    if a.fotogramma is not None:
        src = os.path.join(d, "finale.mp4") if os.path.exists(os.path.join(d, "finale.mp4")) else video
        out = os.path.join(cart, f"f_{a.fotogramma:.2f}.png")
        esegui(["ffmpeg", "-v", "error", "-y", "-ss", str(a.fotogramma), "-i", src, "-frames:v", "1", out])
        print("✓", out); return
    for f in os.listdir(cart):
        if f.startswith("foglio_"):
            os.remove(os.path.join(cart, f))
    ff = font_file()
    testo = f"drawtext=fontfile='{ff}':text='%{{pts\\:hms}}':x=6:y=h-30:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6," if ff else ""
    esegui(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf",
            f"fps=4,scale=240:-2,{testo}tile=6x3:padding=8:margin=8:color=0x333333", os.path.join(cart, "foglio_%02d.jpg")])
    fogli = sorted(f for f in os.listdir(cart) if f.startswith("foglio_"))
    # controlli automatici
    R = leggi(os.path.join(d, "riquadri.json"), {"tempi": [], "campioni": []})
    P = {round(c["t"], 2): c for c in leggi(os.path.join(d, "persona.json"), [])}
    err, avv = [], []
    for c in R["campioni"]:
        pc = P.get(round(c["t"], 2)) or P.get(round(round(c["t"] * 4) / 4, 2))
        for r in c["testi"]:
            dove = f"{c['t']:.2f}s {r['tipo'] or r['id']}"
            if r["x"] < X0 - 4 or r["y"] < Y0 - 4 or r["x"] + r["w"] > X1 + 4 or r["y"] + r["h"] > Y1 + 4:
                err.append(f"{dove}: esce dall'area utile ({r['x']},{r['y']} {r['w']}×{r['h']})")
            if pc:
                if any(tocca(r, v, 10) for v in pc["volti"]):
                    err.append(f"{dove}: copre un volto")
                elif r["tipo"] != "sottotitolo" and any(tocca(r, p) for p in principali(pc["persone"])):
                    avv.append(f"{dove}: tocca il corpo della persona")
    g = sorted([x for x in R["tempi"] if x["tipo"] != "sottotitolo"], key=lambda x: x["in"])
    for x in g:
        minimo = 2 + 0.35 * x["parole"]
        if x["out"] - x["in"] < minimo - 0.05:
            avv.append(f"{x['in']:.2f}s {x['id']}: dura {x['out'] - x['in']:.1f} s, ne servono almeno {minimo:.1f} ({x['parole']} parole)")
    for x, y in zip(g, g[1:]):
        if y["in"] < x["out"] - 0.05:
            err.append(f"{y['in']:.2f}s: {x['id']} e {y['id']} sono sullo schermo insieme")
        elif 0.3 < y["in"] - x["out"] < 1.5:
            avv.append(f"{y['in']:.2f}s: {y['id']} entra {y['in'] - x['out']:.1f} s dopo l'uscita di {x['id']} (scatto: unisci o distanzia)")
    dm, dv = durata(os.path.join(d, "montato.mp4")), durata(video)
    if abs(dm - dv) > 0.2:
        err.append(f"durata {dv:.2f} s diversa dal montato {dm:.2f} s")
    # stesso problema sulla stessa grafica in campioni vicini: una riga sola, con l'intervallo
    def compatta(lst):
        import re
        gruppi = {}
        for m in lst:
            t = re.match(r"([\d.]+)s (\S+)?", m)
            chiave = re.sub(r"[\d.,×()]+", "", m.split(": ", 1)[-1]) + "|" + (t.group(2) if t and t.group(2) else "")
            gruppi.setdefault(chiave, []).append((float(t.group(1)) if t else -1, m))
        out = []
        for v in gruppi.values():
            a, b = v[0][0], v[-1][0]
            out.append(v[0][1] + (f"  (da {a:.2f}s a {b:.2f}s, {len(v)} volte)" if len(v) > 1 else ""))
        return out
    err, avv = compatta(err), compatta(avv)
    righe = [f"Video: {os.path.basename(video)} · {dv:.1f} s · fogli da guardare: {len(fogli)}", "",
             "ERRORI (da correggere prima di mostrarlo):"] + ([f"  ✗ {m}" for m in err] or ["  nessuno"]) + \
            ["", "AVVISI (guarda il foglio e decidi):"] + ([f"  ! {m}" for m in avv] or ["  nessuno"]) + \
            ["", "DA GUARDARE A OCCHIO su ogni foglio: animazioni che ripartono, lampi, testo che arriva tardi, parole doppie,",
             "labiale fuori sincrono (5 momenti), tagli che mangiano l'ultima parola."]
    open(os.path.join(d, "controllo.txt"), "w", encoding="utf-8").write("\n".join(righe) + "\n")
    print("\n".join(righe[:3 + len(err) + 1]))
    print(f"✓ {len(fogli)} fogli in {cart} · rapporto in {os.path.join(d, 'controllo.txt')}")


if __name__ == "__main__":
    main()
