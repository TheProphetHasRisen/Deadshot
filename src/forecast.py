# -*- coding: utf-8 -*-
"""The forecast (Brian, 16 Oct 2026; PLANS.md section 4): the rest of the live season, played 100,000 times.

Each team's expected score for each week still to play:
    league average  +  b1 x (his projected best lineup that week  -  the league's)  +  b2 x (his scoring so far  -  the league's)
  * his projected lineup is built from the players on his roster now, each with Sleeper's projection for THAT
    week, scored the league's way. A player out injured, suspended, on a bye or not yet back projects 0 for
    the weeks he will miss and his full value from the week he returns, so injuries, returns, suspensions and
    byes all come in through it. IR slots count: a player stashed there is back in the lineup when he is.
  * b1 and b2 are fitted on every Deadshot season Yahoo reaches (2021-2025), each frozen at the same number of
    weeks played with the projections as they stood then (refit(); backtest.py): each later week's score against
    the projected lineup and the form to date. In this league both are weak (week to week, scores are close to a
    coin flip around the average), so the swing around the expected score is the week-to-week spread that is left.
  * USER's pick after the backtest (17 Oct 2026; mixed()): playoff, bye and seed odds blend that model with the
    standings alone, weight (8 - weeks played) / 6 on the model; title odds use the model alone.
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

_FIT = {}
def _season_fit_data(y):
    """for one finished season: every team's score and projected best lineup, every regular-season week"""
    if y not in _FIT:
        st = TF.settings(y); slots = st['slots']; pj = PR.lookup(y)
        R = P.rosters(y); G = [g for g in P.games(y) if g['status'] == 'postevent' and g['wk'] < st['po']]
        sc = {}
        for g in G: sc[(g['ta'], g['wk'])] = g['aa']; sc[(g['tb'], g['wk'])] = g['ab']
        by = {}
        for r in R: by.setdefault((r['team'], r['wk']), []).append(r)
        pl = {(t, w): _lineup(by.get((t, w), []), w, pj, slots) for (t, w) in sc}
        _FIT[y] = (sc, pl)
    return _FIT[y]

def fit(k, exclude=()):
    """b1, b2 and the spread left, from every finished season (but those excluded): k weeks played, every later
    regular-season week"""
    X, Y = [], []
    for y in [y for y in TF.YEARS if y != TF.LIVE and y not in exclude]:
        sc, PL = _season_fit_data(y)
        teams = {t for t, _ in sc}; weeks = sorted({w for _, w in sc})
        if len(weeks) <= k: continue
        lg_k = sum(v for (t, w), v in sc.items() if w <= k) / sum(1 for (t, w) in sc if w <= k)
        lvl = {t: sum(sc[(t, w)] for w in range(1, k + 1) if (t, w) in sc) / k - lg_k for t in teams}
        for w in weeks:
            if w <= k: continue
            pl = {t: PL[(t, w)] for t in teams}
            pm = sum(pl.values()) / len(pl); am = sum(sc[(t, w)] for t in teams) / len(teams)
            for t in teams: X.append((pl[t] - pm, lvl[t])); Y.append(sc[(t, w)] - am)
    return _ols(X, Y)

def _ols(X, Y):
    """least squares of Y on the two predictors (no intercept: both sides are measured against the league that
    week), with standard errors, p-values and R squared for the model page"""
    n = len(X)
    if n < 30: return dict(b1=0.0, b2=0.0, sd=22.0, n=n)   # nothing to learn from at this point of the season
    sxx = sum(a * a for a, _ in X); syy = sum(b * b for _, b in X); sxy = sum(a * b for a, b in X)
    sxr = sum(a * r for (a, _), r in zip(X, Y)); syr = sum(b * r for (_, b), r in zip(X, Y))
    det = sxx * syy - sxy * sxy
    b1 = (sxr * syy - syr * sxy) / det; b2 = (syr * sxx - sxr * sxy) / det
    res = [r - b1 * a - b2 * b for (a, b), r in zip(X, Y)]
    s2 = sum(e * e for e in res) / (n - 2)
    se1, se2 = math.sqrt(s2 * syy / det), math.sqrt(s2 * sxx / det)
    pv = lambda z: 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    tot = sum(r * r for r in Y)
    corr = sxy / math.sqrt(sxx * syy)
    return dict(b1=b1, b2=b2, sd=math.sqrt(sum(e * e for e in res) / n), n=n, se1=se1, se2=se2, p1=pv(b1 / se1), p2=pv(b2 / se2),
                r2=1 - sum(e * e for e in res) / tot, rawsd=math.sqrt(tot / n), corr=corr)

