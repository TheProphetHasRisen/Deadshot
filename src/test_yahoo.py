# -*- coding: utf-8 -*-
"""Guard rails for the Yahoo client.

    python3 test_yahoo.py

Every case here is a failure that actually escaped as a raw traceback, or a silent
data-loss window, before 13 Sep 2026. None of it talks to Yahoo -- urlopen is replaced
throughout, so this runs offline and in CI.
"""
import io, json, os, ssl, sys, tempfile, time, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yahoo_api as Y
import yahoo_check as C

PASS = FAIL = 0


def check(name, cond, detail=''):
    global PASS, FAIL
    if cond:
        PASS += 1
    else:
        FAIL += 1
        print("  FAIL  %s  %s" % (name, detail))


def probe(name, fn, want=None):
    """Run fn and compare; an exception is a FAIL, never a traceback.

    Without this a reintroduced bug crashed the run instead of reporting it, and a
    crash is exactly what a caller gating on the exit code cannot interpret.
    """
    try:
        got = fn()
    except Exception as e:
        check(name, False, '%s: %s' % (type(e).__name__, str(e).split(chr(10))[0][:60]))
        return
    check(name, got == want if want is not None else bool(got), repr(got)[:60])


def http(code, body, headers=None):
    def boom(*a, **k):
        raise urllib.error.HTTPError('u', code, 'err', headers or {}, io.BytesIO(body))
    return boom


def netdown(*a, **k):
    raise urllib.error.URLError('nodename nor servname provided')


class Patch:
    """Swap urlopen and neuter the backoff sleeps so retries do not take 14 seconds."""
    def __init__(self, fn):
        self.fn = fn

    def __enter__(self):
        self.o, self.s = Y.urllib.request.urlopen, Y.time.sleep
        Y.urllib.request.urlopen = self.fn
        Y.time.sleep = lambda *_: None
        Y._last_call = 0.0

    def __exit__(self, *e):
        Y.urllib.request.urlopen, Y.time.sleep = self.o, self.s


def tok(**kw):
    t = dict(client_id='id', client_secret='sec', access_token='at',
             refresh_token='rt', expires_at=time.time() + 9999)
    t.update(kw)
    return t


