# -*- coding: utf-8 -*-
"""Renders league data back into data.py / weekly*.py source format.

This is the half of the Yahoo pipeline that does not touch Yahoo. Whatever
fetches a season -- the API later, a hand-built dict today -- hands its result
here, and this module writes files in exactly the format export.py already
reads, so nothing downstream changes.

Two hard rules are enforced here rather than left to the caller:

  * A season that is already recorded cannot be modified unless it is named as
    the live season. Live 2026 data can never overwrite finished history.
  * Nothing is written unless the whole result parses and passes verify.py.
    A failed write leaves every file exactly as it was.

Run `python3 test_writer.py` to check it.
"""
import io, os, re, sys, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


class FrozenSeason(Exception):
    """Raised when something tries to rewrite a finished season."""


class VerificationFailed(Exception):
    """Raised when a proposed write would not survive verify.py."""


# ------------------------------------------------------------------ literals
def num(x):
    """Every score in these files is written to exactly two decimal places."""
    return f"{x:.2f}"


def lit(v):
    """A Python literal matching the style already used in the data files."""
    if v is None:
        return "None"
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return num(v)
    if isinstance(v, str):
        return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if isinstance(v, (list, tuple)):
        inner = ",".join(lit(x) for x in v)
        return "[" + inner + "]" if isinstance(v, list) else "(" + inner + ")"
    raise TypeError(f"cannot write {type(v).__name__} into a data file")


# -------------------------------------------------------------- weekly files
def render_weekly(year, games, byes, trades, note=None):
    """A complete weekly<year>.py.

    games  : (week, teamA, actualA, projA, teamB, actualB, projB, bracket)
    byes   : (week, team, actual, proj, bracket)
    trades : (date, [players->teamA], teamA, [players->teamB], teamB)
    """
    out = ["# -*- coding: utf-8 -*-",
           f"# {year} season, every matchup. (week, teamA, actualA, projA, teamB, actualB, projB, bracket)",
           "# bracket: '' = regular season, 'C' = championship, 'S' = consolation"]
    out.append(f"# {note}" if note else f"# Written by writer.py -- do not edit by hand.")
    out.append(f"W{year} = [")
    prev_post = False
    for g in games:
        wk, ta, aa, pja, tb, ab, pjb, br = g
        if br and not prev_post:
            out.append("# --- postseason ---")
            prev_post = True
        out.append(f"({wk},{lit(ta)},{num(aa)},{num(pja)},{lit(tb)},{num(ab)},{num(pjb)},{lit(br)}),")
    out.append("]")

    if byes:
        out.append("# byes -- a bye week still scores (week, team, actual, proj, bracket)")
        body = ",".join(f"({b[0]},{lit(b[1])},{num(b[2])},{num(b[3])},{lit(b[4])})" for b in byes)
        out.append(f"BYES{year}=[{body}]")
    else:
        out.append(f"BYES{year}=[]")

    out.append(f"# {year} trades, newest first. (date, [players->teamA], teamA, [players->teamB], teamB)")
    if trades:
        out.append(f"TRADES{year}=[")
        for (d, pa_, ta, pb_, tb) in trades:
            out.append(f" ({lit(d)},{lit(list(pa_))},{lit(ta)},{lit(list(pb_))},{lit(tb)}),")
        out.append("]")
    else:
        out.append(f"TRADES{year}=[]")
    return "\n".join(out) + "\n"


# ------------------------------------------------------- data.py block bodies
def render_standings(year, rows):
    """rows: (rank, team, W, L, T, PF, PA, moves)"""
    lines = [f"{year}: ["]
    for (rank, team, w, l, t, pf, pa, mv) in rows:
        lines.append(f" ({rank},{lit(team)},{w},{l},{t},{num(pf)},{num(pa)},{lit(mv)}),")
    lines.append("],")
    return lines


def render_final_place(year, order):
    return [f"{year}: [" + ",".join(lit(t) for t in order) + "],"]


def render_managers(year, mapping):
    body = ",".join(f"{lit(t)}:{lit(m)}" for t, m in mapping.items())
    return [f"{year}: {{{body}}},"]


def render_meta(year, meta):
    teams, reg, spots, confirmed = meta
    return [f"    {year}: ({teams}, {reg}, {spots}, {lit(confirmed)}),"]


def render_playoffs(year, games):
    """games: (week, round, teamA, ptsA, teamB, ptsB, void)"""
    return [f" ({year},{wk},{lit(rnd)},{lit(ta)},{num(pa_)},{lit(tb)},{num(pb)},{lit(void)}),"
            for (wk, rnd, ta, pa_, tb, pb, void) in games]


# --------------------------------------------------------- data.py insertion
def _block_bounds(lines, name, opener, closer):
    """Line range of a top-level `NAME = <opener> ... <closer>` block."""
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith(f"{name} = {opener}") or ln.startswith(f"{name}={opener}"):
            start = i
            break
    if start is None:
        raise KeyError(f"{name} not found in data.py")
    for j in range(start + 1, len(lines)):
        if lines[j].rstrip() == closer:
            return start, j
    raise KeyError(f"end of {name} not found")


