# -*- coding: utf-8 -*-
"""A finished season (2021 on), packaged in the same shape as the live one (D.live), so its season
page is drawn by exactly the same code as the 2026 page: standings with all-play and luck, results,
trades graded the same way (wire2026.grade), pickups, drops, the waiver wire, injuries, the team
files and the draft board with steals and busts.

    bundle(y, H) -> dict, called by teamfile.build() for every finished season; export.py puts them
    in D.seasons. H is teamfile's per-season results, so nothing is recomputed.

Sources: Yahoo (yahoo_raw/<y>/) for results, rosters, moves, trades and the draft; Sleeper
(sleeper_season.py) for every NFL player's weekly points, scored with the league's rules, which
the trade grades and the draft board rank against, as draft_points.py does for 2026.
"""
import datetime as dt
from zoneinfo import ZoneInfo
import yahoo_parse as P
import teamfile as TF
import wire2026 as W
import sleeper_season as SL

ET = ZoneInfo('America/New_York')

def _et(ts):
    t = dt.datetime.fromtimestamp(ts, ET)
    return t.strftime('%b ') + str(t.day), t.strftime('%I:%M %p').lstrip('0').lower()

class _Season:
    """the attributes wire2026.grade reads from season2026.py, filled from Yahoo for year y"""
    def __init__(self, y):
        self.MOVES2026, self.TRADES2026, self.TRADETIMES, self.TRADEPOS, self.CLAIMS2026 = [], [], {}, {}, []
        for t in P.transactions(y):
            if t['status'] != 'successful': continue
            d, hm = _et(t['ts'])
            if t['kind'] in ('add', 'drop', 'add/drop'):
                team = next(p['to'] if p['move'] == 'add' else p['frm'] for p in t['players'])
                adds = [(p['n'], p['nfl'], p['pos'], 'W' if p['source'] == 'waivers' else 'FA') for p in t['players'] if p['move'] == 'add']
                drops = [(p['n'], p['nfl'], p['pos']) for p in t['players'] if p['move'] == 'drop']
                self.MOVES2026.append((d, hm, team, adds, drops))
            elif t['kind'] == 'trade':
                sides = {}
                for p in t['players']:
                    sides.setdefault(p['to'], []).append(p['n']); self.TRADEPOS[p['n']] = p['pos']
                if len(sides) != 2: continue
                (ta, ga), (tb, gb) = list(sides.items())
                self.TRADES2026.append((d, ta, ga, tb, gb)); self.TRADETIMES.setdefault(d, hm)
        self.MOVES2026.reverse()
        self.DRAFT2026 = [(pk, team, n, nfl, pos) for pk, team, n, nfl, pos in P.draft(y) if n]
        self.ROSTERS2026 = [(r['wk'], r['team'], r['n'], r['pos'], r['slot'], r['pts']) for r in P.rosters(y)]

