import sys, os, json, math, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D
K=2.37
def neutral_title_odds(seed, spots):
    """A coin-flip baseline that still values a first-round bye.
    Bracket is padded to the next power of two; the top `byes` seeds skip a round,
    so they need one fewer win. Sums to exactly 1.0 across any bracket."""
    rounds = max(1, math.ceil(math.log2(spots)))
    byes = 2**rounds - spots
    return 0.5 ** (rounds - (1 if seed <= byes else 0))
seasons=sorted(D.STANDINGS)
LAST=max(seasons)
rows=[]
for y in seasons:
    co=D.CO_CHAMPS.get(y,[]); teams,g,spots,_=D.SEASON_META[y]; n=len(D.STANDINGS[y])
    lg=sum(r[5] for r in D.STANDINGS[y])/n/g
    sd=math.sqrt(sum((r[5]/g-lg)**2 for r in D.STANDINGS[y])/n)
    fp={};sh={}
    for i,t in enumerate(D.FINAL_PLACE[y]):
        if t in co: fp[t]=1; sh[t]=1/len(co)
        else: fp[t]=i+1; sh[t]=1.0 if i==0 else 0.0
    for (rank,team,W,L,T,pf,pa,mv) in D.STANDINGS[y]:
        G=W+L+T; pyth=pf**K/(pf**K+pa**K); neut=pf**K/(pf**K+(lg*g)**K)*G
        rows.append(dict(y=y,seed=rank,team=team,mgr=D.MANAGERS[y][team],w=W,l=L,t=T,pf=pf,pa=pa,mv=mv,
            g=g,teams=n,spots=spots,place=fp[team],share=sh[team],co=team in co,
            ppg=pf/g,ppga=pa/g,lg=lg,paa=pf/g-lg,saa=pa/g-lg,pi=100*(pf/g)/lg,z=(pf/g-lg)/sd,
            pythW=pyth*G,luck=(W+T/2)-pyth*G,
            po=rank<=spots, sf=(rank-fp[team]) if rank<=spots else None,
            expT=(neutral_title_odds(rank,spots) if rank<=spots else 0)))
bym=collections.defaultdict(list)
for r in rows: bym[r['mgr']].append(r)
pw=collections.Counter(); pl=collections.Counter(); ppts=collections.Counter(); pg=collections.Counter(); fin=collections.Counter()
h2h=collections.defaultdict(lambda:[0,0])
games=[]
for (y,wk,rnd,ta,pa_,tb,pb,void) in D.PLAYOFF_GAMES:
    ma,mb=D.MANAGERS[y][ta],D.MANAGERS[y][tb]
    games.append(dict(y=y,wk=wk,rnd=rnd,ta=ta,ma=ma,pa=pa_,tb=tb,mb=mb,pb=pb,void=void))
    if rnd=="Final": fin[ma]+=1; fin[mb]+=1
    if void: continue
    w,l=(ma,mb) if pa_>pb else (mb,ma)
    pw[w]+=1; pl[l]+=1; ppts[ma]+=pa_; ppts[mb]+=pb; pg[ma]+=1; pg[mb]+=1
    h2h[(w,l)][0]+=1; h2h[(l,w)][1]+=1
