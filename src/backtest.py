# -*- coding: utf-8 -*-
"""The forecast, run on every finished season as it stood after each week, and scored against what happened.

For each season 2021-2025 and each week k played (1 to the last regular-season week but one):
  * the model is fitted on the OTHER seasons only (leave one season out), so it never sees the season it predicts
  * future weeks use the projections known at the time: each player's projection for the next week, carried
    forward, and 0 in his team's bye week (byes are known in advance); never a later week's projection, which
    would know injuries that had not happened yet
  * rosters are as they stood the next week; the schedule left is the real one
Scored with the Brier score: the average of (predicted chance - what happened)^2 over every team, where what
happened is 1 or 0. Lower is better; always saying 60% scores 0.24 in a six-of-ten league. Three rivals:
  coin     every team the same chance (spots / teams)
  record   the simulation with every team equal (no projections, no form): the standings alone
  model    the forecast as built
Also: calibration (of the teams given 70-80%, how many made it), by week, and title odds.
Writes backtest.json for the model page.
"""
import json, random
import forecast as FC, teamfile as TF, yahoo_parse as P, projections as PR, injuries as I

N = 5000

def asof_projection(y, k):
    """projections as known after week k: next week's for every later week, 0 on his team's bye"""
    base = PR.lookup(y)
    pt, played_teams = I.teams(y)
    ids = I._ids()
    def bye(name, pos, nfl, w):
        if (pos or '').split(',')[0] == 'DEF': return I.TEAMFIX.get(nfl, nfl) not in played_teams.get(w, ())
        for c in I.cands(ids, name, pos):
            if c in pt:
                t = I.season_team(pt, c, k + 1)
                return bool(t) and t not in played_teams.get(w, ())
        return False
    def f(name, pos, nfl, w):
        if bye(name, pos, nfl, w): return 0
        return base(name, pos, nfl, k + 1)
    return f

def actual(y):
    st = TF.settings(y)
    rows = [r for r in P.rosters(y)][:0]
    M, L = TF.season(y)
    import data as D
    order = [t for t in sorted(M, key=lambda m: 0)]
    seeds = {}
    for r in D.STANDINGS[y]:
        seeds[r[1]] = r[0]
    champ = D.FINAL_PLACE[y][0] if y in D.FINAL_PLACE else None
    co = getattr(D, 'CO_CHAMPS', {}).get(y, [])
    return seeds, champ, co, st['nteams']

def main():
    out = dict(seasons={}, weeks={}, cal={}, brier={}, n=0)
    rows = []
    for y in [y for y in TF.YEARS if y != TF.LIVE]:
        st = TF.settings(y); last = st['po'] - 1
        seeds, champ, co, spots = actual(y)
        for k in range(1, min(last, 14)):   # every season but 2021 had 14 regular weeks: 13 snapshots each
            F = FC.fit(k, exclude=(y,))
            Fzero = dict(F, b1=0.0, b2=0.0)
            pj = asof_projection(y, k)
            m = FC.run(y, k, N, random.Random(y * 1000 + k), F=F, pj=pj)['teams']
            r0 = FC.run(y, k, N, random.Random(y * 1000 + k), F=Fzero, pj=pj)['teams']
            for t, v in m.items():
                book = next((b for b in seeds if TF._plain(b) == TF._plain(t)), t)
                made = 1 if seeds.get(book, 99) <= spots else 0
                won = 1 if (book == champ or book in co) else 0
                rows.append(dict(y=y, k=k, team=book, made=made, won=won, model=v['po'], record=r0[t]['po'], coin=spots / len(m),
                                 tModel=v['title'], tRecord=r0[t]['title'], tCoin=1 / len(m)))
            print(y, k, 'done', flush=True)
    br = lambda key, outc: sum((r[key] - r[outc]) ** 2 for r in rows) / len(rows)
    out['brier'] = {m: round(br(m, 'made'), 4) for m in ('model', 'record', 'coin')}
    out['brierTitle'] = {m: round(br(t, 'won'), 4) for m, t in (('model', 'tModel'), ('record', 'tRecord'), ('coin', 'tCoin'))}
    for k in sorted({r['k'] for r in rows}):
        rk = [r for r in rows if r['k'] == k]
        out['weeks'][k] = {m: round(sum((r[m] - r['made']) ** 2 for r in rk) / len(rk), 4) for m in ('model', 'record', 'coin')}
    for lo in range(0, 100, 10):
        b = [r for r in rows if lo <= r['model'] * 100 < lo + 10 or (lo == 90 and r['model'] == 1)]
        if b: out['cal'][lo] = dict(n=len(b), said=round(sum(r['model'] for r in b) / len(b), 4), made=round(sum(r['made'] for r in b) / len(b), 4))
    for y in sorted({r['y'] for r in rows}):
        ry = [r for r in rows if r['y'] == y]
        out['seasons'][y] = {m: round(sum((r[m] - r['made']) ** 2 for r in ry) / len(ry), 4) for m in ('model', 'record', 'coin')}
    out['n'] = len(rows); out['runs'] = N
    out['rows'] = [dict(r, model=round(r['model'], 4), record=round(r['record'], 4), tModel=round(r['tModel'], 4), tRecord=round(r['tRecord'], 4)) for r in rows]
    json.dump(out, open('backtest.json', 'w'), separators=(',', ':'))
    print(json.dumps({k: out[k] for k in ('brier', 'brierTitle', 'seasons', 'cal', 'n')}, indent=1))

