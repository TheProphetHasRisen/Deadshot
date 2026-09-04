# Deadshot Record Book — handoff

A single-page, self-contained fantasy football history site for the Deadshot league
(2015–2025, 10 managers active, 20 all-time). Everything ships as one `index.html`
with no images and no CDN scripts. ~500 KB.

> **One exception, verified 2026-08-27:** the `<head>` links
> `fonts.googleapis.com`, which pulls six `.woff2` files from `fonts.gstatic.com`.
> The page is *not* fully offline-capable — with that host blocked it renders in
> fallback faces. Inline them as data URIs if the no-external-requests claim ever
> needs to be true.

Live: deployed on Vercel from a GitHub repo whose only meaningful file is `index.html`.

---

## 1. Build pipeline

```
data.py  +  weekly*.py          ← hand-transcribed source of truth
        │
        ├── export.py           → site_data.json    (all aggregation / analytics)
        │
        └── mksite.py           → index.html        (CSS + markup + JS + embedded JSON)
```

Two commands, in this order, from this directory:

```bash
python3 export.py     # writes site_data.json
python3 mksite.py     # reads site_data.json, writes index.html
```

`mksite.py` prints the byte count on success. Nothing else is generated.

### Test

```bash
npm i playwright                      # once
node test.js                          # headless structural audit, desktop + mobile
CHROMIUM_PATH=/path/to/chromium node test.js   # if you need to point at a specific binary
```

`test.js` asserts row counts for every table/chart on the page and reports any
`pageerror` / console error. A `net::ERR_TUNNEL_CONNECTION_FAILED` line is
expected noise from the sandbox and is not a real failure.

Also worth running after any JS edit:

```bash
python3 - <<'PY'
import re,io
h=io.open('index.html',encoding='utf-8').read()
io.open('/tmp/site.js','w',encoding='utf-8').write(max(re.findall(r'<script>(.*?)</script>',h,re.S),key=len))
PY
node --check /tmp/site.js
```

---

## 2. File map

| File | What it is |
|---|---|
| `data.py` | Canonical dataset. `SEASON_META` (teams / reg games / playoff spots per year), `STANDINGS`, `FINAL_PLACE`, `MANAGERS` (team name → manager, per year), `CHAINED` (team names that persist across years), `CO_CHAMPS`, `PLAYOFF_GAMES`, `MANAGER_ORDER`. |
| `weekly.py` | 2025 week-by-week: `W2025`, `BYES2025`, `TRADES2025` |
| `weekly2024.py` … `weekly2021.py` | Same shape for 2024, 2023, 2022, 2021 |
| `export.py` | All analytics. Reads the above, writes `site_data.json`. |
| `mksite.py` | The whole site. Four raw strings: `HEAD` (all CSS, line ~4), `BODY` (markup + the `__DATA__` placeholder, ~932), `JS` (~1395), `SHELL_TOP` (doctype/meta, ~3536). |
| `site_data.json` | Build artifact. Do not edit by hand. |
| `index.html` | Build artifact. Do not edit by hand — every change goes in `mksite.py`. |
| `CLAUDE.md` | Standing working rules — Claude Code loads this automatically each session |
| `test.js` | Playwright audit |
| `verify.py` | Data integrity checks (HANDOFF section 3 invariants). Exit 1 on any failure. |
| `writer.py` | Renders league data back into `data.py` / `weekly*.py` format. Freezes finished seasons; refuses to write anything that fails `verify.py`. |
| `test_writer.py` | Round-trip and guard-rail tests for `writer.py`. |
| `YAHOO_PLAN.md` | Plan for replacing hand transcription with the Yahoo API. |
| `league_rules_2026.md` | League settings reference |
| `yahoo_scrape_status.md` | Notes from an attempt to pull live Yahoo data |

### Data row shapes

```python
# weekly*.py
W2025 = [(week, teamA, actualA, projA, teamB, actualB, projB, bracket), ...]
#   bracket: '' regular season, 'C' championship bracket, 'S' consolation
BYES2025  = [(week, team, actual, proj, bracket), ...]      # bye weeks still score
TRADES2025 = [("Nov 7", [players...], teamA, [players...], teamB), ...]

# data.py
STANDINGS[year] = [(rank, team, W, L, T, PF, PA, moves), ...]   # moves may be None
PLAYOFF_GAMES   = [(year, week, round, teamA, ptsA, teamB, ptsB, void), ...]
SEASON_META[year] = (teams, reg_games, playoff_spots, spots_confirmed)
```

---

## 3. Verification invariants

These caught real data errors more than once. Run them after adding any season:

- League-wide **PF must equal PA to the cent**.
- Every team's **W + L + T == season length**.
- **Total W == total L** across the league.
- Weekly game log must reconcile against `STANDINGS` for every team.

A 2022 transcription error (five wrong records) was found exactly this way.

These are now automated. `python3 verify.py` runs 517 checks across all seasons and
exits non-zero on any failure, so it can gate a build or an automated fetch. It also
checks team counts, duplicate names, manager/team coverage, `FINAL_PLACE` membership
and playoff-game team names. Confirmed to actually catch things: corrupting one score
by 100 points and flipping one team's record from 5-9 to 6-8 were each caught twice
over, naming the exact team.

**The postseason is recorded twice** -- in `PLAYOFF_GAMES` and again in the weekly
logs -- and until 2026-08-28 nothing checked the two agreed. `inv_playoffs_match_log`
now does: every playoff-table game must exist in that season's weekly log, and the
scores must match to the cent. Verified by typing a digit-swap into the 2025 Final
(142.92 -> 142.29), which it caught. The weekly log legitimately holds four more
postseason games per season than the playoff table: the consolation ladder (`'S'`
bracket) is logged but deliberately left out of `PLAYOFF_GAMES`.

`H2H_SEED` was removed from `data.py` on 2026-08-28. It duplicated the 2024/2025 rows
of `PLAYOFF_GAMES` exactly, nothing referenced it, and it could only ever drift out of
step. Removing it left `index.html` byte-identical, confirming it was dead.

### The build is not bit-reproducible across machines

`pythW`, `luck` and `expOverAvg` derive from `pf**K / (pf**K + pa**K)` with a
non-integer `K = 2.37` ([export.py](export.py) line 24). A fractional exponent goes to the C
library's `pow()`, which CPython does not implement, so the last 1-2 bits depend on
whichever libm the build machine links. **A rebuild that changes only these three
fields inside the embedded JSON is expected and is not a regression.**

