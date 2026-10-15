# -*- coding: utf-8 -*-
"""Check the team files a second way.

    python3 test_teamfile.py

teamfile.py builds each week's best possible lineup greedily (best at each fixed slot, then the
best of the rest at the flex). Here every legal lineup is tried by brute force for every team-week
of the live season and the last full one, and the totals must agree. Then wins above average,
lineup efficiency and points left on the bench are recomputed from the raw rosters and scores.
"""
import sys, itertools
import yahoo_parse as P
import teamfile as TF

bad = []
def best_brute(players, slots):
    pl = [p for p in players if p['slot'] != 'IR']
    by = lambda pos: [p for p in pl if pos in (p['pos'] or '').split(',')]
    best = 0.0
    def pts(ps): return sum(p['pts'] or 0 for p in ps)
    for qb in itertools.combinations(by('QB'), min(slots.get('QB', 0), len(by('QB')))):
        for rb in itertools.combinations(by('RB'), min(slots.get('RB', 0), len(by('RB')))):
            for wr in itertools.combinations(by('WR'), min(slots.get('WR', 0), len(by('WR')))):
                for te in itertools.combinations(by('TE'), min(slots.get('TE', 0), len(by('TE')))):
                    used = {id(p) for p in qb + rb + wr + te}
                    flex = [p for p in pl if id(p) not in used and any(x in ('RB', 'WR', 'TE') for x in (p['pos'] or '').split(','))]
                    fx = max((p['pts'] or 0 for p in flex), default=0) if slots.get('W/R/T') else 0
                    k = max((p['pts'] or 0 for p in by('K')), default=0)
                    d = max((p['pts'] or 0 for p in by('DEF')), default=0)
                    best = max(best, pts(qb + rb + wr + te) + fx + k + d)
    return best

for y in [TF.LIVE, TF.LIVE - 1]:
    if y not in TF.YEARS: continue
    st = TF.settings(y)
    R = P.rosters(y); by = {}
    for r in R: by.setdefault((r['team'], r['wk']), []).append(r)
    n = 0
    for (t, w), pl in by.items():
        if w >= st['po']: continue
        a, b = TF.optimal(pl, st['slots']), best_brute(pl, st['slots'])
        n += 1
        if abs(a - b) > 0.005: bad.append('%d %s week %d best lineup %.2f, brute force %.2f' % (y, t, w, a, b))
    M, _ = TF.season(y)
    G = [g for g in P.games(y) if g['status'] == 'postevent' and g['wk'] < st['po']]
    for m, Z in M.items():
        t = Z['team']; apw = apl = act = opt = 0.0; g = 0
        for wk in sorted({x['wk'] for x in G}):
            sc = {}
            for x in G:
                if x['wk'] == wk: sc[x['ta']] = x['aa']; sc[x['tb']] = x['ab']
            if t not in sc: continue
            g += 1
            apw += sum(sc[t] > v for o, v in sc.items() if o != t); apl += sum(sc[t] < v for o, v in sc.items() if o != t)
            pl = by.get((t, wk), [])
            act += sum(p['pts'] or 0 for p in pl if p['slot'] not in ('BN', 'IR')); opt += best_brute(pl, st['slots'])
        waa = (apw / (apw + apl) - .5) * g
        for k, mine in (('waa', waa), ('eff', act / opt if opt else None), ('left', (opt - act) / g)):
            if mine is not None and abs(mine - Z[k]) > 0.005: bad.append('%d %s %s: %.4f, team file %.4f' % (y, m, k, mine, Z[k]))
    print('  %d: %d team-weeks of best lineups checked by brute force' % (y, n))

# every finished season's win-loss, from Yahoo, must equal the record book's
import data as DB
for y in TF.YEARS:
    if y == TF.LIVE: continue
    M, _ = TF.season(y)
    book = {TF._plain(r[1]): (r[2], r[3]) for r in DB.STANDINGS[y]}
    for m, Z in M.items():
        if (Z['w'], Z['l']) != book.get(TF._plain(Z['team'])):
            bad.append('%d %s: Yahoo %d-%d, record book %s' % (y, m, Z['w'], Z['l'], book.get(TF._plain(Z['team']))))
print('  records: every finished season Yahoo reaches checked against the record book')

if bad:
    print('TEAM FILES DO NOT MATCH a second working:'); [print('  ' + b) for b in bad[:30]]; sys.exit(1)
print('OK - team files match a second working (best lineups, wins above average, efficiency, bench, records)')
