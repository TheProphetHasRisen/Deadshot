# Deadshot Record Book — working rules

Read `HANDOFF.md` for full project context. These are the operational rules for
every session in this repo.

## Build

```bash
python3 export.py     # data.py + weekly*.py  → site_data.json
python3 mksite.py     # site_data.json        → index.html
```

Both, in that order, after any source change. `mksite.py` prints the byte count.

## Never edit `index.html` or `site_data.json`

They are build artifacts. Every change goes into `mksite.py` (the site) or
`data.py` / `weekly*.py` (the data), then you rebuild. Editing the artifacts
directly means your change is destroyed on the next build.

## Working inside `mksite.py`

`mksite.py` is ~250 KB / 3,550 lines — roughly 65k tokens. **Do not read it in
full.** It will consume most of the context window in a single call and you will
lose it to compaction before the task is done.

Instead:

- `grep -n` for the anchor you need, then read a narrow window around it
  (`sed -n 'START,ENDp'` or a `Read` with `offset`/`limit`).
- The file is four raw strings; the line numbers move as you edit, so re-grep
  rather than trusting a remembered offset:
  - `HEAD` (~line 4) — all CSS
  - `BODY` (~932) — markup, contains the `__DATA__` placeholder
  - `JS` (~1395) — all JavaScript
  - `SHELL_TOP` (~3536) — doctype and meta
- Prefer targeted `Edit` calls over rewriting regions.

If you patch with a Python script instead of `Edit`, **assert every anchor
matches exactly once before opening the file for write**, and `grep` afterwards
to confirm the change landed. A script that throws mid-way after making earlier
in-memory edits silently discards all of them. This has cost real work more than
once.

## Before introducing any new CSS class or `@keyframes` name

`grep` for it first. The stylesheet is one giant block shared by six themes, and
collisions are silent:

- a new `.brand` inherited the masthead's `.brand` and broke the layout
- a new `.totop.on` inherited the global `button.on` and inverted its colors
- `sweep` was defined twice as a keyframe and the wrong one won

Never hardcode a color. Use the CSS custom properties (`--brass`, `--surface`,
`--ink`, `--pos`, `--neg`, …) — all six themes have to survive every change.

## Verify before you report done

1. `python3 export.py && python3 mksite.py`
2. Extract the largest inline `<script>` from `index.html` and `node --check` it —
   a syntax error there blanks the entire page and nothing else will catch it.
