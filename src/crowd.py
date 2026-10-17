# -*- coding: utf-8 -*-
"""Against the crowd: every Deadshot lineup and pickup graded against what all of Yahoo was doing.

Yahoo publishes, for every player and every week, the share of all Yahoo leagues that had him rostered
(% rostered) and the share that started him (% started). It keeps the history, so this reaches every
season Yahoo reaches (2021 on), not only the weeks since it was first read (Brian, 16 Oct 2026).

    fetch(y)  -> {week: {player_key: (rostered %, started %)}}, cached in yahoo_raw/<y>/pct_w<week>.json
    build()   -> D.crowd, for the record book's "Against the crowd" section

What it measures, regular season only, like everything else on the site:
  calls      a starter you played over a benched player at the same slot whom the crowd started at least
             20 points more often. Won if your starter outscored him; net is the points the call made.
  gutsy      a starter fewer than 40% of Yahoo teams started. Hit if he beat the median score of every
             starter at his position in this league that week; net is his points over that median, misses included.
  gems       a benched player at least 70% of Yahoo started, and started more widely than the starter he could
             have replaced, who outscored that starter.
  sleepers   a pickup who was on fewer than 25% of Yahoo rosters the week before he was added (the week of the add
             already counts everyone grabbing him), and started at least twice for the team that added him.
  spot       a spot start (Brian's): a starter fewer than 50% of Yahoo started who scored at least twice his own
             points a game up to that week (two or more games played before it).
  chalk      the average % started of a manager's starters: how closely his lineups follow the crowd.
"""
import json, os
import yahoo_parse as P
import teamfile as TF

CALL_GAP, GUTSY, GEM, SLEEPER, SPOT = 20, 40, 70, 25, 50
# finished seasons never change, so their % rostered and % started live in the repo (crowd_hist.json, ~1 MB):
# the scheduled job then reads Yahoo only for the live season. Fetching every season on a fresh machine (about
# 1,400 calls, after the ~1,200 of the season pull) was cut off and the section silently left the site (16 Oct 2026).
HIST = 'crowd_hist.json'
_hist = None
def hist():
    global _hist
    if _hist is None:
        _hist = {int(y): {int(w): {k: tuple(v) for k, v in d.items()} for w, d in ws.items()}
                 for y, ws in (json.load(open(HIST)).items() if os.path.exists(HIST) else [])}
    return _hist

def save_hist():
    """write crowd_hist.json from the cached weekly files of every finished season"""
    out = {}
    for y in TF.YEARS:
        if y == TF.LIVE: continue
        fs = sorted(f for f in os.listdir('yahoo_raw/%d' % y) if f.startswith('pct_w'))
        if fs: out[str(y)] = {f[5:-5]: json.load(open('yahoo_raw/%d/%s' % (y, f))) for f in fs}
    json.dump(out, open(HIST, 'w'), separators=(',', ':'))
    return {y: len(v) for y, v in out.items()}

def _get(path):
    import yahoo_api as Y
    return Y.get(path)

def _pull(K, keys, what, wk):
    out = {}
    for i in range(0, len(keys), 25):
        r = _get('league/%s/players;player_keys=%s/%s;type=week;week=%d' % (K, ','.join(keys[i:i + 25]), what, wk))
        pl = r['fantasy_content']['league'][1]['players']
        for k, v in pl.items():
            if k == 'count': continue
            p = v['player']; key = P.flat(p[0])['player_key']
            for part in p[1:]:
                if isinstance(part, dict) and what in part:
                    x = P.flat(part[what]) if isinstance(part[what], list) else part[what]
                    out[key] = x.get('value')
    return out

def fetch(y, refresh_from=None):
    if y != TF.LIVE and y in hist(): return hist()[y]
    try:
        return _fetch(y, refresh_from)
    except Exception as e:   # Yahoo unreachable or throttling: what was read before still counts
        import sys; print('  (crowd: Yahoo read for %d failed, using the weeks already saved: %s)' % (y, str(e)[:100]), file=sys.stderr)
        out = {}
        for f in os.listdir('yahoo_raw/%d' % y):
            if f.startswith('pct_w'): out[int(f[5:-5])] = {k: tuple(v) for k, v in json.load(open('yahoo_raw/%d/%s' % (y, f))).items()}
        return out