def bundle(y, H):
    st = TF.settings(y)
    G = [g for g in P.games(y) if g['status'] == 'postevent']
    reg = [g for g in G if g['wk'] < st['po']]
    weeks = sorted({g['wk'] for g in reg})
    teams = sorted({g['ta'] for g in reg} | {g['tb'] for g in reg})
    mgr = {t: TF.mgr_of(y, t) for t in teams}
    games = [dict(wk=g['wk'], ta=g['ta'], aa=g['aa'], pa=g['pa'], tb=g['tb'], ab=g['ab'], pb=g['pb']) for g in reg]
    # standings at the end of the regular season, ranked as the league ranks them (record, then points)
    rec = {t: dict(w=0, l=0, t=0, pf=0.0, pa=0.0, res=[], apW=0, apL=0) for t in teams}
    for w in weeks:
        sc = {}
        for g in [g for g in reg if g['wk'] == w]:
            sc[g['ta']] = g['aa']; sc[g['tb']] = g['ab']
            for a, b, x, z in ((g['ta'], g['tb'], g['aa'], g['ab']), (g['tb'], g['ta'], g['ab'], g['aa'])):
                r = rec[a]; r['pf'] += x; r['pa'] += z
                if x > z: r['w'] += 1; r['res'].append('W')
                elif x < z: r['l'] += 1; r['res'].append('L')
                else: r['t'] += 1; r['res'].append('T')
        for t, v in sc.items():
            rec[t]['apW'] += sum(1 for o, u in sc.items() if o != t and v > u)
            rec[t]['apL'] += sum(1 for o, u in sc.items() if o != t and v < u)
    T = P.teams(y); moves = {v['name']: v['moves'] for v in T.values()}
    order = sorted(teams, key=lambda t: (-(rec[t]['w'] + rec[t]['t'] / 2), -rec[t]['pf']))
    standings = []
    for i, t in enumerate(order):
        r = rec[t]; res = r['res']; n = 0
        for x in reversed(res):
            if x != res[-1]: break
            n += 1
        g = r['w'] + r['l'] + r['t']; ap = r['apW'] / (r['apW'] + r['apL']) if r['apW'] + r['apL'] else None
        standings.append(dict(rank=i + 1, team=t, mgr=mgr[t], w=r['w'], l=r['l'], t=r['t'], pf=round(r['pf'], 2), pa=round(r['pa'], 2),
                              streak=(res[-1] + str(n)) if res else '', waiver=None, moves=moves.get(t),
                              apW=r['apW'], apL=r['apL'], luck=None if ap is None else round((r['w'] + r['t'] / 2) - g * ap, 2)))
    # every NFL player's weeks, scored with the league's rules
    by_key, allwk, _ = SL.weekly(y)
    S = _Season(y)
    names = {}
    for d, hm, team, adds, drops in S.MOVES2026:
        for a in adds: names[a[0]] = (a[2], a[1])
        for x in drops: names[x[0]] = (x[2], x[1])
    for pk, team, n, nfl, pos in S.DRAFT2026: names[n] = (pos, nfl)
    for n, pos in S.TRADEPOS.items(): names.setdefault(n, (pos, None))
    wk = {n: SL.lookup(by_key, n, pos, nfl)[1] for n, (pos, nfl) in names.items()}
    wk = {n: v for n, v in wk.items() if v}
    k1 = TF.week_dates(y).get(1)
    wire = W.grade(S, wk, max(weeks), games, allwk, TF.replacement(y, 17), year=y,
                   kick1=dt.datetime(k1.year, k1.month, k1.day, 13, 0) if k1 else None)
    # the draft, and every drafted player's season: points and rank at his position, NFL-wide, the same
    # ranking the Front Office uses (sleeper_season.ranker); a pick who never played ranks behind everyone
    rank = SL.ranker(by_key, allwk, 17)
    dp = {}
    for pk, team, n, nfl, pos in S.DRAFT2026:
        pts, rk = rank(n, pos, nfl)
        if rk is not None: dp[n] = [pts, rk]
    tot = {pos: sorted((sum(v or 0 for v in line[:17]) for line in lines), reverse=True) for pos, lines in allwk.items()}
    curve = {pos: [round(p, 1) for p in lst[:150]] for pos, lst in tot.items()}
    # the NFL team each pick played for THAT season (Yahoo's old drafts carry today's: 2021's McCaffrey "SF")
    import injuries
    ids, st = injuries._ids(), injuries.season_teams(y)
    def then(n, pos, nfl):
        if (pos or '').split(',')[0] == 'DEF': return nfl
        return next((st[c] for c in injuries.cands(ids, n, pos) if c in st), nfl)
    S.DRAFT2026 = [(pk, team, n, then(n, pos, nfl), pos) for pk, team, n, nfl, pos in S.DRAFT2026]
    # the page draws pickups and drops from the team files below; the grader's full lists are not needed
    wire['picks'] = [p for p in wire['picks'] if p.get('g')][:10]
    wire['gone'] = [p for p in wire['gone'] if p.get('g')][:10]
    M, L = H[y]
    # the team-file pieces for this season (careers come from the Front Office data on the page)
    files = {m: dict(team=Z['team'], weekly=Z['weekly'], pickups=Z['pickups'][:8], gone=Z['gone'][:8]) for m, Z in M.items()}
    out = dict(year=y, final=True, weeks=weeks, regWeeks=len(weeks), mgr=mgr, games=games, standings=standings,
                upcoming=[], asOf='Final', trades=[dict(d=d, ta=ta, ga=ga, tb=tb, gb=gb) for (d, ta, ga, tb, gb) in S.TRADES2026],
                draft={str(y): [list(p) for p in S.DRAFT2026]},
                draftPts={str(y): dp, 'weeks': {str(y): 17}, 'curve' + str(y): curve},
                wire=wire,
                tf=dict(files=files,
                        picks=sorted([p for p in L['picks_list'] if TF.skill(p) and p['starts'] and p['val'] is not None], key=lambda p: -p['val'])[:12],
                        picksKD=sorted([p for p in L['picks_list'] if not TF.skill(p) and p['starts'] and p['val'] is not None], key=lambda p: -p['val'])[:6],
                        gone=[g for g in TF.starters_gone(L['gone_list']) if TF.skill(g)][:12],
                        goneKD=[g for g in TF.starters_gone(L['gone_list']) if not TF.skill(g)][:6],
                        hits=L['hits'][:12], injAvg=L['injAvg']))
    # the record book's own team names: Yahoo has "HunchoCamby🥸" for 2021, the record book "HunchoCamby"
    import data as D
    ren = {}
    for t in teams:
        bk = next((b for b in D.MANAGERS.get(y, {}) if TF._plain(b) == TF._plain(t)), t)
        if bk != t: ren[t] = bk
    def walk(x):
        if isinstance(x, dict): return {ren.get(k, k): walk(v) for k, v in x.items()}
        if isinstance(x, list): return [walk(v) for v in x]
        if isinstance(x, tuple): return tuple(walk(v) for v in x)
        return ren.get(x, x) if isinstance(x, str) else x
    return walk(out) if ren else out
