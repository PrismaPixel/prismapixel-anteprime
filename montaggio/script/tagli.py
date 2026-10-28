"""Prepara la lista dei tagli dal parlato (non taglia ancora niente).

  python3 tagli.py --lavoro DIR [--pausa 0.6] [--resta 0.25]

Regole (scritte con parole nostre a partire dal metodo del kit del cliente, vedi FONTE.md):
- frase ripetuta: se una frase ricomincia poco dopo con le stesse prime parole (o quasi uguale), è un nuovo tentativo:
  si tiene l'ULTIMA versione completa e si tolgono quelle prima;
- parola detta due volte di fila ("il il"): si tiene l'ultima;
- pausa più lunga di --pausa secondi: si accorcia lasciando --resta secondi, così suona ancora come una persona;
- mai tagliare dentro una parola: ogni pezzo parte 0,08 s prima della prima parola e finisce 0,12 s dopo l'ultima.
Quando non è sicuro, NON taglia e lo scrive in "dubbi".
Scrive DIR/tagli.json (i pezzi da tenere, nell'ordine) e DIR/tagli.txt (da mostrare prima di tagliare).
Per i video senza parlato (solo riprese, o voce fuori campo registrata a parte) tagli.json si scrive a mano, stesso
formato: {"pezzi": [{"file": ".../girato/02.mp4", "in": 3.0, "out": 6.5}], "voce": ".../voce.wav" | null}.
"""
import argparse, difflib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comune import lavoro, leggi, scrivi

norm = lambda w: re.sub(r"[^\wàèéìòù']", "", w.lower())


def frasi(parole, pausa):
    out, cur = [], []
    for i, p in enumerate(parole):
        if cur:
            prev = parole[cur[-1]]
            if p["file"] != prev["file"] or p["s"] - prev["e"] > pausa * 1.5 or re.search(r"[.?!…]$", prev["w"]):
                out.append(cur); cur = []
        cur.append(i)
    if cur:
        out.append(cur)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lavoro")
    ap.add_argument("--pausa", type=float, default=0.6)
    ap.add_argument("--resta", type=float, default=0.25)
    ap.add_argument("--finestra", type=float, default=30, help="secondi entro cui una frase simile conta come ripetizione")
    a = ap.parse_args()
    d = lavoro(a.lavoro)
    parole = leggi(os.path.join(d, "parole.json"))
    elenco = {g["n"]: g for g in leggi(os.path.join(d, "girato", "elenco.json"), [])}
    if not parole:
        raise SystemExit("✗ manca parole.json: lancia prima trascrivi.py")
    F = frasi(parole, a.pausa)
    tieni = set(range(len(parole)))
    tolto, dubbi = [], []
    testo = lambda idx: " ".join(parole[i]["w"] for i in idx)
    parole_n = lambda idx: [norm(parole[i]["w"]) for i in idx if norm(parole[i]["w"])]
    # 1. frasi ripetute: tiene l'ultima
    for i, fa in enumerate(F):
        na = parole_n(fa)
        if not na:
            continue
        for fb in F[i + 1:i + 4]:
            if parole[fb[0]]["file"] != parole[fa[0]]["file"] or parole[fb[0]]["s"] - parole[fa[-1]]["e"] > a.finestra:
                break
            nb = parole_n(fb)
            stesso_inizio = len(na) >= 2 and nb[:min(3, len(na))] == na[:min(3, len(na))]
            simile = difflib.SequenceMatcher(None, na, nb[:len(na) + 2]).ratio()
            if stesso_inizio or simile >= 0.75:
                tieni -= set(fa)
                tolto.append({"motivo": "frase ripetuta: tengo l'ultima", "testo": testo(fa), "s": parole[fa[0]]["s"], "e": parole[fa[-1]]["e"]})
                break
            if 0.5 <= simile < 0.75:
                dubbi.append({"motivo": "forse la stessa frase detta due volte (tenute entrambe)", "testo": testo(fa) + "  ⟷  " + testo(fb), "s": parole[fa[0]]["s"]})
    # 2. parole doppie di fila
    for fa in F:
        for x, y in zip(fa, fa[1:]):
            if x in tieni and y in tieni and norm(parole[x]["w"]) and norm(parole[x]["w"]) == norm(parole[y]["w"]):
                tieni.discard(x)
                tolto.append({"motivo": "parola detta due volte", "testo": parole[x]["w"] + " " + parole[y]["w"], "s": parole[x]["s"], "e": parole[y]["e"]})
    # 3. pezzi continui e pause accorciate
    idx = sorted(tieni)
    pezzi, cur = [], None
    for i in idx:
        p = parole[i]
        if cur and p["file"] == cur["n"] and p["s"] - parole[cur["parole"][-1]]["e"] <= a.pausa and cur["parole"][-1] == i - 1:
            cur["parole"].append(i); continue
        if cur:
            pezzi.append(cur)
        cur = {"n": p["file"], "parole": [i]}
    if cur:
        pezzi.append(cur)
    usciti, accorciate = [], 0
    for k, pz in enumerate(pezzi):
        g = elenco.get(pz["n"], {})
        prima, ultima = parole[pz["parole"][0]], parole[pz["parole"][-1]]
        inizio = max(0.0, prima["s"] - 0.08)
        fine = min(g.get("durata", 1e9), ultima["e"] + 0.12)
        if usciti and usciti[-1]["file"] == g.get("file"):
            gap = inizio - usciti[-1]["out"]
            if gap > 0:
                accorciate += 1
                # resta un po' di respiro: metà alla fine del pezzo prima, metà all'inizio di questo
                usciti[-1]["out"] = round(min(usciti[-1]["out"] + a.resta / 2, inizio), 2)
                inizio = max(usciti[-1]["out"], inizio - a.resta / 2)
            else:
                usciti[-1]["out"] = round(fine, 2); usciti[-1]["parole"] += pz["parole"]; continue
        usciti.append({"file": g.get("file"), "in": round(inizio, 2), "out": round(fine, 2), "parole": pz["parole"]})
    durata_prima = sum(x.get("durata", 0) for x in elenco.values())
    durata_dopo = sum(x["out"] - x["in"] for x in usciti)
    scrivi(os.path.join(d, "tagli.json"), {"pezzi": usciti, "voce": None, "tolto": tolto, "dubbi": dubbi})
    righe = [f"Durata: {durata_prima:.1f} s → {durata_dopo:.1f} s (tolti {durata_prima - durata_dopo:.1f} s) · {len(usciti)} pezzi · pause accorciate: {accorciate}", ""]
    righe += ["TOLTO:"] + ([f"  {x['s']:7.2f}  {x['motivo']}: «{x['testo']}»" for x in tolto] or ["  niente"])
    righe += ["", "DUBBI (non tagliati, da decidere):"] + ([f"  {x['s']:7.2f}  {x['motivo']}: «{x['testo']}»" for x in dubbi] or ["  nessuno"])
    righe += ["", "PEZZI TENUTI:"] + [f"  {i + 1:2d}. file {os.path.basename(str(p['file']))} {p['in']:7.2f}-{p['out']:7.2f}  «{' '.join(parole[j]['w'] for j in p['parole'])[:90]}»" for i, p in enumerate(usciti)]
    open(os.path.join(d, "tagli.txt"), "w", encoding="utf-8").write("\n".join(righe) + "\n")
    print("\n".join(righe[:3]))
    print(f"✓ lista in {os.path.join(d, 'tagli.txt')}: controllala prima di applica.py")


if __name__ == "__main__":
    main()
