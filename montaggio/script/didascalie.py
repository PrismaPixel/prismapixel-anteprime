"""Didascalie (sottotitoli) dei video verticali con la skill Omnedia Captions (Remotion, MIT): tutto il parlato,
nello stile scelto, reso come video trasparente (ProRes 4444 con alfa) che componi.py mette sopra il montato.

  python3 didascalie.py --lavoro DIR --bozza-piano   → scrive DIR/didascalie/piano_<stile>.json da rivedere (solo
                                                       per gli stili che vogliono un piano: yellow-authority,
                                                       montserrat-difference); poi copialo in piano.json
  python3 didascalie.py --lavoro DIR                 → DIR/didascalie.mov + DIR/didascalie.json + riquadri

Legge DIR/parole_montate.json (tempi delle parole sul montato), DIR/persona.json (volti) e piano.json:
  "didascalie": {"stile": "active-word-highlight" | "yellow-authority" | "editorial-kinetic" |
                          "montserrat-difference" | "nessuno",
                 "colori": {...},          (ruoli colore dello stile; vedi omnedia-captions/styles/<stile>/STYLE.md)
                 "opzioni": {...},         (styleOptions dello stile: editorialPlan, phrases, ...; la posizione la
                                            calcola questo script, se non la dai tu)
                 "correzioni": [{"da": "polignano", "a": "Polignano"}]}   (solo errori di trascrizione)
Senza "stile" decide lo stile del video: naturale → active-word-highlight tutto bianco (nessuna parola colorata),
leggero → active-word-highlight con la parola detta in giallo, grafico → yellow-authority (piano editoriale
dell'agente, testo completo: nessuna parola omessa).

Cosa fa, seguendo la skill (didascalie/omnedia-captions/SKILL.md e references/):
 1. normalized.json dalle parole (tempi rivisti: sono quelli della trascrizione col montaggio applicato);
 2. run.json con stile, colori, opzioni, posizione lontano dai volti e dentro l'area utile x 90-940, y 250-1470;
 3. prepare → progetto Remotion nuovo con create-video (istruzioni ufficiali di Remotion) → attach → render;
 4. DIR/didascalie.mov (1080 × 1920, alfa) e DIR/didascalie/<progetto>/ (progetto modificabile, project.json,
    EDITOR.md);
 5. riquadri del testo a 4 fotogrammi al secondo (dal canale alfa) → DIR/didascalie_riquadri.json per controlla.py.
Serve Node 22+, ffmpeg, le istruzioni Remotion in $MODELLI_MONTAGGIO/remotion-skills (prepara.py) e un Chromium
(REMOTION_BROWSER_EXECUTABLE, o quello di Playwright in /opt/pw-browsers).
"""
import argparse, datetime, glob, json, os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comune import W, H, FPS, UTILE, MODELLI, lavoro, leggi, scrivi

QUI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.normpath(os.path.join(QUI, "..", "didascalie", "omnedia-captions"))
STILI = ("active-word-highlight", "yellow-authority", "editorial-kinetic", "montserrat-difference")
X0, Y0, X1, Y1 = UTILE["x"], UTILE["y"], UTILE["x"] + UTILE["w"], UTILE["y"] + UTILE["h"]
norm = lambda w: re.sub(r"[^\w%€$]", "", w.lower())
FORTE = re.compile(r"[.!?;][”’\"']?$")


def cmd(args, cwd=None, env=None, timeout=1800):
    r = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise SystemExit(f"✗ {' '.join(args[:3])}…\n{r.stderr[-3000:]}\n{r.stdout[-2000:]}")
    return r.stdout


def browser():
    b = os.environ.get("REMOTION_BROWSER_EXECUTABLE")
    if b and os.path.exists(b):
        return b
    trovati = sorted(glob.glob("/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell")) + \
        sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell")))
    return trovati[-1] if trovati else None   # None: Remotion scarica il suo (serve rete verso remotion.media)


def parole_corrette(d, cfg):
    parole = [dict(x) for x in leggi(os.path.join(d, "parole_montate.json"), []) if str(x.get("w", "")).strip()]
    if not parole:
        raise SystemExit("✗ parole_montate.json vuoto: niente parlato. Per un video senza voce: \"stile\": \"nessuno\"")
    corr = {norm(c["da"]): c["a"] for c in cfg.get("correzioni", []) if c.get("da")}
    for x in parole:
        k = norm(x["w"])
        if k in corr:
            coda = re.search(r"[.,;:!?…]+$", x["w"])
            x["w"] = corr[k] + (coda.group(0) if coda else "")
        x["e"] = max(x.get("e", x["s"] + 0.2), x["s"] + 0.04)
    return parole


