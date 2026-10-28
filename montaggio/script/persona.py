"""Trova le persone nel video: corpo intero (anche lontano o di spalle) e volti.

  python3 persona.py --lavoro DIR                 analizza DIR/montato.mp4 → DIR/persona.json (coordinate del palco)
  python3 persona.py --lavoro DIR --girato        analizza ogni file di DIR/girato → DIR/inquadratura.json proposta

Modelli (scaricati da prepara.py): YOLOX-S per il corpo (classe "persona" di COCO) e YuNet per i volti, con OpenCV.
Campiona 4 fotogrammi al secondo. Per ogni campione: riquadri delle persone {x, y, w, h, conf} e dei volti.
Con --girato propone per ogni file il centro dell'inquadratura 9:16 (sulla persona principale, mediana nel tempo) e lo
zoom: 1.0 se la persona è già ben visibile; fino a 1.4 se è piccola e il file è almeno 4K. Se nessuno è inquadrato
(riprese di luogo o prodotto) restano centro e zoom 1.0.
"""
import argparse, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comune import MODELLI, W, H, lavoro, leggi, scrivi

_det = {}


def yolox():
    import cv2
    if "y" not in _det:
        _det["y"] = cv2.dnn.readNet(os.path.join(MODELLI, "yolox.onnx"))
    return _det["y"]


def persone(img, soglia=0.35):
    """Riquadri delle persone in un fotogramma BGR, in pixel del fotogramma."""
    import cv2
    h0, w0 = img.shape[:2]
    r = min(640 / h0, 640 / w0)
    pad = np.full((640, 640, 3), 114, dtype=np.uint8)
    pad[:int(h0 * r), :int(w0 * r)] = cv2.resize(img, (int(w0 * r), int(h0 * r)))
    blob = cv2.dnn.blobFromImage(pad.astype(np.float32), 1.0, (640, 640), swapRB=False)  # YOLOX: BGR 0-255
    net = yolox(); net.setInput(blob)
    out = net.forward()[0]
    grids, strides = [], []
    for s in (8, 16, 32):
        n = 640 // s
        yv, xv = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
        grids.append(np.stack((xv, yv), 2).reshape(-1, 2)); strides.append(np.full((n * n, 1), s))
    g, st = np.concatenate(grids), np.concatenate(strides)
    xy = (out[:, :2] + g) * st
    wh = np.exp(out[:, 2:4]) * st
    score = out[:, 4] * out[:, 5]  # oggetto × classe 0 (persona)
    keep = score > soglia
    if not keep.any():
        return []
    xy, wh, score = xy[keep], wh[keep], score[keep]
    boxes = np.concatenate([xy - wh / 2, wh], 1) / r
    idx = cv2.dnn.NMSBoxes(boxes.tolist(), score.tolist(), soglia, 0.5)
    res = []
    for i in np.array(idx).flatten():
        x, y, w, h = boxes[i]
        x, y = max(0, x), max(0, y)
        res.append({"x": int(x), "y": int(y), "w": int(min(w, w0 - x)), "h": int(min(h, h0 - y)), "conf": round(float(score[i]), 2)})
    return res


def volti(img):
    import cv2
    h0, w0 = img.shape[:2]
    if "f" not in _det:
        _det["f"] = cv2.FaceDetectorYN.create(os.path.join(MODELLI, "yunet.onnx"), "", (320, 320), 0.7, 0.3, 50)
    s = 640 / max(h0, w0)
    small = cv2.resize(img, (int(w0 * s), int(h0 * s)))
    _det["f"].setInputSize((small.shape[1], small.shape[0]))
    _, f = _det["f"].detect(small)
    return [{"x": int(v[0] / s), "y": int(v[1] / s), "w": int(v[2] / s), "h": int(v[3] / s)} for v in (f if f is not None else [])]


def campiona(file, fps=4):
    import cv2
    cap = cv2.VideoCapture(file)
    src = cap.get(cv2.CAP_PROP_FPS) or 30
    passo = max(1, round(src / fps)); i = 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        if i % passo == 0:
            yield i / src, fr
        i += 1
    cap.release()


def analizza(file, fps=4):
    out = []
    for t, fr in campiona(file, fps):
        out.append({"t": round(t, 2), "persone": persone(fr), "volti": volti(fr), "w": fr.shape[1], "h": fr.shape[0]})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lavoro")
    ap.add_argument("--girato", action="store_true")
    ap.add_argument("--fps", type=float, default=4)
    a = ap.parse_args()
    d = lavoro(a.lavoro)
    if a.girato:
        prop = {}
        for g in leggi(os.path.join(d, "girato", "elenco.json"), []):
            ana = analizza(g["file"], 2)
            princ = [max(c["persone"], key=lambda p: p["w"] * p["h"]) for c in ana if c["persone"]]
            nome = os.path.splitext(os.path.basename(g["file"]))[0]
            if not princ:
                prop[nome] = {"cx": 0.5, "cy": 0.5, "zoom": 1.0, "nota": "nessuna persona: riprese di luogo o prodotto"}
                continue
            cx = float(np.median([(p["x"] + p["w"] / 2) / g["larghezza"] for p in princ]))
            cy = float(np.median([(p["y"] + p["h"] / 2) / g["altezza"] for p in princ]))
            alt = float(np.median([p["h"] / g["altezza"] for p in princ]))
            grande = min(g["larghezza"], g["altezza"]) >= 2160
            zoom = 1.0 if alt > 0.45 or not grande else round(min(1.4, 0.55 / max(alt, 0.05)), 2)
            prop[nome] = {"cx": round(cx, 3), "cy": round(cy, 3), "zoom": zoom, "altezza_persona": round(alt, 2),
                          "nota": "persona piccola" + ("" if grande else ", file non 4K: niente zoom") if alt <= 0.45 else "persona ben visibile",
                          "copertura": round(len(princ) / max(1, len(ana)), 2)}
        scrivi(os.path.join(d, "inquadratura.json"), prop)
        for k, v in prop.items():
            print(f"• {k}: centro {v['cx']},{v['cy']} zoom {v['zoom']} · {v['nota']}")
        return
    file = os.path.join(d, "montato.mp4")
    ana = analizza(file, a.fps)
    # riporta tutto alle coordinate del palco 1080 × 1920
    for c in ana:
        sx, sy = W / c["w"], H / c["h"]
        for k in ("persone", "volti"):
            c[k] = [{**p, "x": int(p["x"] * sx), "y": int(p["y"] * sy), "w": int(p["w"] * sx), "h": int(p["h"] * sy)} for p in c[k]]
        c.pop("w"); c.pop("h")
    scrivi(os.path.join(d, "persona.json"), ana)
    con = sum(1 for c in ana if c["persone"])
    print(f"✓ persona.json: {len(ana)} campioni, persone visibili nel {100 * con // max(1, len(ana))}%")


if __name__ == "__main__":
    main()
