"""Desk features added on top of the original page: ticker pages, the weekly summary with
upcoming market events, saved messages, and install-as-app support."""
import json

J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))

# Upcoming market events (from federalreserve.gov FOMC calendar and bls.gov release schedules).
# Times are US Eastern. Add new years here; past dates simply stop showing.
EVENTS = [
    ["10/28/26", "FOMC decision", "2:00 PM"], ["11/6/26", "Jobs report (Oct)", "8:30 AM"],
    ["11/10/26", "CPI (Oct)", "8:30 AM"], ["12/4/26", "Jobs report (Nov)", "8:30 AM"],
    ["12/9/26", "FOMC decision + projections", "2:00 PM"], ["12/10/26", "CPI (Nov)", "8:30 AM"],
    ["1/8/27", "Jobs report (Dec)", "8:30 AM"], ["1/13/27", "CPI (Dec)", "8:30 AM"],
    ["1/27/27", "FOMC decision", "2:00 PM"], ["2/5/27", "Jobs report (Jan)", "8:30 AM"],
    ["2/11/27", "CPI (Jan)", "8:30 AM"], ["3/5/27", "Jobs report (Feb)", "8:30 AM"],
    ["3/10/27", "CPI (Feb)", "8:30 AM"], ["3/17/27", "FOMC decision + projections", "2:00 PM"],
    ["4/2/27", "Jobs report (Mar)", "8:30 AM"], ["4/13/27", "CPI (Mar)", "8:30 AM"],
    ["4/28/27", "FOMC decision", "2:00 PM"], ["5/7/27", "Jobs report (Apr)", "8:30 AM"],
    ["5/12/27", "CPI (Apr)", "8:30 AM"], ["6/4/27", "Jobs report (May)", "8:30 AM"],
    ["6/9/27", "FOMC decision + projections", "2:00 PM"], ["6/10/27", "CPI (May)", "8:30 AM"],
    ["7/2/27", "Jobs report (Jun)", "8:30 AM"], ["7/14/27", "CPI (Jun)", "8:30 AM"],
    ["7/28/27", "FOMC decision", "2:00 PM"], ["8/6/27", "Jobs report (Jul)", "8:30 AM"],
    ["8/11/27", "CPI (Jul)", "8:30 AM"], ["9/3/27", "Jobs report (Aug)", "8:30 AM"],
    ["9/14/27", "CPI (Aug)", "8:30 AM"], ["9/15/27", "FOMC decision + projections", "2:00 PM"],
    ["10/8/27", "Jobs report (Sep)", "8:30 AM"], ["10/14/27", "CPI (Sep)", "8:30 AM"],
    ["10/27/27", "FOMC decision", "2:00 PM"], ["11/5/27", "Jobs report (Oct)", "8:30 AM"],
    ["11/10/27", "CPI (Oct)", "8:30 AM"], ["12/3/27", "Jobs report (Nov)", "8:30 AM"],
    ["12/8/27", "FOMC decision + projections", "2:00 PM"], ["12/10/27", "CPI (Nov)", "8:30 AM"],
]


def fomc_markers(MD):
    """Add future FOMC decision days to the chat's market-day markers (shown once the chat reaches them)."""
    have = {d for d, _ in MD}
    return MD + [[d, 'FOMC decision'] for d, l, _ in EVENTS if l.startswith('FOMC') and d not in have]


PWA_HEAD = ('<link rel=manifest href=manifest.json><link rel=apple-touch-icon href=icon-180.png>'
            '<meta name=apple-mobile-web-app-capable content=yes><meta name=mobile-web-app-capable content=yes>'
            '<meta name=apple-mobile-web-app-title content="TGL Traders"><meta name=theme-color content="#F5F6F3">')