if __name__ == '__main__':
    main()

# ---- the fix under test: fit b1 and b2 the way the forecast uses them, on projections as known after week k
_ASOF = {}
def asof_rows(s, k):
    """for season s at week k: (projected lineup vs league, form, later score vs league) for every later week,
    the lineup built from the roster the next week with projections as known then"""
    if (s, k) in _ASOF: return _ASOF[(s, k)]
    st, rec, roster, left, rw = FC.season_state(s, k)
    sc, _ = FC._season_fit_data(s)
    teams = sorted(rec); slots = st['slots']; pj = asof_projection(s, k)
    lg = sum(r[2] for r in rec.values()) / max(1, sum(len(r[3]) for r in rec.values()))
    lvl = {t: rec[t][2] / max(1, len(rec[t][3])) - lg for t in teams}
    out = []
    for w in sorted({w for (_, w) in sc if w > k}):
        pl = {t: FC._lineup(roster.get(t, []), w, pj, slots) for t in teams}
        pm = sum(pl.values()) / len(pl); am = sum(sc[(t, w)] for t in teams if (t, w) in sc) / len(teams)
        for t in teams:
            if (t, w) in sc: out.append((pl[t] - pm, lvl[t], sc[(t, w)] - am))
    _ASOF[(s, k)] = out
    return out

def fit_asof(k, exclude):
    import math
    X = [r for s in TF.YEARS if s != TF.LIVE and s not in exclude for r in asof_rows(s, k)]
    n = len(X)
    if n < 30: return dict(b1=0.0, b2=0.0, sd=22.0, n=n)
    sxx = sum(a * a for a, _, _ in X); syy = sum(b * b for _, b, _ in X); sxy = sum(a * b for a, b, _ in X)
    sxr = sum(a * r for a, _, r in X); syr = sum(b * r for _, b, r in X); det = sxx * syy - sxy * sxy
    b1 = (sxr * syy - syr * sxy) / det; b2 = (syr * sxx - sxr * sxy) / det
    res = [r - b1 * a - b2 * b for a, b, r in X]
    return dict(b1=b1, b2=b2, sd=math.sqrt(sum(e * e for e in res) / n), n=n)

def variant():
    rows = []
    for y in [y for y in TF.YEARS if y != TF.LIVE]:
        st = TF.settings(y); last = st['po'] - 1
        seeds, champ, co, spots = actual(y)
        for k in range(1, min(last, 14)):
            F = fit_asof(k, (y,)); pj = asof_projection(y, k)
            m = FC.run(y, k, N, random.Random(y * 1000 + k), F=F, pj=pj)['teams']
            for t, v in m.items():
                book = next((b for b in seeds if TF._plain(b) == TF._plain(t)), t)
                rows.append(dict(y=y, k=k, made=1 if seeds.get(book, 99) <= spots else 0, won=1 if (book == champ or book in co) else 0,
                                 fixed=v['po'], tFixed=v['title'], b1=F['b1'], b2=F['b2']))
            print(y, k, 'fixed', round(F['b1'], 3), round(F['b2'], 3), flush=True)
    d = json.load(open('backtest.json'))
    assert len(rows) == len(d['rows'])
    for r, o in zip(rows, d['rows']): o['fixed'] = round(r['fixed'], 4); o['tFixed'] = round(r['tFixed'], 4)
    R = d['rows']
    d['brier']['fixed'] = round(sum((r['fixed'] - r['made']) ** 2 for r in R) / len(R), 4)
    d['brierTitle']['fixed'] = round(sum((r['tFixed'] - r['won']) ** 2 for r in R) / len(R), 4)
    for k in d['weeks']:
        rk = [r for r in R if str(r['k']) == str(k)]; d['weeks'][k]['fixed'] = round(sum((r['fixed'] - r['made']) ** 2 for r in rk) / len(rk), 4)
    for y in d['seasons']:
        ry = [r for r in R if str(r['y']) == str(y)]; d['seasons'][y]['fixed'] = round(sum((r['fixed'] - r['made']) ** 2 for r in ry) / len(ry), 4)
    d['calFixed'] = {}
    for lo in range(0, 100, 10):
        b = [r for r in R if lo <= r['fixed'] * 100 < lo + 10 or (lo == 90 and r['fixed'] == 1)]
        if b: d['calFixed'][lo] = dict(n=len(b), said=round(sum(r['fixed'] for r in b) / len(b), 4), made=round(sum(r['made'] for r in b) / len(b), 4))
    d['fitFixed'] = {k: dict(zip(('b1', 'b2', 'sd'), (round(v, 3) for v in (fit_asof(k, ())['b1'], fit_asof(k, ())['b2'], fit_asof(k, ())['sd'])))) for k in range(1, 14)}
    json.dump(d, open('backtest.json', 'w'), separators=(',', ':'))
    print(json.dumps(dict(brier=d['brier'], brierTitle=d['brierTitle'], calFixed=d['calFixed'], fitFixed=d['fitFixed']), indent=1))
