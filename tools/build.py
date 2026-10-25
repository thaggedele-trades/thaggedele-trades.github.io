"""Build the published site from the encrypted source bundle (m/src.bin).

Applies the desk improvements (encrypted media, Lock button, lazy loading, chat split)
to the original page, then encrypts it with the existing salt so saved logins keep working.
"""
import datetime, gzip, hashlib, json, os, re
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from desk import J, b64d, b64e, enc, save_json, desk_parts, desk_with
import features

RECENT_DAYS = 60

LINKS_CSS = ("#ln{max-width:680px;margin:0 auto;padding:8px}"
  ".lnt input{width:100%;box-sizing:border-box;padding:10px 12px;border:1px solid var(--bd);border-radius:10px;background:transparent;color:var(--tx);font:inherit;font-size:16px;margin:4px 0 8px}"
  ".lns{display:flex;gap:6px;overflow-x:auto;padding-bottom:4px;scrollbar-width:none}"
  ".lns button{flex:none;background:none;border:1px solid var(--bd);color:var(--mu);border-radius:999px;padding:6px 11px;font:700 12px system-ui;cursor:pointer;white-space:nowrap}"
  ".lns button.on{color:var(--tx);border-color:var(--g)}"
  ".lnk{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}"
  ".lnk .ch{display:inline-flex;gap:5px;padding:4px 9px;border-radius:999px;border:1.5px solid transparent;background:linear-gradient(var(--bu),var(--bu)) padding-box,var(--ig) border-box;font:600 12.5px ui-monospace,monospace;cursor:pointer}"
  ".lnk .ch b{color:var(--g)}.lnk .ch.sel{background:var(--ig);color:#fff}.lnk .ch.sel b{color:#fff}"
  ".lnn{color:var(--mu);font-size:12px;margin:6px 2px 10px}"
  ".lnd{margin-left:auto;color:var(--mu);font-size:11.5px;max-width:38%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}"
  ".lnc .pcap{font-size:15px;overflow-wrap:anywhere}"
  ".lnm{display:block;width:100%;padding:11px;border:1px solid var(--bd);border-radius:12px;background:none;color:var(--tx);font:700 13px system-ui;cursor:pointer;margin:4px 0 24px}")

