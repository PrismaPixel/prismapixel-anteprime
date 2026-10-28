"""Applica i tagli e mette il video in verticale (1080 × 1920, 30 fps).

  python3 applica.py --lavoro DIR

Legge DIR/tagli.json (pezzi nell'ordine) e, se c'è, DIR/inquadratura.json (da persona.py o scritto a mano):
  {"01": {"cx": 0.5, "cy": 0.45, "zoom": 1.0}, ...}   centro dell'inquadratura (0-1) e quanto stringere per ogni file.
- Girato verticale: riempie il 9:16 senza bande; con zoom > 1 stringe sul centro indicato.
- Girato orizzontale: ritaglia una finestra 9:16 centrata sulla persona (cx). Se il file è più piccolo di 4K e lo zoom
  supera 1,3 la qualità cala: lo scrive negli avvisi.
- Audio: quello dei pezzi, con dissolvenze di 15 ms sui tagli (niente schiocchi); se tagli.json ha "voce", usa
  quella registrazione per tutto il video (riprese mute sotto).
Scrive DIR/montato.mp4, DIR/mappa.json (dove finisce ogni pezzo) e DIR/parole_montate.json (parole con i tempi del
video montato: sono i tempi da usare per sottotitoli e grafiche).
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comune import W, H, FPS, esegui, info_video, lavoro, leggi, scrivi


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lavoro")
    a = ap.parse_args()
    d = lavoro(a.lavoro)
    T = leggi(os.path.join(d, "tagli.json"))
    if not T or not T.get("pezzi"):
        raise SystemExit("✗ manca tagli.json con i pezzi")
    inq = leggi(os.path.join(d, "inquadratura.json"), {})
    parole = leggi(os.path.join(d, "parole.json"), [])
    voce = T.get("voce")
    files = []
    for p in T["pezzi"]:
        if p["file"] not in files:
            files.append(p["file"])
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for f in files:
        cmd += ["-i", f]
    if voce:
        cmd += ["-i", voce]
    filtri, avvisi, mappa, t = [], [], [], 0.0
    for k, p in enumerate(T["pezzi"]):
        i = files.index(p["file"])
        nome = os.path.splitext(os.path.basename(p["file"]))[0]
        info = info_video(p["file"])
        sw, sh = int(info["width"]), int(info["height"])
        q = inq.get(nome, {})
        zoom = max(1.0, float(q.get("zoom", 1.0)))
        cx, cy = float(q.get("cx", 0.5)), float(q.get("cy", 0.5))
        # finestra 9:16 più grande possibile nel girato, poi stretta di "zoom"
        ch = min(sh, sw * 16 / 9) / zoom
        cw = ch * 9 / 16
        x = min(max(cx * sw - cw / 2, 0), sw - cw)
        y = min(max(cy * sh - ch / 2, 0), sh - ch)
        if cw < W * 0.75:
            avvisi.append(f"pezzo {k + 1}: finestra {int(cw)}×{int(ch)} px, ingrandita a {W}×{H}: qualità bassa (serve girato in 4K o meno zoom)")
        dur = p["out"] - p["in"]
        filtri.append(f"[{i}:v]trim={p['in']}:{p['out']},setpts=PTS-STARTPTS,crop={int(cw)//2*2}:{int(ch)//2*2}:{int(x)}:{int(y)},"
                      f"scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS},format=yuv420p[v{k}]")
        if not voce:
            if p.get("audio", True) and any(x.get("audio") for x in leggi(os.path.join(d, "girato", "elenco.json"), []) if x["file"] == p["file"]):
                filtri.append(f"[{i}:a]atrim={p['in']}:{p['out']},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={max(0, dur - 0.015):.3f}:d=0.015,aresample=48000[a{k}]")
            else:
                filtri.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{dur:.3f}[a{k}]")
        mappa.append({"pezzo": k + 1, "file": p["file"], "in": p["in"], "out": p["out"], "inizio": round(t, 3), "fine": round(t + dur, 3)})
        t += dur
    n = len(T["pezzi"])
    if voce:
        filtri.append("".join(f"[v{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=0[v]")
        cmd += ["-filter_complex", ";".join(filtri), "-map", "[v]", "-map", f"{len(files)}:a", "-shortest"]
    else:
        filtri.append("".join(f"[v{k}][a{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=1[v][a]")
        cmd += ["-filter_complex", ";".join(filtri), "-map", "[v]", "-map", "[a]"]
    out = os.path.join(d, "montato.mp4")
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    esegui(cmd)
    # parole con i tempi del video montato
    nuove = []
    for m, p in zip(mappa, T["pezzi"]):
        for j in p.get("parole", []):
            w = dict(parole[j])
            w["s"] = round(m["inizio"] + max(0, w["s"] - p["in"]), 2)
            w["e"] = round(min(m["fine"], m["inizio"] + w["e"] - p["in"]), 2)
            nuove.append(w)
    scrivi(os.path.join(d, "mappa.json"), {"pezzi": mappa, "avvisi": avvisi})
    scrivi(os.path.join(d, "parole_montate.json"), nuove)
    print(f"✓ montato.mp4: {t:.1f} s, {n} pezzi")
    for x in avvisi:
        print("  !", x)


if __name__ == "__main__":
    main()
