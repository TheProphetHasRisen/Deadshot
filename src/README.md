# Deadshot Record Book — source

Everything that builds `index.html` at the root of this repo. The published site is
that single self-contained file; this folder is what generates it.

Build (from inside this folder):

    python3 export.py     # league data  -> site_data.json
    python3 mksite.py     # site_data.json -> index.html

Check the data first — it exits non-zero if anything is wrong:

    python3 verify.py

`HANDOFF.md` is the full project brief. `CLAUDE.md` carries the standing working
rules. `YAHOO_PLAN.md` covers replacing hand transcription with the Yahoo API.

Not included here: the original `Deadshot History.xlsx` working spreadsheet, which
stays local.
