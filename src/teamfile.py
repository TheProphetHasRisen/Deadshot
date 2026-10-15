# -*- coding: utf-8 -*-
"""The 2026 team files: everything Yahoo can say about each manager, against his own history
(2021 on, the seasons Yahoo reaches) and against the league, plus the playoff-odds model.

    python3 teamfile.py        # prints a summary; export.py calls build() and puts it in D.live.files

Reads only yahoo_raw/<year>/ (yahoo_fetch.py), data.py and season2026.py. Pure Python, no
numpy. Every figure is defined where it is computed, in words, because the page explains
each one under a ? mark and test_teamfile.py recomputes the important ones a second way.
"""
import os, json, math, random, datetime as dt
from zoneinfo import ZoneInfo
import yahoo_parse as P
import data as D
import season2026 as S

ET = ZoneInfo('America/New_York')
LIVE = 2026
YEARS = [y for y in range(2021, LIVE + 1) if os.path.exists('yahoo_raw/%d/teams.json' % y)]
FLEX = ('RB', 'WR', 'TE')
# starting spots league-wide (QB, 2 RB, 2 WR, TE, flex split about 4 RB / 5 WR / 1 TE, K, DEF on 10 teams):
# a player who finished inside these ranks was a starter-quality player that season
STARTERS = {'QB': 10, 'RB': 24, 'WR': 25, 'TE': 11, 'K': 10, 'DEF': 10}

def _plain(name):
    """a team name without emoji or symbols: Yahoo has 'HunchoCamby🥸', the record book 'HunchoCamby'"""
    return ''.join(ch for ch in (name or '') if ch.isalnum()).lower()

def mgr_of(y, team):
    book = S.MGR2026 if y == LIVE else D.MANAGERS.get(y, {})
    if team in book: return book[team]
    return next((m for t, m in book.items() if _plain(t) == _plain(team)), None)

def settings(y):
    s = P.load(y, 'settings')['league'][1]['settings'][0]
    slots = {r['roster_position']['position']: int(r['roster_position']['count']) for r in s['roster_positions']}
    return dict(slots=slots, po=int(s.get('playoff_start_week') or 15), nteams=int(s.get('num_playoff_teams') or 6))

def week_dates(y):
    """week -> its Sunday 1:00 pm Eastern kickoff (the lock this site uses for which week a move counts)"""
    out = {}
    for w in range(1, 19):
        f = 'yahoo_raw/%d/scoreboard_w%d.json' % (y, w)
        if not os.path.exists(f): continue
        ms = P.items(json.load(open(f))['fantasy_content']['league'][1]['scoreboard']['0']['matchups'])
        if not ms: continue   # a week with no matchups yet (the bracket is set later)
        m = ms[0]['matchup']
        start = dt.date.fromisoformat(m['week_start'])
        sun = start + dt.timedelta(days=(6 - start.weekday()) % 7)
        out[w] = dt.datetime(sun.year, sun.month, sun.day, 13, 0, tzinfo=ET)
    return out

def week_of(locks, ts):
    t = dt.datetime.fromtimestamp(ts, ET)
    for w in sorted(locks):
        if t < locks[w]: return w
    return max(locks) + 1

def eligible(pos, slot):
    ps = (pos or '').split(',')
    if slot == 'W/R/T': return any(p in FLEX for p in ps)
    return slot in ps

def _greedy(pool, slots):
    used, total = set(), 0.0
    for slot in ('QB', 'RB', 'WR', 'TE', 'K', 'DEF', 'W/R/T'):
        for _ in range(slots.get(slot, 0)):
            pick = next((p for p in pool if id(p) not in used and eligible(p['pos'], slot)), None)
            if pick: used.add(id(pick)); total += pick['pts'] or 0
    return total

def optimal(players, slots):
    """the best legal lineup from everyone not on IR: fill each fixed slot with the best eligible player,
    then the flex with the best of what is left. With one position each, that greedy order is optimal
    for this roster shape. A player listed at two (Taysom Hill, QB and TE) is tried at each in turn: left
    to the greedy order he took the QB slot from Josh Allen, and the "best possible" lineup came out
    lower than the one actually played (adversarial review, 15 Oct 2026)."""
    import itertools
    pool = sorted([p for p in players if p['slot'] != 'IR'], key=lambda p: -(p['pts'] or 0))
    multi = [p for p in pool if ',' in (p['pos'] or '')]
    if not multi: return _greedy(pool, slots)
    best = 0.0
    for combo in itertools.product(*[(p['pos'] or '').split(',') for p in multi]):
        as_one = {id(p): c for p, c in zip(multi, combo)}
        best = max(best, _greedy([dict(p, pos=as_one.get(id(p), p['pos'])) for p in pool], slots))
    return best

