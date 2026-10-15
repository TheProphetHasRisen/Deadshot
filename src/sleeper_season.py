# -*- coding: utf-8 -*-
"""Every NFL player's points, week by week, for a finished season, scored with Deadshot's rules.

    weekly(y) -> (by_key, allwk, names)
      by_key  {"normalised name|POS": [points or None, week 1..17]}   (None: no game that week)
      allwk   {POS: [[points or None, ...], ...]}                        every player, for ranks
      names   {"normalised name|POS": "Display Name"}

It is what the 2026 page's draft board and trade cards are built on (draft_points.py), done for
2021-2025 so a past season's page can be drawn the same way. Sleeper's replies are cached in
yahoo_raw/ (gitignored): one compact file a season.
"""
import json, os
from scoring import score
import injuries

def _players():
    f = 'yahoo_raw/sleeper_players.json'
    if os.path.exists(f): return json.load(open(f))
    P = injuries._get('https://api.sleeper.app/v1/players/nfl')
    OFF = ('QB', 'RB', 'WR', 'TE', 'K')
    pos = lambda p: p.get('position') if p.get('position') in OFF else next((x for x in p.get('fantasy_positions') or [] if x in OFF), None)
    out = {pid: [p.get('full_name'), pos(p)] for pid, p in P.items() if pos(p)}
    json.dump(out, open(f, 'w')); return out

def weekly(y, weeks=range(1, 18)):
    f = 'yahoo_raw/sleeper_pts_%d.json' % y
    if os.path.exists(f):
        pts = json.load(open(f))
    else:
        P = _players(); pts = {}
        for w in weeks:
            st = injuries._get('https://api.sleeper.app/v1/stats/nfl/regular/%d/%d' % (y, w))
            for pid, s in st.items():
                pos = 'DEF' if pid.isalpha() else (P.get(pid) or [None, None])[1]
                if pos not in ('QB', 'RB', 'WR', 'TE', 'K', 'DEF'): continue
                if pos != 'DEF' and not (s.get('gp') or 0): continue
                pts.setdefault(pid, [None] * len(weeks))[w - 1] = round(score(s, pos), 2)
        json.dump(pts, open(f, 'w'))
    P = _players(); by_key, allwk, names = {}, {}, {}
    for pid, line in pts.items():
        if pid.isalpha(): pos, name = 'DEF', pid
        else:
            name, pos = (P.get(pid) or [None, None])
            if not name: continue
        allwk.setdefault(pos, []).append(line)
        k = (pid if pos == 'DEF' else injuries.norm(name)) + '|' + pos
        if k not in by_key or sum(v or 0 for v in line) > sum(v or 0 for v in by_key[k]):
            by_key[k] = line; names[k] = name
    return by_key, allwk, names

def key(name, pos, nfl=None):
    """the by_key key for a Yahoo player: defenses by NFL team, everyone else by normalised name"""
    p0 = (pos or '').split(',')[0]
    if p0 == 'DEF': return injuries.TEAMFIX.get(nfl, nfl) + '|DEF'
    n = injuries.norm(name); return injuries.ALIAS.get(n, n) + '|' + p0

def keys(name, pos, nfl=None):
    """every by_key key worth trying for a Yahoo player: each spelling (Sleeper renames players) at each
    position Yahoo lists (Cordarrelle Patterson is "WR,RB"; Sleeper has him at RB)"""
    ps = (pos or '').split(',')
    if ps[0] == 'DEF': return [injuries.TEAMFIX.get(nfl, nfl) + '|DEF'] if nfl else []
    return [nm + '|' + p for p in ps for nm in injuries.names(injuries.norm(name))]

def lookup(by_key, name, pos, nfl=None):
    """(key, weekly line) for a Yahoo player, or (None, None)"""
    for k in keys(name, pos, nfl):
        if k in by_key: return k, by_key[k]
    return None, None

def ranker(by_key, allwk, weeks):
    """rank(name, pos, nfl) -> (points over the weeks, rank at his position among every NFL player), one
    ranking for the whole site (the season pages and the Front Office used to rank differently). A
    drafted player Sleeper knows who never played scores 0 and ranks behind everyone who scored."""
    tot = {p: sorted((sum(v or 0 for v in l[:weeks]) for l in lines), reverse=True) for p, lines in allwk.items()}
    ids = injuries._ids()
    def rank(name, pos, nfl=None):
        k, line = lookup(by_key, name, pos, nfl)
        if line is None:
            if (pos or '').split(',')[0] == 'DEF' or not injuries.cands(ids, name, pos): return None, None
            p0 = (pos or '').split(',')[0]
            return 0.0, 1 + sum(1 for t in tot.get(p0, []) if t > 0)
        p0 = k.split('|')[1]; t = sum(v or 0 for v in line[:weeks])
        return round(t, 2), 1 + sum(1 for x in tot.get(p0, []) if x > t + 1e-9)
    return rank
