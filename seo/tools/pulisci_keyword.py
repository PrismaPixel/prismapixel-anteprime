#!/usr/bin/env python3
"""Pulisce le parole chiave di OpenSEO (research_keywords, get_keyword_metrics) o di Manifold (seo_search_keywords).

Tiene solo le ricerche pertinenti al cliente, toglie i doppioni e le ordina per priorità.

  python3 -I pulisci_keyword.py risposta.json --servizi "barca,grotte,escursion,tour,gita" \
      --luoghi "polignano,monopoli" [--escludi "meteo,mare fuori"] [--senza-luogo] [--json]

- servizi: parole (o inizi di parola) del servizio; almeno una deve esserci.
- luoghi: le località del cliente; almeno una deve esserci, salvo --senza-luogo.
- escludi: parole che scartano la riga (marchi altrui, altre città, temi estranei).
Priorità: prima chi vuole comprare o prenotare (intento transazionale o commerciale), poi difficoltà bassa,
poi CPC alto (segno che la ricerca porta clienti), poi volume.
"""
import argparse, json, re, sys, unicodedata


def norm(s):
    s = unicodedata.normalize('NFKD', str(s or '').lower())
    return ''.join(c for c in s if not unicodedata.combining(c))


def righe(dati):
    """Trova le righe con una parola chiave in qualsiasi forma di risposta."""
    out = []
    if isinstance(dati, dict):
        for k in ('results', 'rows', 'keywords', 'items'):
            if isinstance(dati.get(k), list):
                for x in dati[k]:
                    if isinstance(x, dict) and isinstance(x.get('rows'), list):
                        out.extend(x['rows'])
                    else:
                        out.append(x)
        if not out and 'keyword' in dati:
            out.append(dati)
    elif isinstance(dati, list):
        for x in dati:
            out.extend(righe(x) if isinstance(x, (dict, list)) and 'keyword' not in x else [x])
    return [r for r in out if isinstance(r, dict) and r.get('keyword')]


def campo(r, *nomi):
    for n in nomi:
        if r.get(n) is not None:
            return r[n]
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('file')
    p.add_argument('--servizi', required=True)
    p.add_argument('--luoghi', default='')
    p.add_argument('--escludi', default='')
    p.add_argument('--senza-luogo', action='store_true', help='tiene anche le ricerche senza località')
    p.add_argument('--json', action='store_true')
    a = p.parse_args()

    servizi = [norm(x).strip() for x in a.servizi.split(',') if x.strip()]
    luoghi = [norm(x).strip() for x in a.luoghi.split(',') if x.strip()]
    escludi = [norm(x).strip() for x in a.escludi.split(',') if x.strip()]
    dati = json.load(open(a.file, encoding='utf-8'))

    tenute, viste, scartate = [], set(), 0
    for r in righe(dati):
        kw = norm(r['keyword']).strip()
        chiave = re.sub(r'\b(a|di|da|in|il|la|le|lo|gli|i|del|della|dei)\b', ' ', kw)
        chiave = ' '.join(sorted(chiave.split()))
        parole = re.findall(r'[a-z0-9]+', kw)
        ok_servizio = any(any(w.startswith(s) for w in parole) or s in kw for s in servizi)
        ok_luogo = not luoghi or any(l in kw for l in luoghi) or a.senza_luogo
        if not ok_servizio or not ok_luogo or any(e in kw for e in escludi) or chiave in viste:
            scartate += 1
            continue
        viste.add(chiave)
        tenute.append({
            'keyword': r['keyword'],
            'volume': campo(r, 'searchVolume', 'volume', 'search_volume'),
            'kd': campo(r, 'keywordDifficulty', 'kd', 'keyword_difficulty'),
            'cpc': round(campo(r, 'cpc'), 2) if campo(r, 'cpc') is not None else None,
            'concorrenza_annunci': campo(r, 'competition'),
            'intento': campo(r, 'intent', 'main_intent') or 'unknown',
        })

    peso = {'transactional': 0, 'commercial': 1, 'informational': 2, 'navigational': 3, 'unknown': 4}
    tenute.sort(key=lambda x: (peso.get(x['intento'], 4), x['kd'] if x['kd'] is not None else 50,
                               -(x['cpc'] or 0), -(x['volume'] or 0)))
    if a.json:
        json.dump({'tenute': tenute, 'scartate': scartate}, sys.stdout, ensure_ascii=False, indent=1)
        return
    print(f'# {len(tenute)} tenute, {scartate} scartate')
    print('keyword\tvolume\tkd\tcpc\tconc_annunci\tintento')
    for x in tenute:
        print('\t'.join(str(x[k]) if x[k] is not None else '-' for k in
                        ('keyword', 'volume', 'kd', 'cpc', 'concorrenza_annunci', 'intento')))


if __name__ == '__main__':
    main()
