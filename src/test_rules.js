/* Does the League rules card actually match Yahoo?
 *
 *     node test_rules.js
 *
 * TRUTH below is every scoring category on Yahoo's settings page for league 526001,
 * read structurally off the page's own table on 14 Sep 2026 -- 12 offense, 6 kicker,
 * 17 defense, 35 in total. Yahoo shows only the categories the league actually scores,
 * so anything absent there is absent on purpose.
 *
 * This exists because I checked the scoring by reading it and saying "looks right",
 * and that same habit is what put the wrong waiver time on the live site. A category
 * that quietly goes missing from the card is invisible otherwise: the card still looks
 * complete, it just stops mentioning, say, offensive fumble return touchdowns.
 *
 * If Yahoo's settings ever change, re-read that table and update TRUTH in the same
 * commit as the card. Failing here means the two have drifted -- fix the card, or
 * update TRUTH if the league genuinely changed the rule.
 */
const { chromium } = require('playwright');
const path = require('path');

// [category, the value the league scores, section]
const TRUTH = [
  ['Passing yards', '25', 'offense'],
  ['Passing touchdowns', '4', 'offense'],
  ['Interceptions thrown', '-1', 'offense'],
  ['Rushing yards', '10', 'offense'],
  ['Rushing touchdowns', '6', 'offense'],
  ['Receptions', '1', 'offense'],
  ['Receiving yards', '10', 'offense'],
  ['Receiving touchdowns', '6', 'offense'],
  ['Return touchdowns', '6', 'offense'],
  ['2-point conversions', '2', 'offense'],
  ['Fumbles lost', '-2', 'offense'],
  ['Offensive fumble return TD', '6', 'offense'],

  ['Field goals 0-19', '3', 'kicker'],
  ['Field goals 20-29', '3', 'kicker'],
  ['Field goals 30-39', '3', 'kicker'],
  ['Field goals 40-49', '4', 'kicker'],
  ['Field goals 50+', '5', 'kicker'],
  ['Point after attempt', '1', 'kicker'],

  ['Sack', '1', 'defense'],
  ['Interception', '2', 'defense'],
  ['Fumble recovery', '2', 'defense'],
  ['Touchdown', '6', 'defense'],
  ['Safety', '3', 'defense'],
  ['Block kick', '2.5', 'defense'],
  ['Kickoff and punt return TDs', '6', 'defense'],
  ['Points allowed 0', '10', 'defense'],
  ['Points allowed 1-6', '7', 'defense'],
  ['Points allowed 7-13', '4', 'defense'],
  ['Points allowed 14-20', '2', 'defense'],
  ['Points allowed 21-27', '0', 'defense'],
  ['Points allowed 28-34', '-1', 'defense'],
  ['Points allowed 35+', '-4', 'defense'],
  ['4th down stops', '1', 'defense'],
  ['Three and outs forced', '0.5', 'defense'],
  ['Extra point returned', '2', 'defense'],
];

/* What the card has to contain for each category to count as present. Two regexes:
   one that finds the category, one that finds its value near it. Kept explicit rather
   than clever, because a loose match here would pass on a card that says nothing. */
const NEEDS = {
  'Passing yards': /passing\s*25\s*yds\/pt/i,
  'Passing touchdowns': /pass TD 4/i,
  'Interceptions thrown': /INT\s*[-−–]1/i,
  'Rushing yards': /rushing\s*10\s*yds\/pt/i,
  'Rushing touchdowns': /rush TD 6/i,
  'Receptions': /reception\s*1\.0/i,
  'Receiving yards': /receiving\s*10\s*yds\/pt/i,
  'Receiving touchdowns': /rec TD 6/i,
  'Return touchdowns': /return TD 6/i,
  '2-point conversions': /2-point conversion 2/i,
  'Fumbles lost': /fumble lost\s*[-−–]2/i,
  'Offensive fumble return TD': /offensive fumble return TD 6/i,
  'Field goals 0-19': /0[-–]19:\s*3/i,
  'Field goals 20-29': /20[-–]29:\s*3/i,
  'Field goals 30-39': /30[-–]39:\s*3/i,
  'Field goals 40-49': /40[-–]49:\s*4/i,
  'Field goals 50+': /50\+:\s*5/i,
  'Point after attempt': /extra point 1/i,
  'Sack': /sack 1/i,
  'Interception': /INT 2/i,
  'Fumble recovery': /fumble recovery 2/i,
  'Touchdown': /\bTD 6\b/i,
  'Safety': /safety 3/i,
  'Block kick': /block kick 2\.5/i,
  'Kickoff and punt return TDs': /kick\/punt return TD 6/i,
  'Points allowed 0': /0\s*[→>]\s*10/i,
  'Points allowed 1-6': /1[-–]6\s*[→>]\s*7/i,
  'Points allowed 7-13': /7[-–]13\s*[→>]\s*4/i,
  'Points allowed 14-20': /14[-–]20\s*[→>]\s*2/i,
  'Points allowed 21-27': /21[-–]27\s*[→>]\s*0/i,
  'Points allowed 28-34': /28[-–]34\s*[→>]\s*[-−–]1/i,
  'Points allowed 35+': /35\+\s*[→>]\s*[-−–]4/i,
  '4th down stops': /4th[- ]down stop 1/i,
  'Three and outs forced': /three[- ]and[- ]out forced 0\.5/i,
  'Extra point returned': /extra point returned 2/i,
};

/* The league changed these away from Yahoo's default, and the card says so. Losing the
   "(default N)" note is how a reader stops realising Deadshot is not a standard league. */
const FLAGGED_AS_CHANGED = {
  'Receptions': /reception 1\.0[^)]*\(default 0\.5\)/i,
  'Safety': /safety 3\s*\(default 2\)/i,
  'Block kick': /block kick 2\.5\s*\(default 2\)/i,
  '4th down stops': /4th[- ]down stop 1\s*\(default 0\)/i,
  'Three and outs forced': /three[- ]and[- ]out forced 0\.5\s*\(default 0\)/i,
  'Points allowed 14-20': /\(default 14[-–]20 is 1\)/i,
};

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.join(__dirname, 'index.html'));
  await p.waitForTimeout(1300);

  // both places the rules are drawn: the section at the bottom, and the dialog
  const texts = await p.evaluate(() => {
    const section = document.getElementById('rulesBody').innerText;
    document.getElementById('rulesBtn').click();
    const dialog = document.querySelector('#mBody .rules').innerText;
    return { section, dialog };
  });

  let fail = 0;
  for (const where of ['section', 'dialog']) {
    const t = texts[where].replace(/\s+/g, ' ');
    for (const [name, , section] of TRUTH) {
      if (!NEEDS[name].test(t)) {
        console.log(`  MISSING  [${where}/${section}] ${name}`);
        fail++;
      }
    }
    for (const [name, re] of Object.entries(FLAGGED_AS_CHANGED)) {
      if (!re.test(t)) {
        console.log(`  NOT FLAGGED AS NON-DEFAULT  [${where}] ${name}`);
        fail++;
      }
    }
  }
  if (texts.section !== texts.dialog) {
    console.log('  The bottom section and the dialog do not match.');
    fail++;
  }
  if (errs.length) { console.log('  page errors: ' + errs.join(' | ')); fail++; }

  const n = TRUTH.length;
  console.log(fail
    ? `\n${fail} problem(s). ${n} categories checked in each of 2 places.`
    : `\nall ${n} Yahoo scoring categories present in both the section and the dialog, `
      + `${Object.keys(FLAGGED_AS_CHANGED).length} non-default values flagged`);
  await b.close();
  process.exit(fail ? 1 : 0);
})();
