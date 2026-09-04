/* Offline copy for the home-screen app. Written by the build, so VERSION changes
   whenever the page changes and an old store can never outlive its page.

   The page itself is fetched NETWORK FIRST. That is the whole point: a stored copy that
   is served first would leave every reader one launch behind every deploy, which is how
   a site like this quietly stops updating. The store is a fallback for no signal, and it
   is refreshed on every successful visit.

   Fonts and icons are the other way round -- they never change within a version, so they
   come from the store immediately and are only fetched once. */
const VERSION='deadshot-661905';
const CORE=['/','/index.html','/manifest.webmanifest','/favicon-32.png',
            '/favicon.svg','/apple-touch-icon.png','/icon-192.png','/icon-512.png'];
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

  /* the page: always try the network, fall back to the store only when it fails */
  if(r.mode==='navigate'||(url.origin===location.origin&&url.pathname==='/')){
    e.respondWith((async()=>{
      try{
        const net=await fetch(r);
        const c=await caches.open(VERSION); c.put('/',net.clone());
        return net;
      }catch(err){
        return (await caches.match('/'))||(await caches.match('/index.html'))||Response.error();
      }
    })());
    return;
  }

  /* fonts and our own static files: from the store first, fetched once */
  if(FONT.test(r.url)||url.origin===location.origin){
    e.respondWith((async()=>{
      const hit=await caches.match(r);
      if(hit)return hit;
      try{
        const net=await fetch(r);
        if(net&&(net.ok||net.type==='opaque')){
          const c=await caches.open(VERSION); c.put(r,net.clone());
        }
        return net;
      }catch(err){ return hit||Response.error(); }
    })());
  }
});
