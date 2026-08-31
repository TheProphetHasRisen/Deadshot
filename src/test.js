const { chromium } = require('playwright');
const path = require('path');
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
  await b.close();
  console.log(errs.length?('ERRORS:\n'+errs.join('\n')):'NO JS ERRORS');
})();