def refit(k):
    """the model as the live site uses it since 17 Oct 2026 (USER's pick after the backtest): fitted on projections
    as they were known at the time (backtest.py), not on each week's own projection, which knew that week's injuries"""
    import backtest as BT
    R = [r for s in TF.YEARS if s != TF.LIVE for r in BT.asof_rows(s, k)]
    return _ols([(a, b) for a, b, _ in R], [r for _, _, r in R])

def blend_weight(k):
    """the weight on the refitted model for playoff, bye and seed odds; the rest is the standings alone (every team
    equal from here). Read off the backtest: the model is better early, the standings from week 6"""
    return min(1.0, max(0.0, (8 - k) / 6))

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

def run(y, k, n, rnd, F=None, pj=None, qp=None):
    st, rec, roster, left, rw = season_state(y, k)
    teams = sorted(rec); slots = st['slots']; pj = pj or PR.lookup(y, live=(y == TF.LIVE))
    F = F or fit(k)
    lg = sum(r[2] for r in rec.values()) / max(1, sum(len(r[3]) for r in rec.values()))
    lvl = {t: rec[t][2] / max(1, len(rec[t][3])) - lg for t in teams}
    weeks = sorted({g['wk'] for g in left})
    proj = {(t, w): _lineup(roster.get(t, []), w, pj, slots) for t in teams for w in weeks}
    pm = {w: sum(proj[(t, w)] for t in teams) / len(teams) for w in weeks}
    mu = {(t, w): lg + F['b1'] * (proj[(t, w)] - pm[w]) + F['b2'] * lvl[t] for t in teams for w in weeks}
    sd = F['sd']
    nxt = weeks[0] if weeks else None
    # questionable and doubtful players the projection still plays this week: each sits in the share of seasons the
    # NFL's injury reports say such a player sits (qrates.py), costing his team what his lineup loses without him
    QL = []
    if qp and nxt:
        for t in teams:
            rows = roster.get(t, [])
            for r in rows:
                p = qp(r)
                if p is None or p >= 1 or not (pj(r['n'], r['pos'], r['nfl'], nxt) or 0) > 0: continue
                loss = _lineup(rows, nxt, pj, slots) - _lineup([x for x in rows if x is not r], nxt, pj, slots)
                if loss > 0.05: QL.append((t, F['b1'] * loss, p))
    po = {t: 0 for t in teams}; bye = dict(po); title = dict(po); wins = {t: 0.0 for t in teams}; pts = dict(wins)
    seed = {t: [0] * len(teams) for t in teams}
    finalW = {t: {} for t in teams}                      # final wins -> [seasons, made playoffs]
    swing = {t: [0, 0, 0, 0] for t in teams}             # won next week: [n, made it]; lost: [n, made it]
    mwin = {}
    nspots = st['nteams']; nbye = 2 if nspots == 6 else 0   # 2021 had four teams in, no byes
    for _ in range(n):
        W = {t: rec[t][0] for t in teams}; PF = {t: rec[t][2] for t in teams}; nx = {}
        adj = {}
        for t, c, p in QL:
            if rnd.random() >= p: adj[t] = adj.get(t, 0.0) - c
        for g in left:
            a, b = g['ta'], g['tb']
            sa = rnd.gauss(mu[(a, g['wk'])], sd); sb = rnd.gauss(mu[(b, g['wk'])], sd)
            if adj and g['wk'] == nxt: sa += adj.get(a, 0.0); sb += adj.get(b, 0.0)
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
        for t in order[:nbye]: bye[t] += 1
        s = order[:nspots]
        play = lambda x, z: x if rnd.gauss(lg + F['b2'] * lvl[x], sd) > rnd.gauss(lg + F['b2'] * lvl[z], sd) else z
        if nspots == 6:
            q = [play(s[2], s[5]), play(s[3], s[4])]
            q.sort(key=lambda t: s.index(t))             # re-seed: the 1 seed meets the lowest seed left
            f1, f2 = play(s[0], q[1]), play(s[1], q[0])
        else:
            f1, f2 = play(s[0], s[3]), play(s[1], s[2])
        title[play(f1, f2)] += 1
    out = {}
    for t in teams:
        need = _need({w: (c / n, m / n) for w, (c, m) in finalW[t].items()}, n)
        s = swing[t]
        out[t] = dict(po=po[t] / n, bye=bye[t] / n, title=title[t] / n, wins=wins[t] / n, pts=pts[t] / n,
                      seed=[round(c / n, 4) for c in seed[t]], need=need,
                      ifWin=(s[1] / s[0]) if s[0] else None, ifLose=(s[3] / s[2]) if s[2] else None, _sw=[c / n for c in s],
                      byWins={str(w): [c, m] for w, (c, m) in sorted(finalW[t].items())}, _fw={w: (c / n, m / n) for w, (c, m) in finalW[t].items()},
                      mu={str(w): round(mu[(t, w)], 2) for w in weeks}, proj={str(w): round(proj[(t, w)], 2) for w in weeks},
                      w=rec[t][0], l=rec[t][1], pf=round(rec[t][2], 2), level=round(lg + F['b2'] * lvl[t], 2), form=round(lvl[t], 3))
    games = [dict(wk=g['wk'], ta=g['ta'], tb=g['tb'], muA=round(mu[(g['ta'], g['wk'])], 2), muB=round(mu[(g['tb'], g['wk'])], 2),
                  pA=round(mwin.get((g['ta'], g['tb']), 0) / n, 6) if g['wk'] == nxt else None) for g in left]
    done = [[g['wk'], g['ta'], g['tb'], g['aa'], g['ab']] for g in P.games(y) if g['status'] == 'postevent' and g['wk'] <= k and g['wk'] < st['po']]
    return dict(teams=out, games=games, weeks=weeks, next=nxt, lg=round(lg, 2), fit=F, roster_week=rw, roster=roster, pj=pj,
                scores={t: [round(v, 2) for v in rec[t][3]] for t in teams}, done=done)

