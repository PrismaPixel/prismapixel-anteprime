"""Trascrive il girato parola per parola, con i tempi.

  python3 trascrivi.py --lavoro DIR

Legge DIR/girato/elenco.json (da prepara.py). Per ogni file con audio:
- Silero VAD divide l'audio in tratti di voce (una pausa di almeno 0,3 s chiude un tratto);
- Parakeet TDT v3 trascrive ogni tratto (lingua riconosciuta da sola, punteggiatura compresa) con il tempo di ogni pezzo
  di parola; le parole iniziano dove inizia il loro primo pezzo e finiscono dove inizia la parola dopo, o alla fine
  del tratto.
Scrive DIR/parole.json  [{"w": "Ciao", "s": 0.32, "e": 0.61, "file": 1, "tratto": 0}, ...]
e DIR/testo.txt (una frase per riga, con l'inizio in secondi) da leggere e correggere.
I tempi hanno una precisione di circa 0,08 s: per i sottotitoli parola per parola basta.
"""
import argparse, os, sys, time, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comune import MODELLI, lavoro, leggi, scrivi

PAR = os.path.join(MODELLI, "sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8")


def carica_audio(path):
    with wave.open(path) as w:
        assert w.getframerate() == 16000 and w.getnchannels() == 1, "serve wav 16 kHz mono (prepara.py)"
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


def tratti(audio):
    import sherpa_onnx
    cfg = sherpa_onnx.VadModelConfig()
    cfg.silero_vad.model = os.path.join(MODELLI, "silero_vad.onnx")
    cfg.silero_vad.threshold = 0.45
    cfg.silero_vad.min_silence_duration = 0.3
    cfg.silero_vad.min_speech_duration = 0.15
    cfg.silero_vad.max_speech_duration = 25
    cfg.sample_rate = 16000
    vad = sherpa_onnx.VoiceActivityDetector(cfg, buffer_size_in_seconds=120)
    out, win = [], cfg.silero_vad.window_size
    for i in range(0, len(audio), win):
        vad.accept_waveform(audio[i:i + win])
        while not vad.empty():
            seg = vad.front; out.append((seg.start / 16000, np.array(seg.samples, dtype=np.float32))); vad.pop()
    vad.flush()
    while not vad.empty():
        seg = vad.front; out.append((seg.start / 16000, np.array(seg.samples, dtype=np.float32))); vad.pop()
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lavoro")
    ap.add_argument("--thread", type=int, default=max(2, (os.cpu_count() or 4) - 1))
    a = ap.parse_args()
    d = lavoro(a.lavoro)
    elenco = leggi(os.path.join(d, "girato", "elenco.json"))
    if not elenco:
        raise SystemExit("✗ manca girato/elenco.json: lancia prima prepara.py --girato …")
    import sherpa_onnx
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=os.path.join(PAR, "encoder.int8.onnx"), decoder=os.path.join(PAR, "decoder.int8.onnx"),
        joiner=os.path.join(PAR, "joiner.int8.onnx"), tokens=os.path.join(PAR, "tokens.txt"),
        model_type="nemo_transducer", num_threads=a.thread)
    parole, righe, t0 = [], [], time.time()
    for g in elenco:
        if not g.get("audio"):
            continue
        audio = carica_audio(g["audio"])
        for k, (inizio, campioni) in enumerate(tratti(audio)):
            s = rec.create_stream(); s.accept_waveform(16000, campioni); rec.decode_stream(s)
            r = s.result
            fine_tratto = inizio + len(campioni) / 16000
            correnti = []
            for tok, ts in zip(r.tokens, r.timestamps):
                nuovo = tok.startswith(" ") or tok.startswith("▁") or not correnti
                testo = tok.replace("▁", " ")
                if nuovo and testo.strip():
                    correnti.append({"w": testo.strip(), "s": round(inizio + ts, 2)})
                elif correnti:
                    correnti[-1]["w"] += testo.strip()
            for i, p in enumerate(correnti):
                p["e"] = round(min(correnti[i + 1]["s"] if i + 1 < len(correnti) else fine_tratto, p["s"] + 1.2), 2)
                p["file"], p["tratto"] = g["n"], k
            # la punteggiatura da sola si attacca alla parola prima
            pulite = []
            for p in correnti:
                if pulite and not any(c.isalnum() for c in p["w"]):
                    pulite[-1]["w"] += p["w"]; pulite[-1]["e"] = p["e"]
                else:
                    pulite.append(p)
            parole += pulite
            if pulite:
                righe.append(f"[{g['n']}] {pulite[0]['s']:7.2f}  {' '.join(p['w'] for p in pulite)}")
    scrivi(os.path.join(d, "parole.json"), parole)
    open(os.path.join(d, "testo.txt"), "w", encoding="utf-8").write("\n".join(righe) + "\n")
    print(f"✓ {len(parole)} parole in {len(righe)} tratti ({time.time() - t0:.0f} s). Leggi {os.path.join(d, 'testo.txt')}")


if __name__ == "__main__":
    main()