CSS = (
    # tabs: four across on phones
    "@media(max-width:430px){.tabs button{font-size:11.5px!important;letter-spacing:.4px!important;padding:8px 2px!important}}"
    # ticker page card
    ".tkc{background:var(--pn);border:1px solid var(--bd);border-radius:16px;padding:14px;margin:8px 0 14px;box-shadow:0 2px 12px #0000001a}"
    ".tkc h2{all:unset;display:block;font:800 26px ui-monospace,monospace}"
    ".tkc .st{color:var(--mu);font-size:13px;margin:2px 0 10px}"
    ".tkc svg{display:block;width:100%;height:auto;margin:4px 0 2px}.tkc .hit{cursor:pointer}.tkc .hit:hover{fill:rgba(127,127,127,.15)}"
    ".tkc .ax{display:flex;justify-content:space-between;color:var(--mu);font-size:11px;margin-bottom:10px}"
    ".tkc .wh{font-size:13px;margin:0 0 10px}.tkc .wh b{margin-right:10px}"
    ".tkb{display:flex;gap:8px;flex-wrap:wrap}"
    ".tkb button{border:1px solid var(--bd);background:var(--bu);color:var(--tx);border-radius:999px;padding:7px 12px;font:700 13px system-ui;cursor:pointer}"
    # weekly card
    "#wk .row{font-size:14px;margin:6px 0;line-height:1.45}#wk .row>b:first-child{color:var(--mu);font-size:12px;text-transform:uppercase;letter-spacing:.8px;display:block}"
    "#wk .ch{margin:3px 3px 0 0}#wk a{color:#0095f6;text-decoration:none}#wk .lk{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}"
    "#wk .ev{display:flex;gap:8px;align-items:baseline}#wk .ev span:first-child{min-width:82px;font-weight:700}#wk .ev small{color:var(--mu)}"
    "#wk .lv{border:0;background:none;color:#0095f6;font:inherit;padding:0;cursor:pointer}"
    ".ih{display:flex;gap:8px;align-items:center;font-size:13px;background:var(--bu);border-radius:10px;padding:8px 10px;margin:0 0 8px}"
    ".ih span{flex:1}.ih button{border:0;background:none;color:var(--mu);font-size:16px;cursor:pointer}.ih .go{color:#fff;background:var(--ig);border-radius:999px;font:700 12px system-ui;padding:6px 11px}"
    # saved
    ".m i .sv{border:0;background:none;padding:0 0 0 8px;margin:0;font-size:15px;line-height:1;color:var(--mu);cursor:pointer;vertical-align:-1px}"
    ".m i .sv.on{color:#f5b301}"
    ".bk{position:fixed;left:14px;bottom:22px;z-index:40;border:0;border-radius:999px;padding:11px 16px;font:700 14px system-ui;color:#fff;background:var(--ig);box-shadow:0 4px 16px #0005;cursor:pointer;max-width:55vw;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.bk[hidden]{display:none}"
    ".pf{margin:2px 0 12px}.pft{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 8px}.pft span{background:var(--bu);border:1px solid var(--bd);border-radius:999px;padding:4px 10px;font:600 12.5px system-ui}"
    ".pfl{font-size:13.5px;margin:3px 0;line-height:1.4}.pfl .pfi{display:inline-block;width:22px}.pfl b{color:var(--mu);font-weight:700}.pfn{color:var(--mu);font-size:11px;margin-top:6px}"
    ".r .av,.m>b,.ph .av,.ph>b{cursor:pointer}#wk .lv.mb{font-weight:800;text-decoration:underline dotted}#wk .tip{color:var(--mu);font-size:12px;margin:-2px 0 6px}"
    "#svp{max-width:680px;margin:0 auto;padding:8px}"
    # readable links in dark mode
    "body:not(.lt) .m a,body:not(.lt) .pcap a,body:not(.lt) #wk a,body:not(.lt) #wk .lv,body:not(.lt) .sic{color:#5cb8ff}"
)

