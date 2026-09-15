# -*- coding: utf-8 -*-
"""Talking to the Yahoo Fantasy API.

Standard library only, on purpose: this has to run on a stock macOS python3 with no
`pip install` step, and later inside a scheduled job with nothing else available.

Nothing in here ever prints the client secret or the tokens. `.yahoo_tokens.json` is
gitignored; if that file is ever committed the key is burned, because a GitHub object
stays reachable even after the commit is deleted.

Three failure kinds, deliberately separated, because the scheduled fetcher has to treat
them completely differently:

    YahooOffline      Yahoo could not be reached. Transient. Do nothing, try later.
    YahooNeedsSignIn  The stored key is dead or unusable. Brian must re-run yahoo_auth.
    YahooError        Yahoo answered, with a refusal. Read .status and decide.

The site's rule is that a failed fetch is a no-op, never a broken page, so nothing in
here may ever surface as a bare traceback.
"""
import json, os, ssl, sys, time, urllib.parse, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
TOKENS = os.path.join(HERE, '.yahoo_tokens.json')

AUTH_URL = 'https://api.login.yahoo.com/oauth2/request_auth'
TOKEN_URL = 'https://api.login.yahoo.com/oauth2/get_token'
API = 'https://fantasysports.yahooapis.com/fantasy/v2'

# Must match the Redirect URI registered on the app, character for character --
# trailing slash included. Yahoo rejects the exchange outright if it differs.
REDIRECT = 'https://www.deadshotleague.com/'

# Yahoo stopped answering at roughly 120 rapid requests during the 2025 scrape (see
# yahoo_scrape_status.md). Backfilling per-week rosters is ~1,700 calls, so pace every
# request from one place rather than hoping each caller remembers to.
MIN_GAP = 0.35
RETRIES = 4
_last_call = 0.0


# ---------------------------------------------------------------- errors ----------
class YahooError(Exception):
    """Yahoo answered and refused. .status and .body carry the only useful detail."""
    def __init__(self, status, body, url=''):
        self.status, self.body, self.url = status, body, url
        super().__init__('HTTP %s from %s\n%s' % (status, url or '?', body))


class YahooOffline(YahooError):
    """Could not reach Yahoo at all -- no network, DNS, TLS. Always transient."""
    def __init__(self, detail):
        super().__init__(0, 'Could not reach Yahoo: %s' % detail)


class YahooNeedsSignIn(YahooError):
    """The stored key cannot be used or repaired. Only a fresh sign-in fixes it."""
    def __init__(self, why):
        self.why = why
        super().__init__(0, why + '\n\nFix it by running:   python3 yahoo_auth.py')


# ---------------------------------------------------------------- tls -------------
def _ssl_context():
    """python.org's macOS build ships with an EMPTY trust store until someone runs
    "Install Certificates.command", so every https call dies with
    CERTIFICATE_VERIFY_FAILED. certifi's bundle is already on disk here, so fall back
    to it rather than sending Brian off to run an installer. Verification stays on
    either way -- this picks a trust store, it does not skip the check."""
    ctx = ssl.create_default_context()
    if ctx.cert_store_stats().get('x509_ca', 0):
        return ctx
    try:
        import certifi
        alt = ssl.create_default_context(cafile=certifi.where())
        if alt.cert_store_stats().get('x509_ca', 0):
            return alt
    except Exception:
        pass
    return None          # checked at call time; see _open


SSL = _ssl_context()

NO_CERTS = (
    "This Python has no certificate authorities installed, so it cannot verify that it\n"
    "is really talking to Yahoo, and every request would fail with an unreadable SSL\n"
    "error. Two ways to fix it, either is fine:\n\n"
    "  python3 -m pip install --upgrade certifi\n\n"
    "or run the installer that shipped with Python:\n\n"
    "  open \"/Applications/Python %d.%d/Install Certificates.command\"\n"
) % sys.version_info[:2]


# ---------------------------------------------------------------- transport -------
def _open(req):
    """Every request goes through here: paced, retried on the failures worth retrying,
    and with the three error kinds separated before anything escapes."""
    global _last_call
    if SSL is None:
        raise YahooError(0, NO_CERTS)

    for attempt in range(RETRIES):
        gap = MIN_GAP - (time.time() - _last_call)
        if gap > 0:
            time.sleep(gap)
        _last_call = time.time()
        try:
            with urllib.request.urlopen(req, timeout=30, context=SSL) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', 'replace')
            # 429 is the rate limiter, 5xx is Yahoo having a moment. Both are worth
            # waiting out; everything else is a real answer and must not be retried.
            if e.code in (429, 500, 502, 503, 504) and attempt < RETRIES - 1:
                wait = float(e.headers.get('Retry-After') or 0) or (2 ** attempt) * 2
                time.sleep(min(wait, 60))
                continue
            raise YahooError(e.code, body, req.full_url)
        except urllib.error.URLError as e:
            # no network, DNS failure, TLS failure. Retry briefly, then give up cleanly
            # rather than letting a raw URLError traceback out of a scheduled job.
            if attempt < RETRIES - 1:
                time.sleep((2 ** attempt) * 2)
                continue
            raise YahooOffline(e.reason)
        except (json.JSONDecodeError, ValueError) as e:
            raise YahooError(0, 'Yahoo sent something that is not JSON: %s' % e,
                             req.full_url)


