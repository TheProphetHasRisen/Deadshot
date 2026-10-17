# -*- coding: utf-8 -*-
"""The GM report card (USER, 17 Oct 2026: the net points rework). Every decision a manager made, graded against
the alternative he really had at that moment, in points, regular season, 2021 on:

  draft     each pick (kickers and defenses aside) against the next five players taken: his season over the
            free-agent level at his position (posvalue.py), minus theirs on average. He could have had any of them.
  waivers   each pickup against the best-projected free agent at the same position that week (the one he left
            there), over the weeks he kept him: the points each actually scored.
  drops     each cut against keeping him: the free-agent level at his position minus what the dropped player
            scored, every week left in the regular season. Cutting a player who then flopped scores plus.
  trades    each side's value at position against the other side's (teamfile.py, as the trade cards grade them).
  lineups   his starters' points against the lineup the projections would have set from the same roster that
            week (Sleeper's projection, made before the games): start/sit with only what was known then.

Each part is turned into a percentile against every manager-season since 2021 (points a week, so a season in
progress compares fairly), and the grade is the average of the five: each skill counts the same.

    build() -> {years, seasons: {y: {mgr: {part: points, ...}}}, pct: {...}, overall: {...}}
"""
import teamfile as TF, yahoo_parse as P, projections as PR, injuries as I
import posvalue as PV

PARTS = ('draft', 'waivers', 'drops', 'trades', 'lineups')
KD = ('K', 'DEF')

def _weekly(y, weeks):
    """f(name, pos, nfl) -> [points by week 1..18], every NFL player, from Sleeper"""
    A = PV._actual(y, weeks); ids = I._ids()
    def f(name, pos, nfl):
        p0 = (pos or '').split(',')[0]
        if p0 == 'DEF': return A.get(I.TEAMFIX.get(nfl, nfl)) or [None] * 18
        for c in I.cands(ids, name, pos):
            if c in A: return A[c]
        return [None] * 18
    return f

def _proj_lineup(rows, wk, pj, slots):
    """the lineup the projections would have set: dedicated slots by projection, then the flex; returns its real points"""
    pool = sorted(rows, key=lambda r: -(pj(r['n'], r['pos'], r['nfl'], wk) or 0))
    used, pts = set(), 0.0
    order = [s for s in ('QB', 'RB', 'WR', 'TE', 'K', 'DEF') if slots.get(s)] + (['W/R/T'] if slots.get('W/R/T') else [])
    for s in order:
        for _ in range(slots[s]):
            c = next((r for r in pool if id(r) not in used and TF.eligible(r['pos'], s)), None)
            if c: used.add(id(c)); pts += c['pts'] or 0
    return pts

