"""Unisce video montato, grafiche (PNG della scena), didascalie (DIR/didascalie.mov, trasparente) e la voce.

  python3 componi.py --lavoro DIR --bozza      → DIR/bozza.mp4  (540 × 960, leggera, per l'anteprima)
  python3 componi.py --lavoro DIR              → DIR/finale.mp4 (1080 × 1920, H.264 alta qualità, per pubblicare)

Layout "diviso" (da zone.json, quando una grafica non ha spazio accanto alla persona): in quell'intervallo il video
scende di 700 px e la parte alta resta libera per la grafica, con il colore --carta del tema (opzione --fondo).
Le grafiche devono essere state rese con lo stesso formato (rendi_grafiche.py, con o senza --bozza); senza grafiche
(stile naturale) basta didascalie.py. Le didascalie stanno sopra a tutto.
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comune import W, H, FPS, durata, esegui, lavoro, leggi


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lavoro")
    ap.add_argument("--bozza", action="store_true")
    ap.add_argument("--fondo", default="#ffffff", help="colore della parte alta nel layout diviso")
    a = ap.parse_args()
    d = lavoro(a.lavoro)
    base = os.path.join(d, "montato.mp4")
    graf = os.path.join(d, "grafiche_bozza" if a.bozza else "grafiche")
    did = os.path.join(d, "didascalie.mov")
    ha_graf = os.path.isdir(graf) and any(f.endswith(".png") for f in os.listdir(graf))
    if not ha_graf and not os.path.exists(did):
        raise SystemExit(f"✗ mancano grafiche e didascalie: lancia rendi_grafiche.py{' --bozza' if a.bozza else ''} "
                         "e/o didascalie.py")
    s = 0.5 if a.bozza else 1
    w, h = int(W * s), int(H * s)
    zone = leggi(os.path.join(d, "zone.json"), {})
    piano = {g["id"]: g for g in leggi(os.path.join(d, "piano.json"), {}).get("grafiche", [])}
    divisi = [(piano[k]["in"], piano[k]["out"]) for k, v in zone.items() if isinstance(v, dict) and v.get("diviso") and k in piano]
    f = [f"[0:v]scale={w}:{h}:flags=lanczos,setsar=1[b0]"]
    cur = "b0"
    for i, (t0, t1) in enumerate(divisi):
        dy = int(700 * s)
        f.append(f"[{cur}]split[s{i}a][s{i}b]")
        f.append(f"[s{i}b]crop={w}:{h - dy}:0:0,pad={w}:{h}:0:{dy}:color={a.fondo}[s{i}c]")
        f.append(f"[s{i}a][s{i}c]overlay=0:0:enable='between(t,{t0 - 0.05:.2f},{t1 + 0.35:.2f})'[d{i}]")
        cur = f"d{i}"
    ingressi = []
    if ha_graf:
        ingressi += ["-framerate", str(FPS), "-i", os.path.join(graf, "%06d.png")]
        f.append(f"[{cur}][1:v]overlay=0:0:format=auto[g]")
        cur = "g"
    if os.path.exists(did):
        k = 2 if ha_graf else 1
        ingressi += ["-i", did]
        f.append(f"[{k}:v]scale={w}:{h}:flags=lanczos,format=yuva444p[dd]")
        f.append(f"[{cur}][dd]overlay=0:0:format=auto:eof_action=pass[t]")
        cur = "t"
    f.append(f"[{cur}]format=yuv420p[v]")
    out = os.path.join(d, "bozza.mp4" if a.bozza else "finale.mp4")
    q = ["-preset", "veryfast", "-crf", "27", "-b:a", "128k"] if a.bozza else ["-preset", "slow", "-crf", "17", "-profile:v", "high", "-b:a", "192k"]
    esegui(["ffmpeg", "-v", "error", "-y", "-i", base, *ingressi,
            "-filter_complex", ";".join(f), "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", *q[:-2], "-c:a", "aac", *q[-2:],
            "-r", str(FPS), "-t", f"{durata(base):.3f}", "-movflags", "+faststart", out])
    dv, dg = durata(out), durata(base)
    print(f"✓ {os.path.basename(out)}: {dv:.2f} s (montato {dg:.2f} s){'' if abs(dv - dg) < 0.2 else '  ! durata diversa: controlla'}")


if __name__ == "__main__":
    main()
