# -*- coding: utf-8 -*-
"""Deadshot's scoring, applied to Sleeper's public weekly stats. One copy, used by draft_points.py
and sleeper_season.py. The league's 35 scoring settings are the same in every season Yahoo reaches
(2021-2026, checked 15 Oct 2026), so one function scores them all. See league_rules_2026.md."""
g = lambda s, k: float(s.get(k) or 0)

def pa_pts(pa):
    return 10 if pa == 0 else 7 if pa <= 6 else 4 if pa <= 13 else 2 if pa <= 20 else 0 if pa <= 27 else -1 if pa <= 34 else -4

def score(s, pos):
    if pos == 'DEF':
        return (g(s, 'sack') + 2 * g(s, 'int') + 2 * g(s, 'fum_rec') + 6 * (g(s, 'def_td') + g(s, 'def_st_td'))
                + 3 * g(s, 'safe') + 2.5 * g(s, 'blk_kick') + g(s, 'def_4_and_stop') + 0.5 * g(s, 'def_3_and_out')
                + (pa_pts(g(s, 'pts_allow')) if 'pts_allow' in s else 0))
    if pos == 'K':
        fifty = g(s, 'fgm_50p') if 'fgm_50p' in s else g(s, 'fgm_50_59') + g(s, 'fgm_60p')
        return (3 * (g(s, 'fgm_0_19') + g(s, 'fgm_20_29') + g(s, 'fgm_30_39')) + 4 * g(s, 'fgm_40_49') + 5 * fifty + g(s, 'xpm'))
    return (g(s, 'pass_yd') / 25 + 4 * g(s, 'pass_td') - g(s, 'pass_int') + g(s, 'rush_yd') / 10 + 6 * g(s, 'rush_td')
            + g(s, 'rec') + g(s, 'rec_yd') / 10 + 6 * g(s, 'rec_td') - 2 * g(s, 'fum_lost')
            + 2 * (g(s, 'pass_2pt') + g(s, 'rush_2pt') + g(s, 'rec_2pt'))
            + 6 * (g(s, 'kr_td') + g(s, 'pr_td') + g(s, 'st_td') + g(s, 'fum_rec_td')))