class _Ranks:
    """{(position, player): finishing rank at the position}, by Sleeper's weekly stats scored with the
    league's rules over the league's own weeks (1-17; the live season, the weeks played). Yahoo's
    season rankings count NFL week 18, which the league does not play, so the Front Office and the
    season pages gave the same pick two different finishes (adversarial review, 15 Oct 2026)."""
    def __init__(self, y, played=None):
        import sleeper_season as SL
        self.nfl = {}
        if y == LIVE:
            dp = json.load(open('draft_points.json')) if os.path.exists('draft_points.json') else {}
            wk, allwk = dp.get('wk%d' % y) or {}, dp.get('allwk%d' % y) or {}
            n = played or int((dp.get('weeks') or {}).get(str(y)) or 0)
            tot = {p: sorted((sum(v or 0 for v in l[:n]) for l in ls), reverse=True) for p, ls in allwk.items()}
            def r(name, pos, nfl=None):
                line = wk.get(name)
                if line is None: return None, None
                p0 = (pos or '').split(',')[0]; t = sum(v or 0 for v in line[:n])
                return round(t, 2), 1 + sum(1 for x in tot.get(p0, []) if x > t + 1e-9)
            self.r = r
        else:
            by_key, allwk, _ = SL.weekly(y); self.r = SL.ranker(by_key, allwk, 17)
    def get(self, k, default=None):
        pos, name = k
        out = self.r(name, pos, self.nfl.get(name))[1]
        return default if out is None else out

def ranks(y):
    return _Ranks(y)

def yahoo_ranks(y):
    """{(position, player): Yahoo's season rank at the position} (pos_totals still reads Yahoo's files)"""
    out = {}
    for pos in ('QB', 'RB', 'WR', 'TE', 'K', 'DEF'):
        n = 0
        for pg in range(4):
            f = 'yahoo_raw/%d/rank_%s_%d.json' % (y, pos, pg)
            if not os.path.exists(f): break
            for x in P.items(json.load(open(f))['fantasy_content']['league'][1]['players']):
                n += 1; out[(pos, P.flat(x['player'][0])['name']['full'])] = n
    return out

def pos_totals(y):
    """{position: season points of every ranked player there, best first}, from Yahoo's rankings"""
    out = {}
    for pos in STARTERS:
        tot = []
        for pg in range(4):
            f = 'yahoo_raw/%d/rank_%s_%d.json' % (y, pos, pg)
            if not os.path.exists(f): break
            for x in P.items(json.load(open(f))['fantasy_content']['league'][1]['players']):
                pp = P.flat(x['player'][1:]).get('player_points') or {}
                tot.append(float(pp.get('total') or 0))
        out[pos] = tot
    return out

def replacement(y, games):
    """points a game of a replacement-level player at each position that season: the first one past
    the league's starters (STARTERS) in Yahoo's season rankings, by the league's own scoring"""
    T = pos_totals(y)
    return {pos: T[pos][n] / games for pos, n in STARTERS.items() if len(T.get(pos, [])) > n and games}

