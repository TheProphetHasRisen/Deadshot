# -*- coding: utf-8 -*-
"""What can this key actually see? Run it any time:

    python3 yahoo_check.py

Answers the two questions that decide whether the fetcher can be built:
  1. Is Fantasy Sports access switched on at all, or is Yahoo still sitting on it?
  2. Can it reach our own league, and how far back does the history go?
"""
import sys, time
import yahoo_api as Y

FIRST_SEASON = 2015          # the league's first year; this one really is fixed


def seasons():
    """2015 through the season now in progress.

    This was `range(2015, 2027)`, which quietly stops covering the current season on
    1 Jan 2027 -- the same class of bug we just spent a day removing from the site's
    copy. The NFL season is named for the year it starts, so it rolls over in about
    August, not January.
    """
    now = time.localtime()
    latest = now.tm_year if now.tm_mon >= 8 else now.tm_year - 1
    return list(range(FIRST_SEASON, latest + 1))


def _walk(o, key):
    """Yahoo's JSON nests dicts inside numbered-key dicts inside lists. Rather than
    model that, pull out every value stored under `key`, wherever it is buried."""
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key:
                out.append(v)
            else:
                out += _walk(v, key)
    elif isinstance(o, list):
        for v in o:
            out += _walk(v, key)
    return out


def report():
    print("=" * 62)
    print("Checking the Yahoo key")
    print("=" * 62)

    # --- 1. the simplest possible authenticated call -------------------------------
    # Order matters: the narrow causes are caught before the general one, because
    # "Yahoo is unreachable" and "your key is dead" are not "access is not on yet",
    # and telling Brian the wrong one sends him to fix something that is not broken.
    try:
        Y.get('game/nfl')
    except Y.YahooOffline as e:
        print("\nCOULD NOT REACH YAHOO.\n")
        print("%s\n" % e.body)
        print("Nothing here is broken -- this is the network, not the key.\n"
              "Try again in a bit:  python3 yahoo_check.py")
        return 2
    except Y.YahooNeedsSignIn as e:
        print("\nTHE SAVED KEY CANNOT BE USED.\n")
        print("%s\n" % e.body)
        return 3
    except Y.YahooError as e:
        print("\nFANTASY ACCESS IS NOT ON YET.\n")
        print("Yahoo answered HTTP %s. What it said:\n%s\n" % (e.status, e.body[:600]))
        if e.status in (401, 403):
            print("That is the 'you are who you say you are, but you are not allowed\n"
                  "this data' answer. It means the sign-in worked and Yahoo simply has\n"
                  "not attached Fantasy Sports to the app yet.\n\n"
                  "Nothing to fix on our side. Wait for them, then run this again:\n"
                  "  python3 yahoo_check.py")
        return 1
    print("\n  Fantasy access:      ON")

    # --- 2. our own leagues, season by season --------------------------------------
    try:
        r = Y.get('users;use_login=1/games;game_keys=nfl/leagues')
        names = _walk(r, 'name')
        print("  Leagues on this account (current season): %s"
              % (', '.join(str(n) for n in names[:8]) or 'none found'))
    except Y.YahooError as e:
        print("  Could not list leagues: HTTP %s %s" % (e.status, e.body[:200]))

    # --- 3. how far back the history goes ------------------------------------------
    print("\n  Season by season, what this account can reach:")
    reachable = []
    for y in seasons():
        try:
            r = Y.get('users;use_login=1/games;seasons=%d/leagues' % y)
            names = [str(n) for n in _walk(r, 'name')]
            # the game itself is called "Football"; league names are the useful ones
            leagues = [n for n in names if n.lower() not in ('football', 'nfl')]
            if leagues:
                reachable.append(y)
                print("    %d  %s" % (y, ', '.join(leagues[:4])))
            else:
                print("    %d  -" % y)
        except Y.YahooOffline:
            print("    %d  could not reach Yahoo -- stopping here" % y)
            break
        except Y.YahooError as e:
            # one unreachable season is not a reason to abandon the other eleven
            print("    %d  error HTTP %s" % (y, e.status))

    print("\n" + "=" * 62)
    if reachable:
        print("Reachable seasons: %s" % ', '.join(str(y) for y in reachable))
        print("Send this whole output back and I will start on the fetcher.")
    else:
        print("Signed in fine, but no leagues came back for any year.")
        print("Most likely this is the wrong Yahoo account -- the app can live on one")
        print("account, but you have to SIGN IN as the one that plays in Deadshot.")
        print("Delete .yahoo_tokens.json and run yahoo_auth.py again as that account.")
    print("=" * 62)
    return 0


if __name__ == '__main__':
    sys.exit(report())
