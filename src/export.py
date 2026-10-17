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
json.dump(out,open('site_data.json','w'),indent=1,separators=(',',': '),default=lambda o:round(o,4) if isinstance(o,float) else o)
print("rows",len(rows),"mgrs",len(mgrs),"games",len(games),"h2h pairs",len(h2h))
print("bytes",len(open('site_data.json').read()))

# ---- weekly layer, per season ----
import weekly as WK25, weekly2024 as WK24, weekly2023 as WK23, weekly2022 as WK22, weekly2021 as WK21
SRC={2025:(WK25.W2025,WK25.BYES2025,WK25.TRADES2025),2024:(WK24.W2024,WK24.BYES2024,WK24.TRADES2024),
     2023:(WK23.W2023,WK23.BYES2023,WK23.TRADES2023),
     2022:(WK22.W2022,WK22.BYES2022,WK22.TRADES2022),
     2021:(WK21.W2021,WK21.BYES2021,WK21.TRADES2021)}
# the live season joins the weekly layer (its games so far, its trades), so Week by Week, the Trade
# Market, the records and everything else built on this layer carry 2026 as it is played. It stays
# out of the season rows, careers-by-season and champions until the final.
try:
    import season2026 as _S26
    if _S26.W2026:
        SRC[2026]=(_S26.W2026, [], [(d, ga, ta, gb, tb) for (d, ta, ga, tb, gb) in _S26.TRADES2026])
    MGRS_LIVE={2026: _S26.MGR2026}
except ImportError:
    MGRS_LIVE={}
WKALL={}
for YR,(GAMES,BYES,TRD) in SRC.items():
    reg=[g for g in GAMES if g[7]=='']
    teams=sorted({g[1] for g in GAMES}|{g[4] for g in GAMES})
    # the live season's games carry its own team names, so its own manager list names them (the record
    # book's copy only exists once the final is written, and test_writer.py writes a made-up one)
    mgr={t:(MGRS_LIVE.get(YR) or D.MANAGERS.get(YR))[t] for t in teams}
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
# the seasons a manager played inside the logged years, the one being played included (its trades are in
# the ledger, so it has to be in the count they are divided by)
_LIVEM=set((MGRS_LIVE.get(max(tYears)) or {}).values()) if tYears and max(tYears) in MGRS_LIVE else set()
def _yrs(m): return [y for y in tYears if any(r['mgr']==m and r['y']==y for r in rows) or (y in MGRS_LIVE and m in _LIVEM)]
for m in tCnt:
    yrs=_yrs(m)
    busy=max(((tYear[y][m],y) for y in tYears if tYear[y][m]), default=(0,None))
    tMgr.append(dict(name=m,trades=tCnt[m],seasons=len(yrs),
        per=(tCnt[m]/len(yrs) if yrs else 0),partners=len(tPartners[m]),
        pin=tPlayersIn[m],pout=tPlayersOut[m],
        busyN=busy[0],busyY=busy[1]))
for m in [mm['name'] for mm in mgrs]:
    if m in tCnt: continue
    yrs=_yrs(m)
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
        m=D.MANAGERS.get(y, {}).get(me)
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
json.dump(out,open('site_data.json','w'),indent=1,separators=(',',': '),default=lambda o:round(o,4) if isinstance(o,float) else o)
print("weekly seasons:",sorted(WKALL),"| bytes",len(open('site_data.json').read()))
for y in sorted(WKALL):
    ap=WKALL[y]['allplay']
    best=max(ap,key=lambda t:ap[t]['pct'])
    print("  ",y,"best all-play:",best,ap[best]['w'],'-',ap[best]['l'],"| top rivalry:",WKALL[y]['rivals'][0]['a'],"vs",WKALL[y]['rivals'][0]['b'])

# ---- the live season ----------------------------------------------------------------------
# 2026 is shown in its own section and kept OUT of the record book (rows, careers, champions,
# head to head) until it is finished: half a season would drag every career rate around.
# Week 5 was not in the screenshots; its scores come from the standings totals minus weeks
# 1-4, and its pairings from whose points-for matches whose points-against. check_2026.py
# proves the same arithmetic reconciles every record, streak, PF and PA.
try:
    import season2026 as S26
except ImportError:
    S26 = None
