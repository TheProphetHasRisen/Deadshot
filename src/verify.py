# -*- coding: utf-8 -*-
"""Data integrity checks for the Deadshot dataset.

Runs the invariants from HANDOFF section 3 against data.py + weekly*.py and
reports every violation. Exits non-zero if anything fails, so it can gate a
build or an automated Yahoo fetch:

    python3 verify.py            # check the committed dataset
    python3 verify.py --quiet    # only print failures

These are the checks that caught a real 2022 transcription error (five wrong
records). Any future fetcher must pass this before it is allowed to write.
"""
import sys, os, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D

CENT = 0.005          # "equal to the cent" tolerance
FAILS = []
CHECKS = 0


def check(ok, label, detail=""):
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append((label, detail))
    return ok


def weekly_sources():
    """Every season that has a week-by-week log, as {year: (games, byes)}."""
    import weekly, weekly2024, weekly2023, weekly2022, weekly2021
    return {
        2025: (weekly.W2025, weekly.BYES2025),
        2024: (weekly2024.W2024, weekly2024.BYES2024),
        2023: (weekly2023.W2023, weekly2023.BYES2023),
        2022: (weekly2022.W2022, weekly2022.BYES2022),
        2021: (weekly2021.W2021, weekly2021.BYES2021),
    }


def weekly_modules():
    """The weekly modules themselves, for checks that need more than games+byes.

    weekly_sources() deliberately returns only (games, byes); reaching for a module
    attribute on that tuple silently yields nothing, which once made three shape
    checks below into no-ops that always passed.
    """
    import weekly, weekly2024, weekly2023, weekly2022, weekly2021
    return {2025: weekly, 2024: weekly2024, 2023: weekly2023,
            2022: weekly2022, 2021: weekly2021}


# ---------------------------------------------------------------- invariants
def inv_pf_equals_pa():
    """League-wide points for must equal points against, to the cent.

    Every point scored is a point scored against somebody. If these drift, a
    score was transcribed wrong somewhere in that season.
    """
    for y, rows in sorted(D.STANDINGS.items()):
        pf = sum(r[5] for r in rows)
        pa = sum(r[6] for r in rows)
        check(abs(pf - pa) < CENT, f"{y}: league PF must equal PA",
              f"PF {pf:.2f} vs PA {pa:.2f} (off by {pf - pa:+.2f})")


def inv_games_played():
    """Each team's W + L + T must equal that season's regular-season length."""
    for y, rows in sorted(D.STANDINGS.items()):
        length = D.SEASON_META[y][1]
        for (rank, team, w, l, t, pf, pa, mv) in rows:
            check(w + l + t == length, f"{y}: {team} games played",
                  f"{w}-{l}-{t} = {w + l + t} games, season is {length}")


def inv_wins_equal_losses():
    """Total wins must equal total losses across the league."""
    for y, rows in sorted(D.STANDINGS.items()):
        w = sum(r[2] for r in rows)
        l = sum(r[3] for r in rows)
        check(w == l, f"{y}: total W must equal total L", f"{w} W vs {l} L")


def inv_standings_rows():
    """Team count must match SEASON_META, and no duplicate team names."""
    for y, rows in sorted(D.STANDINGS.items()):
        teams = D.SEASON_META[y][0]
        check(len(rows) == teams, f"{y}: team count",
              f"{len(rows)} rows, SEASON_META says {teams}")
        names = [r[1] for r in rows]
        dupes = [n for n, c in collections.Counter(names).items() if c > 1]
        check(not dupes, f"{y}: duplicate team names", ", ".join(dupes))


def inv_managers_cover_standings():
    """Every team in the standings must have a manager, and vice versa."""
    for y, rows in sorted(D.STANDINGS.items()):
        standing = {r[1] for r in rows}
        managed = set(D.MANAGERS.get(y, {}))
        missing = standing - managed
        extra = managed - standing
        check(not missing, f"{y}: teams with no manager", ", ".join(sorted(missing)))
        check(not extra, f"{y}: managers with no team", ", ".join(sorted(extra)))


def inv_final_place():
    """FINAL_PLACE must list exactly the teams that played that season."""
    for y, rows in sorted(D.STANDINGS.items()):
        standing = {r[1] for r in rows}
        final = D.FINAL_PLACE.get(y, [])
        check(len(final) == len(rows), f"{y}: FINAL_PLACE length",
              f"{len(final)} entries for {len(rows)} teams")
        check(set(final) == standing, f"{y}: FINAL_PLACE names",
              f"only in FINAL_PLACE: {sorted(set(final) - standing)} | "
              f"only in STANDINGS: {sorted(standing - set(final))}")


