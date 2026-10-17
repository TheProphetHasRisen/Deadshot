# -*- coding: utf-8 -*-
"""The forecast (Brian, 16 Oct 2026; PLANS.md section 4): the rest of the live season, played 100,000 times.

Each team's expected score for each week still to play:
    league average  +  b1 x (his projected best lineup that week  -  the league's)  +  b2 x (his scoring so far  -  the league's)
  * his projected lineup is built from the players on his roster now, each with Sleeper's projection for THAT
    week, scored the league's way. A player out injured, suspended, on a bye or not yet back projects 0 for
    the weeks he will miss and his full value from the week he returns, so injuries, returns, suspensions and
    byes all come in through it. IR slots count: a player stashed there is back in the lineup when he is.
  * b1 and b2 are fitted on every Deadshot season Yahoo reaches (2021-2025): the same number of weeks played,
    each later week's score against the projected lineup and the form to date. In this league both are weak
    (week to week, scores are close to a coin flip around the average), so the fit shrinks both hard and the
    swing around the expected score is the week-to-week spread that is left.
Then the real schedule is played out: wins, then points for (how Yahoo has seeded every tie since 2021); the
top six make it, the top two get byes; the bracket re-seeds after the first round (the 1 seed meets the lowest
seed left).

Returned for the page: every team's odds (playoffs, bye, title, each seed), projected wins and points, the
record he needs (playoff odds at each final win total), this week's swing (odds if he wins, if he loses), each
matchup this week, the schedule still to play, his players out and when they are back, and the odds after
every week played so far (re-run as the season stood then).
"""
import math, random
import yahoo_parse as P
import teamfile as TF
import projections as PR

N, N_PAST = 1000000, 20000   # a million seasons for the week ahead (USER, 16 Oct 2026); 20,000 for each past week's re-run
OUT = ('O', 'IR', 'PUP-R', 'PUP-P', 'SUSP', 'NFI-R', 'NFI-A', 'D', 'Q', 'IR-R', 'COVID-19', 'NA')

def _lineup(rows, wk, pj, slots):
    """projected best lineup that week from these players (IR included: projections zero him until he is back)"""
    pr = [dict(r, slot='BN', pts=(pj(r['n'], r['pos'], r['nfl'], wk) or 0)) for r in rows]
    return TF.optimal(pr, slots)

def fit(k):
    """b1, b2 and the spread left, from every finished season: k weeks played, every later regular-season week"""
    X, Y = [], []
    for y in [y for y in TF.YEARS if y != TF.LIVE]:
        st = TF.settings(y); slots = st['slots']; pj = PR.lookup(y)
        R = P.rosters(y); G = [g for g in P.games(y) if g['status'] == 'postevent' and g['wk'] < st['po']]
        sc = {}
        for g in G: sc[(g['ta'], g['wk'])] = g['aa']; sc[(g['tb'], g['wk'])] = g['ab']
        teams = {t for t, _ in sc}; weeks = sorted({w for _, w in sc})
        if len(weeks) <= k: continue
        lg_k = sum(v for (t, w), v in sc.items() if w <= k) / sum(1 for (t, w) in sc if w <= k)
        lvl = {t: sum(sc[(t, w)] for w in range(1, k + 1) if (t, w) in sc) / k - lg_k for t in teams}
        by = {}
        for r in R: by.setdefault((r['team'], r['wk']), []).append(r)
        for w in weeks:
            if w <= k: continue
            pl = {t: _lineup(by.get((t, w), []), w, pj, slots) for t in teams}
            pm = sum(pl.values()) / len(pl); am = sum(sc[(t, w)] for t in teams) / len(teams)
            for t in teams: X.append((pl[t] - pm, lvl[t])); Y.append(sc[(t, w)] - am)
    n = len(X)
    sxx = sum(a * a for a, _ in X); syy = sum(b * b for _, b in X); sxy = sum(a * b for a, b in X)
    sxr = sum(a * r for (a, _), r in zip(X, Y)); syr = sum(b * r for (_, b), r in zip(X, Y))
    det = sxx * syy - sxy * sxy
    b1 = (sxr * syy - syr * sxy) / det; b2 = (syr * sxx - sxr * sxy) / det
    res = [r - b1 * a - b2 * b for (a, b), r in zip(X, Y)]
    # the score spread around the expected score, plus the spread of the league average week to week
    return dict(b1=b1, b2=b2, sd=math.sqrt(sum(e * e for e in res) / n), n=n)

