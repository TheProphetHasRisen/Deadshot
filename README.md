# Deadshot Fantasy Football — The Record Book

Static site. One self-contained `index.html`, no build step, no dependencies.

**Live:** (Vercel fills this in after the first deploy)

## Structure
- `index.html` — the entire site. Data is embedded as JSON near the top of the file.

## Updating
Replace `index.html` and push. Vercel redeploys automatically, usually in under 30 seconds.

## Coverage
- 10 seasons, 2015–2025 (2019 absent from source records)
- 20 managers, 96 team-seasons
- All 55 playoff games, 2015–2025
- Full 2025 regular-season game log (70 games, with weekly projections)
- 2025 trades

## Known data gaps
- 2019 season missing entirely
- 2022 win-loss column totals 72W/68L where both must equal 70
- Regular-season game logs for 2015–2024 not yet loaded
