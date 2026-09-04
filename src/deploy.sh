#!/usr/bin/env bash
# Deadshot Record Book — build, verify, deploy.
#   ./deploy.sh            build + verify only, no push   (safe, default)
#   ./deploy.sh --push     build + verify + commit + push (Vercel auto-deploys)
#
# Requires: python3, gh (authenticated), and node for the verify steps.
set -euo pipefail
cd "$(dirname "$0")"

REPO="${DEADSHOT_REPO:-}"                       # e.g. brianberger/deadshot
CLONE="${DEADSHOT_CLONE:-$HOME/.deadshot-deploy}"
PUSH=0; [ "${1:-}" = "--push" ] && PUSH=1

say(){ printf '\n\033[1m== %s\033[0m\n' "$*"; }

say "build"
python3 export.py >/dev/null
python3 mksite.py

say "verify"
if command -v node >/dev/null 2>&1; then
  python3 - <<'PY'
import re,io
h=io.open('index.html',encoding='utf-8').read()
io.open('.site.check.js','w',encoding='utf-8').write(max(re.findall(r'<script>(.*?)</script>',h,re.S),key=len))
PY
  # A command on the LEFT of && is exempt from set -e, so `node --check x && echo OK`
  # printed the syntax error and carried straight on to the push. It has to be || exit.
  if node --check .site.check.js; then
    echo "  node --check OK"; rm -f .site.check.js
  else
    rm -f .site.check.js
    echo "  !! the page's JavaScript does not parse — refusing to go further"; exit 1
  fi
  if node -e "require('playwright')" >/dev/null 2>&1; then
    # no `| tail -1`: it hid the multi-line error report and swallowed the exit code
    node test.js || { echo "  !! test.js failed — refusing to go further"; exit 1; }
    # the worker and the manifest ship too, and neither was ever checked. A broken worker
    # is a sticky, per-device, invisible failure; a stray comma in the manifest silently
    # stops Add to Home Screen working.
    node --check sw.js || { echo "  !! sw.js does not parse — refusing"; exit 1; }
    echo "  sw.js OK"
    python3 -c "import json;json.load(open('manifest.webmanifest'))" \
      || { echo "  !! manifest.webmanifest is not valid JSON — refusing"; exit 1; }
    echo "  manifest OK"
    # the preview cards carry the season counts, so they are redrawn from the fresh build
    say "link previews"
    node mkog.js
  else
    echo "  (playwright not installed — skipping test.js and the preview cards)"
    # the preview PNGs have the season counts baked into their pixels, so shipping the
    # ones already on disk would put stale numbers in every link preview
    [ $PUSH -eq 1 ] && { echo "  !! refusing to push unverified, and with stale link previews"; exit 1; }
  fi
else
  echo "  !! node not found — SKIPPING syntax check and test.js"
  [ $PUSH -eq 1 ] && { echo "  refusing to push unverified"; exit 1; }
fi

# never ship a file that isn't named exactly index.html, or that looks truncated
[ -s index.html ] || { echo "index.html missing/empty"; exit 1; }
grep -q '</html>' index.html || { echo "index.html looks truncated"; exit 1; }
printf '  %s bytes\n' "$(wc -c < index.html | tr -d ' ')"

[ $PUSH -eq 1 ] || { say "done (build only — pass --push to deploy)"; exit 0; }

[ -n "$REPO" ] || { echo "Set DEADSHOT_REPO=owner/name first."; exit 1; }
say "deploy -> $REPO"
[ -d "$CLONE/.git" ] || gh repo clone "$REPO" "$CLONE"
git -C "$CLONE" fetch --quiet origin
BR="$(git -C "$CLONE" symbolic-ref --short HEAD)"
git -C "$CLONE" reset --hard --quiet "origin/$BR"
# snapshot BEFORE the overwrite: this used to run after, so every archived file was the
# page that went live *after* the date in its own filename
say "snapshot the page being replaced"
mkdir -p "$CLONE/past"
if [ -s "$CLONE/index.html" ]; then
  PREV="$CLONE/past/index-$(git -C "$CLONE" log -1 --format=%cd --date=format:%Y-%m-%d-%H%M -- index.html 2>/dev/null || date +%Y-%m-%d-%H%M).html"
  cp "$CLONE/index.html" "$PREV" 2>/dev/null || true
fi
ls -1t "$CLONE/past"/index-*.html 2>/dev/null | tail -n +11 | while read -r old; do rm -f "$old"; done
printf '  %s snapshots kept\n' "$(ls -1 "$CLONE/past"/index-*.html 2>/dev/null | wc -l | tr -d ' ')"

cp index.html "$CLONE/index.html"          # same name, overwrite in place; never delete first
[ -f og.png ] && cp og.png "$CLONE/og.png"   # default link-preview card, served from the root
for f in og-*.png; do [ -f "$f" ] && cp "$f" "$CLONE/$f"; done   # one card per theme
mkdir -p "$CLONE/t"                          # per-theme preview shims; see mkog.js
for f in t/*.html; do [ -f "$f" ] && cp "$f" "$CLONE/$f"; done
# The repo carries a src/ copy of the build, and the CI check rebuilds the page from it
# and compares. Nothing was updating src/, so that check compared the live page against a
# months-old build and failed on every single push -- the one guard against a hand-edited
# index.html was pure noise. Sync it.
mkdir -p "$CLONE/src"
for f in data.py export.py mksite.py verify.py writer.py test.js test_writer.py \
         weekly.py weekly2021.py weekly2022.py weekly2023.py weekly2024.py deploy.sh \
         CLAUDE.md HANDOFF.md README.md AUDIT.md YAHOO_PLAN.md \
         league_rules_2026.md yahoo_scrape_status.md; do
  [ -f "$f" ] && cp "$f" "$CLONE/src/$f"
done

for f in favicon.svg favicon-32.png apple-touch-icon.png icon-192.png icon-512.png icon-maskable-512.png vercel.json \
         manifest.webmanifest sw.js; do
  [ -f "$f" ] && cp "$f" "$CLONE/$f"           # icons and response headers, served from root
done
git -C "$CLONE" add -A index.html og.png og-*.png t src favicon.svg favicon-32.png \
  apple-touch-icon.png icon-192.png icon-512.png icon-maskable-512.png vercel.json manifest.webmanifest sw.js
if git -C "$CLONE" diff --cached --quiet; then
  echo "  index.html unchanged — nothing to deploy"; exit 0
fi
git -C "$CLONE" add past
git -C "$CLONE" commit -qm "Update index.html ($(date +%Y-%m-%d))"
git -C "$CLONE" push -q origin "$BR"
echo "  pushed to $REPO@$BR — Vercel will redeploy"