def main():
    tmpdir = tempfile.mkdtemp()
    Y.TOKENS = os.path.join(tmpdir, 'tok.json')

    print("storage")
    # --- an interrupted write must not destroy the key that already worked ---------
    Y.save(tok(access_token='GOOD'))
    real = json.dump
    json.dump = lambda *a, **k: (_ for _ in ()).throw(IOError('disk full'))
    try:
        Y.save(tok(access_token='NEW'))
    except IOError:
        pass
    json.dump = real
    probe("interrupted save keeps the previous key",
          lambda: Y.load()['access_token'], 'GOOD')
    check("interrupted save leaves no .tmp behind",
          not os.path.exists(Y.TOKENS + '.tmp'))

    # --- the secret must never be readable by anyone else, not even briefly --------
    seen = {}
    real_open = os.open
    os.open = lambda p, f, m=0o777: seen.setdefault('mode', m) and 0 or real_open(p, f, m)
    Y.save(tok())
    os.open = real_open
    check("token file is created 0600, not chmod'd afterwards",
          seen.get('mode') == 0o600, 'created with %s' % oct(seen.get('mode', 0)))
    check("token file on disk is 0600",
          (os.stat(Y.TOKENS).st_mode & 0o777) == 0o600)

    # --- a damaged or partial file must explain itself ----------------------------
    open(Y.TOKENS, 'w').write('{"client_id": "id", "access_to')
    try:
        Y.load(); check("corrupt file raises", False)
    except Y.YahooNeedsSignIn as e:
        check("corrupt file names the fix", 'yahoo_auth.py' in e.body)
    except Exception as e:
        check("corrupt file raises YahooNeedsSignIn", False, type(e).__name__)

    Y.save({'access_token': 'at', 'expires_at': 0})
    try:
        Y.load(); check("incomplete file raises", False)
    except Y.YahooNeedsSignIn as e:
        check("incomplete file says what is missing", 'client_id' in e.body)
    except Exception as e:
        check("incomplete file raises YahooNeedsSignIn", False, type(e).__name__)

    print("network")
    Y.save(tok())
    # --- no bare URLError may escape: the scheduled job must see a clean no-op -----
    with Patch(netdown):
        try:
            Y.get('game/nfl'); check("offline raises", False)
        except Y.YahooOffline:
            check("network down -> YahooOffline", True)
        except Exception as e:
            check("network down -> YahooOffline", False, type(e).__name__)

    # --- a revoked key is not the same as Yahoo being down ------------------------
    Y.save(tok(expires_at=0))
    with Patch(http(400, b'{"error":"INVALID_REFRESH_TOKEN"}')):
        try:
            Y.get('game/nfl'); check("revoked raises", False)
        except Y.YahooNeedsSignIn as e:
            check("revoked key -> YahooNeedsSignIn", True)
            check("revoked key names the fix", 'yahoo_auth.py' in e.body)
        except Exception as e:
            check("revoked key -> YahooNeedsSignIn", False, type(e).__name__)

    # --- a token-endpoint outage during refresh is transient, not a dead key ------
    Y.save(tok(expires_at=0))
    with Patch(netdown):
        try:
            Y.get('game/nfl'); check("refresh offline raises", False)
        except Y.YahooOffline:
            check("refresh with no network -> YahooOffline (not NeedsSignIn)", True)
        except Exception as e:
            check("refresh with no network -> YahooOffline", False, type(e).__name__)

    print("rate limiting")
    Y.save(tok())
    # --- 429 must be waited out, because the backfill is ~1,700 requests ----------
    calls = {'n': 0}

    def flaky(*a, **k):
        calls['n'] += 1
        if calls['n'] < 3:
            raise urllib.error.HTTPError('u', 429, 'slow down',
                                         {'Retry-After': '1'}, io.BytesIO(b'{}'))
        class R:
            def read(self): return b'{"ok":1}'
            def __enter__(self): return self
            def __exit__(self, *e): pass
        return R()
    with Patch(flaky):
        check("429 is retried and then succeeds", Y.get('game/nfl') == {'ok': 1})
        check("429 retried the right number of times", calls['n'] == 3, calls['n'])

    # --- but a real refusal must not be retried 4 times ---------------------------
    calls['n'] = 0

    def forbidden(*a, **k):
        calls['n'] += 1
        raise urllib.error.HTTPError('u', 403, 'no', {}, io.BytesIO(b'{"error":"nope"}'))
    with Patch(forbidden):
        try:
            Y.get('game/nfl')
        except Y.YahooError as e:
            check("403 is not retried", calls['n'] == 1, '%d attempts' % calls['n'])
            check("403 keeps its status", e.status == 403)

    # --- requests are paced, or Yahoo stops answering at ~120 ---------------------
    class OK:
        def read(self): return b'{}'
        def __enter__(self): return self
        def __exit__(self, *e): pass
    saved_sleep = Y.time.sleep
    Y.urllib.request.urlopen, Y._last_call = (lambda *a, **k: OK()), 0.0
    t0 = time.time()
    Y.get('game/nfl'); Y.get('game/nfl'); Y.get('game/nfl')
    check("consecutive requests are paced apart",
          time.time() - t0 >= Y.MIN_GAP * 2 - 0.05,
          '%.2fs for 3 calls' % (time.time() - t0))
    Y.time.sleep = saved_sleep

    print("misc")
    # --- the year range must not need editing every January ----------------------
    now = time.localtime()
    expect = now.tm_year if now.tm_mon >= 8 else now.tm_year - 1
    check("seasons() reaches the current season", C.seasons()[-1] == expect,
          '%d vs %d' % (C.seasons()[-1], expect))
    check("seasons() starts at the league's first year", C.seasons()[0] == 2015)

    # --- the JSON walker against Yahoo's real nesting ----------------------------
    sample = {"fantasy_content": {"users": {"0": {"user": [{"guid": "x"}, {"games": {
        "0": {"game": [{"game_key": "449"}, {"leagues": {"0": {"league": [
            {"name": "DEADSHOT", "league_id": "214163"}]}, "count": 1}}]}, "count": 1}}]},
        "count": 1}}}
    check("_walk finds a deeply nested league name",
          C._walk(sample, 'name') == ['DEADSHOT'])
    check("_walk returns [] for an absent key", C._walk(sample, 'nope') == [])

    # --- an empty trust store must explain itself, not emit raw SSL noise --------
    saved = Y.SSL
    Y.SSL = None
    try:
        Y.get('game/nfl'); check("no CA store raises", False)
    except Y.YahooError as e:
        check("no CA store gives a fixable message", 'certifi' in e.body)
    finally:
        Y.SSL = saved

    print("\n%d passed, %d failed" % (PASS, FAIL))
    return 1 if FAIL else 0


if __name__ == '__main__':
    sys.exit(main())