def frasi(parole, max_parole=None, pausa=0.7):
    """Frasi per la skill: si chiudono su . ! ? e sulle pause lunghe; max_parole per gli stili a frasi brevi."""
    out, cur = [], []
    for x in parole:
        if cur and (x["s"] - cur[-1]["e"] > pausa or (max_parole and len(cur) >= max_parole)
                    or (max_parole and x["s"] - cur[-1]["e"] >= 0.35)):
            out.append(cur); cur = []
        cur.append(x)
        if FORTE.search(x["w"]) or (max_parole and re.search(r"[,:]$", x["w"]) and len(cur) >= 2):
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def normalizza(gruppi):
    return {"sentences": [{"words": [{"text": (" " if i else "") + x["w"], "startMs": round(x["s"] * 1000),
                                      "endMs": round(x["e"] * 1000), "timestampMs": None, "confidence": None}
                                     for i, x in enumerate(g)]} for g in gruppi]}


def volti_in(d):
    out = []
    for c in leggi(os.path.join(d, "persona.json"), []):
        out += [(v["y"], v["y"] + v["h"]) for v in c.get("volti", [])]
    return out


def banda_libera(volti, y_top, y_bot, quota=0.03):
    """True se la banda verticale [y_top, y_bot] tocca un volto in meno del 3% dei campioni."""
    if not volti:
        return True
    toccati = sum(1 for a, b in volti if not (b < y_top - 20 or a > y_bot + 20))
    return toccati / len(volti) <= quota


def posizione(stile, d, opzioni):
    """Sceglie la posizione dentro l'area utile e lontano dai volti. Ritorna (opzioni aggiornate, nota)."""
    volti = volti_in(d)
    o = dict(opzioni)
    # lati: l'area utile è x 90-940 (a destra ci sono i pulsanti dell'app), quindi testo largo al massimo 800 px
    # centrato su x 510; ogni stile ha la sua chiave (le due di AWH ed EK sono aggiunte, vedi MODIFICHE.md)
    if stile == "active-word-highlight":
        o.setdefault("leftRatio", round(110 / W, 4)); o.setdefault("widthRatio", round(800 / W, 4))
    elif stile == "editorial-kinetic":
        o.setdefault("widthRatio", round(840 / W, 4)); o.setdefault("centerXRatio", round(510 / W, 4))
    elif stile == "yellow-authority":
        o.setdefault("scale", 0.9)
    elif stile == "montserrat-difference":
        o.setdefault("maxWidthRatio", round(800 / W, 4))
    if stile == "active-word-highlight" and "bottomRatio" not in o:
        # due righe da 64 px (≈ 160 px); il bordo basso del blocco a 1459 = sopra la didascalia dell'app
        for fondo in (1459, 1300, 760):
            if banda_libera(volti, fondo - 170, fondo):
                o["bottomRatio"] = round(1 - fondo / H, 4)
                return o, f"blocco con il fondo a y {fondo}"
        o["bottomRatio"] = round(1 - 1459 / H, 4)
        return o, "nessuna banda senza volti: fondo a y 1459, guarda il foglio"
    if stile == "yellow-authority" and "anchor" not in o:
        k = H / 1280   # tela di progetto 720 × 1280
        for cy in (1330, 1120, 560):
            if banda_libera(volti, cy - 130, cy + 130):
                o["anchor"] = {"x": round(510 / k), "y": round(cy / k)}
                return o, f"riga centrata a y {cy}"
        o["anchor"] = {"x": round(510 / k), "y": round(1330 / k)}
        return o, "nessuna banda senza volti: y 1330, guarda il foglio"
    if stile == "editorial-kinetic" and "centerRatio" not in o:
        for cy in (1180, 640):
            if banda_libera(volti, cy - 230, cy + 230):
                o["centerRatio"] = round(cy / H, 4)
                return o, f"composizione centrata a y {cy}"
        o["centerRatio"] = round(1180 / H, 4)
        return o, "nessuna banda senza volti: y 1180, guarda il foglio"
    if stile == "montserrat-difference" and "position" not in o:
        for cy in (430, 1250):
            if banda_libera(volti, cy - 120, cy + 300):
                o["position"] = {"x": round(510 / W, 4), "y": round(cy / H, 4)}
                return o, f"composizione a y {cy}"
        o["position"] = {"x": round(510 / W, 4), "y": round(430 / H, 4)}
        return o, "nessuna banda senza volti: y 430, guarda il foglio"
    return o, "posizione data nel piano"