def season(y):
    """everything for one season, keyed by manager"""
    st = settings(y); slots = st['slots']; locks = week_dates(y)
    G = [g for g in P.games(y) if g['status'] == 'postevent']
    R = P.rosters(y); X = [t for t in P.transactions(y) if t['status'] == 'successful']
    RK = ranks(y); RK.nfl = {r['n']: r['nfl'] for r in R}
    try: RK.nfl.update({n: nfl for _, _, n, nfl, _ in P.draft(y) if n and n not in RK.nfl})
    except Exception: pass
    reg = [g for g in G if g['wk'] < st['po']]
    weeks = sorted({g['wk'] for g in reg})
    # a finished season's rankings cover 17 NFL games; the live one, the weeks played so far
    RP = replacement(y, 17 if y != LIVE else len(weeks))
    trades_list, draft_list, picks_list, gone_list = [], [], [], []
    def value(rows, pos):
        """points that counted, minus a replacement-level starter at his position in the same starts"""
        r0 = RP.get((pos or '').split(',')[0])
        return None if r0 is None else sum((r['pts'] or 0) - r0 for r in rows)
    # rosters by (team, week)
    by = {}
    for r in R: by.setdefault((r['team'], r['wk']), []).append(r)
    score = {}
    for g in G: score[(g['ta'], g['wk'])] = (g['aa'], g['ab'], g['tb']); score[(g['tb'], g['wk'])] = (g['ab'], g['aa'], g['ta'])
    teams = sorted({g['ta'] for g in G} | {g['tb'] for g in G})
    M = {}
    for t in teams:
        m = mgr_of(y, t)
        if not m: continue
        M[m] = dict(team=t, g=0, w=0, l=0, pf=0.0, apw=0, apl=0, act=0.0, opt=0.0, lost_lineup=0, perfect=0,
                    adds=0, fa=0, wv=0, drops=0, trades=0, pk_pts=0.0, pk_marg=0.0, pk_starts=0, dr_pts=0.0,
                    drafted_pts=0.0, held=[], pickups=[], gone=[], trade_net=0.0, trade_w=0, trade_l=0, weekly=[], pk_val=0.0,
                    inj_g=0, inj_val=0.0)
    # results, all-play, lineups: regular season only, so seasons compare like for like
    for wk in weeks:
        sc = {t: score[(t, wk)][0] for t in teams if (t, wk) in score}
        for t in teams:
            m = mgr_of(y, t)
            if m not in M or (t, wk) not in score: continue
            me, opp, ot = score[(t, wk)]; Z = M[m]
            Z['g'] += 1; Z['w'] += me > opp; Z['l'] += me < opp; Z['pf'] += me
            Z['apw'] += sum(1 for o, v in sc.items() if o != t and me > v); Z['apl'] += sum(1 for o, v in sc.items() if o != t and me < v)
            pl = by.get((t, wk), [])
            act = sum(p['pts'] or 0 for p in pl if p['started']); opt = optimal(pl, slots)
            Z['act'] += act; Z['opt'] += opt
            if me < opp and opt > opp: Z['lost_lineup'] += 1
            if opt - act < 0.005: Z['perfect'] += 1
            Z['weekly'].append(dict(wk=wk, pts=round(me, 2), opp=round(opp, 2), vs=mgr_of(y, ot), opt=round(opt, 2),
                                    ap=sum(1 for o, v in sc.items() if o != t and me > v)))
    # who held whom, week by week
    held = {}
    for r in R: held.setdefault((r['team'], r['n']), set()).add(r['wk'])
    def stint(team, n, w0):
        """the weeks in a row this team held him from week w0 on. It must start AT w0: a move undone before
        the week locked has no weeks of its own, rather than borrowing the next add's or trade's (the
        2022 trade Krueger and Wu undid 87 minutes later was credited with a later deal's starts)"""
        hw = held.get((team, n), ())
        if w0 not in hw: return []
        run = [w0]
        while run[-1] + 1 in hw: run.append(run[-1] + 1)
        return run
    played_wks = {g['wk'] for g in G}   # weeks with final scores: a lineup set for a week not yet played is not a start
    def starts(team, n, wks):
        return [r for w in wks if w in played_wks for r in by.get((team, w), []) if r['n'] == n and r['started']]
    def marginal(team, r):
        """his points minus the best bench player who could have filled the same slot that week"""
        bench = [b for b in by.get((team, r['wk']), []) if b['slot'] == 'BN' and eligible(b['pos'], r['slot'])]
        return (r['pts'] or 0) - max([b['pts'] or 0 for b in bench], default=0)
    # a trade and its exact undo before the next week locked: neither happened
    import wire2026 as WR
    void = WR.undone([(t['ts'], week_of(locks, t['ts']), [(p['n'], p['frm'], p['to']) for p in t['players']])
                      for t in X if t['kind'] == 'trade'])
    # moves
    for t in X:
        if t['kind'] not in ('add', 'drop', 'add/drop', 'trade'): continue
        w = week_of(locks, t['ts']); d = dt.datetime.fromtimestamp(t['ts'], ET)
        if t['kind'] == 'trade':
            if t['ts'] in void: continue
            sides = {}
            for p in t['players']: sides.setdefault(p['to'], []).append(p)
            if len(sides) != 2: continue
            (ta, pa), (tb, pb) = sides.items()
            # graded on value at position: each player's points in the weeks he started for his new team
            # (regular season), minus a replacement-level starter at his position over those same starts,
            # so a quarterback's big raw totals do not decide every deal
            def detail(team, ps):
                out = []
                for p in ps:
                    ss = [r for r in starts(team, p['n'], stint(team, p['n'], w)) if r['wk'] < st['po']]
                    v = value(ss, p['pos'])
                    out.append(dict(n=p['n'], pos=p['pos'], starts=len(ss), counted=round(sum(r['pts'] or 0 for r in ss), 2),
                                    val=None if v is None else round(v, 2)))
                return out
            da, db = detail(ta, pa), detail(tb, pb)
            # a side's return is never worth less than getting nothing: a team that never started what it got
            # does not "win" because the other side started theirs below replacement (adversarial review)
            va, vb = max(0.0, sum(x['val'] or 0 for x in da)), max(0.0, sum(x['val'] or 0 for x in db))
            trades_list.append(dict(y=y, d=d.strftime('%b %-d'), wk=w,
                                    a=dict(m=mgr_of(y, ta), team=ta, got=da, counted=round(sum(x['counted'] for x in da), 2), val=round(va, 2)),
                                    b=dict(m=mgr_of(y, tb), team=tb, got=db, counted=round(sum(x['counted'] for x in db), 2), val=round(vb, 2))))
            for team, mine, theirs in ((ta, va, vb), (tb, vb, va)):
                m = mgr_of(y, team)
                if m not in M: continue
                M[m]['trades'] += 1; M[m]['trade_net'] += mine - theirs
                M[m]['trade_w'] += mine > theirs; M[m]['trade_l'] += mine < theirs
            continue
        for p in t['players']:
            team = p['to'] if p['move'] == 'add' else p['frm']; m = mgr_of(y, team)
            if m not in M: continue
            Z = M[m]
            if p['move'] == 'add':
                Z['adds'] += 1; Z['fa' if p['source'] != 'waivers' else 'wv'] += 1
                if w >= st['po']: continue   # pickups are judged on the regular season, like everything here
                run = [x for x in stint(team, p['n'], w) if x < st['po'] and x in played_wks]; ss = starts(team, p['n'], run)
                # kickers and defenses: a team almost never keeps a spare on the bench, so "over the
                # bench" would credit every point; they count toward points, not toward this
                kd = (p['pos'] or '').split(',')[0] in ('K', 'DEF')
                pts = sum(r['pts'] or 0 for r in ss); mg = None if kd else sum(marginal(team, r) for r in ss)
                Z['pk_pts'] += pts; Z['pk_marg'] += mg or 0; Z['pk_starts'] += 0 if kd else len(ss)
                val = value(ss, p['pos'])
                if (p['pos'] or '').split(',')[0] in ('QB', 'RB', 'WR', 'TE'): Z['pk_val'] += val or 0
                Z['pickups'].append(dict(n=p['n'], pos=p['pos'], d=d.strftime('%b %-d'), wk=w, held=len(run), starts=len(ss),
                                         pts=round(pts, 2), marg=None if mg is None else round(mg, 2), how='claim' if p['source'] == 'waivers' else 'free agent',
                                         rank=RK.get((p['pos'], p['n'])), val=None if val is None else round(val, 2)))
                picks_list.append(dict(Z['pickups'][-1], y=y, m=m, team=team))
            elif p['move'] == 'drop':
                Z['drops'] += 1
                if w >= st['po']: continue   # a cut after the regular season is not a waiver decision that cost anything
                # how long he had him: the weeks in a row on this roster that end the week before the drop (a
                # same-week add and drop is 0, and counts toward patience as one)
                hw = held.get((team, p['n']), ()); run = []
                while (w - 1 - len(run)) in hw: run.append(w - 1 - len(run))
                Z['held'].append(len([x for x in run if x in played_wks]))
                # what came after, for other teams, until this team took him back; regular season only
                back = min([x for x in hw if x >= w] or [99])
                after = [r for r in R if r['n'] == p['n'] and w <= r['wk'] < min(back, st['po']) and r['wk'] in played_wks and r['team'] != team]
                counted = sum(r['pts'] or 0 for r in after if r['started'])
                Z['gone'].append(dict(n=p['n'], pos=p['pos'], d=d.strftime('%b %-d'), wk=w, held=len([x for x in run if x in played_wks]),
                                      rank=RK.get((p['pos'], p['n'])), counted=round(counted, 2),
                                      to=sorted({mgr_of(y, r['team']) for r in after if r['started']} - {None})))
                gone_list.append(dict(Z['gone'][-1], y=y, m=m))
    # the draft: points that counted from each manager's own picks, while he kept them
    try:
        nt = len(teams); seen = {}
        for pick, team, n, nfl, pos in P.draft(y):
            m = mgr_of(y, team)
            if m not in M or not n: continue
            ss = [r for r in starts(team, n, stint(team, n, 1)) if r['wk'] < st['po']]
            got = sum(r['pts'] or 0 for r in ss); M[m]['drafted_pts'] += got
            p0 = (pos or '').split(',')[0]; seen[p0] = seen.get(p0, 0) + 1
            val = value(ss, pos)
            draft_list.append(dict(y=y, pick=pick, rnd=(pick - 1) // nt + 1, slot=(pick - 1) % nt + 1, m=m, n=n, pos=p0,
                                   taken=seen[p0], rank=RK.get((p0, n)), starts=len(ss), counted=round(got, 2),
                                   val=None if val is None else round(val, 2)))
    except (KeyError, IndexError, FileNotFoundError):
        pass
    # the league that season
    allw = [x['pts'] for Z in M.values() for x in Z['weekly']]
    mu = sum(allw) / len(allw) if allw else 0
    sd = math.sqrt(sum((v - mu) ** 2 for v in allw) / len(allw)) if allw else 0
    ppw = sd / 0.39894 if sd else None   # points a week per win, at an average score (see the In wins ?)
    for Z in M.values():
        g = Z['g'] or 1
        Z['ap'] = Z['apw'] / (Z['apw'] + Z['apl']) if Z['apw'] + Z['apl'] else None
        # wins above an average team: what this scoring earns against every opponent every week, over .500
        Z['waa'] = (Z['ap'] - 0.5) * Z['g'] if Z['ap'] is not None else None
        Z['eff'] = Z['act'] / Z['opt'] if Z['opt'] else None
        Z['left'] = (Z['opt'] - Z['act']) / g
        Z['patience'] = sum(Z['held']) / len(Z['held']) if Z['held'] else None
        Z['pickups'].sort(key=lambda x: -(x['val'] if x['val'] is not None else -999))
        # drops that came back: players who finished as a starter at their position and scored for someone
        # after the cut; a player cut more than once by the same manager is listed once, by the cut that cost most
        one = {}
        for x in Z['gone']:
            if x['rank'] and x['rank'] <= STARTERS.get((x['pos'] or '').split(',')[0], 12) and (x['counted'] > 0 or y == LIVE):
                if x['n'] not in one or (x['counted'], x['wk']) > (one[x['n']]['counted'], one[x['n']]['wk']): one[x['n']] = x
        Z['gone'] = sorted(one.values(), key=lambda x: (x['rank'], -x['counted']))
    eff_avg = sum(Z['act'] for Z in M.values()) / sum(Z['opt'] for Z in M.values()) if M else None
    opt_avg = sum(Z['opt'] for Z in M.values()) / max(1, sum(Z['g'] for Z in M.values()))
    for Z in M.values():
        # wins added by lineup calls, against a manager who set lineups at the league's average
        # efficiency: (his efficiency - league's) x his best possible points a week, in wins
        Z['lineup_wins'] = ((Z['eff'] - eff_avg) * Z['opt'] / ppw) if Z['eff'] is not None and ppw else None
        Z['pickup_wins'] = Z['pk_marg'] / ppw if ppw else None
    # games missed, from 2021 (injuries.py): a regular starter (started at least half the games he played
    # for this team) who missed a week cost his points a game over a replacement-level starter at his
    # position. Regular season only. Turned into wins with this season's points per win.
    hits = []
    try:
        import injuries
        _pl = injuries.played(y, live=(y == LIVE))
        PL = lambda n, pos, nfl, wk, bye=None: _pl(n, pos, nfl, bye, wk)
    except Exception:
        PL = None
    # what a drafted player was expected to score a game: what the player who finished at the slot he was
    # drafted at (the Nth at his position) scored. A pick who barely played is valued mostly on that,
    # his own scoring counting for more as his games pile up (EXP_G games' worth of the expectation)
    EXP_G = 4
    TOT = pos_totals(y); ngames = 17 if y != LIVE else max(1, len(weeks))
    taken = {d['n']: (d['pos'], d['taken'], d['m']) for d in draft_list}
    def slot_ppg(n):
        t = taken.get(n)
        if not t: return None
        tot = TOT.get(t[0], [])
        return tot[t[1] - 1] / ngames if len(tot) >= t[1] else (tot[-1] / ngames if tot else None)
    via_trade = {(p['to'], p['n']) for t in X if t['kind'] == 'trade' and t['ts'] not in void for p in t['players']}
    if PL:
        reg_wks = set(weeks)
        played_pts = {}
        for r in R:
            if r['wk'] in reg_wks and PL(r['n'], r['pos'], r['nfl'], r['wk'], r.get('bye')):
                played_pts.setdefault(r['n'], {})[r['wk']] = r['pts'] or 0
        for (team, n), wks in held.items():
            m = mgr_of(y, team)
            if m not in M: continue
            rows = [r for w in sorted(wks) if w in reg_wks for r in by.get((team, w), []) if r['n'] == n]
            if not rows: continue
            pos = (rows[0]['pos'] or '').split(',')[0]
            pl = [r for r in rows if PL(r['n'], r['pos'], r['nfl'], r['wk'], r.get('bye'))]
            # missed: his team played and he did not. An IR slot is not a miss by itself: a player stashed
            # there who played that week (Omarion Hampton, 2025 week 14) was not missing anything
            miss = [r for r in rows if PL(r['n'], r['pos'], r['nfl'], r['wk'], r.get('bye')) is False]
            if not miss: continue
            ppg_w = played_pts.get(n, {}); g = len(ppg_w)
            ppg = sum(ppg_w.values()) / g if g else None
            sp = slot_ppg(n)
            if ppg is None and sp is None: continue
            # a regular starter: started at least half the games he played for this team, or this manager
            # drafted him as a starter at his position (a top pick hurt early still counts). An IR stash who
            # never played is not one, and someone else's draft slot says nothing about this team's lineup
            t = taken.get(n)
            drafted_starter = bool(t) and t[2] == m and t[1] <= STARTERS.get(t[0], 0)
            starter = (pl and sum(1 for r in pl if r['started']) * 2 >= len(pl)) or drafted_starter
            if not starter: continue
            exp = ((ppg or 0) * g + sp * EXP_G) / (g + EXP_G) if sp is not None else ppg
            lost = max(0.0, exp - RP.get(pos, 0)) * len(miss)
            Z = M[m]; Z['inj_g'] += len(miss); Z['inj_val'] += lost
            hits.append(dict(y=y, m=m, n=n, pos=pos, missed=len(miss), ppg=None if ppg is None else round(ppg, 2), g=g,
                             exp=round(exp, 2), slot=(t[0] + str(t[1])) if t and t[2] == m else None,
                             how='draft' if t and t[2] == m else 'trade' if (team, n) in via_trade else 'pickup', val=round(lost, 2),
                             wks=[r['wk'] for r in miss]))
    hits.sort(key=lambda h: -h['val'])
    inj_avg = sum(Z['inj_val'] for Z in M.values()) / max(1, len(M))
    for Z in M.values():
        # injury luck, in wins: the league's average loss to missed games minus his (plus = lucky)
        Z['inj_wins'] = Z['inj_val'] / ppw if ppw else None
        Z['inj_luck'] = (inj_avg - Z['inj_val']) / ppw if ppw else None
    # who held whom: weeks on a manager's roster, every player
    hw = {}
    for r in R:
        m = mgr_of(y, r['team'])
        if m and r['wk'] in weeks: hw[(r['n'], m)] = hw.get((r['n'], m), 0) + 1
    league = dict(year=y, avg=mu, sd=sd, ppw=ppw, eff=eff_avg, opt=opt_avg, weeks=len(weeks), repl=RP, hits=hits,
                  injAvg=inj_avg,
                  trades_list=trades_list, draft_list=draft_list, picks_list=picks_list, gone_list=gone_list,
                  held=[dict(n=n, m=m, wks=v) for (n, m), v in hw.items()],
                  moves=sum(Z['adds'] for Z in M.values()) / max(1, len(M)),
                  trades=sum(Z['trades'] for Z in M.values()) // 2, teams=len(M))
    return M, league

# ------------------------------------------------------------------ the model
def model(H, played):
    """Playoff odds. First a regression on every logged season: a team's points a game over weeks
    1..k (k = weeks played this year) against its points a game over the rest of the regular
    season. The slope says how much of an early hot or cold start carries on. Then 20,000 runs of
    the rest of the 2026 schedule, each team scoring around its regressed level with the weekly
    spread history shows; top six make it, the top two get byes, and the bracket is played out."""
    xs, ys, resid_w = [], [], []
    for y in YEARS:
        if y == LIVE: continue
        for Z in H[y][0].values():
            wk = [x['pts'] for x in Z['weekly']]
            if len(wk) <= played: continue
            xs.append(sum(wk[:played]) / played); ys.append(sum(wk[played:]) / len(wk[played:]))
            m = sum(wk) / len(wk); resid_w += [v - m for v in wk]
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys)); sxx = sum((a - mx) ** 2 for a in xs)
    b = sxy / sxx; a = my - b * mx
    syy = sum((v - my) ** 2 for v in ys); r = sxy / math.sqrt(sxx * syy)
    wsd = math.sqrt(sum(v * v for v in resid_w) / len(resid_w))
    M26 = H[LIVE][0]
    # the 2026 field: this season's level, scaled to this season's scoring
    lg_hist = sum(H[y][1]['avg'] for y in YEARS if y != LIVE) / len([y for y in YEARS if y != LIVE])
    scale = H[LIVE][1]['avg'] / lg_hist
    level = {m: (a + b * (sum(x['pts'] for x in Z['weekly'][:played]) / played / scale)) * scale for m, Z in M26.items()}
    # the schedule still to play
    team_m = {Z['team']: m for m, Z in M26.items()}
    sched = [(g['wk'], team_m[g['ta']], team_m[g['tb']]) for g in P.games(LIVE) if g['status'] != 'postevent' and g['wk'] < settings(LIVE)['po']]
    base = {m: [Z['w'], Z['pf']] for m, Z in M26.items()}
    rnd = random.Random(2026); N = 20000
    po = {m: 0 for m in M26}; bye = dict(po); title = dict(po); wins = dict(po)
    for _ in range(N):
        rec = {m: [v[0], v[1]] for m, v in base.items()}
        for wk, ta, tb in sched:
            sa = rnd.gauss(level[ta], wsd); sb = rnd.gauss(level[tb], wsd)
            rec[ta][1] += sa; rec[tb][1] += sb
            rec[ta if sa > sb else tb][0] += 1
        seeds = sorted(rec, key=lambda m: (-rec[m][0], -rec[m][1]))[:6]
        for m in rec: wins[m] += rec[m][0]
        for m in seeds: po[m] += 1
        for m in seeds[:2]: bye[m] += 1
        play = lambda x, z: x if rnd.gauss(level[x], wsd) > rnd.gauss(level[z], wsd) else z
        q1, q2 = play(seeds[2], seeds[5]), play(seeds[3], seeds[4])
        s1, s2 = play(seeds[0], q2), play(seeds[1], q1)
        title[play(s1, s2)] += 1
    odds = [dict(mgr=m, team=M26[m]['team'], level=round(level[m], 2), po=po[m] / N, bye=bye[m] / N, title=title[m] / N,
                 wins=wins[m] / N) for m in M26]
    odds.sort(key=lambda o: -o['po'])
    return dict(n=n, a=a, b=b, r=r, wsd=wsd, played=played, runs=N, odds=odds,
                weeksLeft=len({w for w, _, _ in sched}))

