# -*- coding: utf-8 -*-
"""Pin every computed number so a changed formula cannot ship silently.

    python3 test_numbers.py            check against numbers.lock.json
    python3 test_numbers.py --accept   record the current numbers as the new truth

WHY THIS EXISTS
---------------
`verify.py` proves the raw data is internally consistent: points balance, records add
up, the weekly log rebuilds the standings. It says nothing about the arithmetic layered
on top -- power index, Z-score, pythagorean wins, luck, all-play, expected titles. Nudge
one of those formulas and every existing check still passes, the page still renders, and
the site shows a wrong number with total confidence. There is no symptom. Nobody would
notice.

This is the tripwire. It records what every computed number is today and shouts if one
moves without someone meaning it.

WHAT IT ALLOWS
--------------
Adding a season must NOT fail this. So rows are keyed by (year, team) and managers by
name, and only keys present in BOTH the lock file and the current build are compared.
New keys are reported and ignored; that is what adding 2026 looks like. Changing what
2015 scored is what a broken formula looks like, and that fails.

FLOAT NOISE
-----------
HANDOFF documents that pythW / luck / expOverAvg come from `pf**K/(pf**K+pa**K)` with a
fractional exponent, so the last bit or two varies between machines. Those three get a
tolerance wide enough to swallow that (1e-6) and still catch any real formula change,
which would move them by orders of magnitude more. Everything else is compared exactly.

WHEN IT FAILS
-------------
Read what moved. If you changed the data on purpose -- corrected a score, added a season
-- run `--accept` and commit the new lock file alongside the data change, so the diff
shows both. If you did not change anything on purpose, you have found a bug.
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'site_data.json')
LOCK = os.path.join(HERE, 'numbers.lock.json')

# the three the platform's libm makes non-reproducible across machines; see HANDOFF
FUZZY = {'pythW', 'luck', 'expOverAvg'}
FUZZ_TOL = 1e-6


def numbers(o):
    """Every numeric field, booleans excluded (bool is an int in Python)."""
    return {k: v for k, v in o.items()
            if isinstance(v, (int, float)) and not isinstance(v, bool)}


def snapshot():
    """Only what is genuinely frozen.

    A team-season is history: what Iridocyclitis did in 2015 can never legitimately
    change, so every one of those is pinned.

    A manager's CAREER is not frozen while he is still playing -- adding 2026 rightly
    moves Burke's win rate, career power index and luck. Pinning those would make every
    new season fail this test, and a test that cries wolf every September gets run with
    --accept without reading it, which is worse than no test. So careers are pinned only
    for managers who have stopped playing. Ten of the twenty have, which still covers
    every career-aggregation formula -- cpi, zAvg, all-play, expected titles, the lot.
    """
    with io.open(DATA, encoding='utf-8') as f:
        d = json.load(f)
    newest = max(d['seasons'])
    rows = {'%d|%s' % (r['y'], r['team']): numbers(r) for r in d['rows']}
    mgrs = {m['name']: numbers(m) for m in d['mgrs'] if m['last'] < newest}
    return {'rows': rows, 'mgrs': mgrs}


def drifted(field, was, now):
    if was == now:
        return False
    if field in FUZZY and isinstance(was, float) and isinstance(now, float):
        return abs(was - now) > FUZZ_TOL
    return True


def main():
    cur = snapshot()
    total = sum(len(v) for sect in cur.values() for v in sect.values())

    if '--accept' in sys.argv:
        with io.open(LOCK, 'w', encoding='utf-8') as f:
            json.dump(cur, f, indent=1, sort_keys=True)
        print("Recorded %d numbers: %d team-seasons and %d retired managers' careers."
              % (total, len(cur['rows']), len(cur['mgrs'])))
        print("Commit numbers.lock.json together with whatever changed them.")
        return 0

    if not os.path.exists(LOCK):
        print("No numbers.lock.json yet. Create it with:\n  python3 test_numbers.py --accept")
        return 1
    with io.open(LOCK, encoding='utf-8') as f:
        old = json.load(f)

    moved, added, gone, newfields = [], [], [], []
    for sect in ('rows', 'mgrs'):
        for key, fields in cur[sect].items():
            if key not in old[sect]:
                added.append('%s %s' % (sect, key))
                continue
            was = old[sect][key]
            for field, now in fields.items():
                if field not in was:
                    newfields.append('%s.%s' % (sect, field))
                elif drifted(field, was[field], now):
                    moved.append((sect, key, field, was[field], now))
        for key in old[sect]:
            if key not in cur[sect]:
                gone.append('%s %s' % (sect, key))

    for label, items in (('new (fine, this is what adding a season looks like)', added),
                         ('new fields (fine)', sorted(set(newfields)))):
        if items:
            print("%d %s: %s%s" % (len(items), label, ', '.join(items[:6]),
                                   ' ...' if len(items) > 6 else ''))

    if gone:
        print("\n%d REMOVED -- a team-season or manager the site used to have is gone:"
              % len(gone))
        for g in gone[:10]:
            print("   " + g)

    if moved:
        print("\n%d NUMBER(S) CHANGED. Nothing in the raw data checks would catch this.\n"
              % len(moved))
        for sect, key, field, was, now in moved[:25]:
            print("   %-28s %-12s %r -> %r" % (key, field, was, now))
        if len(moved) > 25:
            print("   ... and %d more" % (len(moved) - 25))
        print("\nIf you meant to change this (corrected a score, reworked a formula):")
        print("  python3 test_numbers.py --accept   and commit the lock file with it.")
        print("If you did not, a formula has been broken.")

    if moved or gone:
        return 1
    print("OK - all %d computed numbers unchanged (%d team-seasons, %d retired careers)"
          % (total, len(cur['rows']), len(cur['mgrs'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
