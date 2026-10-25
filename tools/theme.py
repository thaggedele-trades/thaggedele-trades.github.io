"""Visual theme for the desk and the login page.

Paper and ink, with marigold as the one brand color (mark, active tab, primary button).
Green and red are kept for market meaning only. Type is IBM Plex Sans, with Plex Mono for tickers.
"""

FONTS = ''.join(
    f"@font-face{{font-family:'{fam}';src:url(fonts/{file}) format('woff2');font-weight:{w};font-display:swap}}"
    for fam, file, w in [
        ('IBM Plex Sans', 'ibm-plex-sans-latin-400-normal.woff2', 400),
        ('IBM Plex Sans', 'ibm-plex-sans-latin-500-normal.woff2', 500),
        ('IBM Plex Sans', 'ibm-plex-sans-latin-600-normal.woff2', 600),
        ('IBM Plex Mono', 'ibm-plex-mono-latin-500-normal.woff2', 500),
        ('IBM Plex Mono', 'ibm-plex-mono-latin-600-normal.woff2', 600),
    ])

SANS = "'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',sans-serif"
MONO = "'IBM Plex Mono',ui-monospace,Menlo,monospace"

MARK = '<img class=mk src=logo.jpg alt="" width=36 height=36>'

DISCLAIMER = ('For discussion among members only. Nothing here is investment advice; do your own research. '
              'Names are shown as initials and personal details are removed.')

