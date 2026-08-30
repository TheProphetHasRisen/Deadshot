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
  node --check .site.check.js && echo "  node --check OK"
  rm -f .site.check.js
  if node -e "require('playwright')" >/dev/null 2>&1; then
    node test.js | tail -1
  else
    echo "  (playwright not installed — skipping test.js)"
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
cp index.html "$CLONE/index.html"          # same name, overwrite in place; never delete first
[ -f og.png ] && cp og.png "$CLONE/og.png"   # link-preview card, served from the site root
git -C "$CLONE" add index.html og.png
if git -C "$CLONE" diff --cached --quiet; then
  echo "  index.html unchanged — nothing to deploy"; exit 0
fi
git -C "$CLONE" commit -qm "Update index.html ($(date +%Y-%m-%d))"
git -C "$CLONE" push -q origin "$BR"
echo "  pushed to $REPO@$BR — Vercel will redeploy"
