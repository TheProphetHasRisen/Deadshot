# -*- coding: utf-8 -*-
"""Check the hand-typed 2026 data against itself, and recover week 5.

    python3 check_2026.py

Week 5 is not in the screenshots. Each team's week-5 score is its standings PF minus its
weeks 1-4 points; its opponent's is PA minus weeks 1-4 PA. Pairing whose week-5 PF equals
whose week-5 PA recovers the matchups. Then everything has to reconcile: W-L, PF, PA, the
streaks, and both drafts must be 150 unique picks, 15 per team.
"""
import sys
from season2026 import W2026, STANDINGS2026_WK5 as ST, DRAFT2026, DRAFT2025, TRADES2026

fail = []
teams = list(ST)
pf = {t: 0.0 for t in teams}; pa = {t: 0.0 for t in teams}; res = {t: [] for t in teams}
for wk, a, sa, _, b, sb, _, _ in W2026:
    pf[a] += sa; pa[a] += sb; pf[b] += sb; pa[b] += sa
    res[a].append('W' if sa > sb else 'L'); res[b].append('W' if sb > sa else 'L')
for wk in range(1, 5):
    seen = [t for g in W2026 if g[0] == wk for t in (g[1], g[4])]
    if sorted(seen) != sorted(teams): fail.append('week %d does not have every team once' % wk)
# week 5, recovered
w5pf = {t: round(ST[t][4] - pf[t], 2) for t in teams}
w5pa = {t: round(ST[t][5] - pa[t], 2) for t in teams}
pairs, used = [], set()
for t in teams:
    if t in used: continue
    opp = [o for o in teams if o != t and o not in used and abs(w5pf[o] - w5pa[t]) < .005 and abs(w5pa[o] - w5pf[t]) < .005]
    if len(opp) != 1: fail.append('week 5: cannot pair %s (%d candidates)' % (t, len(opp))); continue
    used |= {t, opp[0]}; pairs.append((t, w5pf[t], opp[0], w5pf[opp[0]]))
for a, sa, b, sb in pairs:
    res[a].append('W' if sa > sb else 'L'); res[b].append('W' if sb > sa else 'L')
for t in teams:
    _, w, l, tie, _, _, streak, _, _ = ST[t]
    if (res[t].count('W'), res[t].count('L')) != (w, l): fail.append('%s record %s v standings %d-%d' % (t, ''.join(res[t]), w, l))
    last = res[t][-1]; n = 0
    for r in reversed(res[t]):
        if r != last: break
        n += 1
    if last + str(n) != streak: fail.append('%s streak %s%d v standings %s' % (t, last, n, streak))
print('week 5, recovered from the standings:')
for a, sa, b, sb in pairs: print('  %-22s %7.2f  v  %7.2f  %s' % (a, sa, sb, b))
tot_pf, tot_pa = sum(v[4] for v in ST.values()), sum(v[5] for v in ST.values())
if abs(tot_pf - tot_pa) > .005: fail.append('league PF %.2f != PA %.2f' % (tot_pf, tot_pa))
for name, d in (('2026', DRAFT2026), ('2025', DRAFT2025)):
    picks = [p[0] for p in d]
    if sorted(picks) != list(range(1, 151)): fail.append(name + ' draft picks are not exactly 1-150')
    per = {}
    for p in d: per[p[1]] = per.get(p[1], 0) + 1
    if set(per.values()) != {15} or len(per) != 10: fail.append(name + ' draft: not 15 picks for each of 10 teams')
    # snake order: the same team picks n and 21-n in rounds one and two
    first = {p[1]: p[0] for p in d if p[0] <= 10}
    for p in d:
        rnd = (p[0] - 1) // 10 + 1; slot = first[p[1]]
        want = (rnd - 1) * 10 + (slot if rnd % 2 else 11 - slot)
        if p[0] != want: fail.append('%s draft: %s at %d breaks the snake (expected %d)' % (name, p[2], p[0], want))
for d, a, ga, b, gb in TRADES2026:
    if a not in teams or b not in teams: fail.append('trade team not in league: ' + a + ' / ' + b)
print('\n' + ('\n'.join('  FAIL ' + f for f in fail) if fail else 'OK - weeks 1-5 reconcile with the standings (records, streaks, PF, PA); both drafts are 150 snake picks'))
sys.exit(1 if fail else 0)
