# -*- coding: utf-8 -*-
"""Every rostered player's Yahoo injury status, saved on every update (USER, 16 Oct 2026), so the site can learn
how often a player listed Questionable or Doubtful actually plays, instead of guessing.

status_log.json: {week: {player: status}}. A week's entry is rewritten on each update until that week's games
have kicked off, so what is kept is the last status before the games (what a manager saw when setting his lineup).
Committed by the scheduled job; read later by the forecast (questionable players as a chance).
"""
import json, os
import yahoo_parse as P
import teamfile as TF

F = 'status_log.json'

def update(y=None):
    y = y or TF.LIVE
    log = json.load(open(F)) if os.path.exists(F) else {}
    G = P.games(y); started = {g['wk'] for g in G if g['status'] != 'preevent'}
    R = P.rosters(y)
    if not R: return log
    wk = max(r['wk'] for r in R)
    if wk in started and str(wk) in log: return log        # games under way: the pre-kickoff statuses are kept
    log[str(wk)] = {r['n']: r.get('status') or 'OK' for r in R if r['wk'] == wk}
    json.dump(log, open(F, 'w'), indent=0, sort_keys=True)
    return log

if __name__ == '__main__':
    l = update(); print('status log: weeks', sorted(l, key=int), 'players this week', len(l[max(l, key=int)]) if l else 0)
