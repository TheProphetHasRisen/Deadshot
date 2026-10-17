# -*- coding: utf-8 -*-
"""Manager net points (Brian, 16 Oct 2026; PLANS.md section 2). Every point a manager's lineups scored came from a
draft pick, a pickup or a trade. Against the league's average manager that season:

  draft     points that counted from players he drafted, while he kept them
  pickups   points that counted from players he picked up
  trades    points that counted from players he traded for
  lineups   his lineups against the crowd's: the same roster each week, every slot given to whoever Yahoo started
            most (crowd.py), so the call is judged with what was known that week

Draft, pickups and trades add up to his points that counted against the average, so the total squares with his
scoring (a trader who sends away his draft picks shows it as a lower draft and a higher trades figure). Trade
grading 2.0 (trade2.py) answers the other question, whether each deal helped. All four are points, so the page
adds them unweighted by default; its sliders let a reader weight them. Turned into wins at each season's points
per win.
"""
import teamfile as TF

def build(crowd):
    out = {}
    cm = (crowd or {}).get('mgrs') or {}
    for y in TF.YEARS:
        M, L = TF.season(y)
        src = {m: dict(draft=0.0, pickups=Z['pk_pts'], trades=0.0) for m, Z in M.items()}
        for d in L['draft_list']:
            if d['m'] in src: src[d['m']]['draft'] += d['counted'] or 0
        for t in L['trades_list']:
            for side in ('a', 'b'):
                m = t[side]['m']
                if m in src: src[m]['trades'] += t[side]['counted'] or 0
        avg = {k: sum(v[k] for v in src.values()) / max(1, len(src)) for k in ('draft', 'pickups', 'trades')}
        for m, Z in M.items():
            c = cm.get(m, {}).get(y) or cm.get(m, {}).get(str(y)) or {}
            out.setdefault(m, {})[y] = dict(draft=round(src[m]['draft'] - avg['draft'], 2), pickups=round(src[m]['pickups'] - avg['pickups'], 2),
                                            trades=round(src[m]['trades'] - avg['trades'], 2), lineups=round(c.get('ssNet', 0.0), 2),
                                            ppw=round(L['ppw'] or 0, 2), g=Z['g'], partial=(y == TF.LIVE))
    return out