DESK_CSS = FONTS + f"""
:root{{--bg:#0E151D;--pn:#151F2A;--bd:#243242;--tx:#E6EBEF;--mu:#98A6B3;--bu:#1C2836;--g:#3FB37F;--r:#E2645A;--acc:#F2A54A;--acct:#F2A54A;--lnk:#7DB9F0;--ig:linear-gradient(var(--acc),var(--acc))}}
body.lt{{--bg:#F5F6F3;--pn:#FFFFFF;--bd:#E1E5E0;--tx:#172231;--mu:#5D6873;--bu:#EEF1ED;--g:#1E8257;--r:#C0443A;--acc:#D98324;--acct:#9E5810;--lnk:#1D6BB0}}
body{{font-family:{SANS}!important;font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased}}
input,select,button{{font-family:{SANS}}}
:focus-visible{{outline:2px solid var(--acc)!important;outline-offset:2px}}
/* header */
.top{{background:var(--pn)!important;backdrop-filter:none!important}}
.tk{{background:var(--bu)!important;border-bottom:1px solid var(--bd)!important;font:500 12.5px {SANS}!important;color:var(--mu);gap:14px;padding:6px 12px;overflow-x:auto;scrollbar-width:none;white-space:nowrap}}
.tk .tkl{{color:var(--acct);font-weight:600}}.tk .tke{{color:var(--tx)}}.tk .tke small{{color:var(--mu);font-size:12px;margin-left:4px}}
.tb{{position:relative;padding:10px 12px!important;gap:10px!important}}
.tb h1{{font:600 19px/1.2 {SANS}!important;font-style:normal!important;letter-spacing:-.01em!important;align-items:center!important;gap:9px!important}}
.tb h1 .lg,body:not(.lt) .tb h1 .lg,body.lt .tb h1 .lg{{color:var(--tx)!important;-webkit-text-fill-color:var(--tx)!important;background:none!important;padding:0!important}}
.dy{{font:600 10.5px {MONO}!important;color:var(--acct)!important;border:1px solid var(--acc);border-radius:4px;padding:1px 5px;letter-spacing:.04em}}
.mk{{width:44px;height:44px;flex:none;border-radius:11px;object-fit:cover;background:#FEECD6;box-shadow:0 0 0 1px var(--bd)}}
#gear{{width:38px;height:38px;border-radius:50%;border:1px solid var(--bd);background:var(--pn);color:var(--tx);display:flex;align-items:center;justify-content:center;cursor:pointer;flex:none}}
#gear svg{{width:19px;height:19px}}
#menu{{position:absolute;right:12px;top:calc(100% + 4px);z-index:60;background:var(--pn);border:1px solid var(--bd);border-radius:12px;box-shadow:0 12px 32px #0003;padding:6px;min-width:250px}}
#menu[hidden]{{display:none}}
#menu .mi{{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:8px 10px;font-size:14.5px;border-radius:8px}}
#menu .mi+.mi{{border-top:1px solid var(--bd)}}
#menu .mi button{{all:unset;cursor:pointer;min-width:44px;height:34px;padding:0 12px;border-radius:999px;border:1px solid var(--bd);background:var(--bu);color:var(--tx);font:500 13.5px {SANS};display:inline-flex;align-items:center;justify-content:center;gap:6px;white-space:nowrap}}
#menu .mi button{{width:auto!important;height:34px!important;padding:0 12px!important;font-size:13.5px!important;background:var(--bu)!important;box-shadow:none!important;color:var(--tx)!important}}
#menu #lk::after{{content:'Lock';margin-left:6px}}
#menu .mi button:focus-visible{{outline:2px solid var(--acc)}}
.sb{{padding:0 12px 10px!important;gap:8px!important}}
input,select{{border:1px solid var(--bd)!important;border-radius:10px!important;background:var(--bu)!important;font-size:15px!important}}
input:focus,select:focus{{outline:2px solid var(--acc)!important}}
.tabs button{{font:500 14.5px {SANS}!important;letter-spacing:0!important;text-transform:none!important;color:var(--mu)!important;padding:10px 4px!important}}
.tabs button.on{{color:var(--tx)!important;font-weight:600!important}}
.tabs button.on:after{{background:var(--acc)!important;left:30%!important;right:30%!important;height:2px!important;border-radius:2px!important}}
#c{{font-size:13px}}#c a{{color:var(--r)!important}}
/* cards */
.bd,.tkc,.pk{{background:var(--pn)!important;border:1px solid var(--bd)!important;border-radius:14px!important;box-shadow:none!important}}
.bd{{padding:14px!important}}
.bd h3{{background:none!important;-webkit-background-clip:border-box!important;background-clip:border-box!important;color:var(--tx)!important;-webkit-text-fill-color:var(--tx)!important;text-transform:none!important;letter-spacing:-.005em!important;font:600 16px {SANS}!important;margin:0 0 10px!important}}
.ch,.bd .ch,.lnk .ch,#wk .ch,.pt span{{background:var(--bu)!important;border:1px solid var(--bd)!important;color:var(--tx)!important;font:500 12.5px {MONO}!important;padding:4px 9px!important;border-radius:999px!important}}
.ch b,.bd .ch b,.lnk .ch b{{color:var(--acct)!important;font-weight:600}}
.ch.sel,.bd .ch.sel,.lnk .ch.sel{{background:var(--tx)!important;color:var(--pn)!important;border-color:var(--tx)!important}}
.ch.sel b,.bd .ch.sel b,.lnk .ch.sel b{{color:var(--acc)!important}}
.rg button,.lns button,.pv button,.tkb button{{font:500 13px {SANS}!important;background:var(--bu)!important;border:1px solid var(--bd)!important;color:var(--tx)!important}}
.rg button.on,.lns button.on,.pv button.on{{background:var(--tx)!important;color:var(--pn)!important;border-color:var(--tx)!important}}
#wk .row>b:first-child{{text-transform:none!important;letter-spacing:0!important;font:600 13px {SANS}!important;color:var(--mu)!important}}
#wk a,#wk .lv{{color:var(--lnk)!important}}#wk .lv.mb{{text-decoration:none!important;font-weight:600}}
.ih{{background:var(--bu)!important;border:1px solid var(--bd)}}.ih .go{{background:var(--acc)!important;color:#1B1206!important}}
.tkc h2{{font:600 24px {MONO}!important;letter-spacing:-.01em}}
.tkc .pf{{font-size:inherit!important;opacity:1!important;padding:0!important}}
.pft span{{font:500 12.5px {SANS}!important;background:var(--bu)!important}}
.pfl b{{font-weight:600!important}}
/* chat */
.mo{{color:var(--mu)!important;text-transform:none!important;letter-spacing:0!important;font:600 13.5px {SANS}!important}}
.mo:before,.mo:after{{background:var(--bd)!important;height:1px!important;opacity:1!important}}
h2 span{{font:500 12.5px {SANS}!important;color:var(--mu)!important;background:var(--pn)!important;border:1px solid var(--bd)!important}}
.md{{background:var(--bu)!important;border-left:3px solid var(--r)!important;font:600 13.5px {SANS}!important;border-radius:8px!important}}
.md.fo{{border-left-color:var(--acc)!important}}
.m{{background:var(--pn)!important;border:1px solid var(--bd)!important;box-shadow:none!important;border-radius:16px 16px 16px 4px!important;padding:9px 13px!important}}
.m b{{filter:none!important;font-weight:600!important;font-size:13.5px!important}}
.m a,.pcap a,.bb a{{color:var(--lnk)!important}}
.t{{color:var(--acct)!important;font:600 .95em {MONO}!important}}
.av{{background:var(--c)!important;border:0!important;box-shadow:none!important;flex:0 0 32px!important;height:32px!important;font:600 11px {SANS}!important}}
.m i .sv.on{{color:var(--acc)!important}}
figcaption{{background:var(--tx)!important;color:var(--pn)!important;font:500 12.5px {SANS}!important}}
.sic{{color:var(--lnk)!important;font-weight:600!important}}
details.cx summary{{color:var(--acct)!important}}
#jb button{{background:var(--pn)!important;color:var(--tx)!important;border:1px solid var(--bd)!important;box-shadow:0 4px 14px #0000002e!important;font:600 13px {SANS}!important}}
#jb button.on{{border-color:var(--acc)!important;outline:0!important}}
.bk{{background:var(--tx)!important;color:var(--pn)!important;font:600 14px {SANS}!important;box-shadow:0 6px 18px #0004!important}}
footer.disc{{max-width:680px;margin:0 auto;font-size:12.5px;line-height:1.5;color:var(--mu);padding:18px 16px 90px;opacity:1!important}}
/* wide screens: chat in the middle, weekly card and tickers alongside */
@media(min-width:1060px){{
 .tb,.sb,.tabs,#c,#ph,#ln,#svp,main,footer.disc{{max-width:680px!important;margin-left:calc(50% - 510px)!important;margin-right:0!important}}
 #side{{position:fixed;top:var(--toph,150px);left:calc(50% + 190px);width:320px;max-height:calc(100vh - var(--toph,150px) - 12px);overflow:auto;scrollbar-width:thin}}
 #side .wr{{padding:0!important;max-width:none!important}}#side .bd{{margin:0 0 12px!important}}
 body.phon #side{{display:none}}
 #jb{{right:auto!important;left:calc(50% + 40px)}}
 .bk{{left:calc(50% - 510px)!important}}
}}
"""

