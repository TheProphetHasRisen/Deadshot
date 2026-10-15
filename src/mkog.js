/* Link-preview cards, one per theme.
   ----------------------------------------------------------------------------
   Discord, iMessage and the rest fetch og:image server-side from the URL alone.
   They never see the reader's theme, so a single og.png could only ever show one
   of the six. The fix is one image per theme plus a tiny shim page per theme that
   carries the matching og tags (see the t/ files, written by this script too);
   the Copy link buttons point at the shim for whatever theme the sharer is on.

   Every colour comes from the live stylesheet, so a theme change here needs no
   change there. Redacted deliberately maps to Classic: the hidden theme should
   not be the thing that greets someone who has never seen the site.

   Run:  node mkog.js        (writes og-<skin>.png, og.png and t/<skin>.html)
*/
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const SITE = 'file://' + path.join(ROOT, 'index.html');
const W = 1200, H = 630;

/* The host every absolute URL in the shim points at. It must be a host that actually
   serves the images, or the preview comes back with no picture at all -- so it matches
   the host named in index.html's own og tags. The two used to disagree, which meant a
   link to / and a link to /t/red advertised different canonical hosts for the same page.
   If this changes, change SITE_HOST in mksite.py's HEAD to match. */
const HOST = 'https://deadshotleague.com';

/* the five a reader can actually choose; redact is hidden and falls back to og */
const SKINS = ['red', 'og', 'scope', 'leather', 'arcade'];
const FALLBACK = { redact: 'og' };