def inv_weekly_reconciles():
    """The week-by-week log must reproduce STANDINGS exactly.

    This is the strongest check in the file: it rebuilds each team's record and
    points from the individual game results and compares against the season
    totals that were transcribed separately.
    """
    for y, (games, byes) in sorted(weekly_sources().items()):
        rows = {r[1]: r for r in D.STANDINGS[y]}
        w = collections.Counter()
        l = collections.Counter()
        t = collections.Counter()
        pf = collections.Counter()
        pa = collections.Counter()
        for (wk, ta, aa, pja, tb, ab, pjb, br) in games:
            if br:                       # postseason, not in the regular-season record
                continue
            pf[ta] += aa; pa[ta] += ab
            pf[tb] += ab; pa[tb] += aa
            if aa > ab:   w[ta] += 1; l[tb] += 1
            elif ab > aa: w[tb] += 1; l[ta] += 1
            else:         t[ta] += 1; t[tb] += 1

        for team, r in sorted(rows.items()):
            got = (w[team], l[team], t[team])
            want = (r[2], r[3], r[4])
            check(got == want, f"{y}: {team} record from game log",
                  f"log says {got[0]}-{got[1]}-{got[2]}, standings say {want[0]}-{want[1]}-{want[2]}")
            check(abs(pf[team] - r[5]) < CENT, f"{y}: {team} points for from game log",
                  f"log {pf[team]:.2f} vs standings {r[5]:.2f} (off by {pf[team] - r[5]:+.2f})")
            check(abs(pa[team] - r[6]) < CENT, f"{y}: {team} points against from game log",
                  f"log {pa[team]:.2f} vs standings {r[6]:.2f} (off by {pa[team] - r[6]:+.2f})")


def inv_weekly_shape():
    """Every regular-season week must have the same number of games, and the
    team names in the log must match the standings for that year."""
    for y, (games, byes) in sorted(weekly_sources().items()):
        names = {r[1] for r in D.STANDINGS[y]}
        seen = {g[1] for g in games} | {g[4] for g in games} | {b[1] for b in byes}
        unknown = seen - names
        check(not unknown, f"{y}: game log names not in standings", ", ".join(sorted(unknown)))

        per_week = collections.Counter(g[0] for g in games if g[7] == '')
        expect = len(names) // 2
        for wk, n in sorted(per_week.items()):
            check(n == expect, f"{y} week {wk}: game count",
                  f"{n} games for {len(names)} teams, expected {expect}")

        weeks = sorted(per_week)
        length = D.SEASON_META[y][1]
        check(len(weeks) == length, f"{y}: regular-season weeks in log",
              f"{len(weeks)} weeks logged, SEASON_META says {length}")


def inv_playoff_games():
    """Playoff results must reference real teams from that season."""
    for (y, wk, rnd, ta, pa_, tb, pb, void) in D.PLAYOFF_GAMES:
        names = {r[1] for r in D.STANDINGS[y]}
        check(ta in names, f"{y} {rnd}: unknown team", ta)
        check(tb in names, f"{y} {rnd}: unknown team", tb)


def inv_playoffs_match_log():
    """The postseason is recorded twice -- in PLAYOFF_GAMES and again in the weekly
    log -- and nothing used to check the two agreed.

    Two rules. Every game in the playoff table must exist in that season's weekly
    log, and wherever both record the same matchup the scores must be identical.
    The weekly log legitimately holds more: the consolation ladder ('S' bracket)
    is logged but deliberately kept out of the playoff table.
    """
    for y, (games, byes) in sorted(weekly_sources().items()):
        log = {}
        for (wk, ta, aa, pja, tb, ab, pjb, br) in games:
            if br:
                log[(wk, frozenset((ta, tb)))] = {(ta, round(aa, 2)), (tb, round(ab, 2))}
        for (yy, wk, rnd, ta, pa_, tb, pb, void) in D.PLAYOFF_GAMES:
            if yy != y:
                continue
            key = (wk, frozenset((ta, tb)))
            if not check(key in log, f"{y} {rnd}: not in the week-by-week log",
                         f"week {wk}, {ta} vs {tb}"):
                continue
            want = {(ta, round(pa_, 2)), (tb, round(pb, 2))}
            check(log[key] == want, f"{y} {rnd}: score disagrees with the game log",
                  f"log {sorted(log[key])} vs playoff table {sorted(want)}")


