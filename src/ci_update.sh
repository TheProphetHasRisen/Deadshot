#!/usr/bin/env bash
# The scheduled job: runs on GitHub, in the public site repo (TheProphetHasRisen/Deadshot), from the
# copy of the source that deploy.sh keeps in its src/ folder. It reads Yahoo, rebuilds the page,
# runs every check deploy.sh runs (it calls deploy.sh, build only), and publishes to that same repo,
# which Vercel redeploys from. Nothing on Brian's Mac is involved.
#
# The workflow that runs it is ci/update.yml (deploy.sh installs it as .github/workflows/update.yml).
# The Yahoo sign-in arrives as the YAHOO_TOKENS secret, is written for the length of the run only,
# and is never committed (the site repo's .gitignore names it, and only named files are added).
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT/src"

# the page's typefaces and art live at the site root; the checks load them from beside the page
for d in fonts art manifest.webmanifest favicon.svg favicon-32.png apple-touch-icon.png icon-192.png icon-512.png \
         icon-maskable-512.png vercel.json; do
  [ -e "$d" ] || [ ! -e "../$d" ] || ln -s "../$d" "$d"
done

[ -n "${YAHOO_TOKENS:-}" ] || { echo "The YAHOO_TOKENS secret is missing: see ci/update.yml"; exit 1; }
( umask 077; printf '%s' "$YAHOO_TOKENS" > .yahoo_tokens.json )
trap 'rm -f "$ROOT/src/.yahoo_tokens.json"' EXIT

# what Yahoo said last time (the read time aside), to skip a publish when nothing has moved
sig(){ { grep -v '^ASOF' season2026_yahoo.py; cat status_log.json; python3 news.py --sig 2>/dev/null; } 2>/dev/null | shasum | cut -c1-40; }   # a status change or new injury news counts too
before="$(sig)"

for y in 2021 2022 2023 2024 2025; do
  [ -f "yahoo_raw/$y/teams.json" ] || python3 yahoo_fetch.py "$y"
done
python3 yahoo_fetch.py 2026
python3 yahoo_to_2026.py
python3 statuslog.py >/dev/null || true      # every player's injury status, kept each week (statuslog.py)
if [ "$before" = "$(sig)" ] && [ "${FORCE:-0}" != 1 ]; then
  echo "Nothing new on Yahoo since the last update: not publishing."; exit 0
fi
python3 draft_points.py >/dev/null

DEADSHOT_NO_REFRESH=1 ./deploy.sh          # build and every check; it stops the run on any failure

cp index.html 404.html sw.js "$ROOT/"
for f in og.png og-*.png; do [ -f "$f" ] && cp "$f" "$ROOT/$f"; done
mkdir -p "$ROOT/t" && cp t/*.html "$ROOT/t/" 2>/dev/null || true

cd "$ROOT"
git add index.html 404.html sw.js og.png og-*.png t src/season2026_yahoo.py src/draft_points.json src/status_log.json src/pred_log.json src/lab_feed.json
if git diff --cached --quiet; then echo "The page came out the same: nothing to publish."; exit 0; fi
git -c user.name="Deadshot updater" -c user.email="41898282+github-actions[bot]@users.noreply.github.com" \
    commit -qm "Live update from Yahoo ($(TZ=America/Los_Angeles date '+%b %-d, %-I:%M %p PT'))"
if [ "${DRYRUN:-0}" = 1 ]; then echo "Rehearsal: would publish this commit."; git log -1 --stat | head -20; exit 0; fi
git push -q
echo "Published. Vercel redeploys from here."