LINKS_JS = r"""let LN=false,LS='all',LT='',LM='',LQ='',LP=60;const ln=$('ln'),tL=$('tL');
const NEWS=/(^|\.)(yahoo|cnbc|reuters|bloomberg|wsj|marketwatch|investing|coindesk|cointelegraph|forbes|fool|benzinga|seekingalpha|barrons|nytimes|cnn|bbc|businessinsider|thestreet|theblock|investopedia|tipranks|stocktitan|newsbreak|newsbreakapp|ft|apnews|axios|decrypt|zerohedge|blockworks|usnews|finviz|economictimes|livemint|moneycontrol|ndtv|thehindu|bitcoinmagazine|theverge|techcrunch|politico|washingtonpost|theguardian|fortune|morningstar|kiplinger|investors|zacks|nasdaq|fxstreet|kitco|foxbusiness|nbcnews|cbsnews|abcnews|aljazeera|businesstoday|indiatimes|hindustantimes|coingape|dlnews|semafor|theinformation|electrek|teslarati|msn)\.[a-z.]+$/i;
const LRX=/(https?:\/\/[^\s<]+|www\.[^\s<]+)/i;
function lhost(u){try{return new URL(u.startsWith('http')?u:'https://'+u).hostname.replace(/^(www|m|amp)\./,'')}catch(e){return''}}
function lsrc(h){if(/(^|\.)(x|twitter)\.com$/.test(h))return'x';if(/(^|\.)(youtube\.com|youtu\.be)$/.test(h))return'yt';if(NEWS.test(h))return'news';return'other'}
const LSN={all:'All',x:'𝕏 Posts',yt:'▶ YouTube',news:'📰 News',other:'Other'};
function links(){const L=[];for(let ix=D.length-1;ix>=0;ix--){const u=(D[ix][3]||'').match(LRX);if(!u)continue;const h=lhost(u[0]);if(/thaggedele-trades/.test(h))continue;L.push([ix,h,lsrc(h)])}return L}
function showLN(){showPH(true);ph.hidden=true;tC.classList.remove('on');LN=true;ln.hidden=false;tL.classList.add('on');LP=60;rln();scrollTo({top:0})}
tL.onclick=()=>{LM='';showLN()};
function rln(){const L=links(),cnt={all:L.length,x:0,yt:0,news:0,other:0};L.forEach(x=>cnt[x[2]]++);
const tc=new Map();L.forEach(([ix])=>tick(D[ix][3]).forEach(t=>tc.set(t,(tc.get(t)||0)+1)));const lq=LQ.toLowerCase();
const F=L.filter(([ix,h,s])=>(LS=='all'||s==LS)&&(!LM||D[ix][2]==LM)&&(!LT||tick(D[ix][3]).has(LT))&&(!lq||D[ix][3].toLowerCase().includes(lq)||h.includes(lq)));
ln.textContent='';const top=document.createElement('div');top.className='lnt';
const inp=document.createElement('input');inp.type='search';inp.placeholder='Search links';inp.value=LQ;let tm;inp.oninput=()=>{clearTimeout(tm);tm=setTimeout(()=>{LQ=inp.value;LP=60;rln();const i2=ln.querySelector('input');i2.focus();try{i2.setSelectionRange(i2.value.length,i2.value.length)}catch(e){}},300)};top.append(inp);
const sr=document.createElement('div');sr.className='lns';for(const k in LSN){const b=document.createElement('button');b.type='button';b.textContent=LSN[k]+' '+cnt[k].toLocaleString();b.className=LS==k?'on':'';b.onclick=()=>{LS=k;LP=60;rln()};sr.append(b)}top.append(sr);
const tr=document.createElement('div');tr.className='lnk';[...tc].sort((a,b)=>b[1]-a[1]).slice(0,14).forEach(([t,n])=>{const s=document.createElement('span');s.className='ch'+(t==LT?' sel':'');s.innerHTML='$'+t+' <b>'+n+'</b>';s.onclick=()=>{LT=LT==t?'':t;LP=60;rln()};tr.append(s)});top.append(tr);
const nt=document.createElement('div');nt.className='lnn';nt.textContent=F.length.toLocaleString()+' links'+(LT?' · $'+LT:'')+(LM?' · by '+LM:'')+' · newest first'+(FULL?'':' · loading older…');top.append(nt);ln.append(top);
for(const [ix,h] of F.slice(0,LP)){const m=D[ix],k=document.createElement('div');k.className='pk lnc';const hd=document.createElement('div');hd.className='ph';const av=document.createElement('div');av.className='av';av.style.setProperty('--c',col(m[2]));av.textContent=m[2].replace(/\./g,'').slice(0,3);const b=document.createElement('b');b.style.color=col(m[2]);b.textContent=m[2];const sm=document.createElement('small');sm.textContent=m[0];const dm=document.createElement('span');dm.className='lnd';dm.textContent=h;hd.append(av,b,sm,dm);const cp=document.createElement('div');cp.className='pcap';TX(cp,m[3]);const a=document.createElement('a');a.className='sic';a.textContent='Show in chat';a.onclick=()=>nav(()=>{showPH(false);q.value='';f.value='';TK='';r();FULLP.then(()=>go('x'+D.indexOf(m)))});k.append(hd,cp,a);ln.append(k)}
if(F.length>LP){const mb=document.createElement('button');mb.type='button';mb.className='lnm';mb.textContent='Show more ('+(F.length-LP).toLocaleString()+' left)';mb.onclick=()=>{const y=scrollY;LP+=60;rln();scrollTo(0,y)};ln.append(mb)}
if(!F.length){const e=document.createElement('p');e.className='lnn';e.textContent='No links match.';ln.append(e)}}"""