def season_state(y, k):
    """the season as it stood after week k: records, points, form, rosters, schedule left"""
    st = TF.settings(y); R = P.rosters(y)
    G = [g for g in P.games(y) if g['wk'] < st['po']]
    done = [g for g in G if g['status'] == 'postevent' and g['wk'] <= k]
    left = [g for g in G if g['wk'] > k]
    rec = {}
    for g in done:
        for t, a, b in ((g['ta'], g['aa'], g['ab']), (g['tb'], g['ab'], g['aa'])):
            r = rec.setdefault(t, [0, 0, 0.0, []]); r[0] += a > b; r[1] += a < b; r[2] += a; r[3].append(a)
    rw = max([r['wk'] for r in R if r['wk'] <= k + 1] or [1])
    roster = {}
    for r in R:
        if r['wk'] == rw: roster.setdefault(r['team'], []).append(r)
    return st, rec, roster, left, rw

def run(y, k, n, rnd, F=None):
    st, rec, roster, left, rw = season_state(y, k)
    teams = sorted(rec); slots = st['slots']; pj = PR.lookup(y, live=(y == TF.LIVE))
    F = F or fit(k)
    lg = sum(r[2] for r in rec.values()) / max(1, sum(len(r[3]) for r in rec.values()))
    lvl = {t: rec[t][2] / max(1, len(rec[t][3])) - lg for t in teams}
    weeks = sorted({g['wk'] for g in left})
    proj = {(t, w): _lineup(roster.get(t, []), w, pj, slots) for t in teams for w in weeks}
    pm = {w: sum(proj[(t, w)] for t in teams) / len(teams) for w in weeks}
    mu = {(t, w): lg + F['b1'] * (proj[(t, w)] - pm[w]) + F['b2'] * lvl[t] for t in teams for w in weeks}
    sd = F['sd']
    nxt = weeks[0] if weeks else None
    po = {t: 0 for t in teams}; bye = dict(po); title = dict(po); wins = {t: 0.0 for t in teams}; pts = dict(wins)
    seed = {t: [0] * len(teams) for t in teams}
    finalW = {t: {} for t in teams}                      # final wins -> [seasons, made playoffs]
    swing = {t: [0, 0, 0, 0] for t in teams}             # won next week: [n, made it]; lost: [n, made it]
    mwin = {}
    nspots = 6
    for _ in range(n):
        W = {t: rec[t][0] for t in teams}; PF = {t: rec[t][2] for t in teams}; nx = {}
        for g in left:
            a, b = g['ta'], g['tb']
            sa = rnd.gauss(mu[(a, g['wk'])], sd); sb = rnd.gauss(mu[(b, g['wk'])], sd)
            PF[a] += sa; PF[b] += sb; win = a if sa > sb else b; W[win] += 1
            if g['wk'] == nxt: nx[a] = win == a; nx[b] = win == b; mwin[(a, b)] = mwin.get((a, b), 0) + (win == a)
        order = sorted(teams, key=lambda t: (-W[t], -PF[t]))
        made = set(order[:nspots])
        for i, t in enumerate(order): seed[t][i] += 1
        for t in teams:
            wins[t] += W[t]; pts[t] += PF[t]
            fw = finalW[t].setdefault(W[t], [0, 0]); fw[0] += 1; fw[1] += t in made
            if t in nx:
                s = swing[t]
                if nx[t]: s[0] += 1; s[1] += t in made
                else: s[2] += 1; s[3] += t in made
        for t in made: po[t] += 1
        for t in order[:2]: bye[t] += 1
        s = order[:nspots]
        play = lambda x, z: x if rnd.gauss(lg + F['b2'] * lvl[x], sd) > rnd.gauss(lg + F['b2'] * lvl[z], sd) else z
        q = [play(s[2], s[5]), play(s[3], s[4])]
        q.sort(key=lambda t: s.index(t))                 # re-seed: the 1 seed meets the lowest seed left
        f1, f2 = play(s[0], q[1]), play(s[1], q[0])
        title[play(f1, f2)] += 1
    out = {}
    for t in teams:
        need = {}
        for thr in (0.5, 0.8, 0.95):
            ok = [w for w, (c, m) in sorted(finalW[t].items()) if c >= max(30, n // 2000) and m / c >= thr]
            need[str(thr)] = ok[0] if ok else None
        s = swing[t]
        out[t] = dict(po=po[t] / n, bye=bye[t] / n, title=title[t] / n, wins=wins[t] / n, pts=pts[t] / n,
                      seed=[round(c / n, 4) for c in seed[t]], need=need,
                      ifWin=(s[1] / s[0]) if s[0] else None, ifLose=(s[3] / s[2]) if s[2] else None,
                      byWins={str(w): [c, m] for w, (c, m) in sorted(finalW[t].items())},
                      mu={str(w): round(mu[(t, w)], 2) for w in weeks}, proj={str(w): round(proj[(t, w)], 2) for w in weeks},
                      w=rec[t][0], l=rec[t][1], pf=round(rec[t][2], 2), level=round(lg + F['b2'] * lvl[t], 2))
    games = [dict(wk=g['wk'], ta=g['ta'], tb=g['tb'], muA=round(mu[(g['ta'], g['wk'])], 2), muB=round(mu[(g['tb'], g['wk'])], 2),
                  pA=round(mwin.get((g['ta'], g['tb']), 0) / n, 4) if g['wk'] == nxt else None) for g in left]
    return dict(teams=out, games=games, weeks=weeks, next=nxt, lg=round(lg, 2), fit=F, roster_week=rw, roster=roster, pj=pj)

def build(y=None):
    y = y or TF.LIVE
    st = TF.settings(y)
    played = max([g['wk'] for g in P.games(y) if g['status'] == 'postevent' and g['wk'] < st['po']] or [0])
    if not played: return None
    rnd = random.Random(y)
    now = run(y, played, N, rnd)
    T = now['teams']
    # injuries: his players listed out, doubtful or questionable this week, their projection, and the week they are back
    inj = {}
    for t, rows in now['roster'].items():
        for r in rows:
            if (r.get('status') or '') not in OUT: continue
            back = next((w for w in now['weeks'] if (now['pj'](r['n'], r['pos'], r['nfl'], w) or 0) > 0), None)
            inj.setdefault(t, []).append(dict(n=r['n'], pos=(r['pos'] or '').split(',')[0], status=r['status'], slot=r['slot'],
                                              thisWeek=now['pj'](r['n'], r['pos'], r['nfl'], now['next']) if now['next'] else None, back=back))
    # schedule left: each opponent's expected score, against the league's
    sos = {}
    for t in T:
        opp = [(g['tb'] if g['ta'] == t else g['ta'], g['wk']) for g in now['games'] if t in (g['ta'], g['tb'])]
        sos[t] = round(sum(T[o]['mu'][str(w)] for o, w in opp) / len(opp) - now['lg'], 2) if opp else None
    # the odds as the season stood after each week, each re-run with what was known then
    hist = {}
    for k in range(1, played + 1):
        try:
            r = run(y, k, N_PAST, random.Random(y * 100 + k))
            hist[k] = {t: dict(po=round(v['po'], 4), bye=round(v['bye'], 4), title=round(v['title'], 4)) for t, v in r['teams'].items()}
        except Exception:
            pass
    hist[played] = {t: dict(po=round(v['po'], 4), bye=round(v['bye'], 4), title=round(v['title'], 4)) for t, v in T.items()}
    mgr = {t: TF.mgr_of(y, t) for t in T}
    return dict(year=y, played=played, regWeeks=st['po'] - 1, runs=N, next=now['next'], lg=now['lg'],
                fit={k: (round(v, 4) if isinstance(v, float) else v) for k, v in now['fit'].items()},
                teams=[dict(team=t, mgr=mgr[t], **{k: (round(v, 4) if isinstance(v, float) else v) for k, v in T[t].items()}, sos=sos[t], inj=inj.get(t, []))
                       for t in sorted(T, key=lambda t: -T[t]['po'])],
                games=now['games'], history=hist)

if __name__ == '__main__':
    import time; t0 = time.time(); F = build()
    print('seconds', round(time.time() - t0, 1), 'fit', F['fit'])
    for t in F['teams']:
        print('%-24s %d-%d po %.3f bye %.3f title %.3f wins %.1f need %s ifW %.2f ifL %.2f sos %+.1f inj %d' % (
            t['team'], t['w'], t['l'], t['po'], t['bye'], t['title'], t['wins'], t['need'], t['ifWin'] or 0, t['ifLose'] or 0, t['sos'] or 0, len(t['inj'])))
    print('sum po', round(sum(t['po'] for t in F['teams']), 3), 'games next', [(g['ta'], g['pA']) for g in F['games'] if g['pA'] is not None])