const card = (lede) => {
  const cs = getComputedStyle(document.documentElement);
  const v = n => cs.getPropertyValue(n).trim();
  const F = [
    [document.querySelector('#f1'), 'SEASONS'],
    [document.querySelector('#f2'), 'MANAGERS'],
    [document.querySelector('#f3'), 'TEAM-SEASONS'],
    [document.querySelector('#f4'), 'GAMES LOGGED'],
  ].map(([el, k]) => [el ? el.textContent.trim() : '', k]);

  const wrap = document.createElement('div');
  wrap.id = '__og';
  wrap.style.cssText = `position:fixed;left:0;top:0;width:1200px;height:630px;z-index:99999;
    background:${v('--mast-bg')};color:${v('--mast-ink')};overflow:hidden;
    display:flex;flex-direction:column;justify-content:center;padding:0 76px;
    font-family:"IBM Plex Sans",sans-serif`;
  wrap.innerHTML = `
    <div style="position:absolute;inset:0;background:radial-gradient(760px 460px at 78% 22%,
      ${v('--mast-glow') || 'transparent'},transparent 70%)"></div>
    <div style="position:absolute;right:84px;top:50%;transform:translateY(-50%);width:186px;height:186px;opacity:.92">
      <svg viewBox="0 0 120 120" style="width:100%;height:100%">
        <circle cx="60" cy="60" r="50" fill="none" stroke="${v('--mast-kick')}" stroke-width="8"/>
        <g stroke="${v('--mast-kick')}" stroke-width="11" stroke-linecap="round">
          <path d="M60 4V40"/><path d="M60 80V116"/><path d="M4 60H40"/><path d="M80 60H116"/></g>
        <circle cx="60" cy="60" r="6.5" fill="${v('--mast-kick')}"/>
      </svg></div>
    <div style="position:relative;max-width:790px">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:19px;letter-spacing:.34em;
        color:${v('--mast-kick')}">FANTASY FOOTBALL &nbsp;·&nbsp; EST. 2015</div>
      <div style="font-family:'Big Shoulders Display',sans-serif;font-weight:900;font-size:132px;
        line-height:.88;letter-spacing:.02em;margin-top:12px">DEADSHOT</div>
      <div style="font-family:Fraunces,Georgia,serif;font-weight:700;font-style:italic;font-size:44px;
        line-height:1;margin-top:2px;color:${v('--mast-kick')}">Archives</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:19px;line-height:1.62;margin-top:22px;
        color:${v('--mast-sub')};max-width:660px">${lede}</div>
      <div style="display:flex;gap:52px;margin-top:30px;padding-top:24px;
        border-top:1px solid ${v('--mast-rule')}">
        ${F.map(([n, k]) => `<div>
          <div style="font-family:'Big Shoulders Display',sans-serif;font-weight:900;font-size:46px;
            line-height:1;color:${v('--mast-kick')}">${n}</div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:.2em;
            margin-top:5px;color:${v('--mast-sub')}">${k}</div></div>`).join('')}
      </div>
    </div>`;
  document.body.appendChild(wrap);
};

/* The shim exists only so a crawler can read theme-specific og tags. A person who
   clicks is bounced straight through to the real page, query and hash intact. */
const shim = (skin, img, T) => `<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Deadshot Record Book</title>
<link rel="canonical" href="${HOST}/">
<meta name="robots" content="noindex">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Deadshot Record Book">
<meta property="og:title" content="Deadshot Record Book">
<meta property="og:description" content="${T.long}">
<meta property="og:url" content="${HOST}/">
<meta property="og:image" content="${HOST}/${img}">
<meta property="og:image:width" content="${W}">
<meta property="og:image:height" content="${H}">
<meta property="og:image:alt" content="${T.alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Deadshot Record Book">
<meta name="twitter:description" content="${T.short}">
<meta name="twitter:image" content="${HOST}/${img}">
<script>
/* a crawler stops at the tags above; a person is sent on with everything they arrived with */
(function(){var q=location.search,h=location.hash;location.replace('/'+q+h);})();
</script>
<noscript><meta name="note" content="no redirect without javascript: a meta refresh cannot
carry the query and hash, and a crawler that honours it would read the main page's default
card instead of this theme's. The link below is the manual way through."></noscript>
<style>body{background:#0A0A0B;color:#DCD7C9;font:15px/1.6 system-ui,sans-serif;
  display:grid;place-items:center;height:100vh;margin:0}a{color:#C8A24A}</style>
</head><body><p>Taking you to the <a href="/">Deadshot Record Book</a>&hellip;</p></body></html>
`;

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  const p = await ctx.newPage();
  await p.goto(SITE, { waitUntil: 'load' });
  await p.waitForTimeout(2200);
  try { await p.evaluate(() => document.fonts.ready); } catch (e) {}

  /* The counts come off the page itself -- the same four figures the masthead shows -- so
     a new season rewrites the card, its alt text and every shim without anyone editing
     this file. They used to be typed in here as "Ten seasons ... 410 games logged". */
  const N = await p.evaluate(() => ({
    seasons: +document.querySelector('#f1').textContent.trim(),
    mgrs: +document.querySelector('#f2').textContent.trim(),
    logged: document.querySelector('#f4').textContent.trim(),
  }));
  const WORD = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
    'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
    'seventeen', 'eighteen', 'nineteen', 'twenty'];
  const w = n => WORD[n] || String(n);              /* digits past twenty */
  const Sz = w(N.seasons)[0].toUpperCase() + w(N.seasons).slice(1);
  const T = {
    card: `${Sz} seasons of champions, standings, power rankings, head-to-head and trades. The whole record book, in one place.`,
    long: `${Sz} seasons of champions, standings, power rankings, head-to-head and trades. The whole league record book, in one place.`,
    short: `${Sz} seasons of champions, standings, power rankings, head-to-head and trades.`,
    alt: `Deadshot Archives: ${w(N.seasons)} seasons, ${w(N.mgrs)} managers, ${N.logged} games logged.`,
  };

  fs.mkdirSync(path.join(ROOT, 't'), { recursive: true });

  for (const skin of SKINS) {
    await p.evaluate(s => {
      const el = document.querySelector('#__og'); if (el) el.remove();
      document.documentElement.dataset.skin = s;
      REDRAW.forEach(f => { try { f(); } catch (e) {} });
    }, skin);
    await p.waitForTimeout(450);
    await p.evaluate(card, T.card);
    await p.waitForTimeout(350);
    const el = await p.$('#__og');
    const file = `og-${skin}.png`;
    await el.screenshot({ path: path.join(ROOT, file) });
    fs.writeFileSync(path.join(ROOT, 't', `${skin}.html`), shim(skin, file, T));
    console.log('  ' + file.padEnd(16) + (fs.statSync(path.join(ROOT, file)).size / 1024).toFixed(0) + 'kb   t/' + skin + '.html');
  }
  /* the hidden theme borrows Classic rather than greeting a stranger with a redaction */
  for (const [from, to] of Object.entries(FALLBACK)) {
    fs.writeFileSync(path.join(ROOT, 't', `${from}.html`), shim(from, `og-${to}.png`, T));
    console.log('  ' + from.padEnd(16) + '-> og-' + to + '.png   t/' + from + '.html');
  }
  /* the bare root keeps a default, which is the site's own default theme */
  fs.copyFileSync(path.join(ROOT, 'og-red.png'), path.join(ROOT, 'og.png'));
  console.log('  og.png           <- og-red.png (the default theme)');

  await b.close();
})();
