# Pulling league data from Yahoo automatically — the plan

**Where things stand:** applied 28 Aug 2026. **Approved 10 Sep 2026** — the agreement is
signed. Remaining: register the app to mint the key, send Yahoo the Client ID, wait for
them to switch Fantasy Sports access on.

Two goals, not one:

1. Stop transcribing our own league by hand. Nothing about how the site looks or works
   changes — only where the numbers come from.
2. Pull **season-level fantasy football data for each year** as well — player fantasy
   stats, average draft position, ownership — not just this league. That is what feeds
   the draft board in `draft/`, which currently leans on scraped ESPN and FantasyPros
   files. Same key, same API, different endpoints.

---

## The short version

1. **You applied.** Done.
2. **Yahoo approved.** Done.
3. **You register the app and mint the key.** ~60 seconds on developer.yahoo.com/apps.
   This was missing from an earlier version of this document, which wrongly said the key
   arrives when Yahoo approves you. It does not — approval only unlocks your ability to
   create one, and Yahoo then wants the Client ID back via their confirmation form.
4. **Yahoo attaches Fantasy Sports permissions.** Out of our hands, and the last blocker.
5. **You do a one-time sign-in** — about two minutes, walked through step by step.
6. **I build the fetcher**, roughly half of which I can build before access lands.
7. **It runs itself weekly** during the season and updates the site.

---

## What I can build now, before approval

About half the work doesn't touch Yahoo at all, and it's the half that protects
the site from bad data.

### Already done — the safety net

`verify.py` checks the whole dataset for errors and refuses to pass if it finds
any. It runs today:

- league-wide points for must equal points against, to the cent
- every team's wins + losses + ties must equal the season length
- total wins must equal total losses
- **the week-by-week log must reproduce the season standings exactly** — the
  strongest check, it rebuilds every record and points total from individual games
- team counts, duplicate names, managers matching teams, final placings matching
  the field, playoff games referencing real teams

517 checks against the current 10 seasons. All pass.

Proven to actually catch things: changing one score by 100 points was caught twice
over and named the exact team; changing one team's record from 5-9 to 6-8 was
caught twice over. It exits with a failure code, so it can block a bad build
without anyone watching.

### Still to build before approval

- **The writer** — turns fetched data into exactly the file format the site already
  reads, so nothing downstream changes. Testable without Yahoo by round-tripping
  the existing seasons and checking the files come back identical.
- **The guard rails** — a finished season can never be overwritten; a failed fetch
  writes nothing and leaves the last good site up.

### What genuinely has to wait

The part that reads Yahoo's replies. I don't know the exact shape of their data for
this league, and guessing it would mean rewriting it later. That's the piece that
starts the day access is granted.

---

## What happens after Yahoo approves

### Step 1 — you sign in once (about two minutes)

Yahoo does **not** hand over a key on approval. Brian registers an "app" on
developer.yahoo.com/apps — a short form, no software involved — and that mints the
Client ID and Client Secret. The Client ID goes back to Yahoo on their confirmation
form; the Secret never leaves that page until it goes into secret storage.

Then he approves access in his browser, once. I never see his password, and neither
key ever appears in this project. `.gitignore` blocks `.env`, `*_secret*` and
`*refresh_token*` so one cannot be committed by accident.

You'll get exact instructions when we get there: what to open, what to paste, what
appears on screen, and what it looks like when it worked.

### Step 2 — I build and test the fetcher

Run by hand at first, against seasons we already have transcribed. That's the real
test: **if the fetched 2025 season doesn't match your hand-typed 2025 season, the
fetcher is wrong.** We already have five seasons of known-good weekly data to check
against, which is a luxury.

### Step 3 — backfill whatever Yahoo still has

We have season totals back to 2015 but week-by-week detail only from 2021. If
Yahoo still holds the earlier seasons, several features currently dark for
2015–2020 light up. If it doesn't, nothing is lost — we keep what we have.

**Unknown until we have access.** Yahoo keeps league history going back many years,
but whether every detail survives for a 2015 league is not something I can confirm
from outside.

### Step 4 — it runs itself

A scheduled job once a week during the season. It fetches, checks itself against
every rule above, and only then updates the site.

---

## The rules it will follow

These are hard requirements, not preferences.

1. **Your key is never visible.** It lives in GitHub's secret storage. It never
   appears in this project, in any file, or in anything I can read.
2. **The site's data files stay the source of truth.** The fetcher writes them in
   the exact existing format. The parts that build the page never change.
3. **Every fetch is checked before it counts.** A fetch that fails any check writes
   nothing and reports loudly.
4. **Finished seasons are frozen.** Live 2026 data can never overwrite a completed
   historical season.
5. **If Yahoo is down or the key stops working, the last good site stays up.** A
   failure is always a no-op, never a broken page.

---

## What could go wrong

| Risk | What it means | What we do |
|---|---|---|
| **Yahoo denies access** | The whole automatic route is closed | You keep transcribing; the site is unaffected. Nothing built so far is wasted — the safety net works regardless of where data comes from |
| **They never reply** | Same as denial, but with no answer | Reapply once with more detail. No other lever exists |
| **Yahoo's data disagrees with yours** | Their record of an old season differs from your transcription | Your transcription wins unless Yahoo is clearly right. This is a decision for you, not me |
| **2015–2020 detail is gone** | Those seasons stay as totals only | Accept it. Nothing currently working breaks |
| **Too many requests too fast** | Yahoo cuts us off, as it did before at about 120 | Deliberate pacing and stopping when told to. Very low volume anyway |
| **The key stops working** | Fetches start failing | Site keeps serving the last good version; you re-approve once |

---

## Roughly who does what

| | You | Me |
|---|---|---|
| Applying to Yahoo | done | — |
| Waiting | — | — |
| Signing in once | ~2 min | walkthrough |
| Building and testing | — | most of the work |
| Checking a season looks right | ~10 min | — |
| Running it every week | nothing | automatic |

Your total involvement after approval is roughly fifteen minutes.

---

## Historical IR placement — checked 12 Sep 2026, and it survives

The feature Brian wants most (injury luck; who won a trade) rests on whether Yahoo
returns a team's roster *as it stood in a given week*, IR slot included, for a season
that has already finished. Checked directly against the archived 2025 league on the
website, week 5:

```
QB    | Jake Browning
...
IR    | Joe Burrow
IR    | Joe Mixon
```

That is week-5 truth, not end-of-season state: Browning is only in the QB slot because
Burrow was hurt at the time. Yahoo therefore stores and serves per-week roster
composition, IR included, for completed seasons.

**Caveat:** this was verified on the *website*, not the API, because the API was still
403 at the time. Both read the same roster records and the API's roster resource takes
a `;week=` parameter, so this is strong evidence rather than proof. Re-confirm against
`team/{team_key}/roster;week=N` on day one.

Also confirmed while looking: the signed-in Yahoo account is the one in DEADSHØT
(league 526001 for 2026, 214163 for 2025), and the league's own season list runs
2013 → 2026, so the history exists at least that far back.

## Open questions I can't answer yet

- How long Yahoo takes to provision, now that the Client ID is submitted.
- Whether the 2015–2020 seasons return per-week rosters the way 2025 does. Could not
  test: Yahoo's year picker no longer resolves old league ids, and the archived pages
  blocked the script that would have read them.
- Whether player *status* strings (Questionable, Out, the injury note) are historical
  or only ever current. The IR slot is the reliable signal either way.

All of these resolve within a day of access being granted.