def _post(url, fields):
    return _open(urllib.request.Request(url, data=urllib.parse.urlencode(fields).encode(),
                                        headers={'Content-Type': 'application/x-www-form-urlencoded',
                                                 'Accept': 'application/json'}))


def auth_url(client_id, state='deadshot'):
    return AUTH_URL + '?' + urllib.parse.urlencode({
        'client_id': client_id, 'redirect_uri': REDIRECT,
        'response_type': 'code', 'state': state})


# ---------------------------------------------------------------- storage ---------
def save(tok):
    """Write to a fresh 0600 file, then rename over the old one.

    Two bugs this closes. open(TOKENS,'w') truncated the good file before writing the
    new one, so an interrupted write (crash, full disk, Ctrl-C during a refresh) left a
    half-written file and cost a full browser re-authorisation. And it created the file
    at the umask default -- the secret sat on disk world-readable until the chmod a
    moment later. os.open with 0600 plus os.replace makes the swap atomic and means the
    secret is never readable by anyone else, not even briefly.
    """
    tmp = TOKENS + '.tmp'
    if os.path.exists(tmp):
        os.remove(tmp)
    fd = os.open(tmp, os.O_CREAT | os.O_WRONLY | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(tok, f, indent=1)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, TOKENS)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


REQUIRED = ('client_id', 'client_secret', 'access_token', 'refresh_token')


def load():
    if not os.path.exists(TOKENS):
        raise YahooNeedsSignIn("No Yahoo sign-in has been done on this machine yet.")
    try:
        with open(TOKENS) as f:
            tok = json.load(f)
    except (json.JSONDecodeError, ValueError):
        raise YahooNeedsSignIn(
            "The saved Yahoo key file is damaged -- it is not readable as JSON.\n"
            "Most likely something interrupted a write. Nothing is lost except the key.")
    missing = [k for k in REQUIRED if not tok.get(k)]
    if missing:
        raise YahooNeedsSignIn(
            "The saved Yahoo key file is missing: %s." % ', '.join(missing))
    return tok


# ---------------------------------------------------------------- oauth -----------
def exchange(client_id, client_secret, code):
    """Authorisation code -> access token + refresh token. Runs once, at sign-in."""
    tok = _post(TOKEN_URL, {
        'client_id': client_id, 'client_secret': client_secret,
        'redirect_uri': REDIRECT, 'code': code,
        'grant_type': 'authorization_code'})
    tok['client_id'] = client_id
    tok['client_secret'] = client_secret
    tok['expires_at'] = time.time() + int(tok.get('expires_in', 3600)) - 60
    return tok


# Yahoo's names for "this key is finished, sign in again" rather than "try later".
DEAD = ('INVALID_REFRESH_TOKEN', 'INVALID_GRANT', 'TOKEN_EXPIRED',
        'INVALID_CLIENT', 'INVALID_CLIENT_SECRET', 'INVALID_CONSUMER_KEY')


def refresh(tok):
    """Access tokens last an hour; the refresh token is the thing worth keeping.

    A revoked refresh token used to escape as a bare HTTP 400 against the *token*
    endpoint, which read like the Fantasy API had broken. It is its own condition: only
    a new sign-in fixes it, and the caller needs to be able to tell that apart from
    Yahoo simply being unreachable.
    """
    try:
        new = _post(TOKEN_URL, {
            'client_id': tok['client_id'], 'client_secret': tok['client_secret'],
            'redirect_uri': REDIRECT, 'refresh_token': tok['refresh_token'],
            'grant_type': 'refresh_token'})
    except YahooOffline:
        raise
    except YahooError as e:
        if e.status in (400, 401, 403) and any(d in e.body.upper() for d in DEAD):
            raise YahooNeedsSignIn(
                "Yahoo has stopped accepting the saved key. That normally means the\n"
                "Yahoo password changed, or access was revoked in account settings.")
        raise
    tok.update(new)
    tok['expires_at'] = time.time() + int(new.get('expires_in', 3600)) - 60
    save(tok)
    return tok


def get(path, tok=None):
    """GET a Fantasy API path, refreshing the access token first if it has aged out.

    `path` is everything after /fantasy/v2, e.g. 'game/nfl'. JSON is requested
    explicitly -- the API answers in XML otherwise.
    """
    tok = tok or load()
    if time.time() >= tok.get('expires_at', 0):
        tok = refresh(tok)
    sep = '&' if '?' in path else '?'
    url = '%s/%s%sformat=json' % (API, path.lstrip('/'), sep)
    return _open(urllib.request.Request(url, headers={
        'Authorization': 'Bearer ' + tok['access_token'],
        'Accept': 'application/json'}))
