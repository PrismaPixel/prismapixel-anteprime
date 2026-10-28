"""Rende la scena (grafiche + sottotitoli) fotogramma per fotogramma, con lo sfondo trasparente.

  python3 rendi_grafiche.py --lavoro DIR [--bozza] [--secondi N] [--scena FILE]

Apre DIR/scena/scena.html in Chromium (Playwright), ferma il tempo e porta ogni elemento all'istante esatto di ogni
fotogramma (window.seek), poi salva un PNG trasparente. I fotogrammi senza niente sullo schermo non si rendono: puntano a
un unico PNG vuoto. --bozza rende a metà risoluzione (540 × 960), più veloce, per l'anteprima.
Scrive DIR/grafiche[_bozza]/NNNNNN.png e DIR/riquadri.json (dove sono i testi, 4 volte al secondo, per controlla.py).
La durata è quella di DIR/montato.mp4 (o --secondi).
"""
import argparse, os, shutil, sys, time
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comune import W, H, FPS, durata, lavoro, scrivi


def apri(p, scena, scala):
    b = p.chromium.launch(args=["--force-color-profile=srgb", "--disable-lcd-text"])
    pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=scala)
    pg.goto("file://" + os.path.abspath(scena))
    pg.wait_for_function("window.palcoPronto !== undefined")
    pg.evaluate("window.palcoPronto")
    return b, pg


def parte(job):
    from playwright.sync_api import sync_playwright
    scena, scala, cartella, fotogrammi = job
    with sync_playwright() as p:
        b, pg = apri(p, scena, scala)
        for f in fotogrammi:
            pg.evaluate("t => window.seek(t)", f / FPS)
            pg.screenshot(path=os.path.join(cartella, f"{f:06d}.png"), omit_background=True,
                          clip={"x": 0, "y": 0, "width": W, "height": H})
        b.close()
    return len(fotogrammi)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lavoro")
    ap.add_argument("--bozza", action="store_true")
    ap.add_argument("--secondi", type=float)
    ap.add_argument("--scena")
    ap.add_argument("--processi", type=int, default=max(1, min(4, (os.cpu_count() or 2) // 2)))
    a = ap.parse_args()
    d = lavoro(a.lavoro)
    scena = a.scena or os.path.join(d, "scena", "scena.html")
    if not os.path.exists(scena):
        raise SystemExit(f"✗ manca {scena}")
    sec = a.secondi or durata(os.path.join(d, "montato.mp4"))
    scala = 0.5 if a.bozza else 1
    cartella = os.path.join(d, "grafiche_bozza" if a.bozza else "grafiche")
    shutil.rmtree(cartella, ignore_errors=True); os.makedirs(cartella)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b, pg = apri(p, scena, scala)
        tempi = pg.evaluate("window.tempi()")
        riquadri = [{"t": round(i / 4, 2), "testi": pg.evaluate("t => window.riquadri(t)", i / 4)} for i in range(int(sec * 4) + 1)]
        # PNG vuoto per i fotogrammi senza grafiche
        pg.evaluate("window.seek(-10)")
        vuoto = os.path.join(cartella, "vuoto.png")
        pg.screenshot(path=vuoto, omit_background=True, clip={"x": 0, "y": 0, "width": W, "height": H})
        b.close()
    scrivi(os.path.join(d, "riquadri.json"), {"tempi": tempi, "campioni": riquadri})
    n = int(round(sec * FPS))
    attivi = [f for f in range(n) if any(x["in"] - 0.05 <= f / FPS <= x["out"] + 0.35 for x in tempi)]
    for f in set(range(n)) - set(attivi):
        os.link(vuoto, os.path.join(cartella, f"{f:06d}.png"))
    t0 = time.time()
    k = a.processi
    pezzi = [attivi[i::k] for i in range(k)]
    with ProcessPoolExecutor(k) as ex:
        fatti = sum(ex.map(parte, [(scena, scala, cartella, pz) for pz in pezzi if pz]))
    print(f"✓ {fatti} fotogrammi con grafiche su {n} ({time.time() - t0:.0f} s) in {cartella}")


if __name__ == "__main__":
    main()
