# -*- coding: utf-8 -*-
"""One-time Yahoo sign-in. Run it once; after that the site refreshes its own key.

    python3 yahoo_auth.py

Brian runs this, not me. The client secret is typed into his own terminal with echo
off, goes straight into a gitignored file, and is never printed back.
"""
import getpass, re, sys, urllib.parse, webbrowser
import yahoo_api as Y


def ask(label, secret=False):
    while True:
        v = (getpass.getpass(label) if secret else input(label)).strip()
        if v:
            return v
        print("  (that came through empty -- try again)")


def main():
    print("""
================= Yahoo sign-in, one time only =================

You need two things from developer.yahoo.com/apps -> Deadshot Archives:
  the Client ID (Consumer Key)   -- long, ends in --
  the Client Secret              -- shorter

Nothing you type here is shown on screen or sent anywhere except Yahoo.
It is saved to .yahoo_tokens.json, which git is set up to refuse to commit.
""")
    client_id = ask("Client ID: ")
    client_secret = ask("Client Secret (it will not appear as you type or paste): ", secret=True)

    url = Y.auth_url(client_id)
    print("""
---------------------------------------------------------------
STEP 1. A browser tab should open. If it does not, copy this in:

%s

STEP 2. Sign in as the Yahoo account that is IN the Deadshot league
        (it does not have to be the one the app was made on), and
        click Agree.

STEP 3. You will land on deadshotleague.com and the page will look
        completely normal. That is fine. Look at the ADDRESS BAR --
        it will read something like

          https://www.deadshotleague.com/?code=abcd1234&state=deadshot

        Copy the whole address bar and paste it below.
---------------------------------------------------------------
""" % url)
    try:
        webbrowser.open(url)
    except Exception:
        pass

    pasted = ask("Paste the address bar here: ")
    # accept the whole URL or just the bare code, whichever he grabbed
    m = re.search(r'[?&]code=([^&\s]+)', pasted)
    code = urllib.parse.unquote(m.group(1)) if m else pasted
    if 'http' in code:
        sys.exit("\nThat does not look like it had a code in it.\n"
                 "Make sure the address bar shows ?code=... after you clicked Agree,\n"
                 "then run this again.")

    print("\nSwapping that for a key...")
    try:
        tok = Y.exchange(client_id, client_secret, code)
    except Y.YahooError as e:
        # Yahoo's error codes are specific and worth translating, because each one has
        # exactly one fix and the raw JSON tells Brian nothing.
        PLAIN = {
            'INVALID_CONSUMER_KEY':
                "The Client ID is wrong. Copy it again from developer.yahoo.com/apps ->\n"
                "Deadshot Archives -- select the whole field, it is ~100 characters and\n"
                "ends in --. A truncated copy looks exactly like this.",
            'INVALID_CLIENT_SECRET':
                "The Client Secret is wrong. Copy it again from the same page.",
            'INVALID_AUTHORIZATION_CODE':
                "That code was already used or has expired. They are single use and only\n"
                "last a few minutes. Just run this again.",
            'INVALID_GRANT':
                "That code was already used or has expired. Run this again.",
            'INVALID_REDIRECT_URI':
                "The Redirect URI on the app does not match. It has to be exactly\n"
                "  %s\n"
                "trailing slash included. Fix it on the app page, then run this again."
                % Y.REDIRECT,
        }
        code_name = ''
        try:
            import json as _j
            code_name = _j.loads(e.body).get('error', '')
        except Exception:
            pass
        print("\nYahoo would not complete the sign-in.\n")
        if code_name in PLAIN:
            print(PLAIN[code_name] + "\n")
        else:
            print("HTTP %s. What Yahoo said:\n%s\n" % (e.status, e.body))
            print("Usually one of: the code was already used (run this again), a typo in\n"
                  "the Client ID or Secret, or a Redirect URI that is not exactly %s"
                  % Y.REDIRECT)
        sys.exit(1)

    Y.save(tok)
    print("Signed in. The key is saved and git cannot commit it.\n")
    print("Now checking what that key can actually see...\n")

    import yahoo_check
    sys.exit(yahoo_check.report())


if __name__ == '__main__':
    main()