mgrs=[]
for m,rs in bym.items():
    W=sum(r['w'] for r in rs); L=sum(r['l'] for r in rs); T=sum(r['t'] for r in rs); G=W+L+T
    pis=[r['pi'] for r in rs]; mean=sum(pis)/len(pis)
    zs=[r['z'] for r in rs]
    zavg=sum(r['z']*(r['w']+r['l']+r['t']) for r in rs)/G
    rec=[r['pi'] for r in rs if r['y']>=LAST-2]
    cpi=sum(r['pi']*(r['w']+r['l']+r['t']) for r in rs)/G
    apps=sum(1 for r in rs if r['po'])
    exp=sum(neutral_title_odds(r['seed'],r['spots']) for r in rs if r['po'])
    mgrs.append(dict(name=m,seasons=len(rs),first=min(r['y'] for r in rs),last=max(r['y'] for r in rs),
        w=W,l=L,t=T,g=G,winpct=(W+T/2)/G,titles=sum(r['share'] for r in rs),
        second=sum(1 for r in rs if r['place']==2),third=sum(1 for r in rs if r['place']==3),
        podium=sum(1 for r in rs if r['place']<=3),lastPl=sum(1 for r in rs if r['place']==r['teams']),
        avgPlace=sum(r['place'] for r in rs)/len(rs),best=min(r['place'] for r in rs),worst=max(r['place'] for r in rs),
        pf=sum(r['pf'] for r in rs),pa=sum(r['pa'] for r in rs),ppg=sum(r['pf'] for r in rs)/G,
        cpi=cpi,peak=max(pis),floor=min(pis),zAvg=zavg,zPeak=max(zs),zFloor=min(zs),sd=(math.sqrt(sum((p-mean)**2 for p in pis)/len(rs)) if len(rs)>1 else None),
        form=(sum(rec)/len(rec) if rec else None),trend=((sum(rec)/len(rec))-cpi if rec else None),
        luck=sum(r['luck'] for r in rs),pythW=sum(r['pythW'] for r in rs),
        apps=apps,expT=exp,vsExp=sum(r['share'] for r in rs)-exp,
        poG=pw[m]+pl[m],poW=pw[m],poL=pl[m],poPPG=(ppts[m]/pg[m] if pg[m] else None),finals=fin[m],
        lastTitle=(max([r['y'] for r in rs if r['place']==1]) if any(r['place']==1 for r in rs) else None)))
champs=[]
for y in seasons:
    co=D.CO_CHAMPS.get(y,[])
    cs=co if co else [D.FINAL_PLACE[y][0]]
    champs.append(dict(y=y,teams=cs,mgrs=[D.MANAGERS[y][t] for t in cs],
        runner=(None if co else D.FINAL_PLACE[y][1]),third=D.FINAL_PLACE[y][2 if not co else 2],
        last=D.FINAL_PLACE[y][-1],spots=D.SEASON_META[y][2],g=D.SEASON_META[y][1],n=len(D.STANDINGS[y]),
        lg=[r for r in rows if r['y']==y][0]['lg'],
        co=bool(co)))
out=dict(seasons=seasons,last=LAST,rows=rows,mgrs=sorted(mgrs,key=lambda m:(-m['titles'],-m['podium'],-m['winpct'])),
    champs=champs,games=games,h2h={f"{a}|{b}":v for (a,b),v in h2h.items()})
json.dump(out,open('site_data.json','w'),separators=(',',':'),default=lambda o:round(o,4) if isinstance(o,float) else o)
print("rows",len(rows),"mgrs",len(mgrs),"games",len(games),"h2h pairs",len(h2h))
print("bytes",len(open('site_data.json').read()))

# ---- weekly layer, per season ----
import weekly as WK25, weekly2024 as WK24, weekly2023 as WK23, weekly2022 as WK22, weekly2021 as WK21
SRC={2025:(WK25.W2025,WK25.BYES2025,WK25.TRADES2025),2024:(WK24.W2024,WK24.BYES2024,WK24.TRADES2024),
     2023:(WK23.W2023,WK23.BYES2023,WK23.TRADES2023),
     2022:(WK22.W2022,WK22.BYES2022,WK22.TRADES2022),
     2021:(WK21.W2021,WK21.BYES2021,WK21.TRADES2021)}
