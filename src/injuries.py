# -*- coding: utf-8 -*-
"""Who missed games, from 2021 on: worked out week by week, since Yahoo keeps no injury history.

A rostered player MISSED a week when his NFL team played and he did not (Sleeper's public weekly
stats mark every player who played with gp). Which team he played for, and that team's bye, come from
Sleeper's week-by-week stats for every finished season: Yahoo's old rosters carry each player's
CURRENT team and bye (2021's McCaffrey shows as a 49er with the 49ers' bye), which counted real byes as
missed games and dropped real absences (adversarial review, 15 Oct 2026). The live season uses Yahoo's,
which is current. Injury, illness, suspension or a
benching all look the same from the outside, so the site calls it "missed games", not "injuries".

    played(y)  -> a function (player, position, NFL team, week) -> True, False, or None if unknown

Sleeper's replies are cached in yahoo_raw/ (gitignored) after the first pull.
"""
import json, os, re, ssl, urllib.request
try:
    import certifi; CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CTX = ssl.create_default_context()

def _get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'deadshot'}), context=CTX, timeout=90) as r:
        return json.load(r)

def norm(n):
    n = (n or '').lower().replace('.', '').replace("'", '').replace('’', '').replace('-', ' ')
    return re.sub(r'\b(jr|sr|ii|iii|iv|v)\b', '', n).replace('  ', ' ').strip()

# Yahoo's name -> Sleeper's, either way round (Sleeper renames players: "Gabriel Davis" is now "Gabe Davis")
ALIAS = {'hollywood brown': 'marquise brown', 'gabe davis': 'gabriel davis', 'chig okonkwo': 'chigoziem okonkwo',
         'josh palmer': 'joshua palmer', 'mitch trubisky': 'mitchell trubisky', 'eli mitchell': 'elijah mitchell',
         'bam knight': 'zonovan knight'}
def names(n):
    """every spelling to try for a normalised name"""
    out = [n, ALIAS.get(n, n)] + [k for k, v in ALIAS.items() if v == n]
    return list(dict.fromkeys(out))
TEAMFIX = {'JAC': 'JAX', 'WSH': 'WAS', 'LA': 'LAR', 'OAK': 'LV'}

def _ids():
    f = 'yahoo_raw/sleeper_ids.json'
    if os.path.exists(f): return json.load(open(f))
    P = _get('https://api.sleeper.app/v1/players/nfl')
    out = {}
    for pid, p in P.items():
        # every position he can be played at, not only his listed one (Travis Hunter is listed as a cornerback)
        for pos in dict.fromkeys([p.get('position')] + list(p.get('fantasy_positions') or [])):
            if p.get('full_name') and pos in ('QB', 'RB', 'WR', 'TE', 'K'):
                out.setdefault(norm(p['full_name']) + '|' + pos, []).append(pid)
    json.dump(out, open(f, 'w'))
    return out

def _gp(y):
    f = 'yahoo_raw/sleeper_gp_%d.json' % y
    if os.path.exists(f) and y < 2026: return {int(k): set(v) for k, v in json.load(open(f)).items()}
    out = {}
    for w in range(1, 19):
        st = _get('https://api.sleeper.app/v1/stats/nfl/regular/%d/%d' % (y, w))
        ids = [pid for pid, s in st.items() if (s.get('gp') or 0) > 0]
        if ids: out[w] = ids
    json.dump(out, open(f, 'w'))
    return {int(k): set(v) for k, v in out.items()}

def cands(ids, name, pos):
    """Sleeper ids for a Yahoo player: every spelling, every position Yahoo lists ("QB,TE" for Taysom Hill)"""
    out = []
    for nm in names(norm(name)):
        for p in (pos or '').split(','):
            out += ids.get(nm + '|' + p, [])
    return list(dict.fromkeys(out))

def teams(y):
    """for a finished season: which NFL team each player played for each week, and which teams played
    each week (a team missing from a week was on its bye). From Sleeper's stats, which carry the team."""
    f = 'yahoo_raw/sleeper_team_%d.json' % y
    if os.path.exists(f):
        d = json.load(open(f))
    else:
        d = dict(pt={}, played={})
        for w in range(1, 19):
            rows = _get('https://api.sleeper.com/stats/nfl/%d/%d?season_type=regular' % (y, w)
                        + ''.join('&position[]=' + p for p in ('QB', 'RB', 'WR', 'TE', 'K', 'DEF')))
            tm = set()
            for r in rows:
                t, o = r.get('team'), r.get('opponent')
                if t and o: tm |= {t, o}
                if t and r.get('player_id'): d['pt'].setdefault(r['player_id'], {})[str(w)] = t
            if tm: d['played'][str(w)] = sorted(tm)
        json.dump(d, open(f, 'w'))
    return {pid: {int(w): t for w, t in v.items()} for pid, v in d['pt'].items()}, {int(w): set(v) for w, v in d['played'].items()}

def season_team(pt, pid, wk):
    """his team in week wk: that week's, else the nearest week before, else after (a player traded mid-season
    keeps the team he was with around the week in question)"""
    v = pt.get(pid) or {}
    if wk in v: return v[wk]
    before = [w for w in v if w < wk]; after = [w for w in v if w > wk]
    return v[max(before)] if before else v[min(after)] if after else None

def played(y, live=False):
    """(name, positions, Yahoo NFL team, Yahoo bye, week) -> True (played), False (his team played and he did
    not), None (his team was off, or he cannot be matched)"""
    ids, gp = _ids(), _gp(y)
    pt, tp = ({}, {}) if live else teams(y)
    def f(name, pos, nfl, bye, wk):
        if wk not in gp: return None
        p0 = (pos or '').split(',')[0]
        if p0 == 'DEF':   # a defense always plays when its team does
            t = TEAMFIX.get(nfl, nfl)
            return (True if t in gp[wk] else None) if live else (True if t in tp.get(wk, ()) else None)
        cand = cands(ids, name, pos)
        if not cand: return None
        if any(c in gp[wk] for c in cand): return True
        if live or not pt: return None if wk == bye else False
        team = next((season_team(pt, c, wk) for c in cand if pt.get(c)), None)
        if team is None: return None if wk == bye else False   # never played all season: Yahoo's bye is the best there is
        return False if team in tp.get(wk, ()) else None
    return f

def season_teams(y):
    """{Sleeper id: the team he played most weeks for that season}, for labelling old draft boards"""
    pt, _ = teams(y)
    out = {}
    for pid, v in pt.items():
        c = {}
        for t in v.values(): c[t] = c.get(t, 0) + 1
        out[pid] = max(c, key=c.get)
    return out