def season(y):
    st = TF.settings(y); slots = st['slots']; live = y == TF.LIVE
    M, L = TF.season(y)
    weeks = sorted({x['wk'] for Z in M.values() for x in Z['weekly']})
    if not weeks: return {}
    pts = _weekly(y, weeks)
    pv = PV.season(y)['pos']
    fa_lvl = {p: v['fa'] for p, v in pv.items()}
    R = P.rosters(y); by = {}
    for r in R: by.setdefault(r['wk'], []).append(r)
    FA = PV.free_agents(y, lambda w: by.get(w, []), weeks, live=live, top=2)
    pj = PR.lookup(y, live=live)
    nw = len(weeks)
    out = {m: dict(team=Z['team'], g=Z['g'], **{k: 0.0 for k in PARTS}, n={k: 0 for k in PARTS}) for m, Z in M.items()}
    seas = lambda n, pos, nfl: sum(v or 0 for i, v in enumerate(pts(n, pos, nfl)) if i + 1 in weeks)
    # the draft: each pick against the next five taken (kickers and defenses aside)
    D = sorted([d for d in L['draft_list'] if d['pos'] not in KD], key=lambda d: d['pick'])
    nfl = {r['n']: r['nfl'] for r in R}
    val = lambda d: seas(d['n'], d['pos'], nfl.get(d['n'])) - fa_lvl.get(d['pos'], 0) * nw
    V = [val(d) for d in D]
    for i, d in enumerate(D):
        alt = V[i + 1:i + 6]
        if d['m'] in out and alt:
            out[d['m']]['draft'] += V[i] - sum(alt) / len(alt); out[d['m']]['n']['draft'] += 1
    # pickups: against the best-projected free agent at his position that week, over the weeks he kept him
    for p in L['picks_list']:
        m = p['m']
        if m not in out or p['wk'] not in weeks: continue
        p0 = (p['pos'] or '').split(',')[0]
        alts = [x for x in FA.get(p0, {}).get(p['wk'], []) if I.norm(x[1]) != I.norm(p['n'])]
        if not alts: continue
        run = [w for w in range(p['wk'], p['wk'] + max(1, p['held'])) if w in weeks]
        mine = pts(p['n'], p['pos'], nfl.get(p['n'])); A = PV._actual(y, weeks).get(alts[0][2]) or [None] * 18
        out[m]['waivers'] += sum((mine[w - 1] or 0) - (A[w - 1] or 0) for w in run); out[m]['n']['waivers'] += 1
    # drops: keeping him against the free-agent level, every week left
    for g in L['gone_list']:
        m = g['m']; p0 = (g['pos'] or '').split(',')[0]
        if m not in out or g['wk'] not in weeks or p0 not in fa_lvl: continue
        line = pts(g['n'], g['pos'], nfl.get(g['n']))
        after = [w for w in weeks if w >= g['wk']]
        out[m]['drops'] += sum(fa_lvl[p0] - (line[w - 1] or 0) for w in after if line[w - 1] is not None); out[m]['n']['drops'] += 1
    # trades: value at position, as the trade cards grade them
    for m, Z in M.items():
        out[m]['trades'] = Z['trade_net']; out[m]['n']['trades'] = Z['trades']
    # lineups: his starters against the projections' lineup from the same roster
    team_m = {Z['team']: m for m, Z in M.items()}
    for w in weeks:
        rows = {}
        for r in by.get(w, []): rows.setdefault(r['team'], []).append(r)
        for t, rs in rows.items():
            m = team_m.get(t)
            if m not in out: continue
            act = sum(r['pts'] or 0 for r in rs if r['started'])
            out[m]['lineups'] += act - _proj_lineup([r for r in rs if r['slot'] != 'IR'], w, pj, slots); out[m]['n']['lineups'] += 1
    for v in out.values():
        for k in PARTS: v[k] = round(v[k], 2)
    return out

HIST = 'report_hist.json'

def build():
    import json, os
    h = json.load(open(HIST)) if os.path.exists(HIST) else {}
    S = {}
    for y in TF.YEARS:
        if y != TF.LIVE and str(y) in h: S[y] = h[str(y)]; continue    # finished seasons are frozen (and need full Sleeper tables)
        try: S[y] = season(y)
        except Exception as e:
            import sys; print('  (report card %d left out: %s)' % (y, str(e)[:100]), file=sys.stderr)
    fin = {str(y): {m: {k: v for k, v in r.items() if k not in ('pct', 'grade')} for m, r in s.items()} for y, s in S.items() if y != TF.LIVE}
    if fin and fin != h: json.dump(fin, open(HIST, 'w'), indent=0, sort_keys=True)
    # percentiles against every finished manager-season, points a week
    pool = {k: sorted(v[k] / max(1, v['g']) for y, s in S.items() if y != TF.LIVE for v in s.values()) for k in PARTS}
    def pct(k, x):
        P_ = pool[k]
        if not P_: return None
        below = sum(1 for v in P_ if v < x - 1e-9); same = sum(1 for v in P_ if abs(v - x) <= 1e-9)
        return round(100 * (below + same / 2) / len(P_))
    for y, s in S.items():
        for v in s.values():
            v['pct'] = {k: pct(k, v[k] / max(1, v['g'])) for k in PARTS}
            ps = [x for x in v['pct'].values() if x is not None]
            v['grade'] = round(sum(ps) / len(ps)) if ps else None
    return dict(years=sorted(S), seasons={str(y): s for y, s in S.items()}, parts=list(PARTS), pool=len(pool['draft']))

if __name__ == '__main__':
    import time; t0 = time.time(); B = build(); print('seconds', round(time.time() - t0, 1), 'pool', B['pool'])
    for y in B['years']:
        s = B['seasons'][str(y)]
        for m, v in sorted(s.items(), key=lambda x: -(x[1]['grade'] or 0)):
            print(y, m[:16].ljust(16), 'grade', v['grade'], ' '.join('%s %+.0f(%s)' % (k[:4], v[k], v['pct'][k]) for k in PARTS))
