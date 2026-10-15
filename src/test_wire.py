# -*- coding: utf-8 -*-
"""Check the 2026 trade and waiver grades against a second, independent working.

    python3 test_wire.py

wire2026.py grades the trades and the waiver wire; export.py puts the result on the page as
D.live.wire. This recomputes every graded number from the raw inputs (the moves typed into
season2026.py, each player's weekly points in draft_points.json, the season's results in
site_data.json) WITHOUT importing wire2026, then compares. A formula slip in either shows up
as a mismatch. deploy.sh gates on it.
"""
import json, sys, datetime as dt
sys.path.insert(0, '.')
import season2026 as S

site = json.load(open('site_data.json'))['live']
W = site['wire']
dp = json.load(open('draft_points.json'))
wk, played = dp['wk2026'], int(dp['weeks']['2026'])
allwk, cpg = dp['allwk2026'], dp['curvePG2026']
# a typical starter: the average of the best 10 QB, 24 RB, 25 WR, 11 TE by points a game
TYP = {p: sum(cpg[p][:n]) / n for p, n in dict(QB=10, RB=24, WR=25, TE=11, K=10, DEF=10).items()}
def rank(pos, mine, a, b):
    if mine is None: return None
    pool = []
    for line in allwk[pos]:
        xs = [v for v in line[a - 1:b] if v is not None]
        if 2 * len(xs) >= (b - a + 1): pool.append(sum(xs) / len(xs))
    return 1 + len([v for v in pool if v > mine + 1e-9])
games = site['games']
bad = []

def near(a, b, tol=0.011):
    return (a is None and b is None) or (a is not None and b is not None and abs(a - b) <= tol)

def check(what, mine, theirs, tol=0.011):
    if not near(mine, theirs, tol): bad.append(f'{what}: expected {mine}, page has {theirs}')

# a move counts from the first week whose Sunday 10:00 lock is still ahead of it
LOCKS = [dt.datetime(2026, 9, 13, 10) + dt.timedelta(weeks=k) for k in range(20)]
def week_of(d, t):
    ts = dt.datetime.strptime(f'{d} 2026 {t}', '%b %d %Y %I:%M %p')
    return next(i + 1 for i, lk in enumerate(LOCKS) if ts < lk)

def ppg(n, a, b):
    xs = [v for i, v in enumerate(wk[n]) if a <= i + 1 <= min(b, played) and v is not None]
    return (sum(xs) / len(xs) if xs else None), len(xs), sum(xs)

def form(t, a, b):
    w = l = 0; pts = []; beat = faced = 0
    for k in range(a, b + 1):
        wg = [g for g in games if g['wk'] == k]
        sc = {}
        for g in wg: sc[g['ta']] = g['aa']; sc[g['tb']] = g['ab']
        if t not in sc: continue
        pts.append(sc[t])
        beat += sum(sc[t] > v for o, v in sc.items() if o != t); faced += len(sc) - 1
        g = [g for g in wg if t in (g['ta'], g['tb'])][0]
        me, op = (g['aa'], g['ab']) if g['ta'] == t else (g['ab'], g['aa'])
        w += me > op; l += me < op
    return w, l, (sum(pts) / len(pts) if pts else None), (beat / faced if faced else None), len(pts)

