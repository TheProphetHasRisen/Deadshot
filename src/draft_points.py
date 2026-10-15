# -*- coding: utf-8 -*-
"""Score every drafted player with Deadshot's own scoring, to find the draft's steals and busts.

    python3 draft_points.py

Pulls each week's NFL box-score stats from Sleeper's public API (no key, read only) and scores
them with the league's settings (league_rules_2026.md / test_rules.js): full PPR, 25 passing
yards a point, 4 per passing TD, -1 per interception, 10 rushing/receiving yards a point,
6 per TD, -2 per fumble lost, 2 per two-point conversion; kickers 3/3/3/4/5 by distance and 1
per extra point; defenses 1 per sack, 2 per interception and fumble recovery, 6 per TD,
3 per safety, 2.5 per blocked kick, 1 per 4th-down stop, 0.5 per three-and-out, and the
points-allowed scale 10/7/4/2/0/-1/-4.

For each drafted player it records his points and where that put him at his position among
EVERY player in the NFL, so a pick can be judged: drafted as the 12th running back, finished
as the 3rd. Writes draft_points.json, which export.py reads. Re-run it each week in season.
"""
import json, re, sys, urllib.request, ssl
sys.path.insert(0, '.')
import season2026 as S

try:
    import certifi; CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CTX = ssl.create_default_context()

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'deadshot'}), context=CTX, timeout=60) as r:
        return json.load(r)

SEASONS = {2025: range(1, 18), 2026: range(1, 6)}
g = lambda s, k: float(s.get(k) or 0)

def pa_pts(pa):
    return 10 if pa == 0 else 7 if pa <= 6 else 4 if pa <= 13 else 2 if pa <= 20 else 0 if pa <= 27 else -1 if pa <= 34 else -4

def score(s, pos):
    if pos == 'DEF':
        return (g(s, 'sack') + 2 * g(s, 'int') + 2 * g(s, 'fum_rec') + 6 * (g(s, 'def_td') + g(s, 'def_st_td'))
                + 3 * g(s, 'safe') + 2.5 * g(s, 'blk_kick') + g(s, 'def_4_and_stop') + 0.5 * g(s, 'def_3_and_out')
                + (pa_pts(g(s, 'pts_allow')) if 'pts_allow' in s else 0))
    if pos == 'K':
        fifty = g(s, 'fgm_50p') if 'fgm_50p' in s else g(s, 'fgm_50_59') + g(s, 'fgm_60p')
        return (3 * (g(s, 'fgm_0_19') + g(s, 'fgm_20_29') + g(s, 'fgm_30_39')) + 4 * g(s, 'fgm_40_49') + 5 * fifty + g(s, 'xpm'))
    return (g(s, 'pass_yd') / 25 + 4 * g(s, 'pass_td') - g(s, 'pass_int') + g(s, 'rush_yd') / 10 + 6 * g(s, 'rush_td')
            + g(s, 'rec') + g(s, 'rec_yd') / 10 + 6 * g(s, 'rec_td') - 2 * g(s, 'fum_lost')
            + 2 * (g(s, 'pass_2pt') + g(s, 'rush_2pt') + g(s, 'rec_2pt'))
            + 6 * (g(s, 'kr_td') + g(s, 'pr_td') + g(s, 'st_td') + g(s, 'fum_rec_td')))

def norm(n):
    n = n.lower().replace('.', '').replace("'", '').replace('-', ' ')
    return re.sub(r'\b(jr|sr|ii|iii|iv|v)\b', '', n).replace('  ', ' ').strip()

print('players...'); P = get('https://api.sleeper.app/v1/players/nfl')
pos_of = {pid: (p.get('position') or '') for pid, p in P.items()}
by_name = {}
for pid, p in P.items():
    if p.get('full_name') and p.get('position') in ('QB', 'RB', 'WR', 'TE', 'K'):
        by_name.setdefault((norm(p['full_name']), p['position']), []).append(pid)