GEAR = ('<svg viewBox="0 0 24 24" fill=none stroke=currentColor stroke-width=1.8 stroke-linecap=round stroke-linejoin=round aria-hidden=true>'
        '<circle cx=12 cy=12 r=3.2 /><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/></svg>')

DESK_JS = r"""
(()=>{const tb=document.querySelector('.tb'),h1=tb.querySelector('h1');h1.insertAdjacentHTML('afterbegin',__MARK__);
const ban=document.querySelector('.ban');if(ban)ban.closest('.wr').remove();
const g=el('button');g.id='gear';g.type='button';g.setAttribute('aria-label','Settings');g.setAttribute('aria-expanded','false');g.setAttribute('aria-controls','menu');g.innerHTML=__GEAR__;
const mn=el('div');mn.id='menu';mn.hidden=true;mn.setAttribute('role','menu');
const row=(label,btn)=>{if(!btn)return;const r=el('div','mi');r.append(el('span','',label),btn);mn.append(r)};
row('Theme',$('dm'));row('Background music',$('mu'));row('Lock this device',$('lk'));
tb.append(g,mn);g.onclick=e=>{e.stopPropagation();mn.hidden=!mn.hidden;g.setAttribute('aria-expanded',String(!mn.hidden))};
document.addEventListener('click',e=>{if(!mn.hidden&&!e.target.closest('#menu')){mn.hidden=true;g.setAttribute('aria-expanded','false')}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!mn.hidden){mn.hidden=true;g.focus()}});
$('tC').textContent='Levels';$('tL').textContent='Links';$('tS').textContent='Saved';
const bh=[...document.querySelectorAll('.bd h3')].find(x=>/talked/i.test(x.textContent));if(bh)bh.textContent='Most-discussed tickers';
const strip=$('tk');if(strip){strip.textContent='';const now=new Date();now.setHours(0,0,0,0);const up=EV.filter(e=>dd(e[0])>=now).slice(0,3);
if(up.length){strip.append(el('span','tkl','Next up'));up.forEach(([d,l,t])=>{const s=el('span','tke',dd(d).toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric'})+': '+l);s.append(el('small','',t+' ET'));strip.append(s)});strip.title='Upcoming market events (US Eastern time)'}else strip.remove()}
const wkw=$('wk')&&$('wk').parentElement,bdw=$('bo')&&$('bo').closest('.wr');if(wkw&&bdw){const sd=el('aside');sd.id='side';wkw.before(sd);sd.append(wkw,bdw)}
const cnt=$('c');const setH=()=>{if(cnt)document.documentElement.style.setProperty('--toph',(cnt.offsetTop+cnt.offsetHeight+22)+'px')};setH();addEventListener('resize',setH);
const ft=document.querySelector('footer');if(ft){ft.className='disc';ft.textContent=__DISC__}
const sp=showPH;showPH=on=>{sp(on);document.body.classList.toggle('phon',!!on)};
document.querySelectorAll('meta[name=theme-color]').forEach(m=>m.content=document.body.classList.contains('lt')?'#F5F6F3':'#0E151D');})();
"""

