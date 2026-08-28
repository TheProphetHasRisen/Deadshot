# -*- coding: utf-8 -*-
DATA=open('site_data.json').read()

HEAD = r"""<title>Deadshot Record Book</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800;900&family=Press+Start+2P&family=Fraunces:opsz,wght@9..144,600;9..144,700;9..144,900&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<style>
/* ============ SKINS ============ */
:root,:root[data-skin="scope"]{
  --ground:#080B09; --surface:#0E1411; --surface-2:#131B17;
  --ink:#DCEDE2; --ink-2:#8FA898; --ink-3:#718A79;
  --rule:#1E2E24; --rule-2:#16221B;
  --brass:#35E07A; --brass-2:#1E7A44; --brass-wash:#0D2416;
  --pos:#D9603F; --neg:#3C9FD4; --mid:#3A4A41;
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
  --shadow:0 1px 2px rgba(26,18,16,.07),0 8px 26px -14px rgba(142,21,32,.22);
  --mast-bg:#8E1520; --mast-ink:#FFFFFF; --mast-sub:#F0C9CC; --mast-kick:#F0C9CC;
  --mast-rule:#6E0F18; --mast-glow:rgba(0,0,0,.28); --mast-glow2:transparent;
  --head-ink:#1A1210; --hover:#FBF4F3; --nav-bg:rgba(255,255,255,.94); --ov:rgba(26,18,16,.62);
  --band:rgba(142,21,32,.055); --glow:rgba(142,21,32,.5);
  --rt:#FFFFFF; --rt-grid:#B8434C; --rt-ring:#6E0F18; --rt-g1:#7A1119; --rt-g2:#5C0B12;
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
  --ink:#E8E4FF; --ink-2:#A79DD6; --ink-3:#8279B0;
  --rule:#2E2159; --rule-2:#211846;
  --brass:#FF2E88; --brass-2:#A31E5C; --brass-wash:#2A0C22;
  --pos:#FF8A4C; --neg:#56C7F5; --mid:#443868;
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
  --ink:#DCD7C9; --ink-2:#9E988B; --ink-3:#7B7568;
  --rule:#2B2B30; --rule-2:#1F1F23;
  --brass:#C8A24A; --brass-2:#8E7231; --brass-wash:#1D1912;
  --pos:#C0392B; --neg:#5B8CA8; --mid:#3B3B42;
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
  --shadow:0 1px 2px rgba(0,0,0,.5),0 10px 26px -14px rgba(0,0,0,.75);
  --mast-bg:#35190F; --mast-ink:#FFFFFF; --mast-sub:#D9BCA4; --mast-kick:#FFFFFF;
  --mast-rule:#6B4028; --mast-glow:rgba(0,0,0,.5); --mast-glow2:rgba(255,255,255,.12);
  --head-ink:#FFFFFF; --hover:#552C1A; --nav-bg:rgba(53,25,15,.95); --ov:rgba(20,9,5,.84);
  --band:rgba(255,255,255,.05); --glow:rgba(255,255,255,.55);
  --rt:#FFFFFF; --rt-grid:#7A5238; --rt-ring:#2A1209; --rt-g1:#4A2614; --rt-g2:#2A1209;
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
.gl{display:inline-flex;align-items:center;justify-content:center;width:17px;height:17px;
  border-radius:50%;border:1px solid var(--brass-2);color:var(--brass);background:transparent;
  font-size:10px;font-weight:700;font-family:"IBM Plex Mono",monospace;line-height:1;
  cursor:help;vertical-align:middle;margin-left:5px;flex:none;user-select:none}
.gl:hover,.gl:focus{background:var(--brass);color:var(--surface);outline:none}
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
.mast::before{content:"";position:absolute;inset:0;
  background-image:linear-gradient(var(--mast-grid) 1px,transparent 1px),linear-gradient(90deg,var(--mast-grid) 1px,transparent 1px);
  background-size:34px 34px;opacity:.5}
.mast::after{content:"";position:absolute;inset:0;
  background:radial-gradient(120% 130% at 22% 40%,transparent 20%,var(--mast-vig) 78%)}
.mast-in{position:relative;z-index:2;display:flex;flex-wrap:wrap;align-items:center;gap:16px 32px;
  padding:26px 22px 24px;max-width:var(--max);margin:0 auto}
.scope{flex:0 0 auto;width:126px;height:126px;filter:drop-shadow(0 0 11px var(--mast-glow))}
.scope .sweep{animation:scopeSpin 5.5s linear infinite;transform-origin:60px 60px}
@keyframes scopeSpin{to{transform:rotate(360deg)}}
@media (prefers-reduced-motion:reduce){.scope .sweep{animation:none}}
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
@media(max-width:640px){.scope{width:88px;height:88px}.facts{gap:14px}.fact b{font-size:17px}}
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
table.heat td.h.e span{color:var(--ink-3);opacity:.35;cursor:default}
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
table.mtx td.self span{background:var(--rule-2);color:var(--ink-3)}
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
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,104px),1fr));gap:1px;background:var(--rule);border:1px solid var(--rule);border-radius:3px;overflow:hidden;margin-bottom:20px}
.tile{background:var(--surface);color:var(--ink);padding:11px 13px}
.tile b{display:block;font-family:Fraunces,serif;font-weight:700;font-size:22px;line-height:1.15;font-variation-settings:"opsz" 40}
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
<script>(function(){try{var k=localStorage.getItem("deadshot.skin");var ok=["scope","og","red","leather","arcade"];if(k==="redact"&&localStorage.getItem("deadshot.clearance")==="1")ok.push("redact");document.documentElement.setAttribute("data-skin",ok.indexOf(k)>-1?k:"og");}catch(e){document.documentElement.setAttribute("data-skin","og");}})();</script>
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
<div class="mast"><div class="mast-in">
    <svg class="scope" viewBox="0 0 120 120" role="img" aria-label="Deadshot crosshair">
      <defs>
        <clipPath id="ck"><circle cx="60" cy="60" r="52"/></clipPath>
        <radialGradient id="glass" cx="38%" cy="32%">
          <stop offset="0" stop-color="var(--rt-g1)"/><stop offset="1" stop-color="var(--rt-g2)"/>
        </radialGradient>
      </defs>
      <circle cx="60" cy="60" r="55" fill="none" stroke="var(--rt-ring)" stroke-width="6"/>
      <circle cx="60" cy="60" r="52" fill="url(#glass)"/>
      <g clip-path="url(#ck)" stroke="var(--rt-grid)" stroke-width=".7" opacity=".65">
        <path d="M12 24H108M12 36H108M12 48H108M12 60H108M12 72H108M12 84H108M12 96H108"/>
        <path d="M24 12V108M36 12V108M48 12V108M60 12V108M72 12V108M84 12V108M96 12V108"/>
      </g>
      <g clip-path="url(#ck)" class="sweep">
        <path d="M60 60 L60 4 A56 56 0 0 1 96 20 Z" fill="var(--rt)" opacity=".09"/>
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
  </div></div>
<nav><div class="nav-row" id="navRow"><div class="nav-in"><a class="navmark" href="#champions" aria-label="Top"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="50" fill="none" stroke="var(--brass)" stroke-width="9"/><g stroke="var(--brass)" stroke-width="13" stroke-linecap="round"><path d="M60 6V40"/><path d="M60 80V114"/><path d="M6 60H40"/><path d="M80 60H114"/></g><circle cx="60" cy="60" r="7" fill="var(--brass)"/></svg></a><span id="nav" style="display:contents"></span></div></div>
  <div class="fb"><div class="fb-in">
    <span class="fb-lab">Managers</span>
    <button id="fActive">Active 10</button><button id="fAll">All 20</button><button id="fNone">None</button>
    <button id="fToggle">Choose managers &#9662;</button>
    <span class="fb-count" id="fCount"></span>
    <span class="fb-lab" style="margin-left:14px">Theme</span>
    <button data-skin-btn="scope">Scope</button><button data-skin-btn="og">Classic</button><button data-skin-btn="red">Crimson</button><button data-skin-btn="leather">Pigskin</button><button data-skin-btn="arcade">Arcade</button>
  </div><div class="fb-chips" id="fChips" hidden></div></div>
</nav>
<div class="wrap">

  <section id="champions">
    <div class="sec-head"><h2>Champions</h2><div class="rule-note">Click a year to jump to that bracket<br>with the winner's run traced</div></div>
    <div class="board" id="board"></div>
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
          <input id="search" type="search" placeholder="filter managers…" style="width:150px"><span class="sub" id="searchN"></span></div></div>
      <div class="scroll"><table id="tAll"></table></div>
    </div>
  </section>
  <section id="power">
    <div class="sec-head"><h2>Power Index<span class="gl" data-gl="pi" tabindex="0">?</span></h2><div class="rule-note">Sorted: seasons played, then surname<br>Click a row to lock it — stacks with others</div></div>
    <p class="lede"><strong>100 is exactly average for that season.</strong> 112 means you scored 12% more than the typical team that year. Because it is re-based every season it survives scoring inflation — a 110 in 2015 and a 110 in 2025 are the same achievement, even though the league scored 12% more points in 2025.</p>
    <div class="card">
      <div class="card-h"><h3>Power Index by manager and season</h3><span class="sub" id="piLegend"></span></div>
      <div class="card-b scroll"><table class="heat" id="tHeat"></table></div>
    </div>
  </section>
  <section id="rankings">
    <div class="sec-head"><h2>Power Rankings</h2><div class="rule-note">The ten active managers · live model</div></div>
    <p class="lede">Not a career table — a <strong>forward-looking</strong> one. It weights recent seasons above old ones, shrinks small samples toward the league mean, and ignores win-loss record entirely in favour of scoring, because record carries luck and scoring does not. Drag the slider to change how hard the model discounts the past and watch the order move.</p>
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

    <div class="card">
      <div class="card-h"><h3>Career races &mdash; one manager, every season</h3>
        <span class="sub">Every season with a game log &middot; one line per season, brightest is most recent</span></div>
      <div class="card-b" style="padding-bottom:4px"><div class="pills" id="crPick"></div></div>
      <div class="card-b" style="padding:0 16px 6px"><div class="pills" id="crLeg"></div></div>
      <div class="card-b" style="padding-top:4px"><div class="chart" id="crace"></div>
        <p style="margin:10px 0 0;font-size:12.5px;color:var(--ink-3)">The same bump chart, re-cut by manager: one line per season, <strong>brightest is most recent</strong>. Each line is labelled with its year and the team name that year &mdash; the names change, the manager does not. Weekly game logs exist for <span id="crSpan"></span> only, so earlier seasons cannot be drawn. There is no shaded playoff band here because the field size changed between these seasons; each line's dashed tail ends at where that season actually finished.</p></div>
    </div>
  </section>


  <section id="shape">
    <div class="sec-head"><h2>Season Shape</h2><div class="rule-note">Was it a dogfight or a walkover?</div></div>
    <p class="lede">A league average hides the interesting part. These show <strong>how spread out</strong> the league was each year — whether everyone was bunched together or three teams ran away with it.</p>
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
    <p class="lede">Season totals can only ever <em>estimate</em> luck; <strong>weekly scores measure it directly.</strong> Pick a season — the whole section below re-reads. Greyed years have no game log loaded yet. This section always shows <strong>every manager who played that year</strong>; the manager filter above governs the all-time sections only.</p>
    <div class="pills" id="wkYears"></div>

    <div class="card">
      <div class="card-h"><h3>The race — league position, week by week</h3>
        <span class="sub">Rank 1 at the top · click any number of teams to lock them</span></div>
      <div class="card-b" style="padding-bottom:6px"><div class="pills" id="raceLeg"></div></div>
      <div class="card-b" style="padding-top:4px"><div class="chart" id="race"></div>
        <p style="margin:10px 0 0;font-size:12.5px;color:var(--ink-3)">Standing after each week, ranked by record then points for — the same tiebreak the league uses. The shaded band is that season's playoff field &mdash; <span id="raceSpots"></span>. Every dot is a distinct position, so hovering one is never ambiguous even where lines cross. The dashed tail past the divider is the postseason: where each team actually finished.</p></div>
    </div>

    <div class="card">
      <div class="card-h"><h3>All-play &mdash; the record with the schedule removed</h3><span class="gl" data-gl="allplay" tabindex="0">?</span>
        <span class="sub" id="apSub">Sorted: all-play win %</span></div>
      <div class="card-b" style="padding-bottom:0"><p style="margin:0 0 14px;font-size:13.5px;color:var(--ink-2)">Each week, count how many of the other nine teams you outscored. Every week, versus everyone.</p></div>
      <div class="scroll"><table id="tAP"></table></div>
    </div>

    <div class="card">
      <div class="card-h"><h3>Beating the projection</h3><span class="sub">Actual points minus the projections, per week</span></div>
      <div class="card-b" style="padding-bottom:0"><p style="margin:0 0 14px;font-size:13.5px;color:var(--ink-2)">The grey number under every score is what the site projected. Consistently clearing it means your start/sit calls and waiver pickups were working &mdash; though a good chunk of this is noise, so read the per-week column, not the season total.</p></div>
      <div class="scroll"><table id="tProj"></table></div>
    </div>

    <div class="card">
      <div class="card-h"><h3>Rivalry week &mdash; on the numbers</h3><span class="gl" data-gl="rivalry" tabindex="0">?</span><span class="sub">meetings &times; balance &times; closeness</span></div>
      <div class="card-b" style="padding-bottom:0"><p style="margin:0 0 14px;font-size:13.5px;color:var(--ink-2)" id="rivPick"></p></div>
      <div class="scroll"><table id="tRiv"></table></div>
    </div>

    <div class="card">
      <div class="card-h"><h3>Weekly scoreboard</h3><div class="right pills" id="wkSel"></div></div>
      <div class="card-b" id="wkOut"></div>
    </div>

    <div class="card">
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
    <p class="lede">Everything here comes from season totals and the playoff game log, so it spans all ten seasons. The Week by Week section goes deeper but only for the years whose game logs are loaded.</p>
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
  </section>

  <section id="fivehundred">
    <div class="sec-head"><h2>The .500 Line</h2><div class="rule-note">Who lives above it, who lives under it<br>Sorted: games clear of even</div></div>
    <p class="lede">Win percentage tells you where a career ended up. It does not tell you how much of it was spent winning. <strong>Games clear</strong> is wins minus losses across a whole career &mdash; the plainest measure there is. <strong>Weeks above</strong> goes finer, walking each season week by week and asking whether that manager's record was above water at the time; it covers 2021&ndash;2025, the seasons with a loaded game log. <strong>Expected vs average</strong> asks a different question again: forget the schedule, how many wins did the <em>scoring</em> earn above a perfectly average team?</p>
    <div class="card">
      <div class="card-h"><h3>Above and below</h3><span class="gl" data-gl="five" tabindex="0">?</span>
        <span class="sub">Career &middot; every manager</span>
        <div class="right"><button id="fiveMore" class="on">Hide table &#9652;</button></div></div>
      <div class="scroll" id="fiveTbl"><table id="tFive"></table></div>
    </div>
  </section>

  <section id="records">
    <div class="sec-head"><h2>Record Book</h2><div class="rule-note">Each table by its own metric</div></div>
    <p class="lede">Season length has been 13, 14 and 15 games, so the headline records are <strong>per game</strong>; raw totals are kept separately and labelled as counting records, because a 15-game season will always out-total a 13-game one. <strong>Single-season records include everyone</strong> &mdash; one enormous year is a real record no matter how briefly someone played. The career <em>rate</em> tables below (win %, average finish, power index, luck) exclude one-season managers, whose tiny samples otherwise own every extreme; the career <em>counting</em> tables (total points, playoff wins) include everyone, since volume cannot be inflated by a short career.</p>
    <div id="recs"></div>
  </section>

  <section id="seasons">
    <div class="sec-head"><h2>Seasons</h2><div class="rule-note">Standings and bracket, year by year<br>Everyone who played that season is shown</div></div>
    <div class="pills" id="yrPills" style="margin:16px 0 18px"></div>
    <div id="seasonPane"></div>
    <div id="schedPane"></div>
  </section>

  <section id="h2h">
    <div class="sec-head"><h2>Head to Head</h2><div class="rule-note">Sorted: seasons played</div></div>
    <p class="lede">Read across: the row manager's record against the column manager. Playoffs cover all ten seasons; regular season covers only the years whose game logs are loaded. Use the manager filter at the top to cut the grid down to the people you care about.</p>
    <div class="card">
      <div class="card-h"><h3>Pick two managers</h3><div class="right">
        <select id="cmpA"></select><span class="sub">versus</span><select id="cmpB"></select></div></div>
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
    <p class="lede">Every trade in the five seasons whose transaction logs are loaded. A trade counts once for each side, so the two managers in a deal each get credit for it. <em>In</em> and <em>out</em> count players, not deals &mdash; a three-for-one shows up as 3 in and 1 out for the side receiving three.</p>
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

  <section id="method">
    <div class="card" style="margin-bottom:18px">
      <div class="card-h"><h3>League rules</h3><span class="sub">Read from Yahoo &middot; league 526001 &middot; 26 Aug 2026</span></div>
      <div class="card-b">
        <p class="lede" style="margin:0 0 13px">Everything below is the league's own configuration, not an assumption. The one that matters most for reading any number on this site: <strong>Deadshot is full PPR</strong> &mdash; a reception is worth 1.0, double Yahoo's default. That is why scores here run 120&ndash;140 rather than 90&ndash;110, and why raw points cannot be compared against another league.</p>
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
</div>
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
    <div class="wr-top"><div class="wrb" id="wrBrand"></div><button class="wr-x" id="wrX" aria-label="Close">&#10005;</button></div>
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
const SECS=[['champions','Champions'],['alltime','All-Time'],['power','Power Index'],['rankings','Power Rankings'],
 ['shape','Season Shape'],['weekly','Week by Week'],['luck','Luck'],['advanced','Advanced'],['fivehundred','.500 Line'],
 ['records','Records'],['seasons','Seasons'],['h2h','Head to Head'],['trades-sec','Trade Market'],['method','Method']];
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
  const t0=c.currentTime+(delay||0);
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
  const t0=c.currentTime+(delay||0), n=Math.max(1,Math.floor(c.sampleRate*dur));
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
  shot(){                            /* the sixth — one round, and the whole valley hears it */
    ALARM.stop(true);
    /* the whip of the round going past: very short, very bright, very loud */
    noise(.012,.95,16000,9000,0,'highpass',.35);
    noise(.05,.8,12000,2600,.004,'highpass',.6);
    /* the muzzle blast behind it */
    noise(.34,.85,4200,120,.02,'lowpass',1.6);
    tone(78,.75,'sawtooth',.42,30,.02);
    tone(44,1.5,'sine',.3,24,.03);
    /* eight returns off the terrain: later, quieter, and darker each time */
    [[.19,.34],[.36,.26],[.58,.2],[.86,.15],[1.2,.11],[1.62,.08],[2.1,.055],[2.66,.035]]
      .forEach(([d,v],i)=>{
        noise(.3+i*.11,v,2800-i*300,90,d,'lowpass',1.1);
        tone(150-i*11,.5+i*.1,'sine',v*.4,60,d);
      });
    /* the long tail hanging in the air */
    noise(3.6,.13,700,45,.3,'lowpass',.8);
    tone(38,4,'sine',.11,26,.32);
    /* glass, once the report is on its way out */
    for(let i=0;i<24;i++)
      tone(1500+Math.random()*4400,.06+Math.random()*.11,'triangle',.03,700,.14+Math.random()*.6);
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
    if(e.key.length!==1)return;
    buf=(buf+e.key.toLowerCase()).slice(-24);
    if(buf.endsWith('cossu')){buf='';botCall();}
    if(buf.endsWith('chaos')){buf='';chaos();}
  });
})();
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
  setTimeout(()=>el.classList.add('out'),2600);
  setTimeout(()=>el.remove(),3400);
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
(function(){let k='og';try{k=localStorage.getItem('deadshot.skin')||'og';}catch(e){}
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
  if(!seq||!row)return null;
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
    ${rivals.length?`<div class="sub-h">Playoff head-to-head</div><div style="display:flex;flex-wrap:wrap;gap:7px">${
      rivals.map(r=>`<span class="chip" style="cursor:pointer" data-m="${esc(r.o)}"><b>${r.w}–${r.l}</b> vs ${esc(r.o)}</span>`).join('')}</div>`:''}`;
  const wb=$('#mBody .wrapBtn'); if(wb)wb.onclick=()=>openWrapped(wb.dataset.w);
  ov.classList.add('on'); document.body.style.overflow='hidden'; $('#mX').focus();
}
function closeMgr(){ov.classList.remove('on');document.body.style.overflow='';hideTip();
  if(RETFOCUS&&document.contains(RETFOCUS)){try{RETFOCUS.focus();}catch(e){}} RETFOCUS=null;}
$('#mX').onclick=closeMgr;
ov.addEventListener('click',e=>{if(e.target===ov)closeMgr();});
addEventListener('keydown',e=>{if(e.key==='Escape'&&ov.classList.contains('on'))closeMgr();});
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
      `<th class="s${st.i===i?' '+st.dir:''}${c.c==='num'?' num':''}" data-i="${i}"${c.t?` title="${c.t}"`:''}>${c.h}</th>`).join('')+'</tr></thead><tbody>'+
      d.map((r,n)=>`<tr class="${opts.cls?opts.cls(r):''}">`+(opts.rank?`<td class="rk">${n+1}</td>`:'')+
      cols.map(c=>`<td class="${c.c||''}">${c.f(r)}</td>`).join('')+'</tr>').join('')+'</tbody>';
    $$('th.s',el).forEach(th=>th.onclick=()=>{const i=+th.dataset.i;
      if(st.i===i)st.dir=st.dir==='desc'?'asc':'desc'; else{st.i=i;st.dir=cols[i].asc?'asc':'desc';} render();});
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
      <span>SCORE</span><span>PROJ W%</span><span>vs&nbsp;λ1</span><span>EVID</span></div>`+out;
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
   {h:'Manager',f:r=>mlink(r.name),c:'nm',k:r=>r.name,asc:1},
   {h:'Szns',f:r=>r.seasons,c:'num',k:r=>r.seasons},
   {h:'Career PI',f:r=>f(r.cpi,1),c:'num',k:r=>r.cpi},
   {h:'Peak',f:r=>f(r.peak,1),c:'num',k:r=>r.peak},
   {h:'Floor',f:r=>f(r.floor,1),c:'num',k:r=>r.floor},
   {h:'Std dev',f:r=>r.sd==null?'—':f(r.sd,1),c:'num',k:r=>r.sd,t:'Low = metronome, high = boom or bust'},
   {h:'Z avg',f:r=>(r.zAvg>=0?'+':'')+r.zAvg.toFixed(2),c:'num',k:r=>r.zAvg,t:'Standard deviations above or below the league mean, averaged over a career. 0 = exactly average, +1 = a full deviation clear of the field.'},
   {h:'Z peak',f:r=>(r.zPeak>=0?'+':'')+r.zPeak.toFixed(2),c:'num',k:r=>r.zPeak,t:'Best single season by Z-score'},
   {h:'Z floor',f:r=>(r.zFloor>=0?'+':'')+r.zFloor.toFixed(2),c:'num',k:r=>r.zFloor,t:'Worst single season by Z-score'},
   {h:(()=>{const q=advYears();const a=Math.max(q[0],q[q.length-1]-2),b=q[q.length-1];return a===b?'Form '+b:'Form '+String(a).slice(2)+'–'+String(b).slice(2);})(),f:r=>r.form==null?'—':f(r.form,1),c:'num',k:r=>r.form},
   {h:'Trend',f:r=>r.trend==null?'—':(r.trend>=0?'+':'')+r.trend.toFixed(1),c:'num',k:r=>r.trend},
   {h:'',f:r=>r.trend==null?'':dbar(r.trend,9,pol(r.trend)),k:r=>r.trend},
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
    t:'Record against opponents who finished that season above .500. Every game on record — all ten seasons of playoffs plus the 2021–2025 regular seasons.'},
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
      <span class="sub">${c.n} teams · ${c.g}-game season · ${c.spots}-team bracket · league avg ${c.lg.toFixed(2)} PPG</span></div>
      <div class="scroll"><table id="tS"></table></div></div>
    <div class="card"><div class="card-h"><h3>${y} bracket</h3>
      <span class="sub">${c.co?'Final voided — title split':'Hover a team to trace its run · click to lock it'}</span>
      <span class="sub" id="brkTrace" style="color:var(--brass)"></span></div>
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
  const names=M.map(m=>m.name).sort();
  $('#cmpA').innerHTML=names.map(n=>`<option>${esc(n)}</option>`).join('');
  $('#cmpB').innerHTML=names.map(n=>`<option>${esc(n)}</option>`).join('');
  $('#cmpA').value='Brian Burke'; $('#cmpB').value='Shane Kaiper';
  function draw(){
    const a=byName[$('#cmpA').value],b=byName[$('#cmpB').value];
    if(!a||!b||a===b){$('#cmpOut').innerHTML='<p class="dim" style="margin:0">Pick two different managers.</p>';return;}
    const splits=[['Regular season','reg'],['Playoffs','po'],['All games','all']];
    const rows=[['Seasons','seasons',0],['Titles','titles',1],['Podiums','podium',0],['Playoff apps','apps',0],
      ['Win %','winpct',3],['Avg finish','avgPlace',2],['PPG','ppg',2],['Power index','cpi',1],
      ['Luck','luck',2],['Playoff W','poW',0]];
    const cell=(m,k,d)=>k==='winpct'?pct(m[k]):(d?(+m[k]).toFixed(d):m[k]);
    const better=(k,x,y)=>k==='avgPlace'?x<y:x>y;
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
  $('#cmpA').onchange=draw; $('#cmpB').onchange=draw; draw(); REDRAW.push(draw);
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
  /* Seasons have to be told apart at a glance. A --mid -> --brass ramp alone was too
     subtle: on several skins those two sit close together and the middle years blurred.
     Ramp from a faint neutral all the way to the full accent (a much wider lightness
     span, which survives every skin including redact where --brass is pure white), and
     vary stroke weight with it as a second, colour-blind-safe cue. */
  const BR=cssv('--brass');
  const FAR=mix(cssv('--surface'),cssv('--ink-3'),0.62);
  const tOf=i=>S.length<2?1:i/(S.length-1);
  const col=i=>S.length<2?BR:mix(FAR,BR,tOf(i));
  const wid=i=>1.7+1.6*tOf(i);
  const rad=i=>3.4+1.2*tOf(i);

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
    return {y:s.y,team:s.team,K:s.K,R,d,c:col(i),w:wid(i),r:rad(i),seedRank:endRank,fin:fp,moved:endRank-fp,
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
    S.map((s,i)=>`<button data-cy="${s.y}" style="padding:4px 9px"><b style="color:${col(i)}">${s.y}</b> <span class="dim">${esc(s.team)}</span></button>`).join('')+
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
  $('#rivPick').innerHTML=`<b>${esc(top.a)}</b> vs <b>${esc(top.b)}</b> — ${top.g} meeting${top.g>1?'s':''}, split ${top.aw}–${top.bw}, decided by an average of <b>${top.marg.toFixed(2)}</b> points. That is the rivalry-week fixture on the numbers.`;

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
        return `<div class="game${vd?' void':''}"><div class="gh">${vd?(roundName(YR,K5,g)||'Week '+w)+' — VOID':(roundName(YR,K5,g)||'Week '+w)+' · margin '+Math.abs(g.aa-g.ab).toFixed(2)}</div>${s(g.ta,g.aa,g.pa,aw)}${s(g.tb,g.ab,g.pb,!aw)}</div>`;}).join('')
      + by.map(b=>`<div class="game"><div class="gh">${byeName(K5,b)}</div><div class="side bye"><span class="tn">${esc(b.t)}<small>${esc(MG[b.t])} · proj ${b.p.toFixed(1)}</small></span><span class="sc">${b.a.toFixed(2)}</span></div></div>`).join('')}</div>`;
  }
  $$('#wkSel button').forEach(b=>b.onclick=()=>drawWk(+b.dataset.w));
  drawWk(WKS[0]); push(()=>{const on=$$('#wkSel button.on')[0]; if(on)drawWk(+on.dataset.w);});

  /* trades */
  function drawTrades(){
  $('#trades').innerHTML=K5.trades.map(t=>`<div class="card" style="margin-top:0">
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
        if(!n){h+='<td><span style="color:var(--ink-3)">0</span></td>';return;}
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
  tone(62,4.2,'sine',.17,44);               /* the gong */
  tone(93,3.6,'sine',.09,70,null,.02);
  noise(1.1,.13,2600,180);
  tone(48,5.4,'sawtooth',.05,132,null,.15); /* the rising drone */
  [0,.18,.34,.52,.7,.95,1.2,1.5].forEach((d,i)=>
    tone(660*Math.pow(1.16,i),1.5,'sine',.028,null,null,1.0+d));  /* shimmer */
  tone(150,2.4,'sawtooth',.13,36,null,1.05);   /* the hit on the splash */
  noise(1.8,.1,5200,140,1.05);
  tone(41,5,'sine',.09,30,null,1.1);
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
(function(){const WORDS=['commish','commissioner']; let buf='';
  addEventListener('keydown',e=>{
    if(e.metaKey||e.ctrlKey||e.altKey)return;
    const t=e.target; if(t&&/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))return;
    if(e.key.length!==1)return;
    buf=(buf+e.key.toLowerCase()).slice(-24);
    if(WORDS.some(w=>buf.endsWith(w))){buf='';pharaoh();}});})();

glossify();

</script>

"""

SHELL_TOP = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="description" content="The Deadshot fantasy football record book — ten seasons of champions, standings, power rankings, head-to-head and trades.">
<meta name="robots" content="noindex">
'''
out = SHELL_TOP + HEAD + '</head>\n<body>\n' + BODY.replace('__DATA__', DATA) + JS + '\n</body>\n</html>\n'
open('index.html','w').write(out)
print("bytes", len(out))
