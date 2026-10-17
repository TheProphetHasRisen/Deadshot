# -*- coding: utf-8 -*-
"""Trade grading 2.0 (Brian, 16 Oct 2026; PLANS.md section 1): each side against the team it would have been.

For every week from the deal on (regular season, weeks played), for each side:
  actual          points that counted from the players it received (started that week, while on the team)
  counterfactual  the same lineup with the deal undone: every slot a received player started in goes to the
                  player the old roster would have had there, chosen by projection (what was known that week,
                  not hindsight): his bench that week, plus the players he gave away
  net added       actual minus counterfactual. Both sides can be positive: both won.
  potential       the same with each roster's best possible lineup (hindsight): did the deal raise his ceiling,
                  whatever he did with it

Players nobody starts count for nothing on either side by construction, and uneven deals (two for one, a
quarterback for a receiver) need no special case: each vacated slot is refilled from whatever the old roster had.
"""
import json, os
import yahoo_parse as P
import teamfile as TF
import projections as PR

def grade(y, trades, played):
    """trades: [{wk, ta, tb, a: [player dicts received by ta], b: [received by tb]}] (wire2026's shape)"""
    st = TF.settings(y); slots = st['slots']
    R = [r for r in P.rosters(y) if r['wk'] <= played and r['wk'] < st['po']]
    by, where = {}, {}
    for r in R:
        by.setdefault((r['team'], r['wk']), []).append(r); where[(r['n'], r['wk'])] = r
    pj = PR.lookup(y, live=(y == TF.LIVE))
    # a player's points in a week he was on nobody's roster: Sleeper's, scored the league's way
    if y == TF.LIVE:
        dp = json.load(open('draft_points.json')) if os.path.exists('draft_points.json') else {}
        wkl = dp.get('wk%d' % y) or {}
        sl = lambda n, pos, nfl, w: (wkl.get(n) or [None] * 18)[w - 1]
    else:
        import sleeper_season as SL
        bk, _, _ = SL.weekly(y)
        sl = lambda n, pos, nfl, w: (SL.lookup(bk, n, pos, nfl)[1] or [None] * 18)[w - 1]
    info = {}
    for r in R: info.setdefault(r['n'], (r['pos'], r['nfl']))
    def row_of(n, w):
        r = where.get((n, w))
        if r: return dict(r, slot='BN', started=False)
        pos, nfl = info.get(n, (None, None))
        return dict(n=n, pos=pos, nfl=nfl, wk=w, slot='BN', started=False, pts=sl(n, pos, nfl, w) or 0)
    proj = lambda r: pj(r['n'], r['pos'], r['nfl'], r['wk'])
    out = []
    for x in trades:
        w0 = x['wk']; res = {}
        for side, team, got, gave in (('a', x['ta'], [p['n'] for p in x['a']], [p['n'] for p in x['b']]),
                                      ('b', x['tb'], [p['n'] for p in x['b']], [p['n'] for p in x['a']])):
            net = pot = 0.0; weeks = 0; detail = []
            for w in range(w0, played + 1):
                rows = by.get((team, w))
                if not rows: continue
                weeks += 1
                inc = [r for r in rows if r['n'] in got and r['started']]
                actual = sum(r['pts'] or 0 for r in inc)
                pool = [r for r in rows if r['n'] not in got and not r['started'] and r['slot'] != 'IR'] + [row_of(n, w) for n in gave]
                used, cf, fill = set(), 0.0, []
                for r in inc:
                    cand = [c for c in pool if id(c) not in used and TF.eligible(c['pos'], r['slot'])]
                    if not cand: fill.append((r['n'], None, 0)); continue
                    c = max(cand, key=lambda c: (proj(c) if proj(c) is not None else -1, c['pts'] or 0))
                    used.add(id(c)); cf += c['pts'] or 0; fill.append((r['n'], c['n'], c['pts'] or 0))
                net += actual - cf
                cf_roster = [r for r in rows if r['n'] not in got] + [row_of(n, w) for n in gave]
                pot += TF.optimal(rows, slots) - TF.optimal(cf_roster, slots)
                detail.append(dict(wk=w, actual=round(actual, 2), cf=round(cf, 2), fill=fill))
            res[side] = dict(net=round(net, 2), pot=round(pot, 2), weeks=weeks, detail=detail)
        out.append(res)
    return out