GATE_CSS = FONTS + f"""
body{{font-family:{SANS}!important;background:#F5F6F3!important;background-image:none!important;color:#172231!important;flex-direction:column;gap:14px;padding:16px}}
.bx{{border:1px solid #E1E5E0!important;border-radius:16px!important;box-shadow:none!important;padding:32px 26px 22px!important}}
.rg{{background:none!important;width:auto!important;height:auto!important;padding:0!important;margin:0 auto 14px!important;display:flex;justify-content:center}}
.mk{{width:84px;height:84px;border-radius:22px;object-fit:cover;background:#FEECD6;box-shadow:0 0 0 1px #E1E5E0}}
h1{{font:600 25px/1.2 {SANS}!important;font-style:normal!important;letter-spacing:-.015em;margin:0 0 6px!important}}
h1 .lg{{color:#172231!important;-webkit-text-fill-color:#172231!important;background:none!important}}
.dy{{font:600 11px {MONO}!important;color:#9E5810!important;border:1px solid #D98324;border-radius:4px;padding:1px 5px;vertical-align:middle}}
p{{text-transform:none!important;letter-spacing:0!important;font-size:14.5px!important;color:#5D6873!important}}
.c{{font:500 12.5px {MONO}!important}}.c b{{color:#1E8257!important}}.c i{{color:#C0443A!important}}
input[type=password]{{border:1px solid #E1E5E0!important;border-radius:10px!important;background:#fff!important;font-size:16px!important}}
input[type=password]:focus{{outline:2px solid #D98324;outline-offset:1px}}
button{{background:#D98324!important;color:#1B1206!important;font:600 15px {SANS}!important;border-radius:10px!important}}
button:focus-visible{{outline:2px solid #172231;outline-offset:2px}}
label{{color:#5D6873!important;font-size:14px!important}}
.disc{{max-width:360px;text-align:center;font-size:12.5px;line-height:1.5;color:#5D6873;margin:0}}
.sk{{display:block;height:10px;border-radius:5px;margin:8px auto 0;width:80%;background:linear-gradient(90deg,#E9ECE7,#F6F7F4,#E9ECE7);background-size:200% 100%;animation:sk 1.1s linear infinite}}.sk.short{{width:50%}}
@keyframes sk{{to{{background-position:-200% 0}}}}
@media (prefers-reduced-motion:reduce){{.sk{{animation:none}}}}
@media (prefers-color-scheme:dark){{
 body{{background:#0E151D!important;color:#E6EBEF!important}}.bx{{background:#151F2A!important;border-color:#243242!important}}
 h1 .lg{{color:#E6EBEF!important;-webkit-text-fill-color:#E6EBEF!important}}p,label,.disc{{color:#98A6B3!important}}.dy{{color:#F2A54A!important}}
 input[type=password]{{background:#1C2836!important;border-color:#243242!important;color:#E6EBEF!important}}
 .sk{{background:linear-gradient(90deg,#1C2836,#243242,#1C2836);background-size:200% 100%}}
}}
"""


def patch_desk(sub, h):
    import json
    sub('</head>', '<style>' + DESK_CSS + '</style></head>')
    sub("(md.startsWith('FOMC')?'🏛 ':'📉 ')+md", "md")
    sub("a.textContent='↪ Show in chat'", "a.textContent='Show in chat'")
    js = DESK_JS.replace('__MARK__', json.dumps(MARK)).replace('__GEAR__', json.dumps(GEAR)).replace('__DISC__', json.dumps(DISCLAIMER))
    sub("\nwkr();\nr();</script>", "\n" + js + "\nwkr();\nr();</script>")


def patch_gate(gsub):
    gsub('</style>', GATE_CSS + '</style>')
    gsub('<div class=rg><div>📈</div></div>', '<div class=rg>' + MARK + '</div>')
    gsub('</form>', '</form><p class=disc>' + DISCLAIMER + '</p>')
    gsub("e.textContent='Loading desk…';", "e.innerHTML='<span class=sk></span><span class=sk></span><span class=\"sk short\"></span>';")