Observed in practice: rebuilding a checked-in `site_data.json` on a different machine
moved exactly 4 of ~14,000 numbers — one team-season's `pythW` and `luck`, plus that
manager's career `luck` and `expOverAvg` — by ~1e-15 relative. Everything else in
`index.html`, including all CSS, markup and JS, was byte-identical.

Before blaming float noise, confirm that is all it is: `md5` alone will not tell you.
Parse both files and compare structurally. Key *order* changing, a differing value
count in the thousands, or any non-float field moving is a real bug, not libm. Python
version and CPU architecture are **not** the cause — 3.9 and 3.11, arm64 and x86_64,
all agree with each other.

If you ever need the artifacts to hash-match across machines, round these three fields
in `export.py` before serialising; ~1e-10 is far below anything the UI displays.

---

## 4. Analytics glossary (all computed in `export.py`)

- **Power Index** — 100 = that season's league-average PPG. Re-based every year, so a
  110 in 2015 and a 110 in 2025 mean the same thing despite scoring inflation.
- **Z-score** — standard deviations from that season's mean PPG.
- **Pythagorean expectation** — exponent `K = 2.37`.
- **Luck** — actual wins minus Pythagorean wins.
- **All-play** — record if you played every team every week (`apW/apL/apPct`).
- **Expected titles** — bye-aware: `neutral_title_odds(seed, spots)` pads the bracket to
  the next power of two; top `byes` seeds need one fewer win. Verified to sum to exactly
  1.0 per season.
- **Power Rankings** — recency-weighted: each season weighted `λ^(LAST − year)` applied to
  *games played*, then shrunk toward 100 by `N/(N+25)`. λ is a live slider (0.45–1.00).
- **SOS** — `sos`, `sosRel`, `sosAp`, `sosBase` per team-season.
- **Volatility** — `sd` and `cv` (coefficient of variation) of weekly scores.
- **.500 metrics** — `gAbove`, `sznAbove/Below/Even`, `wkAbove/At/Below`, `wkStreak`,
  `expOverAvg`, plus `vsWinW/L`, `vsSubW/L`.

---

## 5. Page structure

Sections, in DOM order (the nav array `SECS` in the JS **must** match this order —
a mismatch between the two was a real reported bug):

```
champions · alltime · power · shape · weekly · luck · advanced
seasons · h2h · trades-sec · records · method
```

Twelve, not fourteen. **Power Rankings was merged into Power Index** and **The .500 Line
into Advanced** (2026-08-31): same content, same order, no separate heading or nav entry.
Both now appear under a `.sub-h` divider inside the host section. Do not assert an exact
section count in tests; assert the page rendered.

### Default theme is Crimson

First-time visitors get `red`, not `og`. That is set in **two** places and both must
agree: the inline script in `SHELL_TOP` that runs before paint (so there is no flash of
the wrong theme), and the fallback in the skin restore near the bottom of `JS`.
The favicon is drawn in Crimson to match.

### The Record Book is last, and starts collapsed

21 tables plus the milestone list made everything below it a long scroll, so `#recsWrap`
is `hidden` by default with a toggle above it. The tables are still built on load, so
`test.js` still counts them and nothing about the data changes.

It also **sits second-to-last, directly before Method** (moved there 2026-09-01). It is
reference material rather than something to read through, so it belongs at the end with
the other reference section rather than cutting the narrative in half. Moving a section
means moving it in **two** places — the markup in `BODY` and the `SECS` array in `JS` —
or the nav highlight tracks the wrong section.

### Shareable cards

Eight canvas-drawn PNGs, all 1080x1080, all handed to the phone's share sheet
(`navigator.share` with a file) and falling back to a download on desktop:

| Card | Where the button is |
|---|---|
| **Manager card** | the manager modal |
| **Head to head** | next to the two pickers in Head to Head |
| **The rivalry** — every meeting in order | "Every meeting", same row |
| **The case against** — the roast | the manager modal |
| **The season** — champion + final table | the Seasons standings card header |
| **The bracket** — the whole postseason | the Seasons bracket card header |
| **The receipt** — one game | the arrow on any result in the weekly scoreboard |
| **League record** — one record | the picker beside the record-book toggle |
| **Wrapped slide** — whatever card is on screen | the arrow in the Wrapped top bar |

**A card wears the theme of the page it came from — with one exception.** `cardPalette()`
reads `--surface`, `--ink`, `--ink-3` and `--brass`. It used to read the **masthead**
tokens, which matched on five skins and was badly wrong on Crimson: that masthead is deep
red while the page itself is cream, so every Crimson card came out a solid red slab that
looked nothing like the site. Anything drawn on a card must take its colour from the
palette — two divider rules in the manager card were hardcoded `rgba(255,255,255,.10)`
from the dark-masthead days and went invisible the moment the ground turned white.

The exception is the **Wrapped slide card**, which paints the same gradient the slide was
on (`WRBG[i % 8]`, parsed out of the CSS string) with the same soft highlights, vignette
and white type. Wrapped is its own world on screen and a card in paper-and-ink read as a
different product. Note the CSS angle convention when converting: 0deg points up and
turns clockwise, so the direction vector is `(sin a, -cos a)` and the gradient line spans
`|W sin a| + |H cos a|`.

**"Every meeting" has to mean every meeting.** The rivalry card used to cut the list and
add "and 2 earlier meetings", which the owner rejected outright. Rows now shrink to fit —
the longest rivalry on record runs to 11 games — and only trim if the step would fall
below 19px, which nothing currently reaches.

`cardBase()` / `cardKick()` / `cardFoot()` / `cardRule()` / `cardTiles()` /
`cardFit()` / `cardClip()` exist so a new card is a layout, not another copy of the
background, the rule lines and the footer. `shareAny(builder, filename, btn)` is the
one wrapper: it disables the button, shows "Building…", swallows `AbortError` (a
dismissed share sheet is not a failure) and restores the label.

