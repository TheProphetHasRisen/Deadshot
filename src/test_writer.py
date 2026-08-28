# -*- coding: utf-8 -*-
"""Proves writer.py cannot silently corrupt or lose data.

Run: python3 test_writer.py

The important test is the round trip. Every existing season is rendered back
into source, re-imported, and compared value by value against what it came
from. If a single score or team name changed, that test fails.
"""
import io, os, sys, shutil, tempfile, importlib.util, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import writer as W
import data as D

HERE = os.path.dirname(os.path.abspath(__file__))
PASS, FAIL = [], []


def ok(cond, label, detail=""):
    (PASS if cond else FAIL).append((label, detail))
    print(("  ok    " if cond else "  FAIL  ") + label)
    if not cond and detail:
        print("          " + str(detail)[:400])


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


SRC = {2025: "weekly", 2024: "weekly2024", 2023: "weekly2023",
       2022: "weekly2022", 2021: "weekly2021"}


def test_weekly_roundtrip():
    print("\nweekly files -- render, re-import, compare every value")
    for year, mod in sorted(SRC.items()):
        m = __import__(mod)
        games = getattr(m, f"W{year}")
        byes = getattr(m, f"BYES{year}")
        trades = getattr(m, f"TRADES{year}")
        text = W.render_weekly(year, games, byes, trades)
        with tempfile.TemporaryDirectory() as t:
            p = os.path.join(t, f"rt{year}.py")
            io.open(p, "w", encoding="utf-8").write(text)
            try:
                r = load(p, f"rt{year}")
            except Exception as e:
                ok(False, f"{year} rendered file is valid Python", e)
                continue
            g2 = getattr(r, f"W{year}")
            b2 = getattr(r, f"BYES{year}")
            t2 = getattr(r, f"TRADES{year}")
            ok(list(g2) == [tuple(x) for x in games],
               f"{year} matchups identical after round trip",
               f"{len(games)} in, {len(g2)} out")
            ok([tuple(x) for x in b2] == [tuple(x) for x in byes],
               f"{year} byes identical after round trip")
            ok([tuple(x) for x in t2] == [tuple(x) for x in trades],
               f"{year} trades identical after round trip")


def test_no_float_drift():
    print("\nno rounding drift -- scores survive as exact cents")
    for year, mod in sorted(SRC.items()):
        m = __import__(mod)
        games = getattr(m, f"W{year}")
        bad = []
        for g in games:
            for v in (g[2], g[3], g[5], g[6]):
                if abs(float(W.num(v)) - v) > 1e-9:
                    bad.append((g[0], v))
        ok(not bad, f"{year} every score renders exactly", bad[:3])


def test_freeze_guard():
    print("\nfinished seasons are frozen")
    try:
        W.assert_writable(2024, live_year=2026)
        ok(False, "rewriting a finished season is refused")
    except W.FrozenSeason as e:
        ok(True, "rewriting a finished season is refused")
    try:
        W.assert_writable(2026, live_year=2026)
        ok(True, "the live season stays writable")
    except W.FrozenSeason as e:
        ok(False, "the live season stays writable", e)
    ok(W.recorded_seasons() == set(D.STANDINGS),
       "recorded seasons detected correctly",
       sorted(W.recorded_seasons()))


def _synthetic_2026():
    """A complete, internally consistent fake season for end-to-end testing."""
    teams = [f"Test Team {i}" for i in range(1, 11)]
    mgrs = D.MANAGER_ORDER[:10]
    weeks = 14
    games, rec, pf, pa = [], {t: [0, 0, 0] for t in teams}, {t: 0.0 for t in teams}, {t: 0.0 for t in teams}
    for wk in range(1, weeks + 1):
        rot = teams[:1] + teams[1:][(wk - 1) % 9:] + teams[1:][:(wk - 1) % 9]
        for i in range(5):
            ta, tb = rot[i], rot[9 - i]
            a = 100.0 + wk + i * 2.5
            b = 100.0 + wk + i * 2.5 + (1.5 if (wk + i) % 2 else -1.5)
            games.append((wk, ta, a, a + 5, tb, b, b + 5, ''))
            pf[ta] += a; pa[ta] += b; pf[tb] += b; pa[tb] += a
            if a > b: rec[ta][0] += 1; rec[tb][1] += 1
            else:     rec[tb][0] += 1; rec[ta][1] += 1
    order = sorted(teams, key=lambda t: (-rec[t][0], -pf[t]))
    standings = [(i + 1, t, rec[t][0], rec[t][1], rec[t][2],
                  round(pf[t], 2), round(pa[t], 2), None) for i, t in enumerate(order)]
    return dict(
        standings=standings,
        meta=(10, weeks, 6, True),
        managers={t: m for t, m in zip(teams, mgrs)},
        final_place=order,
        playoffs=[],
        weekly=(games, [], []),
    )


def test_end_to_end():
    print("\nend to end -- write a new season, then run the real checker on it")
    with tempfile.TemporaryDirectory() as t:
        for f in os.listdir(HERE):
            if f.endswith(".py"):
                shutil.copy(os.path.join(HERE, f), os.path.join(t, f))
        s = _synthetic_2026()
        try:
            written = W.commit_season(2026, live_year=2026, root=t, **s)
            ok(True, "a valid new season is written", ", ".join(written))
        except Exception as e:
            ok(False, "a valid new season is written", e)
            return
        good, out = W.verify_in(t)
        ok(good, "the written season passes verify.py", out[:300])
        r = subprocess.run([sys.executable, "export.py"], cwd=t,
                           capture_output=True, text=True)
        ok(r.returncode == 0, "the site's data step still runs on it",
           (r.stdout + r.stderr)[-300:])


def test_bad_data_rejected():
    print("\nbad data is refused and nothing is written")
    with tempfile.TemporaryDirectory() as t:
        for f in os.listdir(HERE):
            if f.endswith(".py"):
                shutil.copy(os.path.join(HERE, f), os.path.join(t, f))
        before = io.open(os.path.join(t, "data.py"), encoding="utf-8").read()
        s = _synthetic_2026()
        # break it: one team credited a win that never happened
        r0 = list(s["standings"][0])
        r0[2] += 1
        s["standings"][0] = tuple(r0)
        try:
            W.commit_season(2026, live_year=2026, root=t, **s)
            ok(False, "a broken season is refused")
        except W.VerificationFailed as e:
            ok(True, "a broken season is refused")
            ok("total W must equal total L" in str(e) or "games played" in str(e),
               "the refusal says what was wrong", str(e)[:200])
        after = io.open(os.path.join(t, "data.py"), encoding="utf-8").read()
        ok(before == after, "nothing was written when it failed")


if __name__ == "__main__":
    test_weekly_roundtrip()
    test_no_float_drift()
    test_freeze_guard()
    test_end_to_end()
    test_bad_data_rejected()
    print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)
