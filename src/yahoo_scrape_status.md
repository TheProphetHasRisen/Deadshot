# 2025 player-level scrape — status

## What works
- 2025 league is reachable: https://football.fantasysports.yahoo.com/2025/f1/214163
- URL pattern for archived seasons: /{year}/f1/{leagueId}  (IDs differ per year; 2026 = 526001)
- Per-player weekly page: /2025/f1/214163/{teamNum}?week={N}
  Gives pos, player, fantasy points, projected points, for starters + bench + IR.
- Draft results: /2025/f1/214163/draftresults  (165 rows, 16 rounds x 10 teams)

## Extractor — VERIFIED CORRECT
Parse rule: tables whose LAST thead row starts with "Pos"; column index by header
name ("Fan Pts"), because an "Action" column appears on some teams and not others.
Player link is /nfl/players/... EXCEPT team defenses, which are /nfl/teams/... —
missing that dropped the DEF slot and made every week short by 2-21 pts.
Validation: summing non-BN/IR fantasy points reproduced A Storm Is Coming's stored
weekly score for all 14 regular-season weeks, exactly, to the cent.

## Captured so far
Teams 1 (A Storm Is Coming) and 2 (DylansVillans): 509 player-weeks, weeks 1-17.
Held in browser memory (window.__all / window.__csv) — NOT yet in the container.

## Two blockers
1. Yahoo rate limiting. After ~120 rapid fetches, every request returns
   "Request denied" (16-byte body). Teams 3-10 unavailable until it lifts.
2. No bulk transport out of the browser:
   - javascript_tool output caps at ~1.2KB (~40 CSV rows) per call
   - page-initiated downloads are blocked by the extension sandbox (verified:
     file never landed in ~/Downloads)
   - clipboard write blocked (no user gesture) — document.execCommand('copy') false
   Full 2025 player data is ~2,600 rows => ~65 calls through the output channel.

## Recommendation
The Yahoo Fantasy API (OAuth2) solves both blockers: bulk JSON, generous limits,
runs from the container with no browser. Needs the user to register an app and
supply a refresh token as a repo secret. This is the same prerequisite as the
already-agreed endgame (a scheduled job rewriting data.json).

Narrower browser-only fallback: pull ONLY the players involved in 2025's 10 trades
(~25 players x 17 weeks = ~425 rows = ~11 calls). Delivers the banked trade-grading
feature without the full dataset.
