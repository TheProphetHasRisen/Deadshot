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
def main():
    quiet = "--quiet" in sys.argv
    for fn in (inv_pf_equals_pa, inv_games_played, inv_wins_equal_losses,
               inv_standings_rows, inv_managers_cover_standings, inv_final_place,
               inv_weekly_reconciles, inv_weekly_shape, inv_playoff_games,
               inv_playoffs_match_log):
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