# ---------------------------------------------------------------------- main
# ---------------------------------------------------------------------------
# Shape checks.
#
# Everything above tests whether the numbers agree with each other. These test
# whether the data is the right SHAPE: correct types, sane ranges, no blanks.
# The arithmetic checks assume they can do arithmetic; a string where a float
# belongs would blow up with a TypeError rather than a clear message, and a
# silently negative or absurd value would pass every sum while still being wrong.
#
# This matters most for the Yahoo fetcher. A human transcribing a screenshot
# makes plausible-looking mistakes that the arithmetic catches. A parser reading
# someone else's JSON makes structural ones: a null where a number should be, a
# string "12" instead of 12, a score of 0 for a week that was never played.

def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def inv_vs_buckets_balance():
    """The 'vs winners' / 'vs the rest' split has to add up.

    Sorting each side of a game by how good the OPPONENT was is easy to get subtly
    wrong. The identity: wins-vs-winners minus losses-to-the-rest must equal the
    number of winner-vs-winner games minus loser-vs-loser games, because those are
    the only games that put both sides in the same bucket.

    This also documents why nearly every manager is under .500 in that column: a
    mixed game puts the stronger team in 'vs the rest' and the weaker one in
    'vs winners', so the winners bucket is loaded with games played by losing teams.
    That is expected and is not a data error.
    """
    winner = {}
    for y, rows in D.STANDINGS.items():
        for (rk, t, W, L, T, pf, pa, mv) in rows:
            winner[(y, t)] = W > L

    ww = nn = 0
    vs_win_w = vs_win_l = vs_sub_w = vs_sub_l = 0

    def tally(y, ta, pa_, tb, pb):
        nonlocal ww, nn, vs_win_w, vs_win_l, vs_sub_w, vs_sub_l
        if pa_ == pb:
            return
        if (y, ta) not in winner or (y, tb) not in winner:
            return
        a_, b_ = winner[(y, ta)], winner[(y, tb)]
        if a_ and b_:
            ww += 1
        elif not a_ and not b_:
            nn += 1
        for me, mine, opp, theirs in ((ta, pa_, tb, pb), (tb, pb, ta, pa_)):
            strong = winner[(y, opp)]
            if mine > theirs:
                if strong: vs_win_w += 1
                else:      vs_sub_w += 1
            else:
                if strong: vs_win_l += 1
                else:      vs_sub_l += 1

    for year, mod in weekly_modules().items():
        for g in getattr(mod, f"W{year}", []):
            if len(g) == 8 and not g[7]:
                tally(year, g[1], g[2], g[4], g[5])
    for (y, wk, rnd, ta, pa_, tb, pb, void) in D.PLAYOFF_GAMES:
        if not void:
            tally(y, ta, pa_, tb, pb)

    check(vs_win_w - vs_sub_l == ww - nn,
          "vs-winners bucket does not balance",
          f"winsVsWinners {vs_win_w} - lossesToRest {vs_sub_l} = {vs_win_w - vs_sub_l}, "
          f"expected WW {ww} - NN {nn} = {ww - nn}")
    check(vs_win_l - vs_sub_w == ww - nn,
          "vs-the-rest bucket does not balance",
          f"lossesToWinners {vs_win_l} - winsVsRest {vs_sub_w} = {vs_win_l - vs_sub_w}, "
          f"expected {ww - nn}")


def inv_types_standings():
    """Every standings field is the type and range it claims to be."""
    for y, rows in D.STANDINGS.items():
        for r in rows:
            rank, team, W, L, T, pf, pa, mv = r
            tag = f"{y} {team!r}"
            check(isinstance(rank, int) and rank >= 1, f"{tag}: rank must be a positive whole number", repr(rank))
            check(isinstance(team, str) and team.strip() != "", f"{tag}: team name must be a non-empty string")
            for nm, v in (("W", W), ("L", L), ("T", T)):
                check(isinstance(v, int) and v >= 0, f"{tag}: {nm} must be a whole number, zero or more", repr(v))
            for nm, v in (("PF", pf), ("PA", pa)):
                check(_is_num(v) and v > 0, f"{tag}: {nm} must be a positive number", repr(v))
                # a full-PPR fantasy season sits far inside this range; anything outside
                # it is a decimal-point or units error, not a real result
                check(_is_num(v) and 400 <= v <= 4000, f"{tag}: {nm} is outside any plausible season total", repr(v))
            check(mv is None or (isinstance(mv, int) and 0 <= mv <= 500),
                  f"{tag}: roster moves must be a whole number or None", repr(mv))


