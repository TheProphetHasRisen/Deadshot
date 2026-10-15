# -*- coding: utf-8 -*-
"""Turn a season's raw Yahoo replies (yahoo_raw/<year>/, from yahoo_fetch.py) into plain tables.

Yahoo's JSON nests every object as a list of one-key dicts with empty lists between them; flat()
folds that into one dict. Everything returned here is ordinary Python: lists of dicts with
team NAMES (not Yahoo's team keys), so the rest of the code never sees a Yahoo key.
"""
import json, os, glob, datetime as dt

def flat(x):
    """[{a:1},[], {b:2}] -> {a:1, b:2}; nested one-level lists are folded in too"""
    out = {}
    if isinstance(x, dict): return x
    for part in x or []:
        if isinstance(part, dict): out.update(part)
        elif isinstance(part, list): out.update(flat(part))
    return out

def items(d):
    """Yahoo's {"0": {...}, "1": {...}, "count": n} collections, in order"""
    return [d[k] for k in sorted((k for k in d if k.isdigit()), key=int)]

def load(year, name):
    return json.load(open('yahoo_raw/%d/%s.json' % (year, name)))['fantasy_content']

def tidy(name):
    """Yahoo writes Poe’s Palace with a curly apostrophe; data.py has always used the straight one"""
    return name.replace('\u2019', "'") if name else name

def teams(year):
    """{team_key: {'name', 'manager'}}"""
    out = {}
    for t in items(load(year, 'teams')['league'][1]['teams']):
        f = flat(t['team'][0])
        mgr = f.get('managers', [{}])[0].get('manager', {})
        out[f['team_key']] = dict(name=tidy(f['name']), manager=mgr.get('nickname'), moves=int(f.get('number_of_moves') or 0),
                                  trades=int(f.get('number_of_trades') or 0), waiver=f.get('waiver_priority'))
    return out

def games(year):
    """one row per matchup: week, both teams, both scores, both projections, playoff flags"""
    T = teams(year); out = []
    for path in sorted(glob.glob('yahoo_raw/%d/scoreboard_w*.json' % year), key=lambda p: int(p.split('_w')[1][:-5])):
        sb = json.load(open(path))['fantasy_content']['league'][1]['scoreboard']
        for m in items(sb['0']['matchups']):
            m = m['matchup']; side = []
            for t in items(m['0']['teams']):
                f = flat(t['team'][0]); s = t['team'][1]
                side.append((T[f['team_key']]['name'], float(s['team_points']['total']),
                             float(s['team_projected_points']['total']) if 'team_projected_points' in s else None))
            out.append(dict(wk=int(m['week']), status=m['status'], playoffs=m.get('is_playoffs') == '1',
                            consolation=m.get('is_consolation') == '1',
                            ta=side[0][0], aa=side[0][1], pa=side[0][2], tb=side[1][0], ab=side[1][1], pb=side[1][2]))
    return out

def rosters(year):
    """one row per player per team per week: where he played (slot; BN = bench, IR) and his points"""
    T = teams(year); out = []
    for path in glob.glob('yahoo_raw/%d/roster_*_w*.json' % year):
        r = json.load(open(path))['fantasy_content']['team']
        tk = flat(r[0])['team_key']; ro = r[1]['roster']; wk = int(ro['week'])
        for p in items(ro['0']['players']):
            p = p['player']; f = flat(p[0]); rest = flat(p[1:])
            slot = flat(rest['selected_position']).get('position')
            pts = rest.get('player_points', {}).get('total')
            out.append(dict(wk=wk, team=T[tk]['name'], key=f['player_key'], n=f['name']['full'],
                            pos=f.get('display_position'), nfl=(f.get('editorial_team_abbr') or '').upper(),
                            slot=slot, started=slot not in ('BN', 'IR'), pts=float(pts) if pts is not None else None))
    out.sort(key=lambda r: (r['wk'], r['team'], not r['started'], r['n']))
    return out

def transactions(year):
    """oldest first. kind: add, drop, add/drop, trade. Each player: name, pos, nfl, move (add, drop,
    trade), source (freeagents, waivers, team), from/to team names."""
    T = teams(year); out = []
    for t in items(load(year, 'transactions')['league'][1]['transactions']):
        t = t['transaction']; meta = flat(t[0]); pl = []
        for p in items(t[1].get('players', {})) if len(t) > 1 and isinstance(t[1], dict) else []:
            p = p['player']; f = flat(p[0]); td = p[1]['transaction_data']
            td = td[0] if isinstance(td, list) else td
            pl.append(dict(n=f['name']['full'], pos=f.get('display_position'), nfl=(f.get('editorial_team_abbr') or '').upper(),
                           move=td['type'], source=td.get('source_type'),
                           frm=T.get(td.get('source_team_key'), {}).get('name'), to=T.get(td.get('destination_team_key'), {}).get('name')))
        out.append(dict(kind=meta['type'], status=meta.get('status'), ts=int(meta['timestamp']),
                        when=dt.datetime.fromtimestamp(int(meta['timestamp'])), players=pl,
                        faab=meta.get('faab_bid'), trader=T.get(meta.get('trader_team_key'), {}).get('name'),
                        tradee=T.get(meta.get('tradee_team_key'), {}).get('name')))
    out.sort(key=lambda r: r['ts'])
    return out

def draft(year):
    """(overall pick, team, player, NFL team, position), like season2026.DRAFT2026"""
    T = teams(year); out = []
    dr = load(year, 'draft')['league'][1]['draft_results']
    for r in items(dr):
        r = r['draft_result']; f = flat(r) if isinstance(r, list) else r
        p = (f.get('0') or {}).get('players') or f.get('players') or {}
        pf = flat(items(p)[0]['player'][0]) if p else {}
        out.append((int(f['pick']), T[f['team_key']]['name'], pf.get('name', {}).get('full'),
                    (pf.get('editorial_team_abbr') or '').upper(), pf.get('display_position')))
    return sorted(out)