def build():
    H = {y: season(y) for y in YEARS}
    played = H[LIVE][1]['weeks']
    keep = ('g', 'w', 'l', 'pf', 'ap', 'waa', 'eff', 'left', 'lost_lineup', 'perfect', 'adds', 'fa', 'wv', 'drops', 'trades',
            'pk_pts', 'pk_marg', 'pk_starts', 'patience', 'drafted_pts', 'trade_net', 'trade_w', 'trade_l', 'lineup_wins', 'pickup_wins', 'pk_val', 'inj_g', 'inj_val', 'inj_wins', 'inj_luck')
    LEAN = ('trades_list', 'draft_list', 'picks_list', 'gone_list', 'held')
    out = dict(years=YEARS, league={y: {k: v for k, v in H[y][1].items() if k not in LEAN} for y in YEARS}, model=model(H, played), files={})
    for m in H[LIVE][0]:
        hist = {y: {k: H[y][0][m][k] for k in keep} for y in YEARS if m in H[y][0]}
        Z = H[LIVE][0][m]
        out['files'][m] = dict(team=Z['team'], hist=hist, weekly=Z['weekly'], pickups=Z['pickups'][:8], gone=Z['gone'][:8])
    # 2026, league-wide: pickups by value at position (skill positions; kickers and defenses apart,
    # since everyone streams them), and drops of players who are finishing as starters
    L26 = H[LIVE][1]
    out['picks'] = sorted([p for p in L26['picks_list'] if skill(p) and p['starts']], key=lambda p: -p['val'])[:12]
    out['picksKD'] = sorted([p for p in L26['picks_list'] if not skill(p) and p['starts'] and p['val'] is not None], key=lambda p: -p['val'])[:6]
    out['gone'] = [g for g in starters_gone(L26['gone_list']) if skill(g)][:12]
    out['goneKD'] = [g for g in starters_gone(L26['gone_list']) if not skill(g)][:6]
    out['fo'] = front_office(H, keep)
    # every finished season in the live season's shape, for its season page (seasonpage.py)
    import seasonpage
    out['seasons'] = {y: seasonpage.bundle(y, H) for y in YEARS if y != LIVE}
    # injuries, 2026: who missed games so far, and Yahoo's report as it stands for the coming week
    out['hits'] = L26['hits'][:12]
    out['injAvg'] = L26['injAvg']
    try:
        R = P.rosters(LIVE); wk = max(r['wk'] for r in R)
        out['injNow'] = sorted([dict(m=mgr_of(LIVE, r['team']), team=r['team'], n=r['n'], pos=r['pos'], status=r['status'], injury=r['injury'], slot=r['slot'])
                                for r in R if r['wk'] == wk and r['status'] and r['status'] not in ('NA',)],
                               key=lambda x: (x['team'], x['slot'] in ('BN', 'IR'), x['n']))
        out['injWeek'] = wk
    except Exception:
        out['injNow'] = []
    return out

