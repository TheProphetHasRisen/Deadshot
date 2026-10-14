/* ============ Ask the record book ======================================================
   A question in plain English becomes a query: which managers, teams or players, which
   seasons or week, which measure, and what kind of question it is (one value, a head to
   head, a leader board, a season, a week, a team, a player). The answer is then worked out
   from exactly the numbers the page shows -- the same rows, the same career figures, the same
   head-to-head tallies -- and every answer carries a button to the section it came from.

   Modelled on the Celtics Hub ask box. The reader here is deterministic and offline: no key,
   no cost, instant, and the same question always gets the same answer. Words it could not
   place are shown back ("Not used: ..."), so nothing is misread silently.

   Built to grow with the Yahoo data. Player names come from every source that has them (today
   the trade log; once the connection lands, D.players), and each thing that needs Yahoo data
   (drafts, injuries, waivers, lineups) says so plainly until the data for it exists -- see SOON.

   This file is appended to page/site.js inside the same <script>, so it reads the page's own
   globals (D, ROWS, M, MX, openMgr, sg, ...). test_ask.js holds the questions it must keep
   answering; run it after any change here. */
/* exported Ask -- read by test_ask.js through the page */
const Ask=(()=>{
  /* ---------------------------------------------------------------- words in, words out */
  const norm=s=>String(s==null?'':s).toLowerCase()
    .replace(/[‘’`]/g,"'").replace(/[“”"]/g,' ')
    .replace(/%/g,' percent ').replace(/'s\b/g,'').replace(/'/g,'')
    .replace(/\b([a-z])\.([a-z])\./g,'$1$2')          /* C.J. -> cj */
    .replace(/\.(?!\d)/g,' ')                          /* Jr. -> jr, but 0.33 stays */
    .replace(/([a-z])-(?=[a-z])/g,'$1 ')               /* BO-lieve -> bo lieve; 9-5 stays */
    .replace(/[^a-z0-9.+#\- ]/g,' ').replace(/\s+/g,' ').trim();
  const SUFFIX=new Set(['jr','sr','ii','iii','iv','v']);
  const toks=n=>norm(n).split(' ').filter(Boolean);
  const firstOf=n=>toks(n)[0]||'';
  const lastOf=n=>{const t=toks(n);while(t.length>1&&SUFFIX.has(t[t.length-1]))t.pop();return t[t.length-1]||'';};
  const tally=a=>a.reduce((o,x)=>(o[x]=(o[x]||0)+1,o),{});
  const W2N={one:1,two:2,three:3,four:4,five:5,six:6,seven:7,eight:8,nine:9,ten:10};
  const rec=(w,l,t)=>w+'–'+l+(t?'–'+t:'');

  /* ---------------------------------------------------------------- what can be named */
  const MG=M.map(m=>m.name);
  const fc=tally(MG.map(firstOf)), lc=tally(MG.map(lastOf));
  const MGRWORDS=new Set([...MG.map(firstOf),...MG.map(lastOf)]);
  const ENT=[];                  /* {p: phrase, t: kind, v: value}, longest phrase wins */
  MG.forEach(n=>{
    ENT.push({p:norm(n),t:'mgr',v:n});
    if(lc[lastOf(n)]===1)ENT.push({p:lastOf(n),t:'mgr',v:n});
    if(fc[firstOf(n)]===1)ENT.push({p:firstOf(n),t:'mgr',v:n});});
  /* "Brian" is two managers and "Watson" is two more: ask, never guess */
  Object.keys(fc).filter(k=>fc[k]>1).forEach(k=>ENT.push({p:k,t:'amb',v:MG.filter(n=>firstOf(n)===k)}));
  Object.keys(lc).filter(k=>lc[k]>1).forEach(k=>ENT.push({p:k,t:'amb',v:MG.filter(n=>lastOf(n)===k)}));
  /* team names. A few are ordinary words a question would use, or a manager's own name. */
  const TEAMSKIP=new Set(['the end','walter','supreme','victory']);
  const TEAMROWS={}, PLAINTEAMS={};
  ROWS.forEach(r=>{const k=norm(r.team);
    if(TEAMSKIP.has(k)||MGRWORDS.has(k)){(PLAINTEAMS[k]=PLAINTEAMS[k]||[]).push(r); return;}
    if(k.length<3)return;
    (TEAMROWS[k]=TEAMROWS[k]||[]).push(r);});
  Object.keys(TEAMROWS).forEach(k=>ENT.push({p:k,t:'team',v:TEAMROWS[k]}));
  /* NFL players, from every source that has them. Today that is the trade log. */
  const PL={};
  const plOf=n=>(PL[n]=PL[n]||{name:n,trades:[]});
  ((D.trade&&D.trade.log)||[]).forEach(x=>[...x.pa,...x.pb].forEach(n=>plOf(n).trades.push(x)));
  if(Array.isArray(D.players))D.players.forEach(p=>{const n=typeof p==='string'?p:p.name; if(n)plOf(n).info=p;});
  const PNAMES=Object.keys(PL), plc=tally(PNAMES.map(lastOf));
  PNAMES.forEach(n=>{ENT.push({p:norm(n),t:'player',v:n});
    const l=lastOf(n);
    /* a surname alone only when it is unmistakable: unique, not short, not a manager's */
    if(plc[l]===1&&l.length>=5&&!MGRWORDS.has(l))ENT.push({p:l,t:'player',v:n});});
  ENT.sort((a,b)=>b.p.length-a.p.length);

  /* ---------------------------------------------------------------- what can be measured
     car: the career figure, read off the same record the page uses (M).
     row: the same thing for one team-season (ROWS).
     agg: for a span of seasons, from the rows, the way export.py builds the career figure.
     hi:  1 if more is better, 0 if less is (average finish), null if neither (points against).
     rate: a rate, so a one-season career does not top a career leader board (as the record
           book does: rates need 2+ seasons). sec: where the button goes. */
  const F2=v=>v==null?'—':(+v).toFixed(2), F1=v=>v==null?'—':(+v).toFixed(1);
  const titleTxt=v=>v===0?'0':(v%1?String(v):String(v));
  const sumR=(rs,k)=>rs.reduce((s,r)=>s+r[k],0);
  const games=rs=>sumR(rs,'w')+sumR(rs,'l')+sumR(rs,'t');
  const MET={
    titles:{lab:'Titles',syn:['titles','title','championships','championship','rings','ring','trophies','trophy','chips','won it all','won the league','champ','champs','natties'],
      car:m=>m.titles,row:r=>r.place===1?r.share:0,agg:rs=>rs.filter(r=>r.place===1).reduce((s,r)=>s+r.share,0),
      fmt:titleTxt,hi:1,sec:'champions',rowTxt:r=>r.place===1?(r.co?'Co-champion':'Champion'):'No title'},
    podium:{lab:'Podium finishes',syn:['podiums','podium','podium finishes','top 3 finishes','top three finishes','medals'],
      car:m=>m.podium,row:r=>r.place<=3?1:0,agg:rs=>rs.filter(r=>r.place<=3).length,fmt:String,hi:1,sec:'alltime'},
    apps:{lab:'Playoff appearances',syn:['playoff appearances','playoff apps','appearances','times in the playoffs','made the playoffs','postseason appearances','made playoffs'],
      car:m=>m.apps,row:r=>r.po?1:0,agg:rs=>rs.filter(r=>r.po).length,fmt:String,hi:1,sec:'advanced',rowTxt:r=>r.po?'Made the playoffs':'Missed the playoffs'},
    finals:{lab:'Finals reached',syn:['finals reached','final appearances','finals appearances','title games','championship appearances'],
      car:m=>m.finals,fmt:String,hi:1,sec:'advanced'},
    wins:{lab:'Wins',syn:['wins','win total','victories'],car:m=>m.w,row:r=>r.w,agg:rs=>sumR(rs,'w'),fmt:String,hi:1,sec:'alltime'},
    losses:{lab:'Losses',syn:['losses','defeats','loss total'],car:m=>m.l,row:r=>r.l,agg:rs=>sumR(rs,'l'),fmt:String,hi:null,sec:'alltime'},
    record:{lab:'Record',syn:['record','win loss','w l','wl','win loss record'],car:m=>m.winpct,row:r=>(r.w+r.t/2)/r.g,
      agg:rs=>(sumR(rs,'w')+sumR(rs,'t')/2)/games(rs),hi:1,sec:'alltime',
      show:(v,o)=>o?rec(o.w,o.l,o.t)+' <span class="dim">'+pct(v)+'</span>':pct(v)},
    winpct:{lab:'Win %',syn:['win %','win percent','win percentage','winning percentage','win rate','win pct','winning pct'],
      car:m=>m.winpct,row:r=>(r.w+r.t/2)/r.g,agg:rs=>(sumR(rs,'w')+sumR(rs,'t')/2)/games(rs),fmt:pct,hi:1,rate:1,sec:'alltime'},
    ppg:{lab:'Points per game',syn:['ppg','points per game','scoring average','average score','avg score','scoring'],
      car:m=>m.ppg,row:r=>r.ppg,agg:rs=>sumR(rs,'pf')/games(rs),fmt:F2,hi:1,rate:1,sec:'alltime'},
    pf:{lab:'Points for',syn:['points for','total points','pf','points scored','points'],car:m=>m.pf,row:r=>r.pf,agg:rs=>sumR(rs,'pf'),fmt:F2,hi:1,sec:'records'},
    pa:{lab:'Points against',syn:['points against','pa','points allowed','scored against'],car:m=>m.pa,row:r=>r.pa,agg:rs=>sumR(rs,'pa'),fmt:F2,hi:null,sec:'alltime'},
    pi:{lab:'Power index',syn:['power index','power idx','power rating','pi','power'],car:m=>m.cpi,row:r=>r.pi,
      agg:rs=>rs.reduce((s,r)=>s+r.pi*(r.w+r.l+r.t),0)/games(rs),fmt:F1,hi:1,rate:1,sec:'power'},
    z:{lab:'Z-score',syn:['z score','zscore','z'],car:m=>m.zAvg,row:r=>r.z,agg:rs=>rs.reduce((s,r)=>s+r.z*(r.w+r.l+r.t),0)/games(rs),fmt:v=>sg(v,2),hi:1,rate:1,sec:'advanced'},
    luck:{lab:'Luck',syn:['luck','lucky','luckiest','unlucky','unluckiest','schedule luck'],car:m=>m.luck,row:r=>r.luck,agg:rs=>sumR(rs,'luck'),
      fmt:v=>sg(v,2),unit:' wins',hi:1,sec:'luck'},
    allplay:{lab:'All-play record',syn:['all play','allplay','all play record','all play %'],car:m=>m.apPct,fmt:pct,hi:1,rate:1,sec:'weekly',
      show:(v,o)=>o&&o.apW!=null?rec(o.apW,o.apL)+' <span class="dim">'+pct(v)+'</span>':pct(v)},
    finish:{lab:'Average finish',syn:['average finish','avg finish','finish','finished','finishes','place','placed','standing'],
      car:m=>m.avgPlace,row:r=>r.place,agg:rs=>sumR(rs,'place')/rs.length,fmt:F2,hi:0,rate:1,sec:'alltime',rowTxt:r=>r.place===1?(r.co?'Co-champion':'Champion'):ord(r.place)+' of '+r.teams},
    seed:{lab:'Seed',syn:['seed','seeding','seeded'],row:r=>r.seed,fmt:ord,hi:0,sec:'seasons',rowTxt:r=>ord(r.seed)+' seed'},
    trades:{lab:'Trades',syn:['trades','trade','traded','deals','trading','trader'],car:m=>(D.trade.mgr.find(x=>x.name===m.name)||{trades:0}).trades,
      row:r=>D.trade.log.filter(x=>x.y===r.y&&(x.ma===r.mgr||x.mb===r.mgr)).length,fmt:String,hi:1,sec:'trades-sec'},
    moves:{lab:'Roster moves',syn:['roster moves','moves','transactions'],row:r=>r.mv,agg:rs=>rs.every(r=>r.mv!=null)?sumR(rs,'mv'):null,fmt:String,hi:1,sec:'records'},
    seasons:{lab:'Seasons played',syn:['seasons played','years in the league','tenure','longevity','seasons','longest tenured'],car:m=>m.seasons,fmt:String,hi:1,sec:'alltime'},
    consistency:{lab:'Season-to-season spread',syn:['consistency','consistent','most consistent','steadiest','volatile','volatility'],
      car:m=>m.sd,fmt:F1,hi:0,rate:1,sec:'advanced'},
    clutch:{lab:'Titles above expectation',syn:['clutch','clutchest','most clutch','overachiever','overachieved'],car:m=>m.vsExp,fmt:v=>sg(v,2),hi:1,sec:'advanced'},
    lastpl:{lab:'Last-place finishes',syn:['last place finishes','last place','last places','dead last','toilet bowl','sacko','basement'],
      car:m=>m.lastPl,row:r=>r.place===r.teams?1:0,agg:rs=>rs.filter(r=>r.place===r.teams).length,fmt:String,hi:1,sec:'alltime'},
    diff:{lab:'Point differential',syn:['point differential','points differential','differential','average margin','avg margin','margin of victory','scoring margin'],
      car:m=>(m.pf-m.pa)/m.g,row:r=>(r.pf-r.pa)/r.g,agg:rs=>(sumR(rs,'pf')-sumR(rs,'pa'))/games(rs),fmt:v=>sg(v,2),hi:1,rate:1,sec:'alltime'},
    vsproj:{lab:'Points vs projection',syn:['points vs projection','points over projection','above projection','vs projection','versus projection','compared to projection'],fmt:v=>sg(v,2),hi:1,sec:'weekly'},
    beatproj:{lab:'Beat the projection',syn:['beat the projection','beat projection','beat their projection','beat his projection','beats the projection','beats their projection','beats his projection','beats projection','beating their projection','beat projections','beats projections','beating the projection','outscored the projection','over projection','outperformed projection'],fmt:pct,hi:1,sec:'weekly'},
    poRecord:{lab:'Playoff record',syn:['playoff record','postseason record','playoff wins','postseason wins'],car:m=>m.poW,fmt:String,hi:1,sec:'advanced',
      show:(v,o)=>o?rec(o.poW,o.poL):String(v)},
  };
  /* the measures that only make sense one game at a time */
  const GAMEMET={
    score:{lab:'Single-game score',syn:['score','scores','scoring week','scoring game','points in a week','points in a game','week','game'],hi:1},
    margin:{lab:'Winning margin',syn:['blowout','blowouts','biggest win','biggest margin','beatdown','beat down','largest margin','biggest blowout'],hi:1},
    close:{lab:'Closest game',syn:['closest game','closest','tightest','narrowest','photo finish'],hi:0},
    upset:{lab:'Biggest upset',syn:['biggest upset','biggest upsets','upset','upsets'],hi:1},
  };
  const METW=[];
  Object.entries(MET).forEach(([k,m])=>m.syn.concat([norm(m.lab)]).forEach(p=>METW.push({p:norm(p),k})));
  /* "win %" normalises to "win", which on its own is far too common a word to mean win rate */
  for(let i=METW.length-1;i>=0;i--)if(METW[i].p==='win')METW.splice(i,1);
  METW.sort((a,b)=>b.p.length-a.p.length);

  /* Things that need the Yahoo data. While D has no data for one, a question about it is
     answered with what is coming, not with a guess. When the data lands, add its answerer
     below and the line here falls away on its own (the `has` test). */
  const SOON=[
    {re:/\b(draft|drafted|drafts|draft pick|draft picks|first round|adp|auction|keeper|keepers)\b/,has:()=>!!D.draft,
      say:'Draft results come with the Yahoo connection.'},
    {re:/\b(injur\w*|injured reserve|on ir|ir slot|ir stint|hurt)\b/,has:()=>!!D.injuries,
      say:'Injury and IR history comes with the Yahoo connection, so "who had the worst injury luck" will work then.'},
    {re:/\b(waiver|waivers|waiver claim|waiver claims|free agent|free agents|pickup|pickups|picked up|faab)\b/,has:()=>!!D.waivers,
      say:'Waiver claims come with the Yahoo connection. Season totals of roster moves are here now: try "most roster moves".'},
    {re:/\b(started|starter|starters|starting lineup|lineup|lineups|benched|bench points|start sit|start or sit)\b/,has:()=>!!D.lineups,
      say:'Lineups (who started, who sat) come with the Yahoo connection.'},
    {re:/\b(yards|touchdowns|tds|receptions|targets|carries|fantasy points)\b/,has:()=>!!D.playerStats,
      say:'Player stats come with the Yahoo connection.'},
    {re:/\b(streak|streaks|in a row|straight wins|straight losses)\b/,has:()=>false,
      say:'Win streaks are not tallied yet.'},
  ];
  const STOP=new Set(('a an the of in on at for to from by with and or but is was were are be been do did does has have had '+
    'what whats which who whom whose how many much when where why ever all time all-time history overall '+
    'show me tell about give list find get see me my i you your he his him her their they them it its this that these those '+
    'there their season seasons year years league manager managers team teams player players game games week weeks '+
    'number numbers stats stat stat line please vs versus v against compared compare than ago so far since between '+
    'most least fewest best worst highest lowest top bottom leader leaders leads led rank ranking ranked who\'s who whos '+
    'biggest smallest largest greatest single one per average avg total totals career all play played playing deadshot '+
    'record book did do got get go went has had have make made made won win lost lose beat beats beaten time times '+
    'regular postseason playoffs playoff final finals championship bracket head h2h hth us we our out up down over').split(' '));

  /* ---------------------------------------------------------------- how people talk
     The way a league group chat actually asks, rewritten into the plain question it means
     before anything else reads it. Each pair is (what gets typed, what it means). Kept dry
     on purpose: these translate, they do not editorialise. */
  const SAY=[
    [/\b(goat|greatest of all time|best manager|best owner|top dog|king of the league|winningest)\b/g,' most titles '],
    [/\b(worst manager|worst owner|sucks|sucked|trash|garbage|bum|scrub)\b/g,' worst win percentage '],
    [/\b(robbed|screwed|cursed|snake ?bit|snakebitten|hard done by)\b/g,' unluckiest '],
    [/\b(fraud|frauds|fraudulent|carried|got lucky)\b/g,' luckiest '],
    [/\b(choke|chokes|choked|choker|chokers|choking|bottled|bottle job|folds|folded)\b/g,' least clutch '],
    [/\b(owns|owned|dominates|dominated|domination|has the number of|bullies|bullied|daddy|beat up on|beats up on)\b/g,' vs '],
    [/\b(smashed|destroyed|demolished|blew out|blown out|curb stomp\w*|massacre|beatdown|beat down)\b/g,' biggest blowout '],
    [/\b(heartbreak\w*|nail ?biter|squeaked by|squeaker|barely won|barely beat)\b/g,' closest game '],
    [/\b(best team|greatest team|best season|best single season|best year)\b/g,' highest power index season '],
    [/\b(worst team|worst season|worst year)\b/g,' lowest power index season '],
    [/\b(trade happy|trade addict|trade machine|wheeler dealer|wheeling and dealing|most active trader)\b/g,' most trades '],
    [/\b(went off|exploded|hung)\b/g,' highest score '],
    [/\b(best start|best starts|hottest start|fastest start|strongest start)\b/g,' best record first 4 weeks '],
    [/\b(worst start|worst starts|slowest start|coldest start)\b/g,' worst record first 4 weeks '],
    [/\b(best finish(?:er|ers)?|strongest finish|closer|finishes strong|best down the stretch)\b/g,' best record last 4 weeks '],
    [/\b(worst finish(?:er|ers)?|fades|fade|collapses|collapse|worst down the stretch)\b/g,' worst record last 4 weeks '],
    [/\b(most upsets|upset king|giant killer)\b/g,' most wins as underdog '],
    [/\b(gets upset|got upset|upset the most|most upset losses)\b/g,' most losses as favorite '],
    [/\b(bad beat|bad beats|tough luck losses?|unlucky losses?)\b/g,' most losses scoring 130+ '],
    [/\b(lucky wins?|stole wins?|backdoor wins?)\b/g,' most wins scoring under 110 '],
  ];
  /* Typos. Every word the reader knows -- names, team names, players, measures and the
     ordinary words of a question -- is the dictionary. A word it does not know is swapped
     for the nearest one it does, if it is close enough: one slip in a short word, two in a
     longer one, and a name has to keep its first letter when it is two slips away, because
     that is how people mistype and it stops "funny" turning into somebody's surname. The
     answer says what it read ("Read krugr as krueger"), so a wrong guess is visible. */
  const VOCAB=new Map();
  const addV=(w,k)=>{if(w&&w.length>=3&&!/\d/.test(w)&&!VOCAB.has(w))VOCAB.set(w,k);};
  ENT.forEach(e=>e.p.split(' ').forEach(w=>addV(w,e.t==='amb'?'mgr':e.t)));
  METW.forEach(e=>e.p.split(' ').forEach(w=>addV(w,STOP.has(w)?'word':'met')));
  Object.values(GAMEMET).forEach(g=>g.syn.forEach(p=>p.split(' ').forEach(w=>addV(w,'met'))));
  Object.keys(PLAINTEAMS).forEach(k=>k.split(' ').forEach(w=>addV(w,'team')));
  STOP.forEach(w=>addV(w,'word'));
  /* the words that carry a question's meaning outrank a team name that happens to be one
     slip away: "sart" is "start", not the Poison Dart Frogs */
  ('start starts finish finisher fade fades upset upsets stretch closer choke choker robbed goat fraud owns clutch '+
   'underdog underdogs favorite favourite projection projected close blowout blowouts luckiest unluckiest champion '+
   'playoffs titles trades record best worst most least highest lowest week weeks wins losses play').split(' ').forEach(w=>VOCAB.set(w,'met'));
  ('playoffs postseason regular season week career luckiest unluckiest versus against championship champion goat robbed '+
   'fraud choke choker clutch blowout closest trades traded since through draft drafted injury injured waiver lineup streak '+
   'score scored scoring points won beat lost who what weeks first last half early late stretch close blowouts underdog '+
   'underdogs favorite favourite projected projection after loss losses winning losing allowing opponents bounce '+
   'through until before opener often always usually ever never times much many does doing done gets got get play plays played '+
   'playing good bad better worse more less than above below every each any some both other others rest start finish '+
   'starts finishes average usually typically generally game games team teams week season seasons year years').split(' ').forEach(w=>addV(w,'word'));
  function dist(a,b,max){          /* edit distance, counting a swapped pair as one slip */
    if(Math.abs(a.length-b.length)>max)return max+1;
    const d=[]; for(let i=0;i<=a.length;i++)d[i]=[i];
    for(let j=1;j<=b.length;j++)d[0][j]=j;
    for(let i=1;i<=a.length;i++){let low=Infinity;
      for(let j=1;j<=b.length;j++){
        d[i][j]=Math.min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+(a[i-1]===b[j-1]?0:1));
        if(i>1&&j>1&&a[i-1]===b[j-2]&&a[i-2]===b[j-1])d[i][j]=Math.min(d[i][j],d[i-2][j-2]+1);
        if(d[i][j]<low)low=d[i][j];}
      if(low>max)return max+1;}
    return d[a.length][b.length];}
  const KINDRANK={mgr:0,met:1,team:2,player:3,word:4};   /* a tie goes to a name, then a measure */
  function fix(text){
    const fixed=[];
    const words=text.split(' ').map(w=>{
      if(w.length<3||VOCAB.has(w)||/\d/.test(w))return w;
      const short=w.length===3, max=w.length<=4?1:2; let best=null,bd=max+1,br=9;
      for(const [v,k] of VOCAB){
        if(Math.abs(v.length-w.length)>max)continue;
        const d=dist(w,v,max); if(d>max)continue;
        if(d===2&&k!=='word'&&v[0]!==w[0])continue;
        if(short&&(k==='word'||v[0]!==w[0]))continue;
        if(k==='word'&&d>1)continue;          /* only names and measures are worth a two-slip guess */
        const r=KINDRANK[k];
        const better=d<bd||(d===bd&&r<br)||(d===bd&&r===br&&((v[0]===w[0]&&best[0]!==w[0])||(v[0]===w[0])===(best[0]===w[0])&&v.length>best.length&&best.length<w.length));
        if(better){bd=d;best=v;br=r;}}
      if(best){fixed.push([w,best]); return best;}
      return w;});
    return {text:words.join(' '),fixed};}
  const say=t=>{SAY.forEach(([re,to])=>{t=t.replace(re,to);}); return t.replace(/\s+/g,' ');};

  /* ---------------------------------------------------------------- the reader */
  function parse(text){
    const q={raw:text,mgrs:[],teams:[],players:[],years:[],weeks:[],metrics:[],game:null,types:null,final:false,
      want:null,per:null,career:false,h2h:false,amb:null,soon:[],notes:[],missing:[],ignored:[],sl:{},split:null};
    const f=fix(say(norm(text)).trim());
    q.readAs=f.fixed;
    let t=' '+say(' '+f.text+' ').trim()+' ';
    q.said=t;
    if(!t.trim())return q;
    const eat=re=>{const m=t.match(re); if(m)t=t.replace(re,' ').replace(/\s+/g,' '); return m;};
    /* names first: team names carry digits and ordinary words ("12th Man Records") */
    const at={};                     /* where each manager was named, to keep their order */
    for(const e of ENT){
      let i;
      while((i=t.indexOf(' '+e.p+' '))>=0){
        if(e.t==='mgr'){if(!q.mgrs.includes(e.v)){q.mgrs.push(e.v); at[e.v]=i;}}
        else if(e.t==='team')q.teams.push(e.v);
        else if(e.t==='player'){if(!q.players.includes(e.v))q.players.push(e.v);}
        else if(e.t==='amb'&&!q.amb)q.amb={word:e.p,options:e.v};
        t=t.slice(0,i+1)+t.slice(i+1+e.p.length);
      }
    }
    q.mgrs.sort((a,b)=>at[a]-at[b]);
    {const bare=t.replace(/ (?:in |the )?(?:19|20)\d\d /g,' ').trim(); if(PLAINTEAMS[bare]&&!q.mgrs.length&&!q.teams.length){q.teams.push(PLAINTEAMS[bare]); t=t.replace(' '+bare+' ',' ');}}
    t=' '+t.replace(/\s+/g,' ').trim()+' ';
    /* coming with Yahoo */
    for(const s of SOON)if(s.re.test(t)&&!s.has()){q.soon.push(s.say); t=t.replace(s.re,' ');}
    /* seasons */
    let m;
    const keepYear=y=>{
      if(SEA.includes(y)){if(!q.years.includes(y))q.years.push(y); return;}
      if(y===2019)q.missing.push('2019 is missing from the source records, so the book skips from 2018 to 2020.');
      else if(y<SEA[0])q.missing.push('The league started in '+SEA[0]+'.');
      else if(y>LAST)q.missing.push('The '+y+' season is not in the book yet. The latest finished season is '+LAST+'.');
    };
    while((m=t.match(/ (?:from )?(20\d\d) ?(?:-|to|through|thru|until) ?(20\d\d) /))){
      const a=+m[1],b=+m[2]; SEA.filter(y=>y>=Math.min(a,b)&&y<=Math.max(a,b)).forEach(keepYear);
      if(Math.min(a,b)<=2019&&Math.max(a,b)>=2019)q.notes.push('2019 is missing from the source records.');
      t=t.replace(m[0],' ');}
    if((m=eat(/ since (20\d\d) /)))SEA.filter(y=>y>=+m[1]).forEach(keepYear);
    if((m=eat(/ (?:last|past|previous) (\d+|two|three|four|five|six|seven|eight|nine|ten) (?:seasons|years) /))){
      const n=W2N[m[1]]||+m[1]; SEA.slice(-n).forEach(keepYear);}
    if(eat(/ (?:last|previous|past) (?:season|year) |a (?:season|year) ago /))keepYear(LAST);
    if(eat(/ (?:this|current) (?:season|year) /)){
      const now=new Date().getFullYear();
      if(now>LAST)q.notes.push('The '+now+' season is not in the book yet, so this uses '+LAST+', the latest finished one.');
      keepYear(LAST);}
    while((m=t.match(/ (20\d\d|19\d\d) /))){keepYear(+m[1]); t=t.replace(m[0],' ');}
    if(eat(/ (?:career|all time|all-time|ever|of all time|in history|in league history|overall|all seasons|every season) /))q.career=true;
    /* a slice of games: which weeks, and in what situation. Read before "over" and
       "against" are taken as head-to-head words, because "scoring over 150" and "against
       winning teams" are conditions, not opponents. */
    const sl=q.sl, num=x=>W2N[x]||+x;
    if((m=eat(/ (?:in |during |for )?(?:weeks?|wks?|w) ?(\d{1,2}) ?(?:-|to|through|thru|and|until) ?(?:weeks? |wks? )?(\d{1,2}) /))){sl.from=Math.min(+m[1],+m[2]); sl.to=Math.max(+m[1],+m[2]);}
    if((m=eat(/ (?:the )?first (\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten) (?:weeks|games)(?: of (?:the |each |every )?(?:regular )?season)? /))){sl.from=1; sl.to=num(m[1]);}
    if((m=eat(/ (?:the )?(?:last|final) (\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten) (?:weeks|games)(?: of (?:the |each |every )?(?:regular )?season)? /)))sl.lastN=num(m[1]);
    if((m=eat(/ (?:after|from|since|beyond) (?:week|wk) ?(\d{1,2})(?: on| onward| onwards)? /)))sl.from=/ after | beyond /.test(m[0])?+m[1]+1:+m[1];
    if((m=eat(/ (?:before|through|thru|up to|until) (?:week|wk) ?(\d{1,2}) /)))sl.to=/ before /.test(m[0])?+m[1]-1:+m[1];
    if(eat(/ (?:opening week|week one|season opener|openers?) /)){sl.from=1; sl.to=1;}
    if(eat(/ (?:the )?(?:first|1st) half(?: of (?:the |each |every )?(?:regular )?season)? /))sl.half=1;
    if(eat(/ (?:the )?(?:second|2nd) half(?: of (?:the |each |every )?(?:regular )?season)? /))sl.half=2;
    if(eat(/ (?:early (?:in the )?season|early season|start of (?:the )?season|hot starts?|slow starts?|out of the gate) /)){sl.from=1; sl.to=4;}
    if(eat(/ (?:late (?:in the )?season|late season|down the stretch|stretch run|end of (?:the )?(?:regular )?season) /))sl.lastN=4;
    if((m=eat(/ (?:in |during )?(?:games )?(?:decided by|won by|lost by|by) (?:less than|under|fewer than|within) (\d{1,3})(?: points?)? /)))sl.close=+m[1];
    else if(eat(/ (?:in )?(?:close games?|close ones?|tight games?|one score games?|nail ?biters?|coin flips?) /))sl.close=10;
    if(eat(/ (?:in )?(?:blowouts|blowout games|lopsided games|blowout record) /))sl.blow=30;
    if((m=eat(/ (?:when |while |if |in games )?(?:scoring|scored|score|scores|putting up|putting|they put up|he puts up|with) (over|more than|above|at least|under|less than|below|fewer than) (\d{2,3})(?: points?)? /))){
      if(/over|more|above/.test(m[1]))sl.min=+m[2]+0.001; else if(m[1]==='at least')sl.min=+m[2]; else sl.max=+m[2];}
    else if((m=eat(/ (?:when |in games |games )?(?:scoring |with |putting up )?(\d{2,3}) ?(?:\+|plus|or more)(?: points?)? /)))sl.min=+m[1];
    else if((m=t.match(/ (\d{2,3})[ -]?(?:point|pt|pts) (games?|weeks?|outings?|performances?) /))){sl.min=+m[1]; t=t.replace(m[0],' '+m[2]+' ');}
    if((m=eat(/ (?:when |while |if )?(?:allowing|giving up|gave up|opponent scored|opponents score|against) (over|more than|above|under|less than|below) (\d{2,3})(?: points?)? /))){
      if(/over|more|above/.test(m[1]))sl.oppMin=+m[2]+0.001; else sl.oppMax=+m[2];}
    if(eat(/ (?:as an? |as |when )?(?:underdogs?|dogs?|projected to lose|projected lower|projected behind) /))sl.dog=true;
    else if(eat(/ (?:as an? |as |when )?(?:favou?rites?|projected to win|projected higher|projected ahead) /))sl.fav=true;
    if(eat(/ (?:vs|versus|v|against|facing|playing) (?:winning|good|over 500|over \.500|above 500|above \.500|winning record) (?:teams|managers|opponents|records?) /))sl.oppWin=true;
    else if(eat(/ (?:vs|versus|v|against|facing|playing) (?:losing|bad|under 500|under \.500|below 500|below \.500) (?:teams|managers|opponents) /))sl.oppWin=false;
    if(eat(/ (?:vs|versus|v|against|facing|playing) (?:playoff|postseason) (?:teams|managers|opponents) /))sl.oppPO=true;
    else if(eat(/ (?:vs|versus|v|against|facing|playing) (?:non playoff|non-playoff|missed playoff) (?:teams|managers|opponents) /))sl.oppPO=false;
    if(eat(/ (?:after|coming off|following) (?:a )?(?:loss|losses|defeat|l) |bounce ?back(?:s)? /))sl.prev='L';
    else if(eat(/ (?:after|coming off|following) (?:a )?(?:win|wins|victory|w) /))sl.prev='W';
    if(eat(/ (?:in wins|in his wins|when (?:they|he) won|in victories) /))sl.res='W';
    else if(eat(/ (?:in losses|in his losses|when (?:they|he) lost|in defeats) /))sl.res='L';
    if(eat(/ (?:by week|each week|week by week|per week|every week) /))q.split='wk';
    else if(eat(/ (?:by season|each season|every season|per season|season by season|year by year|by year|each year) /))q.split='y';
    /* weeks */
    while((m=t.match(/ (?:week|wk|w) ?(\d{1,2}) /))){q.weeks.push(+m[1]); t=t.replace(m[0],' ');}
    /* which games */
    if(eat(/ (?:the )?(?:final|championship game|title game|championship match|ship) /)){q.final=true; q.types='po';}
    if(eat(/ (?:playoffs|playoff|postseason|post season|bracket) /))q.types='po';
    if(eat(/ (?:regular season|reg season|regular) /))q.types=q.types==='po'?'all':'reg';
    /* what kind of question */
    if(/ (?:vs|versus|v|against|head to head|h2h|beat|beaten|over) /.test(t))q.h2h=true;
    {const ws=[...t.matchAll(/ (luckiest|unluckiest|most|least|fewest|best|worst|highest|lowest|top|bottom|biggest|smallest|largest|greatest|leader|leaders|leads|led|who|whos|which)(?= )/g)].map(x=>x[1]);
      const w=ws.find(x=>!/^(who|whos|which)$/.test(x))||ws[0];
      q.wantWord=ws.find(x=>!/^(who|whos|which)$/.test(x))||null;
      if(w)q.want=/^(least|fewest|lowest|bottom|smallest|unluckiest)$/.test(w)?'lo':w==='best'?'best':w==='worst'?'worst':'hi';}
    if(/ (?:single season|in a season|in one season|one season|season|year) /.test(t))q.per='season';
    if(/ (?:single game|in a game|in a week|one week|one game|scoring week|scoring game|matchup) /.test(t))q.per='game';
    /* the one-game measures first, so "closest game" is not read as "game" */
    for(const [k,g] of Object.entries(GAMEMET))for(const p of g.syn.slice().sort((a,b)=>b.length-a.length)){
      const re=new RegExp(' '+p.replace(/[.+]/g,'\\$&')+' ');
      if(re.test(t)&&(k!=='score'||q.want||q.per==='game')){q.game=q.game||k; t=t.replace(re,' ');}}
    for(const e of METW){const i=t.indexOf(' '+e.p+' '); if(i>=0){if(!q.metrics.includes(e.k))q.metrics.push(e.k); t=t.slice(0,i+1)+t.slice(i+1+e.p.length);}}
    /* "unluckiest" is luck, lowest first; "most consistent" is the smallest spread */
    if(/unlucki|unlucky/.test(q.said)&&q.metrics.includes('luck'))q.want='lo';
    else if(/luckiest/.test(q.said))q.want=q.want||'hi';
    if(q.metrics.includes('consistency')&&/consistent|steadiest/.test(q.said))q.want='best';
    if(q.metrics.includes('consistency')&&/volatil/.test(q.said))q.want='worst';
    if(q.metrics.includes('clutch')&&/least clutch/.test(q.said))q.want='lo';
    q.ignored=t.trim().split(' ').filter(w=>w&&!STOP.has(w)&&!/^\d+$/.test(w)&&w.length>1);
    return q;
  }

  /* ---------------------------------------------------------------- helpers for answers */
  const rowsFor=(name,yrs)=>(rowsOf[name]||[]).filter(r=>!yrs.length||yrs.includes(r.y));
  /* a manager's figures over a span of seasons, built the way the career record is */
  function span(name,yrs){
    const m=byName[name]; if(!yrs.length)return m;
    const rs=rowsFor(name,yrs); if(!rs.length)return null;
    const G=games(rs);
    return {name,seasons:rs.length,first:Math.min(...rs.map(r=>r.y)),last:Math.max(...rs.map(r=>r.y)),
      w:sumR(rs,'w'),l:sumR(rs,'l'),t:sumR(rs,'t'),g:G,winpct:(sumR(rs,'w')+sumR(rs,'t')/2)/G,
      titles:rs.filter(r=>r.place===1).reduce((s,r)=>s+r.share,0),podium:rs.filter(r=>r.place<=3).length,
      apps:rs.filter(r=>r.po).length,avgPlace:sumR(rs,'place')/rs.length,best:Math.min(...rs.map(r=>r.place)),
      pf:sumR(rs,'pf'),pa:sumR(rs,'pa'),ppg:sumR(rs,'pf')/G,luck:sumR(rs,'luck'),
      cpi:rs.reduce((s,r)=>s+r.pi*(r.w+r.l+r.t),0)/G,zAvg:rs.reduce((s,r)=>s+r.z*(r.w+r.l+r.t),0)/G,_rows:rs,_span:true};
  }
  /* playoff games, from the same list the head-to-head grid uses */
  const poGames=(name,yrs)=>POG.filter(g=>(g.ma===name||g.mb===name)&&(!yrs.length||yrs.includes(g.y)));
  const poLine=(name,yrs)=>{const gs=poGames(name,yrs); let w=0,l=0,pts=0;
    gs.forEach(g=>{const mine=g.ma===name?g.pa:g.pb, theirs=g.ma===name?g.pb:g.pa; pts+=mine; mine>theirs?w++:l++;});
    return {w,l,g:gs.length,ppg:gs.length?pts/gs.length:null};};
  const val=(k,o)=>{const d=MET[k]; if(!o)return null;
    if(o._span){if(!d.agg)return undefined; return d.agg(o._rows);} return d.car?d.car(o):undefined;};
  const show=(k,v,o)=>{const d=MET[k]; if(v==null)return '—'; return d.show?d.show(v,o):(d.fmt?d.fmt(v):String(v))+(d.unit||'');};
  const scopeLine=(yrs,types)=>{
    const s=yrs.length?(yrs.length===1?String(yrs[0]):yearList(yrs)):'all '+nOf(SEA.length,'season')+', '+SEA[0]+'–'+LAST;
    return s+(types==='po'?' · playoffs':types==='reg'?' · regular season':'');};
  const tbl=(head,rows)=>`<div class="scroll"><table class="ask-t">${head.some(Boolean)?`<thead><tr>${head.map((h,i)=>`<th${i?' class="num"':''}>${h}</th>`).join('')}</tr></thead>`:''}<tbody>${
    rows.map(r=>'<tr>'+r.map((c,i)=>`<td${i?' class="num"':''}>${c}</td>`).join('')+'</tr>').join('')}</tbody></table></div>`;
  const go=(label,run,primary)=>({label,run,primary:!!primary});
  /* where each measure lives on the page */
  const SECNAME={champions:'Champions',alltime:'the All-Time Table',power:'Power Index',luck:'the Luck Ledger',advanced:'Advanced',
    weekly:'Week by Week',seasons:'Seasons','trades-sec':'the Trade Market',records:'the Record Book',h2h:'Head to Head'};
  const toSection=id=>()=>{
    if(id==='records'){const w=$('#recsWrap'),t=$('#recsToggle'); if(w&&t&&!w.classList.contains('open')&&t.getAttribute('aria-expanded')!=='true')t.click();}
    const el=document.getElementById(id); if(el)el.scrollIntoView({behavior:'smooth'});};
  const secAct=id=>go('Go to '+(SECNAME[id]||id),toSection(id));
  const mgrAct=n=>go('Open '+n+'’s page',()=>openMgr(n),true);
  const seasonAct=y=>go('Go to the '+y+' season',()=>jumpSeason(y));
  const weekAct=(y,w)=>go('Go to week '+w+', '+y,()=>{
    if(typeof drawWeekly==='function')drawWeekly(y);
    const b=$('#wkSel button[data-w="'+w+'"]'); if(b)b.click();
    const el=$('#wkSel'); (el&&el.closest('.card')||$('#weekly')).scrollIntoView({behavior:'smooth'});},true);
  const h2hAct=(a,b)=>go('Open in Head to Head',()=>{
    const hidden=[a,b].filter(n=>!SEL.has(n));
    if(hidden.length)setSel([...SEL,...hidden]);
    /* the pickers are rebuilt on the redraw that follows a filter change */
    requestAnimationFrame(()=>requestAnimationFrame(()=>{
      const A=$('#cmpA'),B=$('#cmpB'); if(A&&B){A.value=a;B.value=b; if(A.onchange)A.onchange();}
      $('#h2h').scrollIntoView({behavior:'smooth'});}));},true);

  /* ---------------------------------------------------------------- answers */
  function answer(q){
    const out={kind:'',title:'',sub:'',body:'',acts:[],readAs:q.readAs||[],notes:q.notes.slice(),soon:q.soon.slice(),missing:q.missing.slice(),ignored:q.ignored.slice()};
    const yrs=q.years.slice().sort((a,b)=>a-b);
    if(q.amb&&!q.mgrs.length){out.kind='Which one?';out.title='“'+q.amb.word.replace(/^./,c=>c.toUpperCase())+'” is '+q.amb.options.length+' managers';
      out.choose=q.amb; return out;}
    if(q.players.length)return player(q,out);
    if(q.teams.length)return team(q,out,yrs);
    if(sliced(q))return ledger(q,out,yrs);
    if(q.mgrs.length>=2)return pair(q,out,yrs);
    if(q.mgrs.length===1&&q.h2h&&(q.want||/ who /.test(q.said))&&!q.metrics.length&&!q.game)return owners(q,out,yrs);
    if(q.weeks.length)return week(q,out,yrs);
    if(q.game)return gameBoard(q,out,yrs);
    if(yrs.length&&!q.mgrs.length&&q.metrics.length&&q.metrics.every(k=>k==='titles'))return season(q,out,yrs);
    if(q.mgrs.length===1)return one(q,out,yrs);
    if(q.metrics.length)return board(q,out,yrs);
    if(yrs.length)return season(q,out,yrs);
    if(q.soon.length||q.missing.length){out.kind='Not yet';out.title=q.soon.length?'That needs the Yahoo data':'Not in the book';return out;}
    out.kind='Ask the record book'; out.title='Try a manager, a season, a team, a week or a player';
    out.empty=true; return out;
  }

  /* one manager: a value, a few values, or the whole career */
  function one(q,out,yrs){
    const n=q.mgrs[0];
    if(q.types==='po'){
      const p=poLine(n,yrs);
      out.kind='Playoffs'; out.title=n+' in the playoffs';
      out.sub=scopeLine(yrs,'po')+' · '+nOf(p.g,'game');
      out.big=p.g?rec(p.w,p.l):'No playoff games';
      if(p.g)out.body=tbl(['','Value'],[['Record',rec(p.w,p.l)],['Points per game',F2(p.ppg)],['Titles',titleTxt(val('titles',span(n,yrs)))],['Appearances',String(val('apps',span(n,yrs)))]]);
      out.acts=[mgrAct(n),secAct('advanced')]; return out;}
    if(yrs.length===1){
      const r=(rowsOf[n]||[]).find(x=>x.y===yrs[0]);
      if(!r){out.kind=String(yrs[0]); out.title=n+' did not play in '+yrs[0];
        out.sub='Seasons: '+yearList((rowsOf[n]||[]).map(x=>x.y)); out.acts=[mgrAct(n)]; return out;}
      const ks=q.metrics.length?q.metrics:['record','finish','ppg','pi','luck','seed'];
      out.kind=r.y+' season'; out.title=n+' in '+r.y; out.sub=r.team+' · '+(r.place===1?(r.co?'Co-champion':'Champion'):ord(r.place)+' of '+r.teams);
      out.body=tbl(['','Value'],ks.filter(k=>MET[k].row).map(k=>{const d=MET[k];
        return [d.lab,k==='record'?rec(r.w,r.l,r.t):d.rowTxt?d.rowTxt(r):(d.fmt?d.fmt(d.row(r)):d.row(r))+(d.unit||'')];}));
      const skip=ks.filter(k=>!MET[k].row); if(skip.length)out.notes.push(skip.map(k=>MET[k].lab).join(', ')+' is a career figure, not a one-season one.');
      out.acts=[seasonAct(r.y),mgrAct(n)]; return out;}
    if(q.split==='y'){
      const rs=rowsFor(n,yrs).slice().sort((a,b)=>a.y-b.y);
      out.kind='Season by season'; out.title=n; out.sub=nOf(rs.length,'season')+(yrs.length?' · '+scopeLine(yrs):'');
      out.body=tbl(['Season','Team','Record','Finish','PPG','Power idx','Luck'],rs.map(r=>[String(r.y),esc(r.team),rec(r.w,r.l,r.t),
        r.place===1?(r.co?'Co-champ':'Champion'):ord(r.place),F2(r.ppg),F1(r.pi),sg(r.luck,2)]));
      out.acts=[mgrAct(n)]; return out;}
    const o=span(n,yrs);
    if(!o){out.kind='Not found'; out.title=n+' did not play in '+yearList(yrs); out.acts=[mgrAct(n)]; return out;}
    const ks=q.metrics.length?q.metrics:null;
    out.kind=yrs.length?yearList(yrs):'Career'; out.title=n;
    out.sub=nOf(o.seasons,'season')+', '+o.first+'–'+o.last+(yrs.length?' · within '+scopeLine(yrs):'');
    if(ks){
      const rows=ks.map(k=>{const v=val(k,o); return v===undefined?[MET[k].lab,'<span class="dim">not for a span of seasons</span>']:[MET[k].lab,show(k,v,o)];});
      if(ks.length===1&&val(ks[0],o)!=null&&val(ks[0],o)!==undefined){out.big=show(ks[0],val(ks[0],o),o);
        if(MET[ks[0]].rate||ks[0]==='luck'){const pool=careerPool(ks[0],yrs);
          const rank=rankOf(pool,n,ks[0]); if(rank)out.sub+=' · '+rank;}}
      out.body=tbl(['','Value'],rows);
      out.acts=[mgrAct(n),secAct(MET[ks[0]].sec)];
    }else{
      out.big=(o.titles?titleTxt(o.titles)+(o.titles===1?' title':' titles')+' · ':'')+rec(o.w,o.l,o.t);
      const p=poLine(n,yrs);
      out.body=tbl(['','Value'],[['Win %',pct(o.winpct)],['Points per game',F2(o.ppg)],['Power index',F1(o.cpi)],['Luck',sg(o.luck,2)+' wins'],
        ['Podium finishes',String(o.podium)],['Playoff appearances',String(o.apps)],['Playoff record',p.g?rec(p.w,p.l):'—'],
        ['Average finish',F2(o.avgPlace)],['Best finish',o.best===1?'Champion':ord(o.best)]]);
      out.acts=[mgrAct(n),secAct('alltime')];
    }
    return out;
  }
  function careerPool(k,yrs){
    return M.map(m=>span(m.name,yrs)).filter(o=>o&&val(k,o)!=null&&val(k,o)!==undefined&&(!MET[k].rate||o.seasons>=2));}
  function rankOf(pool,name,k){
    const d=MET[k], v=o=>val(k,o);
    const s=pool.slice().sort((a,b)=>d.hi===0?v(a)-v(b):v(b)-v(a)); const i=s.findIndex(o=>o.name===name);
    return i<0?'':ord(i+1)+' of '+s.length+(d.rate?' with 2+ seasons':'');}

  /* a leader board: career, or one season at a time */
  function board(q,out,yrs){
    const k=q.metrics[0], d=MET[k];
    let dir=d.hi===null?1:d.hi;                         /* 1: biggest first */
    if(q.want==='hi')dir=1; else if(q.want==='lo')dir=0; else if(q.want==='worst')dir=d.hi===0?1:0; else if(q.want==='best')dir=d.hi===0?0:1;
    const perSeason=!!d.row&&(q.per==='season'||!d.car||yrs.length===1);
    const sorter=(a,b,f)=>dir?f(b)-f(a):f(a)-f(b);
    out.kind=(perSeason?'Single season':'Career')+' · '+d.lab;
    if(perSeason){
      const pool=ROWS.filter(r=>(!yrs.length||yrs.includes(r.y))&&d.row(r)!=null);
      const top=pool.slice().sort((a,b)=>sorter(a,b,d.row)).slice(0,5);
      const lead=top[0];
      if(!lead){out.title='Nothing to rank'; return out;}
      out.title=lead.mgr+', '+lead.y;
      out.big=lead?(k==='record'?rec(lead.w,lead.l,lead.t):(d.fmt?d.fmt(d.row(lead)):d.row(lead))+(d.unit||'')):'';
      out.sub=(dir?'Highest ':'Lowest ')+d.lab.toLowerCase()+' in a season · '+scopeLine(yrs)+' · '+lead.team;
      out.body=tbl(['','Manager','Team','Year',d.lab],top.map((r,i)=>[String(i+1),mlink(r.mgr),esc(r.team),String(r.y),
        k==='record'?rec(r.w,r.l,r.t):(d.fmt?d.fmt(d.row(r)):d.row(r))+(d.unit||'')]));
      out.acts=[seasonAct(lead.y),mgrAct(lead.mgr),secAct(d.sec)];
      return out;}
    const pool=careerPool(k,yrs);
    const top=pool.slice().sort((a,b)=>sorter(a,b,o=>val(k,o))).slice(0,5);
    const lead=top[0];
    if(!lead){out.title='Nothing to rank'; return out;}
    const tied=pool.filter(o=>val(k,o)===val(k,lead));
    out.title=tied.length>1?tied.map(o=>o.name).join(' and '):lead.name;
    out.big=show(k,val(k,lead),lead);
    out.sub=(tied.length>1?'Tied · ':'')+scopeLine(yrs)+(d.rate?' · managers with 2+ seasons':'');
    out.body=tbl(['','Manager','Seasons',d.lab],top.map((o,i)=>[String(i+1),mlink(o.name),String(o.seasons),show(k,val(k,o),o)]));
    out.acts=[mgrAct(lead.name),secAct(d.sec)];
    return out;
  }

  /* one-game records: highest score, biggest blowout, closest game */
  function gameBoard(q,out,yrs){
    const g=GAMEMET[q.game];
    let list=(q.types==='po'?[]:REGG).concat(q.types==='reg'?[]:POG).filter(x=>!yrs.length||yrs.includes(x.y));
    if(q.final)list=POG.filter(x=>/final/i.test(x.lab)&&!/semi|quarter/i.test(x.lab)&&(!yrs.length||yrs.includes(x.y)));
    let dir=g.hi; if(q.want==='lo')dir=q.game==='score'?0:dir; if(q.want==='hi'||q.want==='best')dir=q.game==='close'?0:1; if(q.want==='worst'&&q.game==='score')dir=0;
    let rows;
    if(q.game==='score'){
      rows=[]; list.forEach(x=>{rows.push({y:x.y,lab:x.lab,who:x.ma,opp:x.mb,v:x.pa,o:x.pb}); rows.push({y:x.y,lab:x.lab,who:x.mb,opp:x.ma,v:x.pb,o:x.pa});});
      rows.sort((a,b)=>dir?b.v-a.v:a.v-b.v);
    }else{
      rows=list.map(x=>{const aw=x.pa>x.pb; return {y:x.y,lab:x.lab,who:aw?x.ma:x.mb,opp:aw?x.mb:x.ma,v:Math.abs(x.pa-x.pb),hi:Math.max(x.pa,x.pb),lo:Math.min(x.pa,x.pb)};});
      rows.sort((a,b)=>q.game==='close'||!dir?a.v-b.v:b.v-a.v);
    }
    if(q.mgrs.length===1){const n=q.mgrs[0]; rows=rows.filter(r=>q.game==='score'?r.who===n:(r.who===n||r.opp===n));}
    const top=rows.slice(0,5), lead=top[0];
    out.kind=(q.mgrs.length===1?q.mgrs[0]+' · ':'')+'One game · '+(q.game==='score'?(dir?'Highest score':'Lowest score'):g.lab);
    if(!lead){out.title='No games in that range'; return out;}
    out.title=lead.who+(q.game==='score'?'':' over '+lead.opp);
    out.big=q.game==='score'?F2(lead.v):F2(lead.v)+' points';
    out.sub=lead.lab+(q.game==='score'?' · against '+lead.opp+' ('+F2(lead.o)+')':' · '+F2(lead.hi)+'–'+F2(lead.lo));
    out.body=tbl(['','Manager','Game',q.game==='score'?'Points':'Margin'],top.map((r,i)=>[String(i+1),mlink(r.who),
      esc(r.lab)+' <span class="dim">v '+esc(r.opp)+'</span>',F2(r.v)]));
    out.notes.push('Covers every playoff game since '+SEA[0]+(q.types==='po'?'':' and the regular seasons with a game log ('+yearList(D.wkYears||[])+')')+'.');
    const wk=lead.lab.match(/^(\d{4}) week (\d+)$/);
    out.acts=[wk?weekAct(+wk[1],+wk[2]):seasonAct(lead.y),mgrAct(lead.who)];
    return out;
  }

  /* two or more managers: head to head, or side by side */
  function pair(q,out,yrs){
    const [a,b]=q.mgrs;
    if(q.metrics.includes('trades')){
      const deals=D.trade.log.filter(x=>((x.ma===a&&x.mb===b)||(x.ma===b&&x.mb===a))&&(!yrs.length||yrs.includes(x.y)));
      out.kind='Trades'; out.title=a+' and '+b; out.big=nOf(deals.length,'trade');
      out.sub=yearList(D.trade.years||[])+', the seasons with transaction logs';
      if(deals.length)out.body=tbl(['When','Deal'],deals.map(x=>[x.d+' '+x.y,dealTxt(x)]));
      out.acts=[secAct('trades-sec')]; return out;}
    if(q.metrics.length||q.mgrs.length>2){
      const ks=q.metrics.length?q.metrics:['titles','record','ppg','pi','luck','finish'];
      const os=q.mgrs.map(n=>span(n,yrs));
      out.kind='Side by side'; out.title=q.mgrs.join(' vs '); out.sub=scopeLine(yrs);
      out.body=tbl(['',...q.mgrs.map(n=>esc(n.split(' ').slice(-1)[0]))],ks.map(k=>[MET[k].lab,...os.map(o=>{
        if(!o)return '<span class="dim">did not play</span>'; const v=val(k,o); return v===undefined?'—':show(k,v,o);})]));
      out.acts=[h2hAct(a,b)]; return out;}
    const key=q.types==='po'?'po':q.types==='reg'?'reg':'all';
    const games=MX[key].g.filter(g=>((g.ma===a&&g.mb===b)||(g.ma===b&&g.mb===a))&&(!yrs.length||yrs.includes(g.y)));
    let w=0,l=0; games.forEach(g=>{const win=g.pa>g.pb?g.ma:g.mb; win===a?w++:l++;});
    out.kind='Head to head · '+(key==='po'?'playoffs':key==='reg'?'regular season':'every game on record');
    out.title=a+' vs '+b;
    if(!games.length){out.big='Never met'; out.sub='No game between them on record'+(yrs.length?' in '+yearList(yrs):'')+'.';
      out.notes.push('Regular-season games are on record for '+yearList(D.wkYears||[])+'; playoff games for every season.'); out.acts=[h2hAct(a,b)]; return out;}
    out.big=rec(w,l); out.sub=(w>l?a+' leads':w<l?b+' leads':'Dead even')+' · '+nOf(games.length,'game')+(yrs.length?' · '+yearList(yrs):'');
    const last=games.slice().sort((x,y)=>y.y-x.y||(y.wk||0)-(x.wk||0)).slice(0,6);
    out.body=tbl(['Game','Winner','Score'],last.map(g=>{const aw=g.pa>g.pb;
      return [esc(g.lab),esc((aw?g.ma:g.mb).split(' ').slice(-1)[0]),F2(Math.max(g.pa,g.pb))+'–'+F2(Math.min(g.pa,g.pb))];}));
    if(games.length>6)out.notes.push('The six most recent of '+games.length+' meetings.');
    if(key!=='po')out.notes.push('Regular-season games are on record for '+yearList(D.wkYears||[])+'; playoff games for every season.');
    out.acts=[h2hAct(a,b),mgrAct(a)]; return out;
  }
  /* "who owns Kaiper": everybody's record against one manager, best first */
  function owners(q,out,yrs){
    const n=q.mgrs[0], key=q.types==='po'?'po':q.types==='reg'?'reg':'all';
    const lo=q.want==='lo'||q.want==='worst';
    const vs={};
    MX[key].g.filter(g=>(g.ma===n||g.mb===n)&&(!yrs.length||yrs.includes(g.y))).forEach(g=>{
      const o=g.ma===n?g.mb:g.ma, oWon=(g.ma===o)===(g.pa>g.pb);
      const r=vs[o]=vs[o]||{name:o,w:0,l:0}; oWon?r.w++:r.l++;});
    const list=Object.values(vs).filter(r=>r.w+r.l>=3);
    list.sort((a,b)=>{const pa=a.w/(a.w+a.l),pb=b.w/(b.w+b.l); return lo?pa-pb||b.l-a.l:pb-pa||b.w-a.w;});
    out.kind='Head to head · against '+n;
    if(!list.length){out.title='Nobody has played '+n+' three times'; out.acts=[mgrAct(n)]; return out;}
    const top=list[0];
    out.title=lo?n+' owns '+top.name:top.name+' owns '+n;
    out.big=rec(top.w,top.l); out.sub=(lo?'The worst record against '+n:'The best record against '+n)+' · 3+ meetings · '+scopeLine(yrs,q.types);
    out.body=tbl(['','Manager','Record v '+esc(n.split(' ').slice(-1)[0]),'Win %'],list.slice(0,6).map((r,i)=>[String(i+1),mlink(r.name),rec(r.w,r.l),pct(r.w/(r.w+r.l))]));
    if(key!=='po')out.notes.push('Regular-season games are on record for '+yearList(D.wkYears||[])+'; playoff games for every season.');
    out.acts=[h2hAct(top.name,n),mgrAct(n)]; return out;
  }
  /* ================================================ the game log: one row per team per game
     Every regular-season game in the seasons with a log (both scores, both Yahoo projections,
     how many of the league that team outscored that week) and every playoff game since the
     start. The same games the head-to-head grid counts, so a record here agrees with it. */
  let GLC=null;
  function games1(){
    if(GLC)return GLC;
    const rows=[], rowOf={}; ROWS.forEach(r=>{rowOf[r.y+'|'+r.mgr]=r;});
    (D.wkYears||[]).forEach(y=>{const K=D.wk[y];
      const reg=K.games.filter(g=>g.br===''), last=Math.max(...reg.map(g=>g.wk));
      reg.forEach(g=>[[g.ta,g.aa,g.pa,g.tb,g.ab,g.pb],[g.tb,g.ab,g.pb,g.ta,g.aa,g.pa]].forEach(([t,p,pr,o,op,opr])=>{
        const ra=((K.race||{})[t]||[]).find(x=>x.w===g.wk);
        rows.push({y,wk:g.wk,last,team:t,mgr:K.mgr[t],opp:o,oppMgr:K.mgr[o],pts:p,opts:op,proj:pr,oproj:opr,po:false,
          ap:ra?ra.ap:null,apN:K.teams.length-1});}));});
    D.games.filter(g=>!g.void).forEach(g=>[[g.ta,g.ma,g.pa,g.tb,g.mb,g.pb],[g.tb,g.mb,g.pb,g.ta,g.ma,g.pa]].forEach(([t,mg,p,o,om,op])=>
      rows.push({y:g.y,wk:g.wk,team:t,mgr:mg,opp:o,oppMgr:om,pts:p,opts:op,proj:null,oproj:null,po:true,rnd:g.rnd})));
    /* what came the week before, and how good the opponent was that season */
    const run={}; rows.filter(r=>!r.po).forEach(r=>(run[r.y+'|'+r.mgr]=run[r.y+'|'+r.mgr]||[]).push(r));
    Object.values(run).forEach(a=>{a.sort((x,z)=>x.wk-z.wk); a.forEach((r,i)=>{r.prev=i?(a[i-1].pts>a[i-1].opts?'W':'L'):null;});});
    rows.forEach(r=>{const o=rowOf[r.y+'|'+r.oppMgr]; r.oppPct=o?(o.w+o.t/2)/o.g:null; r.oppPO=o?o.po:null;
      r.win=r.pts>r.opts; r.tie=r.pts===r.opts;});
    return GLC=rows;
  }
  const WEEKISH=s=>s.from!=null||s.to!=null||s.lastN||s.half||s.prev||s.dog||s.fav;
  function sliced(q){const s=q.sl;
    if(Object.keys(s).length||q.metrics.some(k=>k==='beatproj'||k==='vsproj')||(q.game==='upset'))return true;
    if(q.split==='wk'&&q.mgrs.length)return true;
    /* "Wu record in week 1": one week, asked about a measure rather than the scoreboard */
    if(q.weeks.length&&q.metrics.some(k=>['record','wins','losses','winpct','ppg','pa','allplay','luck'].includes(k))&&(q.mgrs.length||q.want)){
      s.from=Math.min(...q.weeks); s.to=Math.max(...q.weeks); q.weeks=[]; return true;}
    return false;}
  /* which games: a week-based question means the regular season (playoff weeks are not
     "week 3"), a projection only exists in the regular season, otherwise every game */
  const gameSet=q=>q.types||(WEEKISH(q.sl)||q.split==='wk'||q.metrics.some(k=>k==='beatproj'||k==='vsproj')||q.game==='upset'?'reg':'all');
  function inSlice(r,q,yrs,set){const s=q.sl;
    if(yrs.length&&!yrs.includes(r.y))return false;
    if(set==='reg'&&r.po)return false; if(set==='po'&&!r.po)return false;
    if(s.from!=null&&r.wk<s.from)return false; if(s.to!=null&&r.wk>s.to)return false;
    if(s.lastN&&(r.po||r.wk<=r.last-s.lastN))return false;
    if(s.half){if(r.po)return false; const mid=Math.ceil(r.last/2); if(s.half===1?r.wk>mid:r.wk<=mid)return false;}
    if(s.close!=null&&Math.abs(r.pts-r.opts)>=s.close)return false;
    if(s.blow!=null&&Math.abs(r.pts-r.opts)<s.blow)return false;
    if(s.min!=null&&r.pts<s.min)return false; if(s.max!=null&&r.pts>=s.max)return false;
    if(s.oppMin!=null&&r.opts<s.oppMin)return false; if(s.oppMax!=null&&r.opts>=s.oppMax)return false;
    if(s.dog&&!(r.proj!=null&&r.proj<r.oproj))return false; if(s.fav&&!(r.proj!=null&&r.proj>r.oproj))return false;
    if(s.oppWin===true&&!(r.oppPct>.5))return false; if(s.oppWin===false&&!(r.oppPct<.5))return false;
    if(s.oppPO===true&&!r.oppPO)return false; if(s.oppPO===false&&r.oppPO!==false)return false;
    if(s.prev&&r.prev!==s.prev)return false;
    if(s.res==='W'&&!r.win)return false; if(s.res==='L'&&(r.win||r.tie))return false;
    return true;}
  function tot(rs){let w=0,l=0,t=0,pts=0,opp=0,exp=0,expG=0,expW=0,bp=0,bpN=0,vp=0,hi=-Infinity,lo=Infinity;
    rs.forEach(r=>{r.tie?t++:r.win?w++:l++; pts+=r.pts; opp+=r.opts; if(r.pts>hi)hi=r.pts; if(r.pts<lo)lo=r.pts;
      if(r.ap!=null){exp+=r.ap/r.apN; expG++; expW+=r.tie?.5:r.win?1:0;}
      if(r.proj!=null){bpN++; vp+=r.pts-r.proj; if(r.pts>r.proj)bp++;}});
    const g=rs.length;
    return {g,w,l,t,pct:g?(w+t/2)/g:null,ppg:g?pts/g:null,papg:g?opp/g:null,margin:g?(pts-opp)/g:null,
      ap:expG?exp/expG:null,luck:expG?expW-exp:null,bp:bpN?bp/bpN:null,bpN,vp:bpN?vp/bpN:null,hi:g?hi:null,lo:g?lo:null};}
  /* the measure a slice is about, and how it is shown */
  const LM={pct:{lab:'Record',v:x=>x.pct,s:x=>rec(x.w,x.l,x.t)+' <span class="dim">'+pct(x.pct)+'</span>'},
    ppg:{lab:'Points per game',v:x=>x.ppg,s:x=>F2(x.ppg)},
    papg:{lab:'Points against per game',v:x=>x.papg,s:x=>F2(x.papg),lo:1},
    ap:{lab:'All-play',v:x=>x.ap,s:x=>pct(x.ap)},
    luck:{lab:'Luck',v:x=>x.luck,s:x=>sg(x.luck,2)+' wins'},
    bp:{lab:'Beat the projection',top:['Beat the projection most often','Beat the projection least often'],v:x=>x.bp,s:x=>pct(x.bp)+' <span class="dim">of '+x.bpN+'</span>'},
    vp:{lab:'Points vs projection',top:['Most points over projection','Furthest under projection'],v:x=>x.vp,s:x=>sg(x.vp,2)+' a game'},
    margin:{lab:'Point differential',v:x=>x.margin,s:x=>sg(x.margin,2)+' a game'},
    wins:{lab:'Wins',v:x=>x.w,s:x=>nOf(x.w,'win')+' <span class="dim">'+rec(x.w,x.l,x.t)+'</span>'},
    losses:{lab:'Losses',v:x=>x.l,s:x=>nOf(x.l,'loss').replace('losss','losses')+' <span class="dim">'+rec(x.w,x.l,x.t)+'</span>'},
    n:{lab:'Games',v:x=>x.g,s:x=>nOf(x.g,'game')}};
  /* "how many", "how often" and "most ..." questions about a slice are counts; otherwise the
     measure named, and a record when none is */
  const lmOf=q=>{const k=q.metrics.find(k=>['ppg','pf','pa','allplay','luck','beatproj','vsproj','diff','wins','losses'].includes(k));
    const counting=/ (?:how many|how often|number of|count) /.test(q.said)||(/^(most|least|fewest)$/.test(q.wantWord||'')&&!q.metrics.length&&/ (?:games|times|weeks) /.test(q.said));
    if(k==='wins'||k==='losses')return q.want||counting?k:'pct';
    if(!k&&counting)return 'n';
    return {ppg:'ppg',pf:'ppg',pa:'papg',allplay:'ap',luck:'luck',beatproj:'bp',vsproj:'vp',diff:'margin'}[k]||'pct';};
  /* the slice, said in words */
  function sliceLine(q,set){const s=q.sl, bits=[];
    if(s.from!=null||s.to!=null)bits.push(s.from===s.to?'Week '+s.from:s.from!=null&&s.to!=null?'Weeks '+s.from+'–'+s.to:s.from!=null?'Week '+s.from+' on':'Through week '+s.to);
    if(s.lastN)bits.push('Last '+nOf(s.lastN,'week')+' of the regular season');
    if(s.half)bits.push((s.half===1?'First':'Second')+' half of the regular season');
    if(s.close!=null)bits.push('Games decided by under '+s.close);
    if(s.blow!=null)bits.push('Blowouts (by '+s.blow+'+)');
    if(s.min!=null)bits.push('Scoring '+(s.min%1?'over '+Math.floor(s.min):s.min+'+'));
    if(s.max!=null)bits.push('Scoring under '+s.max);
    if(s.oppMin!=null)bits.push('Allowing over '+Math.floor(s.oppMin));
    if(s.oppMax!=null)bits.push('Allowing under '+s.oppMax);
    if(s.dog)bits.push('Projected to lose'); if(s.fav)bits.push('Projected to win');
    if(s.oppWin===true)bits.push('Against winning teams'); if(s.oppWin===false)bits.push('Against losing teams');
    if(s.oppPO===true)bits.push('Against playoff teams'); if(s.oppPO===false)bits.push('Against non-playoff teams');
    if(s.prev)bits.push('After a '+(s.prev==='L'?'loss':'win'));
    if(s.res)bits.push(s.res==='W'?'In wins':'In losses');
    if(!bits.length)return set==='reg'?'Every regular-season game':set==='po'?'Every playoff game':'Every game';
    bits.push(set==='reg'?'regular season':set==='po'?'playoffs':'all games');
    return bits.join(' · ');}
  const MINGAMES=4;

  function ledger(q,out,yrs){
    const set=gameSet(q), all=games1(), lm=LM[lmOf(q)];
    const pool=all.filter(r=>inSlice(r,q,yrs,set));
    if(q.game)return sliceGames(q,out,pool,set);
    const seasonsCovered=[...new Set(all.filter(r=>!r.po).map(r=>r.y))];
    out.kind=sliceLine(q,set);
    if(set!=='po'&&(!yrs.length||yrs.some(y=>!seasonsCovered.includes(y))))
      out.notes.push('Week-by-week games are on record for '+yearList(seasonsCovered)+'; earlier seasons have season totals only'+(set==='all'?', so they count playoff games alone.':'.'));
    if(q.metrics.includes('beatproj')||q.sl.dog||q.sl.fav)out.notes.push('Projections are Yahoo’s own, taken before each game.');
    /* everybody, for ranks and leader boards */
    const byM={}; pool.forEach(r=>(byM[r.mgr]=byM[r.mgr]||[]).push(r));
    const table=Object.entries(byM).map(([n,rs])=>({n,x:tot(rs)})).filter(o=>lm.v(o.x)!=null);
    const order=(a,b)=>{const d=lm.v(b.x)-lm.v(a.x); return (lm.lo?-d:d)||b.x.g-a.x.g;};
    const ranked=table.filter(o=>o.x.g>=MINGAMES).sort(order);
    if(q.mgrs.length>=2){
      const [a,b]=q.mgrs, rs=pool.filter(r=>r.mgr===a&&r.oppMgr===b), x=tot(rs);
      out.title=a+' vs '+b; out.big=x.g?rec(x.w,x.l,x.t):'Never met in that slice';
      out.sub=nOf(x.g,'game')+(x.g?' · '+a.split(' ').slice(-1)[0]+' scored '+F2(x.ppg)+' a game, '+b.split(' ').slice(-1)[0]+' '+F2(x.papg):'');
      if(x.g)out.body=tbl(['Game','Winner','Score'],rs.slice().sort((r,z)=>z.y-r.y||z.wk-r.wk).slice(0,8).map(r=>[r.y+(r.po?' '+esc(r.rnd||'playoffs'):' week '+r.wk),
        esc((r.win?a:b).split(' ').slice(-1)[0]),F2(Math.max(r.pts,r.opts))+'–'+F2(Math.min(r.pts,r.opts))]));
      out.acts=[h2hAct(a,b)]; return out;}
    if(q.mgrs.length===1&&q.h2h&&(q.want||/ who /.test(q.said))&&lm===LM.pct){
      const n=q.mgrs[0], vs={};
      pool.filter(r=>r.oppMgr===n).forEach(r=>(vs[r.mgr]=vs[r.mgr]||[]).push(r));
      const lo=q.want==='lo'||q.want==='worst';
      const list=Object.entries(vs).map(([o,rs])=>({n:o,x:tot(rs)})).filter(o=>o.x.g>=2)
        .sort((a,b)=>lo?a.x.pct-b.x.pct||b.x.l-a.x.l:b.x.pct-a.x.pct||b.x.w-a.x.w);
      out.title=list.length?(lo?n+' owns '+list[0].n:list[0].n+' owns '+n):'Too few games against '+n+' in that slice';
      if(list.length){out.big=rec(list[0].x.w,list[0].x.l,list[0].x.t); out.sub='Record against '+n+' · 2+ meetings in the slice';
        out.body=tbl(['','Manager','Record v '+esc(n.split(' ').slice(-1)[0]),'Win %'],list.slice(0,6).map((o,i)=>[String(i+1),mlink(o.n),rec(o.x.w,o.x.l,o.x.t),pct(o.x.pct)]));
        out.acts=[h2hAct(list[0].n,n),mgrAct(n)];}
      return out;}
    if(q.mgrs.length===1){
      const n=q.mgrs[0], mine=pool.filter(r=>r.mgr===n), x=tot(mine);
      out.title=n;
      if(!x.g){out.big='No games'; out.sub='Nothing on record for '+n+' in that slice.'; out.acts=[mgrAct(n)]; return out;}
      out.big=lm.s(x);
      const sz=[...new Set(mine.map(r=>r.y))].sort((a,b)=>a-b);
      out.sub=nOf(x.g,'game')+' · '+F2(x.ppg)+' points a game · '+(sz.length===1?sz[0]:yearList(sz));
      /* the layer underneath: the same seasons with this slice taken out */
      const rest=all.filter(r=>r.mgr===n&&sz.includes(r.y)&&(set==='all'||(set==='po')===r.po)&&!inSlice(r,q,yrs,set)), xr=tot(rest);
      const i=ranked.findIndex(o=>o.n===n);
      const ctx=[];
      if(xr.g)ctx.push([set==='all'?'His other games':'The rest of those seasons',lm===LM.n?nOf(xr.g,'game'):lm.s(xr)+' <span class="dim">'+nOf(xr.g,'game')+'</span>']);
      if(lm===LM.n&&x.g+xr.g)out.big=x.g+' of '+(x.g+xr.g)+' <span class="dim">'+pct(x.g/(x.g+xr.g))+' of his games</span>';
      if(i>=0)ctx.push(['League rank in this slice',ord(i+1)+' of '+ranked.length+' <span class="dim">'+MINGAMES+'+ games</span>']);
      const lg=tot(pool); if(lmOf(q)!=='pct'&&lg.g)ctx.push(['League average in this slice',lm.s(lg)]);
      if(q.split==='wk'){
        const wks=[...new Set(mine.map(r=>r.wk))].sort((a,b)=>a-b);
        out.body=tbl(['Week','Record','PPG',...(lm===LM.pct?[]:[lm.lab])],wks.map(w=>{const t=tot(mine.filter(r=>r.wk===w)); return ['Week '+w,rec(t.w,t.l,t.t),F2(t.ppg),...(lm===LM.pct?[]:[lm.s(t)])];}));
      }else{
        out.body=tbl(['Season','Record','PPG',lm===LM.pct?(set==='all'?'Other games':'Rest of season'):lm.lab],sz.map(y=>{
          const t=tot(mine.filter(r=>r.y===y)), rr=tot(rest.filter(r=>r.y===y));
          return [String(y),rec(t.w,t.l,t.t),F2(t.ppg),lm===LM.pct?(rr.g?rec(rr.w,rr.l,rr.t):'—'):lm.s(t)];}));
      }
      if(ctx.length)out.body+=tbl(['',''],ctx);
      out.acts=[mgrAct(n),secAct('weekly')];
      if(q.sl.from!=null&&q.sl.from===q.sl.to&&sz.length===1)out.acts.unshift(weekAct(sz[0],q.sl.from));
      return out;}
    /* nobody named: who is best (or worst) in this slice */
    const lo=q.want==='lo'||q.want==='worst';
    const list=lo?ranked.slice().reverse():ranked;
    out.title=list.length?list[0].n:'Nobody has '+MINGAMES+' games in that slice';
    const many=lm===LM.n||lm===LM.wins||lm===LM.losses;
    if(list.length){out.big=lm.s(list[0].x); out.sub=(lm.top?lm.top[lo?1:0]:(many?(lo?'Fewest ':'Most '):(lo?'Worst ':'Best '))+lm.lab.toLowerCase())+' · managers with '+MINGAMES+'+ games · '+nOf(pool.length,'team-game')+' in the slice';
      out.body=tbl(['','Manager','Games',lm.lab],list.slice(0,8).map((o,i)=>[String(i+1),mlink(o.n),String(o.x.g),lm.s(o.x)]));
      out.acts=[mgrAct(list[0].n),secAct('weekly')];}
    return out;
  }

  /* the biggest score, blowout, closest game or upset inside a slice */
  function sliceGames(q,out,pool,set){
    let rs=q.mgrs.length===1?pool.filter(r=>r.mgr===q.mgrs[0]):pool;
    const lo=q.want==='lo'||(q.want==='worst'&&q.game==='score');
    let val, lab;
    if(q.game==='score'){val=r=>r.pts; lab='Points';}
    else{rs=rs.filter(r=>r.win||(q.mgrs.length===1&&q.game==='close'));
      if(q.game==='upset'){rs=rs.filter(r=>r.win&&r.proj!=null&&r.proj<r.oproj); val=r=>r.oproj-r.proj; lab='Projected behind by';}
      else{val=r=>Math.abs(r.pts-r.opts); lab='Margin';}}
    const hiFirst=q.game==='close'?false:!lo;
    const top=rs.slice().sort((a,b)=>hiFirst?val(b)-val(a):val(a)-val(b)).slice(0,6), lead=top[0];
    out.kind=(q.mgrs.length===1?q.mgrs[0]+' · ':'')+(q.game==='score'?(lo?'Lowest score':'Highest score'):GAMEMET[q.game].lab)+' · '+sliceLine(q,set);
    if(!lead){out.title='No games in that slice'; return out;}
    const when=r=>r.y+(r.po?' '+(r.rnd||'playoffs'):' week '+r.wk);
    out.title=q.game==='score'?lead.mgr:(lead.win?lead.mgr+' over '+lead.oppMgr:lead.oppMgr+' over '+lead.mgr);
    out.big=F2(val(lead))+(q.game==='score'?'':' points');
    out.sub=when(lead)+' · '+F2(lead.pts)+'–'+F2(lead.opts)+(q.game==='upset'?' · projected '+F2(lead.proj)+' to '+F2(lead.oproj):'');
    out.body=tbl(['','Manager','Game',lab],top.map((r,i)=>[String(i+1),mlink(r.mgr),esc(when(r))+' <span class="dim">v '+esc(r.oppMgr)+'</span>',F2(val(r))]));
    const w=!lead.po&&lead.wk; out.acts=[w?weekAct(lead.y,w):seasonAct(lead.y),mgrAct(lead.mgr)];
    return out;
  }

  const dealTxt=x=>esc(x.ma)+' sent '+esc(x.pa.join(', '))+' to '+esc(x.mb)+' for '+esc(x.pb.join(', '));

  /* a season */
  function season(q,out,yrs){
    if(yrs.length>1){
      out.kind='Champions'; out.title=yearList(yrs);
      out.body=tbl(['Year','Champion','Team'],yrs.map(y=>{const c=D.champs.find(x=>x.y===y)||{};
        return [String(y),(c.mgrs||[]).map(mlink).join(' &amp; '),esc((c.teams||[]).join(' / '))];}));
      out.acts=[seasonAct(yrs[yrs.length-1])]; return out;}
    const y=yrs[0], c=D.champs.find(x=>x.y===y)||{}, rs=ROWS.filter(r=>r.y===y);
    const by=f=>rs.slice().sort((a,b)=>f(b)-f(a))[0];
    const seed1=rs.find(r=>r.seed===1), hiPI=by(r=>r.pi), lucky=by(r=>r.luck);
    out.kind=y+' season'; out.title=(c.mgrs||[]).join(' & ')+(c.co?' (title split)':'');
    out.big=(c.co?'Co-champions':'Champion')+' · '+(c.teams||[]).join(' / ');
    out.sub=nOf(rs.length,'team')+' · '+(c.g||'')+'-game season · '+(c.spots||'')+'-team bracket';
    const line=(lab,r,v)=>[lab,r?mlink(r.mgr)+' <span class="dim">'+esc(r.team)+'</span>':'—',v];
    out.body=tbl(['','Who',''],[
      ['Runner-up',esc(c.runner||'—'),''],['Third',esc(c.third||'—'),''],
      line('Top seed',seed1,seed1?rec(seed1.w,seed1.l,seed1.t):''),
      line('Best power index',hiPI,hiPI?F1(hiPI.pi):''),line('Luckiest',lucky,lucky?sg(lucky.luck,2)+' wins':''),
      ['Last place',esc(c.last||'—'),'']]);
    out.acts=[seasonAct(y),...(c.mgrs||[]).slice(0,1).map(mgrAct)]; out.acts[0].primary=true; if(out.acts[1])out.acts[1].primary=false;
    return out;
  }

  /* a week */
  function week(q,out,yrs){
    const w=q.weeks[0];
    let y=yrs.length?yrs[yrs.length-1]:null;
    const logged=D.wkYears||[];
    if(!y){y=logged[logged.length-1]; out.notes.push('No season given, so this is '+y+'.');}
    if(!logged.includes(y)){out.kind='Week '+w; out.title='No week-by-week log for '+y;
      out.sub='Weekly results are on record for '+yearList(logged)+'.'; out.acts=[seasonAct(y)]; return out;}
    const K=D.wk[y], gs=K.games.filter(g=>g.wk===w);
    if(!gs.length){out.kind='Week '+w; out.title=y+' has no week '+w; out.sub='It ran to week '+Math.max(...K.games.map(g=>g.wk))+'.'; return out;}
    const mine=q.mgrs.length?gs.filter(g=>q.mgrs.includes(K.mgr[g.ta])||q.mgrs.includes(K.mgr[g.tb])):gs;
    out.kind='Week '+w+', '+y+(gs[0].br==='C'?' · playoffs':'');
    out.title=q.mgrs.length&&mine.length===1?(()=>{const g=mine[0],aw=g.aa>g.ab; return K.mgr[aw?g.ta:g.tb]+' beat '+K.mgr[aw?g.tb:g.ta];})():nOf(gs.length,'game');
    if(q.mgrs.length&&mine.length===1){const g=mine[0]; out.big=F2(Math.max(g.aa,g.ab))+'–'+F2(Math.min(g.aa,g.ab));}
    out.body=tbl(['Winner','Score','Loser'],(mine.length?mine:gs).map(g=>{const aw=g.aa>g.ab;
      const W=aw?g.ta:g.tb, L=aw?g.tb:g.ta;
      return [mlink(K.mgr[W])+' <span class="dim">'+esc(W)+'</span>',F2(Math.max(g.aa,g.ab))+'–'+F2(Math.min(g.aa,g.ab)),
        mlink(K.mgr[L])+' <span class="dim">'+esc(L)+'</span>'];}));
    out.acts=[weekAct(y,w)]; return out;
  }

  /* a team name */
  function team(q,out,yrs){
    let rs=[].concat(...q.teams); rs=rs.filter((r,i)=>rs.indexOf(r)===i);
    const pick=yrs.length?rs.filter(r=>yrs.includes(r.y)):rs;
    const use=pick.length?pick:rs;
    if(use.length===1){const r=use[0];
      out.kind='Team · '+r.y; out.title=r.team; out.big=r.place===1?(r.co?'Co-champion':'Champion'):ord(r.place)+' of '+r.teams;
      out.sub=r.mgr+' · '+r.y;
      out.body=tbl(['','Value'],[['Record',rec(r.w,r.l,r.t)],['Seed',ord(r.seed)],['Points per game',F2(r.ppg)],['Power index',F1(r.pi)],['Luck',sg(r.luck,2)+' wins']]);
      out.acts=[seasonAct(r.y),mgrAct(r.mgr)]; out.acts[0].primary=true; out.acts[1].primary=false; return out;}
    out.kind='Team'; out.title=use[0].team; out.sub=nOf(use.length,'season')+' under this name';
    out.body=tbl(['Year','Manager','Record','Finish'],use.sort((a,b)=>a.y-b.y).map(r=>[String(r.y),mlink(r.mgr),rec(r.w,r.l,r.t),r.place===1?'Champion':ord(r.place)]));
    out.acts=[seasonAct(use[use.length-1].y)]; return out;
  }

  /* an NFL player */
  function player(q,out){
    const n=q.players[0], p=PL[n];
    out.kind='Player'; out.title=n;
    const ts=p.trades.slice().sort((a,b)=>a.y-b.y);
    out.big=ts.length?'Traded '+(ts.length===1?'once':ts.length===2?'twice':ts.length+' times'):'No trades on record';
    out.sub='In the trade logs for '+yearList(D.trade.years||[]);
    if(ts.length)out.body=tbl(['When','From','To','Deal'],ts.map(x=>{const fromA=x.pa.includes(n);
      return [x.d+' '+x.y,mlink(fromA?x.ma:x.mb),mlink(fromA?x.mb:x.ma),dealTxt(x)];}));
    if(!D.playerStats)out.notes.push('His fantasy points, who drafted him and his injury history come with the Yahoo connection.');
    out.acts=[secAct('trades-sec')]; return out;
  }

  /* ---------------------------------------------------------------- on the page */
  const EXAMPLES=()=>{
    const act=M.filter(m=>m.last===LAST).sort(bySeasons), a=act[0]&&act[0].name, b=act[1]&&act[1].name;
    const pl=PNAMES.slice().sort((x,y)=>PL[y].trades.length-PL[x].trades.length)[0];
    return [a&&b?a.split(' ').slice(-1)[0]+' vs '+b.split(' ').slice(-1)[0]:null,'who has the most titles','luckiest season ever',
      'highest scoring week','who won '+(LAST-2),act[2]?act[2].name.split(' ')[0]+' in the playoffs':null,'most trades',
      pl?pl+' trade':null,'week 1 '+LAST,'unluckiest manager'].filter(Boolean);};
  let LAST_OUT=null;
  function render(){
    const inp=$('#askIn'), box=$('#askOut'); if(!inp||!box)return;
    const txt=inp.value.trim();
    if(!txt){LAST_OUT=null;
      box.innerHTML=`<div class="ask-k">Try one</div><div class="ask-ex">${EXAMPLES().map(e=>`<button type="button" data-ask="${esc(e)}">${esc(e)}</button>`).join('')}</div>
        <p class="ask-note">Names, seasons, weeks, team names and the players in the trade logs all work. Player stats, drafts and injuries arrive with the Yahoo connection.</p>`;
      $$('[data-ask]',box).forEach(b=>b.onclick=()=>{inp.value=b.dataset.ask; inp.focus(); render();});
      return;}
    let out;
    try{out=answer(parse(txt));}catch(e){out={kind:'Sorry',title:'That one broke the reader',notes:[String(e.message||e)],acts:[],soon:[],missing:[],ignored:[]};}
    LAST_OUT=out;
    let h=`<div class="ask-card">`;
    if(out.readAs&&out.readAs.length)h+=`<div class="ask-read">Read ${out.readAs.map(([a,b])=>`<s>${esc(a)}</s> as <b>${esc(b)}</b>`).join(', ')}</div>`;
    h+=`<div class="ask-k">${esc(out.kind)}</div><div class="ask-h">${esc(out.title)}</div>`;
    if(out.big)h+=`<div class="ask-big">${out.big}</div>`;
    if(out.sub)h+=`<div class="ask-s">${esc(out.sub)}</div>`;
    if(out.choose)h+=`<div class="ask-acts">${out.choose.options.map(o=>`<button type="button" data-pick="${esc(o)}">${esc(o)}</button>`).join('')}</div>`;
    if(out.body)h+=out.body;
    (out.missing||[]).forEach(n=>h+=`<p class="ask-note ask-warn">${esc(n)}</p>`);
    (out.soon||[]).forEach(n=>h+=`<p class="ask-note ask-warn">${esc(n)}</p>`);
    (out.notes||[]).forEach(n=>h+=`<p class="ask-note">${esc(n)}</p>`);
    if(out.ignored&&out.ignored.length)h+=`<p class="ask-note">Not used: ${esc(out.ignored.join(', '))}</p>`;
    /* one button is what Enter does, and only that one is marked */
    const pi=out.acts?out.acts.findIndex(x=>x.primary):-1, main=pi<0?0:pi;
    if(out.acts&&out.acts.length)h+=`<div class="ask-acts">${out.acts.map((a,i)=>`<button type="button" data-act="${i}"${i===main?' class="go"':''}>${esc(a.label)}</button>`).join('')}</div>`;
    if(out.empty)h+=`<div class="ask-ex" style="margin-top:12px">${EXAMPLES().slice(0,6).map(e=>`<button type="button" data-ask="${esc(e)}">${esc(e)}</button>`).join('')}</div>`;
    box.innerHTML=h+'</div>';
    box.innerHTML=tyMinus(box.innerHTML);
    $$('[data-act]',box).forEach(b=>b.onclick=()=>act(out.acts[+b.dataset.act]));
    $$('[data-ask]',box).forEach(b=>b.onclick=()=>{inp.value=b.dataset.ask; inp.focus(); render();});
    $$('[data-pick]',box).forEach(b=>b.onclick=()=>{
      inp.value=(' '+inp.value+' ').replace(new RegExp('\\b'+out.choose.word+'\\b','i'),b.dataset.pick).trim(); inp.focus(); render();});
  }
  function act(a){if(!a)return; const opensDossier=/’s page$/.test(a.label);
    if(!opensDossier)closeMgr(); a.run();}
  let timer=0;
  function open(pre){
    RETFOCUS=document.activeElement;
    $('#mTitle').textContent='Ask the record book';
    $('#mSub').textContent='Plain English · the same numbers as the page';
    $('#mBody').innerHTML=`<div class="ask"><div class="ask-in"><input id="askIn" type="search" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="go"
      aria-label="Ask the record book" placeholder="e.g. ${esc(EXAMPLES()[0]||'who has the most titles')}"></div><div id="askOut" aria-live="polite"></div></div>`;
    ov.classList.add('on'); document.body.style.overflow='hidden'; tabTitle('Ask the record book');
    const inp=$('#askIn'); inp.value=pre||'';
    inp.addEventListener('input',()=>{clearTimeout(timer); timer=setTimeout(render,90);});
    inp.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault(); clearTimeout(timer); render();
      const p=LAST_OUT&&(LAST_OUT.acts||[]).find(a=>a.primary)||LAST_OUT&&(LAST_OUT.acts||[])[0]; if(p)act(p);}});
    render(); inp.focus();
  }
  /* the button in the filter bar, and two keys: "/" anywhere that is not a text box, and
     Cmd/Ctrl+K, the shortcut most search boxes on the web answer to */
  const btn=$('#askBtn'); if(btn)btn.onclick=()=>open();
  addEventListener('keydown',e=>{
    const tg=e.target, typing=tg&&(/^(INPUT|TEXTAREA|SELECT)$/.test(tg.tagName)||tg.isContentEditable);
    if((e.metaKey||e.ctrlKey)&&!e.altKey&&(e.key==='k'||e.key==='K')){e.preventDefault(); if(ov.classList.contains('on')&&$('#askIn'))$('#askIn').focus(); else open(); return;}
    if(e.key==='/'&&!typing&&!e.metaKey&&!e.ctrlKey&&!e.altKey&&!ov.classList.contains('on')){e.preventDefault(); open();}
  });
  return {parse,answer,open,render,ENT,MET,PL};
})();