def _fetch(y, refresh_from=None):
    """% rostered and % started for every player on a Deadshot roster each regular-season week, and for
    every player added in the four weeks before (so a pickup's rise is visible after he is cut).
    Finished weeks are cached; refresh_from re-reads that week and later (the live season's current week)."""
    K = json.load(open('yahoo_raw/league_keys.json'))[str(y)]
    st = TF.settings(y); R = P.rosters(y)
    played = sorted({g['wk'] for g in P.games(y) if g['wk'] < st['po'] and g['status'] == 'postevent'})
    if y == TF.LIVE and played and played[-1] + 1 < st['po']:   # and the week being set now: its lineups are the calls being made
        played.append(played[-1] + 1)
    adds = {}
    locks = TF.week_dates(y)
    for t in P.transactions(y):
        if t['status'] != 'successful': continue
        w = TF.week_of(locks, t['ts'])
        for p in t['players']:
            if p['move'] == 'add' and p.get('key'): adds.setdefault(w, set()).add(p['key'])
    out = {}
    for w in played:
        f = 'yahoo_raw/%d/pct_w%d.json' % (y, w)
        if os.path.exists(f) and not (refresh_from and w >= refresh_from):
            out[w] = {k: tuple(v) for k, v in json.load(open(f)).items()}; continue
        keys = sorted({r['key'] for r in R if r['wk'] == w} | set().union(*[adds.get(x, set()) for x in range(w - 4, w + 1)]))
        own, sta = _pull(K, keys, 'percent_owned', w), _pull(K, keys, 'percent_started', w)
        out[w] = {k: (own.get(k), sta.get(k)) for k in keys}
        json.dump(out[w], open(f, 'w'))
    # a pickup's ownership the week BEFORE he was added: the week of the add already counts everyone else
    # grabbing him at the same time
    for w in played:
        extra = sorted(adds.get(w + 1, set()) - set(out[w]))
        if not extra: continue
        own, sta = _pull(K, extra, 'percent_owned', w), _pull(K, extra, 'percent_started', w)
        out[w].update({k: (own.get(k), sta.get(k)) for k in extra})
        json.dump(out[w], open('yahoo_raw/%d/pct_w%d.json' % (y, w), 'w'))
    return out