JS = r"""
const EV=__EV__;let PTK='',PMB='',SV=false,SVD=new Set();try{SVD=new Set(JSON.parse(localStorage.getItem('tgl_sv')||'[]'))}catch(e){}
const dd=s=>{const p=s.split('/');return new Date(2000+ +p[2],p[0]-1,+p[1])};
const esc=s=>String(s).replace(/[&<>"]/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[ch]));
function el(t,c,x){const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e}
// ---- ticker page
function tkCard(t){const mo=new Map(),who=new Map();let n=0,first='',last='',nl=0,np=0;
const fw=f.value;for(const m of D){const s=m[3]||'';if(fw&&m[2]!==fw)continue;if(!tick(s).has(t))continue;n++;if(!first)first=m[0];last=m[0];const k=mk(m[0]);mo.set(k,(mo.get(k)||0)+1);who.set(m[2],(who.get(m[2])||0)+1);if(LRX.test(s)&&!/thaggedele-trades/.test(s))nl++;if(m[5])np++}
const k=el('div','tkc');k.append(el('h2','','$'+t+(fw?' · '+fw:'')));
k.append(el('div','st',n?n.toLocaleString()+' messages · first '+first+' · last '+last+(FULL?'':' · loading older…'):'No messages yet'));
if(n){const ms=months.slice(months.indexOf(mk(first))),W=600,H=110,bw=W/ms.length,mx=Math.max(...ms.map(x=>mo.get(x)||0));
let s='<svg viewBox="0 0 '+W+' '+(H+4)+'" role="img" aria-label="Messages per month mentioning '+t+'">';
ms.forEach((x,i)=>{const v=mo.get(x)||0,h=v?Math.max(2,v/mx*H):0;s+='<rect x="'+(i*bw+bw*.15).toFixed(1)+'" y="'+(H-h).toFixed(1)+'" width="'+(bw*.7).toFixed(1)+'" height="'+h.toFixed(1)+'" rx="1.5" fill="var(--acc)"><title>'+ml(x)+': '+v+'</title></rect>'});
ms.forEach((x,i)=>{const v=mo.get(x);if(v)s+='<rect class="hit" data-k="'+x+'" x="'+(i*bw).toFixed(1)+'" y="0" width="'+bw.toFixed(1)+'" height="'+(H+4)+'" fill="transparent"><title>'+ml(x)+': '+v+' messages. Tap to open</title></rect>'});s+='<line x1="0" y1="'+H+'" x2="'+W+'" y2="'+H+'" stroke="var(--bd)"/></svg>';const sv=el('div');sv.innerHTML=s;sv.onclick=e=>{const h2=e.target.closest('[data-k]');if(h2)jumpMonth(h2.dataset.k)};k.append(sv);
const ax=el('div','ax');ax.append(el('span','',ml(ms[0])),el('span','','tap a bar to open that month'),el('span','',ml(ms[ms.length-1])));k.append(ax);
const wh=el('div','wh');wh.append(el('span','','Most active: '));[...who].sort((a,b)=>b[1]-a[1]).slice(0,5).forEach(([w,c2])=>{const b=el('b','',w+' '+c2);b.style.color=col(w);wh.append(b)});k.append(wh)}
const bt=el('div','tkb');if(nl){const b=el('button','',nl+' link'+(nl>1?'s':''));b.type='button';b.onclick=()=>nav(()=>{LT=t;LM='';LS='all';LQ='';showLN()});bt.append(b)}
if(np){const b=el('button','',np+' chart'+(np>1?'s':''));b.type='button';b.onclick=()=>nav(()=>{PTK=t;PMB='';showPH(true);rph();scrollTo({top:0})});bt.append(b)}
const cl=el('button','','✕ Clear');cl.type='button';cl.onclick=()=>setTK('');bt.append(cl);k.append(bt);return k}
// ---- weekly summary + upcoming events
function wkr(){const W=$('wk');if(!W||!D.length)return;const nd=dd(D[D.length-1][0]),wk=D.filter(m=>(nd-dd(m[0]))/864e5<7);W.textContent='';
const h=el('h3','','This week on the desk');W.append(h);
let ih=null;try{ih=localStorage.getItem('tgl_ih')}catch(e){}const sa=matchMedia('(display-mode: standalone)').matches||navigator.standalone;
if(!ih&&!sa){const b=el('div','ih');const ios=/iPhone|iPad|iPod/.test(navigator.userAgent);b.append(el('span','',ios?'Add the desk to your Home Screen: tap Share, then “Add to Home Screen”.':'Add the desk to your home screen: open the browser menu ⋮, then “Add to Home screen”.'));
if(window.BIP){const g=el('button','go','Install');g.onclick=async()=>{BIP.prompt();try{await BIP.userChoice}catch(e){}b.remove()};b.append(g)}
const x=el('button','','✕');x.setAttribute('aria-label','Dismiss');x.onclick=()=>{try{localStorage.setItem('tgl_ih','1')}catch(e){}b.remove()};b.append(x);W.append(b)}
const who=new Map();let np=0;wk.forEach(m=>{who.set(m[2],(who.get(m[2])||0)+1);if(m[5])np++});
const r1=el('div','row');r1.append(el('b','','Activity'));r1.append(wk.length.toLocaleString()+' messages from '+who.size+' members · ');
const top=[...who].sort((a,b)=>b[1]-a[1]).slice(0,3);top.forEach(([w,c2],i)=>{const b=el('button','lv mb',w);b.style.color=col(w);b.onclick=()=>nav(()=>openMember(w));r1.append(b,' '+c2+(i<top.length-1?', ':''))});
if(np){r1.append(' · ');const lv=el('button','lv',np+' new chart'+(np>1?'s':''));lv.onclick=()=>nav(()=>{PTK='';PMB='';showPH(true);rph();scrollTo({top:0})});r1.append(lv)}W.append(r1);W.append(el('div','tip','Tap any member’s initials, here or in the chat, to open their page.'));
if(BOARD.w.length){const r2=el('div','row');r2.append(el('b','','Hot tickers'));BOARD.w.slice(0,6).forEach(([t,n])=>{const s=el('span','ch');s.innerHTML='$'+esc(t)+' <b>'+n+'</b>';s.onclick=()=>nav(()=>setTK(t));r2.append(s)});W.append(r2)}
const L=[];for(let i=wk.length-1;i>=0&&L.length<3;i--){const u=(wk[i][3]||'').match(LRX);if(u&&!/thaggedele-trades/.test(u[0]))L.push([u[0],wk[i]])}
if(L.length){const r3=el('div','row');r3.append(el('b','','Latest links'));L.forEach(([u,m])=>{const a=el('a','lk');a.href=u.startsWith('http')?u:'https://'+u;a.target='_blank';a.rel='noopener noreferrer';const tx=(m[3]||'').replace(LRX,'').trim();a.textContent=lhost(u)+(tx?' — '+tx.slice(0,70):'');r3.append(a)});const more=el('button','lv','All links →');more.onclick=()=>nav(()=>{LT='';LM='';LS='all';LQ='';showLN()});r3.append(more);W.append(r3)}
const now=new Date();now.setHours(0,0,0,0);const up=EV.filter(e=>dd(e[0])>=now).slice(0,4);
if(up.length){const r4=el('div','row');r4.append(el('b','','Coming up (ET)'));up.forEach(([d,l,t])=>{const x=dd(d),e=el('div','ev');e.append(el('span','',x.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric'})),el('span','',l),el('small','',t));r4.append(e)});W.append(r4)}}
addEventListener('beforeinstallprompt',e=>{e.preventDefault();window.BIP=e;wkr()});

const BK=el('button','bk');BK.type='button';BK.hidden=true;document.body.append(BK);
// ---- back navigation: every jump from a card, chart, link or name can be undone
const NV=[];let NVP=0;try{history.scrollRestoration='manual'}catch(e){}
function snap(){return{v:LN?'ln':SV?'sv':PH?'ph':'chat',TK,f:f.value,q:q.value,LT,LM,LS,LQ,LP,PTK,PMB,PV,y:scrollY}}
function nlab(s){return s.v=='ln'?'Links'+(s.LM?' · '+s.LM:s.LT?' · $'+s.LT:''):s.v=='ph'?'Levels'+(s.PMB?' · '+s.PMB:s.PTK?' · $'+s.PTK:''):s.v=='sv'?'Saved':s.TK?'$'+s.TK+(s.f?' · '+s.f:''):s.f?s.f:s.q?'your search':'the chat'}
function bkShow(){if(NV.length){BK.textContent='↩ Back to '+nlab(NV[NV.length-1]);BK.hidden=false}else BK.hidden=true}
function nav(fn){const s=snap();fn();NV.push(s);if(NV.length>30)NV.shift();try{history.pushState({tgbk:1},'');NVP++}catch(e){}bkShow()}
function restore(s){q.value=s.q;f.value=s.f;TK=s.TK;LT=s.LT;LM=s.LM;LS=s.LS;LQ=s.LQ;PTK=s.PTK;PMB=s.PMB;PV=s.PV;
if(s.v=='ln'){showLN();LP=s.LP;rln()}else if(s.v=='ph'){showPH(true);rph()}else if(s.v=='sv'){showSV()}else{if(PH)showPH(false);r();while(document.documentElement.scrollHeight<s.y+innerHeight*1.5&&rg());}
const y=s.y;scrollTo(0,y);setTimeout(()=>scrollTo(0,y),80)}
function navBack(){const s=NV.pop();if(s)restore(s);bkShow()}
BK.onclick=()=>{if(NVP>0)history.back();else navBack()};
addEventListener('popstate',()=>{if(NVP>0)NVP--;if(NV.length)navBack()});
function jumpMonth(k){nav(()=>FULLP.then(()=>{if(PH)showPH(false);go('M'+k);const hh=(document.querySelector('.top')||{}).offsetHeight||0;scrollBy(0,-hh-6)}))}

// ---- auto-built trading profile (from chat activity only)
const STY=[['Options trader',/\b(calls?|puts?|strikes?|expiry|0 ?dte|leaps?|premium|theta|spreads?|covered calls?|csp|otm|itm)\b/i],
['Crypto',/\b(btc|eth|sol|xrp|crypto|bitcoin|altcoins?|doge|blockchain)\b/i],
['Leveraged ETFs',/\b(mstu|mstx|mstz|soxl|soxs|tqqq|sqqq|tna|tza|ethu|bmnu|nvdl|tsll|conl|upro|spxl|fngu|labu|nvdu|amdl)\b/i],
['Day trader',/\b(scalp\w*|day ?trad\w*|intraday|[15] ?min|entered|exited|took profits?|booked|stopped out|stop ?loss)\b/i],
['Long-term investor',/\b(long ?term|accumulat\w*|dca|retirement|roth|401k|buy and hold|hodl)\b/i],
['Income plays',/\b(msty|yieldmax|dividends?|covered calls?|income|yield)\b/i],
['Macro watcher',/\b(fed|fomc|cpi|ppi|yields?|treasur\w*|inflation|rate (cut|hike)s?|jobs report|nfp|powell|gdp|recession)\b/i],
['Technical analysis',/\b(support|resistance|breakout|rsi|macd|ema|sma|vwap|fib\w*|levels?|trend ?line|pattern)\b/i]];
const SEC=[['AI chips',/^(NVDA|AMD|AVGO|TSM|SMCI|MRVL|INTC|ARM|MU|ASML|LRCX|SOXL|QCOM|DELL)$/],['Bitcoin & crypto',/^(BTC|ETH|SOL|XRP|ADA|XLM|COIN|MSTR|MSTU|MSTY|MSTX|MSTZ|BMNR|BMNU|ETHU|IBIT|STRK|HOOD|CRCL|SBET|CLSK|MARA)$/],
['Big tech',/^(AAPL|MSFT|GOOGL|GOOG|META|AMZN|NFLX|ORCL|CRM|ADBE|IBM)$/],['Tesla & EVs',/^(TSLA|RIVN|NIO|TSLL)$/],['AI infrastructure',/^(CRWV|NBIS|IREN|ORCL|OKLO|APLD|WULF)$/],
['Quantum',/^(IONQ|RGTI|QBTS|QUBT)$/],['Indexes & volatility',/^(SPX|SPY|QQQ|IWM|VIX|TQQQ|SQQQ|TNA|DIA)$/],['Meme stocks',/^(GME|AMC|DJT|BBAI|SOUN)$/],['Space',/^(RKLB|ASTS|LUNR)$/],['China',/^(BABA|PDD|NIO)$/]];
let BASE=null,BASEN=0;
function hr(t){const p=t.split(/[:\s ]/);let h=+p[0]%12;if(/PM/.test(t))h+=12;return h+(+p[1])/60}
function base(){if(BASE&&BASEN===D.length)return BASE;const per=new Map();for(const m of D){let e=per.get(m[2]);if(!e)per.set(m[2],e={n:0,c:STY.map(()=>0)});e.n++;const s=m[3]||'';STY.forEach(([,rx],i)=>{if(rx.test(s))e.c[i]++})}
const R=[...per.values()].filter(e=>e.n>=20);BASE=STY.map((_,i)=>{const v=R.map(e=>e.c[i]/e.n).sort((a,b)=>a-b);return v.length?v[Math.floor(v.length/2)]:0.01});BASEN=D.length;return BASE}
function profile(w){const B=base();let n=0,lk=0,ph=0;const c=STY.map(()=>0),sc=new Map(),hb={pre:0,mkt:0,aft:0,night:0},dw=[0,0,0,0,0,0,0];let first='';
for(const m of D){if(m[2]!==w)continue;const s=m[3]||'';n++;if(!first)first=m[0];STY.forEach(([,rx],i)=>{if(rx.test(s))c[i]++});if(LRX.test(s))lk++;if(m[5])ph++;
tick(s).forEach(t=>{for(const [nm,rx] of SEC)if(rx.test(t)){sc.set(nm,(sc.get(nm)||0)+1);break}});const h=hr(m[1]);hb[h<4?'night':h<9.5?'pre':h<16?'mkt':h<20?'aft':'night']++;dw[dd(m[0]).getDay()]++}
if(n<5)return null;const tags=[];STY.forEach(([nm],i)=>{const sh=c[i]/n;if(sh>=.03&&sh>=B[i]*1.25)tags.push([nm,sh/B[i]])});tags.sort((a,b)=>b[1]-a[1]);if(tags.length<2){STY.map(([nm],i)=>[nm,c[i]/n]).filter(x=>x[1]>=.05&&!tags.some(t=>t[0]==x[0])).sort((a,b)=>b[1]-a[1]).slice(0,2-tags.length).forEach(x=>tags.push(x))}
const T=tags.slice(0,4).map(x=>x[0]);if(lk/n>.25)T.push('News sharer');if(ph>=3)T.push('Chart poster');
const HL={pre:'pre-market',mkt:'market hours',aft:'after the close',night:'late night'};const hs=Object.entries(hb).sort((a,b)=>b[1]-a[1]);
const DN=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],bd=dw.indexOf(Math.max(...dw));
const secs=[...sc].sort((a,b)=>b[1]-a[1]).slice(0,3).map(x=>x[0]);const yrs=(dd(D[D.length-1][0])-dd(first))/31557600000;const wks=Math.max(1,yrs*52.18);
return {T,active:HL[hs[0][0]]+' ('+Math.round(hs[0][1]/n*100)+'%)'+(hs[1][1]/n>.2?', then '+HL[hs[1][0]]+' ('+Math.round(hs[1][1]/n*100)+'%)':''),day:DN[bd],secs,since:first,yrs,pw:n/wks}}
function profEl(w){const P=profile(w);if(!P)return null;const d=el('div','pf');
if(P.T.length){const t=el('div','pft');P.T.forEach(x=>t.append(el('span','',x)));d.append(t)}
const ln=(ic,lab,val)=>{const r2=el('div','pfl');r2.append(el('b','',lab+' '),val);d.append(r2)};
ln('','Most active (ET):',P.active+' · busiest on '+P.day+'s');if(P.secs.length)ln('','Focus:',P.secs.join(', '));
ln('','Member since:',ml(mk(P.since))+' ('+(P.yrs<1?Math.max(1,Math.round(P.yrs*12))+' mo':P.yrs.toFixed(1)+' yrs')+') · '+(P.pw<1?'':'about ')+(P.pw<1?'less than 1 message':Math.round(P.pw)+' messages')+' a week');
d.append(el('div','pfn','Auto-generated from chat activity. Updates with each export.'));return d}
// ---- member pages
function mbCard(w){const mo=new Map(),tc=new Map();let n=0,first='',last='',nl=0,np=0;
for(const m of D){if(m[2]!==w)continue;const s=m[3]||'';n++;if(!first)first=m[0];last=m[0];const k=mk(m[0]);mo.set(k,(mo.get(k)||0)+1);tick(s).forEach(t=>tc.set(t,(tc.get(t)||0)+1));if(LRX.test(s)&&!/thaggedele-trades/.test(s))nl++;if(m[5])np++}
const k=el('div','tkc');const h=el('h2','',w);h.style.color=col(w);k.append(h);
k.append(el('div','st',n?n.toLocaleString()+' messages ('+(n/D.length*100).toFixed(1)+'% of the chat) · first '+first+' · last '+last+(FULL?'':' · loading older…'):'No messages'));
{const pe=profEl(w);if(pe)k.append(pe)}
if(n){const ms=months.slice(months.indexOf(mk(first))),W=600,H=110,bw=W/ms.length,mx=Math.max(...ms.map(x=>mo.get(x)||0));
let s='<svg viewBox="0 0 '+W+' '+(H+4)+'" role="img" aria-label="Messages per month by '+esc(w)+'">';
ms.forEach((x,i)=>{const v=mo.get(x)||0,hh=v?Math.max(2,v/mx*H):0;s+='<rect x="'+(i*bw+bw*.15).toFixed(1)+'" y="'+(H-hh).toFixed(1)+'" width="'+(bw*.7).toFixed(1)+'" height="'+hh.toFixed(1)+'" rx="1.5" fill="'+col(w)+'"><title>'+ml(x)+': '+v+'</title></rect>'});
ms.forEach((x,i)=>{const v=mo.get(x);if(v)s+='<rect class="hit" data-k="'+x+'" x="'+(i*bw).toFixed(1)+'" y="0" width="'+bw.toFixed(1)+'" height="'+(H+4)+'" fill="transparent"><title>'+ml(x)+': '+v+' messages. Tap to open</title></rect>'});s+='<line x1="0" y1="'+H+'" x2="'+W+'" y2="'+H+'" stroke="var(--bd)"/></svg>';const sv=el('div');sv.innerHTML=s;sv.onclick=e=>{const h2=e.target.closest('[data-k]');if(h2)jumpMonth(h2.dataset.k)};k.append(sv);
const ax=el('div','ax');ax.append(el('span','',ml(ms[0])),el('span','','tap a bar to open that month'),el('span','',ml(ms[ms.length-1])));k.append(ax);
const top=[...tc].sort((a,b)=>b[1]-a[1]).slice(0,8);if(top.length){const tr=el('div','wh');tr.append(el('span','','Talks about most: '));const ck=el('div','lnk');top.forEach(([t,c2])=>{const x=el('span','ch');x.innerHTML='$'+esc(t)+' <b>'+c2+'</b>';x.onclick=()=>nav(()=>setTK(t));ck.append(x)});tr.append(ck);k.append(tr)}}
const bt=el('div','tkb');if(np){const b=el('button','',np+' chart'+(np>1?'s':''));b.type='button';b.onclick=()=>nav(()=>{PMB=w;PTK='';showPH(true);rph();scrollTo({top:0})});bt.append(b)}
if(nl){const b=el('button','',nl+' link'+(nl>1?'s':''));b.type='button';b.onclick=()=>nav(()=>{LM=w;LT='';LS='all';LQ='';showLN()});bt.append(b)}
const cl=el('button','','✕ Clear');cl.type='button';cl.onclick=()=>{f.value='';r();scrollTo({top:0})};bt.append(cl);k.append(bt);return k}
function openMember(w){if(!w)return;if(PH)showPH(false);TK='';q.value='';f.value=w;if(f.value!==w)return;r();const k=document.querySelector('.tkc');if(k){const hh=(document.querySelector('.top')||{}).offsetHeight||0;scrollTo({top:k.getBoundingClientRect().top+scrollY-hh-8})}}
document.addEventListener('click',e=>{const a=e.target.closest('.r .av,.m>b,.ph .av,.ph>b');if(!a||e.target.closest('.tkc'))return;const box=a.closest('.r,.ph');const b=box&&box.querySelector('.m>b,.ph>b');if(b)nav(()=>openMember(b.textContent))});
// ---- saved messages
const SK=m=>m[0]+'|'+m[1]+'|'+m[2]+'|'+(m[3]||'').slice(0,24);
function svSave(){try{localStorage.setItem('tgl_sv',JSON.stringify([...SVD]))}catch(e){}}
function svBtn(m){const k=SK(m),b=el('button','sv'+(SVD.has(k)?' on':''),SVD.has(k)?'★':'☆');b.type='button';b.setAttribute('aria-label','Save message');b.onclick=ev=>{ev.stopPropagation();if(SVD.has(k))SVD.delete(k);else SVD.add(k);svSave();b.textContent=SVD.has(k)?'★':'☆';b.classList.toggle('on',SVD.has(k));if(SV)rsv()};return b}
const svp=$('svp'),tS=$('tS');
function showSV(){showPH(true);ph.hidden=true;tC.classList.remove('on');SV=true;svp.hidden=false;tS.classList.add('on');rsv();scrollTo({top:0})}
tS.onclick=showSV;
function rsv(){svp.textContent='';const S2=[];for(let ix=D.length-1;ix>=0;ix--)if(SVD.has(SK(D[ix])))S2.push(ix);
svp.append(el('div','lnn',S2.length?S2.length+' saved · on this phone only'+(FULL?'':' · loading older…'):'Tap ☆ next to any message’s time to save it here. Saved messages stay on this phone only.'));
for(const ix of S2){const m=D[ix],k=el('div','pk lnc'),hd=el('div','ph'),av=el('div','av',m[2].replace(/\./g,'').slice(0,3));av.style.setProperty('--c',col(m[2]));const b=el('b','',m[2]);b.style.color=col(m[2]);hd.append(av,b,el('small','',m[0]+' · '+m[1]));const un=el('button','sv on','★');un.type='button';un.style.cssText='margin-left:auto;border:0;background:none;font-size:18px;color:#f5b301;cursor:pointer';un.setAttribute('aria-label','Remove from saved');un.onclick=()=>{SVD.delete(SK(m));svSave();rsv()};hd.append(un);
const cp=el('div','pcap');TX(cp,m[3]||'📷');const a=el('a','sic','Show in chat');a.onclick=()=>nav(()=>{showPH(false);q.value='';f.value='';TK='';r();FULLP.then(()=>go('x'+D.indexOf(m)))});k.append(hd,cp,a);svp.append(k)}}
"""