def build(repo, key, src):
    h = src['desk']
    D0, _, MD0 = desk_parts(h)
    h = desk_with(h, D0, features.fomc_markers(MD0))
    gate = src['gate']
    C = json.loads(re.search(r'const C=(\{.*?\});', gate, re.S).group(1))

    def sub(old, new, count=1):
        nonlocal h
        n = h.count(old)
        assert n == count, (old, n)
        h = h.replace(old, new)


    LOADER = r"""<script>
    const TGK=(async()=>{let s=null;try{s=sessionStorage.getItem('tgl_s')||localStorage.getItem('tgl_k')}catch(e){}if(!s)throw 0;return crypto.subtle.importKey('raw',Uint8Array.from(atob(s),c=>c.charCodeAt(0)),'AES-GCM',false,['decrypt'])})();
    const MT={jpg:'image/jpeg',jpeg:'image/jpeg',png:'image/png',mp4:'video/mp4',mp3:'audio/mpeg'},LC=new Map();
    function LD(p){p=p.split('?')[0];if(!LC.has(p))LC.set(p,(async()=>{const r=await fetch('m/'+p.replace(/\//g,'_')+'.bin');if(!r.ok)throw r.status;const b=new Uint8Array(await r.arrayBuffer());const pt=await crypto.subtle.decrypt({name:'AES-GCM',iv:b.slice(0,12)},await TGK,b.slice(12));return URL.createObjectURL(new Blob([pt],{type:MT[p.split('.').pop()]||''}))})());return LC.get(p)}
    function SET(el,a,p){return LD(p).then(u=>{el[a]=u;if(a=='src'&&el.tagName=='VIDEO'&&el._vis)el.play().catch(()=>{})}).catch(()=>{})}
    const LIO='IntersectionObserver'in window?new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;LIO.unobserve(e.target);(e.target._lz||[]).forEach(([a,p])=>SET(e.target,a,p));e.target._lz=null}),{rootMargin:'800px 0px'}):null;
    function LZ(el,a,p){if(!LIO)return SET(el,a,p);(el._lz||(el._lz=[])).push([a,p]);LIO.observe(el)}
    document.addEventListener('DOMContentLoaded',()=>document.querySelectorAll('[data-p]').forEach(el=>LZ(el,'src',el.dataset.p)));
    </script>"""
    sub('<head>', '<head>' + LOADER)
    sub('<img src="img/bullbear-banner.jpg"', '<img data-p="img/bullbear-banner.jpg"')
    sub("el.poster='vid/'+a[1]+'.jpg';el.src='vid/'+a[1]+'.mp4';",
        "LZ(el,'poster','vid/'+a[1]+'.jpg');LZ(el,'src','vid/'+a[1]+'.mp4');")
    sub("el.src='img/'+a[1]+'.jpg'", "LZ(el,'src','img/'+a[1]+'.jpg')")
    sub("im.src='photos/'+m[5]", "LZ(im,'src','photos/'+m[5])", 2)
    sub("im.src='photos/'+D[ix][5]", "LZ(im,'src','photos/'+D[ix][5])")
    sub("es.forEach(e=>{e.isIntersecting?e.target.play()",
        "es.forEach(e=>{e.target._vis=e.isIntersecting;e.isIntersecting?e.target.play()")
    # music: fetch + decrypt only when first played
    sub('<audio id=au src="audio/music.mp3?v=5" loop preload=none></audio>', '<audio id=au loop preload=none></audio>')
    sub("b.onclick=()=>{a.paused?a.play().catch(()=>u(false)):a.pause()};",
        "let ld=false;b.onclick=async()=>{if(!a.paused){a.pause();return}if(!ld){b.textContent='⏳ Loading…';try{a.src=await LD('audio/music.mp3');ld=true}catch(e){b.textContent='🎵 Music';return}}a.play().catch(()=>{b.textContent='▶ Tap to play'})};")
    # lock button
    sub('<button id=mu type=button', '<button id=lk type=button aria-label="Lock desk" title="Lock desk">🔒</button><button id=mu type=button')
    sub('</style>', '#lk{background:none;border:1px solid var(--bd);color:var(--tx);border-radius:50%;width:36px;height:36px;padding:0;cursor:pointer;flex:none}@media(max-width:430px){.tb{gap:6px}.tb h1{font-size:21px!important;gap:4px}.dy{font-size:10.5px}#lk,#dm{width:32px!important;height:32px!important;font-size:14px}#mu{padding:6px 9px!important;font-size:12px!important}}</style>', count=h.count('</style>'))
    h = h.replace('</body>', "<script>document.getElementById('lk').onclick=()=>{if(!confirm('Lock the desk on this device? You will need the password again.'))return;try{localStorage.removeItem('tgl_k');sessionStorage.removeItem('tgl_s')}catch(e){}location.replace(location.pathname)};</script></body>", 1)
    assert "document.getElementById('lk')" in h

    # ---- split the chat: last RECENT_DAYS ship with the page, older messages load right after
    d0 = h.index('<script>const D=') + len('<script>const D=')
    D, d1 = json.JSONDecoder().raw_decode(h, d0)
    dt = lambda d: datetime.date(2000 + int(d.split('/')[2]), *map(int, d.split('/')[:2]))
    last = dt(D[-1][0])
    cut = next(i for i, x in enumerate(D) if (last - dt(x[0])).days <= RECENT_DAYS)
    old_blob = enc(key, gzip.compress(J(D[:cut]).encode(), 9, mtime=0))
    open(os.path.join(repo, 'm', 'chat.bin'), 'wb').write(old_blob)
    CHAT_URL = 'm/chat.bin?v=' + hashlib.sha256(old_blob).hexdigest()[:10]
    h = h[:d0] + J(D[cut:]) + h[d1:]
    members = sorted({x[2] for x in D})
    months = list(dict.fromkeys(f"20{x[0].split('/')[2]}-{x[0].split('/')[0].zfill(2)}" for x in D))
    sub("const S=[...new Set(D.map(m=>m[2]))].sort();", f"const S={J(members)};")
    sub("const months=[...new Set(D.map(m=>mk(m[0])))];", f"const months={J(months)};")
    sub("const dset=new Set(D.map(m=>m[0]));", f"const dset=new Set({J(list(dict.fromkeys(x[0] for x in D)))});")
    sub("D.length.toLocaleString()+' messages'", f"({len(D)}).toLocaleString()+' messages'+(FULL?'':' · loading older messages…')")
    sub("jm.onchange=()=>{if(jm.value)go(jm.value);jm.value=''};", "jm.onchange=()=>{const v=jm.value;jm.value='';if(v)FULLP.then(()=>go(v))};")
    sub("function jump(d){", "function jump(d){if(d==='old'&&!FULL){c.textContent='Loading older messages…';FULLP.then(()=>jump(d));return}")
    sub("<head><script>", "<head><script>let FULL=false,FR;const FULLP=new Promise(z=>FR=z);\n")
    # ---- Links tab: every shared link with its message, filter by source, ticker and search
    sub('<button id=tC aria-label=Levels>📈 Levels</button></div>',
        '<button id=tC aria-label=Levels>📈 Levels</button><button id=tL aria-label=Links>🔗 Links</button></div>')
    sub('<div id=ph hidden></div>', '<div id=ph hidden></div><div id=ln hidden></div>')
    sub('</style>', LINKS_CSS + '</style>', count=h.count('</style>'))
    sub("function showPH(on){PH=on;", "function showPH(on){LN=false;ln.hidden=true;tL.classList.remove('on');PH=on;")
    sub("\nr();</script>", "\n" + LINKS_JS + "\nr();</script>")
    features.patch(h, sub)
    FULL_JS = ("(async()=>{try{const get=()=>fetch('%s').then(z=>{if(!z.ok)throw z.status;return z.arrayBuffer()});const bf=await(window.TGC?window.TGC.catch(get):get());"
      "const b=new Uint8Array(bf);const pt=await crypto.subtle.decrypt({name:'AES-GCM',iv:b.slice(0,12)},await TGK,b.slice(12));"
      "const old=JSON.parse(await new Response(new Blob([pt]).stream().pipeThrough(new DecompressionStream('gzip'))).text());"
      "const cur=D.slice();D.length=0;for(const x of old)D.push(x);for(const x of cur)D.push(x);FULL=true;FR();"
      "if(LN)rln();else if(PH)rph();else{const y=scrollY;r();while(document.documentElement.scrollHeight<y+innerHeight*2&&rg());scrollTo(0,y)}"
      "}catch(e){window.TGC=null;c.textContent='Could not load older messages. Reload to try again.'}})();") % CHAT_URL
    sub("\nr();</script>", "\nr();" + FULL_JS + "</script>")

    # ---- encrypt page, keep salt + iterations
    iv = os.urandom(12)
    ct = AESGCM(key).encrypt(iv, gzip.compress(h.encode(), 9, mtime=0), None)
    C2 = {'s': C['s'], 'v': b64e(iv), 'i': C['i'], 'c': b64e(ct)}

    # ---- patch the gate
    g = re.sub(r'const C=\{.*?\};', lambda m: 'const C=' + json.dumps(C2) + ';', gate, count=1, flags=re.S)
    def gsub(old, new):
        nonlocal g
        assert g.count(old) == 1, old
        g = g.replace(old, new)
    gsub("if(save){const raw=new Uint8Array(await crypto.subtle.exportKey('raw',key));localStorage.setItem('tgl_k',btoa(String.fromCharCode(...raw)))}",
         "const raw=btoa(String.fromCharCode(...new Uint8Array(await crypto.subtle.exportKey('raw',key))));if(save)localStorage.setItem('tgl_k',raw);try{sessionStorage.setItem('tgl_s',raw)}catch(x){}")
    gsub("(async()=>{const s=", "const OK=!!(window.crypto&&crypto.subtle&&window.DecompressionStream);if(!OK){e.textContent='This browser is too old to open the desk. Please update it, or use current Chrome or Safari.';fm.querySelector('button').disabled=true}\n(async()=>{if(!OK)return;const s=")
    gsub("catch(x){e.textContent='Wrong password.'}",
         "catch(x){e.textContent=x&&x.name==='OperationError'?'Wrong password.':'Could not open the desk. Please reload and try again.'}")
    gsub('<title>Thaggedele Traders</title>', '<title>Thaggedele Traders</title>' + features.PWA_HEAD)
    import theme
    theme.patch_gate(gsub)
    gsub("const d=s=>", "window.TGC=fetch('%s').then(z=>{if(!z.ok)throw 0;return z.arrayBuffer()});window.TGC.catch(()=>{});\nconst d=s=>" % CHAT_URL)
    open(os.path.join(repo, 'index.html'), 'w', encoding='utf-8').write(g)
    save_json(key, os.path.join(repo, 'm', 'src.bin'), src)
    return len(D), cut
