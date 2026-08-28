# Pulling league data from Yahoo automatically — the plan

**Where things stand:** the access application was submitted on 28 Aug 2026. Yahoo
has to approve it before anything else can happen. They publish no timetable.

The goal is to stop transcribing seasons by hand. Nothing about how the site looks
or works changes — only where the numbers come from.

---

## The short version

1. **You applied.** Done.
2. **Yahoo approves** (or doesn't). Out of our hands. This is the only real blocker.
3. **You do a one-time sign-in** — about two minutes, walked through step by step.
4. **I build the fetcher**, roughly half of which I can build before approval.
5. **It runs itself weekly** during the season and updates the site.

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

Yahoo issues a key tied to your account. You approve it in your browser, once. I
never see your password, and the key goes straight into GitHub's secret storage
where it stays.

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

## Open questions I can't answer yet

- How long Yahoo takes to approve, or whether they will.
- How far back their data actually goes for this league.
- Whether the earliest seasons include weekly detail or only totals.

All three resolve within a day of access being granted.
