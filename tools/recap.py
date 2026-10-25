"""Weekly WhatsApp recap of the desk, ready to paste into the group.

  DESK_PASSWORD=... python3 tools/recap.py

Covers the 7 days up to the newest message on the desk. Uses initials only and never
includes the password. WhatsApp formatting: *bold*, _italic_.
"""
import datetime, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from desk import key_for, load_json, desk_parts, make_board, day, URL
from features import EVENTS

SITE = 'https://thaggedele-trades.github.io'


def fmt_day(d):
    return day(d).strftime('%a %b %-d')


def recap(src, today=None):
    D, WL, _ = desk_parts(src['desk'])
    end = day(D[-1][0])
    start = end - datetime.timedelta(days=6)
    wk = [m for m in D if day(m[0]) >= start]
    board = make_board(D, WL)
    who = {}
    for m in wk:
        who[m[2]] = who.get(m[2], 0) + 1
    charts = sum(1 for m in wk if len(m) > 5 and m[5])
    links, seen = [], set()
    for m in reversed(wk):
        for u in URL.findall(m[3]):
            h = re.sub(r'^(https?://)?(www\.)?', '', u).split('/')[0].lower()
            if 'thaggedele' in h or h in seen:
                continue
            seen.add(h)
            txt = URL.sub('', m[3]).strip().replace('\n', ' ')
            txt = re.sub(r'\s+', ' ', re.sub(r'[*_~`#]', '', txt)).strip(' -–:')
            if len(txt) < 25:  # use the article's own title from its address
                slug = [p for p in u.split('?')[0].rstrip('/').split('/')[3:] if re.search('[a-z]{3,}-[a-z]', p)]
                if slug:
                    t2 = re.sub(r'(-\d+)+$', '', re.sub(r'\.\w+$', '', slug[-1])).replace('-', ' ').strip()
                    t2 = t2[:1].upper() + t2[1:]
                    txt = f'{txt}: {t2}' if txt else t2
            txt = txt or h
            links.append(txt[:90] + ('…' if len(txt) > 90 else ''))
            links[-1] = (links[-1], u if u.startswith('http') else 'https://' + u)
            break
        if len(links) == 3:
            break
    today = today or datetime.date.today()
    up = [e for e in EVENTS if day(e[0]) >= today and (day(e[0]) - today).days <= 14][:4]

    span = f"{start.strftime('%b %-d')}–{end.day}" if start.month == end.month else \
        f"{start.strftime('%b %-d')} – {end.strftime('%b %-d')}"
    out = [f'📈 *Thaggedele Traders: week of {span}*', '']
    out.append(f'💬 {len(wk):,} messages from {len(who)} traders' +
               (f" · most active: {', '.join(w for w, _ in sorted(who.items(), key=lambda x: -x[1])[:3])}" if who else ''))
    if board['w']:
        out.append('🔥 *Hot tickers:* ' + ' · '.join(f'${t} ({n})' for t, n, _ in board['w'][:5]))
    if charts:
        out.append(f"📊 {charts} new chart{'s' if charts > 1 else ''} on the Levels tab")
    if links:
        out += ['', '🔗 *Worth a look:*'] + [f'• {t}\n  {u}' for t, u in links]
    if up:
        out += ['', '📅 *Coming up (ET):*'] + [f'• {fmt_day(d)}, {t}: {l}' for d, l, t in up]
    out += ['', f'🖥 Full desk, ticker pages and all links: {SITE}', '_DYOR_']
    return '\n'.join(out)


if __name__ == '__main__':
    pw = os.environ.get('DESK_PASSWORD') or sys.exit('Set DESK_PASSWORD first.')
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(recap(load_json(key_for(repo, pw), os.path.join(repo, 'm', 'src.bin'))))
