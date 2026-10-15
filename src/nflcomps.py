# -*- coding: utf-8 -*-
"""Which NFL team is each manager? (a league member's ask, Oct 2026)

Each manager's whole Deadshot career and each NFL franchise's last ten seasons (nfl_teams.py,
2016-2025) are described by the same seven things:

    win %                      regular season
    playoff rate               share of seasons in the playoffs
    title rate                 championships a season
    final rate                 reached the final (Super Bowl) a season
    playoff wins a trip        playoff games won per playoff appearance
    consistency                spread of his season-by-season win % (lower is steadier)
    trend                      win % over the last three seasons minus his whole span

Each is turned into a z-score within its own world (managers against managers, NFL teams against
NFL teams), so "makes the playoffs a lot" means the same thing in a 10-team league as in a
32-team one. Managers and franchises are then paired so the total distance over everyone is as small
as it can be, each franchise used once. export.py calls comps() and puts the result in D.comps.
"""
import math
import nfl_teams as N

MERGE = {'SD': 'LAC', 'OAK': 'LV'}   # same franchise, moved city mid-decade
W = dict(wp=1.5, po=1.0, ti=2.0, fi=1.2, pw=0.7, sd=0.4, tr=0.5)
LABEL = dict(wp='win %', po='playoff rate', ti='titles', fi='finals', pw='playoff wins a trip', sd='consistency', tr='trend')

def _sd(v):
    m = sum(v) / len(v); return math.sqrt(sum((x - m) ** 2 for x in v) / len(v))

def _profile(seasons):
    """seasons: list of dicts with w, l, t, po, pw, fin (reached final), ti (titles, fractional ok)"""
    wp = [(s['w'] + s['t'] / 2) / max(1, s['w'] + s['l'] + s['t']) for s in seasons]
    tot_w = sum(s['w'] + s['t'] / 2 for s in seasons); tot_g = sum(s['w'] + s['l'] + s['t'] for s in seasons)
    n = len(seasons); apps = sum(1 for s in seasons if s['po'])
    last = seasons[-3:]
    lw = sum(s['w'] + s['t'] / 2 for s in last) / max(1, sum(s['w'] + s['l'] + s['t'] for s in last))
    return dict(wp=tot_w / tot_g, po=apps / n, ti=sum(s['ti'] for s in seasons) / n, fi=sum(s['fin'] for s in seasons) / n,
                pw=sum(s['pw'] for s in seasons) / apps if apps else 0, sd=_sd(wp) if n > 1 else 0, tr=lw - tot_w / tot_g,
                n=n, w=sum(s['w'] for s in seasons), l=sum(s['l'] for s in seasons), t=sum(s['t'] for s in seasons),
                apps=apps, titles=sum(s['ti'] for s in seasons), finals=sum(s['fin'] for s in seasons))

def _z(pop):
    keys = list(W)
    mu = {k: sum(p[k] for p in pop.values()) / len(pop) for k in keys}
    sd = {k: _sd([p[k] for p in pop.values()]) or 1 for k in keys}
    return {name: {k: (p[k] - mu[k]) / sd[k] for k in keys} for name, p in pop.items()}

def _assign(cost):
    """the pairing of managers (rows) to franchises (columns) with the smallest total distance, each
    franchise used once (the Hungarian method). A closest-first pairing can leave the last managers
    with whatever is left; this finds the best fit for everyone together."""
    n, m = len(cost), len(cost[0]); INF = float('inf')
    u, v, p, way = [0.0] * (n + 1), [0.0] * (m + 1), [0] * (m + 1), [0] * (m + 1)
    for i in range(1, n + 1):
        p[0] = i; j0 = 0; minv = [INF] * (m + 1); used = [False] * (m + 1)
        while True:
            used[j0] = True; i0 = p[j0]; delta = INF; j1 = 0
            for j in range(1, m + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]: minv[j] = cur; way[j] = j0
                    if minv[j] < delta: delta = minv[j]; j1 = j
            for j in range(m + 1):
                if used[j]: u[p[j]] += delta; v[j] -= delta
                else: minv[j] -= delta
            j0 = j1
            if p[j0] == 0: break
        while True:
            j1 = way[j0]; p[j0] = p[j1]; j0 = j1
            if not j0: break
    return [(p[j] - 1, j - 1) for j in range(1, m + 1) if p[j]]

def comps(rows, games, min_seasons=3):
    """rows: the record book's team-seasons (y, mgr, w, l, t, po, place, share); games: its playoff games"""
    nfl = {}
    for y, teams in sorted(N.SEASONS.items()):
        for ab, r in teams.items():
            nfl.setdefault(MERGE.get(ab, ab), []).append(dict(w=r['w'], l=r['l'], t=r['t'], po=r['po'], pw=r['pw'], fin=r['sb'], ti=r['sbw']))
    pwins = {}
    for g in games:
        if g.get('void'): continue
        win = g['ma'] if g['pa'] > g['pb'] else g['mb']
        pwins[(g['y'], win)] = pwins.get((g['y'], win), 0) + 1
    mg = {}
    for r in sorted(rows, key=lambda r: r['y']):
        mg.setdefault(r['mgr'], []).append(dict(w=r['w'], l=r['l'], t=r['t'], po=bool(r['po']), pw=pwins.get((r['y'], r['mgr']), 0),
                                               fin=1 if r.get('place') in (1, 2) else 0, ti=r.get('share') or 0))
    mg = {m: s for m, s in mg.items() if len(s) >= min_seasons}
    P = {m: _profile(s) for m, s in mg.items()}; Q = {t: _profile(s) for t, s in nfl.items()}
    ZP, ZQ = _z(P), _z(Q)
    dist = lambda a, b: math.sqrt(sum(W[k] * (a[k] - b[k]) ** 2 for k in W))
    ms, ts = sorted(ZP), sorted(ZQ)
    cost = [[dist(ZP[m], ZQ[t]) for t in ts] for m in ms]
    out = []
    for i, j in _assign(cost):
        m, t = ms[i], ts[j]; d = cost[i][j]
        # what makes them alike: the three traits where the two sit closest, among the ones that stand out
        alike = sorted(W, key=lambda k: abs(ZP[m][k] - ZQ[t][k]) - 0.35 * abs(ZP[m][k]))[:3]
        runner = min((x for x in ZQ if x != t), key=lambda x: dist(ZP[m], ZQ[x]))
        out.append(dict(mgr=m, team=t, name=N.NAMES.get(t, t), dist=round(d, 3), alike=[LABEL[k] for k in alike],
                        also=N.NAMES.get(runner, runner), me=P[m], them=Q[t],
                        zme={k: round(v, 2) for k, v in ZP[m].items()}, zthem={k: round(v, 2) for k, v in ZQ[t].items()}))
    out.sort(key=lambda o: -o['me']['wp'])
    return dict(pairs=out, seasons=[min(N.SEASONS), max(N.SEASONS)], minSeasons=min_seasons)

if __name__ == '__main__':
    import json
    d = json.load(open('site_data.json'))
    c = comps(d['rows'], d['games'])
    for o in c['pairs']:
        me, th = o['me'], o['them']
        print('%-18s %-24s  %d-%d %d/%d po %.1f ti | %d-%d %d/%d po %d SB  (alike: %s; also %s)' % (
            o['mgr'], o['name'], me['w'], me['l'], me['apps'], me['n'], me['titles'], th['w'], th['l'], th['apps'], th['n'], th['titles'],
            ', '.join(o['alike']), o['also']))
