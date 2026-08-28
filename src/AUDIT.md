# Cross-theme visual audit — 2026-08-27

## Status: COMPLETE

**Scope checked:** all six themes (`og`, `scope`, `red`, `leather`, `arcade`, `redact`)
at 375, 390, 768, 1024, 1440, 1920px — 36 combinations. Per combination: horizontal
overflow on `<body>`, element/text overlap, text clipping/truncation, 4.5:1 (3:1 for
18px+) contrast, all nav arrows/buttons/toggles reachable, a manager modal opened,
Wrapped run to the last card, both exits (Back to career and Escape) exercised, chaos
triggered and its restoration checked exactly. At 390px specifically: the 6-tap reticle
sequence through breach into the Redacted theme, plus `commish`, `cossu`, and `chaos`,
all screenshotted.

**Fixed — three real, clearly-broken defects, all cross-theme, all verified before and
after with rebuild + `node --check` + `node test.js`:**

1. **Power Rankings ladder columns overlapped on every phone width ≤720px, every
   theme.** Score and win% digits rendered on top of each other ("102.9" colliding with
   "51.7%"). A `grid-template-columns` reserved tracks for two columns that
   `display:none` had already removed from grid layout, shifting every later column
   left by one. [mksite.py:445](mksite.py#L445) — the single most severe finding.
2. **Colour-coded number badges (Power Index heat, head-to-head matrix, trade grid)
   failed WCAG contrast — 39 of 244 on the Classic theme alone, worst case 2.52:1.**
   Root cause was systemic: three call sites picked white-vs-dark text off a flat
   threshold on the *input value*, not the *actual rendered colour*. Rebuilt on real
   luminance math with a mathematically-guaranteed fallback (`max(contrast-to-white,
   contrast-to-black) >= ~4.58` for any background) — the first attempt using only the
   theme's own ink token wasn't sufficient and failed on 5 of 6 themes before the
   fallback was added. [mksite.py:1508](mksite.py#L1508).
3. **The "Champion" bracket-card label failed contrast on 4 of 6 themes** (worst 2.47:1,
   `arcade`), a hardcoded accent-token pairing that had never been checked. Reused the
   fix from #2 rather than inventing a second mechanism. [mksite.py:2738](mksite.py#L2738).

**Also fixed, at your request** (a "harmless" hazard the prior session had documented
but left unfixed): the `data-m` attribute collision, where four unrelated buttons reused
the manager-link attribute — renamed to `data-bal`.

**Still broken:** nothing found. The one anomaly in the 36-combination matrix — a click
timeout on `redact @ 1920` — was investigated and retested in isolation, where it
succeeded in under a second; it was a resource-contention flake from running many
concurrent browser processes during this audit, not a reproducible defect.

**Chosen not to touch, and why:**
- **26 borderline contrast findings on `—`/`·` placeholder characters** (4.24:1 vs
  4.5:1 required) — the dimmed tertiary text token used everywhere for de-emphasized
  meta text, carrying minimal information, 0.26 short. Fixing it site-wide is a visual
  weight decision, not a contained bug fix.
- **`scope` theme's decorative HUD text touching the champions footer's bounding box**
  — verified by screenshot that no actual glyphs collide; it sits in nearby whitespace.
  Cosmetic.
- **Several other flagged "overlaps"** (the back-to-top button's arrow, a wrapped
  caption, a collapsed `<details>` paragraph) — each individually verified as a
  measurement artifact in the audit harness itself (an ancestor's `opacity:0` or
  `content-visibility:hidden` not filtering out correctly), not a real visible defect.
  Detailed below so the harness's own limitations are on record too.
- **The nav row's scroll-right arrow overlapping the last visible tab** — confirmed
  intentional: a standard "more content, keep scrolling" carousel-arrow affordance.

Nothing was pushed or committed — this directory isn't a git repo, so the working files
themselves (`mksite.py`, rebuilt `index.html`/`site_data.json`) are the deliverable, left
as-is for your review.

---

## Pre-audit: harmless latent hazards from the prior session

- **`data-m` attribute collision** (documented in HANDOFF.md section 8 as a known trap,
  left unfixed there): four Season Shape buttons reused the manager-link attribute
  `data-m` for an unrelated purpose (selecting a balance-chart metric: `sd`/`wsd`/
  `rng`/`lg`). Harmless only because `openMgr()` bails silently on an unknown name.
  **Fixed**: renamed to `data-bal` on the four buttons and their three consumers
  ([mksite.py:1179-1182](mksite.py#L1179), [2447-2448](mksite.py#L2447),
  [2450](mksite.py#L2450)). Verified `data-bal` was unused before introducing it.
- **Unclosed `<svg>` in the dossier block**: already fixed in the prior session (moving
  the stamp/meta text out of the SVG into real HTML also closed the tag). Confirmed
  `<svg>`/`</svg>` counts balanced (26/26) before this audit started.

Rebuild after the `data-bal` rename: `node --check` clean. `node test.js` result below.

`node test.js` after the `data-bal` rename: **NO JS ERRORS**, all row/cell counts
unchanged from the pre-rename baseline (board 10, allRows 10, bal 2, etc. — identical
to every prior run this session). Kept.

---

## Real finding #1: Power Rankings ladder — score/win% columns overlapped on mobile

**Severity: high.** Confirmed at every width ≤720px, every theme (shared CSS) — the
score, win%, and streak columns of the Power Rankings ladder rendered on top of each
other. "102.9" and "51.7%" collided into unreadable overlapping digits. This is the
single most severe defect found in the audit.

**Root cause:** [mksite.py:445](mksite.py#L445), the `@media(max-width:720px)` block:

```css
.lad-head,.lad{grid-template-columns:22px minmax(72px,1fr) 0 46px 52px 38px 0}
.lad-ev{display:none}
.lad-track,.lad-track-h{display:none}
```

`.lad-track` and `.lad-ev` are `display:none` at this width — which removes them from
CSS Grid auto-placement *entirely*. But the template still reserved 7 tracks for the
7 DOM children. With only 5 children left to place (`lad-r`, `lad-n`, `lad-s`, `lad-w`,
`lad-mv`), grid auto-placement packed them into the *first* 5 tracks in order — so
`lad-s` (the score) landed in track 3, the `0px` slot meant for the now-invisible
`lad-track`. A 0-width cell doesn't clip its text, so "102.9" spilled outward and
overlapped `lad-w` next to it, which had itself landed one track short of where it
should be.

Confirmed via computed `grid-template-columns` before the fix: `lad-s` measured
`0px` wide; `lad-w` got 46px (meant for `lad-s`); `lad-mv` got 52px (meant for
`lad-w`) — every column shifted, not just the first one.

**Fix:** reserve tracks only for what's actually still in the grid —

```css
.lad-head,.lad{grid-template-columns:22px minmax(72px,1fr) 46px 52px 38px}
```

5 tracks for 5 remaining children. `lad-n` (manager name) also picked up the slack
from the two removed slots — 72px → 87px measured, more room for names before they
ellipsis.

**Verified:**
- Computed columns after: `22px 87px 46px 52px 38px`; `lad-s` measured 174–220 (46px,
  matches spec), `lad-w` 230–282 (52px), `lad-mv` 292–330 (38px) — no overlap, real
  gaps between every column.
- Screenshot after the fix: [audit-screenshots/findings/zoom-rankings-rows.png](audit-screenshots/findings/zoom-rankings-rows.png)
  — every score, win%, and streak indicator in its own column with real gaps between
  them. Before-fix state (the overlapping "102.9"/"51.7%" digits) is reproducible by
  diffing against the pre-fix backup this session kept in the scratchpad
  (`mksite.bak5.py`), not copied into the project since it's a superseded intermediate,
  not a deliverable.
- Width sweep 320/375/390/430/600/719/720/721/768/1024/1440/1920px — **0 column
  overlaps, 0 body horizontal overflow at every width**, including both edges of the
  720px breakpoint.
- `node --check` clean. `node test.js`: **NO JS ERRORS**, all row/cell counts
  unchanged (board 10, allRows 10, bal 2, etc.).

This was found by the general-purpose overlap heuristic in the matrix harness (below),
then hand-verified with a targeted script because the heuristic's raw hit count (30,
capped) was mostly noise from unrelated false positives — see the harness
false-positive note further down. This one held up under inspection; most others in
that batch did not.

---

## Real finding #2: heatmap text colour used a flat threshold, not real contrast — systemic, all themes

**Severity: moderate-to-high, theme-dependent.** Every colour-coded number badge on the
page — Power Index heatmap (`#power`), head-to-head matrix (`#h2h`), trade-year grid
(`#trades-sec`) — decides white-vs-dark text by testing the *input value* against a flat
cutoff, not the *actual rendered background colour*. The two curves drift apart because
the background mix itself is nonlinear (`Math.pow(t,.7)*.85` / `Math.pow(t,.72)*.82`,
capped short of full saturation), so the cutoff doesn't track where contrast actually
flips.

Measured on the Classic (`og`) theme before the fix: **39 of 244 colour-coded number
badges failed 4.5:1**, 19 of those failed even 3:1. Worst case: white text on
`rgb(112,170,207)` measured **2.52:1** — nowhere close.

**Root cause**, three call sites, [mksite.py:1508-1512](mksite.py#L1508) and the two
heatmap builders:

```js
const inkOn=(v,span)=>Math.abs(v)/span>0.62?'#fff':'var(--ink)';                          // Power Index heat
color:${t>.6?'#fff':'var(--ink)'}   // background: mix(surface,brass,pow(t,.7)*.85)       // H2H matrix (x2 sites)
```

Both are proxies — "is the input far enough from center" — standing in for the real
question, "does white or ink actually read better on this pixel." They happened to work
well enough on some themes/ranges and failed on others.

**Fix:** compute real WCAG relative luminance from the colour that's actually being
rendered, and pick whichever text colour wins:

```js
function relLum(hex){...}
function contrastHex(a,b){const L1=relLum(a),L2=relLum(b);return (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);}
function pickInk(bg){return contrastHex(bg,'#ffffff')>=contrastHex(bg,cssv('--ink'))?'#fff':'var(--ink)';}
const inkOn=(v,span)=>pickInk(diverge(v,span));
```

The two H2H/trade-grid call sites now compute the mixed background once into a local
`bg`/`bg3`, use it for both the `background` and `pickInk(bg)` — so the colour that's
judged is the exact colour that's painted, not a re-derivation. `cssv('--ink')` is read
live per theme, so this holds on all six skins without hardcoding anything (`--ink`,
`--pos`, `--neg` are confirmed hex in every skin block, checked before writing this).

**First attempt wasn't sufficient.** "Pick whichever of `#fff` / `var(--ink)` has more
contrast" swept `og` clean (worst 4.52:1) but **failed on five of the other six themes**
— `scope` 26 badges under 4.5:1, `red` 6, `leather` **65**, `arcade` 17, `redact` 7.
Leather's worst case measured **1.33:1** — because on those themes neither candidate,
white or that theme's own `--ink` token, actually clears 4.5:1 against some of the
mixed heat-cell backgrounds. Picking the *better* of two options doesn't guarantee
either one is *good enough*.

**Real fix:** fall back to true black/white when neither theme option clears the bar.
This isn't a guess — for any background colour, `max(contrast-to-white,
contrast-to-black)` is mathematically bounded below by the point where the two curves
cross, which works out to **~4.58:1**, just above the 4.5:1 requirement. So checking
plain black/white as a last resort *guarantees* the threshold is met regardless of
theme or background:

```js
function pickInk(bg){
  const white=contrastHex(bg,'#ffffff'), ink=contrastHex(bg,cssv('--ink'));
  if(Math.max(white,ink)>=4.5) return white>=ink?'#fff':'var(--ink)';
  return contrastHex(bg,'#ffffff')>=contrastHex(bg,'#000000')?'#fff':'#000';
}
```

The theme's own `--ink` token is still preferred whenever it actually works — this only
overrides on the specific cells where it doesn't.

**Verified, all six themes, after the real fix:**

| theme | badges | worst ratio | under 4.5:1 |
|---|---|---|---|
| og | 244 | 4.52 | 0 |
| scope | 244 | 4.76 | 0 |
| red | 244 | 4.58 | 0 |
| leather | 244 | 4.61 | 0 |
| arcade | 244 | 4.52 | 0 |
| redact | 244 | 4.52 | 0 |

Every worst-case ratio sits right at ~4.52–4.76 — exactly where the black/white
crossover math predicts, confirming the fallback is doing the work on the themes where
`--ink` alone couldn't. `node --check` clean; `node test.js` after this fix: **NO JS
ERRORS**, all counts unchanged (board 10, allRows 10, mtx 90, etc.) — kept.

This is a genuine accessibility defect, not a cosmetic one — WCAG 4.5:1 is a hard
requirement the user explicitly asked to verify, and 16% of colour-coded numbers on the
page failed it. Scope stayed tight: two small pure functions, three call sites, no
change to the colour palette, the mix math, or anything visual beyond which of two
already-defined text colours gets used per cell.

---

## Real finding #3: "Champion" bracket-card label failed contrast on 4 of 6 themes

**Severity: moderate.** Found while triaging the matrix run's `contrastFails` for `og` —
28 flagged, 26 of which are a borderline dash/dot placeholder (documented and left alone
below), but one was real: the "Champion" / "Co-champions" label on the bracket's winner
card, [mksite.py:2738](mksite.py#L2738).

**Root cause:** static CSS, `.brk-champ .s{color:var(--brass-2)}` against
`.brk-champ{background:var(--brass-wash)}` — a fixed accent-token pairing that was never
checked for contrast, same anti-pattern as finding #2 but hardcoded in CSS rather than
computed per-cell.

**Measured before the fix, all six themes:**

| theme | ratio | pass? |
|---|---|---|
| og | 2.67 | fail |
| scope | 3.06 | fail |
| red | 4.67 | pass |
| leather | 6.45 | pass |
| arcade | 2.47 | fail |
| redact | 3.83 | fail |

4 of 6 themes failed — this wasn't an `og`-only issue, the matrix run just happened to
surface it there first.

**Fix:** reuse the `pickInk` function from finding #2 rather than inventing a second
mechanism — the label's colour is now computed at render time against the actual
`--brass-wash` value instead of hardcoded to `--brass-2`:

```js
<div class="s" style="color:${pickInk(cssv('--brass-wash'))}">
```

Checked first that `.s` isn't a collision risk (CLAUDE.md's own stated trap) — it's the
only bare `class="s"` in the codebase and the CSS rule is already scoped
`.brk-champ .s`, so no other element is affected.

**Verified, all six themes after the fix:** 14.29–17.89:1 — well clear of the
requirement, because `--brass-wash` is always strongly tinted toward one extreme, so
`pickInk` resolves to near-pure black or white every time rather than needing its
fallback. `node --check` clean; `node test.js`: **NO JS ERRORS**, counts unchanged.

**Left alone — the other 26 `contrastFails` on `og`:** em-dash (`—`) and middle-dot
(`·`) placeholder characters at 4.24:1 against a 4.5:1 requirement. This is `--ink-3`,
the deliberately-dimmed tertiary text token, used everywhere for de-emphasized meta
text — not just these placeholders. The gap is small (0.26), the characters carry
minimal information (an em-dash reads as "no data" whether or not its exact grey hits
WCAG to the decimal), and darkening `--ink-3` sitewide to fix it would be a visual
weight decision across every use of that token, not a contained fix. That crosses from
"clearly broken" into "cosmetic/subjective" per the rules for this pass — documented,
not touched.

---

## Matrix audit

*(Housekeeping note: the first 36-combo pass ran with the harness pointed at the same
`results.json` path as the second pass below, so the raw first-pass data was overwritten
mid-write by the second run. No finding was lost — both real bugs the first pass
surfaced (the ladder grid and the heatmap contrast) are documented and independently
verified above, before this section. The table below is from the second pass: harness
fixed to stop flagging the collapsed manager-checklist as "unreachable" (an ancestor-
visibility bug in the check itself, not the site), both real fixes in place.)*

### Result: 35 of 36 clean; the one exception is a test-environment flake, not a site bug

| theme | 375 | 390 | 768 | 1024 | 1440 | 1920 |
|---|---|---|---|---|---|---|
| og | OK | OK | OK | OK | OK | OK |
| scope | OK | OK | OK | OK | OK | OK |
| red | OK | OK | OK | OK | OK | OK |
| leather | OK | OK | OK | OK | OK | OK |
| arcade | OK | OK | OK | OK | OK | OK |
| redact | OK | OK | OK | OK | OK | **X** |

Every combination: 0 `pageerror`, 0 body horizontal overflow, 0 unreachable controls
(after fixing the checker's own ancestor-visibility gap), 0 real (non-ellipsis) text
clipping, chaos restored every number exactly with 0 mismatches.

**redact @ 1920 flagged an interaction failure**: `page.click('#wrBack')` timed out
after 30s during the automated modal → Wrapped → last card → Back to career flow.
Investigated rather than dismissed: retested that exact combination in isolation
(fresh browser, nothing else running) —

```
mgr: Niko Contreras
r1: {"modalOpen1":true,"wrapOk":{"cards":17,"btnsPresent":true}}
wrBack state: {..."isBtnItself":true}
CLICK SUCCEEDED
pageerrors: 0
```

Modal opened, Wrapped opened with 17 cards, `#wrBack` was correctly the topmost element
at its own center, click succeeded well under a second. By the time this combination
ran (last of 36, after a long session running many concurrent Playwright/Chromium
processes for the other investigations below), the machine was under heavy load — a
30s actionability timeout in that environment is a resource-contention flake, not a
reproducible defect. Confirmed, not fixed, because there is nothing to fix.

### Overlap and clipping categories — heuristic false positives, individually verified

The structural harness's overlap and clipping checks are pairwise/bounding-box
heuristics, not proof of an actual visible defect — each capped-at-30/40 finding was
sampled and traced to a specific mechanism before being dismissed. None were "probably
fine" guesses; each has a concrete measurement or screenshot below.

- **`.totop .ar` (the back-to-top button's arrow) overlapping arbitrary content** — the
  single largest source of overlap noise. `.totop` is `opacity:0;pointer-events:none`
  by default (only visible after scrolling past 640px), but a CSS **child's own computed
  `opacity` doesn't inherit an ancestor's `opacity:0`** — `getComputedStyle` on `.ar`
  reported `opacity:"1"` even though the whole button is invisible. Confirmed via direct
  measurement (`totop.opacity:"0"` vs `ar.opacity:"1"`) and a screenshot at scrollY=0
  showing nothing near the flagged coordinates. Harness bug, not a site bug.
- **`p.plain` (the "In plain English" lambda paragraph) overlapping the Season Shape
  heading** — the paragraph sits inside a native `<details class="expl">`, closed by
  default. Modern Chromium implements closed `<details>` via `content-visibility:hidden`
  on the non-summary content, which still reports a geometric `getBoundingClientRect()`
  for sizing purposes even though nothing paints. Confirmed decisively with the
  browser's own `element.checkVisibility()` API: **`false`**, and `element.innerText`:
  **empty string** — and a screenshot showing only the collapsed "▸ HOW THE SCORE IS
  BUILT" toggle with clean whitespace before "Season Shape." Harness bug, not a site bug.
- **`.nav-ar.r` (the nav row's scroll-right arrow) overlapping the last visible nav
  tab** — confirmed via `elementFromPoint`: the arrow genuinely is the topmost element
  and does sit over the tab's edge. This is intentional: a small opaque button
  affordance floating over the fading edge of a horizontally-scrollable row is a
  standard "there's more, keep going" pattern (same family as a carousel arrow). Not a
  defect — verified deliberate, not fixed.
- **"★ The story of each season" button overlapping its caption** at narrow widths —
  the caption `<span class="sub">` wraps onto a second line below the button; a
  multi-line inline element's bounding rect spans its *entire* run, so it naturally
  overlaps whatever sits beside its first line. Screenshotted at 375px: both lines are
  fully legible, nothing actually collides pixel-for-pixel. Heuristic limitation
  (bounding box vs. rendered glyphs), not a site bug.
- **`scope` theme's decorative HUD readout ("DEADSHOT · OPTIC LIVEMIL-DOT...") overlapping
  the champions-section footer** — the two bounding boxes do intersect (measured), but
  the zoomed screenshot shows the HUD's "HOLD CENTRE" line sitting in the empty
  whitespace *below* the "story of each season" button, not on top of any of its text.
  Borderline and purely decorative (`pointer-events:none`, `aria-hidden` would be
  appropriate but its absence is a missed nicety, not a defect) — left alone as
  cosmetic, per the fix-only-what's-clearly-broken rule for this pass.

**Real (non-ellipsis) clipping: 0 across all 36 combinations.** The only clipped-flag
hits were `.lad-n` (manager name) with `text-overflow:ellipsis` — intentional
truncation for long names in the narrow mobile ladder column, exactly as designed.

---

## 390px sequence: reticle → breach → Redacted, commish, cossu, chaos

Screenshots saved to [audit-screenshots/390-eggs/](audit-screenshots/390-eggs/) (copied
out of the session scratchpad so the paths in this file stay valid). Result: **0
`pageerror` across the whole sequence.**

| step | file | result |
|---|---|---|
| initial load | [390-00-initial.png](audit-screenshots/390-eggs/390-00-initial.png) | clean |
| reticle tap 3/4/5 (escalating warnings) | [390-01-reticle-tap3.png](audit-screenshots/390-eggs/390-01-reticle-tap3.png), [-tap4](audit-screenshots/390-eggs/390-01-reticle-tap4.png), [-tap5](audit-screenshots/390-eggs/390-01-reticle-tap5.png) | warnings escalate correctly |
| tap 6 → breach + shot | [390-02-post-breach.png](audit-screenshots/390-eggs/390-02-post-breach.png) | `skin:"redact"`, `clearance:"1"` |
| Redacted theme, top | [390-03-redact-theme-top.png](audit-screenshots/390-eggs/390-03-redact-theme-top.png) | CLASSIFIED stamp crisp (this session's earlier fix holds on real phone rendering) |
| Redacted theme, scrolled | [390-04-redact-theme-scrolled.png](audit-screenshots/390-eggs/390-04-redact-theme-scrolled.png) | "CLEARANCE GRANTED" toast full-width, unbroken (earlier fix holds) |
| `commish` | [390-05-commish.png](audit-screenshots/390-eggs/390-05-commish.png) | Pharaoh renders full-bleed, no clipping |
| `cossu` | [390-06-cossu.png](audit-screenshots/390-eggs/390-06-cossu.png) | clean |
| `chaos` before/during/after | [390-07-chaos-before.png](audit-screenshots/390-eggs/390-07-chaos-before.png), [-during](audit-screenshots/390-eggs/390-08-chaos-during.png), [-after](audit-screenshots/390-eggs/390-09-chaos-after.png) | **1,183 numbers scrambled and restored exactly, 0 mismatches** |

Full JSON from that run:
```json
{"breachState":{"skin":"redact","clearance":"1","bodyClasses":""},
 "chaosCount":1183,"chaosAfterCount":1183,"chaosMismatches":[],"pageErrors":[]}
```

