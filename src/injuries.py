# -*- coding: utf-8 -*-
"""Who missed games, from 2021 on: worked out week by week, since Yahoo keeps no injury history.

A rostered player MISSED a week when his NFL team played (it was not his bye, which Yahoo's roster
records for each season) and he did not (Sleeper's public weekly stats mark every player who
played with gp). An IR slot that week counts as missed too. Injury, illness, suspension or a
benching all look the same from the outside, so the site calls it "missed games", not "injuries".

    played(y)  -> a function (player, position, NFL team, week) -> True, False, or None if unknown

Sleeper's replies are cached in yahoo_raw/ (gitignored) after the first pull.
"""
import json, os, re, ssl, urllib.request
try:
    import certifi; CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CTX = ssl.create_default_context()

def _get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'deadshot'}), context=CTX, timeout=90) as r:
        return json.load(r)

def norm(n):
    n = (n or '').lower().replace('.', '').replace("'", '').replace('’', '').replace('-', ' ')
    return re.sub(r'\b(jr|sr|ii|iii|iv|v)\b', '', n).replace('  ', ' ').strip()

ALIAS = {'hollywood brown': 'marquise brown', 'gabe davis': 'gabriel davis', 'chig okonkwo': 'chigoziem okonkwo',
         'josh palmer': 'joshua palmer', 'mitch trubisky': 'mitchell trubisky', 'eli mitchell': 'elijah mitchell'}
TEAMFIX = {'JAC': 'JAX', 'WSH': 'WAS', 'LA': 'LAR', 'OAK': 'LV'}

def _ids():
    f = 'yahoo_raw/sleeper_ids.json'
    if os.path.exists(f): return json.load(open(f))
    P = _get('https://api.sleeper.app/v1/players/nfl')
    out = {}
    for pid, p in P.items():
        if p.get('full_name') and p.get('position') in ('QB', 'RB', 'WR', 'TE', 'K'):
            out.setdefault(norm(p['full_name']) + '|' + p['position'], []).append(pid)
    json.dump(out, open(f, 'w'))
    return out

def _gp(y):
    f = 'yahoo_raw/sleeper_gp_%d.json' % y
    if os.path.exists(f) and y < 2026: return {int(k): set(v) for k, v in json.load(open(f)).items()}
    out = {}
    for w in range(1, 19):
        st = _get('https://api.sleeper.app/v1/stats/nfl/regular/%d/%d' % (y, w))
        ids = [pid for pid, s in st.items() if (s.get('gp') or 0) > 0]
        if ids: out[w] = ids
    json.dump(out, open(f, 'w'))
    return {int(k): set(v) for k, v in out.items()}

def played(y):
    ids, gp = _ids(), _gp(y)
    def f(name, pos, nfl, wk):
        if wk not in gp: return None
        p0 = (pos or '').split(',')[0]
        if p0 == 'DEF':
            return TEAMFIX.get(nfl, nfl) in gp[wk]
        cand = ids.get(ALIAS.get(norm(name), norm(name)) + '|' + p0, [])
        if not cand: return None
        return any(c in gp[wk] for c in cand)
    return f