if S26:
    ST = S26.STANDINGS2026_WK5
    games = [dict(wk=w, ta=a, aa=sa, pa=pa_, tb=b, ab=sb, pb=pb_) for (w, a, sa, pa_, b, sb, pb_, br) in S26.W2026]
    pf = {t: 0.0 for t in ST}; pa = {t: 0.0 for t in ST}
    for g in games:
        pf[g['ta']] += g['aa']; pa[g['ta']] += g['ab']; pf[g['tb']] += g['ab']; pa[g['tb']] += g['aa']
    done = max(g['wk'] for g in games)
    if done < 5:
        w5f = {t: round(ST[t][4] - pf[t], 2) for t in ST}; w5a = {t: round(ST[t][5] - pa[t], 2) for t in ST}
        used = set()
        for t in ST:
            if t in used: continue
            o = [x for x in ST if x != t and x not in used and abs(w5f[x] - w5a[t]) < .005 and abs(w5a[x] - w5f[t]) < .005]
            assert len(o) == 1, 'week 5 cannot be recovered for ' + t
            used |= {t, o[0]}
            games.append(dict(wk=5, ta=t, aa=w5f[t], pa=None, tb=o[0], ab=w5f[o[0]], pb=None))
    weeks = sorted({g['wk'] for g in games})
    # all-play: every week, how many of the other nine each team outscored
    ap = {t: [0, 0] for t in ST}
    for wk in weeks:
        sc = {}
        for g in games:
            if g['wk'] == wk: sc[g['ta']] = g['aa']; sc[g['tb']] = g['ab']
        for t, v in sc.items():
            ap[t][0] += sum(1 for o, ov in sc.items() if o != t and v > ov)
            ap[t][1] += sum(1 for o, ov in sc.items() if o != t and v < ov)
    stand = []
    for t, (rank, w, l, tie, f, a, streak, waiver, moves) in sorted(ST.items(), key=lambda kv: kv[1][0]):
        g = w + l + tie
        stand.append(dict(rank=rank, team=t, mgr=S26.MGR2026.get(t), w=w, l=l, t=tie, pf=f, pa=a, streak=streak,
                          waiver=waiver, moves=moves, apW=ap[t][0], apL=ap[t][1],
                          luck=(w + tie / 2) - g * ap[t][0] / (ap[t][0] + ap[t][1]) if ap[t][0] + ap[t][1] else None))
    # The career tables count finished seasons only, like titles, seasons and the power index. Adding
    # 2026's games to some career columns (win-loss, points, all-play) and not others (luck, deserved
    # wins, games clear) made every table that shows both stop adding up (adversarial review, 15 Oct
    # 2026). 2026's games count in head to head, which is labelled 2021-2026, and on its own page; the
    # season joins the careers when the final is written. Each manager carries his 2026 so far, apart.
    byname = {m['name']: m for m in out['mgrs']}
    for r in stand:
        m = byname.get(r['mgr'])
        if m: m['live'] = dict(w=r['w'], l=r['l'], t=r['t'], pf=r['pf'], pa=r['pa'])
    def _files():
        if not os.path.exists('yahoo_raw/2026/teams.json'): return None
        import teamfile
        return json.loads(json.dumps(teamfile.build(), default=str))
    def _wire():
        if not os.path.exists('draft_points.json'): return None
        import wire2026; dp = json.load(open('draft_points.json'))
        repl = None
        if os.path.exists('yahoo_raw/2026/rank_QB_0.json'):
            import teamfile
            repl = teamfile.replacement(2026, int(dp['weeks']['2026']))
        W = wire2026.grade(S26, dp.get('wk2026') or {}, int(dp['weeks']['2026']), games,
                           dp.get('allwk2026'), repl)
        # trade grading 2.0, side by side with the current way while Brian compares them (trade2.py)
        try:
            import trade2
            for x, g in zip(W['trades'], trade2.grade(2026, W['trades'], W['played'])): x['v2'] = g
        except Exception as e:
            print('  (trade 2.0 left out: %s)' % str(e)[:120], file=sys.stderr)
        return W
    up = [dict(wk=wk, ta=u[0], pa=u[1], tb=u[2], pb=u[3], aa=u[4] if len(u) > 4 else None, ab=u[5] if len(u) > 5 else None,
               status=u[6] if len(u) > 6 else 'preevent') for wk, lst in S26.UPCOMING2026.items() for u in lst]
    out['live'] = dict(year=2026, weeks=weeks, regWeeks=14, mgr=S26.MGR2026, games=games, standings=stand, upcoming=up,
                       trades=[dict(d=d, ta=a, ga=ga, tb=b, gb=gb) for (d, a, ga, b, gb) in S26.TRADES2026],
                       draft={'2026': [list(p) for p in S26.DRAFT2026], '2025': [list(p) for p in S26.DRAFT2025]},
                       asOf=getattr(S26, 'ASOF', 'Oct 14, 2026'),
                       # trades and the waiver wire graded by what each player has scored since (wire2026.py)
                       wire=_wire(),
                       # the team files and playoff odds, from every season Yahoo reaches (teamfile.py)
                       files=_files(),
                       # every drafted player's points under league scoring, and his finish at his position
                       draftPts=({k: v for k, v in json.load(open('draft_points.json')).items() if not k.startswith('allwk')}
                                 if os.path.exists('draft_points.json') else None))
    # every finished season since Yahoo, packaged like the live one, for the season pages
    if out['live'].get('files') and out['live']['files'].get('seasons'):
        out['seasonPages'] = out['live']['files'].pop('seasons')
    # which NFL franchise each manager is, on his whole career against its last ten seasons (nflcomps.py)
    import nflcomps
    out['comps'] = nflcomps.comps(out['rows'], out['games'])
    # against the crowd: every lineup and pickup graded against all of Yahoo (crowd.py); needs the Yahoo sign-in
    # the first time each week is read, and is left out (not an error) if Yahoo cannot be reached
    try:
        import crowd
        if os.path.exists('yahoo_raw/league_keys.json'):
            out['crowd'] = crowd.build()
            import netpts; out['netpts'] = netpts.build(out['crowd'])   # manager net points (netpts.py)
        import forecast; out['forecast'] = forecast.build()         # the rest of the live season, played out
    except Exception as e:
        print('  (against the crowd left out: %s)' % str(e)[:120], file=sys.stderr)   # stderr: deploy.sh hides stdout
    json.dump(out, open('site_data.json', 'w'), indent=1, separators=(',', ': '), default=lambda o: round(o, 4) if isinstance(o, float) else o)
    print('live 2026: weeks', weeks, '| teams', len(stand))
