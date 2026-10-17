# -*- coding: utf-8 -*-
"""The latest news on every player Yahoo lists as hurt on a Deadshot roster (USER, 17 Oct 2026).

Yahoo's API says only that a player has a news note, not what it says. ESPN's public per-player news feed
carries the same Rotowire write-ups Yahoo shows, each with the minute it was published. It is unofficial (no
key, no promise it stays), so a failure leaves the news out and nothing else. Only the headline is kept, with
its time and a link to the player's page: the full write-up is Rotowire's, licensed, and stays on their pages.

    latest(players) -> {name: [{t: ISO time, h: headline}, ...newest first], '_link': {name: url}}
"""
import json, os, time, datetime
import injuries as I

IDS = 'yahoo_raw/espn_ids.json'
KEEP, DAYS = 3, 21

def _espn_ids():
    """{Sleeper id: ESPN id}, from Sleeper's player list (refreshed weekly)"""
    if os.path.exists(IDS) and time.time() - os.path.getmtime(IDS) < 7 * 86400:
        return json.load(open(IDS))
    P = I._get('https://api.sleeper.app/v1/players/nfl')
    out = {pid: str(p['espn_id']) for pid, p in P.items() if p.get('espn_id')}
    json.dump(out, open(IDS, 'w'))
    return out

def _search(name):
    """ESPN's own player search, for the few players Sleeper has no ESPN id for (Caleb Williams)"""
    import urllib.parse
    try:
        d = I._get('https://site.web.api.espn.com/apis/common/v3/search?type=player&sport=football&league=nfl&limit=3&query=' + urllib.parse.quote(name))
    except Exception:
        return None
    hit = [it for it in d.get('items') or [] if I.norm(it.get('displayName')) == I.norm(name)]
    return str(hit[0]['id']) if len(hit) == 1 else None

def latest(players):
    """players: [(name, positions)] (defenses are skipped)"""
    ids, E = I._ids(), _espn_ids()
    cut = (datetime.datetime.utcnow() - datetime.timedelta(days=DAYS)).strftime('%Y-%m-%dT%H:%M:%SZ')
    out, link = {}, {}
    for name, pos in players:
        if (pos or '').split(',')[0] == 'DEF': continue
        eid = next((E[c] for c in I.cands(ids, name, pos) if c in E), None) or _search(name)
        if not eid: continue
        try:
            d = I._get('https://site.api.espn.com/apis/fantasy/v2/games/ffl/news/players?limit=12&playerId=' + eid)
        except Exception:
            continue
        items = [dict(t=it['published'], h=it['headline'].strip()) for it in d.get('feed') or []
                 if it.get('type') == 'Rotowire' and it.get('headline') and (it.get('published') or '') >= cut]
        items.sort(key=lambda x: x['t'], reverse=True)
        if items:
            out[name] = items[:KEEP]
            link[name] = 'https://www.espn.com/nfl/player/_/id/' + eid
    out['_link'] = link
    return out

def sig():
    """the newest headline time for every hurt player on a Deadshot roster: changes when news lands"""
    import yahoo_parse as P, teamfile as TF
    R = P.rosters(TF.LIVE); wk = max(r['wk'] for r in R)
    hurt = sorted({(r['n'], r['pos']) for r in R if r['wk'] == wk and (r.get('status') or '') not in ('', 'OK')})
    L = latest(hurt)
    return '\n'.join('%s %s' % (n, L[n][0]['t']) for n in sorted(L) if n != '_link')

if __name__ == '__main__':
    import sys
    if '--sig' in sys.argv: print(sig()); sys.exit()
    r = latest([('A.J. Brown', 'WR'), ('Mike Evans', 'WR'), ('Caleb Williams', 'QB')])
    print(json.dumps(r, indent=1)[:2000])