WKALL={}
for YR,(GAMES,BYES,TRD) in SRC.items():
    reg=[g for g in GAMES if g[7]=='']
    teams=sorted({g[1] for g in GAMES}|{g[4] for g in GAMES})
    mgr={t:D.MANAGERS[YR][t] for t in teams}
    tw={t:{} for t in teams}
    for (w,ta,aa,pa,tb,ab,pb,br) in reg:
        tw[ta][w]=dict(pts=aa,proj=pa,opp=tb,oppPts=ab)
        tw[tb][w]=dict(pts=ab,proj=pb,opp=ta,oppPts=aa)
    WKS=sorted({g[0] for g in reg})
    allplay={}; race={}; five={}
    for t in teams:
        apw=apl=0; cw=0; seq=[]
        for w in WKS:
            me=tw[t][w]; others=[tw[o][w]['pts'] for o in teams if o!=t]
            apw+=sum(1 for x in others if me['pts']>x); apl+=sum(1 for x in others if me['pts']<x)
            cw+= 1 if me['pts']>me['oppPts'] else 0
            seq.append(dict(w=w,wins=cw,pts=me['pts'],proj=me['proj'],opp=me['opp'],oppPts=me['oppPts'],
                            win=me['pts']>me['oppPts'],ap=sum(1 for x in others if me['pts']>x)))
        allplay[t]=dict(w=apw,l=apl,pct=apw/(apw+apl)); race[t]=seq
        # how much of the season was actually spent on the right side of .500
        ab=at=be=0; run=0; best=0
        for i,x in enumerate(seq):
            d=x['wins']-((i+1)-x['wins'])
            if d>0: ab+=1; run+=1; best=max(best,run)
            elif d==0: at+=1; run=0
            else: be+=1; run=0
        five[t]=dict(above=ab,at=at,below=be,streak=best)
    # week-to-week volatility, and how hard the schedule actually was
    ppg={t:sum(tw[t][w]['pts'] for w in WKS)/len(WKS) for t in teams}
    lgppg=sum(ppg.values())/len(teams)
    apn={t:allplay[t]['pct'] for t in teams}
    form={}
    for t in teams:
        pts=[tw[t][w]['pts'] for w in WKS]
        mu=sum(pts)/len(pts)
        sd=math.sqrt(sum((x-mu)**2 for x in pts)/len(pts))
        opps=[tw[t][w]['opp'] for w in WKS]
        sos=sum(ppg[o] for o in opps)/len(opps)
        sosap=sum(apn[o] for o in opps)/len(opps)
        form[t]=dict(sd=sd,cv=100*sd/mu,hi=max(pts),lo=min(pts),ppg=mu,
                     sos=sos,sosRel=sos-lgppg,sosAp=sosap,
                     # every opponent except yourself, faced once each, is the neutral schedule
                     sosBase=(sum(ppg[o] for o in teams if o!=t)/(len(teams)-1)))
    riv=[]
    for i,a_ in enumerate(teams):
        for b_ in teams[i+1:]:
            gs=[g for g in GAMES if {g[1],g[4]}=={a_,b_}]
            if not gs: continue
            aw=sum(1 for g in gs if (g[1]==a_ and g[2]>g[5]) or (g[4]==a_ and g[5]>g[2]))
            marg=sum(abs(g[2]-g[5]) for g in gs)/len(gs)
            bal=1-abs(aw-(len(gs)-aw))/len(gs)
            riv.append(dict(a=mgr[a_],b=mgr[b_],ta=a_,tb=b_,g=len(gs),aw=aw,bw=len(gs)-aw,
                            marg=marg,score=len(gs)*bal*100/(10+marg)))
    riv.sort(key=lambda r:-r['score'])
    WKALL[YR]=dict(weeks=WKS,teams=teams,mgr=mgr,
      games=[dict(wk=g[0],ta=g[1],aa=g[2],pa=g[3],tb=g[4],ab=g[5],pb=g[6],br=g[7]) for g in GAMES],
      byes=[dict(wk=b[0],t=b[1],a=b[2],p=b[3],br=b[4]) for b in BYES],
      allplay=allplay,race=race,rivals=riv[:14],form=form,lgppg=lgppg,five=five,
      trades=[dict(d=t[0],pa=t[1],ta=t[2],pb=t[3],tb=t[4]) for t in TRD])
