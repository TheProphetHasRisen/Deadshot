# -*- coding: utf-8 -*-
import json as _json, hashlib as _hashlib
# site_data.json is stored readable (one field per line) so changes to it are
# legible in git and by eye. The page gets the compact form -- pretty-printing
# inside index.html would add ~100KB to every visitor's download for no benefit.
# json.dumps leaves "<" alone, so a team called "</script>..." closes the tag the data is
# sitting inside and blanks the whole page. Team names come from Yahoo and are whatever a
# manager typed, so this has to be escaped here, at the embed. \u003c is still valid JSON
# and parses back to the same string.
DATA=(_json.dumps(_json.load(open('site_data.json')),separators=(',',':'))
      .replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029'))

HEAD = r"""<title>Deadshot Record Book</title>
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800;900&family=Press+Start+2P&family=Fraunces:opsz,wght@9..144,600;9..144,700;9..144,900&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" crossorigin>
<style>
/* ============ SKINS ============ */
:root,:root[data-skin="scope"]{
  --ground:#080B09; --surface:#0E1411; --surface-2:#131B17;
  --ink:#DCEDE2; --ink-2:#8FA898; --ink-3:#718A79;
  --rule:#1E2E24; --rule-2:#16221B;
  --brass:#35E07A; --brass-2:#1E7A44; --brass-wash:#0D2416;
  --pos:#D9603F; --neg:#3C9FD4; --mid:#3A4A41;
  --sea-1:#35E07A; --sea-2:#E8C24A; --sea-3:#5AB6F0; --sea-4:#FF7A5C; --sea-5:#C08BF5; --sea-6:#6FE8D0; --sea-7:#F58FC8; --sea-8:#C3D94F;
  --shadow:0 1px 2px rgba(0,0,0,.5),0 10px 30px -14px rgba(0,0,0,.8);
  --mast-bg:#080B09; --mast-ink:#EAFBF0; --mast-sub:#8FCFA8; --mast-kick:#35E07A;
  --mast-rule:#16351F; --mast-glow:rgba(53,224,122,.55); --mast-glow2:rgba(53,224,122,.22);
  --head-ink:#EAFBF0; --hover:#16211B; --nav-bg:rgba(14,20,17,.94); --ov:rgba(3,6,4,.82);
  --band:rgba(53,224,122,.06); --glow:rgba(53,224,122,.65);
  --rt:#35E07A; --rt-grid:#1E7A44; --rt-ring:#0E2A18; --rt-g1:#123A22; --rt-g2:#050A07;
  --grid-h:rgba(53,224,122,.045); --grid-v:rgba(53,224,122,.045); --mast-grid:#0F2A19; --mast-vig:rgba(4,7,5,.86);
  --card-r:3px; --wordmark:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  --tex:none; --tex-size:auto; --rule-style:solid;
  --max:1180px;
}
:root[data-skin="og"]{
  --ground:#EDF0F3; --surface:#FFFFFF; --surface-2:#F6F8FA;
  --ink:#10161C; --ink-2:#48545F; --ink-3:#646F7A;
  --rule:#D5DBE1; --rule-2:#E6EAEE;
  --brass:#8C6410; --brass-2:#B8893A; --brass-wash:#F3ECDC;
  --pos:#B0442C; --neg:#1272B0; --mid:#B4BCC4;
  --sea-1:#8C6410; --sea-2:#1F6F60; --sea-3:#245E9E; --sea-4:#A8231F; --sea-5:#6B3E9E; --sea-6:#3B7A2A; --sea-7:#B5541A; --sea-8:#95246F;
  --shadow:0 1px 2px rgba(16,22,28,.06),0 8px 24px -12px rgba(16,22,28,.18);
  --mast-bg:#FFFFFF; --mast-ink:#10161C; --mast-sub:#48545F; --mast-kick:#8C6410;
  --mast-rule:#D5DBE1; --mast-glow:transparent; --mast-glow2:transparent;
  --head-ink:#10161C; --hover:#F1F4F7; --nav-bg:rgba(255,255,255,.94); --ov:rgba(16,22,28,.62);
  --band:rgba(140,100,16,.07); --glow:rgba(140,100,16,.55);
  --rt:#8C6410; --rt-grid:#D9C48C; --rt-ring:#EDE3CC; --rt-g1:#FBF7EC; --rt-g2:#FFFFFF;
  --grid-h:transparent; --grid-v:transparent; --mast-grid:transparent; --mast-vig:transparent; --tex:none;
  --card-r:3px; --tex:none; --rule-style:solid;
}
:root[data-skin="red"]{
  --ground:#F4F1EF; --surface:#FFFFFF; --surface-2:#FAF6F4;
  --ink:#1A1210; --ink-2:#574844; --ink-3:#6E5C57;
  --rule:#E0D6D2; --rule-2:#EFE8E5;
  --brass:#8E1520; --brass-2:#B8434C; --brass-wash:#FBEDED;
  --pos:#B0442C; --neg:#1272B0; --mid:#C3B9B5;
  --sea-1:#9E1723; --sea-2:#1F6F60; --sea-3:#245E9E; --sea-4:#9A7108; --sea-5:#6B3E9E; --sea-6:#3B7A2A; --sea-7:#B5541A; --sea-8:#95246F;
  --shadow:0 1px 2px rgba(26,18,16,.07),0 8px 26px -14px rgba(142,21,32,.22);
  --mast-bg:#8E1520; --mast-ink:#FFFFFF; --mast-sub:#F0C9CC; --mast-kick:#F0C9CC;
  --mast-rule:#6E0F18; --mast-glow:rgba(0,0,0,.28); --mast-glow2:transparent;
  --head-ink:#1A1210; --hover:#FBF4F3; --nav-bg:rgba(255,255,255,.94); --ov:rgba(26,18,16,.62);
  --band:rgba(142,21,32,.055); --glow:rgba(142,21,32,.5);
  --rt:#FFFFFF; --rt-sweep:.30; --rt-grid:#B8434C; --rt-ring:#6E0F18; --rt-g1:#7A1119; --rt-g2:#5C0B12;
  --grid-h:transparent; --grid-v:transparent; --mast-grid:#A32732; --mast-vig:transparent; --tex:none;
  --card-r:3px; --tex-size:auto; --rule-style:solid;
}

[data-skin="scope"] .scopefield{display:block;position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
/* glass vignette — you are looking down a tube */
.scopefield .glass{position:absolute;inset:0;
  background:radial-gradient(76% 60% at 50% 46%,transparent 0%,rgba(3,8,5,.32) 60%,rgba(2,5,3,.92) 100%)}
/* mil-dot reticle, faint enough to read through */
.scopefield .ret{position:absolute;inset:0;width:100%;height:100%;opacity:.15}
.scopefield .ret line,.scopefield .ret path{stroke:#35E07A;fill:none}
.scopefield .corner{stroke:#35E07A;fill:none;stroke-width:2;opacity:.28}
.scopefield .rng{position:absolute;left:0;right:0;height:1px;background:linear-gradient(90deg,
  transparent,rgba(53,224,122,.45) 22%,rgba(53,224,122,.45) 78%,transparent);
  opacity:.45;animation:rangeSweep 17s ease-in-out infinite}
@keyframes rangeSweep{0%,100%{top:14%;opacity:0}6%{opacity:.5}50%{top:86%;opacity:.5}56%{opacity:0}}
.scopefield .hud{position:absolute;left:56px;bottom:16px;font-family:"IBM Plex Mono",monospace;
  font-size:9.5px;letter-spacing:.16em;color:rgba(53,224,122,.42);text-align:left;line-height:1.9}
.scopefield .hud b{color:rgba(214,240,222,.6);font-weight:600}
.scopefield .breathe{animation:breathe 9s ease-in-out infinite}
@keyframes breathe{0%,100%{transform:translate(0,0)}25%{transform:translate(3px,-2px)}
  50%{transform:translate(-2px,3px)}75%{transform:translate(2px,2px)}}
@media (prefers-reduced-motion:reduce){.scopefield .rng,.scopefield .breathe{animation:none!important}}
@media(max-width:760px){.scopefield .hud{display:none}}
:root[data-skin="arcade"]{
  --ground:#07050F; --surface:#120C24; --surface-2:#1B1236;
  --ink:#E8E4FF; --ink-2:#A79DD6; --ink-3:#847BB3;
  --rule:#2E2159; --rule-2:#211846;
  --brass:#FF2E88; --brass-2:#A31E5C; --brass-wash:#2A0C22;
  --pos:#FF8A4C; --neg:#56C7F5; --mid:#443868;
  --sea-1:#FF2E88; --sea-2:#56C7F5; --sea-3:#FFD24A; --sea-4:#7BF59A; --sea-5:#B98BFF; --sea-6:#FF8A4C; --sea-7:#5FE8DE; --sea-8:#FF7FC4;
  --shadow:0 0 0 1px rgba(255,46,136,.12),0 14px 40px -18px rgba(255,46,136,.4);
  --mast-bg:#07050F; --mast-ink:#FFFFFF; --mast-sub:#8FE9FF; --mast-kick:#FF2E88;
  --mast-rule:#2E2159; --mast-glow:rgba(255,46,136,.6); --mast-glow2:rgba(86,199,245,.35);
  --head-ink:#FFFFFF; --hover:#1B1236; --nav-bg:rgba(7,5,15,.95); --ov:rgba(3,2,8,.86);
  --band:rgba(255,46,136,.07); --glow:rgba(255,46,136,.8);
  --rt:#FF2E88; --rt-grid:#4A2C7A; --rt-ring:#1E0F38; --rt-g1:#1B0E3A; --rt-g2:#07040F;
  --grid-h:rgba(255,46,136,.05); --grid-v:rgba(86,199,245,.05); --mast-grid:#241452; --mast-vig:rgba(3,2,8,.82);
  --tex:repeating-linear-gradient(0deg,rgba(0,0,0,.34) 0 1px,transparent 1px 3px);
  --tex-size:auto;
}
:root[data-skin="redact"]{
  --ground:#0A0A0B; --surface:#141416; --surface-2:#1B1B1E;
  --ink:#DCD7C9; --ink-2:#9E988B; --ink-3:#8A8475;
  --rule:#2B2B30; --rule-2:#1F1F23;
  --brass:#C8A24A; --brass-2:#8E7231; --brass-wash:#1D1912;
  --pos:#C0392B; --neg:#5B8CA8; --mid:#3B3B42;
  --sea-1:#C8A24A; --sea-2:#82B3D8; --sea-3:#CC7F6C; --sea-4:#93C289; --sea-5:#B99ED8; --sea-6:#B0B4BE; --sea-7:#7FC9C0; --sea-8:#D493B1;
  --shadow:0 0 0 1px rgba(200,162,74,.1),0 18px 44px -22px rgba(0,0,0,.9);
  --mast-bg:#08080A; --mast-ink:#EDE8DA; --mast-sub:#9E988B; --mast-kick:#B0271F;
  --mast-rule:#2B2B30; --mast-glow:rgba(200,162,74,.28); --mast-glow2:rgba(176,39,31,.2);
  --head-ink:#EDE8DA; --hover:#1B1B1E; --nav-bg:rgba(8,8,10,.96); --ov:rgba(2,2,3,.9);
  --band:rgba(200,162,74,.05); --glow:rgba(200,162,74,.5);
  --rt:#C8A24A; --rt-grid:#3A3A42; --rt-ring:#141416; --rt-g1:#1A1A1E; --rt-g2:#08080A;
  --grid-h:rgba(220,215,201,.028); --grid-v:rgba(220,215,201,.028);
  --mast-grid:#17171B; --mast-vig:rgba(2,2,3,.86);
  --tex:repeating-linear-gradient(0deg,rgba(255,255,255,.014) 0 1px,transparent 1px 2px),
        radial-gradient(circle at 40% 60%,rgba(220,215,201,.02) .6px,transparent 1px);
  --tex-size:auto,7px 7px;
  --card-r:0px; --wordmark:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
}
/* ---- redacted: a file that was never meant to leave the drawer ---- */
[data-skin="redact"] .card,[data-skin="redact"] .plate,[data-skin="redact"] .game,
[data-skin="redact"] .board,[data-skin="redact"] .modal{border-radius:0}
[data-skin="redact"] .card{position:relative}
[data-skin="redact"] .card::before{content:"";position:absolute;left:0;top:0;width:22px;height:22px;
  border-left:2px solid var(--brass);border-top:2px solid var(--brass);opacity:.45;pointer-events:none}
[data-skin="redact"] .card::after{content:"";position:absolute;right:0;bottom:0;width:22px;height:22px;
  border-right:2px solid var(--brass);border-bottom:2px solid var(--brass);opacity:.45;pointer-events:none}
[data-skin="redact"] thead th{background:#000;color:#BDB7A8;letter-spacing:.14em;border-bottom:2px solid var(--brass-2)}
[data-skin="redact"] .sec-head::after{width:74px;height:12px;border-radius:0;bottom:-8px;
  background:#000;box-shadow:0 0 0 1px var(--brass-2)}
[data-skin="redact"] .sec-head h2{letter-spacing:.01em}
[data-skin="redact"] .mast h1{-webkit-text-stroke:0;letter-spacing:.06em}
[data-skin="redact"] .lad-tier span{opacity:.5}
[data-skin="redact"] .mgroup,[data-skin="redact"] .sub-h{color:var(--brass)}
[data-skin="redact"] nav a.on{text-shadow:0 0 10px var(--brass-2)}
/* the stamp and the bars, masthead only */
[data-skin="redact"] .dossier{display:block;position:absolute;inset:0;overflow:hidden;pointer-events:none;z-index:1}
[data-skin="redact"] .dossier svg{width:100%;height:100%}
.dossier .bar{fill:#000;opacity:.92}
.dossier .barline{fill:#fff;opacity:.05}
.dossier .stamp{fill:none;stroke:#B0271F;stroke-width:3;opacity:.82}
.dossier .stampt{fill:#B0271F;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:26px;letter-spacing:.14em;opacity:.86}
.dossier .meta{fill:#8E8779;font-family:"IBM Plex Mono",monospace;font-size:9px;letter-spacing:.17em}
.dossier .blink{animation:redactPulse 4.6s ease-in-out infinite}
@keyframes redactPulse{0%,88%{opacity:.86}92%{opacity:.3}96%{opacity:.86}100%{opacity:.86}}
.dossier .wipe{fill:#000;opacity:.92;animation:redactWipe 13s ease-in-out infinite}
@keyframes redactWipe{0%,42%{transform:scaleX(1)}50%{transform:scaleX(0)}58%,100%{transform:scaleX(1)}}
/* the stamp and file marks sit outside the stretched SVG: preserveAspectRatio="none" skewed
   them 7:1 on a phone. As real elements they scale with the viewport instead of the viewBox. */
.dossier .dz-stamp{position:absolute;right:clamp(6px,2.2vw,24px);top:clamp(8px,2vw,12px);
  transform:rotate(-11deg);transform-origin:100% 0;border:3px solid #B0271F;border-radius:2px;
  color:#B0271F;opacity:.86;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:clamp(16px,4.6vw,27px);letter-spacing:.14em;padding:4px 11px;line-height:1}
.dossier .dz-meta{position:absolute;right:clamp(8px,3vw,42px);bottom:clamp(6px,1.6vw,13px);
  text-align:right;color:#8E8779;font-family:"IBM Plex Mono",monospace;
  font-size:clamp(7px,1.7vw,9px);letter-spacing:.17em;line-height:1.9}
/* the facts row wraps on a phone and would sit under the file marks, so give them their own band */
@media(max-width:900px){[data-skin="redact"] .mast-in{padding-bottom:52px}}
@media (prefers-reduced-motion:reduce){.dossier *,.wr-blob{animation:none!important}}
:root[data-skin="leather"]{
  --ground:#35190F; --surface:#452213; --surface-2:#552C1A;
  --ink:#F6E7D8; --ink-2:#C5A791; --ink-3:#C2A691;
  --rule:#6B4028; --rule-2:#5A3520;
  --brass:#FFFFFF; --brass-2:#C9A88F; --brass-wash:#3E2417;
  --pos:#F08A5C; --neg:#6FC0F0; --mid:#7A5238;
  --sea-1:#F6E7D8; --sea-2:#F0B24A; --sea-3:#7FC5E8; --sea-4:#8FD69A; --sea-5:#E88FA8; --sea-6:#C9A8F0; --sea-7:#F08A5C; --sea-8:#D9D46F;
  --shadow:0 1px 2px rgba(0,0,0,.5),0 10px 26px -14px rgba(0,0,0,.75);
  --mast-bg:#35190F; --mast-ink:#FFFFFF; --mast-sub:#D9BCA4; --mast-kick:#FFFFFF;
  --mast-rule:#6B4028; --mast-glow:rgba(0,0,0,.5); --mast-glow2:rgba(255,255,255,.12);
  --head-ink:#FFFFFF; --hover:#552C1A; --nav-bg:rgba(53,25,15,.95); --ov:rgba(20,9,5,.84);
  --band:rgba(255,255,255,.05); --glow:rgba(255,255,255,.55);
  --rt:#FFFFFF; --rt-sweep:.34; --rt-grid:#7A5238; --rt-ring:#2A1209; --rt-g1:#4A2614; --rt-g2:#2A1209;
  --grid-h:transparent; --grid-v:transparent; --mast-grid:transparent; --mast-vig:rgba(20,9,5,.5);
  --tex:radial-gradient(circle at 30% 30%,rgba(255,232,214,.05) .9px,transparent 1.4px),
        radial-gradient(circle at 70% 70%,rgba(0,0,0,.16) 1px,transparent 1.5px);
  --tex-size:9px 9px;
}
/* ---- skin-specific treatments, not just palette ---- */
[data-skin="leather"] .card,[data-skin="leather"] .board,[data-skin="leather"] .game{
  border-radius:9px}
[data-skin="leather"] .card{position:relative}
[data-skin="leather"] .card::after{content:"";position:absolute;inset:5px;border-radius:6px;pointer-events:none;
  border:1.5px dashed rgba(255,255,255,.13)}
[data-skin="leather"] .plate{border-radius:0}
[data-skin="leather"] .mast h1{-webkit-text-stroke:1px rgba(0,0,0,.25)}
[data-skin="arcade"] .card{border-radius:2px;
  box-shadow:0 0 0 1px rgba(255,46,136,.18),0 0 22px -6px rgba(255,46,136,.35)}
[data-skin="arcade"] .sec-head h2{text-shadow:2px 0 0 rgba(255,46,136,.45),-2px 0 0 rgba(86,199,245,.45)}
[data-skin="arcade"] .mast h1{text-shadow:3px 0 0 rgba(255,46,136,.75),-3px 0 0 rgba(86,199,245,.6),0 0 30px rgba(255,46,136,.5)}
[data-skin="arcade"] .plate .yr{text-shadow:2px 0 0 rgba(86,199,245,.5)}
[data-skin="arcade"] nav a.on{text-shadow:0 0 8px var(--brass)}
/* laces: drawn only on the football skin */
.deco{display:none}
[data-skin="arcade"] .dogfight{display:block;position:absolute;inset:0;overflow:hidden;pointer-events:none;z-index:0;opacity:.62}
[data-skin="arcade"] .dogfight svg{width:100%;height:100%}
.dogfight .ship{fill:#56C7F5;opacity:.85}
.dogfight .ship.chase{fill:#FF2E88;opacity:.9}
.dogfight .bolt{fill:#FFE24A;opacity:.95}
.dogfight .boom{fill:#FFE24A;opacity:0}
.dogfight .flee{animation:fly 9s linear infinite}
.dogfight .chase{animation:fly 9s linear infinite;animation-delay:.62s}
.dogfight .b1{animation:shot 9s linear infinite;animation-delay:1.5s}
.dogfight .b2{animation:shot 9s linear infinite;animation-delay:3.1s}
.dogfight .b3{animation:shot 9s linear infinite;animation-delay:5.4s}
.dogfight .boom{animation:boom 9s linear infinite;animation-delay:6.2s}
@keyframes fly{
  0%{transform:translate(-130px,126px)}
  20%{transform:translate(300px,14px)}
  46%{transform:translate(700px,134px)}
  72%{transform:translate(1060px,16px)}
  100%{transform:translate(1530px,128px)}}
@keyframes shot{
  0%,13%{transform:translate(-30px,132px);opacity:0}
  15%{opacity:1}
  36%{transform:translate(660px,138px);opacity:1}
  42%{opacity:0}
  100%{transform:translate(660px,138px);opacity:0}}
@keyframes boom{
  0%,66%{transform:translate(1080px,20px) scale(.2);opacity:0}
  70%{opacity:.9;transform:translate(1080px,20px) scale(1)}
  77%{opacity:0;transform:translate(1080px,20px) scale(2.2)}
  100%{opacity:0}}
@media (prefers-reduced-motion:reduce){.dogfight *{animation:none!important}.dogfight{opacity:.25}}
.laces{display:none}
[data-skin="leather"] .ball{display:none;position:fixed;right:-70px;bottom:-40px;width:420px;height:262px;
  color:rgba(255,255,255,.055);pointer-events:none;z-index:0}
[data-skin="leather"] .ball svg{width:100%;height:100%}
[data-skin="leather"] .sec-head::after{width:34px;height:11px;border-radius:50%;bottom:-6px;
  background:var(--brass);box-shadow:none}
[data-skin="leather"] thead th{border-bottom:2px solid rgba(255,255,255,.28)}
[data-skin="leather"] .laces{display:none}
@media(max-width:1080px){[data-skin="leather"] .deco{display:none}
.laces{display:none}}
/* Every masthead decoration is a 1400x170 SVG drawn with preserveAspectRatio="none".
   On a phone that squashes it about 3.6:1, which distorts its shapes and drags them
   across the stat line. They are decoration only, so drop them on small screens.
   Same trap the redacted dossier hit at 7.2:1. */
@media(max-width:700px){.mast .deco{display:none!important}}
/* ================= ARCADE: full-page background field ================= */
[data-skin="arcade"] .field{display:block;position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.field .stars{position:absolute;top:-8%;left:0;width:200%;height:116%;background-repeat:repeat;will-change:transform}
.field .s1{background-size:300px 210px;opacity:.9;
  background-image:radial-gradient(1.9px 1.9px at 34px 44px,rgba(232,228,255,1),transparent 100%),
  radial-gradient(1.7px 1.7px at 166px 138px,rgba(86,199,245,.95),transparent 100%),
  radial-gradient(1.6px 1.6px at 248px 60px,rgba(255,46,136,.9),transparent 100%),
  radial-gradient(1.5px 1.5px at 98px 182px,rgba(255,226,74,.8),transparent 100%),
  radial-gradient(1.4px 1.4px at 282px 168px,rgba(232,228,255,.8),transparent 100%),
  radial-gradient(1.3px 1.3px at 122px 96px,rgba(155,123,255,.85),transparent 100%);
  animation:starA 34s linear infinite}
.field .s2{background-size:230px 160px;opacity:.6;
  background-image:radial-gradient(1.2px 1.2px at 60px 24px,rgba(232,228,255,.8),transparent 100%),
  radial-gradient(1.1px 1.1px at 210px 120px,rgba(167,157,214,.8),transparent 100%),
  radial-gradient(1px 1px at 130px 168px,rgba(86,199,245,.7),transparent 100%);
  animation:starB 62s linear infinite}
.field .s3{background-size:160px 120px;opacity:.38;
  background-image:radial-gradient(.9px .9px at 22px 96px,rgba(232,228,255,.75),transparent 100%),
  radial-gradient(.9px .9px at 142px 30px,rgba(255,46,136,.6),transparent 100%);
  animation:starC 104s linear infinite}
@keyframes starA{from{transform:translate3d(0,0,0)}to{transform:translate3d(-300px,0,0)}}
@keyframes starB{from{transform:translate3d(0,0,0)}to{transform:translate3d(-230px,0,0)}}
@keyframes starC{from{transform:translate3d(0,0,0)}to{transform:translate3d(-160px,0,0)}}
.field .sky{position:absolute;inset:0;width:100%;height:100%;opacity:.6}
.field .fs{fill:#56C7F5}
.field .fs.hot{fill:#FF2E88}
.field .fb{fill:#FFE24A}
.field .inv{fill:#9B7BFF;opacity:.5}
/* top lane: a slow chase across the whole page */
.field .lane1 .run{animation:laneA 26s linear infinite}
.field .lane1 .hunt{animation:laneA 26s linear infinite;animation-delay:1.1s}
.field .lane1 .t1{animation:tracerA 26s linear infinite;animation-delay:5s}
.field .lane1 .t2{animation:tracerA 26s linear infinite;animation-delay:11.5s}
.field .lane1 .pop{animation:popA 26s linear infinite;animation-delay:17.6s}
@keyframes laneA{
  0%{transform:translate(-220px,690px)} 22%{transform:translate(340px,300px)}
  50%{transform:translate(820px,640px)} 78%{transform:translate(1280px,250px)}
  100%{transform:translate(1820px,560px)}}
@keyframes tracerA{
  0%,8%{transform:translate(-140px,700px);opacity:0} 10%{opacity:1}
  26%{transform:translate(700px,470px);opacity:1} 31%{opacity:0}
  100%{transform:translate(700px,470px);opacity:0}}
@keyframes popA{
  0%,64%{transform:translate(1290px,255px) scale(.2);opacity:0}
  68%{opacity:.85;transform:translate(1290px,255px) scale(1)}
  76%{opacity:0;transform:translate(1290px,255px) scale(2.6)}
  100%{opacity:0}}
/* bottom lane: a lone runner the other way */
.field .lane2 .run{animation:laneB 41s linear infinite}
@keyframes laneB{
  0%{transform:translate(1780px,180px) scaleX(-1)} 40%{transform:translate(900px,420px) scaleX(-1)}
  70%{transform:translate(420px,150px) scaleX(-1)} 100%{transform:translate(-260px,380px) scaleX(-1)}}
/* marching invaders, deep background */
.field .sq1{animation:marchA 19s steps(14) infinite}
.field .sq2{animation:marchB 27s steps(18) infinite}
@keyframes marchA{0%{transform:translate(-180px,120px)}100%{transform:translate(1760px,120px)}}
@keyframes marchB{0%{transform:translate(1740px,810px)}100%{transform:translate(-200px,810px)}}
[data-skin="arcade"] .card,[data-skin="arcade"] .plate,[data-skin="arcade"] .game,
[data-skin="arcade"] .board,[data-skin="arcade"] .modal{background-color:rgba(18,12,36,.9)}
[data-skin="arcade"] #wkYears{background-color:rgba(7,5,15,.94)}
@media(max-width:760px){[data-skin="arcade"] .field .sky{display:none}}
/* ================= CRIMSON: sniper masthead ================= */
[data-skin="red"] .snipe{display:block;position:absolute;inset:0;overflow:hidden;pointer-events:none;z-index:1}
[data-skin="red"] .snipe svg{width:100%;height:100%}
.snipe .rule{stroke:#FFFFFF;opacity:.2}
.snipe .rule2{stroke:#FFFFFF;opacity:.14}
.snipe .lab{fill:#FFFFFF;font-family:"IBM Plex Mono",monospace;font-size:9px;letter-spacing:.2em;opacity:.5;text-anchor:middle}
.snipe .stad .base{stroke:#FFFFFF;stroke-width:1.4;opacity:.22;fill:none}
.snipe .stad .tick{stroke:#FFFFFF;stroke-width:1.5;opacity:.3;fill:none}
.snipe .stad .tickM{stroke:#FFFFFF;stroke-width:2.4;opacity:.6;fill:none;stroke-linecap:round}
.snipe .gate{stroke:#FFFFFF;stroke-width:2;fill:none;opacity:.9;stroke-linecap:round;
  animation:gateRun 9s cubic-bezier(.35,.05,.2,1) infinite}
@keyframes gateRun{
  0%{transform:translateX(490px);opacity:0}
  8%{opacity:.85}
  44%{transform:translateX(1322px);opacity:.85}
  50%{opacity:.35}54%{opacity:.95}
  76%{transform:translateX(1322px);opacity:.95}
  86%{opacity:0}100%{transform:translateX(490px);opacity:0}}
.snipe .apex{stroke:#FFFFFF;fill:#FFFFFF;stroke-width:1.4;opacity:.5}
.snipe .tag{fill:#F0C9CC;font-family:"IBM Plex Mono",monospace;font-size:8px;letter-spacing:.14em;opacity:.55}
.snipe .tgt{fill:#FFFFFF;opacity:.5;animation:tdrift 15s ease-in-out infinite alternate}
.snipe .brk{stroke:#FFFFFF;fill:none;stroke-width:2;opacity:0;transform-origin:1322px 130px;
  animation:lock 9s cubic-bezier(.3,.7,.2,1) infinite}
.snipe .arc{stroke:#F6D8DA;fill:none;stroke-width:1.4;stroke-dasharray:5 7;opacity:.28;
  stroke-dashoffset:0;animation:drift2 3.4s linear infinite}
.snipe .trace{stroke:#FFFFFF;stroke-width:2;stroke-linecap:round;opacity:0;
  stroke-dasharray:1180;stroke-dashoffset:1180;animation:fire 9s linear infinite}
.snipe .hit{stroke:#FFFFFF;fill:none;stroke-width:2.2;opacity:0;transform-origin:1322px 130px;
  animation:impact 9s linear infinite}
.snipe .rd{fill:#FFFFFF;font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.14em;opacity:0;text-anchor:end}
.snipe .rd1{animation:read 9s linear infinite}
.snipe .rd2{animation:read 9s linear infinite;animation-delay:2.4s}
.snipe .rd3{animation:read 9s linear infinite;animation-delay:4.8s}
.snipe .sweep{stroke:#FFFFFF;stroke-width:1.3;opacity:.18;animation:snipeSweep 9s ease-in-out infinite}
@keyframes tdrift{from{transform:translateX(-26px)}to{transform:translateX(22px)}}
@keyframes lock{
  0%{transform:scale(3.4);opacity:0} 12%{opacity:.55}
  46%{transform:scale(1);opacity:.95} 62%{opacity:.35} 66%{opacity:.95}
  78%{transform:scale(1);opacity:0} 100%{transform:scale(3.4);opacity:0}}
@keyframes fire{
  0%,60%{stroke-dashoffset:1180;opacity:0}
  61%{opacity:.95} 66%{stroke-dashoffset:0;opacity:.95} 70%{opacity:0}
  100%{stroke-dashoffset:0;opacity:0}}
@keyframes impact{
  0%,66%{transform:scale(.2);opacity:0}
  69%{transform:scale(1);opacity:.9} 78%{transform:scale(3);opacity:0} 100%{opacity:0}}
@keyframes read{0%,2%{opacity:0}6%{opacity:.85}24%{opacity:.85}28%{opacity:0}100%{opacity:0}}
@keyframes snipeSweep{0%{transform:translateX(-120px)}50%{transform:translateX(1320px)}100%{transform:translateX(-120px)}}
@keyframes drift2{to{stroke-dashoffset:-24}}
@media (prefers-reduced-motion:reduce){.snipe *,.field *{animation:none!important}
  .snipe .brk,.snipe .rd1{opacity:.6!important;transform:scale(1)!important}}
@media(max-width:900px){[data-skin="red"] .snipe .lab,[data-skin="red"] .snipe .rd,
  [data-skin="red"] .snipe .tag,[data-skin="red"] .snipe .apex{display:none}}
/* ================= PIGSKIN: the field, the ball, the stitching ================= */
[data-skin="leather"] .gridiron{display:block;position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.gridiron .yard{position:absolute;inset:0;
  background-image:repeating-linear-gradient(90deg,rgba(255,255,255,.055) 0 2px,transparent 2px 78px)}
.gridiron .yard5{position:absolute;inset:0;
  background-image:repeating-linear-gradient(90deg,rgba(255,255,255,.1) 0 3px,transparent 3px 390px)}
.gridiron .hash{position:absolute;left:0;right:0;height:9px;
  background-image:repeating-linear-gradient(90deg,rgba(255,255,255,.075) 0 2px,transparent 2px 26px)}
.gridiron .h1{top:31%}.gridiron .h2{top:69%}
.gridiron .goal{position:absolute;right:2.5vw;top:50%;width:130px;height:150px;margin-top:-75px;opacity:.1}
.gridiron .goal svg{width:100%;height:100%}
.gridiron .trail{position:absolute;inset:0;width:100%;height:100%;opacity:.16}
.gridiron .trail path{fill:none;stroke:#FFF;stroke-width:2;stroke-dasharray:3 12;stroke-linecap:round}
/* the ball itself — square box, so it never distorts */
.pball{position:absolute;left:0;top:0;width:66px;height:44px}
.pball svg{width:100%;height:100%;display:block}
.pball .hide{fill:#7A3F1C;stroke:#4E2710;stroke-width:3}
.pball .stripe{stroke:#FFF6EC;stroke-width:3.4;fill:none;stroke-linecap:round}
.pball .lace{stroke:#FFF6EC;stroke-width:3.6;stroke-linecap:round}
.gridiron .pball{animation:punt 24s cubic-bezier(.36,.03,.62,1) infinite}
@keyframes punt{
  0%{transform:translate(-12vw,84vh) rotate(-40deg);opacity:0}
  5%{opacity:.9}
  28%{transform:translate(24vw,22vh) rotate(110deg)}
  50%{transform:translate(50vw,7vh) rotate(230deg)}
  72%{transform:translate(76vw,18vh) rotate(350deg)}
  95%{transform:translate(102vw,60vh) rotate(480deg);opacity:.9}
  100%{transform:translate(112vw,76vh) rotate(510deg);opacity:0}}
/* masthead: sideline strip, goalposts, a ball on a dotted arc */
[data-skin="leather"] .pigskin{display:block;position:absolute;inset:0;overflow:hidden;pointer-events:none;z-index:1}
[data-skin="leather"] .pigskin svg.chalk{width:100%;height:100%}
.pigskin .yl{stroke:#FFF;opacity:.2}
.pigskin .yl5{stroke:#FFF;opacity:.34}
.pigskin .hm{stroke:#FFF;opacity:.24}
.pigskin .yn{fill:#FFF;opacity:.3;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:20px;letter-spacing:.06em}
.pigskin .gp{stroke:#F6E7D8;opacity:.34;fill:none;stroke-width:3.2;stroke-linecap:round}
.pigskin .parc{fill:none;stroke:#FFF;stroke-width:1.6;stroke-dasharray:3 9;opacity:.3;
  animation:pdrift 3s linear infinite}
@keyframes pdrift{to{stroke-dashoffset:-24}}
.pigskin .pball{animation:snap 11s cubic-bezier(.32,.02,.5,1) infinite}
@keyframes snap{
  0%,4%{transform:translate(61.5vw,150px) rotate(-42deg) scale(.6);opacity:0}
  11%{opacity:1}
  38%{transform:translate(76vw,36px) rotate(140deg) scale(.86)}
  60%{transform:translate(83vw,25px) rotate(250deg) scale(.92)}
  84%{transform:translate(92vw,44px) rotate(400deg) scale(.9)}
  96%{transform:translate(95.8vw,66px) rotate(462deg) scale(.86);opacity:1}
  100%{transform:translate(96.5vw,72px) rotate(474deg) scale(.86);opacity:0}}
/* stitching, everywhere a seam belongs */
[data-skin="leather"] nav{border-top:2px dashed rgba(255,255,255,.22)}
[data-skin="leather"] .sec-head::after{width:52px;height:9px;border-radius:0;bottom:-7px;background:none;
  box-shadow:none;border-top:3px solid rgba(255,255,255,.9);
  background-image:repeating-linear-gradient(90deg,#FFF 0 8px,transparent 8px 15px);
  background-size:100% 3px;background-position:0 6px;background-repeat:no-repeat}
[data-skin="leather"] thead th{background:linear-gradient(180deg,#5F3320,#4A2716);letter-spacing:.11em}
[data-skin="leather"] .card,[data-skin="leather"] .plate,[data-skin="leather"] .game,
[data-skin="leather"] .board,[data-skin="leather"] .modal{background-color:rgba(69,34,19,.94)}
[data-skin="leather"] #wkYears{background-color:rgba(53,25,15,.95)}
@media (prefers-reduced-motion:reduce){.gridiron *,.pigskin *{animation:none!important}}
@media(max-width:820px){.gridiron .goal,.pigskin .yn{display:none}}
/* An element with an inline display beats the hidden attribute, which is exactly how the
   trade grid stayed on screen while its own card said it was collapsed. */
[hidden]{display:none!important}
.gl{display:inline-flex;align-items:center;justify-content:center;width:17px;height:17px;
  border-radius:50%;border:1px solid var(--brass-2);color:var(--brass);background:transparent;
  font-size:10px;font-weight:700;font-family:"IBM Plex Mono",monospace;line-height:1;
  cursor:help;vertical-align:middle;margin-left:5px;flex:none;user-select:none}
.gl:hover,.gl:focus{background:var(--brass);color:var(--surface);outline:none}
/* the coarse-pointer bump below is on .gl alone, which loses to `th .gl-th` on
   specificity, so a header "?" stayed a 14px target on a phone */
@media(pointer:coarse){th .gl-th{width:23px;height:23px;font-size:12px}}
/* the in-header version rides small and low-key, so twelve of them across a stats table
   read as punctuation rather than as twelve more things to look at */
th .gl-th{width:14px;height:14px;font-size:8.5px;margin-left:6px;border-color:var(--rule);
  color:var(--ink-3);opacity:.75;text-transform:none;letter-spacing:0}
th .gl-th:hover,th .gl-th:focus{opacity:1;border-color:var(--brass-2);background:var(--brass);
  color:var(--surface)}
.plain{margin:9px 0 0;font-size:12.5px;color:var(--ink-2);line-height:1.5}
@media(pointer:coarse){
  button,select,input[type=search]{min-height:36px}
  .gl{width:23px;height:23px;font-size:12.5px;margin-left:7px}
  .pills button,.fb button{padding:9px 13px}
  table.mtx td span{min-height:30px;display:inline-flex;align-items:center;justify-content:center}
  #ladder .lad{padding:9px 6px}
  .hlc{padding:17px 16px}}
.plain b{color:var(--ink)}
/* power ladder */
#ladder{display:flex;flex-direction:column;gap:2px;font-size:13px}
.lad-head,.lad{display:grid;grid-template-columns:26px minmax(96px,1.35fr) minmax(150px,3fr) 54px 64px 46px 34px;
  align-items:center;gap:10px}
.lad-head{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.09em;text-transform:uppercase;
  color:var(--ink-3);padding:0 6px 6px;border-bottom:1px solid var(--rule-2);margin-bottom:4px}
.lad-head>span:nth-child(n+4){text-align:right}
.lad-track-h{position:relative;height:11px}
.lad-track-h i{position:absolute;font-style:normal;white-space:nowrap}
.lad{padding:5px 6px;border-radius:3px;cursor:pointer;color:var(--ink);transition:background .12s}
.lad:hover{background:var(--hover)}
.lad.top .lad-n{font-weight:700}
.lad-r{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--ink-3);text-align:right}
.lad.top .lad-r{color:var(--brass);font-weight:700}
.lad-n{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lad-track{position:relative;height:16px;background:var(--surface-2);border-radius:2px;overflow:hidden}
.lad-mid{display:none}
.lad-bar{position:absolute;top:3px;bottom:3px;border-radius:1px;opacity:.8;
  transition:left .32s cubic-bezier(.4,0,.2,1),width .32s cubic-bezier(.4,0,.2,1)}
.lad-dot{position:absolute;top:50%;width:9px;height:9px;margin:-4.5px 0 0 -4.5px;border-radius:50%;
  box-shadow:0 0 0 2px var(--surface);transition:left .32s cubic-bezier(.4,0,.2,1)}
.lad-s{text-align:right;font-family:"IBM Plex Mono",monospace;font-weight:700;font-variant-numeric:tabular-nums}
.lad-w{text-align:right;font-family:"IBM Plex Mono",monospace;color:var(--ink-2);font-size:12px;font-variant-numeric:tabular-nums}
.lad-mv{text-align:right;font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--ink-3)}
.lad-mv.up{color:var(--pos)}.lad-mv.dn{color:var(--neg)}
.lad-ev{text-align:right;font-size:8px;letter-spacing:.5px;white-space:nowrap}
.lad-tier{display:flex;align-items:center;gap:8px;font-family:"IBM Plex Mono",monospace;font-size:9px;
  letter-spacing:.16em;text-transform:uppercase;margin:9px 6px 3px;opacity:.85}
.lad-tier span{flex:1;height:1px;background:currentColor;opacity:.3}
@media(max-width:720px){.lad-head,.lad{grid-template-columns:22px minmax(72px,1fr) 46px 52px 38px}
  .lad-ev{display:none}
  .lad-track,.lad-track-h{display:none}}
.hl{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,268px),1fr));gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:var(--card-r);overflow:hidden;box-shadow:var(--shadow)}
.hlc{background:var(--surface);color:var(--ink);padding:15px 16px 14px;display:flex;flex-direction:column;gap:3px;
  border:0;text-align:left;font-family:inherit;font-size:inherit;cursor:pointer;transition:background .12s;position:relative}
.hlc:hover{background:var(--surface-2)}
.hlc .k{font-family:"IBM Plex Mono",monospace;font-size:9.5px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--brass);font-weight:600}
.hlc .v{font-family:Fraunces,Georgia,serif;font-weight:700;font-size:21px;line-height:1.15;margin-top:5px;
  font-variation-settings:"opsz" 40;color:var(--ink)}
.hlc .n{font-size:12.5px;color:var(--ink-2);line-height:1.5;margin-top:4px}
.hlc .n b{color:var(--ink)}
.hlc .fig{position:absolute;right:14px;top:12px;font-family:"IBM Plex Mono",monospace;font-size:11px;
  color:var(--ink-3);font-variant-numeric:tabular-nums}
.toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%) translateY(14px);z-index:200;
  width:max-content;max-width:min(92vw,460px);
  background:#000;color:#DCD7C9;border:1px solid var(--brass-2);border-radius:2px;
  padding:11px 18px;font-family:"IBM Plex Mono",monospace;font-size:12.5px;letter-spacing:.06em;
  box-shadow:0 12px 40px rgba(0,0,0,.5);opacity:0;pointer-events:none;transition:opacity .3s,transform .3s}
.toast.on{opacity:1;transform:translateX(-50%) translateY(0)}
.toast.warn{border-color:#B0271F;color:#F0D9D6;box-shadow:0 0 0 1px rgba(176,39,31,.35),0 0 34px rgba(176,39,31,.28),0 12px 40px rgba(0,0,0,.6);line-height:1.7}
.toast.warn .sig{color:#E0392B;margin-right:6px}
.toast.warn .dim2{color:#9E8C8A;font-size:11px;letter-spacing:.14em;text-transform:uppercase}
.toast .cur{display:inline-block;width:7px;margin-left:5px;color:#E0392B;animation:caret 1s steps(1) infinite}
@keyframes caret{0%,49%{opacity:1}50%,100%{opacity:0}}
/* the room closing in */
.omen{position:fixed;inset:0;z-index:150;pointer-events:none;opacity:0;
  transition:opacity .55s ease;background:
    radial-gradient(74% 58% at 50% 40%,transparent 0%,rgba(58,0,0,.5) 50%,rgba(3,0,0,.97) 100%),
    linear-gradient(rgba(7,0,0,.42),rgba(7,0,0,.42))}
.omen::after{content:"";position:absolute;inset:0;opacity:.5;
  background:repeating-linear-gradient(0deg,rgba(224,57,43,.05) 0 1px,transparent 1px 3px)}
.omen.lv3{opacity:.42}.omen.lv4{opacity:.72}.omen.lv5{opacity:.95}
.omen.lv4,.omen.lv5{animation:omenFlick 2.4s steps(1) infinite}
@keyframes omenFlick{0%,92%{filter:none}94%{filter:brightness(1.7)}96%{filter:none}98%{filter:brightness(1.4)}100%{filter:none}}
.mast .scope.hot{filter:drop-shadow(0 0 14px rgba(224,57,43,.85));animation:scopeHot .9s ease-in-out infinite}
@keyframes scopeHot{0%,100%{filter:drop-shadow(0 0 10px rgba(224,57,43,.6))}
  50%{filter:drop-shadow(0 0 22px rgba(224,57,43,1))}}
/* the sixth round */
.breach{position:fixed;inset:0;z-index:400;pointer-events:none;display:none;overflow:hidden}
.breach.on{display:block}
.breach .void{position:absolute;inset:0;background:#000;opacity:0;transition:opacity .5s ease}
.breach .void.in{opacity:1}
.breach .flash{position:absolute;inset:0;background:#fff;opacity:0}
.breach .hole{position:absolute;width:0;height:0}
.breach .hole i,.breach .hole b{position:absolute;left:0;top:0;border-radius:50%;transform:translate(-50%,-50%)}
.breach .hole i{width:26px;height:26px;background:radial-gradient(circle,#000 34%,rgba(20,0,0,.6) 62%,transparent 72%);
  box-shadow:0 0 0 2px rgba(255,120,60,.55),0 0 26px rgba(255,120,40,.75);
  opacity:0;animation:holePunch .3s ease-out forwards}
.breach .hole b{width:16px;height:16px;background:#FFE8B0;opacity:0;
  animation:holeFlash .34s ease-out forwards}
@keyframes holePunch{0%{opacity:0;transform:translate(-50%,-50%) scale(.2)}
  30%{opacity:1;transform:translate(-50%,-50%) scale(1.25)}100%{opacity:1;transform:translate(-50%,-50%) scale(1)}}
@keyframes holeFlash{0%{opacity:1;transform:translate(-50%,-50%) scale(.4)}
  100%{opacity:0;transform:translate(-50%,-50%) scale(3.4)}}
.breach .flash.go{animation:breachFlash .5s ease-out forwards}
@keyframes breachFlash{0%{opacity:0}6%{opacity:1}22%{opacity:.35}55%{opacity:.12}100%{opacity:0}}
.breach .cracks{position:absolute;inset:0;width:100%;height:100%}
.breach .crack{fill:none;stroke:#FFF;stroke-linecap:round;stroke-linejoin:round;
  filter:drop-shadow(0 0 5px rgba(224,57,43,.95)) drop-shadow(0 0 14px rgba(224,57,43,.5));
  stroke-dasharray:var(--len);stroke-dashoffset:var(--len);
  animation:crackDraw .34s cubic-bezier(.2,.8,.3,1) forwards}
.breach .crack.case{stroke:#0A0004;opacity:.72;filter:none}
@keyframes crackDraw{to{stroke-dashoffset:0}}
.breach .shard{position:absolute;inset:0;background:#050506;opacity:0;
  box-shadow:inset 0 0 0 1px rgba(224,57,43,.28);will-change:transform,opacity}
.breach .shard.go{animation:shardOut .9s cubic-bezier(.18,.72,.28,1) forwards}
@keyframes shardOut{0%{opacity:0;transform:none}10%{opacity:1;transform:none}
  100%{opacity:0;transform:translate(var(--dx),var(--dy)) rotate(var(--rot)) scale(1.3)}}
body.breaching>.mast,body.breaching>nav,body.breaching>.wrap{
  animation:quakeHard .62s cubic-bezier(.36,.07,.19,.97)}
@keyframes quakeHard{
  8%{transform:translate3d(-9px,4px,0) rotate(-.35deg)}
  18%{transform:translate3d(11px,-6px,0) rotate(.4deg)}
  30%{transform:translate3d(-13px,5px,0) rotate(-.45deg)}
  44%{transform:translate3d(9px,-4px,0) rotate(.3deg)}
  60%{transform:translate3d(-6px,3px,0) rotate(-.2deg)}
  78%{transform:translate3d(3px,-2px,0)}
  100%{transform:none}}
@media (prefers-reduced-motion:reduce){.breach .shard,.breach .crack,.breach .flash{animation:none!important}
  body.breaching>*{animation:none!important}}
body.quake>.mast,body.quake>nav,body.quake>.wrap{
  animation:quake .5s cubic-bezier(.36,.07,.19,.97)}
@keyframes quake{10%,90%{transform:translate3d(-1px,0,0)}20%,80%{transform:translate3d(2px,0,0)}
  30%,50%,70%{transform:translate3d(-3px,0,0)}40%,60%{transform:translate3d(3px,0,0)}
  100%{transform:none}}
@media (prefers-reduced-motion:reduce){.omen{animation:none!important}
  .mast .scope.hot{animation:none!important}body.quake>*{animation:none!important}}
.toast b{color:var(--brass);font-weight:700}
[data-skin-btn="redact"]{font-family:"IBM Plex Mono",monospace;letter-spacing:.1em}
.mast .scope{cursor:pointer}
details.expl{border-top:0}
details.expl>summary{cursor:pointer;list-style:none;font-family:"IBM Plex Mono",monospace;font-size:10.5px;
  text-transform:uppercase;letter-spacing:.11em;color:var(--brass);font-weight:600;padding:3px 0;
  display:flex;align-items:center;gap:7px}
details.expl>summary::-webkit-details-marker{display:none}
details.expl>summary::before{content:"\25B8";display:inline-block;transition:transform .16s;font-size:11px}
details.expl[open]>summary::before{transform:rotate(90deg)}
details.expl>summary:hover{color:var(--ink)}
details.expl>p,details.expl .plain{margin-top:9px}
.rules{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,232px),1fr));gap:16px 22px}
.rules h4{font-family:"IBM Plex Mono",monospace;font-size:10px;text-transform:uppercase;letter-spacing:.12em;
  color:var(--brass);font-weight:600;margin:0 0 6px}
.rules ul{margin:0;padding-left:16px;font-size:12.5px;line-height:1.65;color:var(--ink-2)}
.rules li b{color:var(--ink)}
/* ================= THE PHARAOH ================= */
.pharaoh{position:fixed;inset:0;z-index:500;pointer-events:none;display:none;overflow:hidden;
  background:radial-gradient(120% 90% at 50% 62%,#241206 0%,#0A0503 52%,#000 100%);opacity:0}
.pharaoh.on{display:block;animation:phIn .7s ease forwards}
.pharaoh.out{animation:phOut 1.1s ease forwards}
@keyframes phIn{to{opacity:1}}
@keyframes phOut{to{opacity:0}}
.ph-rays{position:absolute;left:50%;top:58%;width:200vmax;height:200vmax;margin:-100vmax 0 0 -100vmax;
  opacity:0;animation:phRays 7.7s ease-out forwards;
  background:repeating-conic-gradient(from 0deg,rgba(255,140,32,.2) 0deg 3.5deg,rgba(227,178,60,.07) 3.5deg 7deg,transparent 7deg 15deg)}
@keyframes phRays{0%{opacity:0;transform:rotate(0) scale(.4)}
  18%{opacity:.85}70%{opacity:.5}100%{opacity:0;transform:rotate(26deg) scale(1.1)}}
.ph-glow{position:absolute;left:50%;top:60%;width:120vmin;height:120vmin;margin:-60vmin 0 0 -60vmin;
  border-radius:50%;opacity:0;animation:phGlow 7.7s ease-out forwards;
  background:radial-gradient(circle,rgba(255,168,60,.62) 0%,rgba(200,60,20,.2) 34%,transparent 68%)}
@keyframes phGlow{0%{opacity:0;transform:scale(.3)}22%{opacity:1;transform:scale(1)}
  75%{opacity:.7}100%{opacity:0;transform:scale(1.25)}}
.ph-mask{position:absolute;left:50%;bottom:-9vh;width:min(66vh,470px);
  transform:translate(-50%,26vh) scale(.84);opacity:0;
  animation:phRise 7.7s cubic-bezier(.16,.85,.24,1) forwards;
  filter:drop-shadow(0 0 46px rgba(255,150,50,.6)) drop-shadow(0 0 90px rgba(190,40,10,.4))}
@keyframes phRise{0%{transform:translate(-50%,34vh) scale(.8);opacity:0}
  16%{opacity:1}34%{transform:translate(-50%,0) scale(1);opacity:1}
  78%{transform:translate(-50%,-1vh) scale(1.02);opacity:1}
  100%{transform:translate(-50%,-6vh) scale(1.05);opacity:0}}
.ph-mask svg{width:100%;height:auto;display:block}
.ph-shine{animation:phShine 7.7s ease-in-out forwards}
@keyframes phShine{0%,20%{transform:translateX(-420px)}52%{transform:translateX(420px)}100%{transform:translateX(420px)}}
.ph-txt{position:absolute;left:0;right:0;top:5%;text-align:center;padding:0 18px;z-index:3;
  text-shadow:0 6px 34px rgba(0,0,0,.85),0 0 60px rgba(0,0,0,.7)}
.ph-txt div{font-family:var(--wordmark),"Big Shoulders Display",Impact,sans-serif;font-weight:900;
  line-height:.96;letter-spacing:.06em;opacity:0;
  background:linear-gradient(180deg,#FFF0C0 6%,#E3B23C 46%,#A5761F 96%);
  -webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 3px 0 rgba(0,0,0,.45)) drop-shadow(0 0 26px rgba(227,178,60,.65))}
.ph-txt .l1{font-size:clamp(34px,8.4vw,104px);animation:phL 7.7s cubic-bezier(.14,.9,.2,1) forwards;animation-delay:.55s}
.ph-txt .l2{font-size:clamp(22px,5.1vw,62px);margin-top:.12em;
  animation:phL 7.7s cubic-bezier(.14,.9,.2,1) forwards;animation-delay:1.05s}
@keyframes phL{0%{opacity:0;letter-spacing:.5em;transform:scale(1.12)}
  10%{opacity:1;letter-spacing:.06em;transform:scale(1)}
  80%{opacity:1}100%{opacity:0;transform:scale(1.03)}}
.ph-g{position:absolute;color:#E3B23C;opacity:0;animation:phFloat 7.7s ease-out forwards}
.ph-g svg{width:100%;height:100%;display:block;opacity:.8}
@keyframes phFloat{0%{opacity:0;transform:translateY(30px) rotate(0)}
  18%{opacity:.85}80%{opacity:.3}100%{opacity:0;transform:translateY(-58vh) rotate(18deg)}}
.ph-sand{position:absolute;inset:0;opacity:0;animation:phSand 7.7s ease-out forwards;
  background:radial-gradient(1.6px 1.6px at 20% 70%,rgba(255,214,120,.9),transparent),
    radial-gradient(1.3px 1.3px at 70% 40%,rgba(255,214,120,.7),transparent),
    radial-gradient(1.5px 1.5px at 44% 88%,rgba(255,230,170,.8),transparent),
    radial-gradient(1.2px 1.2px at 86% 76%,rgba(255,214,120,.6),transparent);
  background-size:280px 280px,190px 190px,240px 240px,160px 160px}
@keyframes phSand{0%{opacity:0;background-position:0 0,0 0,0 0,0 0}
  25%{opacity:.9}100%{opacity:0;background-position:0 -300px,0 -220px,0 -260px,0 -180px}}
@media (prefers-reduced-motion:reduce){.pharaoh *{animation-duration:.01s!important}}
.botcall{position:fixed;inset:0;z-index:320;display:flex;align-items:center;justify-content:center;
  background:rgba(2,6,4,.9);animation:bcIn .22s ease-out;font-family:"IBM Plex Mono",monospace}
.botcall.out{animation:bcOut .7s ease-in forwards}
@keyframes bcIn{from{opacity:0}to{opacity:1}}
@keyframes bcOut{to{opacity:0}}
.botcall .bc-in{position:relative;text-align:center;padding:34px 52px;border:1px solid #35E07A;
  background:rgba(4,14,8,.94);box-shadow:0 0 0 1px rgba(53,224,122,.25),0 0 60px rgba(53,224,122,.28);overflow:hidden}
.botcall .bc-scan{position:absolute;left:0;right:0;height:34%;top:-40%;
  background:linear-gradient(180deg,transparent,rgba(53,224,122,.16),transparent);
  animation:bcScan 1.5s linear infinite}
@keyframes bcScan{to{top:110%}}
.botcall .bc-tag{font-size:10px;letter-spacing:.34em;color:#35E07A;opacity:.75}
.botcall .bc-l1{font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;font-weight:900;
  font-size:clamp(46px,10vw,104px);line-height:.95;color:#EAFFF2;letter-spacing:.04em;margin-top:8px;
  text-shadow:0 0 26px rgba(53,224,122,.6),3px 0 0 rgba(255,46,136,.5),-3px 0 0 rgba(86,199,245,.4);
  animation:bcGlitch 2.4s steps(1) infinite}
.botcall .bc-l2{font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;font-weight:900;
  font-size:clamp(34px,7.4vw,74px);line-height:1;color:#35E07A;letter-spacing:.16em;
  text-shadow:0 0 30px rgba(53,224,122,.75)}
@keyframes bcGlitch{0%,88%{transform:none}90%{transform:translateX(-4px) skewX(-6deg)}
  92%{transform:translateX(5px) skewX(5deg)}94%{transform:none}}
.botcall .bc-sub{margin-top:12px;font-size:11.5px;letter-spacing:.2em;color:#8FE9C4;opacity:.8}
.botcall .bc-bits{margin-top:6px;font-size:10px;letter-spacing:.3em;color:#35E07A;opacity:.4}
@media (prefers-reduced-motion:reduce){.botcall *{animation:none!important}}
/* the reigning champion, in his own colours */
.kdef{position:fixed;inset:0;z-index:320;display:flex;align-items:center;justify-content:center;
  background:radial-gradient(120% 90% at 50% 40%,rgba(60,4,9,.94),rgba(6,3,3,.97));
  animation:kdIn .26s ease-out;font-family:"IBM Plex Mono",monospace}
.kdef.out{animation:kdOut .7s ease-in forwards}
@keyframes kdIn{from{opacity:0}to{opacity:1}}
@keyframes kdOut{to{opacity:0}}
.kdef .kd-in{position:relative;text-align:center;padding:36px 54px;max-width:min(92vw,760px);
  border:1px solid #D9A82B;background:rgba(24,4,7,.92);
  box-shadow:0 0 0 1px rgba(217,168,43,.22),0 0 70px rgba(142,21,32,.6);overflow:hidden}
.kdef .kd-ray{position:absolute;left:-40%;right:-40%;height:180%;top:-40%;
  background:conic-gradient(from 0deg,transparent 0deg,rgba(217,168,43,.14) 18deg,transparent 38deg,
    transparent 180deg,rgba(217,168,43,.10) 198deg,transparent 218deg);
  animation:kdRay 9s linear infinite}
@keyframes kdRay{to{transform:rotate(360deg)}}
.kdef .kd-tag{position:relative;font-size:10px;letter-spacing:.34em;color:#D9A82B;opacity:.85}
.kdef .kd-l1{position:relative;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:clamp(50px,11vw,118px);line-height:.94;letter-spacing:.03em;margin-top:8px;
  color:#F6D77A;text-shadow:0 0 30px rgba(217,168,43,.7),0 3px 0 rgba(142,21,32,.85);
  animation:kdGlow 2.8s ease-in-out infinite}
@keyframes kdGlow{0%,100%{text-shadow:0 0 26px rgba(217,168,43,.55),0 3px 0 rgba(142,21,32,.85)}
  50%{text-shadow:0 0 46px rgba(217,168,43,.95),0 3px 0 rgba(142,21,32,.85)}}
.kdef .kd-l2{position:relative;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:clamp(24px,5vw,50px);line-height:1.04;letter-spacing:.1em;margin-top:4px;
  color:#FFF3D6;text-shadow:0 0 24px rgba(142,21,32,.9)}
.kdef .kd-sub{position:relative;margin-top:14px;font-size:11.5px;letter-spacing:.2em;color:#E7B9BD;opacity:.9}
.kdef .kd-mgr{position:relative;margin-top:6px;font-size:10.5px;letter-spacing:.28em;color:#D9A82B;opacity:.55}
@media (prefers-reduced-motion:reduce){.kdef *{animation:none!important}}

/* Burke: ten seasons out of ten, and a scoring line that barely moves. Black and white,
   with bamboo. */
.pnda{position:fixed;inset:0;z-index:320;display:flex;align-items:center;justify-content:center;
  background:radial-gradient(120% 90% at 50% 40%,rgba(20,21,16,.96),rgba(4,5,4,.98));
  animation:pnIn .26s ease-out;font-family:"IBM Plex Mono",monospace}
.pnda.out{animation:pnOut .7s ease-in forwards}
@keyframes pnIn{from{opacity:0}to{opacity:1}}
@keyframes pnOut{to{opacity:0}}
.pnda .pn-in{position:relative;text-align:center;padding:32px 54px 34px;max-width:min(92vw,720px);
  border:1px solid #6FA33F;background:rgba(12,14,10,.94);
  box-shadow:0 0 0 1px rgba(244,241,230,.14),0 0 66px rgba(111,163,63,.3)}
.pnda .pn-face{position:relative;width:118px;height:104px;margin:2px auto 16px}
.pnda .pn-face .ear{position:absolute;width:46px;height:46px;border-radius:50%;background:#141510;
  border:3px solid #F4F1E6;top:0}
.pnda .pn-face .ear.l{left:0}.pnda .pn-face .ear.r{right:0}
.pnda .pn-face .head{position:absolute;left:9px;right:9px;top:14px;height:90px;border-radius:50%;
  background:#F4F1E6}
.pnda .pn-face .eye{position:absolute;width:30px;height:37px;border-radius:50%;background:#141510;top:24px}
.pnda .pn-face .eye.l{left:14px;transform:rotate(-15deg)}
.pnda .pn-face .eye.r{right:14px;transform:rotate(15deg)}
.pnda .pn-face .eye i{position:absolute;width:9px;height:9px;border-radius:50%;background:#F4F1E6;
  left:10px;top:11px;animation:pnBlink 4.4s steps(1) infinite}
@keyframes pnBlink{0%,95%{opacity:1}96%,99%{opacity:.15}100%{opacity:1}}
.pnda .pn-face .nose{position:absolute;left:50%;transform:translateX(-50%);top:58px;
  width:22px;height:15px;border-radius:50%;background:#141510}
.pnda .pn-tag{font-size:11px;letter-spacing:.32em;color:#B7DA8C}
.pnda .pn-l1{font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;font-weight:900;
  font-size:clamp(44px,9.5vw,100px);line-height:.95;letter-spacing:.03em;margin-top:8px;color:#F4F1E6;
  text-shadow:0 0 30px rgba(244,241,230,.28)}
.pnda .pn-l2{font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;font-weight:900;
  font-size:clamp(22px,4.6vw,46px);line-height:1.05;letter-spacing:.1em;margin-top:3px;color:#9FD063}
.pnda .pn-sub{margin-top:13px;font-size:12px;letter-spacing:.2em;color:#EAE6D6}
.pnda .pn-facts{margin-top:8px;font-size:11px;letter-spacing:.22em;color:#BFDD96}
@media (prefers-reduced-motion:reduce){.pnda *{animation:none!important}}

/* Kaiper: ten seasons of it, seven of them under the same prehistoric name. Amber,
   jungle dark, and something heavy walking towards you. */
.jrsc{position:fixed;inset:0;z-index:320;display:flex;align-items:center;justify-content:center;
  background:radial-gradient(120% 90% at 50% 45%,rgba(14,20,10,.95),rgba(3,5,3,.98));
  animation:jrIn .26s ease-out;font-family:"IBM Plex Mono",monospace}
.jrsc.out{animation:jrOut .7s ease-in forwards}
@keyframes jrIn{from{opacity:0}to{opacity:1}}
@keyframes jrOut{to{opacity:0}}
.jrsc .jr-in{position:relative;text-align:center;padding:34px 54px;max-width:min(92vw,760px);
  border:1px solid #E8A33D;background:rgba(16,12,5,.93);
  box-shadow:0 0 0 1px rgba(232,163,61,.2),0 0 70px rgba(196,64,43,.42);overflow:hidden}
.jrsc .jr-rip{position:absolute;left:50%;top:50%;width:44px;height:44px;margin:-22px 0 0 -22px;
  border:2px solid rgba(232,163,61,.5);border-radius:50%;animation:jrRip 3s ease-out infinite;pointer-events:none}
.jrsc .jr-rip:nth-of-type(2){animation-delay:1s}
.jrsc .jr-rip:nth-of-type(3){animation-delay:2s}
@keyframes jrRip{from{transform:scale(.3);opacity:.75}to{transform:scale(15);opacity:0}}
.jrsc .jr-tag{position:relative;font-size:11px;letter-spacing:.32em;color:#F0906A}
.jrsc .jr-l1{position:relative;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:clamp(40px,9vw,96px);line-height:.95;letter-spacing:.03em;margin-top:8px;
  color:#E8A33D;text-shadow:0 0 34px rgba(232,163,61,.6),0 3px 0 rgba(60,30,6,.9);
  animation:jrShake 3.4s ease-in-out infinite}
@keyframes jrShake{0%,86%,100%{transform:none}88%{transform:translate(2px,-1px)}
  90%{transform:translate(-2px,1px)}92%{transform:translate(1px,1px)}94%{transform:none}}
.jrsc .jr-l2{position:relative;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:clamp(21px,4.4vw,44px);line-height:1.05;letter-spacing:.1em;margin-top:3px;
  color:#F3E2C4}
.jrsc .jr-sub{position:relative;margin-top:13px;font-size:12px;letter-spacing:.2em;color:#F2DDBB}
.jrsc .jr-facts{position:relative;margin-top:8px;font-size:11px;letter-spacing:.22em;color:#EFAE86}
@media (prefers-reduced-motion:reduce){.jrsc *{animation:none!important}}

/* Wu: lacquer red and gold leaf, and a carver's seal. The seal carries the number of
   seasons he has played, in Chinese numerals, because that is a fact rather than a
   decoration. */
.nwu{position:fixed;inset:0;z-index:320;display:flex;align-items:center;justify-content:center;
  background:radial-gradient(120% 90% at 50% 40%,rgba(74,8,10,.95),rgba(12,3,3,.98));
  animation:wuIn .28s ease-out;font-family:"IBM Plex Mono",monospace}
.nwu.out{animation:wuOut .7s ease-in forwards}
@keyframes wuIn{from{opacity:0}to{opacity:1}}
@keyframes wuOut{to{opacity:0}}
.nwu .wu-in{position:relative;text-align:center;padding:34px 56px;max-width:min(92vw,740px);
  border:1px solid #E8C46A;background:rgba(28,5,6,.93);
  box-shadow:0 0 0 1px rgba(232,196,106,.24),0 0 74px rgba(176,26,32,.62);overflow:hidden}
.nwu .wu-in::before,.nwu .wu-in::after{content:"";position:absolute;width:26px;height:26px;
  border:2px solid #E8C46A;opacity:.55}
.nwu .wu-in::before{left:12px;top:12px;border-right:0;border-bottom:0}
.nwu .wu-in::after{right:12px;bottom:12px;border-left:0;border-top:0}
.nwu .wu-seal{position:relative;width:82px;height:82px;margin:0 auto 14px;border-radius:5px;
  background:#B01A20;border:3px solid #E8C46A;display:grid;place-items:center;
  transform:rotate(-4deg);box-shadow:0 0 34px rgba(176,26,32,.75)}
.nwu .wu-seal span{font-family:"Noto Serif SC","Songti SC","SimSun",serif;font-size:44px;
  line-height:1;color:#FFF3D6;font-weight:700}
.nwu .wu-tag{position:relative;font-size:11px;letter-spacing:.32em;color:#F0CE84}
.nwu .wu-l1{position:relative;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:clamp(44px,9.5vw,102px);line-height:.95;letter-spacing:.03em;margin-top:8px;
  color:#F7E3AE;text-shadow:0 0 32px rgba(232,196,106,.6),0 3px 0 rgba(96,10,12,.9)}
.nwu .wu-l2{position:relative;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:clamp(22px,4.6vw,46px);line-height:1.05;letter-spacing:.09em;margin-top:3px;
  color:#F26B62}
.nwu .wu-sub{position:relative;margin-top:13px;font-size:12px;letter-spacing:.2em;color:#F6E2C4}
.nwu .wu-facts{position:relative;margin-top:8px;font-size:11px;letter-spacing:.22em;color:#F0CE84}
@media (prefers-reduced-motion:reduce){.nwu *{animation:none!important}}

/* Gearing: scarlet and gold, and the yard lines you get to look along when your seat
   is one of the twenty at pitch level. */
.gr49{position:fixed;inset:0;z-index:320;display:flex;align-items:center;justify-content:center;
  background:radial-gradient(120% 90% at 50% 42%,rgba(126,4,4,.95),rgba(14,3,3,.98));
  animation:grIn .28s ease-out;font-family:"IBM Plex Mono",monospace}
.gr49.out{animation:grOut .7s ease-in forwards}
@keyframes grIn{from{opacity:0}to{opacity:1}}
@keyframes grOut{to{opacity:0}}
.gr49 .gr-in{position:relative;text-align:center;padding:34px 56px 30px;max-width:min(92vw,760px);
  border:1px solid #C9AE72;background:linear-gradient(180deg,rgba(122,6,6,.96),rgba(74,4,4,.97));
  box-shadow:0 0 0 1px rgba(201,174,114,.3),0 0 84px rgba(170,0,0,.75);overflow:hidden}
.gr49 .gr-turf{position:absolute;left:0;right:0;bottom:0;height:96px;pointer-events:none;
  background:repeating-linear-gradient(90deg,transparent 0 46px,rgba(255,255,255,.30) 46px 49px);
  mask-image:linear-gradient(180deg,transparent,#000);
  -webkit-mask-image:linear-gradient(180deg,transparent,#000)}
.gr49 .gr-tag{position:relative;font-size:13px;font-weight:600;letter-spacing:.24em;color:#FFEFC4;
  text-shadow:0 1px 3px rgba(40,0,0,.9)}
.gr49 .gr-l1{position:relative;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:clamp(42px,9vw,98px);line-height:.95;letter-spacing:.03em;margin-top:8px;
  color:#F4E7C4;text-shadow:0 0 30px rgba(179,153,93,.55),0 3px 0 rgba(120,0,0,.95)}
.gr49 .gr-l2{position:relative;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:clamp(20px,4.2vw,42px);line-height:1.06;letter-spacing:.08em;margin-top:3px;
  color:#F2D89C}
.gr49 .gr-sub{position:relative;margin-top:13px;font-size:12px;letter-spacing:.2em;color:#F3E3C6}
.gr49 .gr-facts{position:relative;margin-top:8px;font-size:11px;letter-spacing:.22em;color:#E8D3A0}
@media (prefers-reduced-motion:reduce){.gr49 *{animation:none!important}}

/* Niko: two titles running, the second with a worse team than the first. A marquee. */
.mrqe{position:fixed;inset:0;z-index:320;display:flex;align-items:center;justify-content:center;
  background:radial-gradient(120% 90% at 50% 40%,rgba(28,20,10,.95),rgba(6,5,4,.98));
  animation:mqIn .28s ease-out;font-family:"IBM Plex Mono",monospace}
.mrqe.out{animation:mqOut .7s ease-in forwards}
@keyframes mqIn{from{opacity:0}to{opacity:1}}
@keyframes mqOut{to{opacity:0}}
.mrqe .mq-in{position:relative;text-align:center;padding:40px 56px;max-width:min(92vw,760px);
  border:2px solid #F2C75C;background:linear-gradient(180deg,rgba(24,16,8,.96),rgba(46,10,12,.95));
  box-shadow:0 0 0 1px rgba(242,199,92,.22),0 0 80px rgba(242,199,92,.34)}
.mrqe .mq-bulbs{position:absolute;left:14px;right:14px;display:flex;justify-content:space-between}
.mrqe .mq-bulbs.t{top:11px}.mrqe .mq-bulbs.b{bottom:11px}
.mrqe .mq-bulbs i{width:8px;height:8px;border-radius:50%;background:#F2C75C;
  box-shadow:0 0 9px #F2C75C;animation:mqBulb 1.1s ease-in-out infinite}
.mrqe .mq-bulbs i:nth-child(3n+2){animation-delay:.37s}
.mrqe .mq-bulbs i:nth-child(3n+3){animation-delay:.73s}
@keyframes mqBulb{0%,100%{opacity:1}50%{opacity:.22}}
.mrqe .mq-tag{position:relative;font-size:15px;font-weight:600;letter-spacing:.26em;color:#FFDD8E;
  text-shadow:0 1px 3px rgba(30,10,0,.9)}
.mrqe .mq-l1{position:relative;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:clamp(42px,9vw,98px);line-height:.95;letter-spacing:.03em;margin-top:9px;
  color:#FFF4DA;text-shadow:0 0 34px rgba(242,199,92,.6),0 3px 0 rgba(110,18,22,.95)}
.mrqe .mq-l2{position:relative;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:clamp(21px,4.4vw,44px);line-height:1.06;letter-spacing:.09em;margin-top:3px;
  color:#F2C75C}
.mrqe .mq-dir{position:relative;font-family:Fraunces,Georgia,serif;font-style:italic;
  font-weight:600;font-size:clamp(15px,2.6vw,22px);line-height:1.2;margin-top:6px;color:#F7E7C6}
.mrqe .mq-rule{position:relative;height:1px;margin:16px auto 0;max-width:74%;
  background:linear-gradient(90deg,transparent,rgba(242,199,92,.5),transparent)}
.mrqe .mq-sub{position:relative;margin-top:13px;font-size:12px;letter-spacing:.18em;color:#F7E7C6}
.mrqe .mq-facts{position:relative;margin-top:8px;font-size:11px;letter-spacing:.22em;color:#E9BE72}
@media (prefers-reduced-motion:reduce){.mrqe *{animation:none!important}}

/* Wesley: the best win rate on record, and a rating that has fallen every single year.
   His own five seasons are drawn as the line they make. */
.tkr{position:fixed;inset:0;z-index:320;display:flex;align-items:center;justify-content:center;
  background:radial-gradient(120% 90% at 50% 40%,rgba(6,14,12,.96),rgba(2,4,4,.98));
  animation:tkIn .28s ease-out;font-family:"IBM Plex Mono",monospace}
.tkr.out{animation:tkOut .7s ease-in forwards}
@keyframes tkIn{from{opacity:0}to{opacity:1}}
@keyframes tkOut{to{opacity:0}}
.tkr .tk-in{position:relative;text-align:center;padding:32px 54px 30px;max-width:min(92vw,760px);
  border:1px solid #2E7D5B;background:rgba(4,10,9,.95);
  box-shadow:0 0 0 1px rgba(63,208,122,.16),0 0 70px rgba(228,69,60,.3)}
.tkr .tk-chart{position:relative;width:min(100%,420px);margin:2px auto 14px}
.tkr .tk-chart svg{display:block;width:100%;height:auto}
.tkr .tk-dot{animation:tkPulse 1.6s ease-in-out infinite}
@keyframes tkPulse{0%,100%{opacity:1}50%{opacity:.3}}
.tkr .tk-tag{position:relative;font-size:11px;letter-spacing:.32em;color:#E4453C}
.tkr .tk-l1{position:relative;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:clamp(40px,8.6vw,94px);line-height:.95;letter-spacing:.03em;margin-top:8px;
  color:#E9F5EC;text-shadow:0 0 30px rgba(63,208,122,.35)}
.tkr .tk-l2{position:relative;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:clamp(21px,4.4vw,44px);line-height:1.06;letter-spacing:.09em;margin-top:3px;
  color:#E4453C}
.tkr .tk-sub{position:relative;margin-top:13px;font-size:12px;letter-spacing:.18em;color:#CFE7D8}
.tkr .tk-facts{position:relative;margin-top:8px;font-size:11px;letter-spacing:.22em;color:#5FD497}
@media (prefers-reduced-motion:reduce){.tkr *{animation:none!important}}

/* McMahon: league lore says he is unguardable on a court. The record says the rim was
   never his problem. */
.hoop{position:fixed;inset:0;z-index:320;display:flex;align-items:center;justify-content:center;
  background:radial-gradient(120% 90% at 50% 42%,rgba(58,32,12,.96),rgba(8,5,3,.98));
  animation:hpIn .28s ease-out;font-family:"IBM Plex Mono",monospace}
.hoop.out{animation:hpOut .7s ease-in forwards}
@keyframes hpIn{from{opacity:0}to{opacity:1}}
@keyframes hpOut{to{opacity:0}}
.hoop .hp-in{position:relative;text-align:center;padding:30px 56px 34px;max-width:min(92vw,760px);
  border:1px solid #E07B2C;background:linear-gradient(180deg,rgba(46,26,10,.96),rgba(24,13,5,.97));
  box-shadow:0 0 0 1px rgba(224,123,44,.24),0 0 76px rgba(224,123,44,.34);overflow:hidden}
.hoop .hp-court{position:absolute;left:50%;bottom:-118px;transform:translateX(-50%);
  width:236px;height:236px;border:2px solid rgba(244,233,214,.28);border-radius:50%;pointer-events:none}
.hoop .hp-ball{position:relative;width:86px;height:86px;margin:0 auto 14px;border-radius:50%;
  background:radial-gradient(circle at 34% 30%,#F09A4E,#C9631E 68%);
  box-shadow:0 0 30px rgba(224,123,44,.5);animation:hpBounce 1.9s cubic-bezier(.5,0,.6,1) infinite}
@keyframes hpBounce{0%,100%{transform:translateY(0) scaleY(1)}
  42%{transform:translateY(-16px) scaleY(1.03)}52%{transform:translateY(0) scaleY(.93)}62%{transform:translateY(0) scaleY(1)}}
.hoop .hp-ball{overflow:hidden}
/* the two curved seams: an ellipse narrower than the ball, showing only its sides */
.hoop .hp-ball::before{content:"";position:absolute;top:-1px;bottom:-1px;left:50%;width:58%;
  margin-left:-29%;border-radius:50%;border:3px solid rgba(60,26,8,.72);border-top:0;border-bottom:0}
/* and the horizontal seam */
.hoop .hp-ball::after{content:"";position:absolute;left:0;right:0;top:50%;height:3px;
  margin-top:-1.5px;background:rgba(60,26,8,.72)}
.hoop .hp-seam{position:absolute;left:50%;top:0;bottom:0;width:3px;margin-left:-1.5px;
  background:rgba(60,26,8,.72)}
.hoop .hp-tag{position:relative;font-size:11px;letter-spacing:.32em;color:#F2B071}
.hoop .hp-l1{position:relative;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:clamp(40px,8.6vw,94px);line-height:.95;letter-spacing:.03em;margin-top:8px;
  color:#FBEEDA;text-shadow:0 0 30px rgba(224,123,44,.5),0 3px 0 rgba(70,32,8,.9)}
.hoop .hp-l2{position:relative;font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif;
  font-weight:900;font-size:clamp(21px,4.4vw,44px);line-height:1.06;letter-spacing:.09em;margin-top:3px;
  color:#F09A4E}
.hoop .hp-sub{position:relative;margin-top:13px;font-size:12px;letter-spacing:.18em;color:#F7E3C8}
.hoop .hp-facts{position:relative;margin-top:8px;font-size:11px;letter-spacing:.22em;color:#F2B071}
@media (prefers-reduced-motion:reduce){.hoop *{animation:none!important}}
.chaosov{position:fixed;inset:0;z-index:180;pointer-events:none;
  background:repeating-linear-gradient(0deg,rgba(255,255,255,.05) 0 1px,transparent 1px 3px);
  animation:chFlick .09s steps(1) infinite}
@keyframes chFlick{0%{opacity:.85;transform:translateY(0)}50%{opacity:.5;transform:translateY(1px)}100%{opacity:.85}}
.chaosov .ch-msg{position:absolute;left:0;right:0;top:44%;text-align:center;
  font-family:"IBM Plex Mono",monospace;font-size:clamp(15px,3vw,30px);letter-spacing:.34em;
  color:#fff;opacity:0;text-shadow:0 0 26px rgba(0,0,0,.9),3px 0 0 rgba(255,46,136,.6),-3px 0 0 rgba(86,199,245,.6)}
.chaosov.settle .ch-msg{animation:chMsg 1.5s ease forwards}
@keyframes chMsg{0%{opacity:0;letter-spacing:.7em}22%{opacity:1;letter-spacing:.34em}70%{opacity:1}100%{opacity:0}}
body.chaosing{animation:chShake .13s steps(2) infinite}
@keyframes chShake{0%{transform:none}50%{transform:translate3d(1px,-1px,0)}100%{transform:none}}
body.chaosing td.num,body.chaosing td.mono,body.chaosing .lad-s{color:var(--brass)!important}
@media (prefers-reduced-motion:reduce){.chaosov,body.chaosing{animation:none!important}}
#tTrMtx{width:auto}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:"IBM Plex Sans",system-ui,-apple-system,sans-serif;font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased;position:relative}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:linear-gradient(var(--grid-h) 1px,transparent 1px),linear-gradient(90deg,var(--grid-v) 1px,transparent 1px);
  background-size:44px 44px;
  -webkit-mask-image:radial-gradient(130% 90% at 50% 0%,#000 0%,transparent 72%);
  mask-image:radial-gradient(130% 90% at 50% 0%,#000 0%,transparent 72%)}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:var(--tex,none);background-size:var(--tex-size,auto);opacity:.9}
.wrap,nav,.mast{position:relative;z-index:1}
h1,h2,h3,h4{font-family:Fraunces,Georgia,serif;text-wrap:balance;margin:0;font-variation-settings:"SOFT" 0,"WONK" 0}
a{color:var(--brass)}
.wrap{max-width:var(--max);margin:0 auto;padding:0 22px}
.mono{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-variant-numeric:tabular-nums}
.num{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-variant-numeric:tabular-nums;text-align:right}
/* ---------- masthead: the scope ---------- */
.mast{position:relative;overflow:hidden;background:var(--mast-bg);border-bottom:1px solid var(--mast-rule)}
/* Installed on a phone the page gets the whole screen, status bar included, so the
   masthead has to hold its own space back or the clock and battery sit on the wordmark.
   Scoped to the installed app: in a browser there is no inset to reserve. */
@media (display-mode:standalone){
  .mast{padding-top:env(safe-area-inset-top,0px)}
  .totop{bottom:calc(18px + env(safe-area-inset-bottom,0px))}
}
.mast::before{content:"";position:absolute;inset:0;
  background-image:linear-gradient(var(--mast-grid) 1px,transparent 1px),linear-gradient(90deg,var(--mast-grid) 1px,transparent 1px);
  background-size:34px 34px;opacity:.5}
.mast::after{content:"";position:absolute;inset:0;
  background:radial-gradient(120% 130% at 22% 40%,transparent 20%,var(--mast-vig) 78%)}
.mast-in{position:relative;z-index:2;display:flex;flex-wrap:wrap;align-items:center;gap:16px 32px;
  padding:26px 22px 24px;max-width:var(--max);margin:0 auto}
.scope{flex:0 0 auto;width:126px;height:126px;filter:drop-shadow(0 0 11px var(--mast-glow))}
/* the reticle grid becomes a football field on Pigskin: yard lines, sidelines, hashes */
.scope .sw0{stop-opacity:0}
.scope .sw1{stop-opacity:calc(var(--rt-sweep,.62) * .42)}
.scope .sw2{stop-opacity:var(--rt-sweep,.62)}
.scope .rt-grid-field{display:none}
[data-skin="leather"] .scope .rt-grid-plain{display:none}
[data-skin="leather"] .scope .rt-grid-field{display:block}
.scope .sweep{animation:scopeSpin 5.5s linear infinite;transform-origin:60px 60px}
@keyframes scopeSpin{to{transform:rotate(360deg)}}
/* the contact only exists on the redacted file: the sweep passes it once per rotation
   and it answers. Hidden everywhere else so the other five skins are untouched. */
.scope .blip{opacity:0}
[data-skin="redact"] .scope .blip{animation:blipPing 5.5s linear infinite}
[data-skin="redact"] .scope .blip-ring{animation:blipRing 5.5s linear infinite;transform-origin:84px 41px}
/* the wedge is bright at its LEADING edge, which sits at rot+42 and crosses the blip
   at rot 9.6deg = 2.7% of the cycle. Ping there, sharply, then fade out. */
@keyframes blipPing{0%,2.4%{opacity:0}3.4%{opacity:1}9%{opacity:.5}17%,100%{opacity:0}}
@keyframes blipRing{0%,2.4%{transform:scale(1);opacity:0}3.4%{transform:scale(1);opacity:.9}
  19%,100%{transform:scale(3.6);opacity:0}}
[data-skin="redact"] .scope{filter:drop-shadow(0 0 13px var(--mast-glow)) drop-shadow(0 0 2px rgba(200,162,74,.35))}
@media (prefers-reduced-motion:reduce){.scope .sweep{animation:none}
  [data-skin="redact"] .scope .blip,[data-skin="redact"] .scope .blip-ring{animation:none}
  [data-skin="redact"] .scope .blip{opacity:.9}}
.brand{display:flex;flex-direction:column;gap:1px;min-width:0;position:relative;z-index:2}
.kicker{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.34em;text-transform:uppercase;
  color:var(--mast-kick);opacity:.9}
.mast h1{font-family:var(--wordmark);font-weight:900;
  font-size:clamp(48px,9vw,92px);line-height:.86;letter-spacing:.055em;color:var(--mast-ink);margin:2px 0 0;
  text-shadow:0 0 20px var(--mast-glow),0 0 52px var(--mast-glow2)}
.mast .sub{font-family:Fraunces,Georgia,serif;font-style:italic;font-size:clamp(15px,2vw,20px);
  color:var(--mast-sub);margin-top:5px;font-variation-settings:"opsz" 40}
.facts{display:flex;gap:22px;flex-wrap:wrap;margin-left:auto;position:relative;z-index:2}
.fact{display:flex;flex-direction:column;padding-left:11px;border-left:1px solid var(--mast-rule)}
.fact b{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:21px;line-height:1.15;color:var(--mast-kick);
  font-variant-numeric:tabular-nums}
.fact span{font-size:9.5px;text-transform:uppercase;letter-spacing:.13em;color:var(--mast-sub);opacity:.8;font-family:"IBM Plex Mono",monospace}
@media(max-width:640px){.scope{width:64px;height:64px}
  .mast-in{padding:15px 16px 14px;gap:10px 18px}
  .mast h1{font-size:clamp(34px,10.5vw,92px);letter-spacing:.04em}
  .kicker{font-size:9px;letter-spacing:.26em}
  .facts{gap:10px 14px;margin-top:2px}
  .fact{padding-left:9px}
  .fact b{font-size:15px}.fact span{font-size:8.5px;letter-spacing:.1em}
  .mast .sub-wm{font-size:19px}}
.navmark{flex:0 0 auto;display:flex;align-items:center;padding:0 10px 0 4px;position:sticky;left:0;z-index:5;background:linear-gradient(var(--nav-bg),var(--nav-bg)),linear-gradient(var(--nav-bg),var(--nav-bg));box-shadow:-16px 0 0 var(--nav-bg),-16px 0 0 var(--nav-bg)}
.navmark svg{width:18px;height:18px;opacity:.9}
nav{position:sticky;top:0;z-index:40;background:var(--nav-bg);backdrop-filter:blur(8px);border-bottom:1px solid var(--rule)}
.nav-row{position:relative;max-width:var(--max);margin:0 auto}
.nav-in{display:flex;gap:2px;overflow-x:auto;padding:0 14px;
  scrollbar-width:none;-ms-overflow-style:none;scroll-behavior:smooth}
.nav-in::-webkit-scrollbar{display:none}
.nav-row::before,.nav-row::after{content:"";position:absolute;top:0;bottom:0;width:46px;pointer-events:none;
  z-index:3;opacity:0;transition:opacity .22s}
.nav-row::before{left:46px;background:linear-gradient(90deg,var(--nav-bg) 12%,transparent)}
.nav-row::after{right:0;background:linear-gradient(270deg,var(--nav-bg) 12%,transparent)}
.nav-row.sL::before{opacity:1}.nav-row.sR::after{opacity:1}
.nav-ar{position:absolute;top:50%;transform:translateY(-50%);z-index:4;width:26px;height:26px;
  display:none;align-items:center;justify-content:center;border-radius:50%;cursor:pointer;
  background:var(--surface);border:1px solid var(--rule);color:var(--ink-2);font-size:12px;line-height:1;padding:0}
.nav-row.sL .nav-ar.l{display:flex}.nav-row.sR .nav-ar.r{display:flex}
.nav-ar.l{left:50px}.nav-ar.r{right:2px}
.nav-ar:hover{color:var(--brass);border-color:var(--brass-2)}
@media(max-width:760px){.nav-ar{display:none!important}}
nav a{flex:0 0 auto;padding:11px 13px;font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-2);text-decoration:none;white-space:nowrap;border-bottom:2px solid transparent;font-family:"IBM Plex Mono",monospace}
nav a:hover{color:var(--ink)}
nav a.on{color:var(--brass);border-bottom-color:var(--brass)}
nav a:focus-visible,button:focus-visible,select:focus-visible,input:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--brass);outline-offset:2px}
section{padding:52px 0 6px;scroll-margin-top:96px}
.fb{border-top:1px solid var(--rule-2);background:var(--surface)}
.fb-in{display:flex;gap:7px;align-items:center;max-width:var(--max);margin:0 auto;padding:7px 22px;flex-wrap:wrap}
.skip{position:absolute;left:-9999px;top:0;z-index:500;padding:12px 18px;
  background:var(--brass);color:var(--surface);font-family:"IBM Plex Mono",monospace;
  font-size:13px;font-weight:600;text-decoration:none;border-radius:0 0 4px 0}
.skip:focus{left:0}
@media(pointer:coarse){
  /* WCAG asks for roughly 44px of touch target. These controls were 25-27px, which is
     a lot of mis-taps on a phone. Grow the hit area, not the visual weight. */
  nav a{padding-top:15px;padding-bottom:15px}
  .fb-in button,.fb-in select,.pills button,.card-h button,.card-h .right button{
    min-height:40px;padding-top:9px;padding-bottom:9px}
  .chip{min-height:38px;display:inline-flex;align-items:center}
  .fb-sum{min-height:46px}
  #recsToggle,#toTop,.wrapBtn{min-height:44px}
}
.fb-sum{display:none}
@media(max-width:760px){
  .fb-sum{display:flex;width:100%;align-items:center;gap:8px;padding:9px 16px;
    background:none;border:0;border-radius:0;cursor:pointer;text-align:left;
    font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.09em;
    text-transform:uppercase;color:var(--ink-2)}
  .fb-sum b{color:var(--brass);font-weight:600}
  .fb-sum .ar{margin-left:auto;transition:transform .18s}
  .fb.open .fb-sum .ar{transform:rotate(180deg)}
  .fb .fb-in{display:none}
  .fb.open .fb-in{display:flex;padding-top:0;padding-bottom:10px}
}
.fb-lab{font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:var(--ink-3);font-family:"IBM Plex Mono",monospace;font-weight:600}
.fb-count{font-size:11px;color:var(--ink-3);font-family:"IBM Plex Mono",monospace;margin-left:auto}
.fb-in [data-skin-btn]{padding:4px 9px}
#wkYears{position:sticky;top:86px;z-index:30;background:var(--ground);margin:0 -8px 20px;padding:9px 8px;
  border-bottom:1px solid var(--rule);box-shadow:0 6px 14px -12px rgba(0,0,0,.6)}
#wkYears .now{margin-left:auto;font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--brass);
  letter-spacing:.09em;text-transform:uppercase;font-weight:600}
.fb-chips[hidden]{display:none}
.fb-chips{max-width:var(--max);margin:0 auto;padding:2px 22px 11px;display:flex;flex-wrap:wrap;gap:5px}
.fb-chips button{padding:3px 9px;font-size:11px;opacity:.45}
.fb-chips button.on{opacity:1}
.fb-chips button::before{content:"\2715";margin-right:5px;font-size:8px;opacity:.6}
.fb-chips button.on::before{content:"\2713"}
tr.off{opacity:.3}
.side.off,.game.off{opacity:.32}
.sec-head{display:flex;align-items:baseline;gap:14px;border-bottom:1px var(--rule-style) var(--brass-2);padding-bottom:9px;margin-bottom:6px;position:relative}
.sec-head::after{content:"";position:absolute;left:0;bottom:-1px;width:74px;height:2px;background:var(--brass);box-shadow:0 0 10px var(--mast-glow2)}
.sec-head h2{font-size:clamp(22px,3vw,30px);font-weight:700;letter-spacing:-.012em;font-variation-settings:"opsz" 72;color:var(--head-ink)}
.sec-head .rule-note{margin-left:auto;font-size:10.5px;font-family:"IBM Plex Mono",monospace;text-transform:uppercase;letter-spacing:.09em;color:var(--ink-3);text-align:right}
.lede{color:var(--ink-2);max-width:70ch;margin:14px 0 22px;font-size:14.5px}
.lede strong{color:var(--ink);font-weight:600}
.card{background:var(--surface);border:1px solid var(--rule);border-radius:var(--card-r);box-shadow:var(--shadow);overflow:hidden;color:var(--ink)}
.card+.card{margin-top:20px}
.card-h{display:flex;align-items:baseline;gap:12px;padding:13px 16px;border-bottom:1px solid var(--rule);background:var(--surface-2);flex-wrap:wrap}
.card-h h3{font-size:15px;font-weight:700;font-variation-settings:"opsz" 20}
/* trade cards are titled "TeamA <-> TeamB". A long team name with no spaces in it
   cannot wrap, and pushed the heading straight out of the card on a phone. Let it
   break mid-word rather than overflow; min-width:0 so the flex child may shrink. */
#trades .card-h{min-width:0}
#trades .card-h h3{overflow-wrap:anywhere;min-width:0}
#trades .sub-h{overflow-wrap:anywhere;min-width:0}
.card-h .sub{font-size:11.5px;color:var(--ink-3);font-family:"IBM Plex Mono",monospace}
.card-h .right{margin-left:auto;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.card-b{padding:16px}
.scroll{overflow-x:auto}
.board{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,196px),1fr));gap:1px;background:var(--rule);border:1px solid var(--rule);border-radius:3px;overflow:hidden}
.plate{background:var(--surface);color:var(--ink);padding:15px 16px 14px;display:flex;flex-direction:column;gap:3px;cursor:pointer;transition:background .12s;border:0;text-align:left;font-family:inherit;font-size:inherit;color:inherit}
.plate:hover{background:var(--surface-2)}
.plate{position:relative}
.plate .cup{position:absolute;right:13px;top:12px;width:30px;height:34px;color:var(--brass);opacity:.5;transition:opacity .15s,transform .15s}
.plate:hover .cup{opacity:1;transform:translateY(-2px) scale(1.06)}
.plate.split .cup{opacity:.38}
.plate .yr{font-family:Fraunces,serif;font-weight:900;font-size:31px;line-height:1;letter-spacing:-.02em;color:var(--brass);font-variation-settings:"opsz" 60;text-shadow:0 0 14px var(--mast-glow2)}
.plate .mgr{font-weight:700;font-size:14.5px;margin-top:5px}
.plate .tm{font-size:12.5px;color:var(--ink-2);font-style:italic}
.plate .meta{margin-top:8px;padding-top:8px;border-top:1px solid var(--rule-2);font-size:10.5px;font-family:"IBM Plex Mono",monospace;color:var(--ink-3);letter-spacing:.03em;text-transform:uppercase}
table{border-collapse:collapse;width:100%;font-size:13.5px;color:var(--ink)}
td{color:var(--ink)}
th,td{padding:7px 9px;text-align:left;border-bottom:1px solid var(--rule-2);white-space:nowrap}
thead th{position:sticky;top:0;background:var(--surface-2);font-size:10.5px;text-transform:uppercase;letter-spacing:.075em;color:var(--ink-2);font-weight:600;font-family:"IBM Plex Mono",monospace;border-bottom:1px solid var(--rule);z-index:2}
th.s{cursor:pointer;user-select:none}
th.s:hover{color:var(--ink)}
th.s::after{content:"\2195";opacity:.28;margin-left:4px;font-size:9px}
th.s.asc::after{content:"\2191";opacity:1;color:var(--brass)}
th.s.desc::after{content:"\2193";opacity:1;color:var(--brass)}
tbody tr:hover{background:var(--hover)}
td.nm{font-weight:600}
td.tm{color:var(--ink-2);font-style:italic}
.rk{color:var(--ink-3);font-family:"IBM Plex Mono",monospace;font-size:11.5px;width:26px;text-align:right}
/* records: the team column absorbs the slack and ellipsizes, so the value never scrolls out of reach */
#recs .scroll table{width:100%}
#recs td.nm,#recs td.tm,#recs td.dim{white-space:normal;overflow-wrap:break-word}
#recs td.num{white-space:normal}
/* narrow phones: tighten the cells first, and only then allow a word to break, so the
   value column is never pushed out of reach on a 320px screen */
@media(max-width:430px){#recs th,#recs td{padding:6px 5px}}
@media(max-width:345px){#recs td.nm,#recs td.tm,#recs td.dim{overflow-wrap:anywhere}}
tr.champ td.nm .mlink::before{content:"\25C6";color:var(--brass);margin-right:6px;font-size:9px;vertical-align:2px}
.dim{color:var(--ink-3)}
.mlink{cursor:pointer;border-bottom:1px dotted var(--brass-2)}
.mlink:hover{color:var(--brass)}
.dimrow{opacity:.14}
.pickrow{box-shadow:inset 3px 0 0 var(--brass)}
#tHeat tbody tr{transition:opacity .1s}
.dbar{position:relative;height:15px;width:120px;display:block}
.dbar i{position:absolute;top:2px;height:11px;border-radius:0 2px 2px 0;display:block}
.dbar i.l{border-radius:2px 0 0 2px}
.dbar u{position:absolute;left:50%;top:0;bottom:0;width:1px;background:var(--rule);display:block}
.chip{display:inline-block;padding:1px 7px;border-radius:2px;font-size:11px;font-family:"IBM Plex Mono",monospace;font-weight:500;border:1px solid var(--rule)}
.chip.y{background:var(--brass-wash);border-color:var(--brass-2);color:var(--brass)}
table.heat td.h{text-align:center;font-family:"IBM Plex Mono",monospace;font-size:11.5px;padding:0;width:52px;border:1px solid var(--surface)}
table.heat td.h span{display:block;padding:7px 0;border-radius:2px;cursor:pointer}
table.heat td.h.e span{color:var(--ink-2);opacity:.85;cursor:default}
button,select,input{font-family:"IBM Plex Mono",monospace;font-size:11.5px;letter-spacing:.04em;color:var(--ink);background:var(--surface);border:1px solid var(--rule);border-radius:2px;padding:5px 10px;cursor:pointer}
input{cursor:text}
button:hover,select:hover{border-color:var(--brass-2)}
button.on{background:var(--brass-wash);border-color:var(--brass-2);color:var(--brass);font-weight:600}
.pills{display:flex;gap:5px;flex-wrap:wrap;align-items:center}
.pills button{padding:5px 11px;font-weight:600}
input[type=range]{-webkit-appearance:none;appearance:none;background:transparent;padding:0;border:0;width:180px;cursor:pointer}
input[type=range]::-webkit-slider-runnable-track{height:4px;background:var(--rule);border-radius:2px}
input[type=range]::-moz-range-track{height:4px;background:var(--rule);border-radius:2px}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:15px;height:15px;border-radius:50%;background:var(--brass);margin-top:-5.5px;border:0}
input[type=range]::-moz-range-thumb{width:15px;height:15px;border-radius:50%;background:var(--brass);border:0}
footer{border-top:1px solid var(--rule);margin-top:60px;padding:26px 0 46px;color:var(--ink-3);font-size:12px}
.tip{position:fixed;pointer-events:none;z-index:120;background:var(--surface);color:var(--ink);border:1px solid var(--brass-2);padding:7px 10px;border-radius:3px;font-size:12px;line-height:1.45;box-shadow:0 6px 20px rgba(0,0,0,.28);opacity:0;transition:opacity .1s;max-width:290px}
.tip b{color:var(--brass)}
.tip.on{opacity:1}
.chart{position:relative}
.chart svg{display:block;width:100%;height:auto;overflow:visible}
/* bracket */
.brk{position:relative;overflow-x:auto;padding:4px 2px 8px}
.brk-in{position:relative;display:flex;gap:44px;min-width:min-content}
.brk svg.conn{position:absolute;inset:0;pointer-events:none;overflow:visible;width:100%;height:100%}
.round{flex:0 0 224px;display:flex;flex-direction:column;justify-content:space-around;gap:14px;position:relative;z-index:1}
.round h4{font-size:10.5px;text-transform:uppercase;letter-spacing:.1em;color:var(--ink-3);font-family:"IBM Plex Mono",monospace;margin:0 0 2px;font-weight:600;text-align:center}
.game{border:1px solid var(--rule);border-radius:var(--card-r);overflow:hidden;background:var(--surface);color:var(--ink);transition:box-shadow .12s,border-color .12s}
.game.hi{border-color:var(--brass);box-shadow:0 0 0 2px var(--brass-wash)}
.game .gh{font-size:9.5px;text-transform:uppercase;letter-spacing:.09em;padding:4px 9px;background:var(--surface-2);color:var(--ink-2);font-family:"IBM Plex Mono",monospace;border-bottom:1px solid var(--rule-2)}
.side{display:flex;align-items:center;gap:8px;padding:7px 9px;font-size:12.5px;cursor:default}
.side+.side{border-top:1px solid var(--rule-2)}
.side .sd{width:15px;font-family:"IBM Plex Mono",monospace;font-size:10px;color:var(--ink-3);text-align:right;flex:0 0 15px}
.side .tn{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.side .tn small{display:block;font-size:10.5px;color:var(--ink-3);font-weight:400}
.side .sc{font-family:"IBM Plex Mono",monospace;font-variant-numeric:tabular-nums;font-size:13px}
.side.w{font-weight:700}
.side.w .sc{color:var(--brass)}
.side.lo{color:var(--ink-3)}
.side.lo .tn{text-decoration:line-through;text-decoration-thickness:1px}
.side.bye{color:var(--ink-3);font-style:italic}
.side.act{background:var(--brass-wash)}
.rt-glow{filter:drop-shadow(0 0 6px var(--mast-glow2))}
.game.void{border-color:var(--neg)}
.game.void .gh{background:var(--neg);color:#fff}
.wk{border-top:1px solid var(--rule-2);padding:10px 0}
.wk:first-child{border-top:0;padding-top:0}
.wk summary{cursor:pointer;font-weight:700;font-size:13.5px;list-style:none;padding:3px 0}
.wk summary::-webkit-details-marker{display:none}
.wk summary::before{content:"\25B8";display:inline-block;margin-right:7px;color:var(--brass);transition:transform .12s}
.wk[open] summary::before{transform:rotate(90deg)}
.wkgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:10px;padding:10px 0 4px}
:root[data-skin="arcade"] .mast h1{font-size:clamp(22px,3.6vw,44px);letter-spacing:.02em;line-height:1.12}
:root[data-skin="arcade"] .fact b,:root[data-skin="arcade"] nav a{letter-spacing:.02em}
:root[data-skin="leather"] .sec-head::after{background:repeating-linear-gradient(90deg,var(--brass) 0 7px,transparent 7px 13px);box-shadow:none}
:root[data-skin="leather"] .mast::before{background-image:
  repeating-linear-gradient(90deg,transparent 0 46px,rgba(255,255,255,.13) 46px 50px);
  background-size:auto;opacity:1}
.brk-champ{align-self:center;text-align:center;padding:14px 12px;border:1px solid var(--brass-2);background:var(--brass-wash);border-radius:3px;box-shadow:0 0 22px var(--mast-glow2)}
.brk-champ .t{font-family:Fraunces,serif;font-weight:900;font-size:19px;color:var(--brass);line-height:1.15;text-shadow:0 0 12px var(--mast-glow2)}
.brk-champ .s{font-size:10.5px;text-transform:uppercase;letter-spacing:.1em;font-family:"IBM Plex Mono",monospace;color:var(--brass-2);margin-bottom:4px}
table.mtx th.v{writing-mode:vertical-rl;transform:rotate(180deg);font-size:10px;padding:8px 3px;text-align:left;height:118px;white-space:nowrap;position:static}
table.mtx td{text-align:center;font-family:"IBM Plex Mono",monospace;font-size:11px;padding:0;border:1px solid var(--surface);width:42px}
table.mtx td span{display:block;padding:6px 0;border-radius:2px}
table.mtx td.self span{background:var(--rule-2);color:var(--ink-2)}
table.mtx th.rw{font-size:12px;text-align:left;font-family:"IBM Plex Sans",sans-serif;font-weight:600;
  position:sticky;left:0;z-index:4;background:var(--surface);text-transform:none;letter-spacing:0;
  box-shadow:1px 0 0 var(--rule)}
table.mtx thead th.rw{z-index:6;background:var(--surface-2)}
.method{border-top:1px solid var(--rule)}
.mrow{display:grid;grid-template-columns:170px 1fr 1fr;border-bottom:1px solid var(--rule-2)}
.mrow>div{padding:12px 14px}
.mrow .k{font-weight:700;font-size:13.5px;border-right:1px solid var(--rule-2)}
.mrow .d{color:var(--ink-2);font-size:13px;border-right:1px solid var(--rule-2)}
.mrow .r{color:var(--ink-2);font-size:13px}
.mrow .k{color:var(--ink)}
.mrow code{font-family:"IBM Plex Mono",monospace;font-size:12px;background:var(--surface-2);padding:1px 4px;border-radius:2px;color:var(--ink)}
.mgroup{background:var(--surface-2);padding:9px 14px;font-family:"IBM Plex Mono",monospace;font-size:10.5px;text-transform:uppercase;letter-spacing:.11em;color:var(--brass);font-weight:600;border-bottom:1px solid var(--rule-2)}
@media(max-width:760px){.mrow{grid-template-columns:1fr}.mrow .k,.mrow .d{border-right:none;border-bottom:1px solid var(--rule-2)}}
/* modal */
.ov{position:fixed;inset:0;background:var(--ov);backdrop-filter:blur(3px);z-index:100;display:none;padding:26px 16px;overflow-y:auto}
.ov.on{display:block}
.modal{max-width:940px;margin:0 auto;background:var(--surface);color:var(--ink);border:1px solid var(--rule);border-radius:4px;box-shadow:0 24px 70px rgba(0,0,0,.4)}
.modal-h{display:flex;align-items:flex-start;gap:16px;padding:20px 22px;border-bottom:1px solid var(--rule);background:var(--surface-2);position:sticky;top:0;z-index:3;border-radius:4px 4px 0 0}
.modal-h h3{font-size:27px;font-weight:900;letter-spacing:-.015em;font-variation-settings:"opsz" 72}
.modal-h .sub{font-size:11.5px;font-family:"IBM Plex Mono",monospace;color:var(--ink-3);text-transform:uppercase;letter-spacing:.08em;margin-top:3px}
.xbtn{margin-left:auto;font-size:16px;line-height:1;padding:6px 11px}
.modal-b{padding:20px 22px 26px;overflow-x:hidden}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,108px),1fr));gap:1px;background:var(--rule);border:1px solid var(--rule);border-radius:3px;overflow:hidden;margin-bottom:20px}
.tile{background:var(--surface);color:var(--ink);padding:11px 13px}
.tile b{display:block;font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-weight:600;font-size:19.5px;line-height:1.2;letter-spacing:-.02em;font-variant-numeric:tabular-nums;white-space:nowrap}
.tile span{font-size:9.5px;text-transform:uppercase;letter-spacing:.09em;color:var(--ink-3);font-family:"IBM Plex Mono",monospace}
.sub-h{font-size:10.5px;text-transform:uppercase;letter-spacing:.11em;color:var(--brass);font-family:"IBM Plex Mono",monospace;font-weight:600;margin:22px 0 9px}
.sub-h:first-child{margin-top:0}

/* ============ Wrapped: story mode ============ */
.wrap-ov{position:fixed;inset:0;z-index:140;display:none;background:#08080a}
.wrap-ov.on{display:flex;align-items:center;justify-content:center}
.wr-stage{position:relative;width:min(452px,calc(100vw - 20px));height:min(812px,calc(100dvh - 20px));
  border-radius:16px;overflow:hidden;box-shadow:0 30px 90px rgba(0,0,0,.62);display:flex;flex-direction:column;
  background:#161622;transition:background .55s ease}
.wr-stage::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(120% 70% at 50% 105%,rgba(0,0,0,.5),transparent 62%);mix-blend-mode:multiply}
.wr-blob{position:absolute;border-radius:50%;filter:blur(46px);opacity:.5;pointer-events:none}
.wr-blob.a{width:64%;aspect-ratio:1;left:-16%;top:6%;background:rgba(255,255,255,.28);animation:wrFloatA 15s ease-in-out infinite}
.wr-blob.b{width:52%;aspect-ratio:1;right:-14%;bottom:10%;background:rgba(255,255,255,.2);animation:wrFloatB 19s ease-in-out infinite}
@keyframes wrFloatA{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(14%,10%) scale(1.14)}}
@keyframes wrFloatB{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(-12%,-9%) scale(1.1)}}
.wr-bars{display:flex;gap:4px;padding:13px 13px 0;position:relative;z-index:5}
.wr-bar{flex:1;height:3px;background:rgba(255,255,255,.26);border-radius:3px;overflow:hidden}
.wr-bar i{display:block;height:100%;width:0;background:#fff;border-radius:3px}
.wr-bar.done i{width:100%}
.wr-top{display:flex;align-items:center;gap:9px;padding:11px 15px 0;position:relative;z-index:5;color:rgba(255,255,255,.82)}
.wr-top .wrb{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.16em;text-transform:uppercase;flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wr-top .wrb b{color:#fff}
.wr-x{margin-left:auto;background:rgba(0,0,0,.26);border:1px solid rgba(255,255,255,.28);color:#fff;
  width:28px;height:28px;border-radius:50%;font-size:13px;line-height:1;cursor:pointer;display:grid;place-items:center;padding:0}
.wr-x:hover{background:rgba(0,0,0,.45)}
.wr-card{flex:1;display:flex;flex-direction:column;justify-content:center;padding:6px 26px 78px;
  position:relative;z-index:6;pointer-events:none;color:#fff;text-shadow:0 2px 18px rgba(0,0,0,.32)}
.wr-k{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;
  color:rgba(255,255,255,.7);animation:wrIn .5s cubic-bezier(.2,.85,.25,1) both}
.wr-v{font-family:Fraunces,serif;font-weight:900;font-variation-settings:"opsz" 96;letter-spacing:-.025em;
  line-height:.92;font-size:clamp(40px,12.5vw,80px);margin:15px 0 17px;word-break:break-word;
  animation:wrPop .62s cubic-bezier(.16,1,.3,1) both;animation-delay:.09s}
.wr-v.sm{font-size:clamp(28px,7.6vw,46px);line-height:1.04}
.wr-n{font-size:15.5px;line-height:1.58;color:rgba(255,255,255,.9);max-width:33ch;
  animation:wrIn .55s cubic-bezier(.2,.85,.25,1) both;animation-delay:.2s}
.wr-n b{color:#fff}
.wr-n .neg{color:#ffc0c0}
.wr-sup{margin-top:20px;display:flex;flex-wrap:wrap;gap:7px;animation:wrIn .55s ease both;animation-delay:.3s}
.wr-pill{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;
  background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.24);border-radius:99px;padding:5px 11px;color:#fff}
@keyframes wrIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes wrPop{from{opacity:0;transform:translateY(24px) scale(.94)}to{opacity:1;transform:none}}
.wr-foot{position:absolute;left:0;right:0;bottom:0;z-index:6;padding:14px 20px 18px;
  display:flex;align-items:center;gap:10px;color:rgba(255,255,255,.72);
  font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.14em;text-transform:uppercase}
.wr-foot .hint{margin-left:auto;opacity:.72}
.wr-nav{position:absolute;top:52px;bottom:0;width:34%;z-index:5;background:transparent;border:0;cursor:default;padding:0}
.wr-nav.l{left:0}.wr-nav.r{right:0;width:66%}
.wr-nav:focus-visible{outline:2px solid #fff;outline-offset:-4px}
.wr-btns{margin-top:26px;display:flex;flex-wrap:wrap;gap:9px;position:relative;z-index:7;
  pointer-events:auto;animation:wrIn .55s ease both;animation-delay:.34s}
.wr-btns button{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;
  background:#fff;color:#111;border:0;border-radius:99px;padding:11px 18px;cursor:pointer;font-weight:600}
.wr-btns button.ghost{background:rgba(255,255,255,.13);color:#fff;border:1px solid rgba(255,255,255,.4)}
.wr-btns button:hover{transform:translateY(-1px)}
.wr-paused{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);z-index:8;
  font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.24em;text-transform:uppercase;color:#fff;
  background:rgba(0,0,0,.42);border:1px solid rgba(255,255,255,.3);border-radius:99px;padding:7px 15px;display:none}
.wrap-ov.hold .wr-paused{display:block}
@media(max-height:620px){.wr-card{padding-bottom:66px}.wr-v{font-size:clamp(34px,9vw,54px);margin:10px 0 12px}.wr-n{font-size:14px}}
/* back to top */
.totop{position:fixed;right:18px;bottom:18px;z-index:90;display:flex;align-items:center;gap:8px;
  font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.13em;text-transform:uppercase;font-weight:600;
  background:var(--brass);color:var(--surface);border:1px solid var(--brass);border-radius:99px;
  padding:11px 17px;cursor:pointer;box-shadow:0 8px 26px rgba(0,0,0,.28);
  opacity:0;transform:translateY(14px);pointer-events:none;transition:opacity .25s ease,transform .25s ease}
.totop.vis{opacity:1;transform:none;pointer-events:auto}
.totop:hover{filter:brightness(1.08)}
.totop .ar{font-size:14px;line-height:1}
@media(max-width:560px){.totop{right:12px;bottom:12px;padding:10px 14px;font-size:10px}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
"""

BODY = r"""
<script>(function(){try{var k=localStorage.getItem("deadshot.skin");var ok=["scope","og","red","leather","arcade"];if(k==="redact"&&localStorage.getItem("deadshot.clearance")==="1")ok.push("redact");document.documentElement.setAttribute("data-skin",ok.indexOf(k)>-1?k:"red");}catch(e){document.documentElement.setAttribute("data-skin","red");}})();</script>
<div class="deco field" aria-hidden="true">
  <div class="stars s1"></div><div class="stars s2"></div><div class="stars s3"></div>
  <svg class="sky" viewBox="0 0 1600 900" preserveAspectRatio="none">
    <g class="lane1">
      <g class="fs run"><g transform="scale(1.35)">
        <path d="M0 7 L0 17 L22 17 L38 12 L22 7 Z"/><rect x="6" y="1" width="9" height="22"/>
        <rect x="-8" y="10" width="8" height="4" opacity=".8"/></g></g>
      <g class="fs hot hunt"><g transform="scale(1.6)">
        <path d="M0 7 L0 17 L22 17 L38 12 L22 7 Z"/><rect x="6" y="1" width="9" height="22"/>
        <rect x="-11" y="9" width="11" height="6" opacity=".85"/></g></g>
      <g class="fb t1"><rect width="30" height="4"/></g>
      <g class="fb t2"><rect width="24" height="4"/></g>
      <g class="fb pop"><circle r="13"/></g>
    </g>
    <g class="lane2"><g class="fs hot run"><g transform="scale(1.2)">
      <path d="M0 7 L0 17 L22 17 L38 12 L22 7 Z"/><rect x="6" y="1" width="9" height="22"/></g></g></g>
    <g class="inv sq1"><rect x="6" y="0" width="18" height="6"/><rect x="0" y="6" width="30" height="6"/>
      <rect x="0" y="12" width="6" height="6"/><rect x="12" y="12" width="6" height="6"/><rect x="24" y="12" width="6" height="6"/></g>
    <g class="inv sq2"><rect x="6" y="0" width="18" height="6"/><rect x="0" y="6" width="30" height="6"/>
      <rect x="6" y="12" width="6" height="6"/><rect x="18" y="12" width="6" height="6"/></g>
  </svg>
</div>
<div class="deco gridiron" aria-hidden="true"><div class="yard"></div><div class="yard5"></div><div class="hash h1"></div><div class="hash h2"></div><div class="goal"><svg viewBox="0 0 130 150" aria-hidden="true"><g stroke="#FFF" stroke-width="6" fill="none" stroke-linecap="round"><path d="M65 150V78"/><path d="M20 78H110"/><path d="M20 78V10"/><path d="M110 78V10"/></g></svg></div><svg class="trail" viewBox="0 0 1600 900" preserveAspectRatio="none"><path d="M-140 760 C300 40 1080 20 1520 560"/></svg><div class="pball"><svg viewBox="0 0 132 88" aria-hidden="true"><ellipse class="hide" cx="66" cy="44" rx="58" ry="33"/><path class="stripe" d="M22 27 Q13 44 22 61"/><path class="stripe" d="M110 27 Q119 44 110 61"/><path class="stripe" d="M40 44H92"/><g class="lace"><path d="M50 35v18M60 33v22M70 33v22M80 35v18"/></g></svg></div></div>
<div class="deco scopefield" aria-hidden="true">
  <div class="glass"></div>
  <svg class="ret breathe" viewBox="0 0 1000 620" preserveAspectRatio="xMidYMid slice">
    <g stroke-width="1">
      <line x1="500" y1="0" x2="500" y2="256"/><line x1="500" y1="364" x2="500" y2="620"/>
      <line x1="0" y1="310" x2="436" y2="310"/><line x1="564" y1="310" x2="1000" y2="310"/>
    </g>
    <g stroke-width="2.6" stroke-linecap="round">
      <path d="M500 288v12M500 320v12M488 310h12M512 310h-12"/>
    </g>
    <g stroke-width="1.6" stroke-linecap="round" opacity=".8">
      <path d="M500 372v9M500 402v9M500 432v9M500 462v9M500 492v9
               M500 248v-9M500 218v-9M500 188v-9M500 158v-9
               M436 310h-9M406 310h-9M376 310h-9M346 310h-9
               M564 310h9M594 310h9M624 310h9M654 310h9"/>
    </g>
    <circle cx="500" cy="310" r="286" stroke-width="1.2" opacity=".45"/>
  </svg>
  <svg class="ret" viewBox="0 0 1000 620" preserveAspectRatio="none" style="opacity:.5">
    <g class="corner" stroke-linecap="round">
      <path d="M22 62V22h44"/><path d="M978 62V22h-44"/>
      <path d="M22 558v40h44"/><path d="M978 558v40h-44"/>
    </g>
  </svg>
  <div class="rng"></div>
  <div class="hud"><b>DEADSHOT</b> &middot; OPTIC LIVE<br>MIL-DOT &middot; 10&times;<br>HOLD CENTRE</div>
</div>
<a class="skip" href="#main">Skip to main content</a>
<header class="mast"><div class="mast-in">
    <svg class="scope" viewBox="0 0 120 120" role="img" aria-label="Deadshot crosshair">
      <defs>
        <clipPath id="ck"><circle cx="60" cy="60" r="52"/></clipPath>
        <radialGradient id="glass" cx="38%" cy="32%">
          <stop offset="0" stop-color="var(--rt-g1)"/><stop offset="1" stop-color="var(--rt-g2)"/>
        </radialGradient>
        <linearGradient id="swp" x1="0" y1="1" x2="1" y2="0">
          <stop class="sw0" offset="0" stop-color="var(--rt)"/>
          <stop class="sw1" offset=".5" stop-color="var(--rt)"/>
          <stop class="sw2" offset="1" stop-color="var(--rt)"/>
        </linearGradient>
      </defs>
      <circle cx="60" cy="60" r="55" fill="none" stroke="var(--rt-ring)" stroke-width="6"/>
      <circle cx="60" cy="60" r="52" fill="url(#glass)"/>
      <g clip-path="url(#ck)" class="rt-grid-plain" stroke="var(--rt-grid)" stroke-width=".7" opacity=".65">
        <path d="M12 24H108M12 36H108M12 48H108M12 60H108M12 72H108M12 84H108M12 96H108"/>
        <path d="M24 12V108M36 12V108M48 12V108M60 12V108M72 12V108M84 12V108M96 12V108"/>
      </g>
      <g clip-path="url(#ck)" class="rt-grid-field" aria-hidden="true">
        <g stroke="var(--rt-grid)" stroke-width=".7" opacity=".8">
          <path d="M20 4V116M32 4V116M44 4V116M56 4V116M68 4V116M80 4V116M92 4V116M104 4V116"/>
        </g>
        <g stroke="var(--rt-grid)" stroke-width="1.5" opacity=".95">
          <path d="M8 4V116M116 4V116"/>
        </g>
        <g stroke="var(--rt-grid)" stroke-width=".55" opacity=".62">
          <path d="M14 40h6M26 40h6M38 40h6M50 40h6M62 40h6M74 40h6M86 40h6M98 40h6M110 40h6"/>
          <path d="M14 80h6M26 80h6M38 80h6M50 80h6M62 80h6M74 80h6M86 80h6M98 80h6M110 80h6"/>
        </g>
      </g>
      <g clip-path="url(#ck)" class="sweep">
        <path d="M60 60 L60 4 A56 56 0 0 1 96 20 Z" fill="url(#swp)"/>
      </g>
      <g clip-path="url(#ck)" class="blip" aria-hidden="true">
        <circle cx="84" cy="41" r="3.1" fill="var(--rt)"/>
        <circle cx="84" cy="41" r="3.1" fill="none" stroke="var(--rt)" stroke-width="1.2" class="blip-ring"/>
      </g>
      <g stroke="var(--rt)" stroke-linecap="round">
        <path d="M60 9V44" stroke-width="6"/><path d="M60 76V111" stroke-width="6"/>
        <path d="M9 60H44" stroke-width="6"/><path d="M76 60H111" stroke-width="6"/>
      </g>
      <g stroke="var(--rt)" stroke-width="2.4" stroke-linecap="round" opacity=".9">
        <path d="M53 52h14M53 68h14M52 53v14M68 53v14"/>
      </g>
      <circle cx="60" cy="60" r="2.6" fill="var(--rt)"/>
      <circle cx="60" cy="60" r="52" fill="none" stroke="var(--rt)" stroke-width="1.4" opacity=".55"/>
    </svg>
    <div class="brand">
      <div class="kicker">Fantasy Football &middot; Est. 2015</div>
      <h1>DEADSHOT</h1>
      <div class="sub">Archives</div>
    </div>
    <div class="deco snipe" aria-hidden="true"><svg viewBox="0 0 1400 170" preserveAspectRatio="none">
      <!-- stadia ranging ladder: bars grow as the range closes -->
      <g class="stad">
        <path class="base" d="M470 162H1352"/>
        <g class="tick"><path d="M470 162v-7M525 162v-5M580 162v-9M635 162v-5M690 162v-7M745 162v-5
          M800 162v-13M855 162v-5M910 162v-7M965 162v-5M1020 162v-9M1075 162v-5
          M1130 162v-7M1185 162v-5M1240 162v-17M1295 162v-5"/></g>
        <g class="tickM"><path d="M470 162v-22M800 162v-26M1130 162v-30M1240 162v-34"/></g>
      </g>
      <text class="lab" x="470" y="133">800</text><text class="lab" x="800" y="129">600</text>
      <text class="lab" x="1130" y="125">400</text><text class="lab" x="1240" y="121">200</text>
      <!-- the gate slides down the ladder and locks -->
      <g class="gate"><path d="M-9 148v20M9 148v20M-9 148h6M9 148h-6M-9 168h6M9 168h-6"/></g>
      <!-- ballistic arc with its apex called out -->
      <path class="arc" d="M492 158 C700 128 940 116 1120 122 C1210 126 1288 130 1330 133"/>
      <g class="sweep"><path d="M0 100V170" stroke-width="1.3"/></g>
      <g class="tgt"><rect x="1316" y="126" width="12" height="19" rx="2"/><circle cx="1322" cy="119" r="4.6"/></g>
      <g class="brk">
        <path d="M1312 111h-12v12M1332 111h12v12M1312 149h-12v-12M1332 149h12v-12"/></g>
      <path class="trace" d="M480 160 L1322 130"/>
      <circle class="hit" cx="1322" cy="130" r="10"/>
      <text class="rd rd1" x="1370" y="30">RANGE 812 &#183; WIND 6 L</text>
      <text class="rd rd2" x="1370" y="30">ELEV +2.4 MIL &#183; HOLD 1.8</text>
      <text class="rd rd3" x="1370" y="30">TARGET LOCKED &#183; SEND IT</text>
    </svg></div>
    <div class="deco dossier" aria-hidden="true"><svg viewBox="0 0 1400 170" preserveAspectRatio="none">
      <rect class="bar" x="470" y="26" width="150" height="15"/>
      <rect class="bar" x="632" y="26" width="86" height="15"/>
      <rect class="bar wipe" x="470" y="128" width="228" height="15" style="transform-origin:470px 0"/>
      <rect class="bar" x="712" y="128" width="104" height="15"/>
      </svg>
      <div class="dz-stamp blink">CLASSIFIED</div>
      <div class="dz-meta">FILE NO. DS-2015/2025 &#183; CLEARANCE: LEAGUE MEMBERS ONLY<br>DISTRIBUTION LIST WITHHELD UNDER SECTION 4(b)</div>
    </div>
    <div class="deco pigskin" aria-hidden="true"><svg class="chalk" viewBox="0 0 1400 170" preserveAspectRatio="none">
      <g class="yl" stroke-width="1.6"><path d="M500 128v42M560 132v38M620 128v42M680 132v38M740 128v42M800 132v38M860 128v42M920 132v38M980 128v42M1040 132v38M1100 128v42M1160 132v38M1220 128v42M1280 132v38"/></g>
      <g class="yl5" stroke-width="2.6"><path d="M470 118v52"/></g>
      <g class="hm" stroke-width="1.6"><path d="M486 118h10M516 118h10M546 118h10M576 118h10M606 118h10M636 118h10M666 118h10M696 118h10M726 118h10M756 118h10M786 118h10M816 118h10M846 118h10M876 118h10M906 118h10M936 118h10M966 118h10M996 118h10M1026 118h10M1056 118h10M1086 118h10M1116 118h10M1146 118h10M1176 118h10M1206 118h10M1236 118h10M1266 118h10M1296 118h10M1326 118h10"/></g>
      <text class="yn" x="608" y="158">30</text><text class="yn" x="848" y="158">40</text>
      <text class="yn" x="1088" y="158">50</text>
      <g class="gp"><path d="M1332 170V98"/><path d="M1292 98h80"/><path d="M1292 98V40"/><path d="M1372 98V40"/></g>
      <path class="parc" d="M868 150 C982 58 1064 18 1152 26 C1244 34 1300 48 1338 68"/>
    </svg><div class="pball"><svg viewBox="0 0 132 88" aria-hidden="true"><ellipse class="hide" cx="66" cy="44" rx="58" ry="33"/><path class="stripe" d="M22 27 Q13 44 22 61"/><path class="stripe" d="M110 27 Q119 44 110 61"/><path class="stripe" d="M40 44H92"/><g class="lace"><path d="M50 35v18M60 33v22M70 33v22M80 35v18"/></g></svg></div></div>
    <div class="deco dogfight" aria-hidden="true"><svg viewBox="0 0 1400 170" preserveAspectRatio="none">
      <g class="ship flee"><g transform="scale(1.5)">
        <path d="M0 7 L0 17 L22 17 L38 12 L22 7 Z"/><rect x="6" y="1" width="9" height="22"/>
        <rect x="-8" y="10" width="8" height="4" opacity=".8"/></g></g>
      <g class="ship chase"><g transform="scale(1.7)">
        <path d="M0 7 L0 17 L22 17 L38 12 L22 7 Z"/><rect x="6" y="1" width="9" height="22"/>
        <rect x="-11" y="9" width="11" height="6" opacity=".85"/></g></g>
      <g class="bolt b1"><rect x="0" y="0" width="26" height="4"/></g>
      <g class="bolt b2"><rect x="0" y="0" width="26" height="4"/></g>
      <g class="bolt b3"><rect x="0" y="0" width="20" height="4"/></g>
      <g class="boom"><circle cx="0" cy="0" r="11"/></g>
    </svg></div>
    <svg class="laces" viewBox="0 0 120 150" aria-hidden="true">
      <path d="M60 8 V142" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round" fill="none" opacity=".95"/>
      <g stroke="#FFFFFF" stroke-width="7" stroke-linecap="round">
        <path d="M30 34 H90"/><path d="M30 61 H90"/><path d="M30 88 H90"/><path d="M30 115 H90"/>
      </g>
      <g stroke="rgba(0,0,0,.28)" stroke-width="1.6">
        <path d="M30 34 H90"/><path d="M30 61 H90"/><path d="M30 88 H90"/><path d="M30 115 H90"/>
      </g>
    </svg>
    <div class="facts">
      <div class="fact"><b id="f1">&mdash;</b><span>Seasons</span></div>
      <div class="fact"><b id="f2">&mdash;</b><span>Managers</span></div>
      <div class="fact"><b id="f3">&mdash;</b><span>Team-seasons</span></div>
      <div class="fact"><b id="f4">&mdash;</b><span>Games logged</span></div>
    </div>
  </div></header>
<nav><div class="nav-row" id="navRow"><div class="nav-in"><a class="navmark" href="#champions" aria-label="Top"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="50" fill="none" stroke="var(--brass)" stroke-width="9"/><g stroke="var(--brass)" stroke-width="13" stroke-linecap="round"><path d="M60 6V40"/><path d="M60 80V114"/><path d="M6 60H40"/><path d="M80 60H114"/></g><circle cx="60" cy="60" r="7" fill="var(--brass)"/></svg></a><span id="nav" style="display:contents"></span></div></div>
  <div class="fb"><button class="fb-sum" id="fbSum" type="button" aria-expanded="false"></button><div class="fb-in">
    <span class="fb-lab">Managers</span>
    <button id="fActive">Active 10</button><button id="fAll">All 20</button><button id="fNone">None</button>
    <button id="fToggle">Choose managers &#9662;</button>
    <span class="fb-count" id="fCount"></span>
    <span class="fb-lab" style="margin-left:14px">Theme</span>
    <button data-skin-btn="scope">Scope</button><button data-skin-btn="og">Classic</button><button data-skin-btn="red">Crimson</button><button data-skin-btn="leather">Pigskin</button><button data-skin-btn="arcade">Arcade</button>
  </div><div class="fb-chips" id="fChips" hidden></div></div>
</nav>
<main id="main" class="wrap">

  <section id="champions">
    <div class="sec-head"><h2>Champions</h2><div class="rule-note">Click a year to jump to that bracket<br>with the winner's run traced</div></div>
    <div class="board" id="board"></div>
    <div class="card" id="arcCard" style="margin-top:18px"><div class="card-b" style="padding:15px 18px">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--brass)">This week in league history</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);margin:3px 0 8px" id="arcLabel">From the archive</div>
      <div id="arcMoment" style="font-size:15px;line-height:1.55;color:var(--ink)"></div>
    </div></div>
    <div style="margin-top:14px"><button id="storiesBtn" class="on" style="padding:8px 15px">&#9733; The story of each season</button>
      <span class="sub" style="margin-left:9px">One headline per year, pulled from the record</span></div>
  </section>

  <section id="alltime">
    <div class="sec-head"><h2>All-Time Table</h2><div class="rule-note">Click a name for a full career<br>Click a column to re-sort</div></div>
    <div class="card">
      <div class="card-h"><h3>Career records</h3><span class="sub" id="rangeSub"></span>
        <div class="right">
          <span class="fb-lab">Seasons</span>
          <button data-yr="3">Last 3</button><button data-yr="5">Last 5</button>
          <button data-yr="10">Last 10</button><button data-yr="0" class="on">All</button>
          <input id="search" type="search" aria-label="Filter managers by name" placeholder="filter managers…" style="width:150px"><span class="sub" id="searchN"></span></div></div>
      <div class="scroll"><table id="tAll"></table></div>
    </div>
  </section>
  <section id="power">
    <div class="sec-head"><h2>Power Index<span class="gl" data-gl="pi" tabindex="0">?</span></h2><div class="rule-note">Sorted: seasons played, then surname<br>Click a row to lock it — stacks with others</div></div>
    <p class="lede"><strong>One number for how well a team scored, with the era taken out.</strong> 100 is exactly that season's league average. 112 means you scored 12% more than the typical team that year. It is the only figure on this site you can lay side by side across every season the league has played, which is what makes it the number to argue with.</p>
    <div class="card">
      <div class="card-h"><h3>How to read it</h3><span class="sub">worked from a real season</span></div>
      <div class="card-b" id="piHelp"></div>
    </div>
    <div class="card">
      <div class="card-h"><h3>Power Index by manager and season</h3><span class="sub" id="piLegend"></span></div>
      <div class="card-b scroll"><table class="heat" id="tHeat"></table></div>
    </div>
  <div class="sub-h" style="margin-top:34px">Power Rankings &middot; the ten active managers, live model</div>
    <p class="lede">Not a career table, a <strong>forward-looking</strong> one. It weights recent seasons above old ones, shrinks small samples toward the league mean, and ignores win-loss record entirely in favour of scoring, because record carries luck and scoring does not. Drag the slider to change how hard the model discounts the past and watch the order move.</p>
    <div class="card">
      <div class="card-h"><h3>Going into <span id="nextYr"></span></h3>
        <div class="right">
          <span class="sub" id="lamLbl"></span><span class="gl" data-gl="lambda" tabindex="0">?</span>
          <input type="range" id="lam" min="45" max="100" value="72" aria-label="Recency weighting">
          <button id="lamReset">Reset</button>
        </div></div>
      <div class="card-b" style="padding-bottom:4px"><div id="ladder"></div></div>
      <div class="card-b" style="padding-top:0"><button id="rankMore">Show model details &#9662;</button>
        <span class="sub" style="margin-left:9px">last season's index, momentum, all-play luck, outlook, evidence</span></div>
      <div class="scroll" id="rankTbl" hidden><table id="tRank"></table></div>
      <div class="card-b" style="border-top:1px solid var(--rule);padding-top:11px">
        <details class="expl"><summary>How the score is built</summary>
        <p class="plain" style="margin:0 0 9px"><b>In plain English:</b> &lambda; ("lambda") is the fade rate on old seasons. Slide it low and only the last year or two really count; slide it to 1.00 and a 2015 season counts exactly as much as a 2025 one. Nothing about the data changes &mdash; only how much weight the model gives the past.</p>
        <p style="margin:0;font-size:13px;color:var(--ink-2)">Each season a manager played gets weight <span class="mono">&lambda;<sup>(2025&nbsp;&minus;&nbsp;year)</sup></span>, so at &lambda;&nbsp;=&nbsp;0.72 the 2025 season counts 1.00, 2024 counts 0.72, 2023 counts 0.52 and so on. Those weights are applied to <em>games played</em>, and the weighted mean of Power Index is then pulled toward 100 by <span class="mono">N&nbsp;/&nbsp;(N&nbsp;+&nbsp;25)</span>, where N is the weighted game count — so a manager with one loud season cannot leapfrog a decade of evidence. Projected win rate converts the score through the same Pythagorean exponent used everywhere else, against a 100-rated opponent.</p>
        </details>
      </div>
    </div>

    <div class="card">
      <div class="card-h"><h3>Career races &mdash; one manager, every season</h3>
        <span class="sub">Every season with a game log &middot; one line per season, each in its own colour</span></div>
      <div class="card-b" style="padding-bottom:4px"><div class="pills" id="crPick"></div></div>
      <div class="card-b" style="padding:0 16px 6px"><div class="pills" id="crLeg"></div></div>
      <div class="card-b" style="padding-top:4px"><div class="chart" id="crace"></div>
        <p style="margin:10px 0 0;font-size:12.5px;color:var(--ink-3)">The same bump chart, re-cut by manager: one line per season, <strong>each season in its own colour</strong>, and a year keeps the same colour on every manager's chart. Weekly game logs exist for <span id="crSpan"></span> only, so earlier seasons cannot be drawn. There is no shaded playoff band here because the field size changed between these seasons; each line's dashed tail ends at where that season actually finished.</p></div>
    </div>
  </section>


  <section id="shape">
    <div class="sec-head"><h2>Season Shape</h2><div class="rule-note">Was it a dogfight or a walkover?</div></div>
    <p class="lede">A league average hides the interesting part. These show <strong>how spread out</strong> the league was each year, whether everyone was bunched together or three teams ran away with it.</p>
    <div class="card">
      <div class="card-h"><h3>Every team, every season</h3><span class="sub">Each dot is one team's Power Index · champions in gold · hover to preview, click to lock — as many as you like</span><div class="right"><button id="spotClear" style="display:none">Clear selection</button></div></div>
      <div class="card-b"><div class="chart" id="strip"></div></div>
    </div>
    <div class="card">
      <div class="card-h"><h3 id="balTitle">Competitive balance</h3>
        <div class="right pills">
          <button data-bal="sd" class="on">Scoring spread</button>
          <button data-bal="wsd">Record spread</button>
          <button data-bal="rng">Power index range</button>
          <button data-bal="lg">League avg PPG</button>
        </div></div>
      <div class="card-b"><div class="chart" id="bal"></div>
        <p class="sub" id="balNote" style="margin:12px 0 0;font-family:'IBM Plex Sans',sans-serif;font-size:13px;color:var(--ink-2)"></p></div>
    </div>
  </section>

  <section id="weekly">
    <div class="sec-head"><h2>Week by Week</h2><div class="rule-note">Every matchup · every projection · every trade</div></div>
    <p class="lede">Season totals estimate luck. <strong>Weekly scores measure it.</strong> Choose a season below and every card in this section follows it. Greyed years have no game log yet. These cards always show everyone who played that season, so the manager filter at the top does not apply here.</p>
    <div class="pills" id="wkYears"></div>

    <div class="card">
      <div class="card-h"><h3>The race — league position, week by week</h3>
        <span class="sub">Rank 1 at the top · click any number of teams to lock them</span></div>
      <div class="card-b" style="padding-bottom:6px"><div class="pills" id="raceLeg"></div></div>
      <div class="card-b" style="padding-top:4px"><div class="chart" id="race"></div>
        <p style="margin:10px 0 0;font-size:12.5px;color:var(--ink-3)">Standing after each week, ranked by record then points for, the same tiebreak the league uses. The shaded band is that season's playoff field: <span id="raceSpots"></span>.</p></div>
    </div>

    <div class="card">
      <div class="card-h"><h3>All-play &mdash; the record with the schedule removed</h3><span class="gl" data-gl="allplay" tabindex="0">?</span>
        <span class="sub" id="apSub">Sorted: all-play win %</span></div>
      <div class="card-b" style="padding-bottom:0"><p style="margin:0 0 14px;font-size:13.5px;color:var(--ink-2)">Each week, count how many of the other nine teams you outscored. Every week, versus everyone.</p></div>
      <div class="scroll"><table id="tAP"></table></div>
    </div>

    <div class="card" data-collapse="closed">
      <div class="card-h"><h3>Beating the projection</h3><span class="sub">Actual points minus the projections, per week</span></div>
      <div class="card-b" style="padding-bottom:0"><p style="margin:0 0 14px;font-size:13.5px;color:var(--ink-2)">Each week's score is shown against what the site projected for it. Beating that projection regularly points to sound start and sit decisions and useful waiver work. Any single week swings heavily on luck, so the per week column carries more meaning than the season total.</p></div>
      <div class="scroll"><table id="tProj"></table></div>
    </div>

    <div class="card" data-collapse="closed">
      <div class="card-h"><h3>Biggest rivals this year</h3><span class="gl" data-gl="rivalry" tabindex="0">?</span><span class="sub">meetings &times; balance &times; closeness</span></div>
      <div class="card-b" style="padding-bottom:0"><p style="margin:0 0 14px;font-size:13.5px;color:var(--ink-2)" id="rivPick"></p></div>
      <div class="scroll"><table id="tRiv"></table></div>
    </div>

    <div class="card">
      <div class="card-h"><h3>Weekly scoreboard</h3>
        <span class="sub">Share on any result makes a picture of it for the group chat</span>
        <button id="wkLink" style="padding:5px 11px;margin-left:8px">&#128279; Copy link to this week</button>
        <div class="right pills" id="wkSel"></div></div>
      <div class="card-b" id="wkOut"></div>
    </div>

    <div class="card" data-collapse="closed" data-collapse-also="#trades">
      <div class="card-h"><h3>Trades</h3><span class="sub" id="trSub"></span></div>
      <div class="card-b"><div class="tiles" id="tradeStat" style="margin-bottom:0"></div></div>
    </div>
    <div id="trades" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,380px),1fr));gap:20px;margin-top:20px"></div>
  </section>

  <section id="luck">
    <div class="sec-head"><h2>The Luck Ledger<span class="gl" data-gl="luck" tabindex="0">?</span></h2><div class="rule-note">Sorted: luckiest first</div></div>
    <p class="lede"><strong>Luck is actual wins minus the wins your points deserved.</strong> Pythagorean expectation says a team scoring 1,900 and allowing 1,700 should win about 8 of 14. Win 11 and you banked three wins your scoring did not earn.</p>
    <div class="card">
      <div class="card-h"><h3>Wins above or below what the scoring earned</h3>
        <div class="right"><button id="qLuck" class="on">Hide 1-season managers</button></div></div>
      <div class="scroll"><table id="tLuck"></table></div>
    </div>
  </section>

  <section id="advanced">
    <div class="sec-head"><h2>Advanced</h2><div class="rule-note">Consistency · Z-score · Playoffs</div></div>
    <p class="lede">These measures are built from season totals and the playoff game log, so they cover all ten seasons. The Week by Week section examines the same ground in more detail, but only for the years with a game log loaded.</p>
    <div class="card">
      <div class="card-h"><h3>Consistency, form and Z-score</h3><span class="gl" data-gl="z" tabindex="0">?</span><span class="sub" id="advSub"></span>
        <div class="right">
          <span class="fb-lab">Seasons</span>
          <button data-adv="1">Last only</button><button data-adv="3">Last 3</button><button data-adv="5">Last 5</button>
          <button data-adv="10">Last 10</button><button data-adv="0" class="on">All</button>
          <button id="advPick">Pick seasons &#9662;</button>
          <button id="qCon" class="on">Hide 1-season managers</button></div></div>
      <div class="card-b" id="advYrChips" hidden style="border-bottom:1px solid var(--rule-2);display:flex;flex-wrap:wrap;gap:6px;align-items:center"></div>
      <div class="scroll"><table id="tCon"></table></div>
    </div>
    <div class="card">
      <div class="card-h"><h3>Playoff résumé</h3><span class="gl" data-gl="expT" tabindex="0">?</span><span class="sub" id="poSub">Sorted: playoff wins</span></div>
      <div class="scroll"><table id="tPO"></table></div>
    </div>
  <div class="sub-h" style="margin-top:34px">The .500 Line &middot; who lives above it, who lives under it</div>
    <p class="lede">Win percentage tells you where a career ended up. It does not tell you how much of it was spent winning. <strong>Games clear</strong> is wins minus losses across a whole career, the plainest measure there is. <strong>Weeks above</strong> goes finer, walking each season week by week and asking whether that manager's record was above water at the time; it covers 2021&ndash;2025, the seasons with a loaded game log. <strong>Expected vs average</strong> asks a different question again: forget the schedule, how many wins did the <em>scoring</em> earn above a perfectly average team?</p>
    <div class="card">
      <div class="card-h"><h3>Above and below</h3><span class="gl" data-gl="five" tabindex="0">?</span>
        <span class="sub">Career &middot; every manager</span>
        <div class="right"><button id="fiveMore" class="on">Hide table &#9652;</button></div></div>
      <div class="scroll" id="fiveTbl"><table id="tFive"></table></div>
    </div>
  </section>


  <section id="seasons">
    <div class="sec-head"><h2>Seasons</h2><div class="rule-note">Standings and bracket, year by year<br>Everyone who played that season is shown</div></div>
    <div class="pills" id="yrPills" style="margin:16px 0 18px"></div>
    <div id="seasonPane"></div>
    <div id="schedPane"></div>
    <div class="card" style="margin-top:20px">
      <div class="card-b" style="padding-top:13px">
        <details class="expl"><summary>Every team name in league history</summary>
        <p class="plain" style="margin:0 0 10px"><b>In plain English:</b> the section above shows one season at a time, so a team from a year you are not looking at cannot be found with your browser's search. This list holds every name the league has ever had, so searching for one always works.</p>
        <div id="teamIndex" style="font-size:13px;color:var(--ink-2)"></div>
        </details>
      </div>
    </div>
  </section>

  <section id="h2h">
    <div class="sec-head"><h2>Head to Head</h2><div class="rule-note">Sorted: seasons played</div></div>
    <p class="lede">Read across: the row manager's record against the column manager. Playoffs cover all ten seasons; regular season covers only the years whose game logs are loaded. Use the manager filter at the top to cut the grid down to the people you care about.</p>
    <div class="card">
      <div class="card-h"><h3>Pick two managers</h3><div class="right">
        <select id="cmpA"></select><span class="sub">versus</span><select id="cmpB"></select>
        <button id="cmpShare" class="on" style="padding:7px 14px;margin-left:8px">&#8593; Share this matchup</button>
        <button id="cmpRiv" style="padding:7px 14px;margin-left:6px">&#8593; Every meeting</button></div></div>
      <div class="card-b" id="cmpOut"></div>
    </div>
    <div class="card">
      <div class="card-h"><h3 id="mtxTitle">Head-to-head</h3><span class="sub">Wins–losses · blank means they have never met · hover for the games</span>
        <div class="right pills">
          <button data-mx="all" class="on">All games</button>
          <button data-mx="reg">Regular season</button>
          <button data-mx="po">Playoffs</button>
        </div></div>
      <div class="card-b" style="padding-bottom:0"><p style="margin:0 0 12px;font-size:13px;color:var(--ink-2)" id="mtxNote"></p></div>
      <div class="card-b scroll" style="padding-top:0"><table class="mtx" id="tMtx"></table></div>
    </div>
  </section>

  <section id="trades-sec">
    <div class="sec-head"><h2>Trade Market</h2><div class="rule-note">Who deals, and who they deal with<br>2021&ndash;2025 &middot; the years with logs</div></div>
    <p class="lede">Every trade in the five seasons whose transaction logs are loaded. A trade counts once for each side, so the two managers in a deal each get credit for it. In and out count players, not deals: a three-for-one shows up as 3 in and 1 out for the side receiving three.</p>
    <div class="card">
      <div class="card-h"><h3>Trade ledger</h3><span class="gl" data-gl="trade" tabindex="0">?</span><span class="sub" id="trLedSub"></span></div>
      <div class="scroll"><table id="tTrLed"></table></div>
    </div>
    <div class="card">
      <div class="card-h"><h3>Who trades with whom</h3><span class="sub">Deals between each pair &middot; blank means they have never traded &middot; hover for the deals</span></div>
      <div class="card-b scroll" style="padding-bottom:0"><table class="mtx" id="tTrMtx"></table></div>
      <div class="card-b"><div class="tiles" id="trPairs"></div></div>
    </div>
    <div class="card">
      <div class="card-h"><h3>Each manager, year by year</h3><span class="sub">Deals made that season &middot; <b>0</b> = played, made none &middot; <b>&middot;</b> = not in the league &middot; hover for the deals</span></div>
      <div class="card-b scroll" style="padding-bottom:0"><table class="mtx" id="tTrYr"></table></div>
    </div>
    <div class="card">
      <div class="card-h"><h3>Trades per season</h3><span class="sub">Total deals in the league each year</span></div>
      <div class="card-b" id="trYears"></div>
    </div>
  </section>

  <section id="records">
    <div class="sec-head"><h2>Record Book</h2><div class="rule-note">Each table by its own metric</div></div>
    <p class="lede">Season length has been 13, 14 and 15 games, so the headline records are <strong>per game</strong>; raw totals are kept separately and labelled as counting records, because a 15-game season will always out-total a 13-game one. <strong>Single-season records include everyone</strong>, because one enormous year is a real record no matter how briefly someone played. The career <em>rate</em> tables below (win %, average finish, power index, luck) exclude one-season managers, whose tiny samples otherwise own every extreme; the career <em>counting</em> tables (total points, playoff wins) include everyone, since volume cannot be inflated by a short career.</p>
    <div style="margin:4px 0 6px"><button id="recsToggle" style="padding:9px 16px">Show the record book &#9662;</button>
      <select id="recPick" style="margin-left:8px"></select>
      <button id="recShare" style="padding:9px 16px;margin-left:6px">&#8593; Share this record</button>
      <span class="sub" style="margin-left:9px" id="recsCount"></span></div>
    <div id="recsWrap" hidden>
      <div id="recs"></div>
      <div class="card" style="margin-top:22px">
        <div class="card-h"><h3>Milestone watch</h3><span class="sub">How close each manager is to the next round number</span></div>
        <div class="card-b" id="mileWatch"></div>
      </div>
    </div>
  </section>

  <section id="method">
    <div class="card" style="margin-bottom:18px">
      <div class="card-h"><h3>League rules</h3><span class="sub">Read from Yahoo &middot; league 526001 &middot; 26 Aug 2026</span></div>
      <div class="card-b">
        <p class="lede" style="margin:0 0 13px">Everything below is the league's own configuration, not an assumption. The one that matters most for reading any number on this site: Deadshot is full PPR, meaning a reception is worth 1.0, double Yahoo's default. That is why scores here run 120&ndash;140 rather than 90&ndash;110, and why raw points cannot be compared against another league.</p>
        <div class="rules">
          <div><h4>Format</h4><ul>
            <li>10 teams &middot; head-to-head &middot; scoring from week 1</li>
            <li>Playoffs: 6 teams, weeks 15&ndash;17</li>
            <li><b>Reseeding after each round</b></li>
            <li>Seed tie-break: head-to-head record, then Yahoo's order</li>
            <li>Fractional and negative points both on</li></ul></div>
          <div><h4>Roster &mdash; 17 slots</h4><ul>
            <li>QB, WR, WR, RB, RB, TE, W/R/T</li>
            <li>K, DEF</li>
            <li>6 bench, 2 IR</li></ul></div>
          <div><h4>Offense</h4><ul>
            <li>Pass 25 yds/pt &middot; pass TD 4 &middot; INT &minus;1</li>
            <li>Rush 10 yds/pt &middot; rush TD 6</li>
            <li><b>Reception 1.0</b> <span class="dim">(default 0.5)</span></li>
            <li>Rec 10 yds/pt &middot; rec TD 6</li>
            <li>2-pt 2 &middot; fumble lost &minus;2</li></ul></div>
          <div><h4>Kicker</h4><ul>
            <li>FG 0&ndash;39: 3 &middot; 40&ndash;49: 4 &middot; 50+: 5</li>
            <li>PAT 1</li></ul></div>
          <div><h4>Defense</h4><ul>
            <li>Sack 1 &middot; INT 2 &middot; fumble rec 2 &middot; TD 6</li>
            <li>Safety 3 <span class="dim">(default 2)</span></li>
            <li>Block kick 2.5 <span class="dim">(default 2)</span></li>
            <li>4th-down stop 1 <span class="dim">(default 0)</span></li>
            <li>Three-and-out 0.5 <span class="dim">(default 0)</span></li>
            <li>Pts allowed 0&rarr;10, 1&ndash;6&rarr;7, 7&ndash;13&rarr;4, 14&ndash;20&rarr;2, 21&ndash;27&rarr;0, 28&ndash;34&rarr;&minus;1, 35+&rarr;&minus;4</li></ul></div>
          <div><h4>Transactions</h4><ul>
            <li>No cap on adds or trades</li>
            <li>Trade deadline: late November</li>
            <li>Commissioner review, 2-day reject window</li>
            <li>Waivers: continual rolling, 2 days</li>
            <li>No draft-pick trading</li></ul></div>
        </div>
      </div>
    </div>
    <div class="sec-head"><h2>Method</h2><div class="rule-note">How every number is derived</div></div>
    <p class="lede">Nothing here is a black box. Each row gives what the metric answers, the arithmetic behind it, and what it cannot see.</p>
    <div class="card"><div class="method" id="methodBody"></div></div>
  </section>

  <footer>
    <strong>Deadshot Fantasy Football — Archives.</strong> Built from the league history workbook.
    Points data is verified: in all ten seasons, league-wide points for equals league-wide points against to the cent.
    One known gap remains: the 2019 season is absent from the source records. The 2022 win-loss column was wrong in the original spreadsheet (72 wins against 68 losses); the 2022 game log settled it, and the corrected records shown here total 70–70 and match Yahoo exactly.
  </footer>
</main>
<div class="deco ball" aria-hidden="true"><svg viewBox="0 0 400 250">
  <ellipse cx="200" cy="125" rx="185" ry="108" fill="none" stroke="currentColor" stroke-width="7"/>
  <path d="M118 125 H282" stroke="currentColor" stroke-width="7" stroke-linecap="round"/>
  <g stroke="currentColor" stroke-width="6" stroke-linecap="round">
    <path d="M150 108 V142"/><path d="M180 104 V146"/><path d="M210 104 V146"/><path d="M240 108 V142"/>
  </g>
  <path d="M56 70 Q92 125 56 180" fill="none" stroke="currentColor" stroke-width="5"/>
  <path d="M344 70 Q308 125 344 180" fill="none" stroke="currentColor" stroke-width="5"/>
</svg></div>
<button class="totop" id="toTop" type="button" aria-label="Back to top"><span class="ar">&#8593;</span> Top</button>
<div class="tip" id="tip"></div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<div class="ov" id="ov"><div class="modal" role="dialog" aria-modal="true" aria-labelledby="mTitle">
  <div class="modal-h"><div><h3 id="mTitle"></h3><div class="sub" id="mSub"></div></div><button class="xbtn" id="mX" aria-label="Close">&#10005;</button></div>
  <div class="modal-b" id="mBody"></div>
</div></div>
<div class="wrap-ov" id="wrapOv" role="dialog" aria-modal="true" aria-label="Season Wrapped">
  <div class="wr-stage" id="wrStage">
    <div class="wr-blob a" aria-hidden="true"></div><div class="wr-blob b" aria-hidden="true"></div>
    <div class="wr-bars" id="wrBars"></div>
    <div class="wr-top"><div class="wrb" id="wrBrand"></div><button class="wr-x" id="wrShare" aria-label="Share this card" title="Share this card">&#8593;</button><button class="wr-x" id="wrX" aria-label="Close" style="margin-left:7px">&#10005;</button></div>
    <button class="wr-nav l" id="wrPrev" aria-label="Previous card"></button>
    <button class="wr-nav r" id="wrNext" aria-label="Next card"></button>
    <div class="wr-card" id="wrCard" aria-live="polite"></div>
    <div class="wr-paused">Paused</div>
    <div class="wr-foot"><span id="wrCount"></span><span class="hint" id="wrHint">Tap right &#8594;</span></div>
  </div>
</div>
<script>const DATA = __DATA__;</script>
"""

JS = r"""
<script>
const $=(s,e=document)=>e.querySelector(s), $$=(s,e=document)=>[...e.querySelectorAll(s)];
const D=DATA, ROWS=D.rows, M=D.mgrs, SEA=D.seasons, LAST=D.last, K=2.37;
const byName={}; M.forEach(m=>byName[m.name]=m);
const rowsOf={}; ROWS.forEach(r=>(rowsOf[r.mgr]=rowsOf[r.mgr]||[]).push(r));
const f=(v,d=2)=>v==null||v===''?'—':(+v).toFixed(d);
const pct=v=>v==null?'—':(100*v).toFixed(1)+'%';
const ord=n=>n+(['','st','nd','rd'][n]||'th');
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const cssv=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const ACTIVE=[...new Set(ROWS.filter(r=>r.y===LAST).map(r=>r.mgr))];
const surname=n=>n.split(' ').slice(-1)[0];
/* seasons played, then surname A-Z — a stated rule, not a hand-placed order */
const bySeasons=(a,b)=>b.seasons-a.seasons||surname(a.name).localeCompare(surname(b.name))||a.name.localeCompare(b.name);
const ALLNAMES=M.map(m=>m.name);
/* ---- global manager filter ---- */
const REDRAW=[];
let SEL=new Set(ACTIVE);            /* first visit shows the current managers only */
try{const st=localStorage.getItem('deadshot.sel');
  if(st){const a=JSON.parse(st); if(Array.isArray(a))SEL=new Set(a.filter(n=>ALLNAMES.includes(n)));}}catch(e){}
/* ---- skins ---- */
const SKINS=['scope','og','red','leather','arcade','redact'];
const SECRET='redact';
function setSkin(k,save){
  if(!SKINS.includes(k))k='og';
  document.documentElement.setAttribute('data-skin',k);
  $$('[data-skin-btn]').forEach(b=>b.classList.toggle('on',b.dataset.skinBtn===k));
  if(save){try{localStorage.setItem('deadshot.skin',k);}catch(e){}}
  /* charts bake colours into markup, so redraw them on a skin change */
  requestAnimationFrame(()=>REDRAW.forEach(f=>{try{f();}catch(e){}}));
}
const vis=n=>SEL.has(n);
function saveSel(){try{localStorage.setItem('deadshot.sel',JSON.stringify([...SEL]));}catch(e){}}
function setSel(list){SEL=new Set(list);saveSel();$('#spotClear').onclick=()=>{PICK.clear();spotlight();};
syncFilter();}
function syncFilter(){
  $$('#fChips button').forEach(b=>b.classList.toggle('on',SEL.has(b.dataset.n)));
  const n=SEL.size;
  $('#fCount').textContent=n===ALLNAMES.length?'all '+n+' shown':n+' of '+ALLNAMES.length+' shown';
  const act=SEL.size===ACTIVE.length&&ACTIVE.every(a=>SEL.has(a));
  $('#fActive').classList.toggle('on',act);
  $('#fAll').classList.toggle('on',n===ALLNAMES.length);
  REDRAW.forEach(f=>{try{f();}catch(e){console.error(e);}});
}

/* tooltip */
const tip=$('#tip');
function showTip(e,h){tip.innerHTML=h;tip.classList.add('on');moveTip(e);}
function moveTip(e){const r=tip.getBoundingClientRect();let x=e.clientX+14,y=e.clientY+16;
  if(x+r.width>innerWidth-8)x=e.clientX-r.width-14; if(y+r.height>innerHeight-8)y=e.clientY-r.height-16;
  tip.style.left=x+'px';tip.style.top=y+'px';}
const hideTip=()=>tip.classList.remove('on');
const GLOSS={
 z:`<b>Z-score</b><br>How far clear of the field you scored, in standard deviations.<br><br>`+
   `Take a team's points per game, subtract that season's league average, then divide by how spread out the league was that year.<br><br>`+
   `<b>0.00</b> = exactly average. <b>+1.00</b> = a full standard deviation above the field, roughly the top 16% of teams. <b>&minus;1.00</b> = the same distance below.<br><br>`+
   `Why it exists: Power Index says <i>how much</i> better you scored. Z says <i>how far clear of the pack</i> you were. In a tightly bunched season a small scoring edge is a big Z; in a wild season the same edge is nothing.`,
 lambda:`<b>&lambda; &mdash; "lambda"</b><br>The fade rate on old seasons.<br><br>`+
   `Each season a manager played is multiplied by &lambda; raised to the power of how many years ago it was. At <b>&lambda; = 0.72</b>: this year counts 1.00, last year 0.72, two years ago 0.52, three years ago 0.37.<br><br>`+
   `<b>Low &lambda; (0.45)</b> &mdash; only the last season or two really matter.<br><b>High &lambda; (1.00)</b> &mdash; every season counts the same, however old.<br><br>`+
   `It changes nothing about the data. It only changes how much the model trusts the past.`,
 pi:`<b>Power Index</b><br>Scoring, indexed so that <b>100 = that season's league average</b>.<br><br>`+
   `A team at 112 scored 12% more than the average team in its own year. A team at 91 scored 9% less.<br><br>`+
   `The point of indexing is cross-era comparison: raw points per game drift over the years as rosters and scoring settings change, so 130 PPG in 2015 and 130 PPG in 2025 are not the same achievement. Power Index makes them comparable.`,
 luck:`<b>Luck</b><br>Actual wins minus the wins your scoring deserved.<br><br>`+
   `The deserved figure comes from Pythagorean expectation &mdash; points for and points against run through an exponent (2.37 here) that converts a scoring ratio into an expected win rate.<br><br>`+
   `<b>+2</b> means you won two more games than your scoring earned; you drew soft matchups or won the close ones. <b>&minus;2</b> means the schedule robbed you.`,
 allplay:`<b>All-play record</b><br>What your record would be if you played <i>everyone</i> every week.<br><br>`+
   `Each week your score is compared against all nine other teams. Beat seven of them and you go 7&ndash;2 that week, regardless of who you were actually scheduled against. An exact tie counts as neither.<br><br>`+
   `Over a season it removes schedule luck almost entirely &mdash; it is the cleanest measure of how well a team actually played.`,
 rivalry:`<b>Rivalry score</b><br>Meetings &times; balance &times; closeness.<br><br>`+
   `A rivalry needs all three: they have to have played often, the record has to be near even, and the games have to be tight. A 6&ndash;0 sweep is a beating, not a rivalry.`,
 expT:`<b>Expected titles</b><br>A coin flip in every round: <b>(&frac12;)^(wins needed)</b>, summed over every playoff berth.<br><br>`+
   `In a 4-team bracket everyone needs 2 wins, so every qualifier is worth 0.25. In a 6-team bracket the top two seeds skip a round &mdash; they need 2 wins and are worth 0.25, while seeds 3&ndash;6 need 3 and are worth 0.125.<br><br>`+
   `It prices the bye a top seed actually earned, and still sums to exactly 1.00 across each season, so it stays neutral.<br><br>`+
   `<b>vs Exp</b> is real titles minus that number &mdash; the closest thing here to a clutch measure.`,
 five:`<b>The .500 line</b><br>.500 means exactly even &mdash; as many wins as losses. A win rate of .500 is 50%.<br><br>`+
   `<b>vs .500</b> here is how far above or below even a career sits: +17.6% means winning 67.6% of the time, 17.6 points clear of even.<br><br>`+
   `<b>Weeks above</b> walks each season week by week and asks whether the record was above even <i>at that moment</i>, not just where it finished. 8-6 wire to wire and 8-6 after a 1-5 start are the same record and completely different seasons.<br><br>`+
   `<b>vs winners</b> is the record against opponents who finished that season above .500.`,
 trade:`<b>Trade counting</b><br>A deal counts once for <i>each</i> side, so both managers get credit for it.<br><br>`+
   `<b>In</b> and <b>out</b> count players, not deals: a three-for-one is 3 in and 1 out for the side receiving three.<br><br>`+
   `Only the seasons whose transaction logs are loaded are counted &mdash; 2021 through 2025.`};
function glossify(root){(root||document).querySelectorAll('[data-gl]').forEach(el=>{
  if(el.dataset.glBound)return; el.dataset.glBound='1';
  const h=GLOSS[el.dataset.gl]; if(h)bindTip(el,h);});}
function bindTip(el,h){el.addEventListener('mouseenter',e=>showTip(e,h));el.addEventListener('mousemove',moveTip);
  el.addEventListener('mouseleave',hideTip);
  if(el.hasAttribute('tabindex')||el.tagName==='BUTTON'){
    el.addEventListener('focus',()=>{const r=el.getBoundingClientRect();
      showTip({clientX:r.left+r.width/2,clientY:r.bottom-4},h);});
    el.addEventListener('blur',hideTip);
    el.addEventListener('keydown',e=>{if(e.key==='Escape')hideTip();});}}

/* colour */
function mix(a,b,t){const p=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16));const A=p(a),B=p(b);
  return '#'+A.map((v,i)=>Math.round(v+(B[i]-v)*t).toString(16).padStart(2,'0')).join('');}
function diverge(v,span){const s=cssv('--surface'),t=Math.max(-1,Math.min(1,v/span));
  return t>=0?mix(s,cssv('--pos'),Math.pow(t,.72)*.82):mix(s,cssv('--neg'),Math.pow(-t,.72)*.82);}
/* WCAG relative luminance -> real contrast, not a guessed threshold on the input value.
   A flat cutoff on v/span drifted out of sync with the actual mixed colour per theme and
   left some heat cells under 3:1 -- e.g. white on rgb(112,170,207) measured 2.52:1. */
function relLum(hex){const c=[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255).map(v=>v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4));
  return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2];}
function contrastHex(a,b){const L1=relLum(a),L2=relLum(b);return (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);}
function pickInk(bg){
  const white=contrastHex(bg,'#ffffff'), ink=contrastHex(bg,cssv('--ink'));
  if(Math.max(white,ink)>=4.5) return white>=ink?'#fff':'var(--ink)';
  /* neither the theme's own ink token nor plain white clears 4.5:1 against this
     particular mixed background -- max(contrast-to-white, contrast-to-black) is
     mathematically >=~4.58 for ANY background (the two curves cross there), so
     falling back to true black/white is a guaranteed last resort, not a guess. */
  return contrastHex(bg,'#ffffff')>=contrastHex(bg,'#000000')?'#fff':'#000';
}
const inkOn=(v,span)=>pickInk(diverge(v,span));

$('#f1').textContent=SEA.length;$('#f2').textContent=M.length;$('#f3').textContent=ROWS.length;$('#f4').textContent=D.games.length+(D.wkYears||[]).reduce((n,y)=>n+D.wk[y].games.filter(g=>g.br==='').length,0);
$('#nextYr').textContent=LAST+1;

/* nav */
const SECS=[['champions','Champions'],['alltime','All-Time'],['power','Power Index'],
 ['shape','Season Shape'],['weekly','Week by Week'],['luck','Luck'],['advanced','Advanced'],
 ['seasons','Seasons'],['h2h','Head to Head'],['trades-sec','Trade Market'],
 ['records','Records'],['method','Method']];
$('#nav').innerHTML=SECS.map(([i,t])=>`<a href="#${i}" data-id="${i}">${t}</a>`).join('');
/* the nav scrolls on every width; it just should not look like it does */
(function(){
  const row=$('#navRow'), sc=$('.nav-in'); if(!row||!sc)return;
  ['l','r'].forEach(side=>{
    const btn=document.createElement('button');
    btn.className='nav-ar '+side; btn.type='button';
    btn.setAttribute('aria-label',side==='l'?'Scroll navigation left':'Scroll navigation right');
    btn.innerHTML=side==='l'?'&#10094;':'&#10095;';
    btn.onclick=()=>sc.scrollBy({left:(side==='l'?-1:1)*Math.max(180,sc.clientWidth*.6),behavior:'smooth'});
    row.appendChild(btn);});
  const sync=()=>{const max=sc.scrollWidth-sc.clientWidth;
    row.classList.toggle('sL',sc.scrollLeft>4);
    row.classList.toggle('sR',sc.scrollLeft<max-4);};
  sc.addEventListener('scroll',sync,{passive:true});
  addEventListener('resize',sync); sync(); setTimeout(sync,400);
  /* keep the active section in view as you scroll the page */
  window.navFollow=id=>{const a=sc.querySelector('a[data-id="'+id+'"]'); if(!a)return;
    const l=a.offsetLeft, r=l+a.offsetWidth;
    if(l<sc.scrollLeft+40)sc.scrollTo({left:Math.max(0,l-60),behavior:'smooth'});
    else if(r>sc.scrollLeft+sc.clientWidth-40)sc.scrollTo({left:r-sc.clientWidth+60,behavior:'smooth'});};
})();
(function(){
  const bt=$('#toTop'); if(!bt)return;
  const top=()=>{try{scrollTo({top:0,behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'});}catch(e){scrollTo(0,0);}
    const h=$('#champions')||document.body; h.setAttribute('tabindex','-1'); h.focus({preventScroll:true});};
  bt.addEventListener('click',top);
  let t=0;
  const sync=()=>{bt.classList.toggle('vis',(scrollY||document.documentElement.scrollTop)>640);};
  addEventListener('scroll',()=>{if(t)return;t=requestAnimationFrame(()=>{t=0;sync();});},{passive:true});
  sync();
})();
const navA=$$('#nav a');
new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting)navA.forEach(a=>a.classList.toggle('on',a.dataset.id===en.target.id));}),
  {rootMargin:'-45% 0px -50% 0px'}).observe&&$$('section').forEach(s=>
  new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){navA.forEach(a=>a.classList.toggle('on',a.dataset.id===en.target.id));
    if(window.navFollow)navFollow(en.target.id);}}),
  {rootMargin:'-45% 0px -50% 0px'}).observe(s));

/* filter bar */
$('#fChips').innerHTML=[...ALLNAMES].sort().map(n=>{
  const m=byName[n], a=ACTIVE.includes(n);
  return `<button data-n="${esc(n)}" title="${m.seasons} seasons${a?' · active':''}">${esc(n)}${a?'':' <span style="opacity:.55">·ret</span>'}</button>`;}).join('');
$$('#fChips button').forEach(b=>b.onclick=()=>{
  const n=b.dataset.n; SEL.has(n)?SEL.delete(n):SEL.add(n); saveSel(); $('#spotClear').onclick=()=>{PICK.clear();spotlight();};
syncFilter();});
$('#fAll').onclick=()=>setSel(ALLNAMES);
$('#fActive').onclick=()=>setSel(ACTIVE);
$('#fNone').onclick=()=>{$('#fChips').hidden=false;$('#fToggle').classList.add('on');setSel([]);};
/* ---- one theme is not on the bar ---- */
const UKEY='deadshot.clearance';
function unlocked(){try{return localStorage.getItem(UKEY)==='1';}catch(e){return false;}}
function toast(html,ms){const t=$('#toast'); t.innerHTML=html; t.classList.add('on');
  clearTimeout(toast._t); toast._t=setTimeout(()=>t.classList.remove('on'),ms||4200);}
function revealSecret(){
  if($('[data-skin-btn="'+SECRET+'"]'))return;
  const bar=$('[data-skin-btn="arcade"]').parentNode;
  const b=document.createElement('button');
  b.dataset.skinBtn=SECRET; b.textContent='Redacted';
  b.title='Clearance granted';
  bar.insertBefore(b,$('[data-skin-btn="arcade"]').nextSibling);
  b.onclick=()=>setSkin(SECRET,true);
}
function grantClearance(loud){
  try{localStorage.setItem(UKEY,'1');}catch(e){}
  revealSecret();
  if(loud){setSkin(SECRET,true);
    toast('<b>CLEARANCE GRANTED</b> &nbsp;·&nbsp; file DS-2015/2025 unsealed &nbsp;·&nbsp; a sixth theme is now on the bar',6000);}
}
/* Sound. Synthesised in the browser — no files, nothing to download, nothing to
   block rendering. Only ever fires from a click, so autoplay policy is satisfied. */
let AC=null;
function ac(){ if(AC)return AC;
  try{AC=new (window.AudioContext||window.webkitAudioContext)();}catch(e){AC=false;}
  return AC; }
const quiet=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
function tone(f,dur,type,vol,slideTo,delay){
  const c=ac(); if(!c||quiet())return;
  /* Never schedule in the past. A fresh AudioContext sits at currentTime 0 for its first
     few milliseconds, so a sound that jitters its own start time could land on a negative
     value, throw, and take its caller down with it. */
  const t0=Math.max(c.currentTime,c.currentTime+(delay||0));
  const o=c.createOscillator(), g=c.createGain();
  o.type=type||'sine'; o.frequency.setValueAtTime(f,t0);
  if(slideTo)o.frequency.exponentialRampToValueAtTime(Math.max(20,slideTo),t0+dur);
  g.gain.setValueAtTime(0.0001,t0);
  g.gain.exponentialRampToValueAtTime(vol||.08,t0+Math.min(.03,dur/3));
  g.gain.exponentialRampToValueAtTime(0.0001,t0+dur);
  o.connect(g).connect(c.destination); o.start(t0); o.stop(t0+dur+.05);
}
function noise(dur,vol,f0,f1,delay,type,curve){
  const c=ac(); if(!c||quiet())return;
  const t0=Math.max(c.currentTime,c.currentTime+(delay||0)), n=Math.max(1,Math.floor(c.sampleRate*dur));
  const b=c.createBuffer(1,n,c.sampleRate), d=b.getChannelData(0);
  const p=curve||1;
  for(let i=0;i<n;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/n,p);
  const src=c.createBufferSource(); src.buffer=b;
  const flt=c.createBiquadFilter(); flt.type=type||'lowpass';
  flt.frequency.setValueAtTime(f0,t0);
  flt.frequency.exponentialRampToValueAtTime(Math.max(40,f1),t0+dur);
  const g=c.createGain(); g.gain.setValueAtTime(Math.max(0.0001,vol),t0);
  g.gain.exponentialRampToValueAtTime(0.0001,t0+dur);
  src.connect(flt).connect(g).connect(c.destination); src.start(t0);
}
/* ---- richer synthesis -------------------------------------------------------
   Everything is generated. No audio files, so the page stays self-contained. */

/* A metallic strike. Real metal rings on inharmonic partials, which is what makes it
   read as brass rather than a tuned note, and each partial dies faster than the one
   below it. Used for the casing hitting the floor. */
function ping(f, dur, vol, delay, tone2) {
  const c = ac(); if (!c || quiet()) return;
  const t0 = Math.max(c.currentTime, c.currentTime + (delay || 0));
  const PARTIALS = [1, 2.76, 5.40, 8.93, 13.34];
  PARTIALS.forEach((m, i) => {
    const o = c.createOscillator(), g = c.createGain();
    o.type = 'sine';
    o.frequency.setValueAtTime(f * m * (tone2 || 1), t0);
    const v = Math.max(0.0002, (vol || 0.1) * Math.pow(0.52, i));
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(v, t0 + 0.0012);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur * Math.pow(0.72, i));
    o.connect(g).connect(c.destination);
    o.start(t0); o.stop(t0 + dur + 0.05);
  });
  noise(0.005, (vol || 0.1) * 0.55, 11000, 4000, delay || 0, 'highpass', 0.4);
}

/* A brass case ejected onto a hard floor: a first hard hit, then bounces that get
   closer together and quieter as it loses energy, then a short skitter as it settles. */
function casing(delay) {
  const d = delay || 0;
  let t = d, gap = 0.42, v = 0.085, f = 2400;
  for (let i = 0; i < 7; i++) {
    ping(f * (0.9 + Math.random() * 0.25), 0.42 - i * 0.04, v, t, 1);
    t += gap;
    gap *= 0.82;                 /* bounces converge, like a dropped coin */
    v *= 0.78;
    f *= 1.04;
  }
  for (let i = 0; i < 7; i++)    /* the last roll along the ground */
    noise(0.035, 0.02, 6000, 2600, t + i * 0.11 + Math.random() * 0.06, 'bandpass', 0.6);
}

/* Thunder directly overhead: the tear, the slam, then rolling returns that arrive
   late and dark because the far ones travelled further through air. */
function thunder(delay) {
  const d = delay || 0;
  noise(0.007, 1.0, 17000, 6500, d, 'highpass', 0.18);        /* the sky splitting */
  noise(0.055, 0.95, 9500, 1100, d + 0.004, 'highpass', 0.65);
  noise(0.55, 0.92, 3200, 80, d + 0.012, 'lowpass', 1.25);    /* the blast */
  tone(72, 1.3, 'sawtooth', 0.46, 24, d + 0.012);             /* the slam */
  tone(38, 2.6, 'sine', 0.44, 17, d + 0.02);                  /* the floor of it */
  [[0.17, 0.5, 950], [0.40, 0.44, 720], [0.72, 0.36, 540],
   [1.12, 0.29, 430], [1.66, 0.22, 340], [2.35, 0.16, 270], [3.15, 0.11, 210]]
    .forEach(([t, v, f]) => {
      noise(1.7, v, f, 45, d + t, 'lowpass', 0.85);
      tone(50 - t * 6, 1.9, 'sine', v * 0.34, 20, d + t);
    });
  noise(6, 0.15, 300, 32, d + 0.45, 'lowpass', 0.65);         /* the long roll away */
}

/* A choir on "ah", far off and rising. Vowels are made by resonances, so the voices
   are plain sawtooth run through the three formants that spell "ah" (about 730,
   1090 and 2440 Hz). Slow swell, slight vibrato, and a drift upward. */
function choirAh(delay, dur) {
  const c = ac(); if (!c || quiet()) return;
  const t0 = c.currentTime + (delay || 0), D = dur || 6;
  const bus = c.createGain();
  bus.gain.setValueAtTime(0.0001, t0);
  bus.gain.exponentialRampToValueAtTime(0.34, t0 + D * 0.5);   /* it arrives slowly */
  bus.gain.setValueAtTime(0.34, t0 + D * 0.66);
  bus.gain.exponentialRampToValueAtTime(0.0001, t0 + D);
  bus.connect(c.destination);

  const formants = [[730, 1.0], [1090, 0.5], [2440, 0.2]].map(([hz, amp]) => {
    const bp = c.createBiquadFilter();
    bp.type = 'bandpass'; bp.frequency.value = hz; bp.Q.value = 3.2;
    const g = c.createGain(); g.gain.value = amp * 7.5;   /* make up what the filters removed */
    bp.connect(g).connect(bus);
    return bp;
  });

  /* root, octave, fifth: an open chord reads as a crowd rather than a person */
  const VOICES = [98, 98.7, 147, 196, 196.9, 294, 392];
  VOICES.forEach((hz, i) => {
    const o = c.createOscillator();
    o.type = 'sawtooth';
    o.frequency.setValueAtTime(hz, t0);
    o.frequency.linearRampToValueAtTime(hz * 1.055, t0 + D);   /* the rise */
    const lfo = c.createOscillator(), lg = c.createGain();
    lfo.frequency.value = 4.3 + i * 0.27;
    lg.gain.value = hz * 0.007;
    lfo.connect(lg).connect(o.frequency);
    lfo.start(t0); lfo.stop(t0 + D + 0.2);
    const vg = c.createGain(); vg.gain.value = 0.5 / VOICES.length;
    o.connect(vg);
    formants.forEach(f => vg.connect(f));
    o.start(t0); o.stop(t0 + D + 0.2);
  });
}

const ALARM={osc:null,lfo:null,g:null,depth:null,
  start(level){
    const c=ac(); if(!c||quiet())return;
    const vol=[0,0,0,.055,.11,.2][level]||.2;
    if(!this.osc){
      /* two-tone klaxon: a square LFO swings the pitch, so it alternates by itself */
      this.osc=c.createOscillator(); this.osc.type='sawtooth';
      this.osc.frequency.value=520;
      this.lfo=c.createOscillator(); this.lfo.type='square'; this.lfo.frequency.value=0.62;
      this.depth=c.createGain(); this.depth.gain.value=95;
      this.lfo.connect(this.depth).connect(this.osc.frequency);
      const hp=c.createBiquadFilter(); hp.type='bandpass'; hp.frequency.value=760; hp.Q.value=1.1;
      this.g=c.createGain(); this.g.gain.value=0.0001;
      this.osc.connect(hp).connect(this.g).connect(c.destination);
      this.osc.start(); this.lfo.start();
    }
    const t=c.currentTime, cur=Math.max(0.0001,this.g.gain.value);
    const ramp=cur<0.002?.18:.7;      /* first blast must land on the click, not after it */
    this.g.gain.cancelScheduledValues(t);
    this.g.gain.setValueAtTime(cur,t);
    this.g.gain.exponentialRampToValueAtTime(vol,t+ramp);
    this.lfo.frequency.setValueAtTime(0.62+(level-3)*0.42,t);  /* slow to start, faster as it closes in */
  },
  stop(hard){
    const c=ac(); if(!c||!this.osc)return;
    const t=c.currentTime, o=this.osc,l=this.lfo,g=this.g;
    g.gain.cancelScheduledValues(t);
    g.gain.setValueAtTime(Math.max(0.0001,g.gain.value),t);
    g.gain.exponentialRampToValueAtTime(0.0001,t+(hard?.06:.3));
    o.stop(t+(hard?.09:.34)); l.stop(t+(hard?.09:.34));
    this.osc=null;this.lfo=null;this.g=null;
  }};
const SFX={
  warn(level){ ALARM.start(level); },
  shot(){                            /* the sixth: one round, and the whole valley hears it */
    ALARM.stop(true);
    /* 1. the crack. A supersonic round makes an N-wave: two transients a hair apart,
       almost all of it above 4kHz, and over before you can place it. */
    noise(.0022,1.0,19000,12000,0,'highpass',.12);
    noise(.0035,.92,15000,7000,.0026,'highpass',.2);
    /* 2. the muzzle blast, a beat behind, with the low end that makes it feel physical */
    noise(.018,1.0,7000,2200,.006,'highpass',.35);
    noise(.16,.9,2600,150,.008,'lowpass',1.1);
    tone(96,.28,'sawtooth',.5,38,.008);
    tone(52,.9,'sine',.44,22,.012);
    /* 3. returns off the terrain. Discrete and spaced, so the ear reads distance
       rather than a wash of static. Each one is darker: air eats the highs first. */
    [[.21,.52,2100],[.44,.40,1500],[.79,.30,1050],[1.24,.22,760],
     [1.83,.155,540],[2.55,.105,400],[3.4,.07,300]]
      .forEach(([d,v,f])=>{
        noise(.17,v,f,90,d,'bandpass',.45);
        tone(120,.38,'sine',v*.34,52,d);
      });
    /* 4. what is left hanging in the air */
    noise(3.2,.1,520,40,.35,'lowpass',.7);
    tone(34,3.6,'sine',.09,24,.36);
    /* 5. the case hits the floor a moment later */
    casing(.78);
  }};
/* the page does not simply change theme — it comes apart */
function breach(ox,oy,then){
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce){then();return;}
  const W=innerWidth,H=innerHeight,R=Math.hypot(W,H)*1.25;
  const el=document.createElement('div'); el.className='breach on';
  const NS='http://www.w3.org/2000/svg';
  const svg=document.createElementNS(NS,'svg'); svg.setAttribute('class','cracks');
  svg.setAttribute('viewBox','0 0 '+W+' '+H); svg.setAttribute('preserveAspectRatio','none');
  const N=11, a0=Math.random()*Math.PI*2, wedge=[];
  for(let i=0;i<N;i++){
    const a=a0+i*2*Math.PI/N+(Math.random()-.5)*.22;
    wedge.push(a);
    /* a jagged run outward, with one fork */
    let d='M'+ox+' '+oy, x=ox,y=oy;
    const steps=4+((Math.random()*3)|0);
    for(let k=1;k<=steps;k++){
      const t=R*k/steps, jit=(Math.random()-.5)*(58+t*.1);
      x=ox+Math.cos(a)*t-Math.sin(a)*jit; y=oy+Math.sin(a)*t+Math.cos(a)*jit;
      d+=' L'+x.toFixed(1)+' '+y.toFixed(1);
      if(k===2&&Math.random()<.6){
        const fa=a+(Math.random()<.5?-1:1)*(.34+Math.random()*.3), fl=R*(.4+Math.random()*.4);
        d+=' M'+x.toFixed(1)+' '+y.toFixed(1)+' L'+(x+Math.cos(fa)*fl).toFixed(1)+' '+(y+Math.sin(fa)*fl).toFixed(1)+' M'+x.toFixed(1)+' '+y.toFixed(1);
      }
    }
    /* two strokes: a dark casing so the crack reads on light themes, then the hot core */
    const wdt=1.4+Math.random()*2.2, dly=(Math.random()*70)+'ms';
    const cas=document.createElementNS(NS,'path');
    cas.setAttribute('class','crack case'); cas.setAttribute('d',d);
    cas.setAttribute('stroke-width',(wdt+3.4).toFixed(1));
    cas.style.setProperty('--len',R*1.9); cas.style.animationDelay=dly;
    svg.appendChild(cas);
    const pth=document.createElementNS(NS,'path');
    pth.setAttribute('class','crack'); pth.setAttribute('d',d);
    pth.setAttribute('stroke-width',wdt.toFixed(1));
    pth.style.setProperty('--len',R*1.9); pth.style.animationDelay=dly;
    svg.appendChild(pth);
  }
  el.appendChild(svg);
  const hole=document.createElement('div'); hole.className='hole';
  hole.style.left=ox+'px'; hole.style.top=oy+'px';
  hole.innerHTML='<i></i><b></b>'; el.appendChild(hole);
  const flash=document.createElement('div'); flash.className='flash'; el.appendChild(flash);
  /* the page splits along those cracks */
  wedge.sort((a,b)=>a-b);
  for(let i=0;i<N;i++){
    const a1=wedge[i], a2=wedge[(i+1)%N]+(i===N-1?2*Math.PI:0), mid=(a1+a2)/2;
    const px=(a,r)=>[(ox+Math.cos(a)*r).toFixed(1)+'px',(oy+Math.sin(a)*r).toFixed(1)+'px'].join(' ');
    const sh=document.createElement('div'); sh.className='shard';
    sh.style.clipPath='polygon('+ox+'px '+oy+'px,'+px(a1,R)+','+px(mid,R)+','+px(a2,R)+')';
    sh.style.setProperty('--dx',(Math.cos(mid)*(W*.42)).toFixed(0)+'px');
    sh.style.setProperty('--dy',(Math.sin(mid)*(H*.5)).toFixed(0)+'px');
    sh.style.setProperty('--rot',((Math.random()-.5)*26).toFixed(1)+'deg');
    sh.style.animationDelay=(70+Math.random()*90)+'ms';
    el.appendChild(sh);
  }
  const vd=document.createElement('div'); vd.className='void'; el.appendChild(vd);
  document.body.appendChild(el);
  document.body.classList.add('breaching');
  setTimeout(()=>flash.classList.add('go'),150);
  setTimeout(()=>{$$('.breach .shard').forEach(x=>x.classList.add('go'));},240);
  setTimeout(()=>vd.classList.add('in'),430);
  setTimeout(()=>{document.body.classList.remove('breaching');
    svg.remove(); then();},950);
  setTimeout(()=>vd.classList.remove('in'),1180);
  setTimeout(()=>el.remove(),1780);
}
if(unlocked())revealSecret();
(function(){                       /* a verdict, freely given */
  let buf='';
  addEventListener('keydown',e=>{
    if(e.metaKey||e.ctrlKey||e.altKey)return;
    const tg=e.target; if(tg&&/^(INPUT|TEXTAREA|SELECT)$/.test(tg.tagName))return;
    if(e.key.length!==1)return;
    buf=(buf+e.key.toLowerCase()).slice(-24);
    if(buf.endsWith('cossu')){buf='';botCall();}
    if(buf.endsWith('chaos')){buf='';chaos();}
    /* first name or surname, either will do. Burke is surname-only on purpose: "brian"
       belongs to the commissioner, and there are two of them in this league. */
    /* the champion goes FIRST: the loop breaks on the first match, so if a manager who
       already has a card of their own wins the title, their own entry would otherwise
       shadow the title defence for the whole of their reign */
    const EGGWORDS=[
      [CHAMP_KEYS,titleDefense],
      [['burke'],pandaWatch],
      [['kaiper','shane'],stillStomping],
      [['wu','nathan'],wuSeal],
      [['gearing','nick'],fieldLevel],
      [['niko','contreras'],marquee],
      [['alpert','wesley'],marketClose],
      [['mcmahon','dylan'],wrongSport],
      ];
    if(eggOpen())return;
    for(const [words,fn] of EGGWORDS)
      if(words.some(w=>buf.endsWith(w))){buf='';fn();break;}
  });
})();
/* Typing the reigning champion's surname wakes him up. The trigger comes from the data
   rather than a hardcoded name, so it follows the trophy: whoever holds it this year is
   who the page answers to. Co-champion years arm both surnames. */
const CHAMP_NOW=(D.champs||[]).filter(c=>c.y===LAST)[0]||null;
/* every part of the champion's name that is long enough to type on purpose, so the card
   answers to a first name as well as a surname, the same as the other eight */
const CHAMP_KEYS=CHAMP_NOW
  ?[...new Set(CHAMP_NOW.mgrs.flatMap(n=>String(n).trim().toLowerCase().split(/\s+/)))]
    .filter(k=>k.length>=4)
  :[];
function titleDefense(){
  if(!CHAMP_NOW||$('.kdef'))return;
  const team=CHAMP_NOW.teams[0], mgrs=CHAMP_NOW.mgrs.join(' & ');
  /* the joke only lands for the team that earned it; every other year gets the plain line */
  const sub=/^hench$/i.test(team)?'which makes you his henchman'
    :(CHAMP_NOW.co?'and the other half of it is still out there':'the rest of you are playing for second');
  const el=document.createElement('div'); el.className='kdef';
  el.innerHTML='<div class="kd-in"><div class="kd-ray"></div>'
    +'<div class="kd-tag">'+(LAST+1)+' &nbsp;T I T L E &nbsp; D E F E N S E</div>'
    +'<div class="kd-l1">'+esc(team.toUpperCase())+'</div>'
    +'<div class="kd-l2">HAS BEGUN '+(CHAMP_NOW.co?'THEIR':'HIS')+' TITLE DEFENSE</div>'
    +'<div class="kd-sub">'+esc(sub)+'</div>'
    +'<div class="kd-mgr">'+esc(mgrs.toUpperCase())+' &middot; CHAMPION '+LAST+'</div></div>';
  document.body.appendChild(el);
  const c=ac();
  safeSFX(()=>battleReady(0));
  const off=()=>{el.classList.add('out');setTimeout(()=>el.remove(),700);};
  el.addEventListener('click',off);
  setTimeout(off,5250);
}


/* ---- four voices, all synthesised ------------------------------------------- */





/* Two independent keydown listeners watch for typed words, so a full name like
   "brian burke" could trip a manager card and the commissioner at the same time and stack
   two full-screen overlays. Both check here first. */
const EGG_SELS='.kdef,.pnda,.jrsc,.nwu,.gr49,.mrqe,.tkr,.hoop,.botcall';
function eggOpen(){
  try{ return !!document.querySelector(EGG_SELS)||(typeof PH_BUSY!=='undefined'&&PH_BUSY); }
  catch(e){ return false; }
}

/* An easter egg's sound is decoration. It must never be able to strand the overlay it
   belongs to, so every card plays through here and nothing it does can escape. */
function safeSFX(fn){ try{ if(ac()&&!quiet())fn(); }catch(e){} }

/* ---- the two men who have never missed a season -------------------------------
   Brian Burke, Shane Kaiper and the owner are the only three who have played all ten.
   Every number in both cards is read from the record, so they cannot go stale. */
function loyalFacts(name){
  const m=byName[name]; if(!m)return null;
  const rs=ROWS.filter(r=>r.mgr===name).sort((a,b)=>a.y-b.y);
  if(!rs.length)return null;
  /* how long they have run under the name they use now */
  let run=1;
  for(let i=rs.length-1;i>0;i--){ if(rs[i-1].team===rs[i].team)run++; else break; }
  return {m:m,rs:rs,team:rs[rs.length-1].team,run:run,
          all:m.seasons===SEA.length,
          first:rs[0].y,last:rs[rs.length-1].y};
}
function pandaWatch(){
  const F=loyalFacts('Brian Burke'); if(!F||$('.pnda'))return;
  const el=document.createElement('div'); el.className='pnda';
  el.innerHTML='<div class="pn-in">'
    +'<div class="pn-face"><span class="ear l"></span><span class="ear r"></span>'
    +'<span class="head"><span class="eye l"><i></i></span><span class="eye r"><i></i></span>'
    +'<span class="nose"></span></span></div>'
    +'<div class="pn-tag">T H E R E &nbsp; A R E &nbsp; N O &nbsp; A C C I D E N T S</div>'
    +'<div class="pn-l1">BRIAN BURKE</div>'
    +'<div class="pn-l2">'+F.m.seasons+' SEASONS OF '+SEA.length+'</div>'
    +'<div class="pn-sub">'+(F.all?'never missed a year, never missed by much'
        :'back for more, and never missed by much')+'</div>'
    +'<div class="pn-facts">'+F.first+'&ndash;'+F.last+' &middot; '+F.m.apps+' OF '+F.m.seasons
      +' IN THE BRACKET &middot; INDEX '+F.m.cpi.toFixed(1)+' &middot; SWING &plusmn;'
      +(F.m.sd==null?'—':F.m.sd.toFixed(1))+'</div></div>';
  document.body.appendChild(el);
  safeSFX(()=>{                          /* two hollow knocks on bamboo */
    ping(392,.55,.075,0,1); ping(330,.7,.065,.20,1);
    tone(98,.7,'triangle',.10,80,0);
  });
  const off=()=>{el.classList.add('out');setTimeout(()=>el.remove(),700);};
  el.addEventListener('click',off);
  setTimeout(off,5250);
}
/* Chinese numerals for the seal. Only ever fed a season count, so ten covers it. */
const CN_NUM=['','\u4E00','\u4E8C','\u4E09','\u56DB','\u4E94','\u516D','\u4E03','\u516B','\u4E5D','\u5341'];

/* A full stand, not static. Cheering is voices, so it is built from a lot of short
   band-limited bursts at slightly different pitches on top of a bed that swells and
   falls, rather than from one long hiss. */
function fansCheer(delay){
  const c=ac(); if(!c||quiet())return;
  const d=delay||0;
  /* Not one pitched note anywhere in here. Any oscillator in a crowd reads as a machine
     -- the first attempt had a handful of sawtooths meant as voices and they came back
     sounding like an arcade cabinet. A crowd is broadband noise, a great deal of it,
     overlapping at every scale. */
  noise(3.2,0.30,1600,700,d,'bandpass',0.26);
  noise(3.0,0.24,900,380,d+0.06,'bandpass',0.40);
  noise(2.8,0.20,420,150,d+0.03,'bandpass',0.52);
  noise(2.6,0.17,240,90,d+0.02,'lowpass',0.62);
  /* the sections of the ground, coming in a beat apart from each other */
  [[0.00,1300],[0.18,1750],[0.34,1000],[0.55,2100]].forEach(([t,f])=>
    noise(2.0+Math.random()*0.6,0.16,f,f*0.4,d+t,'bandpass',0.34));
  /* and a great many individual voices, uneven in length, loudness and colour */
  for(let i=0;i<170;i++){
    const t=d+Math.random()*2.6;
    const f=620+Math.random()*1900;
    noise(0.06+Math.random()*0.20,0.030+Math.random()*0.055,f,f*(0.35+Math.random()*0.4),
      t,'bandpass',0.35+Math.random()*0.7);
  }
}

/* Bracing for a defence: three war drums, a horn climbing a triad, and the whole thing
   locking into place on the top note. Triumphant, but planted rather than celebrating. */
function battleReady(delay){
  const d=delay||0;
  [0,0.26,0.50].forEach((t,i)=>{               /* the drums */
    tone(58-i*4,0.34,'sine',0.30+i*0.03,38,d+t);
    noise(0.18,0.11,320,70,d+t,'lowpass',0.8);
  });
  /* the horn: a fifth, then the octave, then both held together */
  [[0.52,147],[0.72,196],[0.92,294]].forEach(([t,f])=>{
    tone(f,1.5,'sawtooth',0.085,f,d+t);
    tone(f*0.5,1.5,'triangle',0.065,f*0.5,d+t);
  });
  tone(392,1.35,'sawtooth',0.055,392,d+1.06);   /* the answer on top */
  noise(0.5,0.06,2600,700,d+1.06,'bandpass',0.7);
  tone(49,2.0,'sine',0.16,40,d+0.9);            /* the floor it stands on */
}

/* A long, soft gong under a plucked pentatonic figure: the strike, then the room, then
   somebody playing quietly in it. Nothing lands on a beat, so it never becomes a jingle. */
function villageCalm(delay){
  const c=ac(); if(!c||quiet())return;
  const d=delay||0, t0=c.currentTime+d, D=7.5;
  /* the gong, slower to bloom and much slower to go than a struck bell */
  const PART=[1,1.52,2.14,2.71,3.46,4.35,5.62,7.11];
  PART.forEach((m,i)=>{
    const o=c.createOscillator(), g=c.createGain();
    o.type='sine'; o.frequency.setValueAtTime(72*m,t0);
    o.frequency.linearRampToValueAtTime(72*m*0.982,t0+D);
    const v=0.115*Math.pow(0.74,i), bloom=0.09+i*0.05;
    g.gain.setValueAtTime(0.0001,t0);
    g.gain.exponentialRampToValueAtTime(Math.max(0.0004,v),t0+bloom);
    g.gain.exponentialRampToValueAtTime(0.0001,t0+D*Math.pow(0.9,i));
    o.connect(g).connect(c.destination); o.start(t0); o.stop(t0+D+0.1);
  });
  noise(0.09,0.10,5200,800,d,'bandpass',0.5);      /* the mallet */
  noise(3.4,0.035,1400,180,d+0.05,'lowpass',1.6);  /* the air in the room */

  /* a plucked pentatonic line -- sharp attack, long decay, a touch of bend on the way
     out, which is what a stopped string does */
  const SCALE=[262,294,330,392,440,523,587,659];
  const FIG=[[0.55,0],[0.95,2],[1.30,3],[1.80,4],[2.35,5],[2.85,3],[3.40,4],[4.05,2],[4.75,0],[5.60,5]];
  FIG.forEach(([t,k],i)=>{
    const f=SCALE[k], s=t0+t;
    [1,2.01,3.02].forEach((h,hi)=>{               /* a string is not a sine */
      const o=c.createOscillator(), g=c.createGain();
      o.type=hi?'sine':'triangle';
      o.frequency.setValueAtTime(f*h,s);
      o.frequency.linearRampToValueAtTime(f*h*(hi===0?1.004:1),s+0.10);
      const v=(0.075*Math.pow(0.45,hi))*(i%3===0?1:0.8);
      g.gain.setValueAtTime(0.0001,s);
      g.gain.exponentialRampToValueAtTime(v,s+0.006);
      g.gain.exponentialRampToValueAtTime(0.0001,s+1.5*Math.pow(0.7,hi));
      o.connect(g).connect(c.destination); o.start(s); o.stop(s+1.7);
    });
  });
  /* a drone a fifth under it, so the figure has something to sit on */
  [131,196].forEach((f,i)=>{
    const o=c.createOscillator(), g=c.createGain();
    o.type='sine'; o.frequency.value=f;
    g.gain.setValueAtTime(0.0001,t0+0.3);
    g.gain.exponentialRampToValueAtTime(0.030-i*0.008,t0+1.6);
    g.gain.setValueAtTime(0.030-i*0.008,t0+4.2);
    g.gain.exponentialRampToValueAtTime(0.0001,t0+D);
    o.connect(g).connect(c.destination); o.start(t0+0.3); o.stop(t0+D+0.1);
  });
}

/* ---- three more, all argued straight out of the record ---------------------- */

/* A projector running. A real one pulls 24 frames a second, so the clatter is a 24Hz
   pulse train rather than a rhythm you could count -- that fast tick is the whole sound.
   Under it: the motor, and the hiss of the film going through the gate. */
function filmRoll(delay){
  /* The card is up for 5250ms and then fades for 700. The reel should still be running
     when it starts to go, so this covers 5.4s and the motor's own decay carries it into
     the fade rather than stopping dead two seconds early. */
  const d=delay||0, RATE=1/24, RUN=5.4, N=Math.round(RUN/RATE);
  for(let i=0;i<N;i++){
    const t=d+i*RATE+Math.random()*0.0025;   /* never perfectly even, never negative */
    noise(0.010,0.055+Math.random()*0.02,3000,1100,t,'bandpass',0.45);
    noise(0.016,0.030,900,320,t,'lowpass',0.7);
  }
  tone(48,RUN+0.5,'sawtooth',0.055,47,d);          /* the motor */
  tone(96,RUN+0.5,'triangle',0.028,95,d);
  noise(RUN+0.5,0.045,4200,2600,d,'highpass',1.4); /* film through the gate */
  noise(0.5,0.08,1600,400,d,'lowpass',0.6);        /* the lamp striking */
}
/* A closing bell, then the number falling away under it. */
function closeBell(delay){
  const d=delay||0;
  ping(1976,1.7,0.10,d,1); ping(2637,1.4,0.07,d+0.02,1);
  [0,1,2,3].forEach(i=>tone(330*Math.pow(0.84,i),0.34,'triangle',0.055,
    280*Math.pow(0.84,i),d+0.75+i*0.16));
  tone(48,1.8,'sine',0.11,36,d+0.75);
}
/* Three bounces closing up, then the net. */
/* A ball on a hardwood floor. The first version used a sine per bounce and came out
   like a game console: a real bounce has no note in it at all. It is a broadband slap
   that collapses downward in about forty milliseconds, plus the room answering. */
function bounce(t,v){
  noise(0.040,0.34*v,2600,190,t,'lowpass',3.2);      /* the slap of the skin */
  noise(0.075,0.26*v,520,90,t+0.004,'lowpass',2.4);  /* the air inside it */
  noise(0.20,0.055*v,300,80,t+0.012,'lowpass',1.1);  /* the floor and the room */
  noise(0.012,0.12*v,7000,3000,t,'highpass',0.5);    /* the click of the seam */
}
function swish(delay){
  const d=delay||0;
  /* bounces converge the way a dropped ball actually does, and get quieter with it */
  let t=d, gap=0.42, v=1;
  for(let i=0;i<6;i++){ bounce(t,v); t+=gap; gap*=0.80; v*=0.74; }
  /* picked up, then through the net */
  noise(0.30,0.085,5200,1800,t+0.14,'bandpass',0.5);
  noise(0.18,0.05,3000,1100,t+0.20,'bandpass',0.75);
}

/* Niko has two titles back to back, and the second came with a worse team than the
   first -- which is a film joke that happens to be true, so the card checks it. */
function marquee(){
  const F=loyalFacts('Niko Contreras'); if(!F||$('.mrqe'))return;
  const m=F.m;
  const wins=F.rs.filter(r=>r.place===1).sort((a,b)=>a.y-b.y);
  const backToBack=wins.length>1&&SEA.indexOf(wins[1].y)===SEA.indexOf(wins[0].y)+1;
  const worseSequel=wins.length>1&&wins[1].pi<wins[0].pi;
  const last=F.rs[F.rs.length-1];
  /* a marquee bills the picture, not the person: the title goes up in lights and the
     director takes a credit underneath it */
  const title=backToBack?'BACK 2 BACK'
    :(wins.length?(wins.length===1?'ONE FOR THE SHELF':wins.length+' FOR THE SHELF'):'NO STATUE YET');
  const l2=backToBack
    ? wins[0].y+' &amp; '+wins[1].y+' &middot; HELD OVER A SECOND YEAR'
    :(wins.length?wins.map(w=>w.y).join(' &amp; '):m.seasons+' SEASONS, STILL RUNNING');
  /* the second one is the story: it was the lowest score that has ever won this league,
     which is a robbery rather than a repeat. Checked against every champion before it
     gets said. */
  const champPI=[];
  D.champs.forEach(c=>c.teams.forEach(t=>{
    const r=ROWS.find(x=>x.y===c.y&&x.team===t); if(r)champPI.push(r.pi);}));
  const lowestEver=champPI.length?Math.min(...champPI):null;
  const heist=wins.length>1&&lowestEver!=null&&Math.abs(wins[1].pi-lowestEver)<0.05;
  const sub=heist
    ? 'the second one was a robbery — '+wins[1].pi.toFixed(1)+', the lowest score that has ever won this league'
    : worseSequel
    ? 'the sequel scored worse than the original — '+wins[0].pi.toFixed(1)+' then '+
      wins[1].pi.toFixed(1)+' — and still took the trophy'
    : 'nobody in this league has more of them';
  /* the small print at the bottom of a poster: the run, the takings, the reviews, and
     how it finished. Every figure comes out of the record. */
  const bill=[];
  bill.push(F.first+'&ndash;'+F.last);
  bill.push(m.seasons+' SEASONS');
  bill.push(m.w+'&ndash;'+m.l+(m.t?'&ndash;'+m.t:''));
  if(wins.length)bill.push(wins.map(w=>w.pi.toFixed(1)).join(' THEN ')+' IN THE TITLE YEARS');
  bill.push(m.podium+' PODIUM'+(m.podium===1?'':'S'));
  bill.push('FINAL SCREENING '+last.y+', '+ord(last.place)+' OF '+last.teams);
  const billing=bill.join(' &middot; ');
  const el=document.createElement('div'); el.className='mrqe';
  const bulbs='<i></i>'.repeat(11);
  el.innerHTML='<div class="mq-in">'
    +'<div class="mq-bulbs t">'+bulbs+'</div><div class="mq-bulbs b">'+bulbs+'</div>'
    +'<div class="mq-tag">N O W &nbsp; S H O W I N G</div>'
    +'<div class="mq-l1">'+title+'</div>'
    +'<div class="mq-dir">Dir. by '+esc(m.name)+'</div>'
    +'<div class="mq-rule"></div>'
    +'<div class="mq-l2" style="font-size:clamp(16px,3.2vw,32px);margin-top:12px">'+l2+'</div>'
    +'<div class="mq-sub">'+sub+'</div>'
    +'<div class="mq-facts">'+billing+'</div></div>';
  document.body.appendChild(el);
  safeSFX(()=>filmRoll(0));
  const off=()=>{el.classList.add('out');setTimeout(()=>el.remove(),700);};
  el.addEventListener('click',off);
  setTimeout(off,5250);
}

/* Wesley's five seasons make a straight line down, and he has never once won. The card
   plots the line rather than describing it. Every superlative is checked against the
   field first, because he is the best of the active managers and not of all of them. */
function marketClose(){
  const F=loyalFacts('Wesley Alpert'); if(!F||$('.tkr'))return;
  const m=F.m, rs=F.rs, pis=rs.map(r=>r.pi);
  const W=420,H=118,P=14;
  const lo=Math.min(...pis)-3, hi=Math.max(...pis)+3;
  const xs=i=>P+i*(W-P*2)/Math.max(1,pis.length-1);
  const ys=v=>P+(hi-v)*(H-P*2)/(hi-lo);
  const d=pis.map((v,i)=>(i?'L':'M')+xs(i).toFixed(1)+','+ys(v).toFixed(1)).join(' ');
  const dots=pis.map((v,i)=>`<circle cx="${xs(i).toFixed(1)}" cy="${ys(v).toFixed(1)}" r="${i===pis.length-1?5:3.4}"
    fill="#06100D" stroke="${i===pis.length-1?'#E4453C':'#3FD07A'}" stroke-width="2.4"
    ${i===pis.length-1?'class="tk-dot"':''}/>`).join('');
  const labs=`<text x="${xs(0)}" y="${ys(pis[0])-11}" font-size="11" fill="#5FD497"
      font-family="IBM Plex Mono,monospace">${pis[0].toFixed(1)}</text>
    <text x="${xs(pis.length-1)}" y="${ys(pis[pis.length-1])+20}" text-anchor="end" font-size="11"
      fill="#E4453C" font-family="IBM Plex Mono,monospace">${pis[pis.length-1].toFixed(1)}</text>`;
  /* the decline is checked, not asserted: mgrSlide returns 0 the moment a season goes up */
  const decl=mgrSlide(m);
  const active=M.filter(x=>x.last===LAST&&x.seasons>=3);
  const topActive=active.length&&active.slice().sort((a,b)=>b.cpi-a.cpi)[0].name===m.name;
  const qual=M.filter(x=>x.g>=40);
  const bestRate=qual.length&&qual.slice().sort((a,b)=>b.winpct-a.winpct)[0].name===m.name;
  const claim=bestRate?'the best win rate in league history'
    :topActive?'the highest rating of anyone still playing':'a rating near the top of the league';
  const el=document.createElement('div'); el.className='tkr';
  el.innerHTML='<div class="tk-in">'
    +'<div class="tk-chart"><svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Wesley Alpert\'s power index, falling every season">'
      +'<path d="'+d+'" fill="none" stroke="#E4453C" stroke-width="2.6" stroke-linejoin="round"/>'
      +dots+labs+'</svg></div>'
    +'<div class="tk-tag">M A R K E T &nbsp; C L O S E</div>'
    +'<div class="tk-l1">WESLEY ALPERT</div>'
    +'<div class="tk-l2">'+(decl?'DOWN '+(['','ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT'][decl]||decl)+' STRAIGHT':'THE LONG WAY DOWN')+'</div>'
    +'<div class="tk-sub">'+claim+(decl?', and it has fallen in every season since his first':'')+'</div>'
    +'<div class="tk-facts">'+F.first+'&ndash;'+F.last+' &middot; '+m.w+'&ndash;'+m.l+(m.t?'&ndash;'+m.t:'')
      +' ('+pct(m.winpct)+') &middot; '+m.second+' SECOND PLACES &middot; '
      +(m.titles?m.titles+' TITLES':'NO TITLE')+'</div></div>';
  document.body.appendChild(el);
  safeSFX(()=>closeBell(0));
  const off=()=>{el.classList.add('out');setTimeout(()=>el.remove(),700);};
  el.addEventListener('click',off);
  setTimeout(off,5250);
}

/* League lore says McMahon is unguardable on a court. The record says the scoring was
   never his problem either -- he cleared the league average and still lost. */
function wrongSport(){
  const F=loyalFacts('Dylan McMahon'); if(!F||$('.hoop'))return;
  const m=F.m, rs=F.rs;
  const best=rs.reduce((a,b)=>b.pi>a.pi?b:a);
  const above=best.pi>100;
  const rank=M.slice().sort((a,b)=>a.luck-b.luck).findIndex(x=>x.name===m.name)+1;
  const el=document.createElement('div'); el.className='hoop';
  el.innerHTML='<div class="hp-in"><div class="hp-court"></div>'
    +'<div class="hp-ball"><span class="hp-seam"></span></div>'
    +'<div class="hp-tag">W R O N G &nbsp; S P O R T</div>'
    +'<div class="hp-l1">DYLAN McMAHON</div>'
    +'<div class="hp-l2">GIVE HIM A BASKETBALL INSTEAD</div>'
    +'<div class="hp-sub">'+(above
        ? 'right idea, bad execution &mdash; cleared the league average in '+best.y
          +' and still finished '+best.w+'&ndash;'+best.l
        : 'right idea, bad execution')+'</div>'
    +'<div class="hp-facts">'+m.seasons+' SEASONS &middot; '+m.w+'&ndash;'+m.l+(m.t?'&ndash;'+m.t:'')
      +' &middot; LUCK '+(m.luck>=0?'+':'&minus;')+Math.abs(m.luck).toFixed(2)
      +(rank<=3?' &middot; '+ord(rank)+' UNLUCKIEST':'')
      +' &middot; '+(m.apps?m.apps+' IN THE BRACKET':'NO BRACKET YET')+'</div></div>';
  document.body.appendChild(el);
  safeSFX(()=>swish(0));
  const off=()=>{el.classList.add('out');setTimeout(()=>el.remove(),700);};
  el.addEventListener('click',off);
  setTimeout(off,5250);
}

function wuSeal(){
  const F=loyalFacts('Nathan Wu'); if(!F||$('.nwu'))return;
  const m=F.m, n=m.seasons;
  const el=document.createElement('div'); el.className='nwu';
  el.innerHTML='<div class="wu-in">'
    +'<div class="wu-seal"><span>'+(CN_NUM[n]||n)+'</span></div>'
    +'<div class="wu-tag">S E A L E D &nbsp; A N D &nbsp; S T A M P E D</div>'
    +'<div class="wu-l1">NATHAN WU</div>'
    +'<div class="wu-l2">'+m.podium+' TIMES ON THE PODIUM, '+(m.titles?m.titles:'NONE')+' ON THE TOP STEP</div>'
    +'<div class="wu-sub">'+n+' seasons, '+m.apps+' of them in the bracket, and still no ring to show for it</div>'
    +'<div class="wu-facts">'+F.first+'&ndash;'+F.last+' &middot; '+m.w+'&ndash;'+m.l+(m.t?'&ndash;'+m.t:'')
      +' &middot; INDEX '+m.cpi.toFixed(1)+' &middot; PEAK '+m.peak.toFixed(1)+'</div></div>';
  document.body.appendChild(el);
  safeSFX(()=>villageCalm(0));
  const off=()=>{el.classList.add('out');setTimeout(()=>el.remove(),700);};
  el.addEventListener('click',off);
  setTimeout(off,5250);
}
/* Nick keeps a seat at pitch level at Levi's, one of twenty the 49ers put down there in
   the 2026 rebuild, so his card is scarlet and gold and standing on the grass. */
function fieldLevel(){
  const F=loyalFacts('Nick Gearing'); if(!F||$('.gr49'))return;
  const m=F.m, ty=ROWS.filter(r=>r.mgr==='Nick Gearing'&&r.place===1).map(r=>r.y);
  const el=document.createElement('div'); el.className='gr49';
  el.innerHTML='<div class="gr-in"><div class="gr-turf"></div>'
    +'<div class="gr-tag">F I E L D &nbsp; L E V E L &nbsp;&middot;&nbsp; L E V I &rsquo; S</div>'
    +'<div class="gr-l1">NICK GEARING</div>'
    +'<div class="gr-l2">CLOSE ENOUGH TO HEAR THE SNAP COUNT</div>'
    +'<div class="gr-sub">a seat on the grass in Santa Clara, and '
      +(ty.length?'a ring from '+ty.join(' and '):'still chasing a ring')+' in this one</div>'
    +'<div class="gr-facts">'+F.first+'&ndash;'+F.last+' &middot; '+m.seasons+' SEASONS &middot; '
      +m.w+'&ndash;'+m.l+(m.t?'&ndash;'+m.t:'')+' &middot; '+m.apps+' OF '+m.seasons+' IN THE BRACKET</div></div>';
  document.body.appendChild(el);
  safeSFX(()=>fansCheer(0));
  const off=()=>{el.classList.add('out');setTimeout(()=>el.remove(),700);};
  el.addEventListener('click',off);
  setTimeout(off,5250);
}
function stillStomping(){
  const F=loyalFacts('Shane Kaiper'); if(!F||$('.jrsc'))return;
  const el=document.createElement('div'); el.className='jrsc';
  el.innerHTML='<div class="jr-in">'
    +'<div class="jr-rip"></div><div class="jr-rip"></div><div class="jr-rip"></div>'
    +'<div class="jr-tag">T R E M O R &nbsp; D E T E C T E D</div>'
    +'<div class="jr-l1">'+esc(F.team.toUpperCase())+'</div>'
    +'<div class="jr-l2">'+F.m.seasons+' SEASONS. STILL STOMPING.</div>'
    +'<div class="jr-sub">'+F.run+' straight seasons under the same ancient name, and the ground still moves</div>'
    +'<div class="jr-facts">SHANE KAIPER &middot; '+F.first+'&ndash;'+F.last+' &middot; '
      +F.m.w+'&ndash;'+F.m.l+(F.m.t?'&ndash;'+F.m.t:'')
      +(F.all?' &middot; NEVER ONCE ABSENT':' &middot; '+F.m.seasons+' OF '+SEA.length+' SEASONS')+'</div></div>';
  document.body.appendChild(el);
  safeSFX(()=>{             /* three footfalls, getting closer */
    tone(41,.55,'sine',.34,30,0);   noise(.30,.13,240,40,0,'lowpass',.9);
    tone(44,.6,'sine',.38,31,.62);  noise(.34,.16,260,42,.62,'lowpass',.9);
    tone(39,.7,'sine',.40,29,1.20); noise(.38,.17,250,40,1.20,'lowpass',.9);
  });
  const off=()=>{el.classList.add('out');setTimeout(()=>el.remove(),700);};
  el.addEventListener('click',off);
  setTimeout(off,5250);
}
let CH_BUSY=false;
function chaos(){
  if(CH_BUSY)return; CH_BUSY=true;
  const els=[...document.querySelectorAll('td.num,td.mono,.tile b,.lad-s,.lad-w,.hlc .v,.fact b,.plate .yr')]
    .filter(e=>e.offsetParent!==null && /\d/.test(e.textContent)).slice(0,700);
  const orig=els.map(e=>e.innerHTML);
  const scr=t=>t.replace(/\d/g,()=>String.fromCharCode(48+Math.floor(Math.random()*10)));
  /* the charts come apart with the numbers */
  const svgs=[...document.querySelectorAll('.chart svg,.card-b svg,#race svg,.spark svg')].filter(e=>e.offsetParent!==null).slice(0,14);
  const shapes=[];
  svgs.forEach(sv=>{[...sv.querySelectorAll('circle,rect,path,line,polyline,polygon,text,g')]
    .filter(e=>!e.querySelector('circle,rect,path,line,polyline,polygon,text'))
    .slice(0,260).forEach(e=>shapes.push([e,e.getAttribute('transform')]));});
  const rnd=a=>(Math.random()*2-1)*a;
  /* html bars distort too */
  const bars=[...document.querySelectorAll('.dbar i,.lad-bar i,.lad-bar span,.barline i')]
    .filter(e=>e.offsetParent!==null).slice(0,240).map(e=>[e,e.style.width,e.style.left,e.style.transform]);
  const jolt=k=>{
    shapes.forEach(([e,t0])=>{
      const a=k*(0.35+Math.random()*0.9);
      e.setAttribute('transform',(t0?t0+' ':'')+`translate(${rnd(a*1.5).toFixed(1)},${rnd(a*2.2).toFixed(1)}) rotate(${rnd(a*0.5).toFixed(1)})`);});
    bars.forEach(([e,w])=>{
      const base=parseFloat(w)||0, span=Math.min(46,k*3.4);
      e.style.width=Math.max(0.6,base+rnd(span)).toFixed(1)+'%';
      e.style.transform=`translateY(${rnd(k*0.5).toFixed(1)}px)`;});
  };
  const settleShapes=()=>{
    shapes.forEach(([e,t0])=>{if(t0===null)e.removeAttribute('transform');else e.setAttribute('transform',t0);});
    bars.forEach(([e,w,l,tr])=>{e.style.width=w;e.style.left=l;e.style.transform=tr;});
  };
  document.body.classList.add('chaosing');
  const ov=document.createElement('div'); ov.className='chaosov';
  ov.innerHTML='<div class="ch-msg"><span>THE RECORDS DO NOT LIE</span></div>';
  document.body.appendChild(ov);
  const c=ac();
  if(c&&!quiet()){
    for(let i=0;i<26;i++)tone(300+Math.random()*2400,.05,'square',.012,300,i*.06);
    noise(.4,.1,4000,300,1.35);
    tone(220,.9,'sine',.09,110,1.4); tone(330,.9,'sine',.07,165,1.42);
  }
  let n=0;
  const tick=()=>{
    n++;
    els.forEach((e,i)=>{e.innerHTML=scr(orig[i]);});
    jolt(Math.max(1.5,14-n*0.6));
    if(n<20)setTimeout(tick,40+n*4); else finish();
  };
  const finish=()=>{
    els.forEach((e,i)=>{e.innerHTML=orig[i];});
    settleShapes();
    ov.classList.add('settle');
    setTimeout(()=>{ov.remove();document.body.classList.remove('chaosing');CH_BUSY=false;},1500);
  };
  tick();
}
function botCall(){
  if($('.botcall'))return;
  const el=document.createElement('div'); el.className='botcall';
  el.innerHTML='<div class="bc-in"><div class="bc-scan"></div>'
    +'<div class="bc-tag">ANALYSIS COMPLETE</div>'
    +'<div class="bc-l1">COSSU</div><div class="bc-l2">IS A BOT</div>'
    +'<div class="bc-sub">confidence 99.97% &middot; no further questions</div>'
    +'<div class="bc-bits">01000010 01001111 01010100</div></div>';
  document.body.appendChild(el);
  const c=ac(); if(c&&!quiet()){
    [880,1174,1568].forEach((fq,i)=>tone(fq,.09,'square',.05,fq,i*.1));
    tone(120,.5,'square',.06,60,.32);
    noise(.3,.05,3000,400,.32);
  }
  setTimeout(()=>el.classList.add('out'),3250);
  setTimeout(()=>el.remove(),4050);
}

/* or six rounds through the reticle — and the building notices */
(function(){const sc=$('.mast .scope'); if(!sc)return;
  const om=document.createElement('div'); om.className='omen'; document.body.appendChild(om);
  const LINE=[null,null,null,
    ['UNAUTHORIZED ACCESS DETECTED','sector 03 · terminal unknown'],
    ['TRACE INITIATED','something is following the signal back'],
    ['FINAL WARNING','one more and you take the shot']];
  let n=0,t=null;
  const stand=()=>{n=0;om.className='omen';sc.classList.remove('hot');document.body.classList.remove('quake');
    $('#toast').classList.remove('on','warn'); ALARM.stop();};
  sc.addEventListener('click',()=>{
    const c=ac(); if(c&&c.state==='suspended')c.resume();   /* warm it on click 1, silently */
    n++; clearTimeout(t); t=setTimeout(stand,3400);
    if(n>=6){clearTimeout(t);
      const r=sc.getBoundingClientRect();
      stand();
      SFX.shot();
      breach(r.left+r.width/2,r.top+r.height/2,()=>grantClearance(true));
      return;}
    if(n>=3){
      om.className='omen lv'+n;
      sc.classList.add('hot');
      const L=LINE[n];
      SFX.warn(n);
      if(L){const T=$('#toast');T.classList.add('warn');
        toast(`<span class="sig">&#9670;</span> ${L[0]}<br><span class="dim2">${L[1]}</span><span class="cur">&#9612;</span>`,3400);}
      if(n>=5){document.body.classList.remove('quake');void document.body.offsetWidth;document.body.classList.add('quake');}
    }});})();
$$('[data-skin-btn]').forEach(b=>b.onclick=()=>setSkin(b.dataset.skinBtn,true));
(function(){let k='red';try{k=localStorage.getItem('deadshot.skin')||'red';}catch(e){}
  if(k===SECRET&&!unlocked())k='og';
  const use=SKINS.includes(k)?k:'og';
  document.documentElement.setAttribute('data-skin',use);
  $$('[data-skin-btn]').forEach(b=>b.classList.toggle('on',b.dataset.skinBtn===use));})();
$('#fToggle').onclick=()=>{const c=$('#fChips');c.hidden=!c.hidden;
  $('#fToggle').classList.toggle('on',!c.hidden);
  $('#fToggle').innerHTML=c.hidden?'Choose managers &#9662;':'Hide list &#9652;';};

const S2=n=>n.toFixed(2);
/* ============ Wrapped ============ */
const WRBG=['linear-gradient(155deg,#141a3a 0%,#3c2a63 52%,#8e3f76 100%)',
 'linear-gradient(155deg,#08251f 0%,#166b53 54%,#8fd14f 100%)',
 'linear-gradient(155deg,#2a1206 0%,#7d3410 52%,#e59a3c 100%)',
 'linear-gradient(155deg,#0b1730 0%,#1c4f8d 55%,#57c6f5 100%)',
 'linear-gradient(155deg,#2b0b1a 0%,#7d1339 52%,#ff7a6b 100%)',
 'linear-gradient(155deg,#111114 0%,#3b3b41 52%,#c9a34a 100%)',
 'linear-gradient(155deg,#07202f 0%,#12607a 54%,#6ce7f2 100%)',
 'linear-gradient(155deg,#1e1038 0%,#57288a 52%,#bd84fb 100%)'];
const WR={c:[],i:0,el:0,dur:6600,paused:false,name:'',raf:0,last:0,hold:0,x0:null,y0:null,done:false};
const wrRM=()=>matchMedia('(prefers-reduced-motion:reduce)').matches;
function wrapAvail(name){
  const K=D.wk[LAST]; if(!K)return null;
  return Object.keys(K.mgr).find(t=>K.mgr[t]===name)||null;
}
function wrapCards(name){
  const K=D.wk[LAST], t=wrapAvail(name); if(!t)return null;
  const seq=K.race[t], row=ROWS.find(r=>r.y===LAST&&r.team===t), ap=K.allplay[t];
  /* an empty array is truthy, so this used to fall through to a reduce with no initial
     value the moment a new season existed but had no results in it yet */
  if(!seq||!seq.length||!row)return null;
  const fm=(K.form||{})[t]||{}, fv=(K.five||{})[t]||{};
  const pts=seq.map(x=>x.pts);
  const hi=seq.reduce((a,b)=>b.pts>a.pts?b:a), lo=seq.reduce((a,b)=>b.pts<a.pts?b:a);
  const wins=seq.filter(x=>x.win), losses=seq.filter(x=>!x.win);
  const bigW=wins.length?wins.reduce((a,b)=>(b.pts-b.oppPts)>(a.pts-a.oppPts)?b:a):null;
  const bigL=losses.length?losses.reduce((a,b)=>(b.oppPts-b.pts)>(a.oppPts-a.pts)?b:a):null;
  const closest=seq.reduce((a,b)=>Math.abs(b.pts-b.oppPts)<Math.abs(a.pts-a.oppPts)?b:a);
  const robbed=losses.length?losses.reduce((a,b)=>b.pts>a.pts?b:a):null;
  const gifted=wins.length?wins.reduce((a,b)=>b.pts<a.pts?b:a):null;
  const trades=K.trades.filter(x=>x.ta===t||x.tb===t);
  const riv=(K.rivals||[]).filter(r=>r.ta===t||r.tb===t).sort((a,b)=>b.score-a.score)[0];
  const allPPG=Object.keys(K.mgr).map(x=>K.race[x].reduce((s,y)=>s+y.pts,0)/K.weeks.length);
  const myPPG=pts.reduce((a,b)=>a+b,0)/pts.length;
  const rankOf=(v,arr)=>arr.filter(z=>z>v).length+1;
  const realPct=(row.w+row.t/2)/row.g;
  const pr=rankOf(myPPG,allPPG);
  const cards=[
    {intro:1,k:`${LAST} Wrapped`,v:esc(name),sm:1,
     n:`${K.weeks.length} weeks, ${row.g} games and one very long autumn &mdash; your year as <b>${esc(t)}</b>.`,
     pills:[`${row.w}-${row.l}${row.t?'-'+row.t:''}`,ord(row.place)+' of '+row.teams,S2(row.pf)+' PF']},
    {k:'The season',v:`${row.w}&ndash;${row.l}${row.t?'&ndash;'+row.t:''}`,
     n:`You finished <b>${ord(row.place)}</b> of ${row.teams} from the ${ord(row.seed)} seed. ${S2(row.pf)} points for, ${S2(row.pf/row.g)} a game &mdash; ${pr===1?'<b>the best in the league</b>':ord(pr)+' best in the league'}.`,
     pills:[ord(row.seed)+' seed','PPG '+f(row.pf/row.g,1),'#'+pr+' scoring']},
    {k:'Your best week',v:S2(hi.pts),
     n:`Week ${hi.w} against ${esc(hi.opp)}. ${hi.win?'You <b>won it</b>':'<span class="neg">You lost anyway</span>'} &mdash; ${S2(hi.oppPts)} came back the other way.`,
     pills:['Week '+hi.w,'Beat '+hi.ap+' of 9 that week']},
    {k:'Your worst week',v:S2(lo.pts),
     n:`Week ${lo.w} against ${esc(lo.opp)}. ${lo.win?'You <b>somehow won</b>':'You lost'}, ${S2(lo.oppPts)} against &mdash; a ${S2(hi.pts-lo.pts)} point drop from your ceiling.`,
     pills:['Week '+lo.w]},
    bigW?{k:'Biggest win',v:'+'+S2(bigW.pts-bigW.oppPts),
     n:`Week ${bigW.w}: you put ${S2(bigW.pts)}&ndash;${S2(bigW.oppPts)} on ${esc(bigW.opp)}. Never in doubt.`,pills:['Week '+bigW.w]}:null,
    bigL?{k:'Worst beating',v:'&minus;'+S2(bigL.oppPts-bigL.pts),
     n:`Week ${bigL.w}: ${S2(bigL.pts)}&ndash;${S2(bigL.oppPts)} to ${esc(bigL.opp)}. We do not need to talk about it.`,pills:['Week '+bigL.w]}:null,
    {k:'Closest call',v:S2(Math.abs(closest.pts-closest.oppPts)),
     n:`Week ${closest.w} against ${esc(closest.opp)} &mdash; you ${closest.win?'<b>won</b>':'lost'} by ${S2(Math.abs(closest.pts-closest.oppPts))}. One flex decision either way.`,pills:['Week '+closest.w]},
    robbed?{k:'Robbed',v:S2(robbed.pts),
     n:`Week ${robbed.w}. Your best losing score of the year &mdash; and ${esc(robbed.opp)} answered with ${S2(robbed.oppPts)}. That score alone would have beaten <b>${robbed.ap} of the other 9</b>.`,
     pills:['Week '+robbed.w,'Beat '+robbed.ap+' of 9']}:null,
    gifted?{k:'Got away with it',v:S2(gifted.pts),
     n:`Week ${gifted.w}. Your worst winning score, and ${esc(gifted.opp)} still only managed ${S2(gifted.oppPts)}. Take the W and say nothing.`,pills:['Week '+gifted.w]}:null,
    {k:'Against everyone',v:`${ap.w}&ndash;${ap.l}`,
     n:`Against the whole league every week you were ${pct(ap.pct)}. Your real record says ${pct(realPct)}. ${ap.pct>realPct?'<span class="neg">The schedule cost you.</span>':'<b>The schedule was kind to you.</b>'}`,
     pills:['All-play '+pct(ap.pct),'Actual '+pct(realPct)]},
    {k:'Luck',v:(row.luck>=0?'+':'&minus;')+S2(Math.abs(row.luck)),
     n:`Your scoring deserved about <b>${f(row.pythW,1)}</b> wins. You walked off with <b>${row.w}</b>. ${row.luck>=0.8?'The football gods were paying attention.':row.luck<=-0.8?'<span class="neg">The football gods were not.</span>':'More or less what you earned.'}`},
    fm.sd!=null?{k:'Consistency',v:f(fm.sd,1),
     n:`A weekly swing of ${f(fm.cv,1)}% around your own average. Your ceiling was ${S2(hi.pts)}, your floor ${S2(lo.pts)} &mdash; a ${S2(hi.pts-lo.pts)} point spread across the year.`,
     pills:['&sigma; '+f(fm.sd,1),'CV '+f(fm.cv,1)+'%']}:null,
    fm.sos!=null?{k:'The schedule',v:(fm.sos-fm.sosBase>=0?'+':'&minus;')+f(Math.abs(fm.sos-fm.sosBase),2),
     n:`Your opponents averaged ${f(fm.sos,1)} against a balanced draw of ${f(fm.sosBase,1)}. ${fm.sos>fm.sosBase?'<b>A harder road than the league average.</b>':'An easier ride than balanced.'}`}:null,
    fv.above!=null?{k:'Above water',v:`${fv.above}/${K.weeks.length}`,
     n:`Weeks you spent with a winning record${fv.streak?`. Your best run: <b>${fv.streak}</b> straight`:''}.`}:null,
    {k:'Trades',v:String(trades.length||0),
     n:trades.length?trades.map(x=>`${esc(x.d)} &mdash; with ${esc(x.ta===t?x.tb:x.ta)}`).join('<br>'):'You stood pat all season. Not one phone call answered.'},
    riv?{k:'Your rival',v:esc(riv.ta===t?riv.tb:riv.ta),sm:1,
     n:`${riv.g} meeting${riv.g===1?'':'s'} this year, decided by <b>${f(riv.marg,1)}</b> points on average. Nobody else got that close, that often.`}:null,
    {out:1,k:'That was the season',v:row.place===1?'Champion':ord(row.place)+' place',sm:row.place!==1,
     n:`You closed ${LAST} at <b>${row.w}-${row.l}${row.t?'-'+row.t:''}</b>, ${S2(row.pf)} points for and ${S2(row.pa)} against. ${row.place===1?'Nobody can take it off you.':'There is always next year.'}`,
     pills:[ord(row.place)+' of '+row.teams,'All-play '+ap.w+'-'+ap.l,'Luck '+(row.luck>=0?'+':'')+S2(row.luck)]},
  ].filter(Boolean);
  return {cards,row,team:t};
}
/* ---- story player ---- */
const wrOv=$('#wrapOv');
function openWrapped(name){
  const built=wrapCards(name); if(!built)return;
  WR.c=built.cards; WR.i=0; WR.el=0; WR.paused=false; WR.name=name; WR.done=false;
  $('#wrBrand').innerHTML=`${LAST} <b>Wrapped</b> &middot; ${esc(built.team)}`;
  $('#wrBars').innerHTML=WR.c.map((_,i)=>`<span class="wr-bar" data-b="${i}"><i></i></span>`).join('');
  wrOv.classList.add('on'); document.body.style.overflow='hidden';
  wrPaint(); WR.last=0; if(!WR.raf)WR.raf=requestAnimationFrame(wrTick);
  setTimeout(()=>{try{$('#wrX').focus();}catch(e){}},30);
}
function wrPaint(){
  const c=WR.c[WR.i];
  $('#wrStage').style.background=WRBG[WR.i%WRBG.length];
  $('#wrCard').innerHTML=`<div class="wr-k">${c.k}</div>
    <div class="wr-v${c.sm?' sm':''}">${c.v}</div>
    <div class="wr-n">${c.n}</div>
    ${c.pills?`<div class="wr-sup">${c.pills.map(p=>`<span class="wr-pill">${p}</span>`).join('')}</div>`:''}
    ${c.out?`<div class="wr-btns"><button id="wrAgain">&#8635; Play again</button><button class="ghost" id="wrBack">&#8592; Back to career</button></div>`:''}`;
  const bars=$$('#wrBars .wr-bar');
  const lastC=WR.i===WR.c.length-1;
  bars.forEach((b,i)=>{b.classList.toggle('done',i<WR.i||(lastC&&i===WR.i));const f=b.firstElementChild;
    if(i>WR.i)f.style.width='0%'; else if(i<WR.i||lastC)f.style.width='100%'; else f.style.width='0%';});
  $('#wrCount').textContent=(WR.i+1)+' / '+WR.c.length;
  $('#wrHint').innerHTML=WR.i===WR.c.length-1?'Esc to close':(wrRM()?'Tap right &#8594;':'Hold to pause &middot; tap right &#8594;');
  const ag=$('#wrAgain'), bk=$('#wrBack');
  if(ag)ag.onclick=e=>{e.stopPropagation();WR.i=0;WR.el=0;WR.done=false;wrPaint();};
  if(bk)bk.onclick=e=>{e.stopPropagation();wrClose();};
}
function wrTick(ts){
  WR.raf=requestAnimationFrame(wrTick);
  if(!wrOv.classList.contains('on')){WR.last=0;return;}
  if(!WR.last){WR.last=ts;return;}
  const dt=ts-WR.last; WR.last=ts;
  if(WR.paused||WR.done||wrRM())return;
  WR.el+=dt;
  const bar=$(`#wrBars .wr-bar[data-b="${WR.i}"] i`); if(!bar)return;
  const p=Math.min(1,WR.el/WR.dur);
  bar.style.width=(p*100).toFixed(2)+'%';
  if(p>=1)wrGo(1);
}
function wrGo(d){
  const n=WR.i+d;
  if(n<0){WR.el=0;const b=$(`#wrBars .wr-bar[data-b="${WR.i}"] i`);if(b)b.style.width='0%';return;}
  if(n>=WR.c.length){WR.done=true;return;}
  WR.i=n; WR.el=0; WR.done=(WR.i===WR.c.length-1); wrPaint();
}
function wrClose(){
  wrOv.classList.remove('on'); wrOv.classList.remove('hold');
  WR.paused=false; WR.done=true;
  if(WR.raf){cancelAnimationFrame(WR.raf);WR.raf=0;}
  if(!ov.classList.contains('on'))document.body.style.overflow='';
}
$('#wrX').onclick=e=>{e.stopPropagation();wrClose();};
$('#wrNext').onclick=e=>{e.stopPropagation();wrGo(1);};
$('#wrPrev').onclick=e=>{e.stopPropagation();wrGo(-1);};
wrOv.addEventListener('click',e=>{if(e.target===wrOv)wrClose();});
/* hold to pause + swipe */
(function(){
  const st=$('#wrStage');
  const pause=v=>{WR.paused=v;wrOv.classList.toggle('hold',v);};
  st.addEventListener('pointerdown',e=>{
    if(e.target.closest('button')&&!e.target.classList.contains('wr-nav'))return;
    WR.x0=e.clientX;WR.y0=e.clientY;
    WR.hold=setTimeout(()=>{pause(true);},260);
  });
  const end=e=>{
    clearTimeout(WR.hold);
    const wasPaused=WR.paused; pause(false);
    if(WR.x0==null)return;
    const dx=e.clientX-WR.x0, dy=e.clientY-WR.y0; WR.x0=null;
    if(Math.abs(dx)>46&&Math.abs(dx)>Math.abs(dy)){wrGo(dx<0?1:-1);}
    else if(wasPaused){/* it was a hold, not a tap */}
  };
  st.addEventListener('pointerup',end);
  st.addEventListener('pointercancel',()=>{clearTimeout(WR.hold);pause(false);WR.x0=null;});
})();
addEventListener('keydown',e=>{
  if(!wrOv.classList.contains('on'))return;
  if(e.key==='Escape'){e.stopPropagation();wrClose();}
  else if(e.key==='ArrowRight'||e.key==='PageDown'){e.preventDefault();wrGo(1);}
  else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();wrGo(-1);}
  else if(e.key===' '){e.preventDefault();WR.paused=!WR.paused;wrOv.classList.toggle('hold',WR.paused);}
},true);
/* ============ manager modal ============ */
const ov=$('#ov');
let RETFOCUS=null;
function openMgr(name){
  RETFOCUS=document.activeElement;
  const m=byName[name]; if(!m)return;
  const rs=[...rowsOf[name]].sort((a,b)=>a.y-b.y);
  $('#mTitle').textContent=name;
  $('#mSub').textContent=`${m.seasons} season${m.seasons>1?'s':''} · ${m.first}–${m.last} · ${m.w}-${m.l}${m.t?'-'+m.t:''} · ${pct(m.winpct)}`;
  const tiles=[['Titles',m.titles?(m.titles%1?m.titles.toFixed(1):m.titles):'0'],['Podiums',m.podium],
    ['Playoffs',m.apps],['Avg finish',m.avgPlace.toFixed(2)],['Power idx',m.cpi.toFixed(1)],
    ['Luck',(m.luck>=0?'+':'')+m.luck.toFixed(2)],['PPG',m.ppg.toFixed(1)],['Playoff W-L',m.poW+'-'+m.poL],
    ['All-play',m.apW+m.apL?m.apW+'-'+m.apL:'—'],['All-play %',m.apPct==null?'—':pct(m.apPct)],
    ['Best finish',m.best?ord(m.best):'—'],['Finals',m.finals],
    ['Games over .500',(m.gAbove>=0?'+':'−')+Math.abs(m.gAbove)],
    ['Winning seasons',m.sznAbove+'/'+m.seasons],
    ['Vs >.500 tms',(m.vsWinW+m.vsWinL)?m.vsWinW+'-'+m.vsWinL:'—'],
    ['Peak PI',m.peak==null?'—':m.peak.toFixed(1)]];
  /* sparkline of PI */
  const W=560,H=90,P={t:10,r:8,b:18,l:8};
  const ys=v=>P.t+(120-v)/45*(H-P.t-P.b), xs=i=>P.l+i*(W-P.l-P.r)/Math.max(1,SEA.length-1);
  let spark=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Power index by season for ${esc(name)}">
    <line x1="${P.l}" x2="${W-P.r}" y1="${ys(100)}" y2="${ys(100)}" stroke="var(--rule)" stroke-dasharray="3 3"/>
    <text x="${W-P.r}" y="${ys(100)-4}" text-anchor="end" font-size="9.5" fill="var(--ink-3)" font-family="IBM Plex Mono,monospace">100 = league average</text>`;
  const pts=SEA.map((y,i)=>({i,y,r:rs.find(r=>r.y===y)})).filter(p=>p.r);
  let seg=[],segs=[];
  pts.forEach((p,k)=>{ if(k&&p.i!==pts[k-1].i+1){segs.push(seg);seg=[];} seg.push(p); });
  segs.push(seg);
  segs.forEach(sg=>{ if(sg.length>1) spark+=`<path d="${sg.map((p,k)=>(k?'L':'M')+xs(p.i)+','+ys(p.r.pi)).join(' ')}" fill="none" stroke="var(--brass)" stroke-width="2"/>`;});
  pts.forEach(p=>{spark+=`<circle cx="${xs(p.i)}" cy="${ys(p.r.pi)}" r="${p.r.place===1?5:3.5}" fill="${p.r.place===1?'var(--brass)':'var(--surface)'}" stroke="var(--brass)" stroke-width="2"/>`;});
  spark+=SEA.map((y,i)=>`<text x="${xs(i)}" y="${H-4}" text-anchor="middle" font-size="9.5" fill="var(--ink-3)" font-family="IBM Plex Mono,monospace">${String(y).slice(2)}</text>`).join('')+'</svg>';
  const seasonRows=rs.map(r=>`<tr class="${r.place===1?'champ':''}">
    <td class="mono">${r.y}</td><td class="tm">${esc(r.team)}</td><td class="num">${r.seed}</td>
    <td class="mono">${r.w}-${r.l}-${r.t}</td><td class="num">${f(r.pf)}</td><td class="num">${f(r.ppg)}</td>
    <td class="num">${f(r.pi,1)}</td><td class="num">${f(r.luck)}</td>
    <td class="num">${r.place===1?(r.co?'<span class="chip y">Co-champ</span>':'<span class="chip y">Champion</span>'):ord(r.place)}</td></tr>`).join('');
  const pg=D.games.filter(g=>!g.void&&(g.ma===name||g.mb===name))
    .sort((a,b)=>a.y-b.y||a.wk-b.wk).map(g=>{
      const me=g.ma===name, mine=me?g.pa:g.pb, opp=me?g.pb:g.pa, oppN=me?g.mb:g.ma, oppT=me?g.tb:g.ta;
      const win=mine>opp;
      return `<tr><td class="mono">${g.y}</td><td>${g.rnd}</td>
        <td><b style="color:${win?'var(--pos)':'var(--neg)'}">${win?'W':'L'}</b></td>
        <td class="num">${mine.toFixed(2)}</td><td class="num dim">${opp.toFixed(2)}</td>
        <td><span class="mlink" data-m="${esc(oppN)}">${esc(oppN)}</span> <span class="dim tm">${esc(oppT)}</span></td></tr>`;}).join('');
  const rivals=Object.entries(D.h2h).filter(([k])=>k.split('|')[0]===name)
    .map(([k,v])=>({o:k.split('|')[1],w:v[0],l:v[1]})).sort((a,b)=>(b.w+b.l)-(a.w+a.l)||b.w-a.w);
  $('#mBody').innerHTML=`<div class="tiles">${tiles.map(([l,v])=>`<div class="tile"><b>${v}</b><span>${l}</span></div>`).join('')}</div>
    <div class="sub-h">Power index by season</div><div class="chart">${spark}</div>
    <div class="sub-h">Season by season</div><div class="scroll"><table>
      <thead><tr><th>Year</th><th>Team</th><th class="num">Seed</th><th>W-L-T</th><th class="num">PF</th><th class="num">PPG</th><th class="num">Power idx</th><th class="num">Luck</th><th class="num">Finish</th></tr></thead>
      <tbody>${seasonRows}</tbody></table></div>
    ${pg?`<div class="sub-h">Playoff games (${m.poW}–${m.poL})</div><div class="scroll"><table>
      <thead><tr><th>Year</th><th>Round</th><th></th><th class="num">For</th><th class="num">Against</th><th>Opponent</th></tr></thead><tbody>${pg}</tbody></table></div>`:''}
    ${wrapAvail(name)?`<div style="margin:20px 0 0"><button class="wrapBtn on" data-w="${esc(name)}" style="padding:9px 16px">&#9733; ${LAST} Wrapped</button>
      <span class="sub" style="margin-left:9px">the season, one card at a time</span></div>`:''}
    <div style="margin:14px 0 0;display:flex;flex-wrap:wrap;gap:8px;align-items:center">
      <button class="shareBtn" data-s="${esc(name)}" style="padding:9px 16px">&#8593; Share card</button>
      <button class="roastBtn" data-s="${esc(name)}" style="padding:9px 16px">&#8593; The case against</button>
      <button data-link="m=${esc(name)}" data-link-hash="power" style="padding:9px 16px">&#128279; Copy link</button>
      <span class="sub">a picture for the group chat, or a link that opens on this manager</span></div>
    ${rivals.length?`<div class="sub-h">Playoff head-to-head</div><div style="display:flex;flex-wrap:wrap;gap:7px">${
      rivals.map(r=>`<span class="chip" style="cursor:pointer" data-m="${esc(r.o)}"><b>${r.w}–${r.l}</b> vs ${esc(r.o)}</span>`).join('')}</div>`:''}`;
  const wb=$('#mBody .wrapBtn'); if(wb)wb.onclick=()=>openWrapped(wb.dataset.w);
  const sb=$('#mBody .shareBtn'); if(sb)sb.onclick=()=>shareCard(sb.dataset.s,sb);
  const rb=$('#mBody .roastBtn'); if(rb)rb.onclick=()=>shareAny(
    ()=>makeRoastCard(rb.dataset.s),'deadshot-case-against-'+slug(rb.dataset.s)+'.png',rb);
  ov.classList.add('on'); document.body.style.overflow='hidden'; $('#mX').focus();
}
function closeMgr(){ov.classList.remove('on');document.body.style.overflow='';hideTip();
  if(RETFOCUS&&document.contains(RETFOCUS)){try{RETFOCUS.focus();}catch(e){}} RETFOCUS=null;}
$('#mX').onclick=closeMgr;
ov.addEventListener('click',e=>{if(e.target===ov)closeMgr();});
addEventListener('keydown',e=>{if(e.key==='Escape'&&ov.classList.contains('on'))closeMgr();});
/* Keep Tab inside an open overlay. Without this, tabbing walks straight out of the
   dialog and into the page behind it, which for a keyboard user means the modal is
   still covering the screen while focus is somewhere they cannot see. */
const FOCUSABLE='a[href],button:not([disabled]),input:not([disabled]),select,textarea,[tabindex]:not([tabindex="-1"])';
function trapTab(e,box){
  if(e.key!=='Tab')return;
  const f=[...box.querySelectorAll(FOCUSABLE)].filter(el=>el.offsetWidth||el.offsetHeight||el===document.activeElement);
  if(!f.length)return;
  const first=f[0], last=f[f.length-1];
  if(!box.contains(document.activeElement)){e.preventDefault();first.focus();return;}
  if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
  else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
}
addEventListener('keydown',e=>{
  if(wrOv&&wrOv.classList.contains('on')){trapTab(e,wrOv);return;}
  if(ov.classList.contains('on'))trapTab(e,ov.querySelector('.modal')||ov);
},true);
document.addEventListener('click',e=>{const t=e.target.closest('[data-m]'); if(t){openMgr(t.dataset.m);}});
const mlink=n=>`<span class="mlink" data-m="${esc(n)}" tabindex="0" role="button">${esc(n)}</span>`;
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.dataset&&e.target.dataset.m)openMgr(e.target.dataset.m);});

/* ---- spotlight: click to lock any number of managers, hover to preview ---- */
const PICK=new Set();
let HOVER=null;
const lit=()=>PICK.size?PICK:(HOVER?new Set([HOVER]):new Set());
function spotlight(){
  const on=lit(), any=on.size>0;
  $$('#tHeat tbody tr').forEach(tr=>{
    const sel=on.has(tr.dataset.mgr);
    tr.classList.toggle('dimrow',any&&!sel);
    tr.classList.toggle('pickrow',PICK.has(tr.dataset.mgr));});
  const dots=$$('#strip circle[data-mgr]');
  dots.forEach(c=>{const sel=on.has(c.dataset.mgr);
    c.setAttribute('opacity',!any?1:(sel?1:.12));
    c.setAttribute('r',sel?(c.dataset.champ?7.4:5.8):(c.dataset.champ?6:4.2));
    c.setAttribute('stroke',sel?'var(--brass)':(c.dataset.champ?'var(--brass)':'var(--ink-3)'));});
  const box=$('#stripTrails');
  if(box){
    box.innerHTML=[...on].map(m=>{
      const mine=dots.filter(c=>c.dataset.mgr===m).sort((a,b)=>+a.dataset.yr-+b.dataset.yr);
      if(mine.length<2)return '';
      return `<path d="${mine.map((c,i)=>(i?'L':'M')+c.getAttribute('cx')+','+c.getAttribute('cy')).join(' ')}"
        fill="none" stroke="var(--brass)" stroke-width="2.4" stroke-linejoin="round"
        style="filter:drop-shadow(0 0 5px var(--glow))"/>`;}).join('');
  }
  const lbl=$('#stripWho');
  if(lbl)lbl.textContent=on.size?[...on].join('  ·  ')+(PICK.size?'   (click to release)':''):'';
  const cl=$('#spotClear'); if(cl)cl.style.display=PICK.size?'':'none';
}
function togglePick(m){PICK.has(m)?PICK.delete(m):PICK.add(m);spotlight();}

/* champions board */
const CUP=`<svg class="cup" viewBox="0 0 30 34" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
  <path d="M8 3h14v9a7 7 0 0 1-14 0z" fill="currentColor" fill-opacity=".14"/>
  <path d="M8 5H4v3a5 5 0 0 0 4.6 5"/><path d="M22 5h4v3a5 5 0 0 1-4.6 5"/>
  <path d="M15 19v5"/><path d="M10.5 24h9l1.5 6H9z" fill="currentColor" fill-opacity=".1"/>
  <path d="M7.5 31h15"/></svg>`;
$('#board').innerHTML=D.champs.map(c=>`<button class="plate${c.co?' split':''}" data-y="${c.y}">
  ${CUP}<div class="yr">${c.y}</div><div class="mgr">${c.mgrs.map(esc).join(' &amp; ')}</div>
  <div class="tm">${c.teams.map(esc).join(' / ')}</div>
  <div class="meta">${c.co?'Title split · final voided':`${c.spots}-team bracket · ${c.n} teams`}</div></button>`).join('');
$$('#board .plate').forEach(b=>b.onclick=()=>{
  const y=+b.dataset.y, c=D.champs.find(x=>x.y===y);
  LOCKTEAM=c?c.teams[0]:null;
  drawSeason(y);
  $('#seasons').scrollIntoView({behavior:'smooth'});
  setTimeout(()=>{const el=$('#brkIn'); if(el)el.closest('.card').scrollIntoView({behavior:'smooth',block:'center'});},420);});

/* ============ generic table ============ */
function table(el,cols,data,opts={}){
  const st={i:opts.sort??-1,dir:opts.dir??'desc'};
  function render(){
    let d=[...data];
    if(opts.filter)d=d.filter(opts.filter);
    if(st.i>=0){const k=cols[st.i].k;
      d.sort((a,b)=>{let x=k(a),y=k(b);
        if(x==null)x=st.dir==='asc'?Infinity:-Infinity; if(y==null)y=st.dir==='asc'?Infinity:-Infinity;
        if(typeof x==='string')return st.dir==='asc'?x.localeCompare(y):y.localeCompare(x);
        return st.dir==='asc'?x-y:y-x;});}
    el.innerHTML='<thead><tr>'+(opts.rank?'<th></th>':'')+cols.map((c,i)=>
      `<th class="s${st.i===i?' '+st.dir:''}${c.c==='num'?' num':''}" data-i="${i}"${c.t?` data-th-tip="${esc(c.t)}"`:''}>${c.h}</th>`).join('')+'</tr></thead><tbody>'+
      d.map((r,n)=>`<tr class="${opts.cls?opts.cls(r):''}">`+(opts.rank?`<td class="rk">${n+1}</td>`:'')+
      cols.map(c=>`<td class="${c.c||''}">${c.f(r)}</td>`).join('')+'</tr>').join('')+'</tbody>';
    $$('th.s',el).forEach(th=>th.onclick=()=>{const i=+th.dataset.i;
      if(st.i===i)st.dir=st.dir==='desc'?'asc':'desc'; else{st.i=i;st.dir=cols[i].asc?'asc':'desc';} render();});
    /* An explanation hangs off its own "?", never off the heading. Making the whole
       heading the hover target fought with its real job, which is to sort the table:
       you went to read what a column meant and re-sorted the page instead. */
    $$('th[data-th-tip]',el).forEach(th=>{
      const q=document.createElement('span');
      q.className='gl gl-th'; q.tabIndex=0; q.textContent='?';
      q.setAttribute('role','button');
      q.setAttribute('aria-label','What '+th.textContent.trim()+' means');
      q.addEventListener('click',e=>e.stopPropagation());
      /* stopPropagation as well as preventDefault: the th itself has a keydown handler
         that sorts, so Enter on the "?" used to re-sort the table and throw focus away
         instead of showing the explanation */
      q.addEventListener('keydown',e=>{
        if(e.key==='Enter'||e.key===' '){e.preventDefault();e.stopPropagation();
          const r=q.getBoundingClientRect();
          showTip({clientX:r.left+r.width/2,clientY:r.bottom-4},q.dataset.tip||th.dataset.thTip);}
        if(e.key==='Escape')hideTip();});
      q.dataset.tip=th.dataset.thTip;
      bindTip(q,th.dataset.thTip);
      th.appendChild(document.createTextNode(' ')); th.appendChild(q);});
    if(opts.after)opts.after(d);
  }
  render(); return {render};
}
function dbar(v,span,c){const w=Math.min(1,Math.abs(v)/span)*50,left=v>=0?50:50-w;
  return `<span class="dbar"><u></u><i class="${v<0?'l':''}" style="left:${left}%;width:${w}%;background:${c}"></i></span>`;}
const pol=v=>v>=0?'var(--pos)':'var(--neg)';

/* ============ power rankings ============ */
function powerRank(lam){
  return ACTIVE.map(n=>{
    const rs=rowsOf[n]; let num=0,den=0,pnum=0,pden=0;
    rs.forEach(r=>{const w=Math.pow(lam,LAST-r.y); num+=w*r.g*r.pi; den+=w*r.g;
      if(r.y<LAST){pnum+=w*r.g*r.pi; pden+=w*r.g;}});
    const wpi=num/den, neff=den, score=100+(wpi-100)*neff/(neff+25);
    const lastR=rs.find(r=>r.y===LAST), prior=pden?pnum/pden:null;
    const exp=Math.pow(score,K)/(Math.pow(score,K)+Math.pow(100,K));
    /* all-play luck needs no model at all, so prefer it wherever a game log exists */
    let lk=lastR?lastR.luck:null, lkSrc='pythagorean';
    if(lastR&&lastR.apw!=null){
      const apPct=lastR.apw/(lastR.apw+lastR.apl);
      lk=(lastR.w+lastR.t/2)-apPct*(lastR.w+lastR.l+lastR.t); lkSrc='all-play';
    }
    return {n,m:byName[n],score,wpi,neff,last:lastR,mom:(lastR&&prior!=null)?lastR.pi-prior:null,
      lastLuck:lk,luckSrc:lkSrc,exp};
  }).sort((a,b)=>b.score-a.score);
}
let LAM=0.72;
const BASE=(()=>{const o={};powerRank(1).forEach((r,i)=>o[r.n]=i+1);return o;})();
/* the field is tightly bunched, so cut tiers at the two widest real gaps
   rather than at arbitrary score thresholds — and never leave a group of one */
const EV=n=>{const w=n/(n+25); return w>=.7?['HIGH','var(--pos)']:w>=.5?['MEDIUM','var(--brass)']:['LOW','var(--neg)'];};
const TIERNAMES=[['TOP TIER','var(--pos)'],['THE PACK','var(--brass)'],['CHASING','var(--neg)']];
function tierCuts(sc){
  const n=sc.length; if(n<6)return [];
  const MIN=n>=9?3:2, want=n>=8?2:1;
  let best=null;
  const gaps=[];
  for(let i=MIN;i<=n-MIN;i++)gaps.push({i,g:sc[i-1]-sc[i]});
  if(want===1){best=[gaps.reduce((a,b)=>b.g>a.g?b:a).i];}
  else{
    let bs=-1;
    for(let a=0;a<gaps.length;a++)for(let b=a+1;b<gaps.length;b++){
      if(gaps[b].i-gaps[a].i<MIN)continue;
      const t=gaps[a].g+gaps[b].g;
      if(t>bs){bs=t;best=[gaps[a].i,gaps[b].i];}}
    if(!best)best=[gaps.reduce((a,b)=>b.g>a.g?b:a).i];
  }
  return best.sort((a,b)=>a-b);
}
function rankTip(r,rank){
  const m=r.m, rs=[...(rowsOf[r.n]||[])].sort((a,b)=>a.y-b.y);
  const best=rs.reduce((a,b)=>b.pi>a.pi?b:a,rs[0]);
  const worst=rs.reduce((a,b)=>b.pi<a.pi?b:a,rs[0]);
  const titles=rs.filter(x=>x.place===1).map(x=>x.y);
  const [ev]=EV(r.neff), keep=(100*r.neff/(r.neff+25)).toFixed(0);
  const base=BASE[r.n], mv=base?base-rank:0;
  const gap=(r.score-100);
  const L=[];
  L.push(`<b>${esc(r.n)}</b> &middot; power score <b>${r.score.toFixed(1)}</b> &middot; ${ord(rank)}`);
  L.push(`<span style="opacity:.72">${m.seasons} season${m.seasons>1?'s':''} ${m.first}&ndash;${m.last}`
    +(titles.length?` &middot; ${titles.length===1?'champion in ':'champion in '}${titles.join(', ')}`:' &middot; no titles')
    +`</span>`);
  L.push(`Scores <b>${gap>=0?'+':''}${gap.toFixed(1)}%</b> versus a league-average team, `
    +`which projects to <b>${pct(r.exp)}</b> against one.`);
  if(r.last)L.push(`${LAST}: index <b>${f(r.last.pi,1)}</b>`
    +(r.mom!=null?` &mdash; ${r.mom>=0?'<b style="color:var(--pos)">+'+r.mom.toFixed(1)+'</b> above':'<span style="color:var(--neg)">'+r.mom.toFixed(1)+'</span> below'} their own weighted history`:'')+'.');
  else L.push(`<span style="color:var(--neg)">Did not play in ${LAST}</span>, so there is no recent form to weight.`);
  if(best&&worst&&m.seasons>1)
    L.push(`Ceiling <b>${f(best.pi,1)}</b> in ${best.y}, floor <b>${f(worst.pi,1)}</b> in ${worst.y}.`);
  L.push(`Evidence <b>${ev}</b> &mdash; ${r.neff.toFixed(0)} weighted games, so ${keep}% of the raw number survives the shrink.`);
  if(mv>0)L.push(`<b style="color:var(--pos)">Recency is helping.</b> With every season counted equally they would be ${ord(base)}; at &lambda;&nbsp;=&nbsp;${LAM.toFixed(2)} they are ${ord(rank)}.`);
  else if(mv<0)L.push(`<span style="color:var(--neg)">Recency is hurting.</span> Every season equal would put them ${ord(base)}; at &lambda;&nbsp;=&nbsp;${LAM.toFixed(2)} they are ${ord(rank)}.`);
  else L.push(`The weighting does not move them &mdash; ${ord(rank)} either way.`);
  if(r.lastLuck!=null)L.push((r.lastLuck>1.2
    ?`<span style="color:var(--neg)">${LAST} record ran ahead of the scoring by ${r.lastLuck.toFixed(2)} wins</span> &mdash; due a correction.`
    :r.lastLuck<-1.2?`<b style="color:var(--pos)">${LAST} scoring deserved ${(-r.lastLuck).toFixed(2)} more wins</b> &mdash; due a bounce.`
    :`${LAST} record matched the scoring.`)+` <span style="opacity:.6">(${r.luckSrc} luck)</span>`);
  return L.join('<br>');
}
function drawLadder(d){
  if(!d.length){$('#ladder').innerHTML='';return;}
  const sc=d.map(r=>r.score);
  const mu=sc.reduce((a,b)=>a+b,0)/sc.length;
  const sd=Math.sqrt(sc.reduce((t,v)=>t+(v-mu)*(v-mu),0)/sc.length)||1;
  const pad=Math.max(.6,(Math.max(...sc)-Math.min(...sc))*.12);
  const lo=Math.min(100,...sc)-pad, hi=Math.max(100,...sc)+pad;
  const px=v=>((v-lo)/(hi-lo)*100);
  const zero=px(100);
  const cuts=tierCuts(sc);
  const tierOf=i=>cuts.filter(c=>i>=c).length;
  let prevTier=-1,out='';
  d.forEach((r,i)=>{
    const ti=tierOf(i), mv=BASE[r.n]?BASE[r.n]-(i+1):0;
    if(cuts.length&&ti!==prevTier){
      const [tn,tc]=TIERNAMES[Math.min(ti,TIERNAMES.length-1)];
      const gap=ti===0?null:(sc[cuts[ti-1]-1]-sc[cuts[ti-1]]);
      out+=`<div class="lad-tier" style="color:${tc}"><span></span>${tn}${gap!=null?` <em style="font-style:normal;opacity:.65">${gap.toFixed(1)} back</em>`:''}<span></span></div>`;
      prevTier=ti;}
    const tc=TIERNAMES[Math.min(ti,TIERNAMES.length-1)][1];
    const w=Math.abs(px(r.score)-zero);
    const left=r.score>=100?zero:zero-w;
    out+=`<div class="lad${i<3?' top':''}" data-m="${esc(r.n)}">
      <span class="lad-r">${i+1}</span>
      <span class="lad-n">${esc(r.n)}</span>
      <span class="lad-track"><span class="lad-mid" style="display:block;position:absolute;top:0;bottom:0;width:1px;background:var(--rule);left:${zero}%"></span>
        <span class="lad-bar" style="left:${left}%;width:${w}%;background:${r.score>=100?'var(--pos)':'var(--neg)'}"></span>
        <span class="lad-dot" style="left:${px(r.score)}%;background:${tc}"></span></span>
      <span class="lad-s">${r.score.toFixed(1)}</span>
      <span class="lad-w">${pct(r.exp)}</span>
      <span class="lad-mv ${mv>0?'up':mv<0?'dn':''}">${mv>0?'▲'+mv:mv<0?'▼'+(-mv):'—'}</span>
      <span class="lad-ev" style="color:${EV(r.score!=null?r.neff:0)[1]}" title="Evidence: ${EV(r.neff)[0]}">${'●'.repeat(EV(r.neff)[0]==='HIGH'?3:EV(r.neff)[0]==='MEDIUM'?2:1)}<span style="opacity:.25">${'●'.repeat(EV(r.neff)[0]==='HIGH'?0:EV(r.neff)[0]==='MEDIUM'?1:2)}</span></span></div>`;});
  $('#ladder').innerHTML=`<div class="lad-head"><span></span><span></span>
      <span class="lad-track-h"><i style="left:0">${lo.toFixed(1)}</i><i style="left:${zero}%;transform:translateX(-50%)">100 · league average</i><i style="right:0">${hi.toFixed(1)}</i></span>
      <span>SCORE</span><span>PROJ W%</span><span>vs&nbsp;λ1</span><span class="lad-ev">EVID</span></div>`+out;
  $$('#ladder .lad').forEach(el=>{
    el.onclick=()=>openMgr(el.dataset.m);
    const r=d.find(x=>x.n===el.dataset.m);
    bindTip(el,r?rankTip(r,d.indexOf(r)+1):esc(el.dataset.m));});
}
function drawRank(){
  const d=powerRank(LAM).filter(r=>vis(r.n));
  $('#lamLbl').textContent='λ = '+LAM.toFixed(2)+' · '+(LAM>=.97?'all seasons equal':LAM<=.55?'recent seasons dominate':'balanced');
  drawLadder(d);
  table($('#tRank'),[
   {h:'Manager',f:r=>mlink(r.n),c:'nm',k:r=>r.n,asc:1},
   {h:'Power score',f:r=>`<b>${r.score.toFixed(1)}</b>`,c:'num',k:r=>r.score,t:'Recency-weighted, sample-shrunk power index'},
   {h:'',f:r=>dbar(r.score-100,9,pol(r.score-100)),k:r=>r.score},
   {h:'Proj win %',f:r=>pct(r.exp),c:'num',k:r=>r.exp,t:'Pythagorean win rate versus a league-average opponent'},
   {h:LAST+' idx',f:r=>r.last?f(r.last.pi,1):'—',c:'num',k:r=>r.last?r.last.pi:null},
   {h:'Momentum',f:r=>r.mom==null?'—':(r.mom>=0?'+':'')+r.mom.toFixed(1),c:'num',k:r=>r.mom,t:'Last season versus their own weighted history'},
   {h:LAST+' luck',f:r=>r.lastLuck==null?'—':f(r.lastLuck),c:'num',k:r=>r.lastLuck,
    t:'Real wins minus the wins the scoring earned. Uses all-play luck — no model, just the weekly scores — for seasons with a game log, and falls back to Pythagorean for older ones.'},
   {h:'Outlook',f:r=>{
      if(r.lastLuck==null)return '—';
      if(r.lastLuck>1.2)return '<span class="chip" style="border-color:var(--neg);color:var(--neg)">rode luck · due to fall</span>';
      if(r.lastLuck<-1.2)return '<span class="chip" style="border-color:var(--pos);color:var(--pos)">robbed · due to bounce</span>';
      return '<span class="chip dim">record matched scoring</span>';},k:r=>r.lastLuck},
   {h:'Szns',f:r=>r.m.seasons,c:'num',k:r=>r.m.seasons},
   {h:'Evidence',f:r=>{const[e,c]=EV(r.neff);
      return `<span class="chip" style="border-color:${c};color:${c}">${e}</span> <span class="dim">${(100*r.neff/(r.neff+25)).toFixed(0)}%</span>`;},
    c:'num',k:r=>r.neff,
    t:'Weighted games behind the score, expressed as how much of the raw number survives the shrink toward 100. Low means the ranking is running on thin evidence, not that the manager is bad.'},
  ],d,{rank:1,sort:1});
}
$('#rankMore').onclick=()=>{const t=$('#rankTbl'); t.hidden=!t.hidden;
  $('#rankMore').classList.toggle('on',!t.hidden);
  $('#rankMore').innerHTML=t.hidden?'Show model details &#9662;':'Hide model details &#9652;';};
$('#lam').oninput=e=>{LAM=+e.target.value/100;drawRank();};
$('#lamReset').onclick=()=>{LAM=.72;$('#lam').value=72;drawRank();};
drawRank(); REDRAW.push(drawRank);

/* ============ all-time ============ */
/* rebuild career records over an arbitrary window of seasons */
function aggregate(years){
  const set=new Set(years), out={};
  ROWS.filter(r=>set.has(r.y)).forEach(r=>{
    const m=out[r.mgr]=out[r.mgr]||{name:r.mgr,seasons:0,titles:0,second:0,third:0,podium:0,lastPl:0,
      w:0,l:0,t:0,pf:0,pa:0,g:0,apps:0,luck:0,pyth:0,piW:0,places:0,first:9999,last:0,
      apW:0,apL:0,apSzn:0,apRW:0,apG:0};
    m.seasons++; m.titles+=r.share; m.second+=r.place===2?1:0; m.third+=r.place===3?1:0;
    if(r.apw!=null){m.apW+=r.apw; m.apL+=r.apl; m.apSzn++; m.apRW+=r.w+r.t/2; m.apG+=r.w+r.l+r.t;}
    m.podium+=r.place<=3?1:0; m.lastPl+=r.place===r.teams?1:0;
    m.w+=r.w; m.l+=r.l; m.t+=r.t; m.pf+=r.pf; m.pa+=r.pa; m.g+=r.w+r.l+r.t;
    m.apps+=r.po?1:0; m.luck+=r.luck; m.pyth+=r.pythW; m.piW+=r.pi*(r.w+r.l+r.t);
    m.places+=r.place; m.first=Math.min(m.first,r.y); m.last=Math.max(m.last,r.y);});
  return Object.values(out).map(m=>({...m,winpct:(m.w+m.t/2)/m.g,avgPlace:m.places/m.seasons,
    ppg:m.pf/m.g,cpi:m.piW/m.g,pythW:m.pyth,
    apPct:(m.apW+m.apL)?m.apW/(m.apW+m.apL):null,
    apLuck:(m.apW+m.apL)?m.apRW-(m.apW/(m.apW+m.apL))*m.apG:null}))
    .sort((a,b)=>b.titles-a.titles||b.podium-a.podium||b.winpct-a.winpct);
}
let SEARCH='', YRWIN=0;
function windowYears(){return YRWIN?SEA.slice(-YRWIN):SEA;}
function allTimeData(){return YRWIN?aggregate(windowYears()):M;}
let allT;
function buildAll(){
  const yrs=windowYears();
  $('#rangeSub').textContent=YRWIN?`${yrs[0]}–${yrs[yrs.length-1]} only · ${yrs.length} seasons`:`all ${SEA.length} seasons`;
  allT=table($('#tAll'),[
 {h:'Manager',f:r=>mlink(r.name),c:'nm',k:r=>r.name,asc:1},
 {h:'Szns',f:r=>r.seasons,c:'num',k:r=>r.seasons},
 {h:'Titles',f:r=>r.titles?(r.titles%1?r.titles.toFixed(1):r.titles):'—',c:'num',k:r=>r.titles,t:'Co-champions count 0.5'},
 {h:'2nd',f:r=>r.second||'—',c:'num',k:r=>r.second},
 {h:'3rd',f:r=>r.third||'—',c:'num',k:r=>r.third},
 {h:'Podium',f:r=>r.podium||'—',c:'num',k:r=>r.podium},
 {h:'Last',f:r=>r.lastPl||'—',c:'num',k:r=>r.lastPl},
 {h:'W',f:r=>r.w,c:'num',k:r=>r.w},{h:'L',f:r=>r.l,c:'num',k:r=>r.l},
 {h:'Win %',f:r=>pct(r.winpct),c:'num',k:r=>r.winpct},
 {h:'All-play',f:r=>r.apW+r.apL?`<span class="mono">${r.apW}&ndash;${r.apL}</span>`:'—',c:'num',k:r=>r.apPct,
  t:'Record against the whole league every week, summed over the seasons with a loaded game log (2021–2025). Schedule luck removed entirely.'},
 {h:'All-play %',f:r=>r.apPct==null?'—':pct(r.apPct),c:'num',k:r=>r.apPct},
 {h:'Sched luck',f:r=>r.apLuck==null?'—':(r.apLuck>=0?'+':'')+r.apLuck.toFixed(2),c:'num',k:r=>r.apLuck,
  t:'Real wins minus all-play expected wins over those same seasons. No model, no exponent — just how the schedule fell.'},
 {h:'Avg finish',f:r=>f(r.avgPlace),c:'num',k:r=>r.avgPlace,asc:1},
 {h:'Playoffs',f:r=>r.apps,c:'num',k:r=>r.apps},
 {h:'Power idx',f:r=>f(r.cpi,1),c:'num',k:r=>r.cpi},
 {h:'Luck',f:r=>f(r.luck),c:'num',k:r=>r.luck},
 {h:'Span',f:r=>`<span class="dim mono">${r.first}–${r.last}</span>`,k:r=>r.first},
],allTimeData(),{rank:1,sort:-1,cls:r=>r.titles>=1?'champ':'',
   filter:r=>vis(r.name)&&(!SEARCH||r.name.toLowerCase().includes(SEARCH)),
   after:d=>{$('#searchN').textContent=SEARCH?`${d.length} shown`:'';}});
}
buildAll();
$('#search').oninput=e=>{SEARCH=e.target.value.trim().toLowerCase();allT.render();};
$$('[data-yr]').forEach(b=>b.onclick=()=>{
  $$('[data-yr]').forEach(x=>x.classList.toggle('on',x===b));
  YRWIN=+b.dataset.yr; buildAll();});
REDRAW.push(()=>buildAll());

/* ============ heat grid ============ */
/* One line of character, not a second stat table. Thresholds come from the real spread
   of this league (cpi 78-107, luck -12.3 to +9.1, trend -8.0 to +3.0), so every rule
   catches somebody. First match wins.

   Two things the rules must respect. Managers who stopped playing are described in the
   past tense, because "trending up" about someone who left in 2023 is just wrong. And
   no two active managers may land on the same line -- test.js checks that, because
   three of them collided the first time round. */
const MGR_YEARS={}; ROWS.forEach(r=>{(MGR_YEARS[r.mgr]=MGR_YEARS[r.mgr]||[]).push(r.y);});
function mgrGaps(m){
  const ys=(MGR_YEARS[m.name]||[]).slice().sort((a,b)=>a-b);
  if(ys.length<2)return 0;
  /* seasons the league actually ran between their first and last, that they sat out */
  return SEA.filter(y=>y>ys[0]&&y<ys[ys.length-1]&&ys.indexOf(y)<0).length;
}
/* Missed seasons and separate absences are different numbers, and the copy kept confusing
   them: Nick Gearing sat out four seasons but he only ever left ONCE, so "keeps
   disappearing" and "left and returned more than once" were both untrue. Nobody in this
   league has left twice. `back` is the first season after the most recent absence, which
   is what lets a line say whether the title came before it or after it. */
/* A career that has gone down every single season is a rare and specific thing, and
   worth saying out loud. Anything less than three seasons is noise, not a slide. */
function mgrSlide(m){
  const rs=ROWS.filter(r=>r.mgr===m.name).sort((a,b)=>a.y-b.y);
  if(rs.length<3)return 0;
  for(let i=1;i<rs.length;i++) if(rs[i].pi>=rs[i-1].pi) return 0;
  /* the number of DECLINES, not of seasons: five seasons contain four drops, and a first
     season cannot have scored less than the year before */
  return rs.length-1;
}
/* what has happened since the last title, so a line can say whether it stuck */
function mgrSinceTitle(m){
  const rs=ROWS.filter(r=>r.mgr===m.name).sort((a,b)=>a.y-b.y);
  const t=rs.filter(r=>r.place===1);
  if(!t.length)return {n:0,below:0};
  const ly=t[t.length-1].y, after=rs.filter(r=>r.y>ly);
  return {n:after.length,below:after.filter(r=>r.pi<100).length};
}
function mgrSpells(m){
  const ys=(MGR_YEARS[m.name]||[]).slice().sort((a,b)=>a-b);
  if(ys.length<2)return {spells:0,missed:0,back:null};
  let spells=0,missed=0,inGap=false,back=null;
  /* bound is inclusive: a manager whose comeback IS their most recent season never had
     `back` set, so the champion-on-return lines were unreachable in a live season */
  SEA.filter(y=>y>ys[0]&&y<=ys[ys.length-1]).forEach(y=>{
    const out=ys.indexOf(y)<0;
    if(out){missed++; if(!inGap)spells++;}
    else if(inGap)back=y;
    inGap=out;});
  return {spells:spells,missed:missed,back:back};
}
function mgrVibe(m){
  const t=m.titles||0, pod=m.podium||0, ap=m.apps||0, sz=m.seasons||0;
  const cpi=m.cpi, luck=m.luck||0, tr=m.trend||0, rate=sz?ap/sz:0;
  const active=m.last===LAST, gaps=mgrGaps(m), sp=mgrSpells(m);
  const NUMW=['','one','two','three','four','five','six','seven','eight','nine'];
  const gapYr=gaps===1?'a year away':(NUMW[gaps]||gaps)+' years away';
  const tYrs=ROWS.filter(r=>r.mgr===m.name&&r.place===1).map(r=>r.y).sort((a,b)=>a-b);
  const wonOnReturn=sp.back!=null&&tYrs.indexOf(sp.back)>=0;
  const wonAfterGap=sp.back!=null&&tYrs.some(y=>y>=sp.back);
  const slide=mgrSlide(m), post=mgrSinceTitle(m);
  const NUM2=['','one','two','three','four','five','six','seven','eight','nine'];
  const cooled=post.n>=2&&post.below===post.n
    ? '. Below average in every season since.'
    :(post.n===1&&post.below===1?'. Below average ever since.':'.');

  /* one-and-done */
  if(sz===1&&cpi<90)   return 'One season, and it went badly enough that he never came back.';
  if(sz===1&&pod>=1)   return 'One season, one trip to the podium, then gone.';
  if(sz===1)           return 'A single season on the books, too brief to judge.';

  /* gone from the league: everything here is past tense */
  if(!active&&t>=2)    return 'Won twice, then left with the league still owing him a rematch.';
  if(!active&&t>=1)    return 'Left holding a ring, after the years stopped going his way.';
  if(!active&&ap===0)  return 'Never once made the bracket, and eventually stopped turning up.';
  if(!active&&gaps>0)  return 'Played '+sz+' seasons around '+gapYr+', and has not been back since.';
  if(!active)          return 'Played, faded, and has not been back since.';

  /* still playing */
  if(t>=2)             return 'As decorated as this league gets.';
  if(luck<=-8)         return 'The scoring deserved far better than the record ever showed.';
  if(luck>=8.5&&slide>=3) return 'The kindest schedule in the league, and '+(NUM2[slide]||slide)+
                            ' straight seasons of scoring less than the year before.';
  if(luck>=8.5)        return 'Has had the schedule on his side more than anyone.';
  if(slide>=4)         return (NUM2[slide]||slide)+' seasons in the league and every one of them worse than the last.';
  if(t>=1&&tr>=2.5)    return 'Holds the newest trophy and is still climbing.';
  if(t>=1&&sp.spells>=2)          return 'Keeps disappearing for years at a time and keeps coming back with silverware.';
  if(t>=1&&wonOnReturn&&gaps>=3)  return 'Gone for '+(NUMW[gaps]||gaps)+' straight seasons, then champion in his first year back'+cooled;
  if(t>=1&&wonOnReturn)           return 'Sat out a season, came back, and won it at the first attempt'+cooled;
  if(t>=1&&wonAfterGap)           return 'Left the league, came back, and has won it since returning.';
  if(t>=1&&sp.spells>=1)          return 'Won it, disappeared for '+gapYr.replace(' away','')+', and is playing again.';
  if(t>=1&&rate>=0.7)  return 'A permanent fixture in the bracket, with a title to prove it.';
  if(t>0&&t<1)         return 'Owns a share of a title, and will mention it.';
  if(pod>=3&&t<1)      return 'Always in the last room of the season, never the one leaving with it.';
  if(ap===0&&sz>=2)    return 'Still waiting on a first playoff appearance.';
  if(cpi>=103)         return 'Scores like a contender without the trophies to match.';
  if(cpi<=95)          return 'Has spent most of league history playing catch-up.';
  if(tr>=2)            return 'Trending up sharply enough that people have noticed.';
  return 'Steady, mid-table, rarely the story.';
}

/* The explainer is generated rather than written, so the worked example and the band
   counts stay true when a season is added. It is in REDRAW because the band swatches
   come from diverge(), which reads the live theme. */
function drawPiHelp(){
  const host=$('#piHelp'); if(!host)return;
  const first=SEA[0], last=SEA[SEA.length-1];
  const chL=D.champs.find(c=>c.y===last);
  const ex=ROWS.filter(r=>r.y===last&&chL.teams.indexOf(r.team)>=0)[0]
        ||ROWS.filter(r=>r.y===last).sort((a,b)=>b.pi-a.pi)[0];
  const lgA=(D.champs.find(c=>c.y===first)||{}).lg, lgB=chL.lg;
  const infl=lgA?((lgB/lgA-1)*100):null;
  const hi=ROWS.reduce((a,b)=>b.pi>a.pi?b:a), lo=ROWS.reduce((a,b)=>b.pi<a.pi?b:a);
  /* The written labels say what the level is; the four counts beside them say what it has
     actually been worth. That split matters: a label on its own once claimed 110-120 was
     "a contender's year" when the median champion scored 107.4 and one has won at 93.9.
     Every count is read off ROWS, so the words can describe and the numbers can judge. */
  const BANDS=[
    [120,999,'The best seasons this league has produced'],
    [110,120,'A contender&rsquo;s year'],
    [103,110,'Clearly above the field'],
    [97,103,'The middle of the pack'],
    [90,97,'Below the field'],
    [0,90,'A season to forget']];
  /* no "x of y" here: the seasons column is already sitting right beside it */
  const bandCell=(v,hi)=>`<span style="flex:0 0 84px;text-align:right;
    font-family:'IBM Plex Mono',monospace;font-size:12.5px;
    color:${v?(hi?'var(--brass)':'var(--ink)'):'var(--ink-3)'};
    font-weight:${v&&hi?600:400}">${v}</span>`;
  const bandRows=BANDS.map(b=>{
    const rs=ROWS.filter(r=>r.pi>=b[0]&&r.pi<b[1]);
    const n=rs.length;
    const pl=rs.filter(r=>r.po).length;
    const pod=rs.filter(r=>r.place<=3).length;
    const t=rs.filter(r=>r.place===1).length;
    const mid=Math.min(130,Math.max(70,(b[1]>900?126:(b[0]+b[1])/2)));
    const lab=b[1]>900?b[0]+' and up':(b[0]===0?'under '+b[1]:b[0]+'&ndash;'+b[1]);
    return `<div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-top:1px solid var(--rule-2)">
      <span style="flex:0 0 78px;font-family:'IBM Plex Mono',monospace;font-size:12.5px;
        background:${diverge(mid-100,16)};color:${inkOn(mid-100,16)};text-align:center;
        padding:3px 0;border-radius:3px">${lab}</span>
      <span style="flex:1 1 auto;min-width:0;font-size:13.5px;color:var(--ink-2)">${b[2]}</span>
      <span style="flex:0 0 84px;text-align:right;font-family:'IBM Plex Mono',monospace;
        font-size:12.5px;color:var(--ink-3)">${n}</span>
      ${bandCell(pl,false)}${bandCell(pod,false)}${bandCell(t,true)}
    </div>`;}).join('');
  const bandHead=`<div style="display:flex;align-items:flex-end;gap:10px;padding:0 0 5px">
    <span style="flex:0 0 78px"></span><span style="flex:1 1 auto"></span>
    ${['TEAMS','MADE PLAYOFFS','PODIUMS','TITLES'].map(h=>
      `<span style="flex:0 0 84px;text-align:right;font-family:'IBM Plex Mono',monospace;
        font-size:9.5px;letter-spacing:.11em;color:var(--ink-3);line-height:1.25">${h}</span>`).join('')}
  </div>`;

  host.innerHTML=`
  <p style="margin:0 0 12px;font-size:14px;color:var(--ink-2)"><b>The whole calculation:</b>
    take your points per game, divide by what the average team scored that same season,
    multiply by 100.</p>
  <p style="margin:0 0 16px;font-size:14px;color:var(--ink-2)">
    <b>${esc(ex.team)}</b> averaged <b class="mono">${ex.ppg.toFixed(2)}</b> a game in ${ex.y}.
    The league averaged <b class="mono">${ex.lg.toFixed(2)}</b>. That is
    <span class="mono">${ex.ppg.toFixed(2)} &divide; ${ex.lg.toFixed(2)} &times; 100</span> =
    <b class="mono" style="color:var(--brass)">${ex.pi.toFixed(1)}</b> &mdash; they scored
    <b>${(ex.pi-100).toFixed(1)}% ${ex.pi>=100?'more':'less'}</b> than the typical team that year.</p>
  <div class="sub-h" style="margin:0 0 2px">What the number means</div>
  <p style="margin:0 0 8px;font-size:13px;color:var(--ink-3)">Read across: what has actually
    become of the ${ROWS.length} teams on record that landed in each band.</p>
  <div style="overflow-x:auto"><div style="min-width:560px">${bandHead}${bandRows}</div></div>
  <p style="margin:16px 0 0;font-size:14px;color:var(--ink-2)"><b>Why it travels.</b>
    Raw points do not. The league averaged <b class="mono">${lgA?lgA.toFixed(2):'&mdash;'}</b> a game in
    ${first} and <b class="mono">${lgB.toFixed(2)}</b> in ${last}${infl!=null?', '+Math.abs(infl).toFixed(0)+'% '+(infl>=0?'higher':'lower'):''},
    so the same points total means two different things in those two years. Power Index
    is re-based every season, which is why a 110 in ${first} and a 110 in ${last} are the
    same achievement. The best single season on record is
    <b>${esc(hi.team)}</b>${hi.mgr?' ('+esc(hi.mgr)+')':''} in ${hi.y} at
    <b class="mono">${hi.pi.toFixed(1)}</b>; the worst is <b>${esc(lo.team)}</b> in ${lo.y}
    at <b class="mono">${lo.pi.toFixed(1)}</b>.</p>
  <details class="expl" style="margin-top:14px"><summary>What it deliberately ignores</summary>
    <p class="plain" style="margin:0 0 9px"><b>In plain English:</b> it does not care whether you won.</p>
    <p style="margin:0;font-size:13px;color:var(--ink-2)">Power Index only looks at what you
    scored, never at your record. A team can score like a champion and still finish 6&ndash;8
    because of who they happened to be drawn against, and Power Index will still say they
    scored like a champion. That is the point: it measures the team, not the schedule. The
    gap between the two is what <b>Luck</b> measures, and the two sections are meant to be
    read together. It also treats every game equally, so one enormous week and a steady
    season can land on the same number &mdash; <b>Consistency</b> is where that shows up.</p>
  </details>`;
}
drawPiHelp(); REDRAW.push(drawPiHelp);

function drawHeat(){
  const order=[...M].filter(m=>vis(m.name)).sort(bySeasons);
  const pi={}; ROWS.forEach(r=>pi[r.y+'|'+r.mgr]=r);
  let h='<thead><tr><th>Manager</th>'+SEA.map(y=>`<th class="num">${y}</th>`).join('')+'<th class="num">Career</th><th class="num">Szns</th></tr></thead><tbody>';
  order.forEach(m=>{h+=`<tr data-mgr="${esc(m.name)}"><td class="nm">${mlink(m.name)}</td>`;
    SEA.forEach(y=>{const r=pi[y+'|'+m.name];
      h+=r?`<td class="h" data-k="${y}|${esc(m.name)}" data-y="${y}"><span style="background:${diverge(r.pi-100,16)};color:${inkOn(r.pi-100,16)}">${r.pi.toFixed(1)}</span></td>`
          :'<td class="h e"><span>·</span></td>';});
    h+=`<td class="num"><b>${m.cpi.toFixed(1)}</b></td><td class="num dim">${m.seasons}</td></tr>`;});
  $('#tHeat').innerHTML=h+'</tbody>';
  $('#piLegend').innerHTML=`<span style="display:inline-block;width:11px;height:11px;background:${diverge(-14,16)};border:1px solid var(--rule);vertical-align:-1px"></span> below average &nbsp;<span style="display:inline-block;width:11px;height:11px;background:${diverge(14,16)};border:1px solid var(--rule);vertical-align:-1px"></span> above`;
  $$('#tHeat tbody tr[data-mgr]').forEach(tr=>{
    tr.addEventListener('mouseenter',()=>{HOVER=tr.dataset.mgr;spotlight();});
    tr.addEventListener('mouseleave',()=>{HOVER=null;spotlight();});
    tr.addEventListener('click',e=>{if(e.target.closest('.mlink'))return;togglePick(tr.dataset.mgr);});
    tr.style.cursor='pointer';});
  spotlight();
  $$('#tHeat td.h[data-k]').forEach(td=>{const r=pi[td.dataset.k];
    bindTip(td,`<b>${esc(r.mgr)} · ${r.y}</b><br>${esc(r.team)}<br>Power index <b>${r.pi.toFixed(1)}</b> · ${r.ppg.toFixed(2)} PPG vs league ${r.lg.toFixed(2)}<br>${r.w}-${r.l}${r.t?'-'+r.t:''} · finished ${ord(r.place)}<br><i>click to open ${r.y}</i>`);
    td.onclick=()=>{LOCKTEAM=r.team;drawSeason(+td.dataset.y);$('#seasons').scrollIntoView({behavior:'smooth'});};});
  $$('#tHeat tbody tr[data-mgr] td.nm').forEach(td=>{
    const name=td.closest('tr').dataset.mgr, m=M.filter(x=>x.name===name)[0];
    if(m)bindTip(td,`<b>${esc(name)}</b><br>${mgrVibe(m)}`);});
}
drawHeat(); REDRAW.push(drawHeat);

/* ============ season shape charts ============ */
const SEAMETA=SEA.map(y=>{
  const rs=ROWS.filter(r=>r.y===y), n=rs.length;
  const lg=rs[0].lg, sd=Math.sqrt(rs.reduce((a,r)=>a+Math.pow(r.ppg-lg,2),0)/n);
  const mw=rs.reduce((a,r)=>a+(r.w+r.t/2)/r.g,0)/n;
  const wsd=Math.sqrt(rs.reduce((a,r)=>a+Math.pow((r.w+r.t/2)/r.g-mw,2),0)/n)*100;
  return {y,n,lg,sd,wsd,rng:Math.max(...rs.map(r=>r.pi))-Math.min(...rs.map(r=>r.pi)),rs};
});
function lineChart(el,pts,fmt,label,aria){
  const W=760,H=210,P={t:14,r:20,b:30,l:50};
  const xs=i=>P.l+i*(W-P.l-P.r)/(pts.length-1);
  const vals=pts.map(p=>p.v), span=Math.max(...vals)-Math.min(...vals)||1;
  const lo=Math.min(...vals)-span*.22, hi=Math.max(...vals)+span*.22;
  const ys=v=>P.t+(hi-v)/(hi-lo)*(H-P.t-P.b);
  let g='';
  for(let k=0;k<=4;k++){const v=lo+(hi-lo)*k/4;
    g+=`<line x1="${P.l}" x2="${W-P.r}" y1="${ys(v)}" y2="${ys(v)}" stroke="var(--rule-2)"/>
        <text x="${P.l-9}" y="${ys(v)+4}" text-anchor="end" font-size="10.5" fill="var(--ink-3)" font-family="IBM Plex Mono,monospace">${fmt(v)}</text>`;}
  const line=pts.map((p,i)=>(i?'L':'M')+xs(i)+','+ys(p.v)).join(' ');
  const area=`${line} L${xs(pts.length-1)},${ys(lo)} L${xs(0)},${ys(lo)} Z`;
  const dots=pts.map((p,i)=>`<circle cx="${xs(i)}" cy="${ys(p.v)}" r="${i===pts.length-1?5:3.5}" fill="${i===pts.length-1?'var(--brass)':'var(--surface)'}" stroke="var(--brass)" stroke-width="2"/>`).join('');
  const lab=pts.map((p,i)=>`<text x="${xs(i)}" y="${H-P.b+18}" text-anchor="middle" font-size="10.5" fill="var(--ink-3)" font-family="IBM Plex Mono,monospace">${String(p.y).slice(2)}</text>`).join('');
  const hit=pts.map((p,i)=>`<rect x="${xs(i)-19}" y="${P.t}" width="38" height="${H-P.t-P.b}" fill="transparent" data-i="${i}" style="cursor:crosshair"/>`).join('');
  el.innerHTML=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${aria}">
    <defs><linearGradient id="gg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--brass)" stop-opacity=".2"/><stop offset="1" stop-color="var(--brass)" stop-opacity="0"/></linearGradient></defs>
    ${g}<path d="${area}" fill="url(#gg)"/><path d="${line}" fill="none" stroke="var(--brass)" stroke-width="2" stroke-linejoin="round"/>${dots}${lab}${hit}</svg>`;
  $$('rect[data-i]',el).forEach(r=>{const i=+r.dataset.i,p=pts[i],pr=pts[i-1];
    bindTip(r,`<b>${p.y}</b><br>${label}: <b>${fmt(p.v)}</b>`+(pr?`<br>${p.v>pr.v?'▲':'▼'} ${fmt(Math.abs(p.v-pr.v))} vs ${pr.y}`:'')+(p.extra||''));});
}
const BAL={
 sd:{lab:'Scoring spread',fmt:v=>v.toFixed(1),title:'Scoring spread — standard deviation of points per game',
  note:'How far apart the teams were on scoring. A low number means everyone put up similar points; a high number means the league had genuine haves and have-nots.',
  get:m=>m.sd},
 wsd:{lab:'Record spread',fmt:v=>v.toFixed(1)+'%',title:'Record spread — standard deviation of win rate',
  note:'The same idea applied to wins rather than points. When this is high and scoring spread is low, the standings were decided by luck rather than by quality.',
  get:m=>m.wsd},
 rng:{lab:'Power index range',fmt:v=>v.toFixed(1),title:'Power index range — best team minus worst',
  note:'The gap between the best and worst scoring team, in index points. The single bluntest measure of how lopsided a season was.',
  get:m=>m.rng},
 lg:{lab:'League average PPG',fmt:v=>v.toFixed(1),title:'League average points per game',
  note:'Why the Power Index is re-based every year: raw scoring rose about 12% across the decade, so points from different eras are not comparable.',
  get:m=>m.lg},
};
function drawBal(k){
  const b=BAL[k]; $('#balTitle').textContent=b.title; $('#balNote').textContent=b.note;
  lineChart($('#bal'),SEAMETA.map(m=>({y:m.y,v:b.get(m)})),b.fmt,b.lab,
    `${b.lab} by season, ${SEA[0]} to ${LAST}`);
}
$$('#balTitle').length; $$('.card-h .pills button[data-bal]').forEach(b=>b.onclick=()=>{
  $$('.card-h .pills button[data-bal]').forEach(x=>x.classList.toggle('on',x===b)); drawBal(b.dataset.bal);});
drawBal('sd');
REDRAW.push(()=>{const b=$$('.card-h .pills button[data-bal].on')[0]; drawBal(b?b.dataset.bal:'sd');});

/* dot strip */
function drawStrip(){
  const W=880,H=300,P={t:16,r:16,b:30,l:44};
  const lo=Math.min(...ROWS.map(r=>r.pi))-3, hi=Math.max(...ROWS.map(r=>r.pi))+3;
  const xs=i=>P.l+(i+.5)*(W-P.l-P.r)/SEA.length, ys=v=>P.t+(hi-v)/(hi-lo)*(H-P.t-P.b);
  let g='';
  for(let v=Math.ceil(lo/10)*10;v<=hi;v+=10)
    g+=`<line x1="${P.l}" x2="${W-P.r}" y1="${ys(v)}" y2="${ys(v)}" stroke="${v===100?'var(--rule)':'var(--rule-2)'}" stroke-dasharray="${v===100?'4 3':''}"/>
        <text x="${P.l-8}" y="${ys(v)+4}" text-anchor="end" font-size="10" fill="var(--ink-3)" font-family="IBM Plex Mono,monospace">${v}</text>`;
  let dots='',bands='';
  SEA.forEach((y,i)=>{
    const rs=ROWS.filter(r=>r.y===y).sort((a,b)=>b.pi-a.pi);
    bands+=`<line x1="${xs(i)}" x2="${xs(i)}" y1="${ys(Math.max(...rs.map(r=>r.pi)))}" y2="${ys(Math.min(...rs.map(r=>r.pi)))}" stroke="var(--rule)" stroke-width="1"/>`;
    rs.forEach((r,k)=>{const off=(k%2?1:-1)*Math.floor(k/2)*5.4, on=vis(r.mgr);
      dots+= on
        ? `<circle cx="${xs(i)+off}" cy="${ys(r.pi)}" r="${r.place===1?6:4.2}" fill="${r.place===1?'var(--brass)':'var(--surface)'}" stroke="${r.place===1?'var(--brass)':'var(--ink-3)'}" stroke-width="${r.place===1?2:1.6}" data-k="${y}|${esc(r.mgr)}" data-mgr="${esc(r.mgr)}" data-yr="${y}" ${r.place===1?'data-champ="1"':''} style="cursor:pointer"/>`
        : `<circle cx="${xs(i)+off}" cy="${ys(r.pi)}" r="2" fill="var(--rule)" stroke="none"/>`;});
  });
  const lab=SEA.map((y,i)=>`<text x="${xs(i)}" y="${H-P.b+19}" text-anchor="middle" font-size="10.5" fill="var(--ink-3)" font-family="IBM Plex Mono,monospace">${y}</text>`).join('');
  $('#strip').innerHTML=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Power index of every team in every season; gold dots are champions">${g}${bands}
    <g id="stripTrails" style="pointer-events:none"></g>
    ${dots}${lab}
    <text id="stripWho" x="${P.l}" y="${P.t-2}" font-size="12" font-weight="700" fill="var(--brass)" font-family="IBM Plex Sans,sans-serif"></text></svg>`;
  const pi={}; ROWS.forEach(r=>pi[r.y+'|'+r.mgr]=r);
  $$('#strip circle[data-k]').forEach(c=>{const r=pi[c.dataset.k];
    bindTip(c,`<b>${esc(r.mgr)} · ${r.y}</b><br>${esc(r.team)}<br>Power index <b>${r.pi.toFixed(1)}</b><br>${r.w}-${r.l} · finished ${ord(r.place)}${r.place===1?' 🏆':''}`);
    c.addEventListener('click',()=>togglePick(r.mgr));
    c.addEventListener('mouseenter',()=>{HOVER=r.mgr;spotlight();});
    c.addEventListener('mouseleave',()=>{HOVER=null;spotlight();});});
  spotlight();
}
drawStrip(); REDRAW.push(drawStrip);

/* ============ luck ============ */
function drawLuck(){
  const on=$('#qLuck').classList.contains('on');
  table($('#tLuck'),[
   {h:'Manager',f:r=>mlink(r.name),c:'nm',k:r=>r.name,asc:1},
   {h:'Szns',f:r=>r.seasons,c:'num',k:r=>r.seasons},
   {h:'Luck',f:r=>f(r.luck),c:'num',k:r=>r.luck,t:'Actual wins minus Pythagorean wins'},
   {h:'',f:r=>dbar(r.luck,13,pol(r.luck)),k:r=>r.luck},
   {h:'Actual W',f:r=>r.w,c:'num',k:r=>r.w},
   {h:'Deserved W',f:r=>f(r.pythW,1),c:'num',k:r=>r.pythW},
   {h:'Actual win %',f:r=>pct(r.winpct),c:'num',k:r=>r.winpct},
   {h:'Pyth win %',f:r=>pct(r.pythW/r.g),c:'num',k:r=>r.pythW/r.g},
   {h:'Per season',f:r=>f(r.luck/r.seasons),c:'num',k:r=>r.luck/r.seasons},
  ],M.filter(m=>vis(m.name)&&(on?m.seasons>=2:true)),{rank:1,sort:2});
}
$('#qLuck').onclick=e=>{e.target.classList.toggle('on');
  e.target.textContent=e.target.classList.contains('on')?'Hide 1-season managers':'Showing everyone';drawLuck();};
drawLuck(); REDRAW.push(drawLuck);

/* ============ consistency + playoff resume ============ */
let ADVWIN=0, ADVSET=null;                 /* ADVSET = an explicit pick, overrides the window */
function advYears(){
  if(ADVSET&&ADVSET.size)return SEA.filter(y=>ADVSET.has(y));
  return ADVWIN?SEA.slice(-ADVWIN):SEA;
}
function advAgg(){
  const yy=advYears(), set=new Set(yy), END=yy[yy.length-1], out={};
  ROWS.filter(r=>set.has(r.y)).forEach(r=>{
    const m=out[r.mgr]=out[r.mgr]||{name:r.mgr,seasons:0,g:0,piW:0,zW:0,pis:[],zs:[],rec:[],
      titles:0,apps:0,expT:0,poW:0,poL:0,poG:0,poPts:0,finals:0};
    const g=r.w+r.l+r.t;
    m.seasons++; m.g+=g; m.piW+=r.pi*g; m.zW+=r.z*g; m.pis.push(r.pi); m.zs.push(r.z);
    if(r.y>=END-2)m.rec.push(r.pi);
    m.titles+=r.share; if(r.po){m.apps++;m.expT+=(r.expT!=null?r.expT:1/r.spots);}});
  D.games.filter(x=>set.has(x.y)).forEach(x=>{
    [[x.ma,x.pa,x.pb],[x.mb,x.pb,x.pa]].forEach(([n,mine,opp])=>{
      const m=out[n]; if(!m)return;
      if(x.rnd==='Final')m.finals++;
      if(x.void)return;
      m.poG++; m.poPts+=mine; if(mine>opp)m.poW++; else m.poL++;});});
  return Object.values(out).map(m=>{
    const mean=m.pis.reduce((a,b)=>a+b,0)/m.pis.length, cpi=m.piW/m.g,
          form=m.rec.length?m.rec.reduce((a,b)=>a+b,0)/m.rec.length:null;
    return {...m,cpi,peak:Math.max(...m.pis),floor:Math.min(...m.pis),
      sd:m.pis.length>1?Math.sqrt(m.pis.reduce((t,p)=>t+(p-mean)*(p-mean),0)/m.pis.length):null,
      form,trend:form==null?null:form-cpi,
      zAvg:m.zW/m.g,zPeak:Math.max(...m.zs),zFloor:Math.min(...m.zs),
      poPPG:m.poG?m.poPts/m.poG:null,vsExp:m.titles-m.expT};});
}
function drawCon(){
  const yy=advYears(), A=advAgg();
  const multi=yy.length>1, on=$('#qCon').classList.contains('on')&&multi;
  $('#qCon').disabled=!multi;
  $('#qCon').style.opacity=multi?'':'.45';
  $('#qCon').title=multi?'':'Every manager has exactly one season in a single-season window';
  const contig=yy.length===(yy[yy.length-1]-yy[0]+1)||yy.length<2;
  $('#advSub').textContent=(ADVSET&&ADVSET.size)
      ? (contig?`${yy[0]}–${yy[yy.length-1]} · ${yy.length} picked`:`${yy.length} seasons picked · ${yy.join(', ')}`)
      : ADVWIN===1?`${yy[0]} only`
      : ADVWIN?`${yy[0]}–${yy[yy.length-1]} only · ${yy.length} seasons`:`all ${SEA.length} seasons`;
  const yset=new Set(yy);
  $('#poSub').textContent=(yy.length<SEA.length
      ? (yy.length===1?`${yy[0]} · `:(contig?`${yy[0]}–${yy[yy.length-1]} · `:`${yy.length} seasons · `)) : '')
    +`${D.games.filter(g=>yset.has(g.y)).length} playoff games`;
  table($('#tCon'),[
   {h:'Manager',f:r=>mlink(r.name),c:'nm',k:r=>r.name,asc:1,t:'Click any name to open their full career card.'},
   {h:'Szns',f:r=>r.seasons,c:'num',k:r=>r.seasons,t:'Seasons played in the years currently selected above.'},
   {h:'Career PI',f:r=>f(r.cpi,1),c:'num',k:r=>r.cpi,t:'Career Power Index. Every season they played, weighted by games, on the scale where 100 is that season\'s league average. This is the headline number: above 100 means they have outscored the field over their whole career.'},
   {h:'Peak',f:r=>f(r.peak,1),c:'num',k:r=>r.peak,t:'Their best single season, on the same 100-is-average scale. How good they have ever been.'},
   {h:'Floor',f:r=>f(r.floor,1),c:'num',k:r=>r.floor,t:'Their worst single season, same scale. How bad it has ever got.'},
   {h:'Std dev',f:r=>r.sd==null?'—':f(r.sd,1),c:'num',k:r=>r.sd,t:'How far their seasons swing away from their own average. Low is a metronome, the same manager every year. High is boom or bust.'},
   {h:'Z avg',f:r=>(r.zAvg>=0?'+':'')+r.zAvg.toFixed(2),c:'num',k:r=>r.zAvg,t:'Career average, measured in how far clear of the pack they were rather than by how much. 0 is exactly average, +1 is a full standard deviation above the field. In a tightly bunched season a small scoring edge is a big Z; in a wild season the same edge is nothing.'},
   {h:'Z peak',f:r=>(r.zPeak>=0?'+':'')+r.zPeak.toFixed(2),c:'num',k:r=>r.zPeak,t:'Their best season measured the same way: how far clear of the field they got at their very best.'},
   {h:'Z floor',f:r=>(r.zFloor>=0?'+':'')+r.zFloor.toFixed(2),c:'num',k:r=>r.zFloor,t:'Their worst season measured the same way: how far behind the field they fell at their very worst.'},
   {h:(()=>{const q=advYears();const a=Math.max(q[0],q[q.length-1]-2),b=q[q.length-1];return a===b?'Form '+b:'Form '+String(a).slice(2)+'–'+String(b).slice(2);})(),f:r=>r.form==null?'—':f(r.form,1),c:'num',k:r=>r.form,t:'The last three seasons only, on the same 100-is-average scale. Who they are right now, rather than who they have been.'},
   {h:'Trend',f:r=>r.trend==null?'—':(r.trend>=0?'+':'')+r.trend.toFixed(1),c:'num',k:r=>r.trend,t:'Form minus career. A plus means they are playing better than their own history; a minus means they are falling off.'},
   {h:'',f:r=>r.trend==null?'':dbar(r.trend,9,pol(r.trend)),k:r=>r.trend,t:'The Trend column drawn as a bar. Right and warm is improving, left and cool is declining.'},
  ],A.filter(m=>vis(m.name)&&(on?m.seasons>=2:true)),{rank:1,sort:2});
  drawPO();
}
$('#qCon').onclick=e=>{e.target.classList.toggle('on');
  e.target.textContent=e.target.classList.contains('on')?'Hide 1-season managers':'Showing everyone';drawCon();};
drawCon(); REDRAW.push(drawCon);
function drawPO(){table($('#tPO'),[
 {h:'Manager',f:r=>mlink(r.name),c:'nm',k:r=>r.name,asc:1},
 {h:'Apps',f:r=>r.apps,c:'num',k:r=>r.apps},
 {h:'G',f:r=>r.poG,c:'num',k:r=>r.poG},{h:'W',f:r=>r.poW,c:'num',k:r=>r.poW},{h:'L',f:r=>r.poL,c:'num',k:r=>r.poL},
 {h:'Win %',f:r=>r.poG?pct(r.poW/r.poG):'—',c:'num',k:r=>r.poG?r.poW/r.poG:null},
 {h:'PPG',f:r=>r.poPPG==null?'—':f(r.poPPG),c:'num',k:r=>r.poPPG},
 {h:'Finals',f:r=>r.finals||'—',c:'num',k:r=>r.finals},
 {h:'Titles',f:r=>r.titles?(r.titles%1?r.titles.toFixed(1):r.titles):'—',c:'num',k:r=>r.titles},
 {h:'Expected',f:r=>f(r.expT),c:'num',k:r=>r.expT,t:'Coin flip every round: (½)^(wins needed). A first-round bye is worth double, and the season total is always exactly 1.00.'},
 {h:'vs Exp',f:r=>(r.vsExp>=0?'+':'')+r.vsExp.toFixed(2),c:'num',k:r=>r.vsExp},
 {h:'',f:r=>dbar(r.vsExp,1.3,pol(r.vsExp)),k:r=>r.vsExp},
],advAgg().filter(m=>vis(m.name)),{rank:1,sort:3});}
drawPO(); REDRAW.push(drawPO);
$('#advYrChips').innerHTML=SEA.map(y=>`<button data-advy="${y}" style="padding:4px 10px">${y}</button>`).join('')
  +`<button id="advYrAll" style="padding:4px 10px;margin-left:6px">Select all</button>`
  +`<button id="advYrNone" style="padding:4px 10px">Clear</button>`;
function syncAdvChips(){
  const on=ADVSET&&ADVSET.size;
  $$('#advYrChips [data-advy]').forEach(b=>b.classList.toggle('on',!!(on&&ADVSET.has(+b.dataset.advy))));
  $$('[data-adv]').forEach(x=>x.classList.toggle('on',!on&&+x.dataset.adv===ADVWIN));
  $('#advPick').classList.toggle('on',!!on);
}
$$('[data-adv]').forEach(b=>b.onclick=()=>{
  ADVSET=null; ADVWIN=+b.dataset.adv; syncAdvChips(); drawCon();});
$('#advPick').onclick=()=>{const c=$('#advYrChips'); c.hidden=!c.hidden;
  $('#advPick').innerHTML=c.hidden?'Pick seasons &#9662;':'Hide seasons &#9652;';};
$$('#advYrChips [data-advy]').forEach(b=>b.onclick=()=>{
  const y=+b.dataset.advy; if(!ADVSET)ADVSET=new Set();
  ADVSET.has(y)?ADVSET.delete(y):ADVSET.add(y);
  if(!ADVSET.size)ADVSET=null;
  syncAdvChips(); drawCon();});
$('#advYrAll').onclick=()=>{ADVSET=new Set(SEA);syncAdvChips();drawCon();};
$('#advYrNone').onclick=()=>{ADVSET=null;syncAdvChips();drawCon();};
syncAdvChips();

/* ============ records ============ */
function drawFive(){
  table($('#tFive'),[
   {h:'Manager',f:r=>mlink(r.name),c:'nm',k:r=>r.name,asc:1},
   {h:'Szns',f:r=>r.seasons,c:'num',k:r=>r.seasons},
   {h:'W-L',f:r=>`<span class="mono">${r.w}-${r.l}${r.t?'-'+r.t:''}</span>`,k:r=>r.w-r.l},
   {h:'Games clear',f:r=>(r.gAbove>=0?'+':'')+r.gAbove,c:'num',k:r=>r.gAbove,
    t:'Career wins minus losses. Positive means more games won than lost, over everything.'},
   {h:'',f:r=>dbar(r.gAbove,26,pol(r.gAbove)),k:r=>r.gAbove},
   {h:'Win %',f:r=>pct(r.winpct),c:'num',k:r=>r.winpct},
   {h:'vs .500',f:r=>((r.winpct-.5)>=0?'+':'')+(100*(r.winpct-.5)).toFixed(1)+'%',c:'num',k:r=>r.winpct},
   {h:'Szns +',f:r=>r.sznAbove||'—',c:'num',k:r=>r.sznAbove,t:'Seasons finished with a winning record'},
   {h:'Szns −',f:r=>r.sznBelow||'—',c:'num',k:r=>r.sznBelow,t:'Seasons finished with a losing record'},
   {h:'Weeks above',f:r=>r.wkTot?`<span class="mono">${r.wkAbove}/${r.wkTot}</span>`:'—',c:'num',k:r=>r.wkAbovePct,
    t:'Walking each week of 2021–2025: how often was this manager above .500 at that moment? Finishing 8-6 after starting 1-5 is a very different season from 8-6 wire to wire.'},
   {h:'Weeks %',f:r=>r.wkAbovePct==null?'—':pct(r.wkAbovePct),c:'num',k:r=>r.wkAbovePct},
   {h:'',f:r=>r.wkAbovePct==null?'':dbar(r.wkAbovePct-.5,.5,pol(r.wkAbovePct-.5)),k:r=>r.wkAbovePct},
   {h:'Best run',f:r=>r.wkStreak||'—',c:'num',k:r=>r.wkStreak,t:'Longest unbroken run of weeks spent above .500'},
   {h:'vs winners',f:r=>(r.vsWinW+r.vsWinL)?`<span class="mono">${r.vsWinW}-${r.vsWinL}</span>`:'—',c:'num',k:r=>r.vsWinPct,
    t:'Record against opponents who finished that season above .500. Almost nobody is above .500 here and that is arithmetic, not weakness: when a winning team plays a losing one, that game counts as "vs the rest" for the winner and "vs a winner" for the loser, so this column is loaded with the games losing teams played. League-wide it sits at .383 while "vs the rest" sits at .620. Compare managers against each other, not against .500. Covers every playoff game in league history plus the 2021 to 2025 regular seasons; earlier regular seasons have no game log.'},
   {h:'vs win %',f:r=>r.vsWinPct==null?'—':pct(r.vsWinPct),c:'num',k:r=>r.vsWinPct},
   {h:'vs the rest',f:r=>(r.vsSubW+r.vsSubL)?`<span class="mono">${r.vsSubW}-${r.vsSubL}</span>`:'—',c:'num',k:r=>r.vsSubPct,
    t:'Record against opponents who finished .500 or worse.'},
   {h:'Step-up',f:r=>r.vsGap==null?'—':(r.vsGap>=0?'+':'')+(100*r.vsGap).toFixed(1)+'%',c:'num',k:r=>r.vsGap,
    t:'Win rate against winning teams minus win rate against the rest. Everyone is negative — good teams are harder. The question is by how much: a small gap means they play the same against anyone, a big one means they feast on the weak and fold against the strong.'},
   {h:'Exp vs avg',f:r=>(r.expOverAvg>=0?'+':'')+r.expOverAvg.toFixed(2),c:'num',k:r=>r.expOverAvg,
    t:'Pythagorean expected wins minus half their games — how many wins the scoring alone earned above a perfectly average team. Schedule plays no part.'},
   {h:'Luck gap',f:r=>((r.w+r.t/2-r.g/2)-r.expOverAvg>=0?'+':'')+((r.w+r.t/2-r.g/2)-r.expOverAvg).toFixed(2),c:'num',
    k:r=>(r.w+r.t/2-r.g/2)-r.expOverAvg,
    t:'Actual wins above average minus expected wins above average. Positive means the record flatters the scoring.'},
  ],M.filter(m=>vis(m.name)),{rank:1,sort:3});
}
drawFive(); REDRAW.push(drawFive);
$('#fiveMore').onclick=()=>{const t=$('#fiveTbl'); t.hidden=!t.hidden;
  $('#fiveMore').classList.toggle('on',!t.hidden);
  $('#fiveMore').innerHTML=t.hidden?'Show table &#9662;':'Hide table &#9652;';};
function drawRecords(){
  const ROWS=D.rows.filter(r=>vis(r.mgr)), M=D.mgrs.filter(m=>vis(m.name));
  const q=M.filter(m=>m.seasons>=2);
  const S=(a,k,d=1)=>[...a].sort((x,y)=>d?k(y)-k(x):k(x)-k(y)).slice(0,5);
  const sr=(r,v)=>`<td class="nm">${mlink(r.mgr)}</td><td class="tm">${esc(r.team)}</td><td class="num mono">${r.y}</td><td class="num"><b>${v}</b></td>`;
  const cr=(m,v)=>`<td class="nm">${mlink(m.name)}</td><td class="dim">${m.seasons} seasons</td><td></td><td class="num"><b>${v}</b></td>`;
  const B=[['SINGLE SEASON',null],
   ['Highest PPG',S(ROWS,r=>r.ppg).map(r=>sr(r,r.ppg.toFixed(2)))],
   ['Lowest PPG',S(ROWS,r=>r.ppg,0).map(r=>sr(r,r.ppg.toFixed(2)))],
   ['Highest power index',S(ROWS,r=>r.pi).map(r=>sr(r,r.pi.toFixed(1)))],
   ['Lowest power index',S(ROWS,r=>r.pi,0).map(r=>sr(r,r.pi.toFixed(1)))],
   ['Best Z-score',S(ROWS,r=>r.z).map(r=>sr(r,r.z.toFixed(2)))],
   ['Best differential per game',S(ROWS,r=>(r.pf-r.pa)/r.g).map(r=>sr(r,((r.pf-r.pa)/r.g).toFixed(2)))],
   ['Worst differential per game',S(ROWS,r=>(r.pf-r.pa)/r.g,0).map(r=>sr(r,((r.pf-r.pa)/r.g).toFixed(2)))],
   ['Luckiest season',S(ROWS,r=>r.luck).map(r=>sr(r,r.luck.toFixed(2)))],
   ['Unluckiest season',S(ROWS,r=>r.luck,0).map(r=>sr(r,r.luck.toFixed(2)))],
   ['Most roster moves',S(ROWS.filter(r=>r.mv!=null),r=>r.mv).map(r=>sr(r,r.mv))],
   ['COUNTING RECORDS &mdash; totals, not comparable across seasons',null],
   ['Most points in a season',S(ROWS,r=>r.pf).map(r=>sr(r,r.pf.toFixed(2)+' <span class="dim">/'+r.g+'g</span>'))],
   ['Fewest points in a season',S(ROWS,r=>r.pf,0).map(r=>sr(r,r.pf.toFixed(2)+' <span class="dim">/'+r.g+'g</span>'))],
   ['CAREER RATES &mdash; 2+ seasons',null],
   ['Best win %',S(q,m=>m.winpct).map(m=>cr(m,(100*m.winpct).toFixed(1)+'%'))],
   ['Worst win %',S(q,m=>m.winpct,0).map(m=>cr(m,(100*m.winpct).toFixed(1)+'%'))],
   ['Best average finish',S(q,m=>m.avgPlace,0).map(m=>cr(m,m.avgPlace.toFixed(2)))],
   ['Best power index',S(q,m=>m.cpi).map(m=>cr(m,m.cpi.toFixed(1)))],
   ['Worst power index',S(q,m=>m.cpi,0).map(m=>cr(m,m.cpi.toFixed(1)))],
   ['Luckiest career',S(q,m=>m.luck).map(m=>cr(m,m.luck.toFixed(2)))],
   ['Unluckiest career',S(q,m=>m.luck,0).map(m=>cr(m,m.luck.toFixed(2)))],
   ['CAREER TOTALS &mdash; everyone, short careers included',null],
   ['Most career points',S(M,m=>m.pf).map(m=>cr(m,m.pf.toFixed(0)))],
   ['Most playoff wins',S(M,m=>m.poW).map(m=>cr(m,m.poW))]];
  let h='',open=false;
  B.forEach(([t,rows])=>{
    if(!rows){if(open)h+='</div>';
      h+=`<h3 style="font-size:13px;letter-spacing:.11em;text-transform:uppercase;color:var(--brass);font-family:'IBM Plex Mono',monospace;margin:26px 0 12px;font-weight:600">${t}</h3><div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,330px),1fr));gap:16px">`;open=true;return;}
    const lt=t.toLowerCase();
    const gk=lt.includes('power index')?'pi':lt.includes('z-score')?'z':lt.includes('luck')?'luck':null;
    h+=`<div class="card"><div class="card-h"><h3>${t}</h3>${gk?`<span class="gl" data-gl="${gk}" tabindex="0">?</span>`:''}</div><div class="scroll"><table>${
      rows.map((r,i)=>`<tr><td class="rk">${i+1}</td>${r}</tr>`).join('')}</table></div></div>`;});
  $('#recs').innerHTML=h+(open?'</div>':'');
  glossify($('#recs'));
}
drawRecords(); REDRAW.push(drawRecords);
/* The record book is 21 tables and the milestone list. Collapsed by default so the
   sections below it are reachable without a long scroll. */
(function(){
  const t=$('#recsToggle'), w=$('#recsWrap'), c=$('#recsCount');
  if(!t||!w)return;
  const sync=()=>{const open=!w.hidden;
    t.innerHTML=open?'Hide the record book &#9652;':'Show the record book &#9662;';
    t.classList.toggle('on',open);
    if(c)c.textContent=open?'':`${$$('#recs .card').length||21} tables`;};
  t.onclick=()=>{w.hidden=!w.hidden;sync();};
  sync();
})();

/* ============ seasons + real bracket ============ */
const ORD=['Quarterfinal','Semifinal','5th Place Game','Final','3rd Place Game'];
/* known round names straight from the bracket data, plus a derived fallback */
const GKEY=(y,wk,a,b)=>y+'|'+wk+'|'+[a,b].sort().join('~');
const RNDMAP={}, VOIDMAP={};
D.games.forEach(g=>{const k=GKEY(g.y,g.wk,g.ta,g.tb); RNDMAP[k]=g.rnd; if(g.void)VOIDMAP[k]=1;});
const isVoid=(y,wk,a,b)=>!!VOIDMAP[GKEY(y,wk,a,b)];
function poWeeks(K){return [...new Set(K.games.filter(g=>g.br).map(g=>g.wk))].sort((a,b)=>a-b);}
function roundName(y,K,g){
  const hit=RNDMAP[y+'|'+g.wk+'|'+[g.ta,g.tb].sort().join('~')];
  if(hit)return hit;
  if(!g.br)return '';
  const pw=poWeeks(K), i=pw.indexOf(g.wk), n=pw.length;
  if(g.br==='C')return (n>=3?['Quarterfinal','Semifinal','Final']:['Semifinal','Final'])[Math.max(0,i-(n-(n>=3?3:2)))]||'Championship';
  return i===n-1?'Consolation final':'Consolation round '+(i+1);
}
function byeName(K,b){
  const pw=poWeeks(K), i=pw.indexOf(b.wk), n=pw.length;
  if(b.br==='C')return (n>=3&&i===0)?'Quarterfinal bye':'First-round bye';
  return 'Consolation bye';}
function drawSeason(y){
  $$('#yrPills button').forEach(b=>b.classList.toggle('on',+b.dataset.y===y));
  const rs=ROWS.filter(r=>r.y===y).sort((a,b)=>a.seed-b.seed);
  const c=D.champs.find(c=>c.y===y);
  const gs=D.games.filter(g=>g.y===y);
  const wks=[...new Set(gs.map(g=>g.wk))].sort((a,b)=>a-b);
  const seedOf={}; rs.forEach(r=>seedOf[r.team]=r.seed);
  const byes=wks.length?rs.filter(r=>r.seed<=c.spots&&!gs.some(g=>g.wk===wks[0]&&(g.ta===r.team||g.tb===r.team))):[];
  let cols='';
  wks.forEach((wk,wi)=>{
    const gg=gs.filter(g=>g.wk===wk).sort((a,b)=>ORD.indexOf(a.rnd)-ORD.indexOf(b.rnd));
    let inner=gg.map(g=>{
      const aw=g.pa>g.pb,vd=g.void;
      const side=(t,m,p,win)=>`<div class="side ${vd?'':(win?'w':'lo')}" data-team="${esc(t)}"><span class="sd">${seedOf[t]||''}</span><span class="tn">${esc(t)}<small>${esc(m)}</small></span><span class="sc">${p.toFixed(2)}</span></div>`;
      return `<div class="game${vd?' void':''}" data-g="${esc(g.ta)}|${esc(g.tb)}"><div class="gh">${vd?'Final — VOID':esc(g.rnd)}</div>${side(g.ta,g.ma,g.pa,aw)}${side(g.tb,g.mb,g.pb,!aw)}</div>`;}).join('');
    if(wi===0&&byes.length) inner+=byes.map(b=>`<div class="game" data-g="${esc(b.team)}"><div class="gh">First-round bye</div>
      <div class="side bye" data-team="${esc(b.team)}"><span class="sd">${b.seed}</span><span class="tn">${esc(b.team)}<small>${esc(b.mgr)}</small></span><span class="sc">—</span></div></div>`).join('');
    cols+=`<div class="round" data-wk="${wk}"><h4>Week ${wk}</h4>${inner}</div>`;});
  const champT=c.teams.map(esc).join(' &amp; ');
  cols+=`<div class="round" style="flex:0 0 176px"><h4>Champion</h4><div class="brk-champ">
    <div class="s" style="color:${pickInk(cssv('--brass-wash'))}">${c.co?'Co-champions':'Champion'}</div><div class="t">${champT}</div>
    <div style="font-size:11.5px;color:var(--ink-2);margin-top:5px">${c.mgrs.map(esc).join(' &amp; ')}</div></div></div>`;
  $('#seasonPane').innerHTML=`
    <div class="card"><div class="card-h"><h3>${y} standings</h3>
      <span class="sub">${c.n} teams · ${c.g}-game season · ${c.spots}-team bracket · league avg ${c.lg.toFixed(2)} PPG</span>
      <div class="right"><button id="seaShare" style="padding:7px 13px">&#8593; Share the season</button>
        <button data-link="y=${y}" data-link-hash="seasons" style="padding:7px 13px;margin-left:6px">&#128279; Copy link</button></div></div>
      <div class="scroll"><table id="tS"></table></div></div>
    <div class="card"><div class="card-h"><h3>${y} bracket</h3>
      <span class="sub">${c.co?'Final voided — title split':'Hover a team to trace its run · click to lock it'}</span>
      <span class="sub" id="brkTrace" style="color:var(--brass)"></span>
      <div class="right"><button id="brkShare" style="padding:7px 13px">&#8593; Share the bracket</button></div></div>
      <div class="card-b"><div class="brk"><svg class="conn" id="conn" aria-hidden="true"></svg><div class="brk-in" id="brkIn">${cols}</div></div></div></div>`;
  table($('#tS'),[
   {h:'Seed',f:r=>r.seed,c:'num',k:r=>r.seed,asc:1},
   {h:'Team',f:r=>esc(r.team),c:'nm',k:r=>r.team,asc:1},
   {h:'Manager',f:r=>mlink(r.mgr),k:r=>r.mgr,asc:1},
   {h:'W-L-T',f:r=>`<span class="mono">${r.w}-${r.l}-${r.t}</span>`,k:r=>r.w},
   {h:'PF',f:r=>f(r.pf),c:'num',k:r=>r.pf},{h:'PA',f:r=>f(r.pa),c:'num',k:r=>r.pa},
   {h:'PPG',f:r=>f(r.ppg),c:'num',k:r=>r.ppg},
   {h:'Power idx',f:r=>f(r.pi,1),c:'num',k:r=>r.pi},
   {h:'Z',f:r=>(r.z>=0?'+':'')+r.z.toFixed(2),c:'num',k:r=>r.z,t:'Standard deviations from that season\u2019s mean PPG. Power index says how much better; Z says how far clear of the pack, which matters more in a tightly bunched year.'},
   {h:'Luck',f:r=>f(r.luck),c:'num',k:r=>r.luck},
   {h:'Moves',f:r=>r.mv==null?'—':r.mv,c:'num',k:r=>r.mv},
   {h:'Finish',f:r=>r.place===1?`<span class="chip y">${r.co?'Co-champion':'Champion'}</span>`:ord(r.place),c:'num',k:r=>r.place,asc:1},
  ],rs,{sort:0,dir:'asc',cls:r=>(r.place===1?'champ ':'')});
  drawSchedule(y);
  drawConnectors(gs);
  $$('#brkIn .side[data-team]').forEach(s=>{
    s.addEventListener('mouseenter',()=>hiTeam(s.dataset.team));
    s.addEventListener('mouseleave',()=>hiTeam(null));
    s.addEventListener('click',()=>{LOCKTEAM=LOCKTEAM===s.dataset.team?null:s.dataset.team;hiTeam(null);});});
  hiTeam(null);
}
function drawSchedule(y){
  const K=(D.wk||{})[y];
  if(!K){$('#schedPane').innerHTML=`<div class="card"><div class="card-h"><h3>${y} schedule</h3>
    <span class="sub">no game log loaded</span></div><div class="card-b"><p style="margin:0;font-size:13.5px;color:var(--ink-2)">
    Week-by-week results for ${y} have not been captured yet. Only the final standings and the bracket exist for this season.</p></div></div>`;return;}
  const MG=K.mgr, wks=[...new Set(K.games.map(g=>g.wk))].sort((a,b)=>a-b);
  const label=g=>roundName(y,K,g);
  let out=`<div class="card"><div class="card-h"><h3>${y} schedule</h3>
    <span class="sub">${K.games.length} games · every week · winner in bold</span>
    <div class="right"><button id="schedToggle">Expand all</button></div></div><div class="card-b" id="schedBody">`;
  wks.forEach(w=>{
    const gs=K.games.filter(g=>g.wk===w), by=K.byes.filter(b=>b.wk===w);
    const all=gs.flatMap(g=>[g.aa,g.ab]).concat(by.map(b=>b.a));
    const hi=Math.max(...all), lo=Math.min(...all);
    out+=`<details class="wk"><summary>Week ${w} <span class="dim">${gs.length} game${gs.length===1?'':'s'}${by.length?' · '+by.length+' bye'+(by.length===1?'':'s'):''}</span></summary>
      <div class="wkgrid">`+
      gs.map(g=>{const vd=isVoid(y,g.wk,g.ta,g.tb), aw=g.aa>g.ab, dim=vd?' void':'';
        const side=(t,pt,pr,win)=>`<div class="side ${vd?'':(win?'w':'lo')}"><span class="tn">${esc(t)}<small>${esc(MG[t]||'')} · proj ${pr.toFixed(1)}</small></span>
          <span class="sc">${pt.toFixed(2)}</span>${pt===hi?'<span class="chip y" style="margin-left:6px">high</span>':pt===lo?'<span class="chip" style="margin-left:6px;border-color:var(--neg);color:var(--neg)">low</span>':''}</div>`;
        return `<div class="game${dim}"><div class="gh">${vd?(label(g)||'Week '+w)+' — VOID':(label(g)||'Week '+w)+' · margin '+Math.abs(g.aa-g.ab).toFixed(2)}</div>${side(g.ta,g.aa,g.pa,aw)}${side(g.tb,g.ab,g.pb,!aw)}</div>`;}).join('')
      + by.map(b=>`<div class="game"><div class="gh">${byeName(K,b)}</div><div class="side bye"><span class="tn">${esc(b.t)}<small>${esc(MG[b.t]||'')}</small></span><span class="sc">${b.a.toFixed(2)}</span></div></div>`).join('')
      +`</div></details>`;});
  $('#schedPane').innerHTML=out+'</div></div>';
  $('#schedToggle').onclick=e=>{const anyOpen=$$('#schedBody details').some(d=>d.open);
    $$('#schedBody details').forEach(d=>d.open=!anyOpen);
    e.target.textContent=anyOpen?'Expand all':'Collapse all';};
}
let LOCKTEAM=null;
function hiTeam(t){
  const x=t||LOCKTEAM;
  $$('#brkIn .side').forEach(s=>s.classList.toggle('act',!!x&&s.dataset.team===x));
  $$('#brkIn .game').forEach(g=>g.classList.toggle('hi',!!x&&(g.dataset.g||'').split('|').includes(x)));
  $$('#conn path').forEach(p=>{const on=!!x&&p.dataset.team===x;
    p.setAttribute('stroke',on?'var(--brass)':'var(--rule)');p.setAttribute('stroke-width',on?2.4:1.4);});
  const b=$('#brkTrace'); if(b)b.textContent=LOCKTEAM?('tracing '+LOCKTEAM+' — click to clear'):'';
}
function drawConnectors(gs){
  const svg=$('#conn'),wrap=$('#brkIn'); if(!svg||!wrap)return;
  const W=wrap.scrollWidth,H=wrap.scrollHeight;
  svg.setAttribute('viewBox',`0 0 ${W} ${H}`); svg.setAttribute('width',W); svg.setAttribute('height',H);
  const box=wrap.getBoundingClientRect();
  const el={}; $$('#brkIn .game').forEach(g=>{(g.dataset.g||'').split('|').forEach(t=>{(el[t]=el[t]||[]).push(g);});});
  let paths='';
  gs.forEach(g=>{
    const node=$$('#brkIn .game').find(x=>x.dataset.g===g.ta+'|'+g.tb); if(!node)return;
    [g.ta,g.tb].forEach(t=>{
      const prev=(el[t]||[]).filter(x=>x!==node&&x.closest('.round')&&+x.closest('.round').dataset.wk<g.wk);
      if(!prev.length)return;
      const from=prev[prev.length-1].getBoundingClientRect(), to=node.getBoundingClientRect();
      const x1=from.right-box.left+wrap.scrollLeft, y1=from.top+from.height/2-box.top;
      const x2=to.left-box.left+wrap.scrollLeft, y2=to.top+to.height/2-box.top;
      const mx=(x1+x2)/2;
      paths+=`<path d="M${x1},${y1} H${mx} V${y2} H${x2}" fill="none" stroke="var(--rule)" stroke-width="1.4" data-team="${esc(t)}"/>`;});});
  svg.innerHTML=paths;
}
$('#yrPills').innerHTML=SEA.map(y=>`<button data-y="${y}">${y}</button>`).join('');
$$('#yrPills button').forEach(b=>b.onclick=()=>{LOCKTEAM=null;drawSeason(+b.dataset.y);});
drawSeason(LAST);
REDRAW.push(()=>{const on=$$('#yrPills button.on')[0]; if(on)drawSeason(+on.dataset.y);});
addEventListener('resize',()=>{const on=$$('#yrPills button.on')[0]; if(on)drawConnectors(D.games.filter(g=>g.y===+on.dataset.y));});

/* ============ h2h: regular season, playoffs, combined ============ */
const REGG=[];           /* regular-season meetings across every loaded game log */
(D.wkYears||[]).forEach(y=>{const K=D.wk[y];
  K.games.filter(g=>g.br==='').forEach(g=>
    REGG.push({y,wk:g.wk,ma:K.mgr[g.ta],mb:K.mgr[g.tb],pa:g.aa,pb:g.ab,lab:y+' week '+g.wk}));});
const REGYRS=(D.wkYears||[]).join(' and ');
const POG=D.games.filter(g=>!g.void).map(g=>({y:g.y,ma:g.ma,mb:g.mb,pa:g.pa,pb:g.pb,lab:g.y+' '+g.rnd}));
function tally(list){const t={};
  list.forEach(g=>{const w=g.pa>g.pb?g.ma:g.mb,l=g.pa>g.pb?g.mb:g.ma;
    (t[w+'|'+l]=t[w+'|'+l]||[0,0])[0]++; (t[l+'|'+w]=t[l+'|'+w]||[0,0])[1]++;});
  return t;}
const MX={reg:{t:tally(REGG),g:REGG,
   title:'Regular-season head-to-head',
   note:REGYRS+' only — '+REGG.length+' games. The remaining seasons\' game logs have not been loaded yet, so this grid is thin by necessity, not by design.'},
  po:{t:tally(POG),g:POG,
   title:'Playoff head-to-head',
   note:'All 55 playoff games, 2015 to 2025. The voided 2022 final is excluded, so Burke and Kaiper show nothing from it.'},
  all:{t:tally(REGG.concat(POG)),g:REGG.concat(POG),
   title:'All games',
   note:'Every meeting on record: all ten seasons of playoffs plus the '+REGYRS+' regular seasons. '+(REGG.length+POG.length)+' games.'}};
let MXK='all';
function drawMtx(){
  const src=MX[MXK], ord=[...M].filter(m=>vis(m.name)).sort(bySeasons).map(m=>m.name);
  $('#mtxTitle').textContent=src.title; $('#mtxNote').textContent=src.note;
  let h='<thead><tr><th class="rw"></th>'+ord.map(n=>`<th class="v">${esc(n)}</th>`).join('')+'<th class="v">TOTAL</th></tr></thead><tbody>';
  ord.forEach(a=>{h+=`<tr><th class="rw">${mlink(a)}</th>`;let tw=0,tl=0;
    ord.forEach(b=>{
      if(a===b){h+='<td class="self"><span>—</span></td>';return;}
      const v=src.t[a+'|'+b];
      if(!v){h+='<td><span></span></td>';return;}
      tw+=v[0];tl+=v[1];
      const rate=v[0]/(v[0]+v[1])-.5;
      h+=`<td data-a="${esc(a)}" data-b="${esc(b)}"><span style="background:${diverge(rate,.5)};color:${inkOn(rate,.5)}">${v[0]}-${v[1]}</span></td>`;});
    h+=`<td><span style="font-weight:600">${tw+tl?tw+'-'+tl:''}</span></td></tr>`;});
  $('#tMtx').innerHTML=h+'</tbody>';
  $$('#tMtx td[data-a]').forEach(td=>{const a=td.dataset.a,b=td.dataset.b,v=src.t[a+'|'+b];
    const g=src.g.filter(x=>(x.ma===a&&x.mb===b)||(x.ma===b&&x.mb===a))
      .sort((x,y)=>x.y-y.y||(x.wk||0)-(y.wk||0));
    bindTip(td,`<b>${esc(a)} vs ${esc(b)}</b><br>${v[0]}–${v[1]}<br>`+
      g.map(x=>`${esc(x.lab)}: <b>${esc(x.pa>x.pb?x.ma:x.mb)}</b> ${Math.max(x.pa,x.pb).toFixed(2)}–${Math.min(x.pa,x.pb).toFixed(2)}`).join('<br>'));});
}
$$('.pills button[data-mx]').forEach(b=>b.onclick=()=>{
  $$('.pills button[data-mx]').forEach(x=>x.classList.toggle('on',x===b)); MXK=b.dataset.mx; drawMtx();});
drawMtx(); REDRAW.push(drawMtx);
(function(){
  /* the list was built once from every manager, so it ignored the filter at the top
     and never changed when that filter did. Rebuild it on each redraw, keeping the
     current pick when that person is still shown. */
  function fillPickers(){
    const names=M.filter(m=>vis(m.name)).map(m=>m.name).sort();
    const set=(sel,fallback)=>{
      const cur=sel.value;
      sel.innerHTML=names.map(x=>`<option>${esc(x)}</option>`).join('');
      sel.value=names.indexOf(cur)>-1?cur:(names.indexOf(fallback)>-1?fallback:(names[0]||''));
    };
    set($('#cmpA'),'Brian Burke');
    set($('#cmpB'),'Shane Kaiper');
    if(names.length>1&&$('#cmpA').value===$('#cmpB').value){
      const other=names.filter(x=>x!==$('#cmpA').value)[0];
      if(other)$('#cmpB').value=other;
    }
  }
  fillPickers();
  function draw(){
    const a=byName[$('#cmpA').value],b=byName[$('#cmpB').value];
    if(!a||!b||a===b){$('#cmpOut').innerHTML='<p class="dim" style="margin:0">Pick two different managers.</p>';return;}
    const splits=[['Regular season','reg'],['Playoffs','po'],['All games','all']];
    const rows=[['Seasons','seasons',0],['Titles','titles',1],['Podiums','podium',0],['Playoff apps','apps',0],
      ['Win %','winpct',3],['Avg finish','avgPlace',2],['PPG','ppg',2],['Power index','cpi',1],
      ['Luck','luck',2],['Playoff W','poW',0]];
    const cell=(m,k,d)=>k==='winpct'?pct(m[k]):(d?(+m[k]).toFixed(d):m[k]);
    const better=(k,x,y)=>k==='avgPlace'?x<y:x>y;
    {const sh=$('#cmpShare'); if(sh)sh.onclick=()=>shareH2H($('#cmpA').value,$('#cmpB').value,sh);}
    {const rv=$('#cmpRiv'); if(rv)rv.onclick=()=>{const a=$('#cmpA').value,b=$('#cmpB').value;
      shareAny(()=>makeRivalryCard(a,b),'deadshot-'+slug(a)+'-every-meeting-'+slug(b)+'.png',rv);};}
    $('#cmpOut').innerHTML=`<div style="display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start;max-width:100%">
      <table style="flex:1 1 300px;min-width:0"><thead><tr><th></th><th class="num">${esc(a.name)}</th><th class="num">${esc(b.name)}</th></tr></thead><tbody>${
      rows.map(([lab,k,d])=>{const x=a[k],y=b[k];
        return `<tr><td>${lab}</td>
          <td class="num" style="${better(k,x,y)?'font-weight:700;color:var(--brass)':''}">${cell(a,k,d)}</td>
          <td class="num" style="${better(k,y,x)?'font-weight:700;color:var(--brass)':''}">${cell(b,k,d)}</td></tr>`;}).join('')}
      </tbody></table>
      <div style="flex:0 0 240px;padding:14px;border:1px solid var(--rule);border-radius:3px;background:var(--surface-2)">
        ${(()=>{const all=MX.all.t[a.name+'|'+b.name];
          if(!all)return '<p class="dim" style="margin:0;font-size:13px">These two have never met in any game on record.</p>';
          let o=`<div style="font-family:Fraunces,serif;font-size:30px;font-weight:900;color:var(--brass);line-height:1">${all[0]}–${all[1]}</div>
            <div class="dim" style="font-size:12px;margin-bottom:8px">${esc(a.name)}'s all-time record</div>`;
          splits.slice(0,2).forEach(([lab,k])=>{const v=MX[k].t[a.name+'|'+b.name];
            o+=`<div style="font-size:12px;border-top:1px solid var(--rule-2);padding:4px 0"><span class="dim">${lab}</span> <b>${v?v[0]+'–'+v[1]:'—'}</b></div>`;});
          o+=MX.all.g.filter(x=>(x.ma===a.name&&x.mb===b.name)||(x.ma===b.name&&x.mb===a.name))
            .sort((x,y)=>x.y-y.y||(x.wk||0)-(y.wk||0))
            .map(x=>`<div style="font-size:12px;border-top:1px solid var(--rule-2);padding:5px 0">${esc(x.lab)}<br><b>${esc(x.pa>x.pb?x.ma:x.mb)}</b> ${Math.max(x.pa,x.pb).toFixed(2)}–${Math.min(x.pa,x.pb).toFixed(2)}</div>`).join('');
          return o;})()}
      </div></div>`;
  }
  $('#cmpA').onchange=draw; $('#cmpB').onchange=draw; draw();
  REDRAW.push(()=>{fillPickers();draw();});
})();

/* ============ week-by-week, per season ============ */
const WKYEARS=D.wkYears||[];
$('#wkYears').innerHTML='<span class="fb-lab" style="margin-right:4px">Season</span>'+
  SEA.map(y=>WKYEARS.includes(y)
    ? `<button data-wy="${y}">${y}</button>`
    : `<button disabled title="no game log loaded" style="opacity:.32;cursor:not-allowed">${y}</button>`).join('')
  +'<span class="now" id="wkNow"></span>';
let WKREDRAW=[];
/* ---- career races: the bump chart re-cut by manager, one line per season ----
   Weekly logs only exist for D.wkYears (2021-2025), so this can never show a
   manager's full career -- the picker counts and the caption both say so rather
   than silently drawing a shorter line. Seasons are told apart three ways at once:
   a recency colour ramp (--mid -> --brass, newest brightest), a year label at the
   end of every line, and a legend you can click to isolate one season. */
let CRMGR=null; const CRLOCK=new Set(); let CRHOV=null;
function crSeasons(name){
  return (D.wkYears||[]).slice().sort((a,b)=>a-b).map(y=>{
    const K=D.wk[y]; if(!K)return null;
    const team=K.teams.find(t=>K.mgr[t]===name);
    return team?{y:+y,team,K}:null;}).filter(Boolean);
}
function crRank(K){
  const T=K.teams, R={}; T.forEach(t=>R[t]=[]);
  K.weeks.forEach((w,i)=>{
    const snap=T.map(t=>{const seq=K.race[t];
      return {t,wins:seq[i].wins,pf:seq.slice(0,i+1).reduce((s,x)=>s+x.pts,0)};});
    snap.sort((x,y)=>y.wins-x.wins||y.pf-x.pf);
    snap.forEach((o,k)=>R[o.t].push({w,rank:k+1,wins:o.wins,pf:o.pf}));});
  return R;
}
function drawCareerRace(){
  const host=$('#crace'); if(!host)return;
  const YRS=(D.wkYears||[]).slice().sort((a,b)=>a-b);
  if(!YRS.length){host.innerHTML='';return;}
  {const sp=$('#crSpan'); if(sp)sp.textContent=YRS[0]+'–'+YRS[YRS.length-1];}
  /* everyone who appears in at least one logged season, most seasons first */
  const tally={};
  YRS.forEach(y=>Object.values(D.wk[y].mgr).forEach(m=>{tally[m]=(tally[m]||0)+1;}));
  const names=Object.keys(tally).sort((a,b)=>tally[b]-tally[a]||a.localeCompare(b));
  if(!CRMGR||!tally[CRMGR])CRMGR=names[0];
  $('#crPick').innerHTML=`<span class="fb-lab" style="margin-right:4px">Manager</span>`+
    names.map(n=>`<button data-cm="${esc(n)}" style="padding:4px 9px">${esc(n)} <span class="dim">${tally[n]}</span></button>`).join('');
  $$('#crPick button[data-cm]').forEach(b=>{
    b.classList.toggle('on',b.dataset.cm===CRMGR);
    b.onclick=()=>{CRMGR=b.dataset.cm;CRLOCK.clear();CRHOV=null;drawCareerRace();};});

  const S=crSeasons(CRMGR);
  if(!S.length){host.innerHTML='<p style="margin:0;color:var(--ink-3);font-size:13px">No game log for this manager yet.</p>';$('#crLeg').innerHTML='';return;}
  const MAXW=Math.max(...S.map(s=>s.K.weeks.length));
  const NT=Math.max(...S.map(s=>s.K.teams.length));
  const W=980,H=392,P={t:22,r:172,b:34,l:46};
  const NCOL=MAXW+1;
  const xs=i=>P.l+i*(W-P.l-P.r)/(NCOL-1);
  const FINX=xs(NCOL-1);
  const ys=r=>P.t+(r-1)*(H-P.t-P.b)/(NT-1);
  const PLACE={}; ROWS.forEach(r=>{PLACE[r.y+'|'+r.team]=r.place;});
  const MEDAL={1:{f:'#D9A82B',s:'#8A6710',i:'#3A2A05'},2:{f:'#AEB6BD',s:'#6E767D',i:'#2B3035'},3:{f:'#B9793F',s:'#7A4B20',i:'#2E1A08'}};
  /* Seasons have to be told apart at a glance, and a one-hue brightness ramp was not
     enough -- on several skins the middle years blurred into each other. Each season now
     carries its own hue AND its own dash pattern, keyed to the YEAR rather than to this
     manager's place in the list, so 2021 is the same colour on every manager's chart.
     Two independent cues means it survives a screenshot, a printout, and colour
     blindness. The hues are per-skin tokens because all six grounds differ. */
  const NSEA=8;
  const YIDX={}; YRS.forEach((y,k)=>{YIDX[y]=k;});
  const seaK=y=>YIDX[y]%NSEA;
  const col=y=>cssv('--sea-'+(seaK(y)+1))||cssv('--brass');
  const WID=2.4, RAD=3.8;

  let grid='';
  for(let r=1;r<=NT;r++){
    grid+=`<line x1="${P.l}" x2="${W-P.r}" y1="${ys(r)}" y2="${ys(r)}" stroke="var(--rule-2)"/>`+
      `<text x="${P.l-11}" y="${ys(r)+4}" text-anchor="end" font-size="10.5" fill="var(--ink-3)" font-family="IBM Plex Mono,monospace">${r}</text>`;}
  const GAPX=(xs(MAXW-1)+FINX)/2;
  grid+=`<line x1="${GAPX}" x2="${GAPX}" y1="${P.t-14}" y2="${H-P.b+4}" stroke="var(--rule)" stroke-dasharray="3 4"/>`+
    `<text x="${GAPX}" y="${P.t-19}" text-anchor="middle" font-size="9" fill="var(--ink-3)" font-family="IBM Plex Mono,monospace" letter-spacing="1.6">FINISH</text>`;
  for(let i=0;i<MAXW;i++){
    grid+=`<text x="${xs(i)}" y="${H-P.b+18}" text-anchor="middle" font-size="9.5" fill="var(--ink-3)" font-family="IBM Plex Mono,monospace">${i+1}</text>`;}
  grid+=`<text x="${P.l-11}" y="${H-P.b+18}" text-anchor="end" font-size="9" fill="var(--ink-3)" font-family="IBM Plex Mono,monospace">WK</text>`;

  const lines=S.map((s,i)=>{
    const R=crRank(s.K)[s.team];
    const d=R.map((p,k)=>(k?'L':'M')+xs(k)+','+ys(p.rank)).join(' ');
    const endRank=R[R.length-1].rank, fp=PLACE[s.y+'|'+s.team]||endRank;
    return {y:s.y,team:s.team,K:s.K,R,d,c:col(s.y),w:WID,r:RAD,seedRank:endRank,fin:fp,moved:endRank-fp,
            fx:FINX,fy:ys(fp),
            tail:`M${xs(R.length-1)},${ys(endRank)} L${FINX},${ys(fp)}`};});
  /* two seasons can finish in the same place; fan those apart like the season chart does */
  const tie={}; lines.forEach(l=>{(tie[l.fin]=tie[l.fin]||[]).push(l);});
  Object.values(tie).forEach(g=>g.forEach((l,j)=>{
    const k=g.length, off=k>1?(j-(k-1)/2):0;
    l.fy=ys(l.fin)+off*11; l.fx=FINX+(k>1?off*8:0);
    l.tail=`M${xs(l.R.length-1)},${ys(l.seedRank)} L${l.fx},${l.fy}`;}));

  const paths=lines.map(l=>
    `<path class="crl" d="${l.d}" fill="none" stroke="${l.c}" stroke-width="${l.w}" stroke-linejoin="round" stroke-linecap="round" data-cy="${l.y}"/>`+
    `<path class="crl" d="${l.tail}" fill="none" stroke="${l.c}" stroke-width="${l.w}" stroke-dasharray="4 3" stroke-linecap="round" data-cy="${l.y}"/>`).join('');
  const hits=lines.map(l=>`<path class="crhit" d="${l.d}" fill="none" stroke="transparent" stroke-width="15" data-cy="${l.y}" style="cursor:pointer;pointer-events:stroke"/>`).join('');
  let dots='';
  lines.forEach(l=>{l.R.forEach((p,k)=>{
      dots+=`<circle class="crd" cx="${xs(k)}" cy="${ys(p.rank)}" r="${l.r}" fill="var(--surface)" stroke="${l.c}" stroke-width="${Math.max(1.6,l.w-0.5)}" data-cy="${l.y}" data-i="${k}" style="cursor:pointer"/>`;});
    dots+=`<circle class="crd" cx="${l.fx}" cy="${l.fy}" r="${l.r+1.3}" fill="var(--surface)" stroke="${l.c}" stroke-width="${l.w}" data-cy="${l.y}" data-fin="1" style="cursor:pointer"/>`;});
  /* labels: keep one line-height apart, in finishing order */
  const ordered=lines.slice().sort((a,b)=>a.fy-b.fy);
  const LY=[]; ordered.forEach((l,i)=>{let y=l.fy+3.5; if(i&&y-LY[i-1]<16)y=LY[i-1]+16; LY.push(y); l.ly=y;});
  const labs=ordered.map(l=>{
    const nm=l.team.length>15?l.team.slice(0,14)+'…':l.team;
    return `<text class="crt" x="${W-P.r+13}" y="${l.ly}" font-size="11.5" font-family="IBM Plex Sans,sans-serif" data-cy="${l.y}" data-medal="${MEDAL[l.fin]?l.fin:''}" style="cursor:pointer">`+
      `<tspan font-weight="700" fill="${l.c}" font-family="IBM Plex Mono,monospace">${l.y}</tspan>`+
      `<tspan fill="var(--ink-3)" font-size="10.5" dx="5">${esc(nm)}</tspan></text>`;}).join('');

  host.innerHTML=`<svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto" role="img" aria-label="Season-by-season league position for ${esc(CRMGR)}">${grid}${paths}${dots}${labs}${hits}</svg>`;
  /* medals ride to the right of the label, measured after render so they never sit on
     top of the text or on each other -- three seasons can finish in the same place */
  (function(){
    const svg=$('#crace svg'); if(!svg)return;
    const NS='http://www.w3.org/2000/svg';
    $$('#crace .crt').forEach(t=>{
      const rk=t.dataset.medal; if(!rk)return;
      const md=MEDAL[+rk]; const R=6.4;
      let right; try{const bb=t.getBBox(); right=bb.x+bb.width;}
      catch(e){right=+t.getAttribute('x')+t.textContent.length*6.2;}
      const x=right+9+R, y=+t.getAttribute('y')-3.6;
      const g=document.createElementNS(NS,'g'); g.setAttribute('class','crmed'); g.style.pointerEvents='none';
      const c=document.createElementNS(NS,'circle');
      c.setAttribute('cx',x);c.setAttribute('cy',y);c.setAttribute('r',R);
      c.setAttribute('fill',md.f);c.setAttribute('stroke',md.s);c.setAttribute('stroke-width',1.5);
      const n=document.createElementNS(NS,'text');
      n.setAttribute('x',x);n.setAttribute('y',y+3.1);n.setAttribute('text-anchor','middle');
      n.setAttribute('font-size',8.4);n.setAttribute('font-weight',700);n.setAttribute('fill',md.i);
      n.setAttribute('font-family','IBM Plex Mono,monospace');n.textContent=rk;
      g.appendChild(c);g.appendChild(n);svg.appendChild(g);});
  })();

  $('#crLeg').innerHTML=`<span class="fb-lab" style="margin-right:4px">Seasons</span>`+
    S.map(s=>`<button data-cy="${s.y}" style="padding:4px 9px">`+
      `<svg width="19" height="9" viewBox="0 0 19 9" style="vertical-align:-1px;margin-right:5px" aria-hidden="true">`+
      `<line x1="0.5" y1="4.5" x2="18.5" y2="4.5" stroke="${col(s.y)}" stroke-width="3" stroke-linecap="round"/></svg>`+
      `<b style="color:${col(s.y)}">${s.y}</b> <span class="dim">${esc(s.team)}</span></button>`).join('')+
    (S.length>1?`<button id="crClear" style="padding:4px 9px">Clear</button>`:'');

  function paint(hov){
    if(hov!==undefined)CRHOV=hov;
    const on=CRLOCK.size?CRLOCK:(CRHOV?new Set([CRHOV]):new Set()), any=on.size>0;
    $$('#crace .crl').forEach(p=>{const sel=on.has(p.dataset.cy), l=byY[p.dataset.cy];
      p.setAttribute('opacity',!any||sel?1:.13);
      p.setAttribute('stroke-width',sel?(l?l.w+1.2:3.4):(l?l.w:2.2));});
    $$('#crace .crd').forEach(c=>{const sel=on.has(c.dataset.cy);
      c.setAttribute('opacity',!any||sel?1:.13);});
    $$('#crace .crt').forEach(t=>{const sel=on.has(t.dataset.cy);
      t.setAttribute('opacity',!any||sel?1:.32);});
    $$('#crace .crmed').forEach(g=>g.setAttribute('opacity',!any?1:.32));
    $$('#crLeg button[data-cy]').forEach(b=>b.classList.toggle('on',CRLOCK.has(b.dataset.cy)));
  }
  const crToggle=y=>{CRLOCK.has(y)?CRLOCK.delete(y):CRLOCK.add(y);paint();};
  function crWeekTip(l,i){
    const seq=l.K.race[l.team], s=seq[i], p=l.R[i];
    const vsProj=s.pts-s.proj;
    return `<b style="color:${l.c}">${l.y}</b> &middot; ${esc(l.team)}
      <br><span style="opacity:.7">After week ${s.w}</span>
      <br>Position <b>${ord(p.rank)}</b> of ${l.K.teams.length} &middot; record <b>${p.wins}-${s.w-p.wins}</b>
      <br>${s.win?'<b style="color:var(--brass)">WON</b>':'<span style="color:var(--neg)">lost</span>'} ${s.pts.toFixed(2)}&ndash;${s.oppPts.toFixed(2)} vs ${esc(s.opp)}
      <br>Proj ${s.proj.toFixed(1)} (${vsProj>=0?'+':''}${vsProj.toFixed(1)}) &middot; PF ${p.pf.toFixed(1)}`;
  }
  function crFinTip(l){
    const last=l.R[l.R.length-1];
    return `<b style="color:${l.c}">${l.y}</b> &middot; ${esc(l.team)}
      <br><span style="opacity:.7">Final placing</span>
      <br>Regular season <b>${last.wins}-${l.R.length-last.wins}</b> &middot; ${last.pf.toFixed(2)} PF
      <br>Finished <b>${ord(l.fin)}</b> from the ${ord(l.seedRank)} seed
      <br>${l.moved>0?'<b style="color:var(--brass)">+'+l.moved+' in the postseason</b>':l.moved<0?'<span style="color:var(--neg)">'+l.moved+' in the postseason</span>':'held its seed'}`;
  }
  const byY={}; lines.forEach(l=>byY[l.y]=l);
  function nearestWeek(clientX,l){
    const r=$('#crace svg').getBoundingClientRect();
    const vx=(clientX-r.left)/r.width*W;
    const step=(W-P.l-P.r)/(NCOL-1);
    return Math.max(0,Math.min(l.R.length-1,Math.round((vx-P.l)/step)));
  }
  $$('#crace .crd').forEach(c=>{
    const l=byY[c.dataset.cy];
    c.addEventListener('mouseenter',e=>{paint(c.dataset.cy);
      showTip(e,c.dataset.fin?crFinTip(l):crWeekTip(l,+c.dataset.i));});
    c.addEventListener('mousemove',moveTip);
    c.addEventListener('mouseleave',()=>{paint(null);hideTip();});
    c.addEventListener('click',e=>{e.stopPropagation();crToggle(c.dataset.cy);});});
  $$('#crace .crhit').forEach(p=>{
    const l=byY[p.dataset.cy];
    p.addEventListener('mouseenter',e=>{paint(p.dataset.cy);showTip(e,crWeekTip(l,nearestWeek(e.clientX,l)));});
    p.addEventListener('mousemove',e=>{tip.innerHTML=crWeekTip(l,nearestWeek(e.clientX,l));moveTip(e);});
    p.addEventListener('mouseleave',()=>{paint(null);hideTip();});
    p.addEventListener('click',()=>crToggle(p.dataset.cy));});
  /* the year label sits past the last week, in the FINISH column -- same rule as the
     season chart: it is an end-of-line marker, so it shows the final placing. */
  $$('#crace .crt').forEach(t=>{
    const l=byY[t.dataset.cy];
    t.addEventListener('mouseenter',e=>{paint(t.dataset.cy);showTip(e,crFinTip(l));});
    t.addEventListener('mousemove',moveTip);
    t.addEventListener('mouseleave',()=>{paint(null);hideTip();});
    t.addEventListener('click',()=>crToggle(t.dataset.cy));});
  $$('#crLeg button[data-cy]').forEach(b=>{
    b.addEventListener('mouseenter',()=>paint(b.dataset.cy));
    b.addEventListener('mouseleave',()=>paint(null));
    b.addEventListener('click',()=>crToggle(b.dataset.cy));});
  {const cc=$('#crClear'); if(cc)cc.onclick=()=>{CRLOCK.clear();paint();};}
  paint();
}
drawCareerRace(); REDRAW.push(drawCareerRace);
/* every team name ever, alphabetical -- exists so the browser's find can reach names
   from seasons that are not currently on screen. Sits inside a closed <details>, which
   Chrome opens automatically when a search matches inside it. */
function drawTeamIndex(){
  const host=$('#teamIndex'); if(!host)return;
  const by={};
  ROWS.forEach(r=>{(by[r.team]=by[r.team]||{yrs:[],mgrs:new Set()});
    by[r.team].yrs.push(r.y); by[r.team].mgrs.add(r.mgr);});
  const names=Object.keys(by).sort((a,b)=>a.toLowerCase().localeCompare(b.toLowerCase()));
  host.innerHTML=`<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,270px),1fr));gap:4px 18px">`+
    names.map(t=>{const o=by[t]; const ys=o.yrs.sort((a,b)=>a-b);
      const span=ys.length>1?`${ys[0]}\u2013${ys[ys.length-1]}`:`${ys[0]}`;
      return `<div style="padding:2px 0"><b style="color:var(--ink)">${esc(t)}</b> `+
        `<span class="dim">${esc([...o.mgrs].join(', '))} &middot; ${span}</span></div>`;}).join('')+
    `</div><p style="margin:10px 0 0;font-size:12px;color:var(--ink-3)">${names.length} teams across ${SEA.length} seasons.</p>`;
}
drawTeamIndex(); REDRAW.push(drawTeamIndex);
/* Screen-reader and keyboard semantics for tables. Doing this centrally rather than in
   each of the ~20 table builders means a new table gets it for free, and a redraw can
   never lose it. Runs last, and again on every redraw. */
function a11yTables(){
  $$('table').forEach(t=>{
    /* name the table from the nearest visible heading */
    if(!t.getAttribute('aria-label')&&!t.querySelector('caption')){
      const card=t.closest('.card'), sec=t.closest('section');
      const h=(card&&card.querySelector('h3'))||(sec&&sec.querySelector('h2'));
      if(h)t.setAttribute('aria-label',h.textContent.trim().replace(/\s+/g,' '));
    }
    $$('th',t).forEach(th=>{
      if(th.getAttribute('scope'))return;
      const inHead=!!th.closest('thead');
      const firstInRow=th.parentElement&&th.parentElement.firstElementChild===th;
      th.setAttribute('scope',inHead?'col':(firstInRow?'row':'col'));
    });
  });
  /* sortable headers were mouse-only: not focusable, no state announced */
  $$('th.s').forEach(th=>{
    if(th.tabIndex<0||th.tabIndex===undefined)th.tabIndex=0;
    if(!th.getAttribute('role'))th.setAttribute('role','columnheader');
    th.setAttribute('aria-sort',th.classList.contains('asc')?'ascending'
      :th.classList.contains('desc')?'descending':'none');
    if(!th.dataset.kb){
      th.dataset.kb='1';
      const refocus=()=>setTimeout(()=>{
        a11yTables();
        const host=th.closest('table')||document;
        const again=host.isConnected
          ? host.querySelectorAll('th.s')[idxOf(th)]
          : null;
        const live=again||document.querySelectorAll('#'+(hostId||'')+' th.s')[idxOf(th)];
        if(live&&live.focus)live.focus();
      },0);
      const hostId=(th.closest('table')||{}).id||'';
      const idxOf=el=>{const t=el.closest('table');
        return t?[...t.querySelectorAll('th.s')].indexOf(el):0;};
      th.addEventListener('keydown',e=>{
        if(e.key==='Enter'||e.key===' '){e.preventDefault();th.click();refocus();}
      });
      th.addEventListener('click',()=>setTimeout(a11yTables,0));
    }
  });
}
a11yTables(); REDRAW.push(a11yTables);
setTimeout(a11yTables,0);
addEventListener('load',()=>setTimeout(a11yTables,80));
/* On a phone the manager and theme controls wrapped to three rows and pushed the first
   real content most of a screen down. Collapse them behind a one-line summary that says
   what is currently selected, so the state is still visible without the bulk. */
(function(){
  const sum=$('#fbSum'), fb=sum&&sum.closest('.fb');
  if(!fb||!sum)return;
  const SKINNAME={og:'Classic',scope:'Scope',red:'Crimson',leather:'Pigskin',arcade:'Arcade',redact:'Redacted'};
  function label(){
    const n=SEL.size, tot=ALLNAMES.length;
    const who=n===tot?'All '+tot:(n===ACTIVE.length&&ACTIVE.every(a=>SEL.has(a))?'Active '+n:n+' of '+tot);
    const sk=SKINNAME[document.documentElement.getAttribute('data-skin')]||'Classic';
    sum.innerHTML=`Managers <b>${esc(who)}</b> &middot; Theme <b>${esc(sk)}</b><span class="ar">&#9662;</span>`;
  }
  sum.onclick=()=>{const open=fb.classList.toggle('open');
    sum.setAttribute('aria-expanded',open?'true':'false');};
  label();
  REDRAW.push(label);
  $$('[data-skin-btn]').forEach(b=>b.addEventListener('click',()=>setTimeout(label,0)));
})();
/* Any card marked data-collapse gets a Hide/Show control in its header. Add
   data-collapse-also="#id" when related content sits outside the card, as the trade
   grid does. data-collapse="closed" starts it shut; default is open. */
(function(){
  $$('.card[data-collapse]').forEach(card=>{
    const head=card.querySelector('.card-h'); if(!head)return;
    const wrap=document.createElement('div');
    [...card.children].filter(c=>c!==head).forEach(c=>wrap.appendChild(c));
    card.appendChild(wrap);
    const extraSel=card.getAttribute('data-collapse-also');
    const extra=extraSel?$(extraSel):null;
    const btn=document.createElement('button');
    btn.type='button';
    btn.style.cssText='padding:5px 11px;font-size:11px;white-space:nowrap';
    const host=head.querySelector('.right')||head;
    if(host===head)btn.style.marginLeft='auto';
    host.appendChild(btn);
    const sync=()=>{const open=!wrap.hidden;
      btn.innerHTML=open?'Hide &#9652;':'Show &#9662;';
      btn.classList.toggle('on',open);
      if(extra)extra.hidden=!open;};
    btn.onclick=()=>{wrap.hidden=!wrap.hidden;sync();};
    wrap.hidden=(card.getAttribute('data-collapse')==='closed');
    sync();
  });
})();
/* ---- Shareable manager card -------------------------------------------------
   Draws a square PNG on a canvas and hands it to the phone's share sheet, which on
   iOS puts it straight into iMessage. Falls back to a download on desktop browsers
   that have no share sheet. Everything is drawn here: no image files, no libraries,
   so it keeps the "one self-contained page" property. */
function cardWrap(ctx,text,maxW){
  const words=String(text).split(' '); const lines=[]; let cur='';
  words.forEach(w=>{const t=cur?cur+' '+w:w;
    if(ctx.measureText(t).width>maxW&&cur){lines.push(cur);cur=w;} else cur=t;});
  if(cur)lines.push(cur); return lines;
}
async function makeShareCard(name){
  const m=M.filter(x=>x.name===name)[0]; if(!m)return null;
  const mine=ROWS.filter(r=>r.mgr===name);
  const S=1080, c=document.createElement('canvas'); c.width=S; c.height=S;
  const x=c.getContext('2d');
  try{ if(document.fonts&&document.fonts.ready)await document.fonts.ready; }catch(e){}

  const P=cardPalette();
  const GOLD=P.accent, INK=P.ink, DIM=P.dim, BG=P.bg;
  x.fillStyle=BG; x.fillRect(0,0,S,S);
  const g=x.createRadialGradient(180,120,10,180,120,760);
  g.addColorStop(0,P.glow); g.addColorStop(1,P.glow0);
  x.fillStyle=g; x.fillRect(0,0,S,S);

  /* reticle, drawn rather than loaded */
  const cx=S-176, cy=170, R=78;
  x.strokeStyle=GOLD; x.lineCap='round';
  x.lineWidth=11; x.beginPath(); x.arc(cx,cy,R,0,Math.PI*2); x.stroke();
  x.lineWidth=15;
  [[0,-1],[0,1],[-1,0],[1,0]].forEach(([dx,dy])=>{
    x.beginPath(); x.moveTo(cx+dx*R*1.28,cy+dy*R*1.28); x.lineTo(cx+dx*R*0.46,cy+dy*R*0.46); x.stroke();});
  x.fillStyle=GOLD; x.beginPath(); x.arc(cx,cy,10,0,Math.PI*2); x.fill();

  x.textBaseline='alphabetic';
  x.fillStyle=GOLD; x.font='600 25px "IBM Plex Mono",monospace';
  x.fillText('DEADSHOT  ·  EST. 2015'.split('').join(' '),84,138);

  /* name, shrunk to fit rather than clipped */
  let fs=118;
  x.font=`900 ${fs}px "Big Shoulders Display",sans-serif`;
  while(x.measureText(name.toUpperCase()).width>S-300&&fs>52){fs-=4;x.font=`900 ${fs}px "Big Shoulders Display",sans-serif`;}
  x.fillStyle=INK; x.fillText(name.toUpperCase(),84,268);

  x.fillStyle=DIM; x.font='400 30px "IBM Plex Sans",sans-serif';
  x.fillText(`${m.seasons} season${m.seasons>1?'s':''}  ·  ${m.first===m.last?m.first:m.first+'–'+m.last}`,86,316);

  /* the one-line verdict, same sentence the site shows on hover */
  x.fillStyle=INK; x.font='italic 400 40px "IBM Plex Sans",sans-serif';
  const vibe=cardWrap(x,mgrVibe(m),S-170);
  /* four lines fit between the subtitle and the stat row; a verdict that needs more
     than that gets set smaller rather than losing its last clause */
  if(vibe.length>4){
    x.font='italic 400 34px "IBM Plex Sans",sans-serif';
    cardWrap(x,mgrVibe(m),S-170).slice(0,5).forEach((l,i)=>x.fillText(l,84,400+i*46));
  }else vibe.forEach((l,i)=>x.fillText(l,84,404+i*54));

  /* stat row */
  const tiles=[
    ['RECORD',`${m.w}-${m.l}${m.t?'-'+m.t:''}`],
    ['WIN %',pct(m.winpct).replace('%','')],
    ['POWER IDX',m.cpi.toFixed(1)],
    ['TITLES',String(m.titles?(m.titles%1?m.titles.toFixed(1):m.titles):0)]
  ];
  const top=650;
  x.strokeStyle=P.rule; x.lineWidth=1;
  x.beginPath(); x.moveTo(84,top-46); x.lineTo(S-84,top-46); x.stroke();
  tiles.forEach((t,i)=>{
    const pitch=(S-168)/4, px=84+i*pitch;
    /* Walter Bremer's 52-59-1 measures 260px in a 228px column and was printing straight
       over the next tile's value. Shrink to fit the column, never past it. */
    x.fillStyle=GOLD;
    cardFit(x,t[1],pitch-14,62,34,600,'"IBM Plex Mono",monospace');
    x.fillText(t[1],px,top+24);
    x.fillStyle=DIM;  x.font='500 22px "IBM Plex Mono",monospace';
    x.fillText(t[0].split('').join(' '),px,top+62);
  });

  /* best and worst season, the two facts people argue about */
  if(mine.length){
    const hi=mine.reduce((a,b)=>b.pi>a.pi?b:a), lo=mine.reduce((a,b)=>b.pi<a.pi?b:a);
    x.strokeStyle=P.rule;
    x.beginPath(); x.moveTo(84,top+120); x.lineTo(S-84,top+120); x.stroke();
    x.fillStyle=DIM; x.font='400 28px "IBM Plex Sans",sans-serif';
    x.fillText(hi.y===lo.y?`Power index ${hi.pi.toFixed(1)} in ${hi.y}`
      :`Best year ${hi.y} at ${hi.pi.toFixed(1)}   ·   Worst ${lo.y} at ${lo.pi.toFixed(1)}`,84,top+172);
    x.fillText(`Playoffs ${m.apps} of ${m.seasons}   ·   ${m.podium} podium${m.podium===1?'':'s'}   ·   ${m.ppg.toFixed(1)} PPG`,84,top+218);
  }

  x.fillStyle=GOLD; x.font='600 26px "IBM Plex Mono",monospace';
  x.fillText(cardHost(),84,S-72);
  return new Promise(res=>c.toBlob(res,'image/png'));
}
/* Cards are drawn in whatever theme the reader is currently looking at, so the picture
   that lands in the group chat matches the site they were just on. The masthead tokens
   are used because those six are already designed to sit together in every skin. */
function cardHost(){
  try{const h=location.hostname;
    if(h&&h!=='localhost'&&location.protocol!=='file:')return h.replace(/^www\./,'');
  }catch(e){}
  return 'deadshotleague.com';
}
function cardPalette(){
  const hex=v=>{v=(v||'').trim(); return /^#[0-9a-fA-F]{6}$/.test(v)?v:null;};
  /* The card is a picture of the page the reader is on, so it takes the page's own
     surface, ink and accent. It used to take the MASTHEAD's colours, which matched on
     five skins and was badly wrong on Crimson: that masthead is deep red while the page
     itself is cream, so every Crimson card came out a solid red slab that looked
     nothing like the site it came from. */
  const bg=hex(cssv('--surface'))||'#12161B';
  const ink=hex(cssv('--ink'))||'#F6F1E6';
  const dim=hex(cssv('--ink-3'))||'#8C97A3';
  let accent=hex(cssv('--brass'))||'#C8A24A';
  /* kept as a safety net for any future skin that reuses its accent as a surface */
  if(contrastHex(accent,bg)<2.4) accent=hex(cssv('--brass-2'))||hex(cssv('--ink-2'))||ink;
  if(contrastHex(accent,bg)<2.4) accent=ink;
  const rr=parseInt(accent.slice(1,3),16), gg=parseInt(accent.slice(3,5),16), bb=parseInt(accent.slice(5,7),16);
  /* a light surface needs a far gentler wash than a near-black one */
  const lum=(0.2126*rr+0.7152*gg+0.0722*bb)/255;
  const bl=(parseInt(bg.slice(1,3),16)*0.2126+parseInt(bg.slice(3,5),16)*0.7152+parseInt(bg.slice(5,7),16)*0.0722)/255;
  const strength=bl>0.6?0.10:0.20;
  return {bg,ink,dim,accent,rule:bl>0.6?'rgba(0,0,0,.12)':'rgba(255,255,255,.10)',
          glow:`rgba(${rr},${gg},${bb},${strength})`, glow0:`rgba(${rr},${gg},${bb},0)`};
}
async function makeH2HCard(an,bn){
  const a=byName[an], b=byName[bn]; if(!a||!b||an===bn)return null;
  const S=1080, c=document.createElement('canvas'); c.width=S; c.height=S;
  const x=c.getContext('2d');
  try{ if(document.fonts&&document.fonts.ready)await document.fonts.ready; }catch(e){}
  const P=cardPalette();
  x.fillStyle=P.bg; x.fillRect(0,0,S,S);
  const g=x.createRadialGradient(S/2,140,10,S/2,140,780);
  g.addColorStop(0,P.glow); g.addColorStop(1,P.glow0); x.fillStyle=g; x.fillRect(0,0,S,S);

  x.textAlign='center';
  x.fillStyle=P.accent; x.font='600 25px "IBM Plex Mono",monospace';
  x.fillText('H E A D   T O   H E A D',S/2,108);

  const rec=MX.all.t[an+'|'+bn];
  const fit=(t,max,start)=>{let f=start;x.font=`900 ${f}px "Big Shoulders Display",sans-serif`;
    while(x.measureText(t).width>max&&f>40){f-=3;x.font=`900 ${f}px "Big Shoulders Display",sans-serif`;}return f;};
  const A=an.toUpperCase(), B=bn.toUpperCase();
  /* The two names can end up at different sizes, so a fixed offset for "versus" only
     looks centred for one pair. Measure the real ink of each and sit it in the middle
     of the actual gap. */
  const yA=206, yB=340;
  fit(A,S-140,86); const mA=x.measureText(A);
  x.fillStyle=P.ink; x.fillText(A,S/2,yA);
  fit(B,S-140,86); const mB=x.measureText(B);
  x.fillStyle=P.ink; x.fillText(B,S/2,yB);
  const gapTop=yA+(mA.actualBoundingBoxDescent||0);
  const gapBot=yB-(mB.actualBoundingBoxAscent||62);
  x.fillStyle=P.dim; x.font='500 30px "IBM Plex Mono",monospace';
  const mV=x.measureText('versus');
  const vAsc=mV.actualBoundingBoxAscent||21, vDesc=mV.actualBoundingBoxDescent||0;
  x.fillText('versus',S/2,(gapTop+gapBot)/2+(vAsc-vDesc)/2);

  if(rec){
    x.fillStyle=P.accent; x.font='900 176px "Big Shoulders Display",sans-serif';
    x.fillText(`${rec[0]}\u2013${rec[1]}`,S/2,510);
    x.fillStyle=P.dim; x.font='400 27px "IBM Plex Sans",sans-serif';
    x.fillText(`all-time, from ${esc(an)}'s side`,S/2,556);
  }else{
    x.fillStyle=P.dim; x.font='400 40px "IBM Plex Sans",sans-serif';
    x.fillText('They have never met.',S/2,500);
  }

  /* four stats side by side, winner picked out in the accent */
  const meets=MX.all.g.filter(x=>(x.ma===an&&x.mb===bn)||(x.ma===bn&&x.mb===an));
  const ppgIn=who=>{if(!meets.length)return null;
    let t=0; meets.forEach(x=>{t+=(x.ma===who?x.pa:x.pb);}); return t/meets.length;};
  const pA=ppgIn(an), pB=ppgIn(bn);
  const cmp=[['SEASONS','seasons',0],['PPG v EACH OTHER','__h2hppg',2],['POWER IDX','cpi',1],['PODIUMS','podium',0]];
  const lowerWins={};
  x.textAlign='left';
  x.strokeStyle=P.rule; x.lineWidth=1;
  x.beginPath(); x.moveTo(84,markY(0)); x.lineTo(S-84,markY(0)); x.stroke();
  function markY(){return 626;}
  cmp.forEach((row,i)=>{
    const [lab,k,d]=row, y=700+i*82;
    const h2h=k==='__h2hppg';
    const av=h2h?pA:a[k], bv=h2h?pB:b[k];
    const fmt=v=>v==null?'\u2014':(k==='winpct'?pct(v):(d?(+v).toFixed(d):String(v)));
    x.fillStyle=P.dim; x.font='500 21px "IBM Plex Mono",monospace';
    x.textAlign='center'; x.fillText(lab.split('').join(' '),S/2,y-6);
    x.font='600 46px "IBM Plex Mono",monospace';
    x.textAlign='left';  x.fillStyle=(av>bv)?P.accent:P.dim; x.fillText(fmt(av),84,y);
    x.textAlign='right'; x.fillStyle=(bv>av)?P.accent:P.dim; x.fillText(fmt(bv),S-84,y);
    x.textAlign='left';
    if(i<cmp.length-1){x.strokeStyle=P.rule;x.beginPath();x.moveTo(84,y+26);x.lineTo(S-84,y+26);x.stroke();}
  });
  x.textAlign='center';
  x.fillStyle=P.accent; x.font='600 26px "IBM Plex Mono",monospace';
  x.fillText(cardHost(),S/2,S-58);
  return new Promise(res=>c.toBlob(res,'image/png'));
}
async function shareBlob(blob,fname){
  const file=new File([blob],fname,{type:'image/png'});
  if(navigator.canShare&&navigator.canShare({files:[file]})){
    /* files only. Passing title/text makes the share sheet prefill a caption into the
       message, which reads as spam next to the picture. */
    await navigator.share({files:[file]});
  }else{
    const u=URL.createObjectURL(blob), a=document.createElement('a');
    a.href=u; a.download=fname; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(()=>URL.revokeObjectURL(u),4000);
    toast('Card saved to your downloads');
  }
}
async function shareH2H(an,bn,btn){
  const label=btn?btn.innerHTML:null;
  if(btn){btn.disabled=true;btn.innerHTML='Building…';}
  try{
    const blob=await makeH2HCard(an,bn);
    if(!blob){toast('Pick two different managers first');return;}
    await shareBlob(blob,`deadshot-${an.toLowerCase().replace(/[^a-z0-9]+/g,'-')}-v-${bn.toLowerCase().replace(/[^a-z0-9]+/g,'-')}.png`);
  }catch(e){ if(!(e&&e.name==='AbortError'))toast('Could not build the card'); }
  finally{ if(btn){btn.disabled=false;btn.innerHTML=label;} }
}
async function shareCard(name,btn){
  const label=btn?btn.innerHTML:null;
  if(btn){btn.disabled=true;btn.innerHTML='Building…';}
  try{
    const blob=await makeShareCard(name);
    if(!blob)throw new Error('no card');
    const file=new File([blob],`deadshot-${name.toLowerCase().replace(/[^a-z0-9]+/g,'-')}.png`,{type:'image/png'});
    if(navigator.canShare&&navigator.canShare({files:[file]})){
      await navigator.share({files:[file]});
    }else{
      const u=URL.createObjectURL(blob), a=document.createElement('a');
      a.href=u; a.download=file.name; document.body.appendChild(a); a.click(); a.remove();
      setTimeout(()=>URL.revokeObjectURL(u),4000);
      toast('Card saved to your downloads');
    }
  }catch(e){
    if(e&&e.name==='AbortError'){/* the share sheet was dismissed, not an error */}
    else toast('Could not build the card');
  }finally{ if(btn){btn.disabled=false;btn.innerHTML=label;} }
}

/* ---- more shareable cards ---------------------------------------------------
   Every card below is the same 1080 square as the manager and head-to-head cards,
   drawn in whatever theme the reader is looking at, and sent through the same
   shareBlob path. cardBase / cardKick / cardFoot exist so that adding a card is a
   matter of writing a layout, not another copy of the background, the rule lines
   and the footer. */
const CARD_S=1080;
function cardBase(){
  const S=CARD_S, cv=document.createElement('canvas'); cv.width=S; cv.height=S;
  const x=cv.getContext('2d'), P=cardPalette();
  x.fillStyle=P.bg; x.fillRect(0,0,S,S);
  const g=x.createRadialGradient(S/2,130,10,S/2,130,860);
  g.addColorStop(0,P.glow); g.addColorStop(1,P.glow0); x.fillStyle=g; x.fillRect(0,0,S,S);
  x.textBaseline='alphabetic';
  return {cv,x,P,S};
}
async function cardFonts(){try{if(document.fonts&&document.fonts.ready)await document.fonts.ready;}catch(e){}}
function cardKick(x,S,P,t){
  x.textAlign='center'; x.fillStyle=P.accent; x.font='600 25px "IBM Plex Mono",monospace';
  x.fillText(String(t).toUpperCase().split('').join(' '),S/2,108);
}
function cardFoot(x,S,P){
  x.textAlign='center'; x.fillStyle=P.accent; x.font='600 26px "IBM Plex Mono",monospace';
  x.fillText(cardHost(),S/2,S-58);
}
function cardRule(x,S,P,y){
  x.strokeStyle=P.rule; x.lineWidth=1; x.beginPath(); x.moveTo(84,y); x.lineTo(S-84,y); x.stroke();
}
/* shrink to fit rather than clip -- team names in this league run very long */
function cardFit(x,text,maxW,start,min,weight,face){
  let fs=start; x.font=weight+' '+fs+'px '+face;
  while(x.measureText(text).width>maxW&&fs>min){fs-=3; x.font=weight+' '+fs+'px '+face;}
  return fs;
}
function cardClip(x,text,maxW){
  if(x.measureText(text).width<=maxW)return text;
  let t=text;
  while(t.length>2&&x.measureText(t+'…').width>maxW)t=t.slice(0,-1);
  return t+'…';
}
function cardTiles(x,S,P,y,tiles){
  cardRule(x,S,P,y-46); x.textAlign='left';
  tiles.forEach((t,i)=>{
    const px=84+i*((S-168)/tiles.length);
    x.fillStyle=P.accent; x.font='600 56px "IBM Plex Mono",monospace'; x.fillText(t[1],px,y+22);
    x.fillStyle=P.dim; x.font='500 21px "IBM Plex Mono",monospace'; x.fillText(t[0].split('').join(' '),px,y+58);
  });
}
/* the site's copy is HTML; canvas wants plain text */
function cardText(s){
  return String(s).replace(/<br\s*\/?>/gi,' ').replace(/<[^>]*>/g,'')
    .replace(/&mdash;/g,'—').replace(/&ndash;/g,'–').replace(/&minus;/g,'−')
    .replace(/&sigma;/g,'σ').replace(/&harr;/g,'↔').replace(/&nbsp;/g,' ')
    .replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;/g,"'")
    .replace(/&amp;/g,'&').replace(/\s+/g,' ').trim();
}

/* Every meeting between two managers that the data can actually prove: playoff games
   exist for all ten seasons, regular-season games only for the years with a game log.
   The two sources never overlap, because the weekly side skips anything flagged as a
   bracket game. */
function meetings(an,bn){
  const out=[];
  D.games.forEach(g=>{
    if(g.void)return;
    if(g.ma===an&&g.mb===bn)out.push({y:g.y,wk:g.wk,rnd:g.rnd,me:g.pa,them:g.pb,mine:g.ta,theirs:g.tb,po:1});
    else if(g.mb===an&&g.ma===bn)out.push({y:g.y,wk:g.wk,rnd:g.rnd,me:g.pb,them:g.pa,mine:g.tb,theirs:g.ta,po:1});
  });
  (D.wkYears||[]).forEach(y=>{
    const K=D.wk[y]; if(!K)return;
    K.games.forEach(g=>{
      if(g.br)return;
      const ma=K.mgr[g.ta], mb=K.mgr[g.tb];
      if(ma===an&&mb===bn)out.push({y:y,wk:g.wk,rnd:'Week '+g.wk,me:g.aa,them:g.ab,mine:g.ta,theirs:g.tb,po:0});
      else if(mb===an&&ma===bn)out.push({y:y,wk:g.wk,rnd:'Week '+g.wk,me:g.ab,them:g.aa,mine:g.tb,theirs:g.ta,po:0});
    });
  });
  return out.sort((a,b)=>a.y-b.y||a.wk-b.wk);
}

/* every logged game, flattened once and kept, so a card can say where a result ranks */
let LOGGED=null;
function loggedGames(){
  if(LOGGED)return LOGGED;
  const out=[];
  (D.wkYears||[]).forEach(y=>{
    const K=D.wk[y]; if(!K)return;
    K.games.forEach(g=>{
      if(isVoid(y,g.wk,g.ta,g.tb))return;
      out.push({y:y,wk:g.wk,ta:g.ta,tb:g.tb,pa:g.aa,pb:g.ab,prA:g.pa,prB:g.pb,
                ma:K.mgr[g.ta],mb:K.mgr[g.tb],br:g.br});
    });
  });
  LOGGED=out; return out;
}

/* ---- 1. the season card ---- */
async function makeSeasonCard(y){
  const ch=D.champs.find(z=>z.y===y); if(!ch)return null;
  const rs=ROWS.filter(r=>r.y===y).sort((a,b)=>a.place-b.place);
  if(!rs.length)return null;
  await cardFonts();
  const {cv,x,P,S}=cardBase();
  cardKick(x,S,P,'The '+y+' season');

  x.textAlign='center';
  x.fillStyle=P.dim; x.font='500 23px "IBM Plex Mono",monospace';
  x.fillText((ch.co?'CO-CHAMPIONS':'CHAMPION').split('').join(' '),S/2,176);
  const champ=ch.teams.join(' & ').toUpperCase();
  cardFit(x,champ,S-140,96,40,900,'"Big Shoulders Display",sans-serif');
  x.fillStyle=P.ink; x.fillText(champ,S/2,262);
  x.fillStyle=P.dim; x.font='400 27px "IBM Plex Sans",sans-serif';
  x.fillText(ch.mgrs.join(' & '),S/2,304);

  /* the final table, the part everybody argues about */
  cardRule(x,S,P,344);
  const COL={pl:96,tm:202,rec:S-282,pf:S-84};
  x.textAlign='left'; x.fillStyle=P.dim; x.font='500 19px "IBM Plex Mono",monospace';
  x.fillText('F I N',84,382); x.fillText('T E A M',COL.tm,382);
  x.textAlign='right'; x.fillText('W - L',COL.rec,382); x.fillText('P F',COL.pf,382);

  const step=Math.min(40,(S-560)/Math.max(1,rs.length));
  rs.forEach((r,i)=>{
    const ty=420+i*step;
    x.textAlign='left';
    x.fillStyle=r.place===1?P.accent:P.dim;
    x.font='600 25px "IBM Plex Mono",monospace'; x.fillText(String(r.place),84,ty);
    x.fillStyle=r.place===1?P.accent:P.ink;
    x.font=(r.place===1?'600 ':'400 ')+26+'px "IBM Plex Sans",sans-serif';
    x.fillText(cardClip(x,r.team,COL.rec-COL.tm-90),COL.tm,ty);
    x.textAlign='right';
    x.fillStyle=P.dim; x.font='400 24px "IBM Plex Mono",monospace';
    x.fillText(r.w+'-'+r.l+(r.t?'-'+r.t:''),COL.rec,ty);
    x.fillStyle=P.ink; x.fillText(r.pf.toFixed(2),COL.pf,ty);
  });

  /* the row step shrinks past twelve teams but the block underneath did not move, so the
     two summary lines ended up on top of the footer */
  const botY=Math.min(420+rs.length*step+18,S-190);
  cardRule(x,S,P,botY);
  const most=rs.reduce((a,b)=>b.pf>a.pf?b:a);
  const bestRec=rs.reduce((a,b)=>(b.w+b.t/2)>(a.w+a.t/2)?b:a);
  x.textAlign='center'; x.fillStyle=P.dim; x.font='400 26px "IBM Plex Sans",sans-serif';
  x.font='400 24px "IBM Plex Sans",sans-serif';
  x.fillText(ch.n+' teams  ·  '+ch.g+'-game season  ·  '+ch.spots+'-team bracket  ·  final placings',
    S/2,botY+44);
  x.font='400 26px "IBM Plex Sans",sans-serif';
  /* saying "most points: <the champion>" when the table already has them top is noise;
     the interesting version of that fact is when somebody else led and still lost */
  const champTeams=ch.teams;
  const line2=champTeams.indexOf(most.team)>=0
    ? (champTeams.indexOf(bestRec.team)>=0
        ? 'Led the league in scoring and in record. No argument to be had.'
        : 'Led the league in scoring. Best record was '+cardClip(x,bestRec.team,420)+
          ' at '+bestRec.w+'-'+bestRec.l+(bestRec.t?'-'+bestRec.t:'')+'.')
    : 'Most points: '+cardClip(x,most.team,420)+'  ·  '+most.pf.toFixed(2)+
      ', and finished '+ord(most.place)+'.';
  x.fillText(line2,S/2,botY+86);
  cardFoot(x,S,P);
  return new Promise(res=>cv.toBlob(res,'image/png'));
}


/* ---- the bracket ------------------------------------------------------------
   Two shapes exist in this league's history: a 4-team bracket (two semifinals into a
   final) and a 6-team one (two quarterfinals plus two byes, into semifinals, into a
   final). Rounds are read from the data rather than assumed, so a future shape draws
   itself. The placement games sit in a strip underneath: they are part of the record
   but they are not the title path, and mixing them into the columns made the card
   unreadable. */
function bracketFacts(y){
  const ch=D.champs.find(c=>c.y===y); if(!ch)return null;
  const gs=D.games.filter(g=>g.y===y); if(!gs.length)return null;
  const wks=[...new Set(gs.map(g=>g.wk))].sort((a,b)=>a-b);
  const rs=ROWS.filter(r=>r.y===y).sort((a,b)=>a.seed-b.seed);
  const seedOf={}; rs.forEach(r=>{seedOf[r.team]=r.seed;});
  const byes=rs.filter(r=>r.seed<=ch.spots&&
    !gs.some(g=>g.wk===wks[0]&&(g.ta===r.team||g.tb===r.team)));
  const MAIN=['Quarterfinal','Semifinal','Final'];
  const cols=wks.map((w,i)=>({
    w:w,
    games:gs.filter(g=>g.wk===w&&MAIN.indexOf(g.rnd)>=0),
    byes:i===0?byes:[]
  })).filter(c=>c.games.length||c.byes.length);
  const extra=gs.filter(g=>MAIN.indexOf(g.rnd)<0)
    .sort((a,b)=>a.wk-b.wk||a.rnd.localeCompare(b.rnd));
  return {ch:ch,wks:wks,cols:cols,extra:extra,seedOf:seedOf};
}
function cardBox(x,bx,by,bw,bh,r){
  x.beginPath();
  if(x.roundRect)x.roundRect(bx,by,bw,bh,r); else x.rect(bx,by,bw,bh);
}
async function makeBracketCard(y){
  const B=bracketFacts(y); if(!B)return null;
  await cardFonts();
  const {cv,x,P,S}=cardBase();
  const ch=B.ch;

  cardKick(x,S,P,'The '+y+' bracket');
  x.textAlign='center'; x.fillStyle=P.dim; x.font='400 26px "IBM Plex Sans",sans-serif';
  x.fillText(ch.n+' teams  ·  '+ch.spots+'-team bracket  ·  '+
    (B.wks.length>1?'weeks '+B.wks[0]+' to '+B.wks[B.wks.length-1]:'week '+B.wks[0]),S/2,160);

  /* ---- the title path, one column per week ---- */
  const GAP=22, N=B.cols.length;
  const colW=Math.min(360,(S-112-GAP*(N-1))/N);
  const PAD=(S-(colW*N+GAP*(N-1)))/2;
  const GH=28, ROW=36, BOXH=GH+ROW*2, BYEH=GH+ROW, VGAP=16;
  const BTOP=206, BBOT=584;

  const place={};                       /* team -> the box it appears in, for connectors */
  const boxes=B.cols.map((c,ci)=>{
    const items=c.games.map(g=>({g:g}))
      .concat(c.byes.map(b=>({bye:b})));
    const total=items.reduce((n,it)=>n+(it.bye?BYEH:BOXH),0)+VGAP*(items.length-1);
    let ty=BTOP+((BBOT-BTOP)-total)/2;
    return items.map(it=>{
      const h=it.bye?BYEH:BOXH;
      const o={it:it,x:PAD+ci*(colW+GAP),y:ty,w:colW,h:h,ci:ci};
      ty+=h+VGAP;
      if(it.bye)place[it.bye.team]=o;
      else{place[it.g.ta]=place[it.g.ta]||o; place[it.g.tb]=place[it.g.tb]||o;}
      return o;});
  });

  /* connectors first, so the boxes sit on top of them */
  x.strokeStyle=P.dim; x.globalAlpha=.45; x.lineWidth=2;
  boxes.forEach((col,ci)=>{
    if(ci===boxes.length-1)return;
    col.forEach(o=>{
      const it=o.it;
      const winner=it.bye?it.bye.team
        :(isVoid(y,it.g.wk,it.g.ta,it.g.tb)?null:(it.g.pa>it.g.pb?it.g.ta:it.g.tb));
      if(!winner)return;
      const nxt=boxes[ci+1].filter(z=>!z.it.bye&&
        (z.it.g.ta===winner||z.it.g.tb===winner))[0];
      if(!nxt)return;
      const x0=o.x+o.w, y0=o.y+o.h/2, x1=nxt.x, y1=nxt.y+nxt.h/2, mx=(x0+x1)/2;
      x.beginPath(); x.moveTo(x0,y0); x.lineTo(mx,y0); x.lineTo(mx,y1); x.lineTo(x1,y1); x.stroke();
    });
  });
  x.globalAlpha=1;

  const side=(t,mg,pts,bx,by,bw,win,dead)=>{
    x.textAlign='left';
    x.fillStyle=win&&!dead?P.accent:P.dim; x.font='600 17px "IBM Plex Mono",monospace';
    x.fillText(String(B.seedOf[t]||''),bx+12,by+24);
    x.fillStyle=win&&!dead?P.ink:P.dim;
    const tfs=bw<330?18:19;
    x.font=(win&&!dead?'600 ':'400 ')+tfs+'px "IBM Plex Sans",sans-serif';
    /* a six-figure score is 65px at this size; 64 left no gutter at all and the name ran
       into it. 82 buys the score its width plus a real gap. */
    const scoreW=pts==null?0:82;
    x.fillText(cardClip(x,t,bw-46-scoreW),bx+36,by+24);
    if(pts!=null){
      x.textAlign='right'; x.font='500 18px "IBM Plex Mono",monospace';
      x.fillStyle=win&&!dead?P.ink:P.dim;
      x.fillText(pts.toFixed(2),bx+bw-13,by+24);
    }
  };

  boxes.forEach(col=>col.forEach(o=>{
    const it=o.it;
    cardBox(x,o.x,o.y,o.w,o.h,6);
    x.strokeStyle=P.rule; x.lineWidth=1.4; x.stroke();
    /* header strip */
    cardBox(x,o.x,o.y,o.w,GH,6);
    x.save(); x.clip(); x.fillStyle=P.rule; x.fillRect(o.x,o.y,o.w,GH); x.restore();
    const dead=it.bye?false:isVoid(y,it.g.wk,it.g.ta,it.g.tb);
    x.textAlign='left'; x.fillStyle=P.dim; x.font='500 13px "IBM Plex Mono",monospace';
    x.fillText((it.bye?(o.ci===0?'FIRST-ROUND BYE':'BYE'):it.g.rnd.toUpperCase()+(dead?' — VOID':''))
      .split('').join(' '),o.x+13,o.y+19);
    if(it.bye)side(it.bye.team,null,null,o.x,o.y+GH,o.w,true,false);
    else{
      const aw=it.g.pa>it.g.pb;
      side(it.g.ta,it.g.ma,it.g.pa,o.x,o.y+GH,o.w,aw,dead);
      side(it.g.tb,it.g.mb,it.g.pb,o.x,o.y+GH+ROW,o.w,!aw,dead);
    }
  }));

  /* ---- the champion, full width so a long name has somewhere to go ---- */
  const CY=616, MPAD=56;
  const cname=ch.teams.join('  &  ').toUpperCase();
  /* Big Shoulders is a display face with a very tall ascender, so the name has to be
     placed off its measured ascent -- a fixed baseline put it through its own label */
  const nfs=cardFit(x,cname,S-MPAD*2-40,50,24,900,'"Big Shoulders Display",sans-serif');
  const asc=x.measureText(cname).actualBoundingBoxAscent||nfs*0.73;
  const nameBase=CY+44+asc, CH2=nameBase-CY+40;
  cardBox(x,MPAD,CY,S-MPAD*2,CH2,8);
  x.fillStyle=P.accent; x.fill();
  const cink=pickInk(P.accent);
  x.textAlign='center'; x.fillStyle=cink; x.globalAlpha=.74;
  x.font='500 16px "IBM Plex Mono",monospace';
  x.fillText((ch.co?'CO-CHAMPIONS':'CHAMPION').split('').join(' '),S/2,CY+28);
  x.globalAlpha=1;
  x.font='900 '+nfs+'px "Big Shoulders Display",sans-serif';
  x.fillStyle=cink; x.fillText(cname,S/2,nameBase);
  x.globalAlpha=.8; x.font='400 19px "IBM Plex Sans",sans-serif';
  x.fillText(cardClip(x,ch.mgrs.join(' & '),S-MPAD*2-40),S/2,nameBase+27);
  x.globalAlpha=1;

  /* ---- placement games: part of the record, not part of the title path ---- */
  let ey=CY+CH2+54;
  if(B.extra.length){
    x.textAlign='center'; x.fillStyle=P.dim; x.font='500 14px "IBM Plex Mono",monospace';
    x.fillText('A L S O   P L A Y E D',S/2,ey); ey+=34;
    B.extra.slice(0,3).forEach(g=>{
      const aw=g.pa>g.pb;
      const wT=aw?g.ta:g.tb, lT=aw?g.tb:g.ta;
      const wP=aw?g.pa:g.pb, lP=aw?g.pb:g.pa;
      x.textAlign='left'; x.fillStyle=P.dim; x.font='500 15px "IBM Plex Mono",monospace';
      x.fillText(g.rnd.replace(' Game','').toUpperCase(),MPAD,ey);
      x.textAlign='right'; x.font='400 19px "IBM Plex Sans",sans-serif';
      x.fillStyle=P.ink;
      const txt=cardClip(x,wT,300)+'  '+wP.toFixed(2)+'   beat   '+cardClip(x,lT,300)+'  '+lP.toFixed(2);
      x.fillText(cardClip(x,txt,S-MPAD*2-190),S-MPAD,ey);
      ey+=34;
    });
  }
  cardFoot(x,S,P);
  return new Promise(res=>cv.toBlob(res,'image/png'));
}

/* ---- 2. the receipt: one game ---- */
function gameFacts(y,wk,team){
  const K=D.wk[y]; if(!K)return null;
  const g=K.games.find(z=>z.wk===wk&&(z.ta===team||z.tb===team)); if(!g)return null;
  const aFirst=g.aa>=g.ab;
  const A=aFirst?{t:g.ta,p:g.aa,pr:g.pa}:{t:g.tb,p:g.ab,pr:g.pb};
  const B=aFirst?{t:g.tb,p:g.ab,pr:g.pb}:{t:g.ta,p:g.aa,pr:g.pa};
  const all=loggedGames().map(z=>Math.abs(z.pa-z.pb)).sort((a,b)=>b-a);
  const marg=A.p-B.p;
  /* how many of the rest of the league that winning score would have beaten the same
     week. Only exists for regular-season weeks, which is where the race data lives. */
  const wi=K.weeks.indexOf(wk);
  const seq=K.race[A.t];
  const ap=(wi>=0&&seq&&seq[wi])?seq[wi].ap:null;
  return {y:y,wk:wk,A:A,B:B,marg:marg,mgA:K.mgr[A.t],mgB:K.mgr[B.t],
          rnd:roundName(y,K,g)||('Week '+wk),
          vd:isVoid(y,wk,g.ta,g.tb), tie:g.aa===g.ab,
          ap:ap, others:K.teams.length-1,
          rank:all.filter(v=>v>marg).length+1, n:all.length};
}
async function makeGameCard(y,wk,team){
  const G=gameFacts(y,wk,team); if(!G)return null;
  await cardFonts();
  const {cv,x,P,S}=cardBase();
  cardKick(x,S,P,'The receipt');
  x.textAlign='center'; x.fillStyle=P.dim; x.font='400 28px "IBM Plex Sans",sans-serif';
  x.fillText(G.rnd+'  ·  '+G.y+(G.vd?'  ·  VOIDED':''),S/2,162);

  const side=(t,mg,p,ty,win)=>{
    x.textAlign='right'; x.fillStyle=win?P.accent:P.dim;
    x.font='600 78px "IBM Plex Mono",monospace';
    const sw=x.measureText(p.toFixed(2)).width;
    x.fillText(p.toFixed(2),S-84,ty);
    x.textAlign='left'; x.fillStyle=win?P.ink:P.dim;
    cardFit(x,t,S-190-sw,52,26,700,'"IBM Plex Sans",sans-serif');
    /* cardFit stops at its floor and gives up; every other card clips afterwards and this
       one did not, so a long enough name would run under the score */
    x.fillText(cardClip(x,t,S-190-sw),84,ty);
    x.fillStyle=P.dim; x.font='400 25px "IBM Plex Sans",sans-serif';
    x.fillText(mg,84,ty+38);
  };
  side(G.A.t,G.mgA,G.A.p,268,true);
  x.textAlign='center'; x.fillStyle=P.dim; x.font='500 22px "IBM Plex Mono",monospace';
  x.fillText(G.tie?'T I E D   W I T H':'B E A T',S/2,368);
  side(G.B.t,G.mgB,G.B.p,452,false);

  cardRule(x,S,P,540);
  x.textAlign='center';
  x.fillStyle=P.accent; x.font='900 172px "Big Shoulders Display",sans-serif';
  x.fillText(G.marg.toFixed(2),S/2,700);
  x.fillStyle=P.dim; x.font='500 24px "IBM Plex Mono",monospace';
  x.fillText(G.tie?'D E A D   H E A T':'P O I N T   M A R G I N',S/2,748);

  cardRule(x,S,P,800);
  const diff=G.A.p-G.A.pr;
  const lines=[];
  lines.push(G.tie?'A dead heat. It has happened '+
      (loggedGames().filter(z=>z.pa===z.pb).length)+' times in '+G.n+' logged games.'
    :G.rank===1?'The biggest beating in '+G.n+' logged games.'
    :'The '+ord(G.rank)+' biggest margin of '+G.n+' logged games.');
  if(G.ap!=null)lines.push('That '+G.A.p.toFixed(2)+' would have beaten '+G.ap+
    ' of the other '+G.others+' that week.');
  lines.push(cardClip(x,G.A.t,S-260)+' was projected '+G.A.pr.toFixed(1)+'  ·  '+
    (diff>=0?'beat it by ':'missed it by ')+Math.abs(diff).toFixed(1));
  const lTop=lines.length>2?848:868;
  lines.forEach((t,k)=>{
    x.fillStyle=k===0?P.ink:P.dim;
    x.font='400 '+(k===0?28:26)+'px "IBM Plex Sans",sans-serif';
    x.fillText(cardClip(x,t,S-140),S/2,lTop+k*44);
  });
  cardFoot(x,S,P);
  return new Promise(res=>cv.toBlob(res,'image/png'));
}

/* ---- 3. one line from the record book ---- */
let BIGRECS=null;
function bigRecords(){
  if(BIGRECS)return BIGRECS;
  const gs=loggedGames();
  const sc=[];
  gs.forEach(g=>{
    sc.push({y:g.y,wk:g.wk,t:g.ta,m:g.ma,p:g.pa,o:g.tb,op:g.pb});
    sc.push({y:g.y,wk:g.wk,t:g.tb,m:g.mb,p:g.pb,o:g.ta,op:g.pa});
  });
  const pick=(arr,f)=>arr.length?arr.reduce((a,b)=>f(b)>f(a)?b:a):null;
  const R=[];
  const hi=pick(sc,z=>z.p), lo=pick(sc,z=>-z.p);
  const blow=pick(gs,z=>Math.abs(z.pa-z.pb)), close=pick(gs,z=>-Math.abs(z.pa-z.pb));
  const szPF=pick(ROWS,z=>z.pf), szPI=pick(ROWS,z=>z.pi), szW=pick(ROWS,z=>z.w+z.t/2);
  const mostT=pick(M,z=>z.titles);
  const bestPct=pick(M.filter(z=>z.g>=40),z=>z.winpct);
  const mostApp=pick(M,z=>z.apps);
  /* these four come from loggedGames(), which is the weekly logs only -- a subset of the
     league's seasons -- so the label has to carry the coverage or it claims too much */
  const LOGY=(D.wkYears||[]).slice().sort((a,b)=>a-b);
  const SINCE=LOGY.length&&LOGY.length!==SEA.length?' ('+LOGY[0]+'\u2013'+LOGY[LOGY.length-1]+')':'';
  if(hi)R.push({k:'Most points in a week'+SINCE,v:hi.p.toFixed(2),who:hi.m,
    when:hi.t+'  ·  week '+hi.wk+', '+hi.y,sub:'Beat '+hi.o+', who managed '+hi.op.toFixed(2)+'.'});
  if(lo)R.push({k:'Fewest points in a week'+SINCE,v:lo.p.toFixed(2),who:lo.m,
    when:lo.t+'  ·  week '+lo.wk+', '+lo.y,sub:'Faced '+lo.o+', who scored '+lo.op.toFixed(2)+'.'});
  if(blow)R.push({k:'Biggest beating'+SINCE,v:Math.abs(blow.pa-blow.pb).toFixed(2),
    who:(blow.pa>blow.pb?blow.ma:blow.mb),
    when:'week '+blow.wk+', '+blow.y,
    sub:(blow.pa>blow.pb?blow.ta:blow.tb)+' '+Math.max(blow.pa,blow.pb).toFixed(2)+
        ' – '+Math.min(blow.pa,blow.pb).toFixed(2)+' '+(blow.pa>blow.pb?blow.tb:blow.ta)+'.'});
  if(close)R.push({k:'Closest finish'+SINCE,v:Math.abs(close.pa-close.pb).toFixed(2),
    who:(close.pa>close.pb?close.ma:close.mb),
    when:'week '+close.wk+', '+close.y,
    sub:(close.pa>close.pb?close.ta:close.tb)+' '+Math.max(close.pa,close.pb).toFixed(2)+
        ' – '+Math.min(close.pa,close.pb).toFixed(2)+' '+(close.pa>close.pb?close.tb:close.ta)+'.'});
  if(szPF)R.push({k:'Most points in a season',v:szPF.pf.toFixed(2),who:szPF.mgr,
    when:szPF.team+'  ·  '+szPF.y,sub:szPF.ppg.toFixed(2)+' a game across '+szPF.g+' games. Finished '+ord(szPF.place)+'.'});
  if(szW)R.push({k:'Best season record',v:szW.w+'-'+szW.l+(szW.t?'-'+szW.t:''),who:szW.mgr,
    when:szW.team+'  ·  '+szW.y,sub:szW.pf.toFixed(2)+' points for. Finished '+ord(szW.place)+' of '+szW.teams+'.'});
  if(szPI)R.push({k:'Highest power index, one season',v:szPI.pi.toFixed(1),who:szPI.mgr,
    when:szPI.team+'  ·  '+szPI.y,sub:'The strongest single season the league has recorded.'});
  /* pick() keeps the first on a tie, which quietly erased a joint record holder */
  if(mostT&&mostT.titles){
    const tied=M.filter(z=>z.titles===mostT.titles);
    R.push({k:'Most titles',v:String(mostT.titles%1?mostT.titles.toFixed(1):mostT.titles),
      who:tied.map(z=>z.name).join(' & '),
      when:tied.length>1?'shared, and neither has it alone':mostT.seasons+' seasons  ·  '+mostT.first+'–'+mostT.last,
      sub:tied.length>1
        ?'Nobody in league history has more.'
        :'Last one in '+mostT.lastTitle+'. '+mostT.podium+' podium finishes in all.'});
  }
  if(bestPct)R.push({k:'Best career win rate',v:pct(bestPct.winpct),who:bestPct.name,
    when:bestPct.w+'-'+bestPct.l+(bestPct.t?'-'+bestPct.t:'')+'  ·  '+bestPct.g+' games',
    sub:'Across '+bestPct.seasons+' seasons, '+bestPct.first+' to '+bestPct.last+'.'});
  if(mostApp)R.push({k:'Most playoff appearances',v:String(mostApp.apps),who:mostApp.name,
    when:mostApp.apps+' of '+mostApp.seasons+' seasons',
    sub:mostApp.poW+'-'+mostApp.poL+' once they got there.'});
  BIGRECS=R; return R;
}
async function makeRecordCard(i){
  const R=bigRecords()[i]; if(!R)return null;
  await cardFonts();
  const {cv,x,P,S}=cardBase();
  cardKick(x,S,P,'League record');
  x.textAlign='center';
  x.fillStyle=P.dim; x.font='400 33px "IBM Plex Sans",sans-serif';
  x.fillText(R.k,S/2,214);
  cardFit(x,R.v,S-140,210,72,900,'"Big Shoulders Display",sans-serif');
  x.fillStyle=P.accent; x.fillText(R.v,S/2,420);
  cardRule(x,S,P,486);
  cardFit(x,R.who.toUpperCase(),S-140,86,36,900,'"Big Shoulders Display",sans-serif');
  x.fillStyle=P.ink; x.fillText(R.who.toUpperCase(),S/2,576);
  x.fillStyle=P.dim; x.font='400 29px "IBM Plex Sans",sans-serif';
  x.fillText(cardClip(x,R.when,S-140),S/2,626);
  x.fillStyle=P.ink; x.font='italic 400 34px "IBM Plex Sans",sans-serif';
  cardWrap(x,R.sub,S-190).slice(0,3).forEach((l,k)=>x.fillText(l,S/2,724+k*48));
  cardFoot(x,S,P);
  return new Promise(res=>cv.toBlob(res,'image/png'));
}

/* ---- 4. a single Wrapped slide ---- */
/* Wrapped is its own world -- a gradient stage, soft light and white type -- and a card
   that came out in the site's paper-and-ink palette read as a different product. This one
   paints the same gradient the slide was on, so the picture matches what was on screen.
   Big Shoulders, not Fraunces: canvas cannot set a variable font's optical-size axis and
   Fraunces' numerals come out in the wrong forms at display sizes. */
function wrGrad(i){
  const css=WRBG[i%WRBG.length];
  const stops=[]; const re=/(#[0-9a-fA-F]{6})\s+([\d.]+)%/g; let m;
  while((m=re.exec(css)))stops.push([m[1],+m[2]/100]);
  const dm=/^linear-gradient\(\s*([\d.]+)deg/.exec(css);
  return {deg:dm?+dm[1]:155,stops:stops.length?stops:[['#141a3a',0],['#8e3f76',1]]};
}
async function makeWrapCard(name,i){
  const built=wrapCards(name); if(!built)return null;
  const c=built.cards[i]; if(!c)return null;
  await cardFonts();
  const S=CARD_S, cv=document.createElement('canvas'); cv.width=S; cv.height=S;
  const x=cv.getContext('2d'); x.textBaseline='alphabetic';

  /* the stage: CSS 0deg points up and turns clockwise, so the direction vector is
     (sin a, -cos a) and the gradient line spans |W sin a| + |H cos a| */
  const G=wrGrad(i), a=G.deg*Math.PI/180;
  const dx=Math.sin(a), dy=-Math.cos(a);
  const L=Math.abs(S*dx)+Math.abs(S*dy);
  const g=x.createLinearGradient(S/2-dx*L/2,S/2-dy*L/2,S/2+dx*L/2,S/2+dy*L/2);
  G.stops.forEach(st=>g.addColorStop(Math.min(1,Math.max(0,st[1])),st[0]));
  x.fillStyle=g; x.fillRect(0,0,S,S);

  /* the two drifting highlights, as soft radial falloffs rather than a blur filter */
  [[S*0.16,S*0.30,S*0.40,0.26],[S*0.84,S*0.72,S*0.33,0.18]].forEach(b=>{
    const rg=x.createRadialGradient(b[0],b[1],0,b[0],b[1],b[2]);
    rg.addColorStop(0,'rgba(255,255,255,'+b[3]+')');
    rg.addColorStop(1,'rgba(255,255,255,0)');
    x.fillStyle=rg; x.fillRect(0,0,S,S);
  });
  /* the stage's own bottom vignette, so the footer always has something to sit on */
  const vg=x.createRadialGradient(S/2,S*1.02,S*0.1,S/2,S*1.02,S*0.78);
  vg.addColorStop(0,'rgba(0,0,0,.46)'); vg.addColorStop(1,'rgba(0,0,0,0)');
  x.fillStyle=vg; x.fillRect(0,0,S,S);

  const W1='rgba(255,255,255,', INK='#FFFFFF';
  x.textAlign='center';
  x.fillStyle=W1+'.72)'; x.font='600 25px "IBM Plex Mono",monospace';
  x.fillText((LAST+' WRAPPED').split('').join(' '),S/2,110);
  x.fillStyle=INK; x.font='700 46px "IBM Plex Sans",sans-serif';
  x.fillText(cardClip(x,name,S-160),S/2,184);
  x.fillStyle=W1+'.78)'; x.font='400 28px "IBM Plex Sans",sans-serif';
  x.fillText(cardClip(x,built.team,S-160),S/2,228);

  x.strokeStyle=W1+'.22)'; x.lineWidth=1;
  x.beginPath(); x.moveTo(84,278); x.lineTo(S-84,278); x.stroke();

  /* the opening slide's label repeats the kicker and its value is the manager's own
     name, both already printed above */
  const lab=cardText(c.k), val=cardText(c.v);
  const dupLab=lab.toLowerCase()===(LAST+' wrapped').toLowerCase();
  const dupVal=val.toLowerCase()===name.toLowerCase();
  if(!dupLab){
    x.fillStyle=W1+'.72)'; x.font='500 25px "IBM Plex Mono",monospace';
    x.fillText(lab.toUpperCase().split('').join(' '),S/2,338);
  }
  if(!dupVal){
    cardFit(x,val,S-150,c.sm?112:194,54,900,'"Big Shoulders Display",sans-serif');
    x.fillStyle=INK; x.fillText(val,S/2,c.sm?474:516);
  }

  const pills=(c.pills||[]).map(cardText).filter(Boolean).slice(0,3);
  const noteBot=(dupLab&&dupVal)?(pills.length?700:760):(pills.length?826:918);
  const noteTop=(dupLab&&dupVal)?326:576;
  x.font='400 36px "IBM Plex Sans",sans-serif';
  const nl=cardWrap(x,cardText(c.n),S-180).slice(0,5);
  const nStart=noteTop+Math.max(0,(noteBot-noteTop-(nl.length-1)*50)/2);
  x.fillStyle=W1+'.93)';
  nl.forEach((l,k)=>x.fillText(l,S/2,nStart+k*50));

  if(pills.length){
    /* the same lozenges the slide uses, measured so they never touch */
    x.font='500 25px "IBM Plex Mono",monospace';
    const PH=54, py=880, pad=26, gap=14;
    const ws=pills.map(q=>Math.min(S/pills.length-gap,x.measureText(q).width+pad*2));
    const tot=ws.reduce((n,w)=>n+w,0)+gap*(pills.length-1);
    let px=(S-tot)/2;
    pills.forEach((q,k)=>{
      x.fillStyle=W1+'.17)'; x.strokeStyle=W1+'.30)'; x.lineWidth=1.4;
      x.beginPath();
      if(x.roundRect)x.roundRect(px,py-PH/2,ws[k],PH,PH/2);
      else x.rect(px,py-PH/2,ws[k],PH);
      x.fill(); x.stroke();
      x.fillStyle=INK; x.textAlign='center';
      x.fillText(cardClip(x,q,ws[k]-pad),px+ws[k]/2,py+9);
      px+=ws[k]+gap;
    });
  }
  x.textAlign='center'; x.fillStyle=W1+'.8)'; x.font='600 26px "IBM Plex Mono",monospace';
  x.fillText(cardHost(),S/2,S-58);
  return new Promise(res=>cv.toBlob(res,'image/png'));
}

/* ---- 5. the rivalry, meeting by meeting ---- */
async function makeRivalryCard(an,bn){
  if(!byName[an]||!byName[bn]||an===bn)return null;
  const ms=meetings(an,bn);
  if(!ms.length)return null;
  await cardFonts();
  const {cv,x,P,S}=cardBase();
  cardKick(x,S,P,'The rivalry');
  const aw=ms.filter(m=>m.me>m.them).length, bw=ms.length-aw;

  x.textAlign='center'; x.fillStyle=P.ink;
  cardFit(x,an.toUpperCase(),S-160,62,30,900,'"Big Shoulders Display",sans-serif');
  x.fillText(an.toUpperCase(),S/2,188);
  x.fillStyle=P.dim; x.font='400 23px "IBM Plex Mono",monospace'; x.fillText('versus',S/2,228);
  x.fillStyle=P.ink;
  cardFit(x,bn.toUpperCase(),S-160,62,30,900,'"Big Shoulders Display",sans-serif');
  x.fillText(bn.toUpperCase(),S/2,290);

  x.fillStyle=P.accent; x.font='900 100px "Big Shoulders Display",sans-serif';
  x.fillText(aw+'–'+bw,S/2,402);
  x.fillStyle=P.dim; x.font='400 25px "IBM Plex Sans",sans-serif';
  x.fillText(cardClip(x,'every meeting on record, from '+an+"'s side",S-140),S/2,444);

  /* "every meeting" has to mean every meeting: the rows shrink to fit rather than the
     list being cut short. The longest rivalry on record runs to 11 games. */
  const BOT=S-140;
  /* Only steal the space above if the rows genuinely cannot fit without it. The old test
     compared against the DEFAULT step and moved the top up regardless, which dragged the
     divider rule up through the subtitle at eleven meetings. */
  let ROWTOP=534, step=Math.min(40,(BOT-ROWTOP)/ms.length);
  if(step<19){ ROWTOP=496; step=Math.min(40,(BOT-ROWTOP)/ms.length); }
  const shown=step>=19?ms:ms.slice(-Math.floor((BOT-ROWTOP)/19));
  if(step<19)step=19;
  const cut=ms.length-shown.length;
  const fs=Math.max(14,Math.min(24,step*0.60));
  cardRule(x,S,P,ROWTOP-48);
  shown.forEach((m,i)=>{
    const ty=ROWTOP+i*step, win=m.me>m.them;
    x.textAlign='left'; x.fillStyle=P.dim; x.font='400 '+(fs-1)+'px "IBM Plex Mono",monospace';
    x.fillText(String(m.y),84,ty);
    x.fillStyle=win?P.accent:P.dim; x.font='600 '+(fs-1)+'px "IBM Plex Mono",monospace';
    x.fillText(win?'W':'L',158,ty);
    x.fillStyle=P.ink; x.font='400 '+fs+'px "IBM Plex Sans",sans-serif';
    x.fillText(cardClip(x,m.rnd,250),200,ty);
    x.textAlign='right'; x.font='500 '+(fs+1)+'px "IBM Plex Mono",monospace';
    x.fillStyle=win?P.ink:P.dim;
    x.fillText(m.me.toFixed(2)+'  –  '+m.them.toFixed(2),S-84,ty);
  });
  if(cut){
    x.textAlign='center'; x.fillStyle=P.dim; x.font='italic 400 22px "IBM Plex Sans",sans-serif';
    x.fillText('and '+cut+' earlier meeting'+(cut===1?'':'s'),S/2,ROWTOP+shown.length*step+14);
  }
  cardFoot(x,S,P);
  return new Promise(res=>cv.toBlob(res,'image/png'));
}

/* ---- 6. the case against: every unflattering true thing about one manager ---- */
function roastLines(name){
  const m=byName[name]; if(!m)return null;
  const mine=ROWS.filter(r=>r.mgr===name);
  const out=[];
  if(mine.length){
    const worst=mine.reduce((a,b)=>b.pi<a.pi?b:a);
    out.push(['Worst season',worst.y+' as '+worst.team,
      ord(worst.place)+' of '+worst.teams+' at '+worst.w+'-'+worst.l+(worst.t?'-'+worst.t:'')+
      ', power index '+worst.pi.toFixed(1)+'.']);
  }
  if(!m.titles)out.push(['Titles','none in '+m.seasons+' season'+(m.seasons===1?'':'s'),
    m.podium?m.podium+' podium finish'+(m.podium===1?'':'es')+' and not one of them the top step.':'Never once on the podium.']);
  else if(m.lastTitle&&LAST-m.lastTitle>=2)out.push(['Last title',String(m.lastTitle),
    (LAST-m.lastTitle)+' seasons ago. A long time to keep bringing it up.']);
  /* the opponent they have lost to most */
  let worstOpp=null;
  M.forEach(o=>{
    if(o.name===name)return;
    const r=MX.all.t[name+'|'+o.name]; if(!r)return;
    const g=r[0]+r[1]; if(g<2)return;
    const d=r[1]-r[0];
    if(!worstOpp||d>worstOpp.d||(d===worstOpp.d&&g>worstOpp.g))worstOpp={n:o.name,w:r[0],l:r[1],d:d,g:g};
  });
  /* "It is not a rivalry if only one side wins" was firing on a 3-4 record. It now needs a
     real gap AND a win rate under a third, and the sentence quotes the numbers rather than
     making an absolute claim the record may not support. */
  if(worstOpp&&worstOpp.d>=3&&worstOpp.w/worstOpp.g<0.34)out.push(['Owned by',worstOpp.n,
    worstOpp.g+' meetings and '+worstOpp.l+' of them went the other way'+
    (worstOpp.w?'.':'. Not one has ever gone his.')]);
  if(m.luck>=0.5)out.push(['Luck','+'+m.luck.toFixed(2)+' wins',
    'The scoring earned about '+m.pythW.toFixed(1)+' wins. The record says '+m.w+'. The schedule did the work.']);
  else if(m.vsWinPct!=null&&m.vsWinPct<0.5)out.push(['Against good teams',pct(m.vsWinPct),
    m.vsWinW+'-'+m.vsWinL+' against winning teams, '+pct(m.vsSubPct)+' against everyone else. Beats who they are supposed to beat.']);
  if(m.apps<m.seasons)out.push(['Missed the playoffs',
    (m.seasons-m.apps)+' of '+m.seasons+' seasons',
    'In the bracket '+m.apps+' time'+(m.apps===1?'':'s')+', '+m.poW+'-'+m.poL+' once there.']);
  if(m.floor!=null)out.push(['Floor',m.floor.toFixed(1),
    'The worst version of this manager, on the same scale where 100 is league average.']);
  return {m:m,lines:out.slice(0,5)};
}
async function makeRoastCard(name){
  const R=roastLines(name); if(!R||!R.lines.length)return null;
  await cardFonts();
  const {cv,x,P,S}=cardBase();
  cardKick(x,S,P,'The case against');
  x.textAlign='center'; x.fillStyle=P.ink;
  cardFit(x,name.toUpperCase(),S-140,116,44,900,'"Big Shoulders Display",sans-serif');
  x.fillText(name.toUpperCase(),S/2,232);
  x.fillStyle=P.dim; x.font='400 28px "IBM Plex Sans",sans-serif';
  x.fillText(R.m.seasons+' season'+(R.m.seasons===1?'':'s')+'  ·  '+R.m.w+'-'+R.m.l+
    (R.m.t?'-'+R.m.t:''),S/2,280);

  /* measure first: a fact that runs off the bottom of the card is worth less than one
     fewer fact that fits, so entries are dropped from the end until the stack clears
     the footer */
  const TOP=346, BOT=S-118;
  x.font='400 26px "IBM Plex Sans",sans-serif';
  const blocks=R.lines.map(L=>{
    const ls=cardWrap(x,L[2],S-168).slice(0,2);
    return {L:L,ls:ls,h:104+ls.length*32};
  });
  while(blocks.length>1&&blocks.reduce((n,b)=>n+b.h,0)>BOT-TOP)blocks.pop();
  let y=TOP;
  blocks.forEach(B=>{
    cardRule(x,S,P,y-32);
    x.textAlign='left'; x.fillStyle=P.dim; x.font='500 21px "IBM Plex Mono",monospace';
    x.fillText(B.L[0].toUpperCase().split('').join(' '),84,y);
    x.fillStyle=P.accent; x.font='700 39px "IBM Plex Sans",sans-serif';
    x.fillText(cardClip(x,B.L[1],S-168),84,y+46);
    x.fillStyle=P.ink; x.font='400 26px "IBM Plex Sans",sans-serif';
    B.ls.forEach((t,k)=>x.fillText(t,84,y+86+k*32));
    y+=B.h;
  });
  cardFoot(x,S,P);
  return new Promise(res=>cv.toBlob(res,'image/png'));
}

/* ---- one wrapper so a new card needs one line of wiring ---- */
async function shareAny(builder,fname,btn){
  const label=btn?btn.innerHTML:null;
  if(btn){btn.disabled=true;btn.innerHTML='Building…';}
  try{
    const blob=await builder();
    if(!blob){toast('Nothing to put on a card here');return;}
    await shareBlob(blob,fname);
  }catch(e){ if(!(e&&e.name==='AbortError'))toast('Could not build the card'); }
  finally{ if(btn){btn.disabled=false;btn.innerHTML=label;} }
}
const slug=s=>String(s).toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');

/* ---- 7. links that open the site on one exact thing ----
   A picture is good for the group chat; a link is better for an argument, because the
   other person lands on the live page and can keep digging. */
/* A link preview is fetched by Discord or iMessage from the URL alone, server-side, with
   no idea which theme the sharer was looking at. So a shared link points at a one-line
   shim page per theme (t/<skin>.html) that carries the matching og:image and bounces a
   real person straight through to the site with their query and hash intact. Redacted
   maps to Classic on purpose: the hidden theme should not be what greets a stranger. */
const OG_SKINS=['red','og','scope','leather','arcade','redact'];
function deepLink(params,hash){
  let origin;
  try{ origin=location.origin; }catch(e){ origin=''; }
  if(!origin||location.protocol==='file:')origin='https://'+cardHost();
  let skin=''; try{ skin=document.documentElement.dataset.skin||'red'; }catch(e){ skin='red'; }
  const path=OG_SKINS.indexOf(skin)>=0?('/t/'+skin):'/';   /* cleanUrls serves it without .html */
  const q=Object.keys(params).filter(k=>params[k]!=null&&params[k]!=='')
    .map(k=>encodeURIComponent(k)+'='+encodeURIComponent(params[k])).join('&');
  return origin+path+(q?'?'+q:'')+(hash?'#'+hash:'');
}
async function copyLink(url,btn){
  const label=btn?btn.innerHTML:null;
  try{
    if(navigator.clipboard&&navigator.clipboard.writeText)await navigator.clipboard.writeText(url);
    else{
      const ta=document.createElement('textarea'); ta.value=url;
      ta.style.position='fixed'; ta.style.opacity='0'; document.body.appendChild(ta);
      ta.select(); document.execCommand('copy'); ta.remove();
    }
    if(btn){btn.innerHTML='Copied';setTimeout(()=>{btn.innerHTML=label;},1400);}
    else toast('Link copied');
  }catch(e){ toast('Could not copy the link'); }
}
/* one handler for every copy-link button on the page, so new ones need no wiring:
   data-link is a query string, data-link-hash is the section to land on */
document.addEventListener('click',e=>{
  const b=e.target.closest('[data-link]'); if(!b)return;
  e.preventDefault();
  const p={}; String(b.dataset.link).split('&').filter(Boolean).forEach(kv=>{
    const i=kv.indexOf('='); if(i>0)p[kv.slice(0,i)]=kv.slice(i+1);});
  copyLink(deepLink(p,b.dataset.linkHash||''),b);
});

/* ---- wiring for the new cards ----
   Delegated, because the season pane and the weekly scoreboard are rebuilt from
   scratch every time the reader changes year or week, and per-render handlers would
   have to be re-attached each time. */
document.addEventListener('click',e=>{
  const sea=e.target.closest('#seaShare');
  if(sea){
    const on=$$('#yrPills button.on')[0]; if(!on)return;
    const y=+on.dataset.y;
    shareAny(()=>makeSeasonCard(y),'deadshot-'+y+'-season.png',sea);
    return;
  }
  const brk=e.target.closest('#brkShare');
  if(brk){
    const on=$$('#yrPills button.on')[0]; if(!on)return;
    const y=+on.dataset.y;
    shareAny(()=>makeBracketCard(y),'deadshot-'+y+'-bracket.png',brk);
    return;
  }
  if(e.target.closest('#wkLink')){
    const wl=e.target.closest('#wkLink');
    const wy=$$('#wkYears button.on')[0], ww=$$('#wkSel button.on')[0];
    copyLink(deepLink({y:wy?wy.dataset.wy:'',w:ww?ww.dataset.w:''},'weekly'),wl);
    return;
  }
  const rec=e.target.closest('[data-receipt]');
  if(rec){
    const bits=String(rec.dataset.receipt).split('|');
    const y=+bits[0], wk=+bits[1], team=bits[2];
    shareAny(()=>makeGameCard(y,wk,team),'deadshot-'+y+'-week'+wk+'-'+slug(team)+'.png',rec);
  }
});
/* the record picker: the list is generated, so it stays true when the numbers move */
(function(){
  const sel=$('#recPick'), btn=$('#recShare');
  if(!sel||!btn)return;
  const R=bigRecords();
  if(!R.length){sel.style.display='none';btn.style.display='none';return;}
  sel.innerHTML=R.map((r,i)=>'<option value="'+i+'">'+esc(r.k)+'</option>').join('');
  sel.setAttribute('aria-label','Which record to put on a card');
  btn.onclick=()=>shareAny(()=>makeRecordCard(+sel.value),
    'deadshot-record-'+slug(R[+sel.value].k)+'.png',btn);
})();
/* Wrapped: share whatever card is on screen. The story keeps running behind the share
   sheet otherwise, so it is held until the sheet closes. */
(function(){
  const b=$('#wrShare'); if(!b)return;
  b.addEventListener('click',async e=>{
    e.stopPropagation();
    const was=WR.paused; WR.paused=true;
    try{
      await shareAny(()=>makeWrapCard(WR.name,WR.i),
        'deadshot-wrapped-'+slug(WR.name)+'-'+(WR.i+1)+'.png',b);
    }finally{ WR.paused=was; }
  });
})();

/* ---- From the archive -------------------------------------------------------
   A rotating moment pulled from the record. Seeded by the calendar day, so it is
   stable all day and different tomorrow, and never random on reload. During the NFL
   season it prefers moments from the matching week; out of season it draws from
   anything. Nothing here is written by hand: every line is generated from the data,
   so it stays true when the numbers change. */
function nflWeek(d){
  /* NFL week 1 lands in the first full week of September. Good enough to match a
     moment to roughly the right part of the season; it is decoration, not a fixture list. */
  const y=d.getFullYear();
  const sep=new Date(y,8,1);
  const firstThu=new Date(y,8,1+((4-sep.getDay())+7)%7);
  const diff=Math.floor((d-firstThu)/(7*24*3600*1000))+1;
  return (diff>=1&&diff<=17)?diff:null;
}
function archiveMoments(){
  const out=[];
  const S2=v=>v.toFixed(2);
  /* every title game */
  D.champs.forEach(c=>{
    const fin=D.games.filter(g=>g.y===c.y&&g.rnd==='Final'&&!g.void)[0];
    if(fin){
      const win=fin.pa>fin.pb?fin:{ta:fin.tb,ma:fin.mb,pa:fin.pb,tb:fin.ta,mb:fin.ma,pb:fin.pa};
      out.push({wk:fin.wk,y:c.y,html:`In <b>${c.y}</b>, ${esc(win.ta)} (${esc(win.ma)}) beat ${esc(win.tb)} `+
        `<b>${S2(win.pa)}&ndash;${S2(win.pb)}</b> to take the title.`});
    } else if(c.co){
      out.push({wk:17,y:c.y,html:`The <b>${c.y}</b> final was never resolved. ${esc(c.mgrs.join(' and '))} `+
        `split the title and the winnings.`});
    }
  });
  /* every playoff game, framed by how it went */
  D.games.filter(g=>!g.void).forEach(g=>{
    const m=Math.abs(g.pa-g.pb), hi=g.pa>g.pb?g:{ta:g.tb,ma:g.mb,pa:g.pb,tb:g.ta,mb:g.ma,pb:g.pa};
    if(m<6) out.push({wk:g.wk,y:g.y,html:`<b>${g.y}</b> ${esc(g.rnd.toLowerCase())}: ${esc(hi.ta)} survived `+
      `${esc(hi.tb)} by <b>${S2(m)}</b>, ${S2(hi.pa)} to ${S2(hi.pb)}.`});
    else if(m>55) out.push({wk:g.wk,y:g.y,html:`<b>${g.y}</b> ${esc(g.rnd.toLowerCase())}: ${esc(hi.ta)} `+
      `buried ${esc(hi.tb)} by <b>${S2(m)}</b>, ${S2(hi.pa)} to ${S2(hi.pb)}.`});
  });
  /* regular season extremes, from the seasons with a game log */
  (D.wkYears||[]).forEach(y=>{
    const K=D.wk[y]; if(!K)return;
    const flat=[];
    K.games.forEach(g=>{flat.push({wk:g.wk,t:g.ta,p:g.aa,o:g.tb,op:g.ab,br:g.br});
                        flat.push({wk:g.wk,t:g.tb,p:g.ab,o:g.ta,op:g.aa,br:g.br});});
    const reg=flat.filter(x=>!x.br);
    if(!reg.length)return;
    const top=reg.reduce((a,b)=>b.p>a.p?b:a);
    out.push({wk:top.wk,y:+y,html:`Week ${top.wk} of <b>${y}</b>: ${esc(top.t)} hung `+
      `<b>${S2(top.p)}</b> on ${esc(top.o)}, the biggest score of that regular season.`});
    const low=reg.reduce((a,b)=>b.p<a.p?b:a);
    out.push({wk:low.wk,y:+y,html:`Week ${low.wk} of <b>${y}</b>: ${esc(low.t)} managed `+
      `<b>${S2(low.p)}</b>, the quietest week anyone had that year.`});
    /* best score that still lost */
    const robbed=reg.filter(x=>x.p<x.op).reduce((a,b)=>(!a||b.p>a.p)?b:a,null);
    if(robbed) out.push({wk:robbed.wk,y:+y,html:`Week ${robbed.wk} of <b>${y}</b>: ${esc(robbed.t)} scored `+
      `<b>${S2(robbed.p)}</b> and still lost, because ${esc(robbed.o)} answered with ${S2(robbed.op)}.`});
    /* worst score that still won */
    const gifted=reg.filter(x=>x.p>x.op).reduce((a,b)=>(!a||b.p<a.p)?b:a,null);
    if(gifted) out.push({wk:gifted.wk,y:+y,html:`Week ${gifted.wk} of <b>${y}</b>: ${esc(gifted.t)} won with just `+
      `<b>${S2(gifted.p)}</b>, because ${esc(gifted.o)} could only find ${S2(gifted.op)}.`});
    /* the biggest trade of that year */
    const big=(K.trades||[]).reduce((a,b)=>(!a||(b.pa.length+b.pb.length)>(a.pa.length+a.pb.length))?b:a,null);
    if(big&&(big.pa.length+big.pb.length)>=5)
      out.push({wk:null,y:+y,html:`<b>${y}</b>, ${esc(big.d)}: ${esc(big.ta)} and ${esc(big.tb)} swapped `+
        `<b>${big.pa.length+big.pb.length} players</b> in one deal.`});
  });
  /* season-level oddities */
  ROWS.forEach(r=>{
    if(r.luck<=-3.2) out.push({wk:null,y:r.y,html:`${esc(r.team)} finished <b>${r.w}-${r.l}</b> in ${r.y} `+
      `while the scoring earned about <b>${r.pythW.toFixed(1)}</b> wins. The schedule took the rest.`});
    if(r.luck>=3.2) out.push({wk:null,y:r.y,html:`${esc(r.team)} banked <b>${r.w}-${r.l}</b> in ${r.y} `+
      `on scoring worth about <b>${r.pythW.toFixed(1)}</b> wins. Nobody gave it back.`});
    if(r.place===1&&r.seed>=4) out.push({wk:null,y:r.y,html:`${esc(r.team)} went into the ${r.y} playoffs `+
      `as the <b>${ord(r.seed)} seed</b> and came out with the title.`});
  });
  return out;
}
function drawArchive(){
  const host=$('#arcMoment'); if(!host)return;
  const all=archiveMoments(); if(!all.length)return;
  const now=new Date();
  const wk=nflWeek(now);
  const pool=wk?all.filter(m=>m.wk!=null&&Math.abs(m.wk-wk)<=1):[];
  const use=pool.length?pool:all;
  /* day number as the seed: same moment all day, a new one tomorrow */
  const day=Math.floor((now-new Date(now.getFullYear(),0,0))/86400000)+now.getFullYear()*372;
  const pick=use[day%use.length];
  host.innerHTML=pick.html;
  const lab=$('#arcLabel');
  if(lab)lab.textContent=wk&&pool.length?('From the archive · week '+wk):'From the archive';
}

/* ---- Milestone watch --------------------------------------------------------
   Round numbers each manager is closest to. Everyone is shown: it is a ten-person
   league where everybody already knows everybody's business. */
function drawMilestones(){
  const host=$('#mileWatch'); if(!host)return;
  const people=[...M].filter(m=>vis(m.name));
  const rows=[];
  people.forEach(m=>{
    const near=[];
    const step=(v,size,label,unit)=>{
      const next=Math.ceil((v+0.0001)/size)*size;
      near.push({gap:next-v,txt:`<b>${Math.round(next-v).toLocaleString()}</b> ${unit} from ${next.toLocaleString()} ${label}`,pct:v/next});
    };
    step(m.pf,1000,'career points','pts');
    step(m.w,10,'career wins','wins');
    if(m.poG) step(m.poW,5,'playoff wins','wins');
    step(m.g,25,'games played','games');
    near.sort((a,b)=>a.pct===b.pct?a.gap-b.gap:b.pct-a.pct);
    rows.push({m,best:near[0]});
  });
  rows.sort((a,b)=>b.best.pct-a.best.pct);
  host.innerHTML=`<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr));gap:10px 20px">`+
    rows.map(r=>`<div style="display:flex;gap:9px;align-items:baseline;padding:3px 0">`+
      `<span style="flex:0 0 auto">${mlink(r.m.name)}</span>`+
      `<span class="dim" style="font-size:12.5px;min-width:0">${r.best.txt}</span></div>`).join('')+
    `</div><p style="margin:12px 0 0;font-size:12px;color:var(--ink-3)">Closest target first. Career totals only, so these move once a new season is loaded.</p>`;
}
drawArchive(); REDRAW.push(drawArchive);
drawMilestones(); REDRAW.push(drawMilestones);

/* ---- shareable links ----------------------------------------------------------
   Every view used to live at the same address, so nobody could send "look at my 2021
   season" -- the link always opened on the newest year. The address bar now mirrors
   the season and manager on screen, and a fresh visit restores what the link asked for.
   replaceState, not pushState, so picking years does not stack up back-button steps. */
function setUrlParam(k,v){
  try{
    const q=new URLSearchParams(location.search);
    v?q.set(k,String(v)):q.delete(k);
    const qs=q.toString();
    history.replaceState(null,'',(qs?'?'+qs:location.pathname)+location.hash);
  }catch(e){}
}
function applyUrlState(){
  try{
    const q=new URLSearchParams(location.search);
    const y=parseInt(q.get('y'),10);
    if(y){
      /* a shared year means both year-driven sections, so the whole page reads as
         that season no matter which one the reader scrolls to first */
      const wy=$$(`#wkYears button[data-wy="${y}"]`)[0];
      if(wy&&!wy.disabled&&typeof drawWeekly==='function')drawWeekly(y);
      const sy=$$(`#yrPills button[data-y="${y}"]`)[0];
      if(sy&&typeof drawSeason==='function')drawSeason(y);
    }
    const wk=parseInt(q.get('w'),10);
    if(wk){const wb=$$('#wkSel button[data-w="'+wk+'"]')[0]; if(wb)wb.click();}
    const m=q.get('m');
    if(m){const b=$$('#crPick button[data-cm]').filter(x=>x.dataset.cm===m)[0];
      if(b){CRMGR=m;CRLOCK.clear();drawCareerRace();}}
    if(location.hash){const t=document.querySelector(location.hash);
      if(t)setTimeout(()=>t.scrollIntoView(),60);}
  }catch(e){}
}
/* the rest of the page still has initial draws to run; go last so nothing overwrites us */
setTimeout(applyUrlState,0);
/* record whichever picker the reader actually touched -- reading it back off the DOM
   picked up the other section's year instead */
(function(){
  const wire=(sel,attr,key)=>{const host=$(sel); if(!host)return;
    host.addEventListener('click',e=>{const b=e.target.closest('button['+attr+']');
      if(b)setTimeout(()=>setUrlParam(key,b.getAttribute(attr)),0);});};
  wire('#wkYears','data-wy','y');
  wire('#yrPills','data-y','y');
  wire('#crPick','data-cm','m');
  wire('#wkSel','data-w','w');
})();

function drawWeekly(YR){
  $$('#wkYears button[data-wy]').forEach(b=>b.classList.toggle('on',+b.dataset.wy===YR));
  const nowEl=$('#wkNow'); if(nowEl)nowEl.textContent='viewing '+YR;
  WKREDRAW.forEach(f=>{const i=REDRAW.indexOf(f); if(i>=0)REDRAW.splice(i,1);});
  WKREDRAW=[];
  const push=f=>{WKREDRAW.push(f);REDRAW.push(f);};
  const K5=D.wk[YR]; if(!K5)return;
  const T=K5.teams, MG=K5.mgr, WKS=K5.weeks;
  /* ---- bump chart: league position by week ---- */
  const W=980,H=392,P={t:22,r:158,b:34,l:46};
  const NCOL=WKS.length+1;                    /* +1 = the FINAL placement column */
  const xs=i=>P.l+i*(W-P.l-P.r)/(NCOL-1);
  const FINX=xs(NCOL-1), GAPX=(xs(WKS.length-1)+FINX)/2;
  const PLACE={}; ROWS.filter(r=>r.y===YR).forEach(r=>PLACE[r.team]=r.place);
  const ys=r=>P.t+(r-1)*(H-P.t-P.b)/(T.length-1);
  const RANK={}; T.forEach(t=>RANK[t]=[]);
  WKS.forEach((w,i)=>{
    const snap=T.map(t=>{const seq=K5.race[t];
      return {t,wins:seq[i].wins,pf:seq.slice(0,i+1).reduce((s,x)=>s+x.pts,0)};});
    snap.sort((x,y)=>y.wins-x.wins||y.pf-x.pf);
    snap.forEach((o,k)=>RANK[o.t].push({w,rank:k+1,wins:o.wins,pf:o.pf}));});
  const SPOTS=(D.champs.find(c=>c.y===YR)||{}).spots||6;
  let grid='';
  for(let r=1;r<=T.length;r++){
    grid+=`<line x1="${P.l}" x2="${W-P.r}" y1="${ys(r)}" y2="${ys(r)}" stroke="var(--rule-2)"/>
      <text x="${P.l-11}" y="${ys(r)+4}" text-anchor="end" font-size="10.5" fill="${r<=SPOTS?'var(--brass-2)':'var(--ink-3)'}" font-family="IBM Plex Mono,monospace">${r}</text>`;}
  const cut=(ys(SPOTS)+ys(SPOTS+1))/2;
  grid=`<rect x="${P.l}" y="${P.t-14}" width="${xs(WKS.length-1)-P.l+10}" height="${cut-P.t+14}" fill="var(--band)"/>`+grid+
    `<line x1="${P.l}" x2="${W-P.r}" y1="${cut}" y2="${cut}" stroke="var(--brass-2)" stroke-dasharray="5 4" opacity=".9"/>`+
    `<line x1="${GAPX}" x2="${GAPX}" y1="${P.t-14}" y2="${H-P.b+4}" stroke="var(--rule)" stroke-dasharray="3 4"/>
     <text x="${GAPX}" y="${P.t-19}" text-anchor="middle" font-size="9" fill="var(--ink-3)" font-family="IBM Plex Mono,monospace" letter-spacing="1.6">POSTSEASON</text>`;
  const lines=T.map(t=>{
    const reg=RANK[t].map((p,i)=>(i?'L':'M')+xs(i)+','+ys(p.rank)).join(' ');
    const endRank=RANK[t][RANK[t].length-1].rank, fp=PLACE[t]||endRank;
    return {t,m:MG[t],d:reg,fin:{rank:fp},seedRank:endRank,moved:endRank-fp};});
  lines.sort((a,b)=>a.fin.rank-b.fin.rank||a.t.localeCompare(b.t));
  /* co-champions share a final placing (2022), so their end dots and labels would
     land on the exact same point. Fan any tied group apart instead of stacking it. */
  const MEDAL={1:{f:'#D9A82B',s:'#8A6710',i:'#3A2A05'},2:{f:'#AEB6BD',s:'#6E767D',i:'#2B3035'},3:{f:'#B9793F',s:'#7A4B20',i:'#2E1A08'}};
  const tie={}; lines.forEach(l=>{(tie[l.fin.rank]=tie[l.fin.rank]||[]).push(l);});
  Object.values(tie).forEach(g=>g.forEach((l,j)=>{
    const k=g.length, off=k>1?(j-(k-1)/2):0;
    l.fy=ys(l.fin.rank)+off*11;
    l.fx=FINX+(k>1?off*8:0);
    l.tied=k>1;}));
  lines.forEach(l=>{l.tail=`M${xs(WKS.length-1)},${ys(l.seedRank)} L${l.fx},${l.fy}`;});
  const paths=lines.map(l=>`<path class="rl" d="${l.d}" fill="none" stroke="var(--mid)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" data-t="${esc(l.t)}" data-mgr="${esc(l.m)}"/>`
    +`<path class="rl rt2" d="${l.tail}" fill="none" stroke="var(--mid)" stroke-width="2" stroke-dasharray="4 3" stroke-linecap="round" data-t="${esc(l.t)}" data-mgr="${esc(l.m)}"/>`).join('');
  const hits=lines.map(l=>`<path class="hit" d="${l.d}" fill="none" stroke="transparent" stroke-width="15" data-t="${esc(l.t)}" data-mgr="${esc(l.m)}" style="cursor:pointer;pointer-events:stroke"/>`).join('');
  let dots='';
  lines.forEach(l=>{RANK[l.t].forEach((p,i)=>{
    dots+=`<circle class="rd" cx="${xs(i)}" cy="${ys(p.rank)}" r="4.4" fill="var(--surface)" stroke="var(--mid)" stroke-width="2" data-t="${esc(l.t)}" data-mgr="${esc(l.m)}" data-i="${i}" style="cursor:pointer"/>`;});
    dots+=`<circle class="rd rf" cx="${l.fx}" cy="${l.fy}" r="5.6" fill="var(--surface)" stroke="var(--brass-2)" stroke-width="2.4" data-t="${esc(l.t)}" data-mgr="${esc(l.m)}" data-fin="1" style="cursor:pointer"/>`;});
  /* second pass: nothing may sit closer than one line-height to its neighbour */
  const LY=[]; lines.forEach((l,i)=>{let y=l.fy+3.5;
    if(i&&y-LY[i-1]<13)y=LY[i-1]+13; LY.push(y);});
  const labs=lines.map((l,i)=>`<text class="rt" x="${W-P.r+12}" y="${LY[i]}" font-size="11.5" fill="var(--ink-2)" font-family="IBM Plex Sans,sans-serif" data-t="${esc(l.t)}" data-mgr="${esc(l.m)}" data-medal="${MEDAL[l.fin.rank]?l.fin.rank:''}" style="cursor:pointer">${esc(l.t)}${l.tied?' <tspan fill="var(--brass-2)">&#9670;</tspan>':''}</text>`).join('')
    +lines.map((l,i)=>Math.abs(LY[i]-(l.fy+3.5))>1.5
      ? `<line x1="${l.fx+7}" x2="${W-P.r+9}" y1="${l.fy}" y2="${LY[i]-3.5}" stroke="var(--rule)" stroke-width="1"/>`:'').join('');
  const wl=WKS.map((w,i)=>`<text x="${xs(i)}" y="${H-P.b+20}" text-anchor="middle" font-size="10.5" fill="var(--ink-3)" font-family="IBM Plex Mono,monospace">${w}</text>`).join('')
    +`<text x="${FINX}" y="${H-P.b+20}" text-anchor="middle" font-size="10" fill="var(--brass-2)" font-family="IBM Plex Mono,monospace" letter-spacing="1">FIN</text>`;
  $('#race').innerHTML=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="League position by week for all ${T.length} teams in ${YR}; rank one at the top">
    ${grid}${paths}${dots}${hits}${labs}${wl}
    <text x="${P.l-11}" y="${H-P.b+20}" text-anchor="end" font-size="9.5" fill="var(--ink-3)" font-family="IBM Plex Mono,monospace">WK</text></svg>`;
  /* medals ride to the right of the name — measured after render, so they never overlap */
  (function(){
    const svg=$('#race svg'); if(!svg)return;
    const NS='http://www.w3.org/2000/svg';
    $$('#race .rt').forEach(t=>{
      const rk=t.dataset.medal; if(!rk)return;
      const md=MEDAL[+rk]; let w=0; try{w=t.getComputedTextLength();}catch(e){w=t.textContent.length*6.2;}
      const x=+t.getAttribute('x')+w+9, y=+t.getAttribute('y')-3.6;
      const g=document.createElementNS(NS,'g'); g.setAttribute('class','medal'); g.style.pointerEvents='none';
      const c=document.createElementNS(NS,'circle');
      c.setAttribute('cx',x);c.setAttribute('cy',y);c.setAttribute('r',6.6);
      c.setAttribute('fill',md.f);c.setAttribute('stroke',md.s);c.setAttribute('stroke-width',1.6);
      const n=document.createElementNS(NS,'text');
      n.setAttribute('x',x);n.setAttribute('y',y+3.1);n.setAttribute('text-anchor','middle');
      n.setAttribute('font-size',8.6);n.setAttribute('font-weight',700);n.setAttribute('fill',md.i);
      n.setAttribute('font-family','IBM Plex Mono,monospace');n.textContent=rk;
      g.appendChild(c);g.appendChild(n);svg.appendChild(g);});
  })();
  {const rs=$('#raceSpots'); if(rs)rs.textContent=`${SPOTS} of ${T.length} teams made it in ${YR}`;}
  $('#raceLeg').innerHTML=`<span class="fb-lab" style="margin-right:4px">Teams</span>`+
    lines.map(l=>`<button data-t="${esc(l.t)}" data-mgr="${esc(l.m)}" style="padding:4px 9px">${esc(l.t)} <span class="dim">${esc(l.m.split(' ')[0])}</span></button>`).join('')+
    `<button id="raceClear" style="padding:4px 9px">Clear</button>`;
  const RPICK=new Set(); let RHOV=null;
  function paint(hoverT){
    if(hoverT!==undefined)RHOV=hoverT;
    const on=RPICK.size?RPICK:(RHOV?new Set([RHOV]):new Set()), any=on.size>0;
    $$('#race .rl').forEach(p=>{const sel=on.has(p.dataset.t), sh=true;
      p.setAttribute('stroke',sel?'var(--brass)':'var(--mid)');
      p.setAttribute('stroke-width',sel?3.4:2);
      p.setAttribute('opacity',!sh?.06:(!any||sel?1:.14));
      p.style.filter=sel?'drop-shadow(0 0 6px var(--glow))':'none';});
    $$('#race .rd').forEach(c=>{const sel=on.has(c.dataset.t), sh=true;
      c.setAttribute('stroke',sel?'var(--brass)':'var(--mid)');
      c.setAttribute('r',sel?5.4:4.4);
      c.setAttribute('opacity',!sh?.06:(!any||sel?1:.14));});
    $$('#race .rt').forEach(x=>{const sel=on.has(x.dataset.t), sh=true;
      x.setAttribute('fill',sel?'var(--brass)':(sh?'var(--ink-2)':'var(--rule)'));
      x.setAttribute('font-weight',sel?700:400);
      x.setAttribute('opacity',!sh?.35:(!any||sel?1:.35));});
    $$('#raceLeg button[data-t]').forEach(b=>{
      b.classList.toggle('on',RPICK.has(b.dataset.t));
      b.style.opacity=1;});
  }
  const rtoggle=t=>{RPICK.has(t)?RPICK.delete(t):RPICK.add(t);paint();};
  function weekTip(t,i){
    const seq=K5.race[t], s=seq[i], p=RANK[t][i];
    const others=T.filter(o=>o!==t).map(o=>K5.race[o][i].pts);
    const scoreRank=others.filter(x=>x>s.pts).length+1;
    const vsProj=s.pts-s.proj;
    return `<b>${esc(t)}</b> &middot; ${esc(MG[t])}
      <br><span style="opacity:.7">After week ${s.w}</span>
      <br>Position <b>${ord(p.rank)}</b> of 10 &middot; record <b>${p.wins}-${s.w-p.wins}</b>
      <br>${s.win?'<b style="color:var(--brass)">WON</b>':'<span style="color:var(--neg)">lost</span>'} ${s.pts.toFixed(2)}&ndash;${s.oppPts.toFixed(2)} vs ${esc(s.opp)}
      <br>${scoreRank===1?'<b>top score of the week</b>':ord(scoreRank)+' highest that week'} &middot; beat ${s.ap} of 9
      <br>Proj ${s.proj.toFixed(1)} (${vsProj>=0?'+':''}${vsProj.toFixed(1)}) &middot; PF ${p.pf.toFixed(1)}`;
  }
  function nearestWeek(clientX){
    const r=$('#race svg').getBoundingClientRect();
    const vx=(clientX-r.left)/r.width*W;           /* NCOL-1, not WKS.length-1: the FIN column owns a slot too */
    const step=(W-P.l-P.r)/(NCOL-1);
    return Math.max(0,Math.min(WKS.length-1,Math.round((vx-P.l)/step)));
  }
  function finTip(t){
    const l=lines.find(x=>x.t===t), mv=l.moved;
    const last=RANK[t][RANK[t].length-1];
    const wins=last.wins, losses=WKS.length-wins;
    const pog=K5.games.filter(g=>g.br&&(g.ta===t||g.tb===t));
    let pw=0,pl=0,ppf=0,vd=0;
    pog.forEach(g=>{const mine=g.ta===t?g.aa:g.ab, opp=g.ta===t?g.ab:g.aa;
      ppf+=mine;
      if(isVoid(YR,g.wk,g.ta,g.tb)){vd++;return;}   /* played, never resolved */
      if(mine>opp)pw++; else pl++;});
    const pby=K5.byes.filter(b=>b.t===t); pby.forEach(b=>{ppf+=b.a;});
    return `<b>${esc(t)}</b> &middot; ${esc(MG[t])}
      <br><span style="opacity:.7">Final placing</span>${l.tied?' <span style="color:var(--brass)">&#9670; shared</span>':''}
      <br>Regular season <b>${wins}-${losses}</b> &middot; ${last.pf.toFixed(2)} PF
      <br>Finished <b>${ord(l.fin.rank)}</b> from the ${ord(l.seedRank)} seed
      <br>${pog.length?`Postseason <b>${pw}-${pl}</b>${vd?` <span style="color:var(--brass)">+${vd} void</span>`:''} &middot; ${ppf.toFixed(2)} PF`:(pby.length?`Postseason <b>0-0</b> &middot; bye only &middot; ${ppf.toFixed(2)} PF`:'Did not play the postseason')}
      <br>${mv>0?'<b style="color:var(--brass)">+'+mv+' in the postseason</b>':mv<0?'<span style="color:var(--neg)">'+mv+' in the postseason</span>':'held its seed'}`;
  }
  $$('#race .rd').forEach(c=>{
    c.addEventListener('mouseenter',e=>{paint(c.dataset.t);
      showTip(e,c.dataset.fin?finTip(c.dataset.t):weekTip(c.dataset.t,+c.dataset.i));});
    c.addEventListener('mousemove',moveTip);
    c.addEventListener('mouseleave',()=>{paint(null);hideTip();});
    c.addEventListener('click',e=>{e.stopPropagation();rtoggle(c.dataset.t);});});
  $$('#race .hit').forEach(p=>{
    p.addEventListener('mouseenter',e=>{paint(p.dataset.t);showTip(e,weekTip(p.dataset.t,nearestWeek(e.clientX)));});
    p.addEventListener('mousemove',e=>{tip.innerHTML=weekTip(p.dataset.t,nearestWeek(e.clientX));moveTip(e);});
    p.addEventListener('mouseleave',()=>{paint(null);hideTip();});
    p.addEventListener('click',()=>rtoggle(p.dataset.t));});
  /* the team-name label always sits past the last week, in the FIN/medal column --
     it's a fixed end-of-line marker like the medal dot, never a mid-line position,
     so it must show the same final-placing tooltip the medal shows, not a weekly one
     computed from mouse X (which was clamping to the last real week, e.g. "week 14"). */
  $$('#race .rt').forEach(p=>{
    p.addEventListener('mouseenter',e=>{paint(p.dataset.t);showTip(e,finTip(p.dataset.t));});
    p.addEventListener('mousemove',moveTip);
    p.addEventListener('mouseleave',()=>{paint(null);hideTip();});
    p.addEventListener('click',()=>rtoggle(p.dataset.t));});
  $$('#raceLeg button[data-t]').forEach(b=>{
    b.addEventListener('mouseenter',()=>paint(b.dataset.t));
    b.addEventListener('mouseleave',()=>paint(null));
    b.addEventListener('click',()=>rtoggle(b.dataset.t));
  });
  $('#raceClear').onclick=()=>{RPICK.clear();paint();};
  paint(null);
  push(()=>paint(null));

  /* all-play table */
  const ap=T.map(t=>{const a=K5.allplay[t], seq=K5.race[t], real=seq[seq.length-1].wins;
    const pts=seq.reduce((s,x)=>s+x.pts,0), pr=seq.reduce((s,x)=>s+x.proj,0);
    return {t,m:MG[t],apw:a.w,apl:a.l,appct:a.pct,real,exp:a.pct*WKS.length,
      luck:real-a.pct*WKS.length,pts,proj:pr,diff:pts-pr,per:(pts-pr)/WKS.length,
      hi:Math.max(...seq.map(x=>x.pts)),lo:Math.min(...seq.map(x=>x.pts)),
      fm:(K5.form||{})[t]};});
  function drawAP(){table($('#tAP'),[
   {h:'Team',f:r=>esc(r.t),c:'nm',k:r=>r.t,asc:1},
   {h:'Manager',f:r=>mlink(r.m),k:r=>r.m,asc:1},
   {h:'Real W-L',f:r=>`<span class="mono">${r.real}-${WKS.length-r.real}</span>`,c:'num',k:r=>r.real},
   {h:'All-play W-L',f:r=>`<span class="mono">${r.apw}-${r.apl}</span>`,c:'num',k:r=>r.appct,t:'Record if you had played every team every week'},
   {h:'All-play %',f:r=>pct(r.appct),c:'num',k:r=>r.appct},
   {h:'Deserved W',f:r=>f(r.exp,1),c:'num',k:r=>r.exp},
   {h:'Luck',f:r=>f(r.luck),c:'num',k:r=>r.luck,t:'Real wins minus all-play expected wins — the cleanest luck measure there is'},
   {h:'',f:r=>dbar(r.luck,3.2,pol(r.luck)),k:r=>r.luck},
   {h:'High',f:r=>f(r.hi),c:'num',k:r=>r.hi},
   {h:'Low',f:r=>f(r.lo),c:'num',k:r=>r.lo},
   {h:'Week σ',f:r=>r.fm?f(r.fm.sd,1):'—',c:'num',k:r=>r.fm?r.fm.sd:null,
    t:'Standard deviation of this team\u2019s weekly scores. Low = metronome, high = boom or bust. This is real week-to-week volatility, unlike the season-to-season figure in Advanced.'},
   {h:'Swing %',f:r=>r.fm?f(r.fm.cv,1)+'%':'—',c:'num',k:r=>r.fm?r.fm.cv:null,
    t:'Week σ as a percentage of the team\u2019s own average, so a high scorer and a low scorer can be compared fairly.'},
   {h:'SoS',f:r=>r.fm?f(r.fm.sos,1):'—',c:'num',k:r=>r.fm?r.fm.sos:null,
    t:'Strength of schedule: the average season PPG of the opponents actually faced.'},
   {h:'vs neutral',f:r=>r.fm?(r.fm.sos-r.fm.sosBase>=0?'+':'')+(r.fm.sos-r.fm.sosBase).toFixed(2):'—',
    c:'num',k:r=>r.fm?r.fm.sos-r.fm.sosBase:null,
    t:'How much harder or easier than a perfectly balanced schedule — facing every other team once. Positive means a tougher road than anyone else got.'},
   {h:'',f:r=>r.fm?dbar(r.fm.sos-r.fm.sosBase,3,pol(r.fm.sos-r.fm.sosBase)):'',k:r=>r.fm?r.fm.sos-r.fm.sosBase:null},
  ],ap,{rank:1,sort:4});}
  drawAP(); push(drawAP);

  /* projections */
  function drawProj(){table($('#tProj'),[
   {h:'Team',f:r=>esc(r.t),c:'nm',k:r=>r.t,asc:1},
   {h:'Manager',f:r=>mlink(r.m),k:r=>r.m,asc:1},
   {h:'Actual',f:r=>f(r.pts),c:'num',k:r=>r.pts},
   {h:'Projected',f:r=>f(r.proj),c:'num',k:r=>r.proj},
   {h:'Diff',f:r=>f(r.diff),c:'num',k:r=>r.diff},
   {h:'Per week',f:r=>f(r.per),c:'num',k:r=>r.per},
   {h:'',f:r=>dbar(r.per,9,pol(r.per)),k:r=>r.per},
  ],ap,{rank:1,sort:5});}
  drawProj(); push(drawProj);

  /* rivalries */
  function drawRiv(){table($('#tRiv'),[
   {h:'Matchup',f:r=>`${mlink(r.a)} <span class="dim">vs</span> ${mlink(r.b)}`,c:'nm',k:r=>r.score},
   {h:'Meetings',f:r=>r.g,c:'num',k:r=>r.g},
   {h:'Record',f:r=>`<span class="mono">${r.aw}–${r.bw}</span>`,c:'num',k:r=>Math.abs(r.aw-r.bw),asc:1},
   {h:'Avg margin',f:r=>f(r.marg),c:'num',k:r=>r.marg,asc:1},
   {h:'Rivalry score',f:r=>f(r.score,1),c:'num',k:r=>r.score,t:'meetings × balance × closeness'},
   {h:'',f:r=>dbar(r.score-6,7,'var(--brass)'),k:r=>r.score},
  ],K5.rivals,{rank:1,sort:4});}
  drawRiv(); push(drawRiv);
  const top=K5.rivals[0];
  $('#rivPick').innerHTML=`<b>${esc(top.a)}</b> vs <b>${esc(top.b)}</b>: ${top.g} meeting${top.g>1?'s':''}, split ${top.aw}–${top.bw}, decided by an average of <b>${top.marg.toFixed(2)}</b> points. That is the rivalry-week fixture on the numbers.`;

  /* weekly scoreboard */
  const wsel=$('#wkSel');
  const allWk=[...new Set(K5.games.map(g=>g.wk))].sort((a,b)=>a-b);
  wsel.innerHTML=allWk.map(w=>`<button data-w="${w}"${w===WKS[0]?' class="on"':''}>${w}</button>`).join('');
  function drawWk(w){
    $$('#wkSel button').forEach(b=>b.classList.toggle('on',+b.dataset.w===w));
    const gs=K5.games.filter(g=>g.wk===w), by=K5.byes.filter(b=>b.wk===w);
    const all=gs.flatMap(g=>[{t:g.ta,p:g.aa},{t:g.tb,p:g.ab}]).concat(by.map(b=>({t:b.t,p:b.a})));
    const hi=Math.max(...all.map(x=>x.p)), lo=Math.min(...all.map(x=>x.p));
    $('#wkOut').innerHTML=`<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,310px),1fr));gap:12px">${
      gs.map(g=>{const vd=isVoid(YR,g.wk,g.ta,g.tb), aw=g.aa>g.ab;
        const s=(t,p,pr,win)=>`<div class="side ${vd?'':(win?'w':'lo')}"><span class="tn">${esc(t)}<small>${esc(MG[t])} · proj ${pr.toFixed(1)}</small></span>
          <span class="sc">${p.toFixed(2)}</span>${p===hi?'<span class="chip y" style="margin-left:6px">high</span>':p===lo?'<span class="chip" style="margin-left:6px;border-color:var(--neg);color:var(--neg)">low</span>':''}</div>`;
        return `<div class="game${vd?' void':''}"><div class="gh"><button data-receipt="${YR}|${g.wk}|${esc(g.ta)}" title="Make a shareable card of this result" aria-label="Make a shareable card of this result" style="float:right;background:none;border:0;box-shadow:none;color:var(--brass);font-family:inherit;font-size:inherit;letter-spacing:inherit;text-transform:inherit;cursor:pointer;padding:0 2px;margin:0 -2px 0 8px;min-height:0">&#8593; Share</button>${vd?(roundName(YR,K5,g)||'Week '+w)+' — VOID':(roundName(YR,K5,g)||'Week '+w)+' · margin '+Math.abs(g.aa-g.ab).toFixed(2)}</div>${s(g.ta,g.aa,g.pa,aw)}${s(g.tb,g.ab,g.pb,!aw)}</div>`;}).join('')
      + by.map(b=>`<div class="game"><div class="gh">${byeName(K5,b)}</div><div class="side bye"><span class="tn">${esc(b.t)}<small>${esc(MG[b.t])} · proj ${b.p.toFixed(1)}</small></span><span class="sc">${b.a.toFixed(2)}</span></div></div>`).join('')}</div>`;
  }
  $$('#wkSel button').forEach(b=>b.onclick=()=>drawWk(+b.dataset.w));
  drawWk(WKS[0]); push(()=>{const on=$$('#wkSel button.on')[0]; if(on)drawWk(+on.dataset.w);});

  /* trades */
  function drawTrades(){
  /* the source list is newest-first; a season reads better in the order it happened */
  const TMON={Jan:0,Feb:1,Mar:2,Apr:3,May:4,Jun:5,Jul:6,Aug:7,Sep:8,Oct:9,Nov:10,Dec:11};
  const tdate=t=>{const m=/^([A-Za-z]{3})\s+(\d+)/.exec(t.d||'');
    return m?(TMON[m[1]]||0)*100+ +m[2]:0;};
  const TR=K5.trades.slice().sort((a,b)=>tdate(a)-tdate(b));
  $('#trades').innerHTML=TR.map(t=>`<div class="card" style="margin-top:0">
    <div class="card-h"><h3>${esc(t.ta)} &harr; ${esc(t.tb)}</h3><span class="sub">${esc(t.d)}</span>
      <div class="right sub">${esc(MG[t.ta]||'')} &harr; ${esc(MG[t.tb]||'')}</div></div>
    <div class="card-b" style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px">
      <div><div class="sub-h" style="margin:0 0 6px">&rarr; ${esc(t.ta)}</div>${t.pa.map(p=>`<div style="font-size:13px">${esc(p)}</div>`).join('')}</div>
      <div><div class="sub-h" style="margin:0 0 6px">&rarr; ${esc(t.tb)}</div>${t.pb.map(p=>`<div style="font-size:13px">${esc(p)}</div>`).join('')}</div>
    </div></div>`).join('');
  const cnt={}; K5.trades.forEach(t=>{cnt[t.ta]=(cnt[t.ta]||0)+1;cnt[t.tb]=(cnt[t.tb]||0)+1;});
  
  $('#tradeStat').innerHTML=Object.entries(cnt).sort((a,b)=>b[1]-a[1])
    .map(([t,c])=>`<div class="tile"><b>${c}</b><span>${esc(t)}</span></div>`).join('');
  $('#trSub').textContent=`${YR} season · ${K5.trades.length} deal${K5.trades.length===1?'':'s'}`;}
  drawTrades(); push(drawTrades);
  $('#apSub').textContent=`${YR} · ${WKS.length} weeks × ${T.length-1} opponents = ${WKS.length*(T.length-1)} games`;
}
$$('#wkYears button[data-wy]').forEach(b=>b.onclick=()=>drawWeekly(+b.dataset.wy));
drawWeekly(WKYEARS[WKYEARS.length-1]);
REDRAW.push(()=>{});

$('#spotClear').onclick=()=>{PICK.clear();spotlight();};
syncFilter();

/* ============ method ============ */
(function(){
  const R=[
  ['SCORING'],
  ['PPG / PPGA','Points per game scored and allowed.','<code>PF ÷ games</code>. Season length varies — 13 games in 2017, 15 in 2021, 14 elsewhere — so raw PF is never used for cross-era rate or quality comparisons. It appears only in the Record Book, under a clearly labelled counting-record heading where the game count is shown alongside it.'],
  ['Power Index','Scoring strength, era-proofed.','<code>100 × (PPG ÷ that season\'s league-average PPG)</code>. 100 is average, 112 is 12% above the field. League scoring rose about 12% across the decade, which is why this and not PF is the headline number.'],
  ['Z-score','How far above the field, in that league\'s own units of spread.','<code>(PPG − league avg) ÷ population SD of PPG</code> that season. Rewards dominating a tight league. Above +1.5 is genuinely dominant.'],
  ['LUCK'],
  ['Pythagorean win %','The record your points deserved.','<code>PF^k ÷ (PF^k + PA^k)</code>, k = 2.37, the standard fantasy exponent.'],
  ['Luck','Wins you did not earn, or were robbed of.','<code>(Wins + &frac12; ties) − Pythagorean wins</code>. Positive means you won more than your scoring justified. Over one season it is noise; over ten it is a pattern.'],
  ['All-play record','The luck-free record.','Every week, count how many of the other teams you outscored — <code>weeks × opponents</code> games a season, so 126 in a 14-week year and 135 in the 15-week 2021 season. Exact ties count as neither a win nor a loss, so three team-seasons show one game fewer: 2022 week 3, and 2023 weeks 5 and 8. This removes the schedule entirely — it is what your scoring alone was worth. Computed for every season with a loaded game log.'],
  ['All-play luck','The sharpest luck measure available.','<code>Real wins − (all-play win % × weeks played)</code> — 14 in most seasons, 15 in 2021, 13 in 2017. Unlike Pythagorean it needs no model at all, just the weekly scores.'],
  ['CAREER'],
  ['Career power index','Career scoring strength.','Games-weighted mean of season power indexes, so a long career outweighs one hot year.'],
  ['Std dev','Steady or streaky.','Population standard deviation of a manager\'s season power indexes. Low is a metronome, high is boom-or-bust.'],
  ['Form / trend','Better or worse than their own history.','Form is mean power index over 2023–2025. Trend is form minus career index.'],
  ['Expected titles','A neutral baseline for rings.','<code>Σ (½)^(games needed to win)</code> across playoff appearances. A coin flip every round, so a 4-team bracket gives every qualifier 0.25 — but in a 6-team bracket the top two seeds skip a round and are worth 0.25 while seeds 3–6 are worth 0.125. It still sums to exactly 1.00 per season, so it stays neutral while pricing the bye that a top seed actually earned.'],
  ['Title share','Championships, honestly counted.','1.0 for an outright title, 0.5 each for the two 2022 co-champions.'],
  ['POWER RANKINGS'],
  ['Power score','Forward-looking strength, not a career résumé.','Season weight <code>λ^(2025 − year)</code> applied to games played; weighted mean power index shrunk toward 100 by <code>N ÷ (N + 25)</code> where N is weighted games. Uses scoring only — record carries luck, scoring does not.'],
  ['Projected win rate','What the score implies.','<code>score^k ÷ (score^k + 100^k)</code> against a league-average opponent, same exponent as everywhere else.'],
  ['Outlook','Regression flag.','Built from last season\'s luck. A manager whose record beat their scoring is flagged to fall; one whose scoring beat their record is flagged to bounce. Regression to the mean is the most reliable prediction in fantasy.'],
  ['WEEK-BY-WEEK SEASONS'],
  ['Points vs projection','Did you beat the number.','Season actual points minus the sum of weekly projections. Captures start/sit calls and waiver hits that the projection did not see — plus a large amount of noise. Read it in points per week, not totals.'],
  ['Rivalry score','Which fixture deserves a rivalry week.','<code>meetings × balance × closeness</code>, where balance is <code>1 − |W−L| ÷ meetings</code> and closeness is <code>100 ÷ (10 + average margin)</code>. Rewards fixtures that are frequent, even, and tight. Computed within the selected season.'],
  ['STILL MISSING'],
  ['Weekly data before 2021','All-play, race charts and true strength of schedule for 2015–2020.','Needs the weekly game log for those six seasons. Everything the Week by Week section does extends backwards the day each one lands.'],
  ['Trades before 2021','Trade trees, who fleeces whom, player value flow.','2021–2025 transaction logs are loaded; 2015–2020 are not. Grading a trade by what the pieces scored afterwards also needs per-player weekly scoring, which no screenshot has carried yet.'],
  ];
  $('#methodBody').innerHTML=R.map(r=>r.length===1?`<div class="mgroup">${r[0]}</div>`:
    `<div class="mrow"><div class="k">${r[0]}</div><div class="d">${r[1]}</div><div class="r">${r[2]}</div></div>`).join('');
})();
/* ============ trade market ============ */
(function(){
  const TR=D.trade; if(!TR||!TR.mgr.length)return;
  const key=(a,b)=>[a,b].sort().join('|');
  const PAIR={}; TR.pairs.forEach(p=>{PAIR[key(p.a,p.b)]=p.n;});
  const total=TR.log.length;
  $('#trLedSub').textContent=`${total} deals · ${TR.years[0]}–${TR.years[TR.years.length-1]}`;
  function drawLedger(){
    table($('#tTrLed'),[
     {h:'Manager',f:r=>mlink(r.name),c:'nm',k:r=>r.name,asc:1},
     {h:'Szns',f:r=>r.seasons,c:'num',k:r=>r.seasons,t:'Seasons this manager played inside the logged window'},
     {h:'Trades',f:r=>r.trades,c:'num',k:r=>r.trades},
     {h:'',f:r=>dbar(r.trades-6,10,'var(--brass)'),k:r=>r.trades},
     {h:'Per season',f:r=>r.per.toFixed(2),c:'num',k:r=>r.per},
     {h:'Partners',f:r=>r.partners,c:'num',k:r=>r.partners,t:'Distinct managers they have made at least one deal with'},
     {h:'Players in',f:r=>r.pin,c:'num',k:r=>r.pin},
     {h:'Players out',f:r=>r.pout,c:'num',k:r=>r.pout},
     {h:'Net',f:r=>(r.pin-r.pout>=0?'+':'')+(r.pin-r.pout),c:'num',k:r=>r.pin-r.pout,t:'Players received minus players sent. Positive = consolidates, negative = spreads talent out.'},
     {h:'Busiest',f:r=>r.busyY?`${r.busyY} <span class="dim">(${r.busyN})</span>`:'—',c:'num',k:r=>r.busyN},
    ],TR.mgr.filter(r=>vis(r.name)),{rank:1,sort:2});
  }
  drawLedger(); REDRAW.push(drawLedger);

  function drawMtx2(){
    const MXP=Math.max(1,...TR.pairs.map(p=>p.n));
    const ord=TR.mgr.filter(m=>vis(m.name)).map(m=>m.name)
      .sort((a,b)=>(byName[b]?byName[b].seasons:0)-(byName[a]?byName[a].seasons:0)||a.localeCompare(b));
    let h='<thead><tr><th class="rw"></th>'+ord.map(n=>`<th class="v">${esc(n)}</th>`).join('')+'<th class="v">TOTAL</th></tr></thead><tbody>';
    ord.forEach(a=>{h+=`<tr><th class="rw">${mlink(a)}</th>`;let tot=0;
      ord.forEach(b=>{
        if(a===b){h+='<td class="self"><span>—</span></td>';return;}
        const n=PAIR[key(a,b)]||0; if(!n){h+='<td><span></span></td>';return;}
        tot+=n;
        const t=Math.min(1,n/MXP), bg=mix(cssv('--surface'),cssv('--brass'),Math.pow(t,.7)*.85);
        h+=`<td data-a="${esc(a)}" data-b="${esc(b)}"><span style="background:${bg};color:${pickInk(bg)}">${n}</span></td>`;});
      h+=`<td><span style="font-weight:600">${tot||''}</span></td></tr>`;});
    $('#tTrMtx').innerHTML=h+'</tbody>';
    $$('#tTrMtx td[data-a]').forEach(td=>{
      const a=td.dataset.a,b=td.dataset.b;
      const ds=TR.log.filter(x=>(x.ma===a&&x.mb===b)||(x.ma===b&&x.mb===a)).sort((x,y)=>x.y-y.y);
      bindTip(td,`<b>${esc(a)} &harr; ${esc(b)}</b><br>${ds.length} deal${ds.length===1?'':'s'}<br><br>`+
        ds.map(x=>`<b>${x.y}</b> ${esc(x.d)}<br>&rarr; ${esc(x.ta)}: ${x.pa.map(esc).join(', ')}<br>&rarr; ${esc(x.tb)}: ${x.pb.map(esc).join(', ')}`).join('<br><br>'));});
    const top=TR.pairs.filter(p=>vis(p.a)&&vis(p.b)).slice(0,8);
    $('#trPairs').innerHTML=top.map(p=>`<div class="tile"><b>${p.n}</b><span>${esc(p.a.split(' ').slice(-1)[0])} &harr; ${esc(p.b.split(' ').slice(-1)[0])}</span></div>`).join('');
  }
  drawMtx2(); REDRAW.push(drawMtx2);

  function drawTrYr(){
    const ord=TR.mgr.filter(m=>vis(m.name)).map(m=>m.name)
      .sort((a,b)=>(byName[b]?byName[b].seasons:0)-(byName[a]?byName[a].seasons:0)||a.localeCompare(b));
    const cell=(m,y)=>(TR.byYear[y]||{})[m]||0;
    const MXY=Math.max(1,...ord.flatMap(m=>TR.years.map(y=>cell(m,y))));
    const played={}; ROWS.forEach(r=>{played[r.mgr+'|'+r.y]=1;});
    let h='<thead><tr><th class="rw"></th>'+TR.years.map(y=>`<th class="v">${y}</th>`).join('')+'<th class="v">TOTAL</th></tr></thead><tbody>';
    ord.forEach(m=>{h+=`<tr><th class="rw">${mlink(m)}</th>`;let tot=0;
      TR.years.forEach(y=>{
        if(!played[m+'|'+y]){h+='<td class="self"><span>&middot;</span></td>';return;}
        const n=cell(m,y); tot+=n;
        if(!n){h+='<td><span style="color:var(--ink-2)">0</span></td>';return;}
        const t=Math.min(1,n/MXY);
        const bg3=mix(cssv('--surface'),cssv('--brass'),Math.pow(t,.7)*.85);
        h+=`<td data-m="${esc(m)}" data-y="${y}"><span style="background:${bg3};color:${pickInk(bg3)}">${n}</span></td>`;});
      h+=`<td><span style="font-weight:600">${tot||''}</span></td></tr>`;});
    $('#tTrYr').innerHTML=h+'</tbody>';
    $$('#tTrYr td[data-m]').forEach(td=>{
      const m=td.dataset.m, y=+td.dataset.y;
      const ds=TR.log.filter(x=>x.y===y&&(x.ma===m||x.mb===m));
      bindTip(td,`<b>${esc(m)} &middot; ${y}</b><br>${ds.length} deal${ds.length===1?'':'s'}<br><br>`+
        ds.map(x=>{const other=x.ma===m?x.mb:x.ma, got=x.ma===m?x.pa:x.pb, gave=x.ma===m?x.pb:x.pa;
          return `<b>${esc(x.d)}</b> with ${esc(other)}<br>in: ${got.map(esc).join(', ')}<br>out: ${gave.map(esc).join(', ')}`;}).join('<br><br>'));});
  }
  drawTrYr(); REDRAW.push(drawTrYr);

  const yr=TR.years.map(y=>({y,n:Object.values(TR.byYear[y]||{}).reduce((a,b)=>a+b,0)/2}));
  const mx=Math.max(...yr.map(v=>v.n),1);
  $('#trYears').innerHTML=`<div style="display:flex;flex-direction:column;gap:8px">`+yr.map(v=>
    `<div style="display:flex;align-items:center;gap:10px">
       <span class="mono" style="width:46px;color:var(--ink-2);font-size:12.5px">${v.y}</span>
       <span style="flex:1;height:16px;background:var(--rule-2);border-radius:2px;overflow:hidden">
         <span style="display:block;height:100%;width:${(v.n/mx*100).toFixed(1)}%;background:var(--brass)"></span></span>
       <span class="mono" style="width:34px;text-align:right;font-size:12.5px">${v.n}</span></div>`).join('')+'</div>';
})();

/* ============ season stories — one headline per year, all derived ============ */
const STORY=(function(){
  const rows=D.rows, gm=D.games.filter(g=>!g.void);
  const seedOf={}; rows.forEach(r=>seedOf[r.y+'|'+r.team]=r.seed);
  const S=n=>n.toFixed(2), one=n=>n.toFixed(1);
  const RW={'Final':10,'Semifinal':6,'Quarterfinal':4,'3rd Place Game':0,'5th Place Game':0};
  const ALL={};
  D.seasons.forEach(y=>{
    const rs=rows.filter(r=>r.y===y), gs=gm.filter(g=>g.y===y);
    const ch=D.champs.find(c=>c.y===y);
    const cands=[];
    const push=(sc,k,v,n)=>cands.push({sc,k,v,n});

    /* a split title outranks everything else that happened that year */
    if(ch&&ch.co)push(100,'The title nobody won',ch.mgrs.join(' & '),
      `The final fell in the week the NFL cancelled a game. It was never played to a result, so the title was split and the winnings with it. ${ch.mgrs[0]} had come through as the ${ord(rs.find(r=>r.team===ch.teams[0]).seed)} seed.`);

    /* the biggest playoff upset by seed gap */
    let up=null;
    gs.forEach(g=>{const aw=g.pa>g.pb, wT=aw?g.ta:g.tb, lT=aw?g.tb:g.ta;
      const ws=seedOf[y+'|'+wT], ls=seedOf[y+'|'+lT]; if(ws==null||ls==null)return;
      const gap=ws-ls; if(gap<=0)return;
      const c={g,gap,w:aw?g.ma:g.mb,l:aw?g.mb:g.ma,ws,ls,pw:Math.max(g.pa,g.pb),pl:Math.min(g.pa,g.pb),rw:RW[g.rnd]||0};
      if(!up||gap>up.gap||(gap===up.gap&&c.rw>up.rw))up=c;});
    if(up&&up.gap>=2&&up.rw>0)push(40+up.gap*6+up.rw,'Upset of the year',`${up.w} over ${up.l}`,
      `The <b>${ord(up.ws)} seed</b> put out the <b>${ord(up.ls)}</b> in the ${up.g.rnd.toLowerCase()}, ${S(up.pw)}&ndash;${S(up.pl)}.`);

    /* a champion who had no business being there — and the opposite */
    if(ch&&!ch.co){const cr=rs.find(r=>r.team===ch.teams[0]);
      if(cr&&cr.seed>cr.spots/2)push(30+cr.seed*8,
        cr.seed===cr.spots?'In by the skin of their teeth':'Won it from the back half',ch.mgrs[0],
        `Went <b>${cr.w}-${cr.l}${cr.t?'-'+cr.t:''}</b>, made the ${cr.spots}-team bracket as the <b>${ord(cr.seed)} seed</b>, and won the whole thing.`);
      const topPI=rs.reduce((a,b)=>b.pi>a.pi?b:a);
      if(cr&&cr.seed===1&&topPI.team===cr.team)push(46,'Wire to wire',ch.mgrs[0],
        `Top seed, top scorer, champion. Led the league at <b>${one(cr.pi)}</b> power index and never gave the bracket a chance to argue.`);}

    /* the best team of the year, watching someone else lift it */
    const bestNo=rs.filter(r=>r.place!==1).reduce((a,b)=>(!a||b.pi>a.pi)?b:a,null);
    const champR=ch?rs.find(r=>r.team===ch.teams[0]):null;
    if(bestNo&&champR&&bestNo.pi-champR.pi>=6)push(24+(bestNo.pi-champR.pi),'Best team, no title',bestNo.mgr,
      `Led the league at <b>${one(bestNo.pi)}</b> power index &mdash; ${one(bestNo.pi-champR.pi)} clear of the team that actually won it &mdash; and finished ${ord(bestNo.place)}.`);

    /* the luck extremes */
    const lk=rs.reduce((a,b)=>b.luck>a.luck?b:a), ul=rs.reduce((a,b)=>b.luck<a.luck?b:a);
    if(lk.luck>=2.5)push(38+lk.luck*6,'Wins nobody earned',lk.mgr,
      `Won <b>${lk.w}</b> games on scoring worth about ${one(lk.pythW)} &mdash; ${S(lk.luck)} wins of pure schedule${lk.place===1?', and a title to go with them':''}.`);
    if(ul.luck<=-2.5)push(38+(-ul.luck)*6,'Robbed',ul.mgr,
      `${ul.pf>ul.pa?`Outscored the league by <b>${S(ul.pf-ul.pa)}</b> points`:`Scored ${S(ul.pf)}`} and still went <b>${ul.w}-${ul.l}</b>, finishing ${ord(ul.place)} of ${ul.teams}.`);

    /* a season of scoring nobody else was close to */
    const hi=rs.reduce((a,b)=>b.pi>a.pi?b:a), lo=rs.reduce((a,b)=>b.pi<a.pi?b:a);
    const second=rs.filter(r=>r!==hi).reduce((a,b)=>b.pi>a.pi?b:a);
    if(hi.pi>=115)push(30+(hi.pi-100),'Scoring machine',hi.mgr,
      `<b>${one(hi.pi)}</b> power index &mdash; ${one(hi.pi-100)}% clear of the field, and ${one(hi.pi-second.pi)} clear of the next best team. Finished ${ord(hi.place)}.`);
    if(lo.pi<=85)push(28+(100-lo.pi),'The floor',lo.mgr,
      `<b>${one(lo.pi)}</b> power index, ${S(lo.ppg)} a game in a league averaging ${S(lo.lg)}. Went ${lo.w}-${lo.l}${lo.t?'-'+lo.t:''}.`);

    /* a final that came down to nothing */
    const fin=gs.find(g=>g.rnd==='Final');
    if(fin){const mg=Math.abs(fin.pa-fin.pb);
      if(mg<=12)push(44+(14-mg),'Decided by nothing',`${fin.pa>fin.pb?fin.ma:fin.mb} by ${S(mg)}`,
        `The ${y} final went ${S(Math.max(fin.pa,fin.pb))}&ndash;${S(Math.min(fin.pa,fin.pb))}. ${fin.pa>fin.pb?fin.mb:fin.ma} came that close.`);}

    /* the biggest gap between where you started and where you ended */
    const sw=rs.filter(r=>r.sf!=null).reduce((a,b)=>(b.sf>(a?a.sf:-99)?b:a),null);
    if(sw&&sw.sf>=3)push(26+sw.sf*4,'Rose from the pack',sw.mgr,
      `In as the ${ord(sw.seed)} seed, out in ${ord(sw.place)} &mdash; a ${sw.sf}-place climb once the bracket started.`);

    /* every season gets something, even a quiet one */
    if(!cands.length&&ch)push(1,'Champion',ch.mgrs.join(' & '),
      `${ch.teams.join(' / ')} took the ${ch.spots}-team bracket in a ${rs.length}-team league.`);
    ALL[y]={cands,champ:ch?ch.mgrs.join(' & '):''};
  });
  /* ten seasons should read as ten different stories — once an angle is used,
     it has to be clearly better than the alternatives to be used again */
  const out={}, used={};
  const adj=c=>c.sc-26*(used[c.k]||0);
  const best=y=>ALL[y].cands.reduce((a,b)=>adj(b)>adj(a)?b:a);
  [...D.seasons].sort((a,b)=>best(b).sc-best(a).sc).forEach(y=>{
    const w=best(y); used[w.k]=(used[w.k]||0)+1;
    out[y]={y,...w,champ:ALL[y].champ};});
  return out;
})();
function openStories(){
  RETFOCUS=document.activeElement;
  $('#mTitle').textContent='The story of each season';
  $('#mSub').textContent=`${D.seasons.length} seasons · one headline apiece · every word derived from the record`;
  $('#mBody').innerHTML=`<div class="hl">`+D.seasons.map(y=>{const st=STORY[y];
    return `<button class="hlc" data-goy="${y}">
      <span class="fig">${y}</span>
      <span class="k">${esc(st.k)}</span>
      <span class="v">${esc(st.v)}</span>
      <span class="n">${st.n}</span>
      ${st.champ?`<span class="n" style="margin-top:7px;padding-top:7px;border-top:1px solid var(--rule-2);color:var(--ink-3);font-size:11.5px">Champion: ${esc(st.champ)}</span>`:''}
    </button>`;}).join('')+`</div>`;
  $$('#mBody .hlc').forEach(b=>b.onclick=()=>{const y=+b.dataset.goy;closeMgr();jumpSeason(y);});
  ov.classList.add('on'); document.body.style.overflow='hidden'; $('#mX').focus();
}
$('#storiesBtn').onclick=openStories;
function jumpSeason(y){
  drawSeason(y);
  const el=$('#seasons'); if(el)el.scrollIntoView({behavior:'smooth'});
}


/* ============ the second secret: type it and he rises ============ */
const MASK=`<svg viewBox="0 0 420 640" aria-hidden="true">
  <defs>
    <linearGradient id="pAu" x1=".14" y1="0" x2=".9" y2="1">
      <stop offset="0" stop-color="#FFF3C6"/><stop offset=".18" stop-color="#F3CB5A"/>
      <stop offset=".48" stop-color="#CE9B31"/><stop offset=".76" stop-color="#8E611A"/>
      <stop offset="1" stop-color="#5E3D0E"/></linearGradient>
    <linearGradient id="pAuF" x1=".3" y1="0" x2=".8" y2="1">
      <stop offset="0" stop-color="#FFE59A"/><stop offset=".42" stop-color="#E0AE3C"/>
      <stop offset="1" stop-color="#8A5C16"/></linearGradient>
    <linearGradient id="pLap" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2E52C9"/><stop offset=".5" stop-color="#1B348C"/>
      <stop offset="1" stop-color="#0E1E5B"/></linearGradient>
    <radialGradient id="pCheek" cx=".5" cy=".38" r=".62">
      <stop offset="0" stop-color="#FFE9A0" stop-opacity=".55"/><stop offset="1" stop-color="#000" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="pShade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#000" stop-opacity=".42"/><stop offset=".34" stop-color="#000" stop-opacity="0"/>
      <stop offset=".7" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/>
    </linearGradient>
    <radialGradient id="pEye" cx=".4" cy=".34" r=".8">
      <stop offset="0" stop-color="#FFC46A"/><stop offset=".45" stop-color="#FF7A18"/>
      <stop offset="1" stop-color="#7C2A02"/></radialGradient>
    <filter id="pSoft"><feGaussianBlur stdDeviation="2.4"/></filter>
    <filter id="pGrain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3"/>
      <feColorMatrix type="saturate" values="0"/>
      <feComponentTransfer><feFuncA type="linear" slope=".14"/></feComponentTransfer>
      <feComposite in2="SourceGraphic" operator="in"/></filter>
    <clipPath id="pHeadClip"><path d="M210 96 c56 0 88 40 88 96 c0 62-34 118-88 118 c-54 0-88-56-88-118 c0-56 32-96 88-96z"/></clipPath>
    <clipPath id="pNemesClip"><path d="M210 40 c88 0 132 58 132 132 l0 300 -66 22 -18-190 c-14 26-30 40-48 40 c-18 0-34-14-48-40 l-18 190 -66-22 0-300 c0-74 44-132 132-132z"/></clipPath>
  </defs>

  <!-- ===== nemes headdress ===== -->
  <path d="M210 40 c88 0 132 58 132 132 l0 300 -66 22 -18-190 c-14 26-30 40-48 40 c-18 0-34-14-48-40 l-18 190 -66-22 0-300 c0-74 44-132 132-132z" fill="url(#pAu)"/>
  <g clip-path="url(#pNemesClip)">
    <g fill="url(#pLap)">
      <path d="M78 150 h60 l-4 26 h-56z"/><path d="M282 150 h60 l0 26 h-56z"/>
      <path d="M74 196 h62 l-3 26 h-59z"/><path d="M284 196 h58 l0 26 h-55z"/>
      <path d="M72 242 h63 l-2 26 h-61z"/><path d="M285 242 h57 l0 26 h-55z"/>
      <path d="M70 288 h64 l-2 26 h-62z"/><path d="M286 288 h56 l0 26 h-54z"/>
      <path d="M70 334 h64 l-2 26 h-62z"/><path d="M286 334 h56 l0 26 h-54z"/>
      <path d="M70 380 h64 l-2 26 h-62z"/><path d="M286 380 h56 l0 26 h-54z"/>
      <path d="M70 426 h64 l-2 26 h-62z"/><path d="M286 426 h56 l0 26 h-54z"/>
    </g>
    <path d="M70 128 h280 v34 h-280z" fill="url(#pLap)"/>
    <path d="M70 122 h280 v9 h-280z" fill="#F3CB5A"/>
    <path d="M70 160 h280 v9 h-280z" fill="#F3CB5A"/>
    <rect x="0" y="0" width="420" height="640" fill="url(#pShade)"/>
    <rect x="0" y="0" width="420" height="640" filter="url(#pGrain)" fill="#fff" opacity=".5"/>
  </g>

  <!-- ===== face ===== -->
  <path d="M210 96 c56 0 88 40 88 96 c0 62-34 118-88 118 c-54 0-88-56-88-118 c0-56 32-96 88-96z" fill="url(#pAuF)"/>
  <g clip-path="url(#pHeadClip)">
    <ellipse cx="196" cy="180" rx="120" ry="110" fill="url(#pCheek)"/>
    <path d="M298 96 c0 130-20 210-52 240 h72 v-240z" fill="#000" opacity=".2"/>
    <rect x="0" y="0" width="420" height="640" filter="url(#pGrain)" fill="#fff" opacity=".55"/>
  </g>

  <!-- ===== uraeus: the cobra ===== -->
  <g>
    <path d="M210 92 c-16 0-27 12-27 26 c0 10 6 17 14 21 c-9 8-14 18-14 28 h54 c0-10-5-20-14-28 c8-4 14-11 14-21 c0-14-11-26-27-26z" fill="url(#pAu)"/>
    <path d="M210 104 c-9 0-15 7-15 14 c0 6 4 11 9 13 h12 c5-2 9-7 9-13 c0-7-6-14-15-14z" fill="#1B348C"/>
    <circle cx="202" cy="115" r="3.4" fill="#FF7A18"/><circle cx="218" cy="115" r="3.4" fill="#FF7A18"/>
    <path d="M204 138 h12 l-3 14 h-6z" fill="#B23018"/>
    <path d="M186 70 c10-16 38-16 48 0 c-12-8-36-8-48 0z" fill="#C9962E" opacity=".9"/>
  </g>

  <!-- ===== brows, driven down ===== -->
  <g fill="#0B1740">
    <path d="M148 172 q30-10 58 12 l-4 14 q-26-18-52-12z"/>
    <path d="M272 172 q-30-10-58 12 l4 14 q26-18 52-12z"/>
  </g>

  <!-- ===== eyes ===== -->
  <g>
    <path d="M150 208 q28-24 56-4 q-28 20-56 4z" fill="#0D0803"/>
    <path d="M270 208 q-28-24-56-4 q28 20 56 4z" fill="#0D0803"/>
    <path d="M157 207 q22-17 42-3 q-22 13-42 3z" fill="url(#pEye)"/>
    <path d="M263 207 q-22-17-42-3 q22 13 42 3z" fill="url(#pEye)"/>
    <ellipse cx="178" cy="205" rx="5" ry="9" fill="#0A0603"/>
    <ellipse cx="242" cy="205" rx="5" ry="9" fill="#0A0603"/>
    <circle cx="176" cy="201" r="1.8" fill="#FFE9A8" opacity=".9"/>
    <circle cx="240" cy="201" r="1.8" fill="#FFE9A8" opacity=".9"/>
    <g stroke="#0B1740" stroke-width="7" fill="none" stroke-linecap="round">
      <path d="M150 206 l-26-12"/><path d="M270 206 l26-12"/>
      <path d="M168 228 l-9 24"/><path d="M252 228 l9 24"/>
    </g>
    <g filter="url(#pSoft)" opacity=".55">
      <ellipse cx="188" cy="206" rx="26" ry="10" fill="#FF7A18"/>
      <ellipse cx="232" cy="206" rx="26" ry="10" fill="#FF7A18"/>
    </g>
  </g>

  <!-- ===== nose and mouth ===== -->
  <path d="M210 214 l-12 50 q12 8 24 0 z" fill="#8A5C16" opacity=".55"/>
  <path d="M198 264 q12 6 24 0" stroke="#6B4410" stroke-width="2.5" fill="none" opacity=".6"/>
  <path d="M178 292 q32-9 64 0 q-32 13-64 0z" fill="#2E1C05"/>
  <path d="M178 292 q32-9 64 0" stroke="#5E3D0E" stroke-width="2" fill="none"/>

  <!-- ===== false beard, braided ===== -->
  <path d="M192 322 h36 l7 92 q-25 12-50 0z" fill="url(#pAu)"/>
  <g stroke="#7A5112" stroke-width="2.4" opacity=".7">
    <path d="M193 342 h34"/><path d="M195 364 h32"/><path d="M197 386 h30"/><path d="M199 406 h27"/>
  </g>
  <path d="M192 322 h36 l1 12 h-38z" fill="#1B348C"/>

  <!-- ===== usekh collar ===== -->
  <g>
    <path d="M126 470 q84 74 168 0 l16 44 q-100 84-200 0z" fill="url(#pAu)"/>
    <path d="M134 486 q76 64 152 0" stroke="#1B348C" stroke-width="13" fill="none"/>
    <path d="M142 504 q68 56 136 0" stroke="#0FA3A3" stroke-width="11" fill="none"/>
    <path d="M150 521 q60 48 120 0" stroke="#B23018" stroke-width="10" fill="none"/>
    <path d="M158 537 q52 40 104 0" stroke="#1B348C" stroke-width="9" fill="none"/>
    <g fill="#F3CB5A">
      <circle cx="150" cy="500" r="3.4"/><circle cx="176" cy="516" r="3.4"/><circle cx="210" cy="523" r="3.4"/>
      <circle cx="244" cy="516" r="3.4"/><circle cx="270" cy="500" r="3.4"/>
    </g>
  </g>
</svg>`;
const GLYPHS=[
  '<svg viewBox="0 0 40 60"><path d="M20 4a9 9 0 0 1 0 18a9 9 0 0 1 0-18z" fill="none" stroke="currentColor" stroke-width="4"/><path d="M20 22v34M6 32h28" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg>',
  '<svg viewBox="0 0 60 40"><path d="M4 22q26-20 46 0q-20 16-46 0z" fill="none" stroke="currentColor" stroke-width="3.4"/><circle cx="27" cy="21" r="6" fill="currentColor"/><path d="M50 24l8 6M18 30l-4 8" stroke="currentColor" stroke-width="3.4" stroke-linecap="round"/></svg>',
  '<svg viewBox="0 0 60 46"><path d="M30 4L56 42H4z" fill="none" stroke="currentColor" stroke-width="3.6" stroke-linejoin="round"/></svg>',
  '<svg viewBox="0 0 50 50"><circle cx="25" cy="25" r="11" fill="currentColor"/><g stroke="currentColor" stroke-width="3.4" stroke-linecap="round"><path d="M25 2v7M25 41v7M2 25h7M41 25h7M9 9l5 5M36 36l5 5M41 9l-5 5M14 36l-5 5"/></g></svg>'];
function pharaohSFX(){
  const c=ac(); if(!c||quiet())return;
  /* the sky opens first: a full thunderclap, not a gong */
  thunder(0);
  tone(58,5,'sine',.15,40,.02);                 /* the note the clap leaves behind */
  /* then something rises under it. The choir swells late and slowly, so it reads as
     arriving rather than being switched on. */
  choirAh(.85,7.5);
  [0,.2,.38,.58,.8,1.05,1.35,1.7].forEach((d,i)=>
    tone(660*Math.pow(1.16,i),1.8,'sine',.022,null,null,1.5+d));  /* shimmer above it */
  tone(41,6,'sine',.08,28,1.2);                 /* the floor holding it up */
}
let PH_BUSY=false;
function pharaoh(){
  if(PH_BUSY)return; PH_BUSY=true;
  const el=document.createElement('div'); el.className='pharaoh on';
  const glyphs=Array.from({length:14},(_, i)=>{
    const g=GLYPHS[i%GLYPHS.length], sz=20+Math.random()*30;
    return `<div class="ph-g" style="left:${4+Math.random()*92}%;bottom:${-6+Math.random()*24}%;
      width:${sz}px;height:${sz*1.2}px;animation-delay:${(Math.random()*2.4).toFixed(2)}s">${g}</div>`;}).join('');
  el.innerHTML=`<div class="ph-rays"></div><div class="ph-glow"></div><div class="ph-sand"></div>
    ${glyphs}<div class="ph-mask">${MASK}</div>
    <div class="ph-txt"><div class="l1">THE PHARAOH</div><div class="l2">WILL RISE AGAIN</div></div>`;
  document.body.appendChild(el);
  pharaohSFX();
  setTimeout(()=>el.classList.add('out'),6720);
  setTimeout(()=>{el.remove();PH_BUSY=false;},8280);
}
(function(){const WORDS=['commish','commissioner','berger','brian']; let buf='';
  addEventListener('keydown',e=>{
    if(e.metaKey||e.ctrlKey||e.altKey)return;
    const t=e.target; if(t&&/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))return;
    if(e.key.length!==1)return;
    buf=(buf+e.key.toLowerCase()).slice(-24);
    if(WORDS.some(w=>buf.endsWith(w))){buf=''; if(!eggOpen())pharaoh();}});})();

glossify();

</script>

"""

SHELL_TOP = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<meta name="description" content="The Deadshot fantasy football record book — ten seasons of champions, standings, power rankings, head-to-head and trades.">
<meta name="robots" content="noindex">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="theme-color" content="#8E1520">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Deadshot">
<link rel="canonical" href="https://deadshotleague.com/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Deadshot Record Book">
<meta property="og:title" content="Deadshot Record Book">
<meta property="og:description" content="Ten seasons of champions, standings, power rankings, head-to-head and trades — the whole league record book, in one place.">
<meta property="og:url" content="https://deadshotleague.com/">
<meta property="og:image" content="https://deadshotleague.com/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Deadshot Archives — ten seasons, twenty managers, 410 games logged.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Deadshot Record Book">
<meta name="twitter:description" content="Ten seasons of champions, standings, power rankings, head-to-head and trades.">
<meta name="twitter:image" content="https://deadshotleague.com/og.png">
<script>if(location.protocol==='http:'||location.protocol==='https:'){var _va=document.createElement('script');_va.defer=true;_va.src='/_vercel/insights/script.js';document.head.appendChild(_va);}</script>
<script>
/* Keeps a copy on the device so the book opens with no signal. Only over https, so
   opening index.html straight off the disk is unaffected. */
if('serviceWorker'in navigator&&(location.protocol==='https:'||location.hostname==='localhost')){
  addEventListener('load',function(){navigator.serviceWorker.register('/sw.js').catch(function(){});});
}
</script>
'''
SW = r"""/* Offline copy for the home-screen app. Written by the build, so VERSION changes
   whenever the page changes and an old store can never outlive its page.

   The page itself is fetched NETWORK FIRST. That is the whole point: a stored copy that
   is served first would leave every reader one launch behind every deploy, which is how
   a site like this quietly stops updating. The store is a fallback for no signal, and it
   is refreshed on every successful visit.

   Fonts and icons are the other way round -- they never change within a version, so they
   come from the store immediately and are only fetched once. */
const VERSION='deadshot-__VERSION__';
const CORE=['/','/manifest.webmanifest','/favicon-32.png',
            '/favicon.svg','/apple-touch-icon.png','/icon-192.png','/icon-512.png',
            '/icon-maskable-512.png'];
const FONT=/^https:\/\/fonts\.(googleapis|gstatic)\.com\//;

self.addEventListener('install',e=>{
  /* take over straight away rather than waiting for every tab to close */
  self.skipWaiting();
  e.waitUntil(caches.open(VERSION).then(c=>c.addAll(CORE).catch(()=>{})));
});

self.addEventListener('activate',e=>{
  e.waitUntil((async()=>{
    const keys=await caches.keys();
    await Promise.all(keys.filter(k=>k!==VERSION).map(k=>caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch',e=>{
  const r=e.request;
  if(r.method!=='GET')return;
  const url=new URL(r.url);
  const mine=url.origin===location.origin;

  /* the analytics beacon is Vercel's to update, not ours to freeze */
  if(mine&&url.pathname.startsWith('/_vercel/'))return;

  /* the per-theme link-preview stubs are navigations too. They must NEVER be written
     under the key '/', or a shared themed link replaces the stored book with a two-line
     redirector -- and offline that redirector points at itself. */
  if(mine&&url.pathname.startsWith('/t/')){
    e.respondWith(fetch(r).catch(async()=>(await caches.match('/'))||Response.error()));
    return;
  }

  /* The page. Network first, but with two hard rules learned the hard way:
     never store an answer that is not a healthy 200 (one tapped dead link used to
     replace the whole offline book with a 404 page, permanently), and never wait on
     the network for longer than a person will. fetch() only rejects when the network
     is properly down; one bar does not reject, it stalls, so it has to be raced. */
  if(mine&&url.pathname==='/'){
    e.respondWith((async()=>{
      const stored=caches.match('/');
      const live=fetch(r).then(async net=>{
        if(net&&net.ok&&!net.redirected&&net.type==='basic'){
          const c=await caches.open(VERSION); await c.put('/',net.clone());
        }
        return net;
      });
      /* let the fetch finish and refresh the store even if we stopped waiting for it */
      live.catch(()=>{});
      try{
        const net=await Promise.race([
          live,
          new Promise((_,rej)=>setTimeout(()=>rej(new Error('slow')),3500))
        ]);
        return net;
      }catch(err){
        return (await stored)||live;
      }
    })());
    return;
  }

  /* fonts and our own static files: from the store first, fetched once. Only a healthy
     response is kept -- a captive portal's interstitial is a 200 to fetch() but not to
     net.ok, and the font stylesheet is requested with crossorigin so it has a real
     status to check rather than being an opaque blob. */
  if(FONT.test(r.url)||mine){
    e.respondWith((async()=>{
      const hit=await caches.match(r);
      if(hit)return hit;
      try{
        const net=await fetch(r);
        if(net&&net.ok){ const c=await caches.open(VERSION); await c.put(r,net.clone()); }
        return net;
      }catch(err){ return hit||Response.error(); }
    })());
  }
});
"""

out = SHELL_TOP + HEAD + '</head>\n<body>\n' + BODY.replace('__DATA__', DATA) + JS + '\n</body>\n</html>\n'
open('index.html','w').write(out)
# A length is not a fingerprint: two builds of equal length produced a byte-identical
# sw.js, so the browser saw no change and every stored icon and font stayed pinned to the
# old build. A content hash changes whenever anything changes.
_blob = out.encode('utf-8')
open('sw.js','w').write(SW.replace('__VERSION__', _hashlib.sha1(_blob).hexdigest()[:12]))
print("bytes", len(_blob))
