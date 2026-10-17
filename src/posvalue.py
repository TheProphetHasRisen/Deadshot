# -*- coding: utf-8 -*-
"""What a point is worth at each position (USER, 17 Oct 2026), season by season.

On the scoreboard a point is a point wherever it comes from. What differs by position is how many of a
starter's points you could have had for nothing: a free agent at quarterback scores a lot, a free agent at
running back very little. So, every regular-season week, at each position:

  starter       the average points of the league's starters in that slot (Yahoo's official points)
  free agent    what the three best-projected players nobody in Deadshot rostered that week actually scored,
                on average (chosen by Sleeper's projection made before the games, so no hindsight)
  over          starter minus free agent: what a starter there is really worth
  worth         over / starter: of every point a starter there scores, the part a free agent would not give
                you ("cents on the point")
  share         of all the points the league's starters scored over a free agent that season, the part that
                came from this position (flex starters counted at their own position)

    season(y) -> {pos: {...}, weeks: n}
    build()   -> {years: [...], seasons: {y: season(y)}, pos: [...]}
    free_agents(y, rows, weeks) -> {pos: {week: [(projection, name), ...best first]}} for the live needs table

Finished seasons are kept in posvalue_hist.json (committed), so the scheduled job only works out the live one.
"""
import json, os
import yahoo_parse as P
import teamfile as TF
import projections as PR
import injuries as I
import sleeper_season as SL

POS = ('QB', 'RB', 'WR', 'TE', 'K', 'DEF')
HIST = 'posvalue_hist.json'
NFA = 3

def _pos_of():
    pl = SL._players()
    return lambda pid: 'DEF' if pid.isalpha() else (pl.get(pid) or [None, None])[1]

def _name_of():
    pl = SL._players()
    return lambda pid: pid if pid.isalpha() else (pl.get(pid) or [pid])[0]

def _rostered(rows, ids):
    out = set()
    for r in rows:
        p0 = (r['pos'] or '').split(',')[0]
        if p0 == 'DEF': out.add(I.TEAMFIX.get(r['nfl'], r['nfl']))
        else: out.update(I.cands(ids, r['n'], r['pos']))
    return out

def _actual(y, weeks):
    """{sleeper id: [points by week]} for every NFL player, the league's scoring"""
    if y != TF.LIVE:
        SL.weekly(y)
        return json.load(open('yahoo_raw/sleeper_pts_%d.json' % y))
    from scoring import score
    pos_of = _pos_of(); out = {}
    for w in weeks:
        f = 'yahoo_raw/sleeper_ptsw_%d_%d.json' % (y, w)
        if os.path.exists(f): st = json.load(open(f))
        else:
            st = I._get('https://api.sleeper.app/v1/stats/nfl/regular/%d/%d' % (y, w))
            st = {k: v for k, v in st.items() if pos_of(k) in POS}
            json.dump(st, open(f, 'w'))
        for pid, s in st.items():
            pos = pos_of(pid)
            if pos not in POS or (pos != 'DEF' and not (s.get('gp') or 0)): continue
            out.setdefault(pid, [None] * 18)[w - 1] = round(score(s, pos), 2)
    return out

def free_agents(y, rows_by_week, weeks, live=False, top=5):
    """the best-projected free agents at each position, each week: rows_by_week {week: the rostered rows}"""
    T = PR.table(y, live=live, full=True); ids = I._ids(); pos_of = _pos_of(); name_of = _name_of()
    out = {p: {} for p in POS}
    for w in weeks:
        taken = _rostered(rows_by_week(w), ids)
        for p in POS:
            fa = sorted(((line[w - 1], pid) for pid, line in T.items()
                         if pos_of(pid) == p and pid not in taken and line and len(line) >= w and line[w - 1]), reverse=True)[:top]
            out[p][w] = [(round(v, 2), name_of(pid), pid) for v, pid in fa]
    return out

def rest_of_season(y, rows, weeks, live=False, top=NFA):
    """for the live needs table: with this roster taken, each position's free agents by projected points a week
    over the weeks left (byes count as 0), best first: [(average, name), ...]"""
    T = PR.table(y, live=live, full=True); ids = I._ids(); pos_of = _pos_of(); name_of = _name_of()
    taken = _rostered(rows, ids); out = {}
    for p in POS:
        xs = []
        for pid, line in T.items():
            if pos_of(pid) != p or pid in taken or not line: continue
            v = [(line[w - 1] or 0) if len(line) >= w else 0 for w in weeks]
            if any(v): xs.append((sum(v) / len(v), name_of(pid)))
        out[p] = [(round(a, 2), n) for a, n in sorted(xs, reverse=True)[:top]]
    return out

def season(y):
    st = TF.settings(y); live = y == TF.LIVE
    played = sorted({g['wk'] for g in P.games(y) if g['status'] == 'postevent' and g['wk'] < st['po']})
    R = [r for r in P.rosters(y) if r['wk'] in played]
    by = {}
    for r in R: by.setdefault(r['wk'], []).append(r)
    FA = free_agents(y, lambda w: by.get(w, []), played, live=live, top=NFA)
    A = _actual(y, played)
    acc = {p: dict(st=0.0, stN=0, fa=0.0, faN=0, over=0.0) for p in POS}
    for w in played:
        rows = by.get(w, [])
        fa = {}
        for p in POS:
            xs = [(A.get(pid) or [None] * 18)[w - 1] or 0 for _, _, pid in FA[p].get(w, [])]
            if not xs: continue
            fa[p] = sum(xs) / len(xs); acc[p]['fa'] += fa[p]; acc[p]['faN'] += 1
        for r in rows:
            if not r['started'] or r['pts'] is None: continue
            p0 = (r['pos'] or '').split(',')[0]
            if p0 not in POS: continue
            if r['slot'] == p0: acc[p0]['st'] += r['pts']; acc[p0]['stN'] += 1
            if p0 in fa: acc[p0]['over'] += r['pts'] - fa[p0]
    tot = sum(max(0.0, a['over']) for a in acc.values()) or 1.0
    out = {}
    for p, a in acc.items():
        if not a['stN'] or not a['faN']: continue
        s, f = a['st'] / a['stN'], a['fa'] / a['faN']
        out[p] = dict(starter=round(s, 2), fa=round(f, 2), over=round(s - f, 2), worth=round((s - f) / s, 3) if s > 0 else None,
                      share=round(max(0.0, a['over']) / tot, 3))
    return dict(pos=out, weeks=len(played), live=live)

def build():
    h = json.load(open(HIST)) if os.path.exists(HIST) else {}
    S = {}
    for y in TF.YEARS:
        if y != TF.LIVE and str(y) in h: S[y] = h[str(y)]; continue
        try: S[y] = season(y)
        except Exception as e:
            import sys; print('  (positional value %d left out: %s)' % (y, str(e)[:100]), file=sys.stderr)
    fin = {str(y): v for y, v in S.items() if y != TF.LIVE}
    if fin and fin != h: json.dump(fin, open(HIST, 'w'), indent=1)
    return dict(years=sorted(S), seasons={str(y): v for y, v in S.items()}, pos=list(POS), nfa=NFA)

if __name__ == '__main__':
    B = build()
    for y in B['years']:
        s = B['seasons'][str(y)]
        print(y, s['weeks'], '  '.join('%s %.1f/%.1f w%.2f s%.2f' % (p, v['starter'], v['fa'], v['worth'] or 0, v['share']) for p, v in s['pos'].items()))