# ---- trade market, aggregated across every loaded season ----
tCnt=collections.Counter(); tIn=collections.Counter(); tOut=collections.Counter()
tPlayersIn=collections.Counter(); tPlayersOut=collections.Counter()
tPair=collections.Counter(); tYear=collections.defaultdict(collections.Counter)
tPartners=collections.defaultdict(set); tLog=[]
for YR in sorted(WKALL):
    K=WKALL[YR]; mg=K['mgr']
    for t in K['trades']:
        ma,mb=mg.get(t['ta']),mg.get(t['tb'])
        if not ma or not mb: continue
        tCnt[ma]+=1; tCnt[mb]+=1
        tPlayersIn[ma]+=len(t['pa']); tPlayersOut[ma]+=len(t['pb'])
        tPlayersIn[mb]+=len(t['pb']); tPlayersOut[mb]+=len(t['pa'])
        tPair[tuple(sorted([ma,mb]))]+=1
        tYear[YR][ma]+=1; tYear[YR][mb]+=1
        tPartners[ma].add(mb); tPartners[mb].add(ma)
        tLog.append(dict(y=YR,d=t['d'],ma=ma,mb=mb,ta=t['ta'],tb=t['tb'],pa=t['pa'],pb=t['pb']))
tYears=sorted(WKALL)
tMgr=[]
for m in tCnt:
    yrs=[y for y in tYears if any(r['mgr']==m and r['y']==y for r in rows)]
    busy=max(((tYear[y][m],y) for y in tYears if tYear[y][m]), default=(0,None))
    tMgr.append(dict(name=m,trades=tCnt[m],seasons=len(yrs),
        per=(tCnt[m]/len(yrs) if yrs else 0),partners=len(tPartners[m]),
        pin=tPlayersIn[m],pout=tPlayersOut[m],
        busyN=busy[0],busyY=busy[1]))
for m in [mm['name'] for mm in mgrs]:
    if m in tCnt: continue
    yrs=[y for y in tYears if any(r['mgr']==m and r['y']==y for r in rows)]
    if yrs: tMgr.append(dict(name=m,trades=0,seasons=len(yrs),per=0,partners=0,pin=0,pout=0,busyN=0,busyY=None))
tMgr.sort(key=lambda d:-d['trades'])
out.update(trade=dict(years=tYears,mgr=tMgr,
    pairs=[dict(a=k[0],b=k[1],n=v) for k,v in sorted(tPair.items(),key=lambda kv:-kv[1])],
    byYear={y:dict(tYear[y]) for y in tYears},
    log=tLog))
# ---- all-play, back onto the season rows and the career totals ----
# ---- record against teams that finished above .500 ----
winner={}                                   # (year, team) -> did they finish over .500
for r in rows: winner[(r['y'],r['team'])]=r['w']>r['l']
vs=collections.defaultdict(lambda:[0,0,0,0])   # mgr -> [W vs winners, L vs winners, W vs rest, L vs rest]
def logGame(y,ta,pa_,tb,pb):
    if pa_==pb: return
    for me,mine,opp,theirs in ((ta,pa_,tb,pb),(tb,pb,ta,pa_)):
        m=D.MANAGERS[y].get(me)
        if m is None or (y,opp) not in winner: continue
        v=vs[m]; strong=winner[(y,opp)]
        if mine>theirs: v[0 if strong else 2]+=1
        else:           v[1 if strong else 3]+=1
for YR in WKALL:
    for g in WKALL[YR]['games']:
        if g['br']: continue
        logGame(YR,g['ta'],g['aa'],g['tb'],g['ab'])
for (y,wk,rnd,ta,pa_,tb,pb,void) in D.PLAYOFF_GAMES:
    if void: continue
    logGame(y,ta,pa_,tb,pb)