def _year_span(lines, lo, hi, year):
    """Line range of one year's entry inside a block, or None if absent."""
    pat = re.compile(rf"^\s*{year}\s*:")
    for i in range(lo + 1, hi):
        if pat.match(lines[i]):
            j = i + 1
            while j < hi and not re.match(r"^\s*\d{4}\s*:", lines[j]):
                j += 1
            return i, j
    return None


def upsert_block(text, name, year, rendered, opener="{", closer="}"):
    """Replace or insert one year inside a dict-style block, keeping year order."""
    lines = text.split("\n")
    lo, hi = _block_bounds(lines, name, opener, closer)
    span = _year_span(lines, lo, hi, year)
    if span:
        i, j = span
        return "\n".join(lines[:i] + rendered + lines[j:])
    at = hi
    for i in range(lo + 1, hi):
        m = re.match(r"^\s*(\d{4})\s*:", lines[i])
        if m and int(m.group(1)) > year:
            at = i
            break
    return "\n".join(lines[:at] + rendered + lines[at:])


def upsert_playoffs(text, year, rendered):
    """PLAYOFF_GAMES is a flat list grouped by year with blank lines between."""
    lines = text.split("\n")
    lo, hi = _block_bounds(lines, "PLAYOFF_GAMES", "[", "]")
    keep = [ln for ln in lines[lo + 1:hi]
            if not re.match(rf"^\s*\({year},", ln)]
    while keep and not keep[-1].strip():
        keep.pop()
    body = keep + ([""] if keep else []) + rendered
    return "\n".join(lines[:lo + 1] + body + lines[hi:])


# ------------------------------------------------------------------- guards
def recorded_seasons(data_py=None):
    path = data_py or os.path.join(HERE, "data.py")
    text = io.open(path, encoding="utf-8").read()
    lines = text.split("\n")
    lo, hi = _block_bounds(lines, "STANDINGS", "{", "}")
    return {int(m.group(1)) for m in
            (re.match(r"^\s*(\d{4})\s*:", ln) for ln in lines[lo + 1:hi]) if m}


def assert_writable(year, live_year, data_py=None):
    """A finished season is frozen. Only the live season may be rewritten."""
    if year == live_year:
        return
    if year in recorded_seasons(data_py):
        raise FrozenSeason(
            f"{year} is already recorded and is not the live season "
            f"({live_year}). Finished seasons cannot be overwritten.")


def verify_in(directory):
    """Run verify.py against a directory. Returns (ok, output)."""
    r = subprocess.run([sys.executable, "verify.py"], cwd=directory,
                       capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def commit_season(year, live_year, standings=None, meta=None, managers=None,
                  final_place=None, playoffs=None, weekly=None, root=None):
    """Write one season, but only if the result passes verify.py.

    Everything is staged in a scratch copy first. If verification fails,
    nothing in the real directory is touched and the checker's output is
    raised so the failure is loud rather than silent.
    """
    root = root or HERE
    assert_writable(year, live_year, os.path.join(root, "data.py"))

    with tempfile.TemporaryDirectory() as tmp:
        for f in os.listdir(root):
            if f.endswith(".py"):
                io.open(os.path.join(tmp, f), "w", encoding="utf-8").write(
                    io.open(os.path.join(root, f), encoding="utf-8").read())

        dp = os.path.join(tmp, "data.py")
        text = io.open(dp, encoding="utf-8").read()
        if meta is not None:
            text = upsert_block(text, "SEASON_META", year, render_meta(year, meta))
        if standings is not None:
            text = upsert_block(text, "STANDINGS", year, render_standings(year, standings))
        if final_place is not None:
            text = upsert_block(text, "FINAL_PLACE", year, render_final_place(year, final_place))
        if managers is not None:
            text = upsert_block(text, "MANAGERS", year, render_managers(year, managers))
        if playoffs is not None:
            text = upsert_playoffs(text, year, render_playoffs(year, playoffs))
        io.open(dp, "w", encoding="utf-8").write(text)

        wname = "weekly.py" if year == 2025 else f"weekly{year}.py"
        if weekly is not None:
            games, byes, trades = weekly
            io.open(os.path.join(tmp, wname), "w", encoding="utf-8").write(
                render_weekly(year, games, byes, trades))

        ok, out = verify_in(tmp)
        if not ok:
            raise VerificationFailed(
                f"{year} was not written -- the data failed its own checks:\n\n{out}")

        written = ["data.py"]
        io.open(os.path.join(root, "data.py"), "w", encoding="utf-8").write(text)
        if weekly is not None:
            io.open(os.path.join(root, wname), "w", encoding="utf-8").write(
                io.open(os.path.join(tmp, wname), encoding="utf-8").read())
            written.append(wname)
        return written
