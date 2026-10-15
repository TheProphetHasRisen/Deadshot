# -*- coding: utf-8 -*-
"""Pull one Deadshot season from Yahoo, raw, into yahoo_raw/<year>/.

    python3 yahoo_fetch.py 2026          # everything for 2026, weeks played so far
    python3 yahoo_fetch.py 2026 --weeks 6  # only re-pull the given week's scores and rosters
    python3 yahoo_fetch.py 2026 --extras   # only the schedule still to play and the season rankings

Read only: it saves Yahoo's replies exactly as they came, and changes nothing on the site.
yahoo_parse.py turns them into plain tables. Nothing here is committed (yahoo_raw/ is
gitignored): it is a cache that can always be pulled again.
"""
import json, os, sys, time
import yahoo_api as Y

KEYS = 'yahoo_raw/league_keys.json'

def league_key(year):
    keys = json.load(open(KEYS)) if os.path.exists(KEYS) else {}
    if str(year) in keys: return keys[str(year)]
    import re
    r = json.dumps(Y.get('users;use_login=1/games;seasons=%d/leagues' % year))
    for m in re.finditer(r'"league_key": "([^"]+)", "league_id": "\d+", "name": "([^"]+)"', r):
        if 'DEAD' in m.group(2).upper():
            os.makedirs('yahoo_raw', exist_ok=True)   # a fresh machine (the scheduled job's) has none yet
            keys[str(year)] = m.group(1); json.dump(keys, open(KEYS, 'w'), indent=1); return m.group(1)
    raise SystemExit('No Deadshot league found for %d on this Yahoo account' % year)

def pull(year, only_weeks=None):
    K = league_key(year); d = 'yahoo_raw/%d' % year; os.makedirs(d, exist_ok=True)
    def save(name, path):
        for attempt in range(3):
            try:
                r = Y.get(path); break
            except Y.YahooError:
                if attempt == 2: raise
                time.sleep(2 + 3 * attempt)
        json.dump(r, open('%s/%s.json' % (d, name), 'w'))
        return r
    st = save('settings', 'league/%s/settings' % K)['fantasy_content']['league'][0]
    last = int(st.get('current_week') or st['end_week'])
    if st.get('is_finished') or year < time.localtime().tm_year: last = int(st['end_week'])
    if not only_weeks:
        save('teams', 'league/%s/teams' % K)
        save('standings', 'league/%s/standings' % K)
        save('draft', 'league/%s/draftresults/players' % K)
        # every transaction: Yahoo pages them 25 at a time unless asked for more
        save('transactions', 'league/%s/transactions;count=1000' % K)
    teams = json.load(open('%s/teams.json' % d))['fantasy_content']['league'][1]['teams']
    tkeys = [teams[k]['team'][0][0]['team_key'] for k in teams if k != 'count']
    weeks = [] if only_weeks == 'extras' else only_weeks or range(1, last + 1)
    for w in weeks:
        save('scoreboard_w%d' % w, 'league/%s/scoreboard;week=%d' % (K, w))
        for tk in tkeys:
            # who was on each roster that week, where each played (or sat), and his points
            save('roster_%s_w%d' % (tk.split('.')[-1], w),
                 'team/%s/roster;week=%d/players/stats;type=week;week=%d' % (tk, w, w))
    if not only_weeks or only_weeks == 'extras':
        # the rest of the schedule (matchups for weeks not played yet), for the playoff odds
        for w in range(last + 1, int(st['end_week']) + 1):
            save('scoreboard_w%d' % w, 'league/%s/scoreboard;week=%d' % (K, w))
        # every position's season leaders under the league's own scoring: where a dropped or
        # drafted player actually finished. 25 a page, 4 pages a position (K and DEF: 2)
        for pos, pages in (('QB', 2), ('RB', 4), ('WR', 4), ('TE', 3), ('K', 2), ('DEF', 2)):
            for pg in range(pages):
                save('rank_%s_%d' % (pos, pg), 'league/%s/players;position=%s;sort=PTS;sort_type=season;start=%d;count=25/stats;type=season'
                     % (K, pos, pg * 25))
    print('pulled %d: league %s, %d teams, weeks %s' % (year, K, len(tkeys), list(weeks)))

if __name__ == '__main__':
    yr = int(sys.argv[1])
    wk = [int(sys.argv[sys.argv.index('--weeks') + 1])] if '--weeks' in sys.argv else 'extras' if '--extras' in sys.argv else None
    pull(yr, wk)