def bozza_yellow(gruppi_frasi):
    """Piano di partenza per yellow-authority: TUTTE le parole in gruppi brevi bianchi e fermi (plain-center,
    phrase-cut). L'agente lo legge e sceglie dove mettere il giallo, le liste, i titoli (STYLE.md): non è il piano
    finale, è la copertura completa da cui partire."""
    # stesso testo del normalized.json (spazio iniziale solo dentro la frase): la skill confronta source parola per parola
    words = [{"text": w["text"], "s": w["startMs"] / 1000, "e": w["endMs"] / 1000}
             for f in normalizza(gruppi_frasi)["sentences"] for w in f["words"]]
    gruppi, i = [], 0
    while i < len(words):
        fine = i + 1
        while fine < len(words) and fine - i < 3 and (words[fine]["s"] - words[i]["s"]) <= 0.6 \
                and (words[fine]["s"] - words[fine - 1]["e"]) < 0.35 and not FORTE.search(words[fine - 1]["text"].strip()):
            fine += 1
        gruppi.append({"from": i, "to": fine, "template": "plain-center",
                       "reason": "DA RIVEDERE: frase normale, bianca e ferma",
                       "spans": [{"from": i, "to": fine, "role": "ordinary", "recipe": "phrase-cut", "line": 0}]})
        i = fine
    return {"density": 1, "editorialPlan": {"source": [w["text"] for w in words], "groups": gruppi}}