# the name Yahoo's draft room uses, and the one Sleeper files him under
ALIAS = {'Hollywood Brown': 'Marquise Brown'}
ANYPOS = {'Travis Hunter'}   # two-way player: Yahoo lists him at WR, Sleeper at CB
for pick, team, name, nfl, pos in S.DRAFT2025 + S.DRAFT2026:   # score and rank him where he was drafted
    if name in ANYPOS:
        for pid, p in P.items():
            if norm(p.get('full_name') or '') == norm(name) and p.get('active'):
                pos_of[pid] = pos; by_name.setdefault((norm(name), pos), []).append(pid)

out = {}
for y, weeks in SEASONS.items():
    tot, wk = {}, {}
    for w in weeks:
        print(y, 'week', w); st = get(f'https://api.sleeper.app/v1/stats/nfl/regular/{y}/{w}')
        for pid, s in st.items():
            pos = 'DEF' if pid.isalpha() else pos_of.get(pid, '')
            if pos in ('QB', 'RB', 'WR', 'TE', 'K', 'DEF'):
                v = score(s, pos); tot[pid] = tot.get(pid, 0) + v
                wk.setdefault(pid, {})[w] = round(v, 2)
    rank_pos = {}
    for pid, pts in tot.items():
        pos = 'DEF' if pid.isalpha() else pos_of[pid]
        rank_pos.setdefault(pos, []).append((pts, pid))
    rk = {}
    for pos, lst in rank_pos.items():
        lst.sort(reverse=True)
        for i, (pts, pid) in enumerate(lst): rk[pid] = i + 1
    # what the Nth best at each position scored: the points a pick at that slot "should" have
    out['curve' + str(y)] = {pos: [round(p, 1) for p, _ in lst[:250]] for pos, lst in rank_pos.items()}
    # the same, a game at a time, for players with at least half the weeks: replacement level is
    # judged per game, as the players set against it are
    need = (len(weeks) + 1) // 2; pg = {}
    for pid, pts in tot.items():
        ng = len(wk.get(pid, {}))
        if ng >= need: pg.setdefault('DEF' if pid.isalpha() else pos_of[pid], []).append(pts / ng)
    out['curvePG' + str(y)] = {pos: [round(v, 2) for v in sorted(l, reverse=True)[:250]] for pos, l in pg.items()}
    draft = S.DRAFT2026 if y == 2026 else S.DRAFT2025
    res, miss = {}, []
    for pick, team, name, nfl, pos in draft:
        if pos == 'DEF':
            pid = {'WAS': 'WAS', 'LAR': 'LAR', 'LAC': 'LAC', 'JAX': 'JAX'}.get(nfl, nfl)
        else:
            ids = by_name.get((norm(ALIAS.get(name, name)), pos), [])
            if len(ids) > 1: ids = [i for i in ids if i in tot] or ids
            pid = ids[0] if ids else None
        if not pid: miss.append(name); continue
        res[name] = [round(tot.get(pid, 0.0), 2), rk.get(pid)]
    if miss: print('  NOT MATCHED', y, miss)
    out[str(y)] = res
    if y == max(SEASONS):
        # week by week for everyone drafted, traded, added or dropped this season: what grades the
        # trades and the waiver wire. None means no stats that week (a bye, hurt, or inactive).
        names = {(n, nfl, pos) for _, _, n, nfl, pos in draft}
        for _, _, _, adds, drops in S.MOVES2026:
            names |= {(a[0], a[1], a[2]) for a in adds} | {(d[0], d[1], d[2]) for d in drops}
        for t in S.TRADES2026:
            names |= {(n, None, S.TRADEPOS[n]) for n in t[2] + t[4]}
        per, miss = {}, []
        for n, nfl, pos in sorted(names, key=lambda x: (x[0], x[1] or '')):
            if n in per: continue
            if pos == 'DEF': pid = nfl
            else:
                ids = by_name.get((norm(ALIAS.get(n, n)), pos), [])
                if len(ids) > 1: ids = [i for i in ids if i in tot] or ids
                pid = ids[0] if ids else None
            if not pid: miss.append(n); continue
            per[n] = [wk.get(pid, {}).get(w) for w in weeks]
        if miss: print('  NO WEEKLY LINE', miss)
        out['wk' + str(y)] = per
out['weeks'] = {str(y): max(w) for y, w in SEASONS.items()}
json.dump(out, open('draft_points.json', 'w'), indent=1)
print('wrote draft_points.json')
