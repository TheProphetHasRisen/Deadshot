# -*- coding: utf-8 -*-
"""Our weekly game predictions beside Yahoo's, saved every update from week 6 of 2026 (USER, 17 Oct 2026), so at
the end of the season both can be scored on the same games.

pred_log.json: {week: {asOf, late, games: [{ta, tb, ours: our chance ta wins, oursA, oursB: our expected scores,
yahoo: Yahoo's chance ta wins, yahooA, yahooB: Yahoo's projected scores, result: 1/0 once played, aa, ab}]}}

A week's predictions are rewritten on each update until its first game kicks off, so what is kept is the last
word before the games. A week first seen after kickoff (week 6 of 2026, when this started) is kept as it stood
then and marked late. Results are filled in once the week is final. Committed by the scheduled job.
"""
import json, os, datetime
import yahoo_parse as P
import teamfile as TF

F = 'pred_log.json'

def update(FC, y=None):
    y = y or TF.LIVE
    log = json.load(open(F)) if os.path.exists(F) else {}
    G = P.games(y)
    by_wk = {}
    for g in G: by_wk.setdefault(g['wk'], []).append(g)
    # results for weeks already logged
    for wk, e in log.items():
        gs = by_wk.get(int(wk), [])
        if gs and all(g['status'] == 'postevent' for g in gs):
            for x in e['games']:
                g = next((g for g in gs if {g['ta'], g['tb']} == {x['ta'], x['tb']}), None)
                if not g: continue
                a, b = (g['aa'], g['ab']) if g['ta'] == x['ta'] else (g['ab'], g['aa'])
                x['aa'], x['ab'], x['result'] = a, b, (1 if a > b else 0 if a < b else 0.5)
    # this week's predictions, until kickoff
    nxt = FC and FC.get('next')
    if nxt:
        gs = by_wk.get(nxt, [])
        started = any(g['status'] != 'preevent' for g in gs)
        if gs and (not started or str(nxt) not in log):
            out = []
            for f in [g for g in FC['games'] if g['wk'] == nxt and g.get('pA') is not None]:
                g = next((g for g in gs if {g['ta'], g['tb']} == {f['ta'], f['tb']}), None)
                if not g: continue
                same = g['ta'] == f['ta']
                out.append(dict(ta=f['ta'], tb=f['tb'], ours=f['pA'], oursA=f['muA'], oursB=f['muB'],
                                yahoo=round(g['wpa'] if same else g['wpb'], 4) if (g['wpa'] if same else g['wpb']) is not None else None, yahooA=g['pa'] if same else g['pb'], yahooB=g['pb'] if same else g['pa']))
            if out:
                log[str(nxt)] = dict(asOf=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%MZ'), late=started, games=out)
    json.dump(log, open(F, 'w'), indent=0, sort_keys=True)
    return log

def score(log):
    """Brier and correct picks for both, over every finished, logged game"""
    rows = [x for e in log.values() for x in e['games'] if x.get('result') is not None and x.get('yahoo') is not None]
    if not rows: return None
    br = lambda k: sum((x[k] - x['result']) ** 2 for x in rows) / len(rows)
    hit = lambda k: sum(1 for x in rows if (x[k] > 0.5) == (x['result'] == 1)) / len(rows)
    return dict(n=len(rows), ours=round(br('ours'), 4), yahoo=round(br('yahoo'), 4), oursHit=round(hit('ours'), 3), yahooHit=round(hit('yahoo'), 3))