def _need(fw, n):
    """the fewest final wins that get him in at 50%, 80% and 95%: fw {wins: (share of seasons, share made it)}"""
    need = {}
    for thr in (0.5, 0.8, 0.95):
        ok = [w for w, (c, m) in sorted(fw.items()) if c * n >= max(30, n // 2000) and m / c >= thr]
        need[str(thr)] = ok[0] if ok else None
    return need

def mixed(y, k, n, seed, qp=None):
    """the live forecast (USER's pick, 17 Oct 2026): playoff, bye and seed odds from the blend (the refitted model,
    weighted down week by week toward the standings alone); title odds from the refitted model"""
    F = refit(k); wt = blend_weight(k)
    m = run(y, k, n, random.Random(seed), F=F, qp=qp)
    if wt >= 1: r0 = m
    else: r0 = run(y, k, n, random.Random(seed + 7), F=dict(F, b1=0.0, b2=0.0), pj=m['pj'])
    mix = lambda a, b: wt * a + (1 - wt) * b
    for t, v in m['teams'].items():
        z = r0['teams'][t]
        for key in ('po', 'bye', 'wins', 'pts'): v[key] = mix(v[key], z[key])
        v['seed'] = [round(mix(a, b), 4) for a, b in zip(v['seed'], z['seed'])]
        fw = {w: (mix(*(x.get(w, (0, 0))[0] for x in (v['_fw'], z['_fw']))), mix(*(x.get(w, (0, 0))[1] for x in (v['_fw'], z['_fw']))))
              for w in set(v['_fw']) | set(z['_fw'])}
        v['byWins'] = {str(w): [round(c * n), round(mm * n)] for w, (c, mm) in sorted(fw.items()) if c > 0}
        v['need'] = _need(fw, n)
        sw = [mix(a, b) for a, b in zip(v['_sw'], z['_sw'])]
        v['ifWin'] = sw[1] / sw[0] if sw[0] else None; v['ifLose'] = sw[3] / sw[2] if sw[2] else None
        v['title'] = min(v['title'], v['po'])      # the refitted model's title odds, never above his playoff odds
        for key in ('_fw', '_sw'): v.pop(key, None)
    for g, g0 in zip(m['games'], r0['games']):
        if g['pA'] is not None: g['pA'] = round(mix(g['pA'], g0['pA']), 4)
    m['model'] = dict(playoffs='blend', titles='refit', weight=round(wt, 3), week=k)
    return m

def build(y=None):
    y = y or TF.LIVE
    st = TF.settings(y)
    played = max([g['wk'] for g in P.games(y) if g['status'] == 'postevent' and g['wk'] < st['po']] or [0])
    if not played: return None
    # how often a player on the injury report plays (qrates.py): this week's NFL report when it has him, else his
    # Yahoo label; only the week ahead (the past weeks' re-runs have no reports saved)
    try:
        import qrates as QR
        RQ = QR.rates(); cur = QR.current(y, played + 1)
        qp = lambda r: QR.chance(RQ, r.get('status'), r['n'], r['pos'], cur)
    except Exception:
        qp = None
    now = mixed(y, played, N, y, qp=qp)
    T = now['teams']
    # injuries: his players listed out, doubtful or questionable this week, their projection, and the week they are back
    inj = {}; st = TF.settings(y)
    for t, rows in now['roster'].items():
        for r in rows:
            if (r.get('status') or '') not in OUT: continue
            back = next((w for w in now['weeks'] if (now['pj'](r['n'], r['pos'], r['nfl'], w) or 0) > 0), None)
            # what his absence costs: each week he is out, his team's projected best lineup with him (at the
            # projection he carries once back) against without him, added up
            healthy = now['pj'](r['n'], r['pos'], r['nfl'], back) if back else None
            cost = 0.0; costW = {}
            if healthy:
                for w in [w for w in now['weeks'] if w < back]:
                    rows = now['roster'][t]
                    fixed = lambda n, pos, nfl, wk, _n=r['n'], _h=healthy: _h if n == _n else now['pj'](n, pos, nfl, wk)
                    c = _lineup(rows, w, fixed, st['slots']) - _lineup(rows, w, now['pj'], st['slots'])
                    cost += c
                    if c > 0.05: costW[str(w)] = round(c, 2)
            # a player listed questionable or doubtful whom the projection still plays: what his team loses if he sits this week
            sits = None
            if back == now['next'] and now['next'] and (r['status'] in ('Q', 'D') or (qp and (qp(r) or 1) < 1)):
                rows = now['roster'][t]
                sits = round(_lineup(rows, now['next'], now['pj'], st['slots']) - _lineup([x for x in rows if x['n'] != r['n']], now['next'], now['pj'], st['slots']), 2)
            inj.setdefault(t, []).append(dict(n=r['n'], pos=(r['pos'] or '').split(',')[0], status=r['status'], slot=r['slot'],
                                              thisWeek=now['pj'](r['n'], r['pos'], r['nfl'], now['next']) if now['next'] else None, back=back,
                                              cost=round(cost, 1), costW=costW, sits=sits,
                                              plays=(round(qp(r), 3) if qp and qp(r) is not None else None)))
    # what each team needs, by position: his projected starters at each slot over the weeks left, against the
    # league's; the same after the best free agents are counted (a hole waivers can fill is not a need); and his
    # depth, the next man up, over what waivers offer at that position (a backup quarterback is worth little
    # when a free one scores nearly as much: posvalue.py)
    import posvalue as PV
    slots = st['slots']; POS = [p for p in ('QB', 'RB', 'WR', 'TE', 'K', 'DEF') if slots.get(p)]
    allrows = [r for rows in now['roster'].values() for r in rows]
    FAw = PV.free_agents(y, lambda w: allrows, now['weeks'], live=(y == TF.LIVE), top=3)
    FAr = PV.rest_of_season(y, allrows, now['weeks'], live=(y == TF.LIVE))
    repl = {p_: sum(sum(v for v, _, _ in FAw[p_].get(w, [])[:3]) / max(1, len(FAw[p_].get(w, [])[:3])) for w in now['weeks']) / max(1, len(now['weeks'])) for p_ in POS}
    need = {}
    for t, rows in now['roster'].items():
        acc = {p: 0.0 for p in POS + ['FLEX']}; dep = {p: 0.0 for p in POS}; eff = {p: 0.0 for p in POS}; over = {p: 0.0 for p in POS}; n = 0
        weak = {p: 0.0 for p in POS}
        for w in now['weeks']:
            n += 1; left = []
            for p_ in POS:
                xs = sorted([(now['pj'](r['n'], r['pos'], r['nfl'], w) or 0, r['n']) for r in rows if (r['pos'] or '').split(',')[0] == p_], reverse=True)
                k = slots[p_]; acc[p_] += sum(v for v, _ in xs[:k]); dep[p_] += xs[k][0] if len(xs) > k else 0
                weak[p_] += xs[k - 1][0] if len(xs) >= k else 0
                fa = [v for v, _, _ in FAw[p_].get(w, [])[:k]]
                eff[p_] += sum(sorted([v for v, _ in xs] + fa, reverse=True)[:k])
                r_w = sum(fa) / len(fa) if fa else 0
                over[p_] += max(0.0, (xs[k][0] if len(xs) > k else 0) - r_w)
                if p_ in ('RB', 'WR', 'TE'): left += xs[k:]
            if slots.get('W/R/T'): acc['FLEX'] += max([v for v, _ in left] or [0])
        m = max(1, n)
        need[t] = {p_: round(v / m, 2) for p_, v in acc.items()}
        need[t]['_depth'] = {p_: round(v / m, 2) for p_, v in dep.items()}
        need[t]['_over'] = {p_: round(v / m, 2) for p_, v in over.items()}
        need[t]['_eff'] = {p_: round(v / m, 2) for p_, v in eff.items()}
        # the free agent who would help him most: the best one at the position where he beats his weakest starter by most
        fix = [(FAr[p_][0][0] - weak[p_] / m, p_, FAr[p_][0][1]) for p_ in POS if FAr.get(p_)]
        fix = max(fix) if fix else None
        need[t]['_fix'] = [fix[1], fix[2], round(fix[0], 2)] if fix and fix[0] >= 1.0 else None
    lgpos = {p_: sum(v[p_] for v in need.values()) / len(need) for p_ in POS + ['FLEX']}
    lgdep = {p_: sum(v['_depth'][p_] for v in need.values()) / len(need) for p_ in POS}
    # schedule left: each opponent's expected score, against the league's
    sos = {}
    for t in T:
        opp = [(g['tb'] if g['ta'] == t else g['ta'], g['wk']) for g in now['games'] if t in (g['ta'], g['tb'])]
        sos[t] = round(sum(T[o]['mu'][str(w)] for o, w in opp) / len(opp) - now['lg'], 2) if opp else None
    # the odds as the season stood after each week, each re-run with what was known then
    hist = {}
    for k in range(1, played + 1):
        try:
            r = mixed(y, k, N_PAST, y * 100 + k)
            hist[k] = {t: dict(po=round(v['po'], 4), bye=round(v['bye'], 4), title=round(v['title'], 4)) for t, v in r['teams'].items()}
        except Exception:
            pass
    hist[played] = {t: dict(po=round(v['po'], 4), bye=round(v['bye'], 4), title=round(v['title'], 4)) for t, v in T.items()}
    mgr = {t: TF.mgr_of(y, t) for t in T}
    return dict(year=y, played=played, regWeeks=st['po'] - 1, runs=N, next=now['next'], lg=now['lg'], model=now['model'],
                fit={k: (float('%.4g' % v) if isinstance(v, float) else v) for k, v in now['fit'].items()},
                teams=[dict(team=t, mgr=mgr[t], **{k: (round(v, 4) if isinstance(v, float) else v) for k, v in T[t].items()}, sos=sos[t], inj=inj.get(t, []))
                       for t in sorted(T, key=lambda t: -T[t]['po'])],
                games=now['games'], history=hist, scores=now['scores'], done=now['done'],
                fitOld={k: (float('%.4g' % v) if isinstance(v, float) else v) for k, v in fit(played).items()},
                needs=dict(pos=POS + (['FLEX'] if slots.get('W/R/T') else []), league={k: round(v, 2) for k, v in lgpos.items()},
                           leagueDepth={k: round(v, 2) for k, v in lgdep.items()}, teams=need, repl={k: round(v, 2) for k, v in repl.items()},
                           fa={p_: FAr.get(p_, [])[:3] for p_ in POS}, slots={p_: slots.get(p_) for p_ in POS}))

if __name__ == '__main__':
    import time; t0 = time.time(); F = build()
    print('seconds', round(time.time() - t0, 1), 'fit', F['fit'])
    for t in F['teams']:
        print('%-24s %d-%d po %.3f bye %.3f title %.3f wins %.1f need %s ifW %.2f ifL %.2f sos %+.1f inj %d' % (
            t['team'], t['w'], t['l'], t['po'], t['bye'], t['title'], t['wins'], t['need'], t['ifWin'] or 0, t['ifLose'] or 0, t['sos'] or 0, len(t['inj'])))
    print('sum po', round(sum(t['po'] for t in F['teams']), 3), 'games next', [(g['ta'], g['pA']) for g in F['games'] if g['pA'] is not None])
