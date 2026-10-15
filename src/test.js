const { chromium, webkit, devices } = require('playwright');
const path = require('path');
const fs = require('fs');
const FILE = 'file://' + path.join(__dirname, 'index.html');
const EXE = process.env.CHROMIUM_PATH || undefined;
(async()=>{
  const b=await chromium.launch(EXE?{executablePath:EXE}:{});
  const errs=[];
  for(const [w,h,name] of [[1400,1000,'desktop'],[390,844,'mobile']]){
    const p=await b.newPage({viewport:{width:w,height:h}});
    p.on('pageerror',e=>errs.push(name+' PAGEERROR: '+e.message));
    p.on('console',m=>{if(m.type()==='error')errs.push(name+' CONSOLE: '+m.text())});
    await p.goto(FILE);
    await p.waitForTimeout(1200);
    /* every section and every card starts shut (Brian, Oct 2026), with a bar at the top that opens
       the sections, opens everything, or shuts everything again */
    const fold=async()=>p.evaluate(()=>{const q=s=>[...document.querySelectorAll(s)];
      return {secs:q('main#main .sec-fold').length, secsOpen:q('main#main .sec-fold:not([hidden])').length,
              cards:q('main#main .fold-body').length, cardsOpen:q('main#main .fold-body:not([hidden])').length,
              bar:q('main#main > .fold-bar button').length};});
    const f0=await fold();
    if(f0.secs<10||f0.secsOpen||f0.cardsOpen||f0.bar!==3)errs.push(name+' the record book does not start shut: '+JSON.stringify(f0));
    await p.click('main#main > .fold-bar [data-fold="sections"]'); await p.waitForTimeout(150);
    const f1=await fold();
    if(f1.secsOpen!==f1.secs||f1.cardsOpen)errs.push(name+' "Open all sections" did not open just the sections: '+JSON.stringify(f1));
    await p.click('main#main > .fold-bar [data-fold=""]'); await p.waitForTimeout(150);
    const f2=await fold();
    if(f2.secsOpen||f2.cardsOpen)errs.push(name+' "Close everything" left something open: '+JSON.stringify(f2));
    /* a menu link opens the section it points at */
    await p.evaluate(()=>{const a=document.querySelector('#nav a[data-id="h2h"]'); if(a)a.click();}); await p.waitForTimeout(150);
    const f3=await p.evaluate(()=>!document.querySelector('#h2h > .sec-fold').hidden);
    if(!f3)errs.push(name+' the menu link to Head to head did not open it');
    /* a season page and the 2026 page start shut too, and their bar opens every card */
    const sp=await p.evaluate(()=>{const out={};
      if(typeof openSeason==='function'){openSeason(2023);
        const v=document.querySelector('#syView'), q=s=>[...v.querySelectorAll(s)];
        out.season={cards:q('.fold-body').length, open:q('.fold-body:not([hidden])').length};
        v.querySelector('.fold-bar [data-fold="sections"]').click();
        out.season.afterOpen=q('.fold-body:not([hidden])').length;
        const b=document.getElementById('lvSegBook'); if(b)b.click();}
      return out;});
    if(sp.season&&(sp.season.cards<8||sp.season.open||!sp.season.afterOpen))errs.push(name+' the 2023 season page does not start shut, or will not open: '+JSON.stringify(sp));
    await p.click('main#main > .fold-bar [data-fold="deep"]'); await p.waitForTimeout(300);
    const f4=await fold();
    if(f4.secsOpen!==f4.secs||f4.cardsOpen!==f4.cards)errs.push(name+' "Open everything" left something shut: '+JSON.stringify(f4));
    console.log(name+' folding', JSON.stringify({start:f0, sections:f1.secsOpen, season:sp.season}));
    // structural checks
    const r=await p.evaluate(()=>({
      board:document.querySelectorAll('.plate').length,
      allRows:document.querySelectorAll('#tAll tbody tr').length,
      heatRows:document.querySelectorAll('#tHeat tbody tr').length,
      heatCells:document.querySelectorAll('#tHeat td.h[data-k]').length,
      luck:document.querySelectorAll('#tLuck tbody tr').length,
      con:document.querySelectorAll('#tCon tbody tr').length,
      po:document.querySelectorAll('#tPO tbody tr').length,
      recs:document.querySelectorAll('#recs .card').length,
      mtx:document.querySelectorAll('#tMtx td[data-a]').length,
      method:document.querySelectorAll('.mrow').length,
      games:document.querySelectorAll('.game').length,
      race:document.querySelectorAll('#race path[data-t]').length,
      strip:document.querySelectorAll('#strip circle').length,
      bal:document.querySelectorAll('#bal path').length,
      ap:document.querySelectorAll('#tAP tbody tr').length,
      proj:document.querySelectorAll('#tProj tbody tr').length,
      riv:document.querySelectorAll('#tRiv tbody tr').length,
      trades:document.querySelectorAll('#trades .card').length,
      wk:document.querySelectorAll('#wkOut .game').length,
      conn:document.querySelectorAll('#conn path').length,
      cmp:document.querySelectorAll('#cmpOut table tr').length,
      hscroll:document.documentElement.scrollWidth>document.documentElement.clientWidth,
      bodyBg:getComputedStyle(document.body).backgroundColor,
      // every manager still playing must get their own one-line verdict. Three of them
      // collided once and it read like a bug. Retired one-season managers may share.
      vibeDupes:(()=>{
        try{
          const seen={},bad=[];
          DATA.mgrs.filter(m=>m.last===DATA.last).forEach(m=>{
            const v=mgrVibe(m);
            if(seen[v])bad.push(seen[v]+' / '+m.name); else seen[v]=m.name;});
          return bad;
        }catch(e){return ['mgrVibe unavailable: '+e.message];}
      })(),
    }));
    console.log(name, JSON.stringify(r));
    if(r.vibeDupes.length)errs.push(name+' DUPLICATE manager verdicts: '+r.vibeDupes.join(', '));
    if(name==='desktop'){
      await p.screenshot({path:'shot-top.png',clip:{x:0,y:0,width:1400,height:1000}});
      await p.evaluate(()=>document.querySelector('#power').scrollIntoView());
      await p.waitForTimeout(400); await p.screenshot({path:'shot-power.png'});
      await p.evaluate(()=>document.querySelector('#luck').scrollIntoView());
      await p.waitForTimeout(400); await p.screenshot({path:'shot-luck.png'});
      await p.evaluate(()=>document.querySelector('#seasons').scrollIntoView());
      await p.waitForTimeout(400); await p.screenshot({path:'shot-seasons.png'});
      await p.evaluate(()=>document.querySelector('#h2h').scrollIntoView());
      await p.waitForTimeout(400); await p.screenshot({path:'shot-h2h.png'});
      // dark
      await p.emulateMedia({colorScheme:'dark'}); await p.evaluate(()=>scrollTo(0,0));
      await p.waitForTimeout(400); await p.screenshot({path:'shot-dark.png',clip:{x:0,y:0,width:1400,height:1000}});
    }
    await p.close();
  }
  /* the typefaces are self-hosted: all six load off disk, and nothing is fetched from Google */
  {
    const p=await b.newPage({viewport:{width:1200,height:800}});
    await p.goto(FILE); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
    const f=await p.evaluate(()=>({
      loaded:[...document.fonts].filter(x=>x.status==='loaded').length,
      remote:performance.getEntriesByType('resource').map(x=>x.name).filter(n=>!n.startsWith('file:')),
      google:document.documentElement.outerHTML.match(/fonts\.g(oogleapis|static)\.com/g)||[],
    }));
    console.log('fonts',JSON.stringify(f));
    if(f.loaded<6||f.remote.length||f.google.length){console.error('FONT CHECK FAILED');process.exit(1);}
    await p.close();
  }
  await b.close();
  if(errs.length){
    /* deploy.sh gates on this exit code. Printing and exiting 0 meant a broken page
       could sail past the only automated check the site has. */
    console.error('ERRORS:\n'+errs.join('\n'));
    process.exit(1);
  }
  console.log('NO JS ERRORS');

  /* ---- WebKit, at real iPhone sizes ----------------------------------------------
     Safari's engine is the one most readers use and the one that finds layout breaks
     nothing else does (the SE is 320pt wide). Until now only Chromium was checked, so
     the check the rules call the important one never ran before a deploy. */
  const wkExe = webkit.executablePath();
  if(!wkExe || !fs.existsSync(wkExe)){
    console.error('WEBKIT NOT INSTALLED - the iPhone check did not run. Install it once with:\n    npx playwright install webkit');
    process.exit(3);   /* deploy.sh treats 3 as "unverified on a phone": no push */
  }
  const wkErrs=[];
  const wb=await webkit.launch();
  for(const dev of ['iPhone SE','iPhone 15 Pro']){
    const ctx=await wb.newContext({...devices[dev]});
    const p=await ctx.newPage();
    p.on('pageerror',e=>wkErrs.push(dev+' PAGEERROR: '+e.message));
    /* WebKit refuses the manifest link when the page is opened from disk (file://);
       that is the test harness, not the site, and cannot happen on the live URL */
    p.on('console',m=>{if(m.type()==='error'&&!/ERR_TUNNEL|Not allowed to load local resource/.test(m.text()))wkErrs.push(dev+' CONSOLE: '+m.text())});
    await p.goto(FILE,{waitUntil:'load'});
    await p.evaluate(()=>document.fonts.ready);
    await p.waitForTimeout(800);
    const r=await p.evaluate(()=>({
      vw:innerWidth, docW:document.documentElement.scrollWidth,
      fontsLoaded:[...document.fonts].filter(f=>f.status==='loaded').length,
      fontsTotal:document.fonts.size,
      fontsErrored:[...document.fonts].filter(f=>f.status==='error').length,
      /* nothing may come from fonts.googleapis.com / fonts.gstatic.com any more */
      thirdParty:performance.getEntriesByType('resource').map(x=>x.name).filter(n=>!n.startsWith('file:')),
    }));
    /* the page itself must never scroll sideways on a phone; cards scroll inside themselves */
    if(r.docW>r.vw)wkErrs.push(dev+' page scrolls sideways: document '+r.docW+'px wide in a '+r.vw+'px viewport');
    /* the six real typefaces are our own files under fonts/, so they load with no network */
    if(r.fontsLoaded<6)wkErrs.push(dev+' only '+r.fontsLoaded+' of the typefaces loaded (need 6)');
    if(r.thirdParty.length)wkErrs.push(dev+' fetched from a third party: '+r.thirdParty.join(' '));
    /* it starts shut on a phone too; the bar's Open everything opens it */
    const shut=await p.evaluate(()=>document.querySelectorAll('main#main .sec-fold:not([hidden]),main#main .fold-body:not([hidden])').length);
    if(shut)wkErrs.push(dev+' '+shut+' sections or cards started open');
    await p.locator('main#main > .fold-bar [data-fold="deep"]').click();
    await p.waitForTimeout(400);
    const wide=await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
    if(wide>0)wkErrs.push(dev+' with everything open the page scrolls sideways by '+wide+'px');
    /* the manager dossier opens from a name and closes on Escape */
    await p.locator('.mlink').first().click();
    await p.waitForTimeout(400);
    const opened=await p.evaluate(()=>document.getElementById('ov').classList.contains('on'));
    if(!opened)wkErrs.push(dev+' tapping a manager name did not open the dossier');
    await p.keyboard.press('Escape');
    await p.waitForTimeout(300);
    const closed=await p.evaluate(()=>!document.getElementById('ov').classList.contains('on'));
    if(!closed)wkErrs.push(dev+' Escape did not close the dossier');
    console.log('webkit '+dev, JSON.stringify({...r, dossier:opened&&closed}));
    await ctx.close();
  }
  await wb.close();
  if(wkErrs.length){
    console.error('WEBKIT ERRORS:\n'+wkErrs.join('\n'));
    process.exit(1);
  }
  console.log('WEBKIT OK');
})();