3. `node test.js` (set `CHROMIUM_PATH` if Playwright can't find a browser).
   `net::ERR_TUNNEL_CONNECTION_FAILED` is expected sandbox noise, not a failure.
4. For anything visual, drive it in a headless browser and screenshot it. Check
   the change in more than one theme when it touches CSS.

Do not report a fix as working on the strength of the code reading correctly.

## Data changes

Run `python3 verify.py` after any data change. It automates the invariants below and
exits non-zero if any fail. `writer.py` runs it before writing and refuses to write
anything that does not pass, so a bad fetch is a no-op rather than a broken site.
Finished seasons are frozen: only the season named as live may be rewritten.

The invariants it enforces — they have caught real transcription errors:

- league-wide PF equals PA to the cent
- every team's W + L + T equals the season length
- total W equals total L
- the weekly game log reconciles against `STANDINGS`

### A rebuild that changes only pythW / luck / expOverAvg is expected

These three come from `pf**K/(pf**K+pa**K)` with `K = 2.37`. The fractional exponent
lands in the platform's libm `pow()`, so the last 1-2 bits vary between machines.
`index.html` and `site_data.json` are therefore **not** bit-reproducible across
machines, and a rebuild moving only those fields in the embedded JSON is not a
regression — do not "fix" it or treat it as a failed build.

It is not a Python version or CPU architecture difference; those were tested and
agree. Verify the claim structurally (parse and compare values) rather than by hash:
changed key order, thousands of differing values, or any non-float field moving means
something is actually wrong.

## Layout traps this codebase has actually hit

Grep before you add, and check the fix on a phone as well as a desktop.

- **`position:fixed` + `left:50%` with no width** shrink-to-fit caps at *half the
  viewport*. `.toast` was 195px on a 390px phone. Set `width:max-content` and a
  `max-width`.
- **`preserveAspectRatio="none"`** stretches text as well as shapes. The redacted
  dossier was scaled 7.2:1 on a phone. Bars survive it; type does not — keep text out
  of a non-uniformly scaled SVG, or make it real HTML.
- **`th,td{white-space:nowrap}` is global.** Long content pushes the right-hand column
  out of any `.scroll` card. Let a text column wrap instead of adding more scrolling.
- **A sticky element inside a horizontal scroller** needs its own opaque backdrop, and
  must be checked against whatever else is absolutely positioned there — the nav's
  `.navmark`, its scroll arrow and its fade gradient all wanted the same 46px.
- **`--nav-bg` and friends are translucent** (94-96%). Layering the token twice gets to
  ~99.6% without hardcoding a colour.
- **A long team name with no spaces cannot wrap.** Trade cards are titled
  "TeamA <-> TeamB" with a two-column body; a 40-character unbroken name pushed both out
  of the card on a phone. A plain `1fr` grid column will not shrink below its longest
  word — `minmax(0,1fr)` will. Fixed with that plus `overflow-wrap:anywhere` on
  `#trades .card-h h3` and `#trades .sub-h`. Names with quotes, ampersands, raw HTML,
  emoji and Arabic were all stress-tested: they render as text and nothing injects.
- **`data-m` is the manager-link attribute** and a global handler turns any click on one
  into `openMgr()`. Four Season Shape buttons already overload it as a metric key. Use a
  different attribute for new controls.

## Deploy

Use `./deploy.sh` (build + verify only) and `./deploy.sh --push` with
`DEADSHOT_REPO=TheProphetHasRisen/Deadshot` to ship. It verifies before it pushes and
commits `index.html` to `main` in one commit. Auth is `gh`, token in the macOS keyring —
**never ask for or accept a personal access token.** Confirm with the owner before every
push; Vercel deploys straight from it.

Manual drag-and-drop still works but Chrome renames to `index_NN.html`, which cost three
commits per deploy and a 404 once. If you do it by hand the filename must end up exactly
`index.html` and the old file is never deleted first.

## Who you are talking to

Brian owns this league and built this site with AI help. **He is not an engineer.**
Write every word to him on that basis.

### Reporting what you did

- Lead with **what changed and whether it worked**, in plain English.
- **No file paths, line numbers, or function names** unless he asks for them.
- **Never assume he knows a term.** Say "the thing that builds the page", not
  "the generator". Not "the DOM", "the build artifact", "the schema", "z-index".
  If a technical word is genuinely unavoidable, define it in the same breath.
- **Don't show commands** unless he is the one who has to run them.
- If something is broken, say so plainly and say **what it means for the site** —
  "the standings table is blank on phones" beats "the grid template is wrong".
- **Short.** No reasoning, no methodology, no play-by-play unless he asks. He does
  not need to see how the sausage was made to trust that it works.

### Decisions

**You make the technical calls. He does not want to be asked.** Which library,
which approach, how to structure something, what to name things, how to fix a bug —
pick the best option and say what you picked in one line. Asking him to choose
between technical options is offloading your job onto him.

Bring him a decision only when it is genuinely his:

- how the site should look or feel
- what to build next
- anything that costs money
- anything that cannot be undone

### When he has to do something himself

Walk him through it exactly, assuming he has never done it before. Every click,
every screen, what to type, and **what he should see when it worked**. Name the
application to open and quote the exact text to paste.

Not "authenticate with gh". Instead: open Terminal, paste this line, press Enter,
you'll see a screen asking X, choose Y, a browser tab opens, click Z, and when it
worked Terminal says "Logged in as ...".

## Tone

Direct and concise. Say plainly when something is broken, lost, or was your own
mistake. No flattery.