def bozza_montserrat(gruppi_frasi):
    """Piano di partenza per montserrat-difference: una frase breve per composizione, due parole per riga (a 76 px una
    riga di 4 parole esce dai margini), le righe si aggiungono quando vengono dette."""
    phrases = {}
    for k, g in enumerate(gruppi_frasi):
        phrases[str(k)] = {"layout": "stacked", "behavior": "build",
                           "groups": [{"from": i, "to": min(i + 2, len(g)), "line": i // 2} for i in range(0, len(g), 2)]}
    return {"phrases": phrases}


def riquadri(mov, d):
    """Riquadro del testo nel tempo, dal canale alfa del MOV (4 fotogrammi al secondo, a un quarto)."""
    import numpy as np
    w, h = W // 4, H // 4
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mov, "-vf", f"fps=4,scale={w}:{h},format=rgba",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    n = len(raw) // (w * h * 4)
    out = []
    for i in range(n):
        a = np.frombuffer(raw, np.uint8, w * h * 4, i * w * h * 4).reshape(h, w, 4)[:, :, 3]
        ys, xs = np.nonzero(a > 40)
        if len(xs):
            out.append({"t": round(i / 4, 2), "x": int(xs.min()) * 4, "y": int(ys.min()) * 4,
                        "w": int(xs.max() - xs.min() + 1) * 4, "h": int(ys.max() - ys.min() + 1) * 4})
    scrivi(os.path.join(d, "didascalie_riquadri.json"), out)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lavoro")
    ap.add_argument("--bozza-piano", action="store_true")
    a = ap.parse_args()
    d = lavoro(a.lavoro)
    piano = leggi(os.path.join(d, "piano.json"), {})
    cfg = piano.get("didascalie") or {}
    stile_video = piano.get("stile", "naturale")
    stile = cfg.get("stile") or ("yellow-authority" if stile_video == "grafico" else "active-word-highlight")
    cart = os.path.join(d, "didascalie")
    os.makedirs(cart, exist_ok=True)
    if stile == "nessuno":
        for f in ("didascalie.mov", "didascalie_riquadri.json"):
            if os.path.exists(os.path.join(d, f)):
                os.remove(os.path.join(d, f))
        scrivi(os.path.join(d, "didascalie.json"), {"stile": "nessuno"})
        print("✓ nessuna didascalia (scelto nel piano)"); return
    if stile not in STILI:
        raise SystemExit(f"✗ stile sconosciuto: {stile} ({', '.join(STILI)}, nessuno)")
    parole = parole_corrette(d, cfg)
    colori = dict(cfg.get("colori", {}))
    if stile == "active-word-highlight" and not colori and stile_video == "naturale":
        colori = {"base": "#FFFFFF", "active": "#FFFFFF", "shadow": "#000000"}   # naturale: nessuna parola colorata
    gruppi = frasi(parole, {"editorial-kinetic": 5, "montserrat-difference": 4}.get(stile))

    if a.bozza_piano:
        if stile == "yellow-authority":
            bozza = bozza_yellow(gruppi)
        elif stile == "montserrat-difference":
            bozza = bozza_montserrat(gruppi)
        else:
            raise SystemExit(f"✓ {stile} non ha bisogno di un piano: lancia didascalie.py senza --bozza-piano")
        f = os.path.join(cart, f"piano_{stile}.json")
        scrivi(f, bozza)
        print(f"✓ piano di partenza in {f}: rileggilo con STYLE.md, scegli le enfasi e mettilo in "
              f"piano.json → didascalie.opzioni"); return

    opzioni, nota = posizione(stile, d, cfg.get("opzioni", {}))
    if stile == "yellow-authority" and not opzioni.get("editorialPlan"):
        raise SystemExit("✗ yellow-authority vuole il piano editoriale dell'agente: lancia con --bozza-piano, rivedilo "
                         "secondo styles/yellow-authority/STYLE.md e mettilo in piano.json → didascalie.opzioni")
    if stile == "montserrat-difference" and not opzioni.get("phrases"):
        raise SystemExit("✗ montserrat-difference vuole le frasi e i gruppi: lancia con --bozza-piano e rivedili")

    norm_path = os.path.join(cart, "normalized.json")
    scrivi(norm_path, normalizza(gruppi))
    istr = os.path.join(MODELLI, "remotion-skills", "skills", "remotion-best-practices", "SKILL.md")
    if not os.path.exists(istr):
        raise SystemExit(f"✗ mancano le istruzioni Remotion in {istr}: lancia prepara.py")
    ora = datetime.datetime.now(datetime.timezone.utc).isoformat()
    run = {"plugin": {"availableInApp": True, "instructionPath": istr, "checkedAt": ora,
                      "nota": "istruzioni ufficiali Remotion (github.com/remotion-dev/skills), lette dall'agente"},
           "projectFolder": os.path.join(cart, "progetti"), "projectName": "didascalie",
           "style": stile, "colors": colori, "colorsAccepted": True, "styleOptions": opzioni,
           "normalizedPath": norm_path, "width": W, "height": H, "fps": FPS, "export": {"scale": 1},
           "timing": {"status": "word-timing-reviewed",
                      "provenance": "parole_montate.json: trascrizione Parakeet con i tempi per parola, montaggio applicato"},
           "sourceOffsetMs": 0, "timelinePlacementMs": 0}
    run_path = os.path.join(cart, "run.json")
    scrivi(run_path, run)
    cli = os.path.join(SKILL, "scripts", "captions.mjs")
    cmd(["node", cli, "doctor", run_path])
    cmd(["node", cli, "prepare", run_path])
    run = leggi(run_path)
    progetto = run["projectPath"]
    genitore, nome = os.path.split(progetto)
    os.makedirs(genitore, exist_ok=True)
    print(f"• {stile}: {nota}; progetto {progetto}")
    cmd(["npx", "-y", "create-video@latest", "--yes", "--blank", "--no-tailwind", nome], cwd=genitore)
    cmd(["npm", "i", "--no-audit", "--no-fund"], cwd=progetto)
    cmd(["node", cli, "attach", run_path])
    env = dict(os.environ)
    b = browser()
    if b:
        env["REMOTION_BROWSER_EXECUTABLE"] = b
    cmd(["npm", "run", "captions:render"], cwd=progetto, env=env)
    mov = os.path.join(d, "didascalie.mov")
    shutil.copyfile(os.path.join(progetto, "out", "captions.mov"), mov)
    # copertura: le parole mostrate sono quelle del transcript di visualizzazione (qui sempre tutte)
    dette = len(parole)
    if stile == "yellow-authority":
        src = opzioni["editorialPlan"]["source"]
        mostrate = len(src) if [s.strip() for s in src] == [x["w"] for x in parole] else 0
    else:
        mostrate = sum(len(g) for g in gruppi)
    rq = riquadri(mov, d)
    fuori = [r for r in rq if r["x"] < X0 - 4 or r["y"] < Y0 - 4 or r["x"] + r["w"] > X1 + 4 or r["y"] + r["h"] > Y1 + 4]
    scrivi(os.path.join(d, "didascalie.json"), {"stile": stile, "colori": colori, "posizione": nota,
                                                 "parole_dette": dette, "parole_mostrate": mostrate,
                                                 "progetto": progetto, "fuori_area": len(fuori)})
    print(f"✓ didascalie {stile}: {mostrate}/{dette} parole · {os.path.relpath(mov, d)}"
          + (f" · ! {len(fuori)} campioni fuori dall'area utile" if fuori else ""))


if __name__ == "__main__":
    main()