**The receipt closes with three lines, not one.** The ranking ("the 216th biggest margin
of 406 logged games") was briefly removed as saying nothing — the median margin is 23.84,
so most games land mid-table — and the owner asked for it back, so it stays and the
all-play line joins it: how many of the rest of the league that winning score would have
beaten the same week, from `ap`. Playoff weeks have no `ap` and drop to two lines.

**The season card's first column is final placing, not the regular-season order.** A
10-4 team can sit fourth. The column is headed FIN and the footer says "final placings",
because without that the table reads as broken. The footer's second line is generated:
when the champion also led the league in scoring, repeating their own points back at the
reader is noise, so it says that instead and names whoever had the best record.

**Two cards are generated, not written.** `bigRecords()` derives the ten league records
from `ROWS`, `M` and the game logs, and `roastLines(name)` derives the roast from the
same places — so both stay true when the numbers move, and neither can say something
the data does not support. `meetings(a,b)` is the shared meeting list: playoff games
from `D.games` (all ten seasons) plus regular-season games from `D.wk[y].games` where
`br` is empty (2021–2025 only). The two sources cannot overlap.

**The roast measures before it draws.** Five facts that run off the bottom are worth
less than four that fit, so `makeRoastCard` measures every block and pops from the end
until the stack clears the footer. There is an automated check for this: render every
card type for every manager, season, record, Wrapped slide, rivalry pair and a sample
of games, in all six skins (990 renders), and flag any ink painted in the outer thirds
of the footer band. It currently passes clean.

**Wrapped's opening slide needs two guards.** Its label is the same words as the card's
kicker and its value is the manager's own name, both of which are already printed at
the top — so `makeWrapCard` drops each when it duplicates, and re-centres the note into
the space that frees up.

Both take their colours from `cardPalette()`, which reads the live theme's masthead
tokens, so the picture matches the site the reader was just looking at.

**Crimson needs a guard and has one.** That skin defines `--brass` and `--mast-bg` as
the same `#8E1520`, so the accent would be drawn in exactly the background colour and
vanish. `cardPalette()` checks the contrast and falls back to `--mast-kick`, then
`--mast-sub`, then the ink. Any new skin that reuses its accent as a background gets
the same protection for free.

**Do not use Fraunces on the canvas.** It is a variable font and canvas cannot set its
optical-size axis, so its numerals render in the wrong forms at display sizes. Big
Shoulders Display has no such axis and is what both cards use for large numbers.

### Power Index has a generated explainer

`drawPiHelp()` fills `#piHelp` under the Power Index lede: the arithmetic in one line, a
worked example from the most recent champion's season, a table of what each band means
with the count of seasons in it, a paragraph on why the number travels across years, and
a collapsed note on what it deliberately ignores. Every number in it is computed from
`ROWS`, so adding a season keeps it true. It is in `REDRAW` because the band swatches come
from `diverge()`, which reads the live theme.

The owner considers this the most important stat on the site precisely because it is the
only one comparable across seasons — treat the explainer as load-bearing copy, not
decoration.

**The bands carry a written label AND four counts, and that split is deliberate.** The
labels ("a contender's year") describe the scoring level; the counts beside them —
seasons, made playoffs, podiums, titles — say what the level has actually been worth. A
label on its own once overclaimed badly: "a contender's year" sat on 110–120 when the
median champion scored **107.4** and one has won the whole thing at **93.9**. Words
describe, numbers judge. Every count is read off `ROWS`, so the right-hand side cannot go
stale or overclaim; if you edit a label, check it against those counts first.

There is no "x of y" in the playoff column — the seasons count is the column beside it.

### Column headings explain themselves, from their own "?"

`table()` renders a `t:` on a column as `data-th-tip` and hangs a small `.gl.gl-th`
question mark off the heading, with the site's own tooltip bound to **that**, not to the
heading. Two earlier versions were both wrong:

- a plain `title=""` — the browser draws it in its own style after a long delay, and a
  phone can never show it at all;
- the tooltip bound to the whole heading — which fought with the heading's real job. You
  went to read what a column meant and re-sorted the table instead. The `?` stops the
  click from reaching the sort handler.

Every column of the Consistency, form and Z-score table carries one; add `t:` to any new
column and it works with no further wiring.

### Absences: missed seasons and separate departures are different numbers

`mgrGaps(m)` counts seasons sat out. `mgrSpells(m)` counts *separate* absences and returns
the first season back afterwards. The manager verdicts used `mgrGaps` for both and said
untrue things: Nick Gearing sat out four seasons but only ever left **once**, so "keeps
disappearing for years at a time" and "left and returned more than once" were both wrong.
**Nobody in this league has left twice.** Any new line about coming and going must use
`mgrSpells().spells`, not the missed-season count.

Two more helpers feed the verdicts, both requested because a line was true but incomplete:

- `mgrSlide(m)` — the number of seasons when **every** one was lower than the last, else 0.
  Wesley Alpert has gone 113.5 → 108.0 → 104.3 → 98.6 → 94.2, a perfect five-season slide,
  and his line says so alongside his league-best luck. Three seasons is the minimum; below
  that it is noise.
- `mgrSinceTitle(m)` — seasons played since the last title and how many were below average.
  Nick Gearing and Chris Cossu both won and then dropped below 100 in every season since,
  which their lines now carry as a second, flatter sentence rather than a second "and".

The manager share card sets the verdict smaller when it runs past four lines, so a longer
sentence loses no clause.

### Why almost nobody is above .500 against winning teams

Not a bug, and it gets asked. When a winning team plays a losing one, that game lands
in "vs the rest" for the winner and "vs a winner" for the loser, so the vs-winners
bucket is loaded with games played by losing teams. League-wide it sits at .383 while
"vs the rest" sits at .620. Compare managers to each other, not to .500.
`inv_vs_buckets_balance` in `verify.py` pins the arithmetic: wins-vs-winners minus
losses-to-the-rest must equal (winner-vs-winner games) minus (loser-vs-loser games).

Note the coverage too: this stat sees every playoff game plus the 2021-2025 regular
seasons only, because earlier years have no game log.

### Phones

Before content, the page used to spend 696px on a 390px phone, about 82% of a screen.
Now 364px. Three things did it:

- **Masthead** shrinks under 640px: 64px reticle, smaller wordmark, tighter stat row.
- **The manager and theme bar collapses under 760px** behind a one-line summary that
  reads "Managers Active 10 · Theme Crimson". It was 180px of wrapped buttons.
  Note: `$('.fb')` does **not** work to find it, because `.fb` also matches SVG bar
  elements elsewhere on the page and querySelector picks one of those. Reach it via
  `$('#fbSum').closest('.fb')`.
- **Masthead decorations are hidden under 700px.** Each is a 1400x170 SVG drawn with
  `preserveAspectRatio="none"`, so a phone squashes it about 3.6:1 and drags its shapes
  across the stat line. Same trap the redacted dossier hit at 7.2:1.

There is deliberately no separate mobile build. One page, responsive, so a change can
never land on one and miss the other.

### Collapsible cards

Add `data-collapse` to any `.card` and it gets a Hide/Show control in its header.
`data-collapse="closed"` starts it shut. `data-collapse-also="#id"` also toggles
related content that sits outside the card, which the Trades card needs for its grid.

### Formatting audit

`format.js` (session scratchpad) checks the things a "no JS errors" pass never sees, on
every skin at 390 / 768 / 1440: text clipped by its own box, text physically covered by
something painted over it, children escaping their card, and grid cells too narrow for
their content. **Validated by reintroducing a real regression and confirming it fires** —
a checker that has never caught anything proves nothing.

Two traps it exists because of:

- **Never use a loose search-and-replace on a CSS rule.** `.board` and `.tiles` end with
  the same `minmax(min(100%,NNNpx),1fr));gap:1px;background:var(--rule)`, and a regex
  with `count=1` hit `.board` because it appears first in the file. That silently
  squeezed the champions grid from 196px cells to 108px and clipped every team name.
  Anchor on the selector (`.tiles{`) and assert what changed afterwards.
- **Overlap cannot be judged from bounding boxes.** An inline `<sup>` or `<em>` inside a
  paragraph has a rect spanning the whole line run, so box-intersection reports dozens of
  false overlaps. Use `document.elementFromPoint` at the text's own position instead.

Also: when a responsive rule hides grid columns, the **header labels and the row cells
both** need the hiding class. `.lad-ev` was on the row cells only, so on phones the
ladder header had six labels for five columns and "EVID" wrapped into the 22px rank
column.

### Sound

Everything is synthesised with the Web Audio API. There are no audio files and there
must not be, or the page stops being self-contained.

- `thunder()` builds a clap in three parts: a sub-10ms tear, the blast, then seven
  rolling returns that arrive later and darker, because air absorbs high frequencies
  faster than low ones over distance.
- `choirAh()` is sawtooth voices through three bandpass filters at roughly 730, 1090
  and 2440 Hz, which is what spells the vowel "ah". The filters remove most of the
  energy, so the gain after them is multiplied back up by 7.5 — without that it renders
  at a peak of 0.013 and is effectively silent.
- `SFX.shot()` is a rifle report as three separate events, not one noise wash: the
  supersonic N-wave crack, the muzzle blast a few ms behind it, then discrete spaced
  returns. Blurring them together is what made the earlier version sound fake.
- `ping()` / `casing()` are the ejected case. Metal rings on **inharmonic** partials
  (1, 2.76, 5.40, 8.93, 13.34), which is what reads as brass rather than a tuned note.
  Bounces converge in time and decay in level, like a dropped coin.

**How to check a change without hearing it.** Render into an `OfflineAudioContext`,
then measure peak, peak time, RMS, clipped samples and the energy envelope across ten
slices. That is how the silent choir and an over-loud casing were both caught. Targets:
peak roughly 0.3-0.9, zero clipped samples, and an envelope whose shape matches the
intent (the commish cue should read `9311143000`: clap, decay, then the choir rising).

### The masthead reticle

- The sweep is a gradient wedge spanning 42 degrees, rotating clockwise from twelve
  o'clock over 5.5s. It was originally a flat 9% fill, invisible on dark skins. Do not
  widen it and do not add a stroked leading edge; both were tried and rejected.
- **Sweep strength is per skin** via `--rt-sweep`. Crimson and Pigskin set `--rt` to
  pure white, where the default .62 wedge reads as a blown-out triangle; both are turned
  down. Gold skins keep the full value.
- **Redacted only** gets a radar contact at (84,41), which is 51.6 degrees round. The
  wedge covers it between 2.7% and 14.3% of the cycle, so `blipPing` peaks at 9%.
  If the sweep geometry changes, that timing has to move with it.
- **Pigskin only** swaps the square grid for a football field: yard lines, heavier
  sidelines, hash marks. `.rt-grid-plain` and `.rt-grid-field` toggle by skin.

### Automatic checks, snapshots and shape validation (2026-08-31)

- **`.github/workflows/checks.yml`** runs on every push, weekly on a schedule, and on
  demand from the Actions tab. It runs `verify.py`, `test_writer.py`, rebuilds the site
  from `src/`, confirms the rebuilt page matches the published one (ignoring the libm
  float noise documented above), `node --check`s the inline script, and runs `test.js`
  in a real browser. GitHub emails the owner on failure. This exists so the safety net
  works when nobody is holding it, which matters most once the Yahoo fetcher is writing
  data unattended.
- **`verify.py` now also checks shape, not just arithmetic** — types, ranges, bracket
  flags, duplicate matchups, trade structure. 517 checks became 7,468. The arithmetic
  invariants catch the mistakes a human transcriber makes; these catch the ones a parser
  makes (a null, a string where a float belongs, a score of 0 for a week never played).
  Verified by injecting eleven faults and confirming every one is caught.
- **A caution learned the hard way here:** `weekly_sources()` returns `(games, byes)`
  tuples, not modules. Three of the new shape checks originally did
  `getattr(mod, "W2025")` on that tuple, which silently returns nothing, so they ran
  zero assertions and always passed. `weekly_modules()` now exists for checks that need
  the module. **A check that cannot fail is worse than no check**, because it reads as
  coverage. Test new invariants by breaking the data on purpose.
- **`deploy.sh` snapshots the page it replaces** into `past/`, keeping the last ten.
  Rolling back is copying one file, not reconstructing a build.

### site_data.json is stored readable, the page is not

`export.py` writes `site_data.json` with `indent=1` — 21,471 short lines instead of one
249KB line — so a change to it is legible by eye and in a diff. That matters once the
Yahoo fetcher is writing it: "one score changed" needs to be visible, not "a quarter of
a megabyte changed".

**`mksite.py` re-compacts it on the way into the page** (`json.dumps(..., separators=(',',':'))`).
Do not remove that: embedding the indented form would add roughly 100KB to every
visitor's download for no benefit. `index.html` is byte-identical either way — verified.

`site_data.json` is gitignored. It is generated, so committing it invites drift from
`data.py`, which is the actual source of record.

### Sharing, links and analytics (added 2026-08-28)

- **`og.png` lives at the repo root**, not in `src/`, because the share tags point at
  `https://deadshot-iota.vercel.app/og.png`. It is generated by a script kept in the
  session scratchpad, not by the build — if the stats on it go stale, regenerate it.
  `deploy.sh` copies it up alongside `index.html`.
- **Favicon is an inline SVG data URI** in the head, so the "no image files" property
  of the build still holds.
- **Deep links:** `?y=YYYY` sets both year-driven sections, `?m=Manager` sets the career
  chart, and `#section` still scrolls. `applyUrlState()` runs on a `setTimeout(...,0)`
  deliberately — the page has initial draws that would otherwise overwrite it. The
  address bar is updated from the button the reader actually clicked, not read back off
  the DOM, because two different pickers share the `y` parameter.
- **Analytics** is Vercel Web Analytics, injected only when `location.protocol` is
  http(s). Loading it unconditionally 404s under `file://`, which is how every test in
  this repo runs, and that failure shows up as a console error and fails `test.js`.
  It stays inert until Web Analytics is switched on in the Vercel dashboard.
- **Focus is trapped** inside both overlays (`trapTab`). Before this, Tab walked out of
  an open dialog and into the page behind it 19 times out of 20.

### Link previews are per-theme, and that needs a shim

Discord, iMessage and the rest fetch `og:image` **server-side from the URL alone**. They
never see the reader's theme, and the site is one static file, so a single `og.png` could
only ever show one of the six — which is how a stranger ended up being greeted by the
hidden Redacted theme.

`mkog.js` renders one 1200×630 card per theme from the live stylesheet (`node mkog.js`,
and `deploy.sh` runs it on every deploy so the season counts on the card cannot go stale)
and writes a matching one-line shim page to `t/<skin>.html`. The shim carries that theme's
og tags for a crawler and bounces a person straight to `/` with their query and hash
intact. `deepLink()` points a shared link at the shim for whatever theme the sharer is on.

- **Redacted maps to Classic on purpose.** The hidden theme should not be the first thing
  a stranger sees.
- `cleanUrls` is on in `vercel.json`, so links are `/t/red`, not `/t/red.html`. Emitting
  the `.html` form would cost every crawler a redirect hop.
- This is deliberately **not** a serverless function. It stays a static site.
- Adding a theme means adding it to `SKINS` in `mkog.js` **and** `OG_SKINS` in the page,
  then re-running the generator.

### It installs as a home-screen app

`manifest.webmanifest` names it, `sw.js` keeps a copy on the device, and the build writes
`sw.js` itself so its `VERSION` string changes whenever `index.html` changes — an old
store can never outlive the page it belongs to. **VERSION is a content hash, not a
length.** It was `len(out)` first, which meant two builds of equal length shipped a
byte-identical worker: the browser saw no change, never ran `activate`, and every cached
icon and font stayed pinned to the previous build. A same-length edit is mundane on a
660KB page.

**Three rules the worker learned the hard way, all reproduced before they were fixed:**

- **Never store a response that is not a healthy same-origin 200.** The navigation branch
  had no `net.ok` check, so one tapped dead link wrote a 404 page over the stored book and
  the installed app opened to "404 — This page could not be found" on every no-signal
  launch until the site was next loaded online. Captive portals and deploy-window 5xx do
  the same thing.
- **Never key a navigation response as `/` without checking the path.** Every in-scope
  navigation entered that branch, so a shared `/t/<skin>` link wrote a 2KB redirect stub
  over the book — and offline that stub redirects to itself. `/t/*` is now handled
  separately and falls back to the stored book.
- **Network-first must be raced against a clock.** `fetch()` only rejects when the network
  is properly down; one bar does not reject, it stalls. Without a timeout the reader got a
  blank screen with a complete copy sitting unused. It now falls back after 3.5s and lets
  the fetch finish in the background so the next open is fresh.

Fonts are requested with `crossorigin` so their responses have a real status to check —
without it every font response is opaque, indistinguishable from a captive portal's block
page, and a bad first visit poisoned the fonts for good.

**The page is fetched network-first, and that is the whole point.** The obvious way round
(serve the stored copy, refresh in the background) leaves every reader one launch behind
every deploy, which is how a site like this quietly stops updating. Fonts and icons are
cache-first instead, because they never change within a version. `skipWaiting` plus
`clients.claim` means a new version takes over immediately rather than waiting for every
tab to close.

Registration is gated on https or localhost, so opening `index.html` off the disk is
unaffected and stays testable. `vercel.json` marks `sw.js` no-store — a cached copy of the
thing that manages the cache is the classic way to strand everybody on an old build.

Verified end to end against a local server: manifest valid, worker takes control, the full
book (10 plates, 10 rows) and all four typefaces render with the network off, and an edited
page is seen on the very next open rather than the one after.

### Links that open on one exact thing

A picture is for the group chat; a link is for an argument, because the other person
lands on the live page and can keep digging. `applyUrlState()` reads:

- `?y=` — the season (drives both year-driven sections)
- `?w=` — the week inside the weekly scoreboard
- `?m=` — the manager on the career-races chart
- `#section` — where to scroll

All four are written back to the address bar as the reader clicks, so the URL is always
already shareable. Explicit **Copy link** buttons sit on the manager card, the Seasons
standings header and the weekly scoreboard. One delegated handler serves every one of
them: put `data-link="y=2024&w=11"` and `data-link-hash="weekly"` on any button and it
works with no wiring. Values in `data-link` are **raw, not URL-encoded** — `deepLink()`
does the encoding, so encoding them in the attribute double-encodes them.

### Browser find (Cmd+F)

Most of the page is rendered one view at a time, which the browser's find cannot see
into. Audited 2026-08-28:

- **Managers: 20/20 findable.** Names appear in the always-rendered All-Time table.
- **Teams: was 37/73.** The Seasons section renders a single year, so 36 historic team
  names were unreachable. Fixed by adding `#teamIndex` — every team name ever, with its
  manager and years, inside a closed `<details>` in `seasons`. Chrome opens a collapsed
  `<details>` automatically when find matches inside it, so this costs nothing visually
  and makes all 73 reachable.
- **The 18 weekly scoreboards** are closed `<details>` and are already findable for the
  same reason. Do not "fix" them by forcing them open.
- **Still not findable, and cannot reasonably be:** text drawn inside charts (SVG
  `<text>` is not matched by browser find) and the three `hidden` panels (`#fChips`,
  `#rankTbl`, `#advYrChips`). All three only duplicate content that is findable
  elsewhere. `hidden="until-found"` would work if that ever stops being true.

**The bracket card reads its shape from the data.** Two exist in this league's history —
a 4-team bracket (two semifinals into a final) and a 6-team one (two quarterfinals plus
two first-round byes, into semifinals, into a final) — so the columns come from the weeks
that actually have games and the rounds from `g.rnd`, never from an assumed shape. Three
things it learned:

- **placement games do not belong in the columns.** The 5th and 3rd place games are part
  of the record but not the title path, and mixing them in made the card unreadable. They
  sit in an "also played" strip underneath.
- **columns are capped at 360px and the block is centred.** Letting two columns fill the
  full width stretched a 4-team bracket into long empty strips.
- **the champion's name is placed off its measured ascent**, not a fixed baseline. Big
  Shoulders has a very tall ascender and a fixed baseline drove the name straight through
  its own CHAMPION label.

A void final (2022) is labelled VOID, draws no connector onward, and the champion band
says CO-CHAMPIONS with both names.

### The card audit

`scratchpad/audit/cards.js` renders every card the site can produce — manager, head to
head, season, receipt, record, roast, rivalry and every Wrapped slide — in all six skins,
about 3,200 renders, and flags any ink in the gutter between the last line a card may use
(y 950) and the top of the footer text (y 986). Two things it learned the hard way:

- **do not test for "not the background colour".** The manager card's footer is
  left-aligned, so a check that ignored the middle third counted the footer itself.
- **do not compare against a flat colour.** The Wrapped cards are gradients. It tests for
  a sharp *vertical* edge instead (each pixel against the one four rows above), which
  text always makes and a smooth gradient never does.

### The two bump charts

`#race` ("The race", in `weekly`) is **season-scoped** — `drawWeekly(YR)` rebuilds it from the season
pills, one line per team.

`#crace` ("Career races", in `rankings` &mdash; it is manager-centric and cross-season, so it does not belong under the Week by Week season picker) is **manager-scoped and cross-season** — one line per season
for a single manager, drawn by `drawCareerRace()`, registered in `REDRAW` only (never
`WKREDRAW`), so the season pills do not touch it. It reads `D.wkYears`, so it can only
ever show 2021–2025; the caption says so rather than silently drawing a short career.

Seasons are told apart three ways at once, deliberately — several managers reused one
team name for years (Shane Kaiper was "Stegostompem" all five), so the team name alone
identifies nothing:

1. **its own hue**, keyed to the *year index across the whole league*, not to the
   manager's position in their own list — so 2021 is the same colour on every manager's
   chart and two managers can be compared side by side. The hues live in per-skin tokens
   `--sea-1` … `--sea-8` (eight, for headroom; `seaK()` wraps past eight). They are
   per-skin because the six grounds are completely different — a hue that reads on
   Crimson's white disappears on Arcade's purple-black. Every one clears WCAG 3:1
   against its own `--surface` (measured minimum 4.43, on Crimson);
2. a year label at the end of every line;
3. a clickable season legend, each entry carrying a solid swatch in that season's colour.

This replaced an earlier single-hue brightness ramp (faint neutral → full accent, with
stroke weight rising alongside). It was not enough: on several skins the middle years
blurred into each other, and brightness alone dies in a screenshot. Stroke weight is now
uniform (2.4px) and every line is solid.

Two things were built for this chart, shown to the owner, and **rejected — do not
reintroduce them**:

- **a year tag riding on each line.** Noisy, and the tags have to dodge each other
  wherever lines bunch up.
- **a dash pattern per season** (solid / dashed / dotted / dash-dot), added as a
  colour-blind-safe second cue. With five clearly separated hues it only added visual
  noise. Colour alone is the answer here.

Medals on the end labels are positioned **after render, off `getBBox()`** &mdash;
`getComputedTextLength()` ignores the `dx` between the year and team-name tspans and
put the medal on top of the last letter. Three seasons can finish in the same place
(Wesley Alpert finished 2nd three times), so labels are fanned 16px apart.

Both charts bake colours into markup, so both must stay in `REDRAW` or a theme switch
leaves them stale. Both use a 980-unit `viewBox` scaled to the container, which means
**both become very small on a phone** (~312px wide at 390px viewport). That is
pre-existing behaviour shared by the whole chart family, not specific to either one.

### Themes

Six, set via `data-skin` on `<html>` and persisted to `localStorage['deadshot.skin']`:
`og` (Classic — always the default for first-time visitors), `scope`, `red` (Crimson),
`leather` (Pigskin), `arcade`, and `redact` — hidden, only selectable once
`localStorage['deadshot.clearance'] === '1'`.

All colors are CSS custom properties per skin (`--brass`, `--surface`, `--ink`,
`--pos`, `--neg`, …). **Never hardcode a color in a component** — every one of the six
skins has to survive it.

### Easter eggs

- **6 clicks on the masthead reticle** (`.mast .scope`) — escalating warnings, a klaxon
  that builds, and a sniper shot that cracks the page open into the Redacted theme.
- Type **`commish`** or **`commissioner`** — the Pharaoh.
- Type **`cossu`** — "Cossu is a bot".
- Type **`chaos`** — scrambles every number on screen and knocks the charts out of
  alignment, then restores exactly.
- Type **`burke`** — a panda, and a nod to the name he has played under since 2022. Ten
  seasons out of ten and a scoring line that barely moves; black, white and bamboo.
- Type **`kaiper`** — amber, ripples, a tremor and a pterosaur cry. Ten seasons, seven of
  them under the same prehistoric team name.
- Type **`wu`** — lacquer red and gold leaf, with a carver's seal. The seal carries his
  season count in Chinese numerals, because that is a fact rather than a decoration.
- Type **`gearing`** — 49ers scarlet and gold, yard lines and a crowd. He keeps one of the
  twenty field-level seats the 49ers added at Levi's in the 2026 rebuild.

**Every card stays on screen for 5250ms and fades over 700ms.** Cossu's is the exception
at 3250ms. Keep new ones on the same clock.

**Each manager answers to their first name and their surname**, from one `EGGWORDS` table
rather than a wall of `if`s — the loop `break`s on the first match so two words can never
fire two cards. Two deliberate exceptions:

- **Burke is surname-only.** `brian` belongs to the commissioner, and this league has two
  of them.
- The commissioner answers to `commish`, `commissioner`, `berger` and `brian`. That egg
  guards itself with `PH_BUSY` while it runs, so a test that fires it twice in a row will
  look like a broken trigger when it is not.

Six sounds have been rejected by the owner and replaced. Recorded so they do not come
back, and because the reasons generalise:

- a synthesised laugh for the champion — replaced with `battleReady`, war drums and a horn
  climbing to the top note;
- a pterosaur cry for Kaiper — dropped; the footfalls carry it;
- a bell on the end of Wu's gong — replaced with `villageCalm`;
- a projector and applause for Contreras — replaced with `vaultCrack`, because the card
  is now about the robbery rather than the premiere;
- **two** goes at McMahon's basketball. Same lesson as the crowd, learned twice: a bounce
  built from a sine reads as a game console. A real one has no note in it — it is a
  broadband slap that collapses downward in about forty milliseconds, so `bounce()` is
  four layers of filtered noise and no oscillator at all;
- **two** goes at the crowd for Gearing. The lesson is worth keeping: **do not put a
  pitched oscillator in a crowd.** The second attempt used nine sawtooths as "voices" and
  they read immediately as an arcade cabinet. `fansCheer` is now noise and nothing else —
  four beds, four sections offset from each other, and 170 short band-limited bursts of
  random length, loudness and colour.

`screech`, `evilLaugh`, `gong` and `crowdRoar` were deleted once nothing called them.

- Type **`niko`** — a lit marquee, billed the way a cinema bills a picture: the film goes
  up in lights (**BACK 2 BACK**) and the manager takes a director's credit underneath it,
  then a poster's small print. The card checks that the two titles really were consecutive
  and that the second one really was the lowest-scoring champion on record before it says
  either.
- Type **`alpert`** — a trading terminal. His five seasons are plotted as the line they
  actually make, 113.5 down to 94.2, with a closing bell.
- Type **`mcmahon`** — a basketball. League lore says he is unguardable on a court; the
  record says he cleared the league average in 2025 and went 5-9 anyway.

All seven read their numbers out of `loyalFacts()` and `ROWS`, so counts and streaks stay
true. If someone leaves the league, or a name changes, the cards follow.

**Every superlative on these cards is checked against the field before it is printed.**
Two were wrong when first drafted and would have shipped as confident lies: McMahon is the
**second** unluckiest on record, not the first (that is the owner, at -12.30), and Alpert
has the highest rating of anyone **still playing**, not of all time (Giacomo Watson is
higher). Both now compute their rank at draw time. Do not hardcode a "most" or a "best"
here — sort `M` and check.

**An inline `display` beats the `hidden` attribute.** The trade grid carries an inline
`display:grid`, so `[hidden]{display:none}` from the browser's own stylesheet lost to it
and the trade cards stayed on screen the whole time their card said "collapsed". The fix
is a single site-wide `[hidden]{display:none!important}`. Anything using `hidden` on an
element that also sets `display` inline had the same latent bug.

**Every sound is rendered offline and measured before it ships.** Two of the seven came
out inaudible on the first pass — the projector at peak 0.045 and the crowd at 0.09 — and
neither is something you notice by ear on a laptop. Render into an `OfflineAudioContext`,
measure peak and RMS, and only trust the number.
- Type the **reigning champion's surname** — a red-and-gold title-defence card. The
  trigger is generated from `D.champs` for the latest season (`CHAMP_KEYS`), so it follows
  the trophy rather than naming anyone permanently; today it is `krueger`. Co-champion
  years arm both surnames. The "henchman" line only fires for the team that earned it.

All four typed words are guarded against firing while an `input`, `textarea` or `select`
has focus.

All audio is synthesized with the Web Audio API. There are zero audio assets.

---

## 6. Conventions and traps (learned the hard way — please keep)

> `CLAUDE.md` in this directory carries these as standing rules and is loaded
> automatically every session. Keep the two in sync if you change one.

0. **`mksite.py` is ~250 KB / 3,550 lines — about 65k tokens. Never read it in
   full.** One such read eats most of a context window. `grep -n` for the anchor,
   then read a narrow window around it.
1. **Never edit `index.html`.** It is generated. Edit `mksite.py` and rebuild.
2. **Assert before you write.** When patching `mksite.py` with a script, assert the
   anchor string matches exactly once *before* opening the file for write. Several
   edits were silently lost to a script that threw on a stale anchor after having
   already made other changes in memory. Then `grep` to confirm.
3. **Class name collisions.** `mksite.py` is one giant stylesheet. A new `.brand` class
   silently inherited the masthead's `.brand`; a new `.totop.on` inherited the global
   `button.on` styling. Grep for a class name before you introduce it.
4. **`@keyframes` collisions too** — `sweep` was defined twice and the wrong one won.
5. **`position:fixed` under a transformed ancestor** does not anchor to the viewport.
   `<body>` is transformed during some effects; a fixed overlay stretched to the full
   20,000px document and smeared off-screen. Shake `.mast, nav, .wrap` instead of `body`.
6. **Circular CSS variables** (`--x: var(--x)`) are invalid and fail silently.
7. **Duplicate `id`s** — an inner element reusing `id="method"` meant
   `$('#method').innerHTML =` wiped the entire section.
8. **Apostrophes in single-quoted JS strings** — `2021's` broke the whole page.
9. `$` and `$$` are `querySelector` / `[...querySelectorAll]` helpers, defined once.
10. Per-season sections show that year's actual field; they are deliberately **not**
    filtered by the global Active-10 manager filter.

---

## 7. Deploy

Repo: **TheProphetHasRisen/Deadshot** (public, default branch `main`). Vercel serves it
at <https://deadshot-iota.vercel.app>. The repo holds `README.md` and `index.html` only.

```bash
./deploy.sh              # build + verify, no push (safe default)
DEADSHOT_REPO=TheProphetHasRisen/Deadshot ./deploy.sh --push
```

`deploy.sh` runs `export.py` + `mksite.py`, `node --check`s the inline script, runs
`test.js`, refuses to push if `node` is missing or the file looks truncated, then commits
`index.html` to `main` in one commit. Auth is `gh` (`gh auth login --web`); the token
lives in the macOS keyring. **Never ask for or accept a personal access token.**

### The old way, and why it went

Dragging the file onto GitHub in the browser still works, but Chrome saves it as
`index_36.html` when a copy is already in the downloads folder, so each deploy became
three commits — *Delete index.html*, *Add files via upload*, *Rename index_35.html to
index.html* — and once took the site down with a 404. If you do deploy by hand: the
filename must end up exactly `index.html`, and do not delete the old file first.

---

## 8. Fixed issues

### Wrapped story player — final-card buttons were unclickable (fixed 2026-08-26)

**Symptom:** on the final Wrapped card, "Back to career" did nothing and "Play again"
went back exactly one card instead of restarting.

**Cause:** the invisible tap zones sat above the buttons. `.wr-nav.l` (left 34%) and
`.wr-nav.r` (right 66%) are `z-index:5`. The buttons live in `.wr-btns` inside
`.wr-card`, which was `z-index:4` — and because `.wr-card` establishes a stacking
context, the `z-index:7` on `.wr-btns` could not escape it. Every click landed on a nav
zone: "Play again" fell in the left third -> `wrGo(-1)` -> back one card; "Back to
career" fell in the right two-thirds -> `wrGo(1)` -> no-op on the last card.

Both symptoms were the one bug. `wrPaint()` had always reset the bars correctly when
`WR.i===0`; "Play again" only looked like a one-card rewind because the click was
reaching `#wrPrev` and never reaching the button.

**Fix**, in the `HEAD` string of `mksite.py`:

```css
.wr-card{ z-index:6; pointer-events:none; }   /* was z-index:4 */
.wr-btns{ pointer-events:auto; }
```

**Note for future edits:** `.wr-card` is now click-through by design, so taps on card
text intentionally fall through to the nav zones underneath — that is what makes
tap-to-advance work. Any new interactive element added inside `.wr-card` needs its own
`pointer-events:auto` or it will be dead to the mouse.

**How it was verified** — the same script was run against a pre-fix build to prove it
discriminates. Pre-fix, `document.elementFromPoint` at each button's centre returned
`wrPrev` / `wrNext` and Playwright refused to click at all ("`wrNext` intercepts pointer
events"); post-fix both return themselves. Confirmed on the last card that both buttons
respond, "Play again" resets to card 1 with every progress bar cleared, and "Back to
career" closes only the story overlay with the manager modal still open underneath —
across all six themes on desktop and mobile, 0 `pageerror`. Tap-to-advance, the X button
and Escape were re-checked for regressions.

---

### Later fixes in the same session (2026-08-26/27)

All verified headless across six themes and 320-2560px, 0 `pageerror`.

| Fix | Was | Now |
|---|---|---|
| Wrapped card content looked clickable | `.wr-nav` carried `cursor:pointer`, and since `.wr-card` is click-through the pills and headline inherited it | `.wr-nav{cursor:default}` — only the real buttons show a pointer |
| Records tables needed sideways scrolling to see the number | global `th,td{white-space:nowrap}` pushed the value past the card edge; **8/21 cards clipped at 1400px, 9/21 at 390px** | `#recs` lets the manager/team columns wrap and the `/14g` suffix drop a line; 0/21 clip at every width tested |
| Masthead reticle scrolled away | `.navmark` sits inside `.nav-in`, which is `overflow-x:auto` | `position:sticky;left:0`, backdrop layered twice to ~99.6% opacity; `.nav-ar.l` moved to `left:50px` and the fade to `left:46px` so they clear it |
| Easter-egg toasts crushed on phones | `.toast` is `position:fixed;left:50%` with no width, so shrink-to-fit capped at **half the viewport** — 195px on a 390px screen | `width:max-content;max-width:min(92vw,460px)` |
| Redacted dossier text unreadable on phones | the dossier SVG is `preserveAspectRatio="none"`, so on a phone the stamp and file marks were scaled **7.2:1** (0.279 x vs 2.009 y) | stamp and meta are real HTML elements over the SVG, sized in CSS px; the SVG keeps only the bars, which stretch fine |
| Bracket connector SVG exposed to screen readers | no `aria-hidden` | `aria-hidden="true"` — it is decorative, the bracket content is in sibling divs |
| Wrapped blobs animated under `prefers-reduced-motion` | only `.dossier *` was covered | `.dossier *,.wr-blob` |

**Both latent hazards from that audit have since been fixed (2026-08-28):**

1. `data-m` was overloaded — the manager-link attribute (`closest('[data-m]') ->
   openMgr(...)`) was reused by four Season Shape buttons as a *metric* key. It only ever
   worked because `openMgr` bails on an unknown name. Those four now use `data-bal`.
   Keep `openMgr` defensive anyway, and use a different attribute for new controls.
2. The masthead `.dossier` SVG had no closing `</svg>`; the browser recovered because the
   following `</div>` implicitly closed it. Now closed properly. Anything added after
   those elements would otherwise have landed *inside* the SVG.

## 9. Backlog

- **2026 live section** — standings, weekly matchups, rolling power rankings, playoff
  odds. Blocked on a live data source.
- **Yahoo API** — the intended replacement for hand transcription. Plan of record: the
  league owner registers the app and stores the refresh token in GitHub repo secrets; the
  fetcher runs as a scheduled job and never exposes the token to a coding agent. Scraping
  the HTML was tried and abandoned (see `yahoo_scrape_status.md`): grouped two-row
  `<thead>` shifts column indices, team defenses live under `/nfl/teams/` not
  `/nfl/players/` so DEF was silently dropped, and Yahoo rate-limits to a 16-byte
  "Request denied" after roughly 120 rapid fetches.
- **Split `data.json` out of the HTML** — worth doing once something other than a human
  writes the data file. Not before.
- **2015–2020 weekly logs** — only season totals exist for those years; every week-by-week
  feature is dark for them.
- **Trade grading** — score each side of a trade by what the pieces actually produced
  afterwards, plus the manager's W-L in the weeks following.

---

## 10. Owner preferences

Brian owns the league and built this site with AI help. **He is not an engineer.**
`CLAUDE.md` carries the full rules under "Who you are talking to" — keep the two in
sync. The short version:

- Lead with what changed and whether it worked. Plain English.
- No file paths, line numbers, function names, or jargon unless he asks.
- Short. No reasoning unless he asks for it.
- Say plainly when something is broken, and what it means for the site.
- **Claude makes the technical decisions.** Never ask which library, which approach,
  or how to structure something — pick, then say what you picked. Bring him a
  decision only when it is his: look and feel, what to build next, anything that
  costs money, anything that cannot be undone.
- When he has to do something himself, walk him through every click and screen and
  say what he should see when it worked.
- Deploy without asking. Do not ask for or accept a GitHub personal access token.
