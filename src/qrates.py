# -*- coding: utf-8 -*-
"""How often a player on the NFL's official injury report actually plays (USER, 17 Oct 2026), from every report
2021-2025, for players who had played in one of the two weeks before: every NFL player, not only Deadshot's. The reports come from nflverse's public data (the league's own
Wednesday-to-Friday reports, with each player's final practice status), and whether he played from Sleeper's
weekly stats (a game played is a gp). Fantasy positions only, regular season.

    rates()          -> {'Questionable': {'all': p, 'Did Not Participate In Practice': p, ...}, 'Doubtful': {...}, n...}
    current(y, wk)   -> {(normalised name, pos): (status, final practice status)} from this season's report
    chance(r, cur)   -> the chance a Deadshot player listed Q or D plays this week

qrates.json keeps the finished-season rates (committed); the live season's report is read each update.
"""
import csv, io, json, os, urllib.request
import injuries as I

HIST = 'qrates.json'
URL = 'https://github.com/nflverse/nflverse-data/releases/download/injuries/injuries_%d.csv'
POS = ('QB', 'RB', 'WR', 'TE', 'K')
GSIS = 'yahoo_raw/sleeper_gsis.json'

def _csv(y):
    f = 'yahoo_raw/nfl_injuries_%d.json' % y
    if y < 2026 and os.path.exists(f): return json.load(open(f))
    with urllib.request.urlopen(urllib.request.Request(URL % y, headers={'User-Agent': 'deadshot'}), context=I.CTX, timeout=60) as r:
        rows = [x for x in csv.DictReader(io.StringIO(r.read().decode('utf-8'))) if x['game_type'] == 'REG' and x['position'] in POS]
    if y < 2026: json.dump(rows, open(f, 'w'))
    return rows

def _gsis():
    if os.path.exists(GSIS): return json.load(open(GSIS))
    P = I._get('https://api.sleeper.app/v1/players/nfl')
    out = {p['gsis_id'].strip(): pid for pid, p in P.items() if p.get('gsis_id')}
    json.dump(out, open(GSIS, 'w')); return out

def rates(years=range(2021, 2026)):
    if os.path.exists(HIST): return json.load(open(HIST))
    G = _gsis(); cnt = {}
    for y in years:
        gp = I._gp(y)
        for x in _csv(y):
            st = x['report_status']
            if st not in ('Questionable', 'Doubtful', 'Out'): continue
            pid = G.get(x['gsis_id']); wk = int(x['week'])
            if not pid or wk not in gp: continue
            # players who were playing: a game in either of the two weeks before. A backup who never gets on the
            # field shows no game whether hurt or not, and would drag the rates down
            if not any(pid in gp.get(w, ()) for w in (wk - 1, wk - 2)): continue
            played = pid in gp[wk]
            for k in ('all', x['practice_status'] or 'unknown', 'pos:' + x['position']):
                c = cnt.setdefault(st, {}).setdefault(k, [0, 0]); c[0] += 1; c[1] += played
    out = {st: {k: dict(n=n, p=round(m / n, 3)) for k, (n, m) in v.items() if n >= 30} for st, v in cnt.items()}
    json.dump(out, open(HIST, 'w'), indent=1, sort_keys=True)
    return out

def current(y, wk):
    """this season's report for week wk: {(normalised name, position): (status, final practice status)}"""
    try: rows = _csv(y)
    except Exception: return {}
    return {(I.norm(x['full_name']), x['position']): (x['report_status'], x['practice_status'])
            for x in rows if int(x['week']) == wk and x['report_status']}

def chance(R, status, name, pos, cur):
    """the chance he plays: by his final practice status that week when the NFL report has him, else by his
    Yahoo status and position"""
    st = {'Q': 'Questionable', 'D': 'Doubtful'}.get(status)
    p0 = (pos or '').split(',')[0]
    rep = cur.get((I.norm(name), p0))
    if rep and rep[0] == 'Out': return 0.0
    if rep and rep[0] in R:   # the NFL's own report wins over Yahoo's label (A.J. Brown: IR-R on Yahoo, questionable to the NFL)
        return (R[rep[0]].get(rep[1]) or R[rep[0]]['all'])['p']
    if not st or st not in R: return None
    return (R[st].get('pos:' + p0) or R[st]['all'])['p']

if __name__ == '__main__':
    R = rates()
    for st, v in R.items():
        print(st); [print('   %-40s n=%5d plays %.0f%%' % (k, d['n'], d['p'] * 100)) for k, d in sorted(v.items(), key=lambda x: -x[1]['n'])]
