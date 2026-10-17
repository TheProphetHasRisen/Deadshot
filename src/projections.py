# -*- coding: utf-8 -*-
"""Every player's projected points for every week, scored with Deadshot's rules (scoring.py), from Sleeper's
public weekly projections, which it keeps for past seasons. Used for spot starts (twice his projection), the
projected points beside every lineup call, the best and worst lineup calls, and the forecast.

    table(y)            -> {sleeper id or team: [projected points by week 1..18, None if none]}
    lookup(y)           -> f(name, positions, nfl, week) -> projected points or None

Finished seasons are cached in yahoo_raw/sleeper_proj_<year>.json and kept in the repo as proj_hist.json
(players ever on a Deadshot roster), so the scheduled job only reads the live season.
"""
import json, os
from scoring import score
import injuries

HIST = 'proj_hist.json'
OFF = ('QB', 'RB', 'WR', 'TE', 'K', 'DEF')

def _pull(y):
    out = {}
    for w in range(1, 19):
        try:
            rows = injuries._get('https://api.sleeper.com/projections/nfl/%d/%d?season_type=regular' % (y, w)
                                 + ''.join('&position[]=' + p for p in OFF))
        except Exception:
            continue
        for r in rows:
            pid, st = r.get('player_id'), r.get('stats') or {}
            pos = 'DEF' if pid and pid.isalpha() else (r.get('player') or {}).get('position')
            if not pid or pos not in OFF or not st: continue
            out.setdefault(pid, [None] * 18)[w - 1] = round(score(st, pos), 2)
    return out

def table(y, live=False):
    if not live and os.path.exists(HIST):
        h = json.load(open(HIST))
        if str(y) in h: return h[str(y)]
    f = 'yahoo_raw/sleeper_proj_%d.json' % y
    if os.path.exists(f) and not live: return json.load(open(f))
    t = _pull(y)
    if t: json.dump(t, open(f, 'w'))
    elif os.path.exists(f): t = json.load(open(f))
    return t

def lookup(y, live=False):
    T, ids = table(y, live), injuries._ids()
    def f(name, pos, nfl, wk):
        p0 = (pos or '').split(',')[0]
        if p0 == 'DEF':
            line = T.get(injuries.TEAMFIX.get(nfl, nfl))
        else:
            line = next((T[c] for c in injuries.cands(ids, name, pos) if c in T), None)
        return line[wk - 1] if line and 1 <= wk <= len(line) else None
    return f

def save_hist(years, keep):
    """proj_hist.json: finished seasons, only the players in keep[y] (Sleeper ids or teams ever rostered here)"""
    out = {}
    for y in years:
        t = table(y)
        out[str(y)] = {k: v for k, v in t.items() if k in keep.get(y, ()) or k.isalpha()}
    json.dump(out, open(HIST, 'w'), separators=(',', ':'))
    return {y: len(v) for y, v in out.items()}

if __name__ == '__main__':
    import sys
    for y in [int(a) for a in sys.argv[1:]]:
        t = table(y, live=(y == 2026)); print(y, len(t), 'players')
