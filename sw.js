/* Offline copy for the home-screen app. Written by the build, so VERSION changes
   whenever the page changes and an old store can never outlive its page.

   The page itself is fetched NETWORK FIRST. That is the whole point: a stored copy that
   is served first would leave every reader one launch behind every deploy, which is how
   a site like this quietly stops updating. The store is a fallback for no signal, and it
   is refreshed on every successful visit.

   Fonts and icons are the other way round -- they never change within a version, so they
   come from the store immediately and are only fetched once. */
const VERSION='deadshot-01a55be73441';
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
