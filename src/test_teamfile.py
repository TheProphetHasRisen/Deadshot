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

# missed games, recounted another way for one finished season and the live one: walk each roster
# week by week, ask Sleeper's list of who played, and add up what a regular starter's absence cost
import injuries as INJ
for y in [2023, TF.LIVE]:
    if y not in TF.YEARS: continue
    st = TF.settings(y); M, L = TF.season(y)
    R = [r for r in P.rosters(y)]
    G = [g for g in P.games(y) if g['status'] == 'postevent' and g['wk'] < st['po']]
    wks = {g['wk'] for g in G}
    PL = INJ.played(y); RP = L['repl']
    # draft-slot expectation, worked out here from Yahoo's rankings and draft directly
    import json as _j, os as _o
    TOTS = {}
    for pos in ('QB', 'RB', 'WR', 'TE', 'K', 'DEF'):
        tl = []
        for pg in range(4):
            fn = 'yahoo_raw/%d/rank_%s_%d.json' % (y, pos, pg)
            if not _o.path.exists(fn): break
            for x in _j.load(open(fn))['fantasy_content']['league'][1]['players'].values():
                if isinstance(x, dict) and 'player' in x:
                    for part in x['player'][1:]:
                        if isinstance(part, dict) and 'player_points' in part: tl.append(float(part['player_points']['total']))
        TOTS[pos] = tl
    ng = 17 if y != TF.LIVE else len(wks)
    seen = {}; TK = {}
    for pick, tm, pn, nfl, pp in P.draft(y):
        p0 = (pp or '').split(',')[0]; seen[p0] = seen.get(p0, 0) + 1
        if pn: TK[pn] = (p0, seen[p0])
    STARTN = dict(QB=10, RB=24, WR=25, TE=11, K=10, DEF=10)
    pts = {}
    for r in R:
        if r['wk'] in wks and PL(r['n'], r['pos'], r['nfl'], r['wk']): pts.setdefault(r['n'], []).append(r['pts'] or 0)
    tot = {}
    stints = {}
    for r in R:
        if r['wk'] in wks: stints.setdefault((r['team'], r['n']), []).append(r)
    for (team, n), rows in stints.items():
        played_rows = [r for r in rows if PL(r['n'], r['pos'], r['nfl'], r['wk'])]
        missed = [r for r in rows if r['wk'] != r.get('bye') and (r['slot'] == 'IR' or PL(r['n'], r['pos'], r['nfl'], r['wk']) is False)]
        if not missed: continue
        tk = TK.get(n); sp = None
        if tk:
            tl = TOTS.get(tk[0], []); sp = (tl[tk[1] - 1] if len(tl) >= tk[1] else (tl[-1] if tl else None))
            sp = None if sp is None else sp / ng
        gp = len(pts.get(n, [])); own = sum(pts[n]) / gp if gp else None
        if own is None and sp is None: continue
        is_starter = (played_rows and 2 * sum(1 for r in played_rows if r['slot'] not in ('BN', 'IR')) >= len(played_rows)) \
            or (tk is not None and tk[1] <= STARTN.get(tk[0], 0)) or any(r['slot'] == 'IR' for r in rows)
        if not is_starter: continue
        exp = ((own or 0) * gp + sp * 4) / (gp + 4) if sp is not None else own
        pos = (rows[0]['pos'] or '').split(',')[0]
        m = TF.mgr_of(y, team); g, v = tot.get(m, (0, 0.0))
        tot[m] = (g + len(missed), v + max(0.0, exp - RP.get(pos, 0)) * len(missed))
    for m, Z in M.items():
        g, v = tot.get(m, (0, 0.0))
        if g != Z['inj_g'] or abs(v - Z['inj_val']) > 0.05: bad.append('%d %s missed games %d / %.2f, team file %d / %.2f' % (y, m, g, v, Z['inj_g'], Z['inj_val']))
    print('  %d: missed games and value lost recounted for every team' % y)

if bad:
    print('TEAM FILES DO NOT MATCH a second working:'); [print('  ' + b) for b in bad[:30]]; sys.exit(1)
print('OK - team files match a second working (best lineups, wins above average, efficiency, bench, records, missed games)')
