# -*- coding: utf-8 -*-
"""Grade 2026's trades and waiver moves from what each player has scored since.

Reads season2026.py (the moves, typed from Yahoo) and draft_points.json (every player's points,
week by week, scored with Deadshot's rules by draft_points.py). export.py calls grade() and puts
the result on the page as D.live.wire.

Without Yahoo's lineups it cannot know who was started, so "points" here are what a player
scored while on that roster, started or benched. When Yahoo connects, this is the place to
swap in points that counted.

Which week a move counts from: every move is dated, not given a week, so a move counts from
the first week whose Sunday-morning lock (10:00 on the clock in Brian's screenshots) is still
ahead of it. A Tuesday pickup counts that week; a Sunday-afternoon one counts the next.
Thursday games are not split out.
"""
import datetime as dt

KICK1 = dt.datetime(2026, 9, 13, 10, 0)   # week 1's Sunday lock

def when(d, t='12:00 pm'):
    return dt.datetime.strptime(f'{d} 2026 {t}', '%b %d %Y %I:%M %p')

def week_of(ts):
    w = 1
    while ts >= KICK1 + dt.timedelta(days=7 * (w - 1)): w += 1
    return w

TRADE_TIMES = {'Sep 15': '11:27 am', 'Sep 29': '2:32 pm', 'Oct 13': '12:43 pm'}

# Small samples. A player with one game before a trade, or a team with one week, should not set
# the bar on a fluke. Each is eased toward what is typical, by PRIOR_G games' worth of it:
#   player baseline = (his points a game x his games + a typical starter at his position x 3) / (games + 3)
#   team pace       = (its all-play rate x weeks + .500 x 3) / (weeks + 3)
# With 1 game his own number counts a quarter; with 3, half; with 9, three quarters.
PRIOR_G = 3
# starters league-wide: QB, 2 RB, 2 WR, TE, a W/R/T flex, K, DEF on 10 teams (flex about 4 RB,
# 5 WR, 1 TE). "A typical starter" is the average of that many best, by points a game.
STARTERS = {'QB': 10, 'RB': 24, 'WR': 25, 'TE': 11, 'K': 10, 'DEF': 10}

def pos_rank(allwk, pos, mine, a, b):
    """where a points-a-game figure over weeks a..b ranks at a position, among every NFL player
    there who played at least half those weeks"""
    if mine is None or not allwk or pos not in allwk: return None
    need = (b - a + 2) // 2
    others = []
    for line in allwk[pos]:
        xs = [v for v in line[a - 1:b] if v is not None]
        if len(xs) >= need: others.append(sum(xs) / len(xs))
    return 1 + sum(1 for v in others if v > mine + 1e-9)

def team_form(games, t, w0, w1):
    """record, points a week and all-play rate for team t in weeks w0..w1"""
    W = L = 0; pts = []; apw = apn = 0
    for w in range(w0, w1 + 1):
        wg = [g for g in games if g['wk'] == w]
        if not wg: continue
        sc = {g['ta']: g['aa'] for g in wg} | {g['tb']: g['ab'] for g in wg}
        if t not in sc: continue
        me = sc[t]; pts.append(me)
        apw += sum(1 for o, v in sc.items() if o != t and me > v); apn += len(sc) - 1
        g = next(g for g in wg if t in (g['ta'], g['tb']))
        mine, theirs = (g['aa'], g['ab']) if g['ta'] == t else (g['ab'], g['aa'])
        W += mine > theirs; L += mine < theirs
    return dict(w=W, l=L, g=len(pts), ppg=round(sum(pts) / len(pts), 2) if pts else None,
                ap=round(apw / apn, 4) if apn else None)