for m in mgrs:
    a,b,c,e=vs.get(m['name'],[0,0,0,0])
    m['vsWinW'],m['vsWinL'],m['vsSubW'],m['vsSubL']=a,b,c,e
    m['vsWinPct']=(a/(a+b)) if (a+b) else None
    m['vsSubPct']=(c/(c+e)) if (c+e) else None
    m['vsGap']=(m['vsWinPct']-m['vsSubPct']) if (m['vsWinPct'] is not None and m['vsSubPct'] is not None) else None

rowByYT={(r['y'],r['team']):r for r in rows}
for YR in WKALL:
    for t,fv in WKALL[YR]['five'].items():
        r=rowByYT.get((YR,t))
        if r: r['wkAbove']=fv['above']; r['wkAt']=fv['at']; r['wkBelow']=fv['below']; r['wkStreak']=fv['streak']
apM=collections.defaultdict(lambda:[0,0,0])   # mgr -> [w, l, seasons]
for YR in WKALL:
    for t,a in WKALL[YR]['allplay'].items():
        r=rowByYT.get((YR,t))
        if not r: continue
        r['apw']=a['w']; r['apl']=a['l']; r['appct']=a['pct']
        m=apM[r['mgr']]; m[0]+=a['w']; m[1]+=a['l']; m[2]+=1
for m in mgrs:
    rs=bym[m['name']]
    m['gAbove']=sum(r['w'] for r in rs)-sum(r['l'] for r in rs)     # games clear of .500
    m['sznAbove']=sum(1 for r in rs if r['w']>r['l'])
    m['sznBelow']=sum(1 for r in rs if r['w']<r['l'])
    m['sznEven']=sum(1 for r in rs if r['w']==r['l'])
    m['expOverAvg']=sum(r['pythW']-(r['w']+r['l']+r['t'])/2 for r in rs)   # wins the scoring earned above average
    wa=sum(r.get('wkAbove',0) for r in rs); wt=sum(r.get('wkAt',0) for r in rs); wb=sum(r.get('wkBelow',0) for r in rs)
    m['wkAbove']=wa; m['wkAt']=wt; m['wkBelow']=wb
    m['wkTot']=wa+wt+wb
    m['wkAbovePct']=(wa/(wa+wt+wb)) if (wa+wt+wb) else None
    m['wkStreak']=max([r.get('wkStreak',0) for r in rs] or [0])
    w,l,n=apM.get(m['name'],[0,0,0])
    m['apW']=w; m['apL']=l; m['apSzn']=n
    m['apPct']=(w/(w+l)) if (w+l) else None
    # real win% minus all-play win% over the same seasons, in wins per season
    if n:
        yrs={r['y'] for r in bym[m['name']] if 'apw' in r}
        rw=sum(r['w']+r['t']/2 for r in bym[m['name']] if r['y'] in yrs)
        rg=sum(r['w']+r['l']+r['t'] for r in bym[m['name']] if r['y'] in yrs)
        m['apLuck']=rw-(w/(w+l))*rg if (w+l) else None
        m['apGames']=rg
    else:
        m['apLuck']=None; m['apGames']=0
out.update(wk=WKALL, wkYears=sorted(WKALL))
json.dump(out,open('site_data.json','w'),separators=(',',':'),default=lambda o:round(o,4) if isinstance(o,float) else o)
print("weekly seasons:",sorted(WKALL),"| bytes",len(open('site_data.json').read()))
for y in sorted(WKALL):
    ap=WKALL[y]['allplay']
    best=max(ap,key=lambda t:ap[t]['pct'])
    print("  ",y,"best all-play:",best,ap[best]['w'],'-',ap[best]['l'],"| top rivalry:",WKALL[y]['rivals'][0]['a'],"vs",WKALL[y]['rivals'][0]['b'])
