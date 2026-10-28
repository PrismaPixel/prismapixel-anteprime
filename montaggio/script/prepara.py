"""Prepara il lavoro di montaggio: strumenti, modelli, font e girato normalizzato.

  python3 prepara.py --lavoro DIR [--girato a.mov b.mp4 ...] [--font Inter Fraunces]

1. Installa i pacchetti Python che mancano (sherpa-onnx, opencv, numpy).
2. Scarica i modelli UNA volta in $MODELLI_MONTAGGIO (default /tmp/modelli-montaggio), solo da fonti ufficiali su GitHub:
   - trascrizione: NVIDIA Parakeet TDT 0.6B v3 (25 lingue europee, italiano compreso, con i tempi di ogni parola),
     versione int8 di sherpa-onnx (k2-fsa), circa 490 MB; più Silero VAD per dividere l'audio in frasi;
   - persone: YOLOX-S (corpo intero, anche lontano) e YuNet (volto) dall'OpenCV Model Zoo.
3. Copia tema.css e motore.js in DIR/scena e installa i font da npm (@fontsource/<nome>) scrivendo fonts.css.
4. Normalizza il girato in DIR/girato/NN.mp4: rotazione applicata, 30 fotogrammi al secondo costanti, H.264, audio
   48 kHz; più DIR/girato/NN.wav (16 kHz mono) per la trascrizione. Scrive DIR/girato/elenco.json.
Il file originale non si tocca mai.
"""
import argparse, json, os, re, shutil, subprocess, sys, tarfile, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comune import MODELLI, MOTION, FPS, esegui, durata, info_video, lavoro, scrivi

REL = "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/"
ZOO = "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/"
MODELLI_URL = {
    "parakeet": (REL + "sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8.tar.bz2", "sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"),
    "vad": (REL + "silero_vad.onnx", "silero_vad.onnx"),
    "yolox": (ZOO + "object_detection_yolox/object_detection_yolox_2022nov.onnx", "yolox.onnx"),
    "yunet": (ZOO + "face_detection_yunet/face_detection_yunet_2023mar.onnx", "yunet.onnx"),
}


def pacchetti():
    manca = []
    for mod, pip in [("sherpa_onnx", "sherpa-onnx"), ("cv2", "opencv-python-headless"), ("numpy", "numpy")]:
        try:
            __import__(mod)
        except ImportError:
            manca.append(pip)
    if manca:
        print("• installo", " ".join(manca))
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", *manca], check=True)


def scarica(nome):
    url, dest = MODELLI_URL[nome]
    os.makedirs(MODELLI, exist_ok=True)
    finale = os.path.join(MODELLI, dest)
    if os.path.exists(finale):
        return finale
    print(f"• scarico il modello {nome} (una volta sola)…", flush=True)
    tmp = os.path.join(MODELLI, os.path.basename(url) + ".part")
    urllib.request.urlretrieve(url, tmp)
    if url.endswith(".tar.bz2"):
        with tarfile.open(tmp, "r:bz2") as t:
            for m in t.getmembers():  # niente percorsi fuori dalla cartella dei modelli
                if m.name.startswith("/") or ".." in m.name:
                    raise SystemExit(f"✗ archivio sospetto: {m.name}")
            t.extractall(MODELLI)
        os.remove(tmp)
    else:
        os.replace(tmp, finale)
    if not os.path.exists(finale) or (os.path.isfile(finale) and os.path.getsize(finale) == 0):
        raise SystemExit(f"✗ modello {nome} non scaricato bene: riprova")
    return finale


def font(scena, nomi):
    if not nomi:
        return
    cartella = os.path.join(scena, "fonts")
    os.makedirs(cartella, exist_ok=True)
    pacchi = ["@fontsource/" + n.lower().replace(" ", "-") for n in nomi]
    print("• installo i font", ", ".join(nomi))
    subprocess.run(["npm", "i", "--silent", "--no-audit", "--no-fund", "--prefix", cartella, *pacchi], check=True)
    righe = []
    for n, p in zip(nomi, pacchi):
        files = os.path.join(cartella, "node_modules", p, "files")
        if not os.path.isdir(files):
            print(f"  ! font {n} non trovato su npm: resta il font di riserva")
            continue
        for f in sorted(os.listdir(files)):
            m = re.match(r".*-latin-(\d+)-(normal|italic)\.woff2$", f)
            if m:
                rel = os.path.relpath(os.path.join(files, f), scena)
                righe.append(f"@font-face{{font-family:'{n}';src:url('{rel}') format('woff2');font-weight:{m.group(1)};font-style:{m.group(2)};font-display:block}}")
    open(os.path.join(scena, "fonts.css"), "w").write("\n".join(righe) + "\n")


def normalizza(files, d):
    out = os.path.join(d, "girato")
    os.makedirs(out, exist_ok=True)
    elenco = []
    for i, f in enumerate(files, 1):
        base = os.path.join(out, f"{i:02d}")
        info = info_video(f)
        has_audio = bool(json.loads(esegui(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "json", f])).get("streams"))
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", f, "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16"]
        cmd += (["-c:a", "aac", "-b:a", "192k", "-ar", "48000"] if has_audio else ["-an"])
        esegui(cmd + [base + ".mp4"])
        if has_audio:
            esegui(["ffmpeg", "-v", "error", "-y", "-i", base + ".mp4", "-vn", "-ac", "1", "-ar", "16000", base + ".wav"])
        w, h = info_video(base + ".mp4").get("width"), info_video(base + ".mp4").get("height")
        elenco.append({"n": i, "originale": os.path.basename(f), "file": base + ".mp4", "audio": base + ".wav" if has_audio else None,
                       "larghezza": w, "altezza": h, "verticale": h > w, "durata": round(durata(base + ".mp4"), 2),
                       "codec_originale": info.get("codec_name")})
        print(f"• girato {i}: {os.path.basename(f)} → {w}×{h}, {elenco[-1]['durata']} s{'' if has_audio else ', senza audio'}")
    scrivi(os.path.join(out, "elenco.json"), elenco)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lavoro")
    ap.add_argument("--girato", nargs="*", default=[])
    ap.add_argument("--font", nargs="*", default=[], help="nomi Google Fonts, es. Inter Fraunces")
    ap.add_argument("--senza-modelli", action="store_true", help="salta i modelli (solo grafiche)")
    a = ap.parse_args()
    for p in ("ffmpeg", "ffprobe", "node", "npm"):
        if not shutil.which(p):
            raise SystemExit(f"✗ manca {p} nell'ambiente")
    d = lavoro(a.lavoro)
    pacchetti()
    if not a.senza_modelli:
        for k in MODELLI_URL:
            scarica(k)
    scena = os.path.join(d, "scena")
    os.makedirs(scena, exist_ok=True)
    for f in ("tema.css", "motore.js"):
        shutil.copy(os.path.join(MOTION, f), os.path.join(scena, f))
    font(scena, a.font)
    if a.girato:
        normalizza(a.girato, d)
    print("✓ pronto:", d)


if __name__ == "__main__":
    main()
