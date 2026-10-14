/* Does "Ask the record book" still understand the questions people ask, and still give
 * the right number?
 *
 *     node test_ask.js
 *
 * Each case is a question as somebody would type it -- typos, slang and all -- and a check.
 * Wherever the answer is a number, the check works that number out again here, straight
 * from the league data, rather than trusting the reader's own arithmetic. A reader that
 * understands the question and then answers it wrongly is worse than one that says
 * "I don't know", so both halves are tested.
 *
 * Then the box itself is driven like a person would: "/" to open it, type, Enter to jump.
 * deploy.sh gates on this.
 */
const { chromium, webkit, devices } = require('playwright');
const path = require('path');
const FILE = 'file://' + path.join(__dirname, 'index.html');

/* [question, check(answer, truth) -> true or a string saying what was wrong] */
const CASES = [
  // ---- head to head
  ['Burke vs Kaiper', (o, T) => o.kind.startsWith('Head to head') && o.big === T.h2h('Brian Burke', 'Shane Kaiper', 'all') || `got ${o.kind} / ${o.big}, want ${T.h2h('Brian Burke', 'Shane Kaiper', 'all')}`],
  ['burke vs kaiper in the playoffs', (o, T) => /playoffs/.test(o.kind) && (o.big === T.h2h('Brian Burke', 'Shane Kaiper', 'po') || o.big === 'Never met') || `${o.kind} ${o.big}`],
  ['Alpert against Berger regular season', (o, T) => o.big === T.h2h('Wesley Alpert', 'Brian Berger', 'reg') || `${o.big} vs ${T.h2h('Wesley Alpert', 'Brian Berger', 'reg')}`],
  ['who owns kaiper', o => /owns Shane Kaiper/.test(o.title) || o.title],
  ['who does Alpert own', o => /Alpert|owns/.test(o.title + o.kind) || o.title],
  ['gearing alpert trades', (o, T) => o.kind === 'Trades' && o.big === T.tradesBetween('Nick Gearing', 'Wesley Alpert') || `${o.kind} ${o.big}`],
  ['Burke and Kaiper and Krueger', o => o.kind === 'Side by side' || o.kind],
  // ---- leader boards
  ['who has the most titles', (o, T) => o.kind === 'Career · Titles' && o.title.includes(T.most(m => m.titles)) || `${o.kind} ${o.title} want ${T.most(m => m.titles)}`],
  ["who's the goat", (o, T) => o.kind === 'Career · Titles' || o.kind],
  ['luckiest season ever', (o, T) => o.kind === 'Single season · Luck' && o.title === T.rowBest(r => r.luck, 1) || `${o.kind} ${o.title} want ${T.rowBest(r => r.luck, 1)}`],
  ['unluckiest manager', (o, T) => o.kind === 'Career · Luck' && o.title === T.least(m => m.luck) || `${o.title} want ${T.least(m => m.luck)}`],
  ['who got robbed the most', o => /Luck/.test(o.kind) || o.kind],
  ['best win percentage', (o, T) => o.title === T.most(m => m.winpct, m => m.seasons >= 2) || `${o.title} want ${T.most(m => m.winpct, m => m.seasons >= 2)}`],
  ['who sucks', (o, T) => o.title === T.least(m => m.winpct, m => m.seasons >= 2) || `${o.title} want ${T.least(m => m.winpct, m => m.seasons >= 2)}`],
  ['best average finish', (o, T) => o.title.includes(T.least(m => m.avgPlace, m => m.seasons >= 2)) || `${o.title} want ${T.least(m => m.avgPlace, m => m.seasons >= 2)}`],
  ['most trades', (o, T) => o.title === T.mostTrades() || `${o.title} want ${T.mostTrades()}`],
  ['most clutch', o => o.kind === 'Career · Titles above expectation' || o.kind],
  ['biggest choker', o => o.kind === 'Career · Titles above expectation' || o.kind],
  ['most last place finishes', o => o.kind === 'Career · Last-place finishes' || o.kind],
  ['best team ever', (o, T) => o.kind === 'Single season · Power index' && o.title === T.rowBest(r => r.pi, 1) || `${o.kind} ${o.title}`],
  ['worst season ever', (o, T) => o.title === T.rowBest(r => r.pi, 0) || `${o.title} want ${T.rowBest(r => r.pi, 0)}`],
  ['most points in a season', (o, T) => o.kind === 'Single season · Points for' && o.title === T.rowBest(r => r.pf, 1) || `${o.kind} ${o.title}`],
  ['highest power index in 2023', (o, T) => o.title === T.rowBest(r => r.pi, 1, 2023) || `${o.title} want ${T.rowBest(r => r.pi, 1, 2023)}`],
  // ---- one game
  ['highest scoring week', (o, T) => /Highest score/.test(o.kind) && o.big === T.topScore().toFixed(2) || `${o.kind} ${o.big} want ${T.topScore().toFixed(2)}`],
  ['most points in a week', o => /Highest score/.test(o.kind) || o.kind],
  ['biggest blowout', (o, T) => /margin/i.test(o.kind) && o.big === T.bigMargin().toFixed(2) + ' points' || `${o.kind} ${o.big} want ${T.bigMargin().toFixed(2)}`],
  ['closest game ever', (o, T) => /Closest/.test(o.kind) && o.big === T.smallMargin().toFixed(2) + ' points' || `${o.kind} ${o.big}`],
  ['who got destroyed', o => /margin/i.test(o.kind) || o.kind],
  ['burke highest score', o => /^Brian Burke/.test(o.kind) && /Highest score/.test(o.kind) || o.kind],
  // ---- one manager
  ['Krueger', (o, T) => o.title === 'Kevin Krueger' && o.kind === 'Career' || `${o.kind} ${o.title}`],
  ['burke titles', (o, T) => o.big === String(T.mgr('Brian Burke').titles) || `${o.big} want ${T.mgr('Brian Burke').titles}`],
  ["Niko's playoff record", (o, T) => o.big === T.mgr('Niko Contreras').poW + '–' + T.mgr('Niko Contreras').poL || `${o.big}`],
  ['niko in the playoffs', (o, T) => o.title === 'Niko Contreras in the playoffs' && o.big === T.mgr('Niko Contreras').poW + '–' + T.mgr('Niko Contreras').poL || `${o.title} ${o.big}`],
  ['Burke luck 2022', o => o.title === 'Brian Burke in 2022' || o.title],
  ['kaiper 2015', o => o.title === 'Shane Kaiper in 2015' || o.title],
  ['Burke since 2021', o => o.kind.startsWith('2021') && o.title === 'Brian Burke' || `${o.kind} ${o.title}`],
  ['how lucky is wu', (o, T) => o.title === 'Nathan Wu' && o.big.replace(/<[^>]+>/g, '').startsWith(T.signed(T.mgr('Nathan Wu').luck)) || `${o.title} ${o.big}`],
  ['Dylan 2019', o => (o.missing || []).some(m => /2019/.test(m)) || JSON.stringify(o.missing)],
  // ---- typos
  ['krugr', o => o.title === 'Kevin Krueger' && o.readAs.some(r => r[0] === 'krugr') || `${o.title} ${JSON.stringify(o.readAs)}`],
  ['kaipr vs burk', o => o.title === 'Shane Kaiper vs Brian Burke' || o.title],
  ['who has the most championshps', o => o.kind === 'Career · Titles' || o.kind],
  ['luckyest seasn', o => o.kind === 'Single season · Luck' || o.kind],
  ['playofs record for niko', o => /playoffs/i.test(o.title) || o.title],
  ['contrears', o => o.title === 'Niko Contreras' || o.title],
  ['most tradez', o => /Trades/.test(o.kind) || o.kind],
  // ---- seasons, weeks, teams, players
  ['who won 2023', (o, T) => o.kind === '2023 season' && o.title === T.champ(2023) || `${o.kind} ${o.title} want ${T.champ(2023)}`],
  ['2024 champ', (o, T) => o.kind === '2024 season' || o.kind],
  ['2021-2023', o => o.kind === 'Champions' || o.kind],
  ['week 1 2025', o => o.kind === 'Week 1, 2025' || o.kind],
  ['week 3', o => /^Week 3, /.test(o.kind) || o.kind],
  ['week 4 2017', o => /No week-by-week log/.test(o.title) || o.title],
  ['Hench', o => o.title === 'Hench' || o.title],
  ["poe's palace 2023", o => o.title === "Poe's Palace" && /2023/.test(o.kind) || `${o.title} ${o.kind}`],
  ['Iridocyclitis', o => o.title === 'Iridocyclitis' || o.title],
  ["kevin's superb optimal team", o => o.kind.startsWith('Team') || o.kind],
  ['Stefon Diggs', o => o.kind === 'Player' && o.title === 'Stefon Diggs' || `${o.kind} ${o.title}`],
  ['diggs trade', o => o.title === 'Stefon Diggs' || o.title],
  // ---- slices of games: weeks, situations, opponents, projections (the onion layers)
  ['Wu record in weeks 1-4 of regular season', (o, T) => o.title === 'Nathan Wu' && o.big.startsWith(T.sl('Nathan Wu', r => r.wk <= 4, 'reg')) || `${o.title} ${o.big} want ${T.sl('Nathan Wu', r => r.wk <= 4, 'reg')}`],
  ['wu record first 4 weeks', (o, T) => o.big.startsWith(T.sl('Nathan Wu', r => r.wk <= 4, 'reg')) || o.big],
  ['Kaiper record after a loss', (o, T) => o.big.startsWith(T.sl('Shane Kaiper', r => r.prev === 'L', 'reg')) || `${o.big} want ${T.sl('Shane Kaiper', r => r.prev === 'L', 'reg')}`],
  ['Burke record in close games', (o, T) => o.big.startsWith(T.sl('Brian Burke', r => Math.abs(r.pts - r.opts) < 10, 'all')) || `${o.big} want ${T.sl('Brian Burke', r => Math.abs(r.pts - r.opts) < 10, 'all')}`],
  ['Alpert record against winning teams', (o, T) => o.big.startsWith(T.sl('Wesley Alpert', r => r.oppPct > .5, 'all')) || `${o.big} want ${T.sl('Wesley Alpert', r => r.oppPct > .5, 'all')}`],
  ['Krueger record as an underdog', (o, T) => o.big.startsWith(T.sl('Kevin Krueger', r => r.proj < r.oproj, 'reg')) || `${o.big} want ${T.sl('Kevin Krueger', r => r.proj < r.oproj, 'reg')}`],
  ['berger record in the second half of the season', (o, T) => o.big.startsWith(T.sl('Brian Berger', r => r.wk > Math.ceil(r.last / 2), 'reg')) || o.big],
  ['Cossu record last 3 weeks of the regular season', (o, T) => o.big.startsWith(T.sl('Chris Cossu', r => r.wk > r.last - 3, 'reg')) || o.big],
  ['how often does Wu score 150+', (o, T) => o.big.startsWith(T.count('Nathan Wu', r => r.pts >= 150, 'all') + ' of ') || `${o.big} want ${T.count('Nathan Wu', r => r.pts >= 150, 'all')}`],
  ['wu record when scoring under 110', (o, T) => o.big.startsWith(T.sl('Nathan Wu', r => r.pts < 110, 'all')) || o.big],
  ['best start', (o, T) => /Weeks 1–4/.test(o.kind) && o.title === T.bestSl(r => r.wk <= 4, 'reg') || `${o.kind} ${o.title} want ${T.bestSl(r => r.wk <= 4, 'reg')}`],
  ['who fades', (o, T) => /Last 4 weeks/.test(o.kind) && o.title === T.bestSl(r => r.wk > r.last - 4, 'reg', true) || `${o.title} want ${T.bestSl(r => r.wk > r.last - 4, 'reg', true)}`],
  ['most 150 point games', (o, T) => o.title === T.mostCount(r => r.pts >= 150, 'all') || `${o.title} want ${T.mostCount(r => r.pts >= 150, 'all')}`],
  ['most upsets', o => /Projected to lose/.test(o.kind) && /win/.test(o.big) || o.kind],
  ['biggest upset', o => /Biggest upset/.test(o.kind) || o.kind],
  ['highest score in weeks 1-4', (o, T) => o.big === T.topSl(r => r.wk <= 4, 'reg').toFixed(2) || `${o.big} want ${T.topSl(r => r.wk <= 4, 'reg')}`],
  ['who owns Burke in close games', o => /owns Brian Burke/.test(o.title) || o.title],
  ['Berger vs Burke in close games', o => o.title === 'Brian Berger vs Brian Burke' || o.title],
  ['who beats their projection the most', o => /Beat the projection most often/.test(o.sub) || o.sub],
  ['Wu by week', o => o.title === 'Nathan Wu' && /Week 1/.test(o.body) || o.title],
  ['Burke by season', o => o.kind === 'Season by season' || o.kind],
  // ---- things it must not pretend to know
  ['who drafted Justin Jefferson', o => (o.soon || []).some(s => /Draft/.test(s)) || JSON.stringify(o.soon)],
  ['worst injury luck', o => (o.soon || []).some(s => /Injury/.test(s)) || JSON.stringify(o.soon)],
  ['2026', o => (o.missing || []).some(s => /not in the book yet/.test(s)) || JSON.stringify(o.missing)],
  ['2019', o => (o.missing || []).some(s => /2019/.test(s)) || JSON.stringify(o.missing)],
  ['brian', o => o.kind === 'Which one?' && o.choose && o.choose.options.length === 2 || o.kind],
  ['watson', o => o.kind === 'Which one?' || o.kind],
  ['xyzzy plugh', o => o.empty === true || o.kind],
  ['', o => o.empty === true || o.kind],
];

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.goto(FILE); await p.waitForTimeout(1300);
  /* the truth, worked out from DATA in the page, independently of ask.js */
  const results = await p.evaluate(cases => {
    const D = DATA, Mg = D.mgrs, R = D.rows;
    const reg = []; (D.wkYears || []).forEach(y => { const K = D.wk[y]; K.games.filter(g => g.br === '').forEach(g => reg.push({ ma: K.mgr[g.ta], mb: K.mgr[g.tb], pa: g.aa, pb: g.ab })); });
    const po = D.games.filter(g => !g.void).map(g => ({ ma: g.ma, mb: g.mb, pa: g.pa, pb: g.pb }));
    const GL = []; const rowOf = {}; R.forEach(r => { rowOf[r.y + '|' + r.mgr] = r; });
    (D.wkYears || []).forEach(y => { const K = D.wk[y]; const reg = K.games.filter(g => g.br === ''); const last = Math.max(...reg.map(g => g.wk));
      reg.forEach(g => { GL.push({ y, wk: g.wk, last, mgr: K.mgr[g.ta], opp: K.mgr[g.tb], pts: g.aa, opts: g.ab, proj: g.pa, oproj: g.pb, po: false });
        GL.push({ y, wk: g.wk, last, mgr: K.mgr[g.tb], opp: K.mgr[g.ta], pts: g.ab, opts: g.aa, proj: g.pb, oproj: g.pa, po: false }); }); });
    D.games.filter(g => !g.void).forEach(g => { GL.push({ y: g.y, wk: g.wk, mgr: g.ma, opp: g.mb, pts: g.pa, opts: g.pb, po: true }); GL.push({ y: g.y, wk: g.wk, mgr: g.mb, opp: g.ma, pts: g.pb, opts: g.pa, po: true }); });
    const seqs = {}; GL.filter(r => !r.po).forEach(r => (seqs[r.y + '|' + r.mgr] = seqs[r.y + '|' + r.mgr] || []).push(r));
    Object.values(seqs).forEach(a => { a.sort((x, z) => x.wk - z.wk); a.forEach((r, i) => { r.prev = i ? (a[i - 1].pts > a[i - 1].opts ? 'W' : 'L') : null; }); });
    GL.forEach(r => { const o = rowOf[r.y + '|' + r.opp]; r.oppPct = o ? (o.w + o.t / 2) / o.g : null; });
    const T = {
      mgr: n => Mg.find(m => m.name === n),
      h2h: (a, b2, k) => { const gs = (k === 'po' ? po : k === 'reg' ? reg : reg.concat(po)).filter(g => (g.ma === a && g.mb === b2) || (g.ma === b2 && g.mb === a));
        let w = 0, l = 0; gs.forEach(g => ((g.pa > g.pb ? g.ma : g.mb) === a ? w++ : l++)); return gs.length ? w + '–' + l : 'Never met'; },
      most: (f, ok = () => true) => Mg.filter(ok).slice().sort((a, b2) => f(b2) - f(a))[0].name,
      least: (f, ok = () => true) => Mg.filter(ok).slice().sort((a, b2) => f(a) - f(b2))[0].name,
      rowBest: (f, hi, y) => { const r = R.filter(x => !y || x.y === y).slice().sort((a, b2) => hi ? f(b2) - f(a) : f(a) - f(b2))[0]; return r.mgr + ', ' + r.y; },
      mostTrades: () => D.trade.mgr.slice().sort((a, b2) => b2.trades - a.trades)[0].name,
      tradesBetween: (a, b2) => { const n = D.trade.log.filter(x => (x.ma === a && x.mb === b2) || (x.ma === b2 && x.mb === a)).length; return n + ' trade' + (n === 1 ? '' : 's'); },
      topScore: () => Math.max(...reg.concat(po).flatMap(g => [g.pa, g.pb])),
      bigMargin: () => Math.max(...reg.concat(po).map(g => Math.abs(g.pa - g.pb))),
      smallMargin: () => Math.min(...reg.concat(po).map(g => Math.abs(g.pa - g.pb))),
      champ: y => D.champs.find(c => c.y === y).mgrs.join(' & '),
      sl: (n, f, set) => { const rs = GL.filter(r => r.mgr === n && (set === 'all' || (set === 'po') === r.po) && f(r)); const w = rs.filter(r => r.pts > r.opts).length, t = rs.filter(r => r.pts === r.opts).length; return w + '–' + (rs.length - w - t) + (t ? '–' + t : ''); },
      count: (n, f, set) => GL.filter(r => r.mgr === n && (set === 'all' || (set === 'po') === r.po) && f(r)).length,
      bestSl: (f, set, worst) => { const by = {}; GL.filter(r => (set === 'all' || (set === 'po') === r.po) && f(r)).forEach(r => (by[r.mgr] = by[r.mgr] || []).push(r));
        const l = Object.entries(by).filter(([, rs]) => rs.length >= 4).map(([n, rs]) => ({ n, p: rs.filter(r => r.pts > r.opts).length / rs.length, w: rs.filter(r => r.pts > r.opts).length, l: rs.filter(r => r.pts < r.opts).length }));
        l.sort((a, b) => worst ? a.p - b.p || b.l - a.l : b.p - a.p || b.w - a.w); return l[0].n; },
      mostCount: (f, set) => { const by = {}; GL.filter(r => (set === 'all' || (set === 'po') === r.po) && f(r)).forEach(r => { by[r.mgr] = (by[r.mgr] || 0) + 1; }); return Object.entries(by).sort((a, b) => b[1] - a[1])[0][0]; },
      topSl: (f, set) => Math.max(...GL.filter(r => (set === 'all' || (set === 'po') === r.po) && f(r)).map(r => r.pts)),
      signed: v => (Math.abs(v).toFixed(2) === '0.00' ? '' : v > 0 ? '+' : '−') + Math.abs(v).toFixed(2),
    };
    return cases.map(([q, src]) => {
      let o, err = null;
      try { o = Ask.answer(Ask.parse(q)); } catch (e) { err = e.message; }
      if (err) return { q, ok: false, why: 'threw: ' + err };
      const plain = JSON.parse(JSON.stringify({ ...o, acts: (o.acts || []).map(a => a.label) }));
      plain.big = String(plain.big || '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
      let ok;
      try { ok = (0, eval)('(' + src + ')')(plain, T); } catch (e) { ok = 'check threw: ' + e.message; }
      return { q, ok: ok === true, why: ok === true ? '' : String(ok), kind: plain.kind, title: plain.title, big: plain.big };
    });
  }, CASES.map(([q, f]) => [q, f.toString()]));

  let fail = 0;
  for (const r of results) if (!r.ok) { fail++; console.log(`  FAIL  "${r.q}"  ${r.why}`); }
  console.log(`questions: ${results.length - fail} of ${results.length} answered correctly`);

  /* the box itself, driven like a person would */
  const ui = [];
  await p.keyboard.press('/'); await p.waitForTimeout(200);
  if (!(await p.evaluate(() => document.activeElement && document.activeElement.id === 'askIn'))) ui.push('"/" did not open the box with the cursor in it');
  await p.keyboard.type('burke vs kaiper'); await p.waitForTimeout(350);
  if (!(await p.evaluate(() => /Head to head/i.test(document.getElementById('askOut').innerText)))) ui.push('typing did not show an answer');
  await p.keyboard.press('Enter'); await p.waitForTimeout(900);
  const after = await p.evaluate(() => ({ open: document.getElementById('ov').classList.contains('on'), a: document.getElementById('cmpA').value, b: document.getElementById('cmpB').value, title: document.title }));
  if (after.open || after.a !== 'Brian Burke' || after.b !== 'Shane Kaiper') ui.push('Enter did not take you to Head to Head with both managers picked: ' + JSON.stringify(after));
  await p.keyboard.press(process.platform === 'darwin' ? 'Meta+k' : 'Control+k'); await p.waitForTimeout(200);
  await p.keyboard.type('krugr'); await p.waitForTimeout(350);
  if (!(await p.evaluate(() => /Read/.test(document.getElementById('askOut').innerText) && /Kevin Krueger/.test(document.getElementById('askOut').innerText)))) ui.push('Cmd/Ctrl+K or the typo note did not work');
  await p.keyboard.press('Enter'); await p.waitForTimeout(500);
  if (!(await p.evaluate(() => /Kevin Krueger/.test(document.getElementById('mTitle').textContent)))) ui.push('Enter on a manager did not open their page');
  await p.keyboard.press('Escape');
  await b.close();

  /* and on a small iPhone, in Safari's engine */
  const w = await webkit.launch();
  const ctx = await w.newContext({ ...devices['iPhone SE'] });
  const q = await ctx.newPage();
  q.on('pageerror', e => errs.push('webkit: ' + e.message));
  await q.goto(FILE); await q.waitForTimeout(1300);
  const btn = await q.evaluate(() => { const b2 = document.getElementById('askBtn'); const r = b2.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
  if (!btn) ui.push('the Ask button is not visible on an iPhone SE');
  await q.tap('#askBtn'); await q.waitForTimeout(300);
  const fs = await q.evaluate(() => parseFloat(getComputedStyle(document.getElementById('askIn')).fontSize));
  if (fs < 16) ui.push('the box text is ' + fs + 'px; under 16px makes iOS zoom the page');
  await q.fill('#askIn', 'who has the most titles'); await q.waitForTimeout(350);
  const wide = await q.evaluate(() => ({ doc: document.documentElement.scrollWidth, vw: innerWidth, card: !!document.querySelector('#askOut .ask-card') }));
  if (!wide.card) ui.push('no answer card on the phone');
  if (wide.doc > wide.vw) ui.push('the page scrolls sideways with the answer open on a phone');
  await w.close();

  ui.forEach(x => console.log('  FAIL  ' + x));
  if (errs.length) console.log('  page errors: ' + errs.join(' | '));
  console.log(ui.length ? `${ui.length} problem(s) driving the box` : 'the box opens, answers, jumps and works on an iPhone SE');
  process.exit(fail || ui.length || errs.length ? 1 : 0);
})();