def season(y, PCT):
    st = TF.settings(y); R = P.rosters(y); slots = st['slots']
    weeks = sorted({g['wk'] for g in P.games(y) if g['wk'] < st['po'] and g['status'] == 'postevent'})
    by = {}
    for r in R:
        if r['wk'] in weeks: by.setdefault((r['team'], r['wk']), []).append(r)
    S = lambda r: (PCT.get(r['wk'], {}).get(r['key']) or (None, None))[1]
    O = lambda k, w: (PCT.get(w, {}).get(k) or (None, None))[0]
    # each position's starter line: the median score of every starter at that position in the league that week
    line = {}
    for w in weeks:
        for pos in ('QB', 'RB', 'WR', 'TE', 'K', 'DEF'):
            xs = sorted(r['pts'] or 0 for (t, ww), rs in by.items() if ww == w for r in rs if r['started'] and (r['pos'] or '').split(',')[0] == pos)
            if xs: line[(w, pos)] = xs[len(xs) // 2] if len(xs) % 2 else (xs[len(xs) // 2 - 1] + xs[len(xs) // 2]) / 2
    # every player's own scoring week by week (Sleeper, the league's rules), for spot starts
    if y == TF.LIVE:
        dp = json.load(open('draft_points.json')) if os.path.exists('draft_points.json') else {}
        wkl = dp.get('wk%d' % y) or {}
        line_of = lambda r: wkl.get(r['n'])
    else:
        import sleeper_season as SL
        bk, _, _ = SL.weekly(y)
        line_of = lambda r: SL.lookup(bk, r['n'], r['pos'], r['nfl'])[1]
    def before(r):
        ln = line_of(r)
        if not ln: return None
        xs = [v for v in ln[:r['wk'] - 1] if v is not None]
        return sum(xs) / len(xs) if len(xs) >= 2 else None
    M = {}; calls, gutsy, gems, spots = [], [], [], []
    for (team, w), rs in by.items():
        m = TF.mgr_of(y, team)
        if not m: continue
        Z = M.setdefault(m, dict(starts=0, chalk=0.0, chalkN=0, cW=0, cL=0, cNet=0.0, gN=0, gHit=0, gPts=0.0, gNet=0.0, gemN=0, gemPts=0.0, slN=0, slPts=0.0, spN=0, spPts=0.0))
        start = [r for r in rs if r['started']]; bench = [r for r in rs if r['slot'] == 'BN']
        for s in start:
            Z['starts'] += 1; ps = S(s)
            if ps is not None: Z['chalk'] += ps; Z['chalkN'] += 1
            # the crowd's alternative: the most-started benched player who could have filled this slot
            alts = [b for b in bench if TF.eligible(b['pos'], s['slot']) and S(b) is not None]
            if ps is not None and alts:
                b = max(alts, key=S)
                if S(b) - ps >= CALL_GAP:
                    d = (s['pts'] or 0) - (b['pts'] or 0)
                    Z['cW'] += d > 0; Z['cL'] += d < 0; Z['cNet'] += d
                    calls.append(dict(y=y, wk=w, m=m, team=team, n=s['n'], pos=s['pos'], ps=ps, pts=s['pts'] or 0, over=b['n'], opos=b['pos'], pb=S(b), opts=b['pts'] or 0, d=round(d, 2)))
            if ps is not None and ps < SPOT:
                avg = before(s)
                if avg and avg > 0 and (s['pts'] or 0) >= 2 * avg:
                    Z['spN'] += 1; Z['spPts'] += (s['pts'] or 0) - avg
                    spots.append(dict(y=y, wk=w, m=m, team=team, n=s['n'], pos=s['pos'], ps=ps, pts=s['pts'] or 0, avg=round(avg, 2), x=round((s['pts'] or 0) / avg, 2)))
            if ps is not None and ps < GUTSY:
                p0 = (s['pos'] or '').split(',')[0]; ln = line.get((w, p0))
                if ln is not None:
                    Z['gN'] += 1; hit = (s['pts'] or 0) > ln; Z['gHit'] += hit; Z['gNet'] += (s['pts'] or 0) - ln
                    if hit: Z['gPts'] += (s['pts'] or 0) - ln
                    gutsy.append(dict(y=y, wk=w, m=m, team=team, n=s['n'], pos=s['pos'], ps=ps, pts=s['pts'] or 0, line=round(ln, 2), hit=hit, over=round((s['pts'] or 0) - ln, 2)))
        for b in bench:
            pb = S(b)
            if pb is None or pb < GEM: continue
            elig = [s for s in start if TF.eligible(b['pos'], s['slot']) and (S(s) is None or S(s) < pb)]
            if not elig: continue
            s = min(elig, key=lambda r: r['pts'] or 0)
            if (b['pts'] or 0) > (s['pts'] or 0):
                lost = (b['pts'] or 0) - (s['pts'] or 0)
                Z['gemN'] += 1; Z['gemPts'] += lost
                gems.append(dict(y=y, wk=w, m=m, team=team, n=b['n'], pos=b['pos'], pb=pb, pts=b['pts'] or 0, over=s['n'], ps=S(s), spts=s['pts'] or 0, lost=round(lost, 2)))
    # sleepers: pickups the crowd had barely noticed the week they were added
    sleepers = []
    M_, L = TF.season(y)
    keyof = {}
    for r in R: keyof.setdefault(r['n'], r['key'])
    for p in L['picks_list']:
        k = keyof.get(p['n']); own = (O(k, p['wk'] - 1) if p['wk'] > 1 else None) if k else None
        if own is None and k: own = O(k, p['wk'])
        if own is None or own >= SLEEPER or p['starts'] < 2: continue
        later = [O(k, w) for w in range(p['wk'] + 1, p['wk'] + 5) if O(k, w) is not None]
        Z = M.get(p['m'])
        if Z: Z['slN'] += 1; Z['slPts'] += p['pts']
        sleepers.append(dict(y=y, wk=p['wk'], d=p['d'], m=p['m'], team=p['team'], n=p['n'], pos=p['pos'], own=own, later=max(later) if later else None,
                             starts=p['starts'], pts=p['pts'], val=p['val']))
    return M, calls, gutsy, gems, sleepers, spots

def build():
    years = list(TF.YEARS)
    mg, calls, gutsy, gems, sleepers, spots, weeks = {}, [], [], [], [], [], {}
    for y in years:
        try:
            # the live season re-reads its last finished week and the week being set (lineups change until kickoff)
            last = max([g['wk'] for g in P.games(y) if g['status'] == 'postevent'] or [1]) if y == TF.LIVE else None
            PCT = fetch(y, refresh_from=last)
            if not PCT: continue
            M, c, g, gm, sl, sp = season(y, PCT)
        except Exception as e:   # one season failing never takes the others off the page
            import sys; print('  (crowd: %d left out: %s)' % (y, str(e)[:120]), file=sys.stderr); continue
        for m, Z in M.items(): mg.setdefault(m, {})[y] = {k: round(v, 2) if isinstance(v, float) else v for k, v in Z.items()}
        calls += c; gutsy += g; gems += gm; sleepers += sl; spots += sp
        weeks[y] = len({c_['wk'] for c_ in c} | {x['wk'] for x in g})
    years = [y for y in years if y in weeks]
    # each list keeps its top rows per season, so the page can show any one season or all of them
    def top(rows, key, n=15):
        out = []
        for y in years: out += sorted([r for r in rows if r['y'] == y], key=key)[:n]
        return out
    kd = lambda r: (r['pos'] or '').split(',')[0] in ('K', 'DEF')
    return dict(years=years, mgrs=mg, weeks=weeks,
                best=top([c for c in calls if c['d'] > 0], lambda x: -x['d']), worst=top([c for c in calls if c['d'] < 0], lambda x: x['d']),
                gutsy=top([x for x in gutsy if x['hit']], lambda x: -x['over']),
                spots=top(spots, lambda x: -(x['pts'] - x['avg'])),
                gems=top(gems, lambda x: -x['lost']),
                sleepers=top([x for x in sleepers if not kd(x)], lambda x: -(x['val'] or 0)),
                sleepersKD=top([x for x in sleepers if kd(x)], lambda x: -(x['val'] or 0), 6),
                rules=dict(call=CALL_GAP, gutsy=GUTSY, gem=GEM, sleeper=SLEEPER, spot=SPOT))

if __name__ == '__main__':
    import sys
    for y in [int(a) for a in sys.argv[1:]] or TF.YEARS:
        PCT = fetch(y, refresh_from=(None if y != TF.LIVE else max([0] + [int(f[5:-5]) for f in os.listdir('yahoo_raw/%d' % y) if f.startswith('pct_w')]) or None))
        print(y, 'weeks', len(PCT), 'players a week', round(sum(len(v) for v in PCT.values()) / max(1, len(PCT))))