def patch(h, sub):
    """Apply the features to the desk page. `sub` is build.py's checked replace."""
    sub('</style>', CSS + '</style>', count=h.count('</style>'))
    sub('<title>Thaggedele Traders</title>', '<title>Thaggedele Traders</title>' + PWA_HEAD)
    sub('<button id=tL aria-label=Links>🔗 Links</button></div>',
        '<button id=tL aria-label=Links>🔗 Links</button><button id=tS aria-label=Saved>★ Saved</button></div>')
    sub('<div id=ln hidden></div>', '<div id=ln hidden></div><div id=svp hidden></div>')
    sub('<div class=wr><div class=bd><h3>🔥 Most-talked-about tickers</h3>',
        '<div class=wr><div class=bd id=wk></div></div><div class=wr><div class=bd><h3>🔥 Most-talked-about tickers</h3>')
    sub("function showPH(on){LN=false;", "function showPH(on){SV=false;svp.hidden=true;tS.classList.remove('on');const wkc=$('wk');if(wkc)wkc.parentElement.hidden=on||!!TK||!!f.value;LN=false;")
    sub("TX(e,m[3]);const i=document.createElement('i');i.textContent=m[1];e.append(i);",
        "TX(e,m[3]);const i=document.createElement('i');i.textContent=m[1];i.append(svBtn(m));e.append(i);")
    sub("a.onclick=()=>{showPH(false);q.value='';f.value='';TK='';r();go('x'+ix)}", "a.onclick=()=>nav(()=>{showPH(false);q.value='';f.value='';TK='';r();go('x'+ix)})")
    sub("if(t&&!t.classList.contains('ch')){setTK(t.dataset.t);return}", "if(t&&!t.classList.contains('ch')){nav(()=>setTK(t.dataset.t));return}")
    sub("rg();fill()}", "if(TK)o.prepend(tkCard(TK));else if(f.value)o.prepend(mbCard(f.value));const wkc=$('wk');if(wkc)wkc.parentElement.hidden=!!TK||!!f.value;rg();fill()}")
    sub("function setTK(t){TK=t;scrollTo({top:0});r()}",
        "function setTK(t){TK=t;r();const k=document.querySelector('.tkc');if(k){const hh=(document.querySelector('.top')||{}).offsetHeight||0;scrollTo({top:k.getBoundingClientRect().top+scrollY-hh-8})}else scrollTo({top:0})}")
    sub("tC.onclick=()=>{showPH(true);rph();scrollTo({top:0})};", "tC.onclick=()=>{PTK='';PMB='';showPH(true);rph();scrollTo({top:0})};")
    sub("D.forEach((m,ix)=>{if(m[5])P.push(ix)})", "D.forEach((m,ix)=>{if(m[5]&&(!PTK||tick(m[3]||'').has(PTK))&&(!PMB||m[2]==PMB))P.push(ix)})")
    sub("sp.textContent=P.length+' level posts'", "sp.textContent=P.length+' level posts'+(PTK?' · $'+PTK:'')+(PMB?' · by '+PMB:'')")
    sub("\nr();</script>", "\n" + JS.replace('__EV__', J(EVENTS)) + "\nwkr();\nr();</script>")
    import theme
    theme.patch_desk(sub, h)