def grade(S, wk, played, games=(), allwk=None, curve=None):
    """wk: {player: [points by week, None = no game]}; played: last week with stats;
    games: the season's results; allwk: {pos: every NFL player's weeks}, for ranks;
    curve: {pos: points a game, best first}, for a typical starter."""
    typical = {p: sum(curve[p][:n]) / n for p, n in STARTERS.items() if curve and len(curve.get(p, [])) >= n}
    pts = lambda n, a, b: [x for x in (wk.get(n) or [])[max(a, 1) - 1:min(b, played)] if x is not None]
    # every event oldest first: the draft, then each move and trade in the order Yahoo made them
    ev = [(dt.datetime(2026, 9, 1), 'draft', (team, name)) for _, team, name, _, _ in S.DRAFT2026]
    for i, (d, t, team, adds, drops) in enumerate(reversed(S.MOVES2026)):
        ev.append((when(d, t), 'move', (team, adds, drops, i)))
    for i, tr in enumerate(S.TRADES2026):
        ev.append((when(tr[0], TRADE_TIMES.get(tr[0], '12:00 pm')), 'trade', (tr, i)))
    ev.sort(key=lambda e: e[0])
    own, held, adds_out = {}, [], []
    def close(name, last):
        if name in own:
            team, start, kind = own.pop(name); held.append((name, team, start, last, kind))
    for ts, kind, x in ev:
        w = 1 if kind == 'draft' else week_of(ts)
        if kind == 'draft':
            own[x[1]] = (x[0], 1, 'draft')
        elif kind == 'move':
            team, adds, drops, _ = x
            for n, *_ in drops:
                if n not in own: own[n] = (team, 1, 'before')
                close(n, w - 1)
            for n, nfl, pos, how in adds:
                close(n, w - 1); own[n] = (team, w, how)
                adds_out.append(dict(n=n, nfl=nfl, pos=pos, how=how, team=team, d=ts.strftime('%b %-d'), wk=w))
        else:
            (d, ta, ga, tb, gb), _ = x
            for n in ga: close(n, w - 1); own[n] = (ta, w, 'trade')
            for n in gb: close(n, w - 1); own[n] = (tb, w, 'trade')
    for n, (team, start, kind) in list(own.items()): held.append((n, team, start, 99, kind))

    # pickups: what each added player has scored for the team that added him, while he was there
    picks = []
    for a in adds_out:
        h = next((h for h in held if h[0] == a['n'] and h[1] == a['team'] and h[2] == a['wk'] and h[4] == a['how']), None)
        if not h: continue
        p = pts(a['n'], h[2], h[3])
        if h[2] > played: continue
        picks.append(dict(a, until=None if h[3] >= 99 else h[3], g=len(p), pts=round(sum(p), 2)))
    picks.sort(key=lambda r: -r['pts'])

    # the ones that got away: a player dropped, and what he has scored since (and for whom)
    gone = []
    for i, (d, t, team, adds, drops) in enumerate(reversed(S.MOVES2026)):
        w = week_of(when(d, t))
        for n, nfl, pos in drops:
            if w > played: continue
            p = pts(n, w, played)
            later = [h for h in held if h[0] == n and h[2] >= w and h[1] != team]
            gone.append(dict(n=n, nfl=nfl, pos=pos, team=team, d=when(d, t).strftime('%b %-d'), wk=w, g=len(p),
                             pts=round(sum(p), 2), to=later[0][1] if later else None))
    gone.sort(key=lambda r: -r['pts'])

    # trades: each side's players before the deal (points a game) and since (total)
    trades = []
    for d, ta, ga, tb, gb in S.TRADES2026:
        w = week_of(when(d, TRADE_TIMES.get(d, '12:00 pm')))
        def side(names):
            out = []
            for n in names:
                pre, post = pts(n, 1, w - 1), pts(n, w, played); pos = S.TRADEPOS.get(n)
                pp = sum(pre) / len(pre) if pre else None
                qq = sum(post) / len(post) if post else None
                # against his own form, eased toward a typical starter while his sample is small
                ty = typical.get(pos)
                base = ((sum(pre) + ty * PRIOR_G) / (len(pre) + PRIOR_G) if ty is not None else pp) if pre or ty is not None else None
                out.append(dict(n=n, pos=pos, pre=None if pp is None else round(pp, 2), preG=len(pre),
                                post=round(sum(post), 2), postG=len(post),
                                base=None if base is None else round(base, 2), typical=None if ty is None else round(ty, 2),
                                chg=round(qq - base, 2) if base is not None and qq is not None else None,
                                rkPre=pos_rank(allwk, pos, pp, 1, w - 1) if w > 1 else None,
                                rkPost=pos_rank(allwk, pos, qq, w, played) if played >= w else None))
            return out
        def form(t):
            b4, af = team_form(games, t, 1, w - 1), team_form(games, t, w, played)
            pace = (b4['ap'] * b4['g'] + 0.5 * PRIOR_G) / (b4['g'] + PRIOR_G) if b4['ap'] is not None else None
            exp = round(pace * af['g'], 2) if pace is not None and af['g'] else None
            return dict(before=b4, since=af, pace=None if pace is None else round(pace, 4), xw=exp,
                        woe=round(af['w'] - exp, 2) if exp is not None else None)
        A, B = side(ga), side(gb)
        trades.append(dict(d=d, wk=w, ta=ta, tb=tb, a=A, b=B, weeksSince=max(0, played - w + 1),
                           aPost=round(sum(p['post'] for p in A), 2), bPost=round(sum(p['post'] for p in B), 2),
                           aPre=round(sum(p['pre'] or 0 for p in A), 2), bPre=round(sum(p['pre'] or 0 for p in B), 2),
                           # each side's players against their own form before the deal, a game, summed
                           aChg=round(sum(p['chg'] for p in A if p['chg'] is not None), 2) if played >= w else None,
                           bChg=round(sum(p['chg'] for p in B if p['chg'] is not None), 2) if played >= w else None,
                           fa=form(ta), fb=form(tb)))

    # how busy each team has been, and the claims that were fought over
    busy = {}
    for d, t, team, adds, drops in S.MOVES2026:
        b = busy.setdefault(team, dict(team=team, adds=0, drops=0, claims=0))
        b['adds'] += len(adds); b['drops'] += len(drops); b['claims'] += sum(1 for a in adds if a[3] == 'W')
    claims = [dict(d=d, n=n, team=w, pr=p, lost=[dict(team=t, pr=q) for t, q in lo]) for d, n, w, p, lo in S.CLAIMS2026]
    return dict(played=played, picks=picks, gone=gone, trades=trades,
                busy=sorted(busy.values(), key=lambda b: -b['adds']), claims=claims)
