"""Funzioni comuni degli script di montaggio PrismaPixel.

Tutti i file di lavoro stanno in una cartella (default /tmp/lavoro/<slug>/montaggio, opzione --lavoro).
Le misure del formato verticale sono qui e solo qui: gli altri script le importano.
"""
import json, os, shutil, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.normpath(os.path.join(QUI, "..", "motion"))
MODELLI = os.environ.get("MODELLI_MONTAGGIO", "/tmp/modelli-montaggio")

# Formato verticale 9:16 (stesse zone dell'agente video AI)
W, H, FPS = 1080, 1920, 30
UTILE = {"x": 90, "y": 250, "w": 850, "h": 1220}      # area utile: x 90-940, y 250-1470
ZONE_APP = {"alto": 250, "basso": 450, "destra": 140, "sinistra": 90}  # coperte da nome profilo, didascalia, pulsanti
MARGINE_PERSONA = 40                                   # aria intorno al corpo, in pixel del palco


def lavoro(cartella=None):
    d = cartella or os.environ.get("LAVORO_MONTAGGIO") or "/tmp/lavoro/montaggio"
    os.makedirs(d, exist_ok=True)
    return d


def esegui(cmd, **kw):
    """Esegue un comando e fa vedere l'errore in chiaro se fallisce."""
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.stderr.write(f"\n✗ Comando fallito: {' '.join(map(str, cmd))[:300]}\n{r.stderr[-3000:]}\n")
        raise SystemExit(r.returncode)
    return r.stdout


def durata(file):
    out = esegui(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", file])
    return float(json.loads(out)["format"]["duration"])


def info_video(file):
    out = esegui(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                  "stream=width,height,r_frame_rate,codec_name:stream_side_data=rotation:stream_tags=rotate",
                  "-of", "json", file])
    s = (json.loads(out).get("streams") or [{}])[0]
    return s


def leggi(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def scrivi(path, dati):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=1)


def serve(prog):
    if not shutil.which(prog):
        raise SystemExit(f"✗ Manca {prog}: lancia prima script/prepara.py")
