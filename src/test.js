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