def inv_types_meta():
    """SEASON_META describes a league that could actually exist."""
    for y, meta in D.SEASON_META.items():
        check(isinstance(y, int) and 1990 <= y <= 2100, f"SEASON_META key {y!r} is not a plausible year")
        check(isinstance(meta, tuple) and len(meta) == 4,
              f"SEASON_META[{y}] must be (teams, reg_games, playoff_spots, confirmed)", repr(meta))
        if not (isinstance(meta, tuple) and len(meta) == 4):
            continue
        teams, g, spots, confirmed = meta
        check(isinstance(teams, int) and 2 <= teams <= 32, f"SEASON_META[{y}]: team count out of range", repr(teams))
        check(isinstance(g, int) and 1 <= g <= 20, f"SEASON_META[{y}]: regular season length out of range", repr(g))
        check(isinstance(spots, int) and 1 <= spots <= teams,
              f"SEASON_META[{y}]: playoff spots must be between 1 and the team count", repr(spots))
        check(isinstance(confirmed, bool), f"SEASON_META[{y}]: confirmed flag must be True or False", repr(confirmed))


def inv_types_weekly():
    """Weekly rows are numbers, and nobody scored a negative or impossible total."""
    for year, mod in weekly_modules().items():
        games = getattr(mod, f"W{year}", [])
        for g in games:
            check(len(g) == 8, f"{year} weekly row has {len(g)} fields, expected 8", repr(g)[:90])
            if len(g) != 8:
                continue
            wk, ta, aa, pa_, tb, ab, pb, br = g
            tag = f"{year} wk{wk} {ta} vs {tb}"
            check(isinstance(wk, int) and 1 <= wk <= 20, f"{tag}: week number out of range", repr(wk))
            for nm, v in (("actual A", aa), ("projected A", pa_), ("actual B", ab), ("projected B", pb)):
                check(_is_num(v), f"{tag}: {nm} must be a number", repr(v))
                check(_is_num(v) and 0 < v < 400, f"{tag}: {nm} is outside any plausible weekly score", repr(v))
            check(br in ("", "C", "S"), f"{tag}: bracket flag must be '', 'C' or 'S'", repr(br))
            check(ta != tb, f"{tag}: a team cannot play itself")


def inv_no_duplicate_matchups():
    """The same two teams cannot appear twice in one week."""
    for year, mod in weekly_modules().items():
        seen = {}
        for g in getattr(mod, f"W{year}", []):
            if len(g) != 8:
                continue
            key = (g[0], frozenset((g[1], g[4])))
            check(key not in seen, f"{year} week {g[0]}: {g[1]} vs {g[4]} appears more than once")
            seen[key] = True


def inv_trades_shape():
    """Trades name two different teams and move at least one player each way."""
    for year, mod in weekly_modules().items():
        for t in getattr(mod, f"TRADES{year}", []):
            check(len(t) == 5, f"{year} trade row has {len(t)} fields, expected 5", repr(t)[:80])
            if len(t) != 5:
                continue
            date, pa_, ta, pb, tb = t
            tag = f"{year} trade {date!r}"
            check(isinstance(date, str) and date.strip() != "", f"{tag}: needs a date")
            check(ta != tb, f"{tag}: both sides are the same team ({ta!r})")
            for nm, side in (("first", pa_), ("second", pb)):
                check(isinstance(side, list) and len(side) > 0, f"{tag}: {nm} side has no players", repr(side)[:60])
                check(all(isinstance(x, str) and x.strip() for x in side),
                      f"{tag}: {nm} side has a blank or non-text player name", repr(side)[:60])
            known = {r[1] for r in D.STANDINGS.get(year, [])}
            for team in (ta, tb):
                check(team in known, f"{tag}: {team!r} did not play in {year}")


def main():
    quiet = "--quiet" in sys.argv
    for fn in (inv_pf_equals_pa, inv_games_played, inv_wins_equal_losses,
               inv_standings_rows, inv_managers_cover_standings, inv_final_place,
               inv_weekly_reconciles, inv_weekly_shape, inv_playoff_games,
               inv_playoffs_match_log,
               inv_types_standings, inv_types_meta, inv_types_weekly,
               inv_no_duplicate_matchups, inv_trades_shape, inv_vs_buckets_balance):
        fn()

    if FAILS:
        print(f"FAILED — {len(FAILS)} of {CHECKS} checks\n")
        for label, detail in FAILS:
            print(f"  {label}")
            if detail:
                print(f"      {detail}")
        print("\nNothing should be written to the site with these outstanding.")
        return 1

    if not quiet:
        print(f"OK — all {CHECKS} checks passed "
              f"({len(D.STANDINGS)} seasons, {len(weekly_sources())} with week-by-week logs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