times = {'Sep 15': '11:27 am', 'Sep 29': '2:32 pm', 'Oct 13': '12:43 pm'}
assert len(W['trades']) == len(S.TRADES2026)
for (d, ta, ga, tb, gb), T in zip(S.TRADES2026, W['trades']):
    w = week_of(d, times[d]); check(f'{d} trade week', w, T['wk'], 0)
    for key, names, got in (('a', ga, T['a']), ('b', gb, T['b'])):
        chg = 0; tot = 0
        for n, P in zip(names, got):
            pre, _, _ = ppg(n, 1, w - 1); post, g, s = ppg(n, w, played)
            check(f'{d} {n} before a game', pre, P['pre']); check(f'{d} {n} points since', s if g else 0, P['post'])
            pos = S.TRADEPOS[n]; g0 = len([v for v in wk[n][:w - 1] if v is not None])
            bar = ((pre or 0) * g0 + TYP[pos] * 3) / (g0 + 3)
            check(f'{d} {n} bar', bar, P['base'], 0.02)
            mine_c = post - bar if post is not None else None
            check(f'{d} {n} against his own form', mine_c, P['chg'], 0.02)
            check(f'{d} {n} rank before', rank(pos, pre, 1, w - 1) if w > 1 else None, P['rkPre'], 0)
            check(f'{d} {n} rank since', rank(pos, post, w, played) if played >= w else None, P['rkPost'], 0)
            chg += mine_c or 0; tot += s
        check(f'{d} side {key} against own form', chg if played >= w else None, T[key + 'Chg'], 0.05)
        check(f'{d} side {key} points since', tot, T[key + 'Post'], 0.05)
    for key, t in (('a', ta), ('b', tb)):
        F = T['f' + key]
        bw, bl, bp, bap, bg = form(t, 1, w - 1); aw, al, ap_, aap, ag = form(t, w, played)
        check(f'{d} {t} wins before', bw, F['before']['w'], 0); check(f'{d} {t} losses before', bl, F['before']['l'], 0)
        check(f'{d} {t} points a week before', bp, F['before']['ppg']); check(f'{d} {t} all-play before', bap, F['before']['ap'], 0.0001)
        check(f'{d} {t} wins since', aw, F['since']['w'], 0); check(f'{d} {t} points a week since', ap_, F['since']['ppg'])
        pace = (bap * bg + 0.5 * 3) / (bg + 3) if bap is not None else None
        xw = pace * ag if pace is not None and ag else None
        check(f'{d} {t} expected wins since', xw, F['xw']); check(f'{d} {t} wins over pace', None if xw is None else aw - xw, F['woe'])

# pickups: replay every move and trade in order, tracking who holds whom from which week
ev = [(dt.datetime(2026, 9, 1), 0, ('draft', t, n)) for _, t, n, _, _ in S.DRAFT2026]
for i, (d, t, team, adds, drops) in enumerate(reversed(S.MOVES2026)):
    ev.append((dt.datetime.strptime(f'{d} 2026 {t}', '%b %d %Y %I:%M %p'), 1 + i, ('move', team, adds, drops, d, t)))
for d, ta, ga, tb, gb in S.TRADES2026:
    ev.append((dt.datetime.strptime(f'{d} 2026 {times[d]}', '%b %d %Y %I:%M %p'), 9999, ('trade', ta, ga, tb, gb, d)))
ev.sort(key=lambda e: (e[0], e[1]))
hold, stints = {}, []
for ts, _, x in ev:
    if x[0] == 'draft': hold[x[2]] = (x[1], 1, 'draft'); continue
    w = 1 + sum(ts >= lk for lk in LOCKS)
    if x[0] == 'move':
        _, team, adds, drops, d, t = x
        for n, *_ in drops:
            prev = hold.pop(n, (team, 1, 'before')); stints.append((n, prev[0], prev[1], w - 1, prev[2]))
        for n, nfl, pos, how in adds:
            if n in hold: prev = hold.pop(n); stints.append((n, prev[0], prev[1], w - 1, prev[2]))
            hold[n] = (team, w, how)
    else:
        _, ta, ga, tb, gb, d = x
        for n, t in [(n, ta) for n in ga] + [(n, tb) for n in gb]:
            if n in hold: prev = hold.pop(n); stints.append((n, prev[0], prev[1], w - 1, prev[2]))
            hold[n] = (t, w, 'trade')
for n, (t, w0, k) in hold.items(): stints.append((n, t, w0, 99, k))
mine = sorted(((n, t, round(ppg(n, a, b)[2], 2)) for n, t, a, b, k in stints if k in ('FA', 'W') and a <= played),
              key=lambda r: -r[2])
page = [(p['n'], p['team'], p['pts']) for p in W['picks']]
for m, p in zip(mine[:15], page[:15]):
    if m[2] != p[2]: bad.append(f'pickup points: expected {m}, page has {p}')

if bad:
    print('TRADE AND WAIVER GRADES DO NOT MATCH a second working:'); [print('  ' + b) for b in bad[:40]]
    sys.exit(1)
print(f'OK - 2026 grades match a second working ({len(W["trades"])} trades, every player, both teams each side, '
      f'{min(15, len(mine))} top pickups, ranks and small-sample bars)')