LISTED = {'QB': 50, 'RB': 100, 'WR': 100, 'TE': 75, 'K': 50, 'DEF': 50}   # how deep Yahoo's ranked lists are pulled

def skill(p):
    return (p['pos'] or '').split(',')[0] in ('QB', 'RB', 'WR', 'TE')

def starters_gone(rows):
    """drops of players who finished the season as a starter at their position and scored for someone after
    the cut (the live season: anyone, while it is played), best finish first; a player cut more than once
    by the same manager is listed once, by the cut that cost most"""
    one = {}
    for x in rows:
        if not (x['rank'] and x['rank'] <= STARTERS.get((x['pos'] or '').split(',')[0], 12)): continue
        if x['counted'] <= 0 and x.get('y') != LIVE: continue
        k = (x.get('y'), x.get('m'), x['n'])
        if k not in one or (x['counted'], x['wk']) > (one[k]['counted'], one[k]['wk']): one[k] = x
    return sorted(one.values(), key=lambda x: (x['rank'], -x['counted']))

def front_office(H, keep):
    """every season Yahoo reaches, for the record book's Front Office section"""
    fin = [y for y in YEARS if y != LIVE]
    mgrs = {}
    for y in YEARS:
        for m, Z in H[y][0].items():
            mgrs.setdefault(m, {})[y] = {k: Z[k] for k in keep}
    allp = [p for y in YEARS for p in H[y][1]['picks_list'] if p['starts'] and p['val'] is not None]
    trades = [t for y in YEARS for t in H[y][1]['trades_list']]
    draft = [d for y in YEARS for d in H[y][1]['draft_list']]
    # what each first-round slot has meant: the manager who drew it, where he finished, his record
    slots = {}
    for d in draft:
        if d['rnd'] != 1 or d['y'] not in fin: continue
        book = D.MANAGERS[d['y']]; team = next((t for t, mm in book.items() if mm == d['m']), None)
        order = D.FINAL_PLACE.get(d['y'], []); place = order.index(team) + 1 if team in order else None
        rec = next(((r[2], r[3]) for r in D.STANDINGS[d['y']] if r[1] == team), (0, 0))
        # a shared title (2022's final was voided): both co-champions are champions, at half a title each
        co = team in getattr(D, 'CO_CHAMPS', {}).get(d['y'], [])
        slots.setdefault(d['slot'], []).append(dict(y=d['y'], m=d['m'], n=d['n'], place=1 if co else place, co=co, w=rec[0], l=rec[1]))
    held, yrs = {}, {}
    for y in YEARS:
        for h in H[y][1]['held']:
            held[(h['n'], h['m'])] = held.get((h['n'], h['m']), 0) + h['wks']
            yrs.setdefault((h['n'], h['m']), set()).add(y)
    loyal = sorted(({'n': n, 'm': m, 'wks': v, 'yrs': sorted(yrs[(n, m)])} for (n, m), v in held.items()), key=lambda x: (-x['wks'], -len(x['yrs'])))
    best_owner = {}
    for x in loyal:
        if x['n'] not in best_owner: best_owner[x['n']] = x
    return dict(years=YEARS, finished=fin, mgrs=mgrs,
                picks=sorted([p for p in allp if skill(p)], key=lambda p: -p['val'])[:25],
                picksKD=sorted([p for p in allp if not skill(p)], key=lambda p: -p['val'])[:10],
                gone=[g for g in starters_gone([g for y in YEARS for g in H[y][1]['gone_list']]) if skill(g)][:30],
                goneKD=[g for g in starters_gone([g for y in YEARS for g in H[y][1]['gone_list']]) if not skill(g)][:10],
                trades=trades,
                # drafted as the Nth at his position, finished Mth: the biggest climbs (skill positions) ...
                draftBest=sorted([d for d in draft if d['rank'] and d['pos'] in ('QB', 'RB', 'WR', 'TE') and d['y'] != LIVE],
                                 key=lambda d: (-(d['taken'] - d['rank']), -(d['val'] or 0)))[:20],
                # ... and the biggest falls among the first three rounds (a player outside Yahoo's
                # ranked list finished worse than the last ranked spot)
                draftWorst=sorted([dict(d, fell=(d['rank'] or LISTED[d['pos']] + 1) - d['taken']) for d in draft
                                   if d['rnd'] <= 3 and d['pos'] in ('QB', 'RB', 'WR', 'TE') and d['y'] != LIVE],
                                  key=lambda d: -d['fell'])[:20],
                draftByMgr=[dict(m=m, y=y, val=round(sum(d['val'] or 0 for d in draft if d['m'] == m and d['y'] == y), 1))
                            for m in mgrs for y in YEARS if any(d['m'] == m and d['y'] == y for d in draft)],
                slots=[dict(slot=k, seasons=v) for k, v in sorted(slots.items())],
                # for the season pages: each finished season's whole draft, its best pickups and its
                # drops that came back. Draft rows: [pick, round, slot, manager, player, pos, taken, rank, starts, counted]
                drafts={y: [[d['pick'], d['rnd'], d['slot'], d['m'], d['n'], d['pos'], d['taken'], d['rank'], d['starts'], d['counted']]
                            for d in draft if d['y'] == y] for y in fin},
                yPicks={y: sorted([p for p in H[y][1]['picks_list'] if skill(p) and p['starts'] and p['val'] is not None],
                                  key=lambda p: -p['val'])[:10] for y in fin},
                yGone={y: [g for g in starters_gone(H[y][1]['gone_list']) if skill(g)][:10] for y in fin},
                yLeague={y: {k: v for k, v in H[y][1].items() if k in ('avg', 'sd', 'ppw', 'eff', 'moves', 'trades', 'weeks')} for y in fin},
                hits=sorted([h for y in YEARS for h in H[y][1]['hits']], key=lambda h: -h['val'])[:25],
                yHits={y: H[y][1]['hits'][:10] for y in fin},
                loyal=list(best_owner.values())[:30])

if __name__ == '__main__':
    o = build()
    print('years', o['years'])
    md = o['model']; print('model: %d team-seasons, slope %.2f, r %.2f, weekly spread %.1f, weeks left %d' % (md['n'], md['b'], md['r'], md['wsd'], md['weeksLeft']))
    for x in md['odds']: print('  %-16s playoffs %4.0f%%  bye %4.0f%%  title %4.0f%%  wins %.1f' % (x['mgr'], 100 * x['po'], 100 * x['bye'], 100 * x['title'], x['wins']))
    for y in o['years']: L = o['league'][y]; print(y, 'avg %.1f  lineup eff %.3f  moves/team %.1f  trades %d' % (L['avg'], L['eff'] or 0, L['moves'], L['trades']))
    m = 'Brian Berger'; f = o['files'][m]
    for y, h in f['hist'].items(): print(m, y, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in h.items()})
