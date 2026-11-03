#!/usr/bin/env python3
"""Appiattisce le posizioni di OpenSEO (get_ranked_keywords) o di Manifold (seo_get_ranked_keywords).

  python3 -I posizioni.py risposta.json [--max 100] [--monitorate "ricerca 1;ricerca 2"] [--json]

Tiene: ricerca, posizione organica, pagina, volume, difficoltà, CPC, intento. Con --monitorate segna le ricerche
monitorate che non compaiono ("oltre 100").
"""
import argparse, json, sys


def flat(r):
    if 'keyword_data' in r:  # formato OpenSEO / DataForSEO grezzo
        kd_ = r['keyword_data'] or {}
        info = kd_.get('keyword_info') or {}
        el = (r.get('ranked_serp_element') or {}).get('serp_item') or {}
        return {'keyword': kd_.get('keyword'), 'posizione': el.get('rank_group'), 'url': el.get('relative_url') or el.get('url'),
                'volume': info.get('search_volume'), 'kd': (kd_.get('keyword_properties') or {}).get('keyword_difficulty'),
                'cpc': round(info['cpc'], 2) if info.get('cpc') is not None else None, 'intento': (kd_.get('search_intent_info') or {}).get('main_intent'),
                'tipo': el.get('type')}
    return {'keyword': r.get('keyword'), 'posizione': r.get('organic_rank') or r.get('rank'), 'url': r.get('url'),
            'volume': r.get('volume'), 'kd': r.get('kd'), 'cpc': round(r['cpc'], 2) if r.get('cpc') is not None else None, 'intento': r.get('intent'), 'tipo': r.get('type')}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('file')
    p.add_argument('--max', type=int, default=100)
    p.add_argument('--monitorate', default='')
    p.add_argument('--json', action='store_true')
    a = p.parse_args()
    d = json.load(open(a.file, encoding='utf-8'))
    grezze = d.get('keywords') or d.get('rows') or []
    righe = [flat(r) for r in grezze]
    righe = [r for r in righe if r['keyword'] and (r['tipo'] in (None, 'organic')) and (r['posizione'] or 999) <= a.max]
    righe.sort(key=lambda r: (r['posizione'] or 999))
    trovate = {r['keyword'].lower() for r in righe}
    mancanti = [m.strip() for m in a.monitorate.split(';') if m.strip() and m.strip().lower() not in trovate]
    if a.json:
        json.dump({'posizioni': righe, 'monitorate_oltre_100': mancanti}, sys.stdout, ensure_ascii=False, indent=1)
        return
    print('posizione\tkeyword\tpagina\tvolume\tkd\tcpc\tintento')
    for r in righe:
        print('\t'.join(str(r[k]) if r[k] is not None else '-' for k in ('posizione', 'keyword', 'url', 'volume', 'kd', 'cpc', 'intento')))
    for m in mancanti:
        print(f'oltre 100\t{m}\t-\t-\t-\t-\t-')


if __name__ == '__main__':
    main()
