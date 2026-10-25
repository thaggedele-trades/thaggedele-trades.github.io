"""Shared helpers for the Thaggedele Traders desk.

Nothing private lives in this file. Real names, the chat and the page source are kept
encrypted in m/src.bin and m/chat.bin, and only the desk password opens them.
"""
import base64, datetime, gzip, json, os, re
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

b64d = base64.b64decode
b64e = lambda b: base64.b64encode(b).decode()
J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))


# ---------- crypto ----------
def gate_params(repo):
    g = open(os.path.join(repo, 'index.html'), encoding='utf-8').read()
    return g, json.loads(re.search(r'const C=(\{.*?\});', g, re.S).group(1))


def key_for(repo, password):
    _, C = gate_params(repo)
    key = PBKDF2HMAC(hashes.SHA256(), 32, b64d(C['s']), C['i']).derive(password.encode())
    AESGCM(key).decrypt(b64d(C['v']), b64d(C['c']), None)  # raises if the password is wrong
    return key


def enc(key, data):
    iv = os.urandom(12)
    return iv + AESGCM(key).encrypt(iv, data, None)


def dec(key, blob):
    return AESGCM(key).decrypt(blob[:12], blob[12:], None)


def save_json(key, path, obj):
    open(path, 'wb').write(enc(key, gzip.compress(J(obj).encode(), 9, mtime=0)))


def load_json(key, path):
    return json.loads(gzip.decompress(dec(key, open(path, 'rb').read())))


# ---------- WhatsApp export ----------
LINE = re.compile(r'^‎?\[(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{2}:\d{2}[\s ][AP]M)\] (.*?): (.*)$')


def parse_export(text):
    out = []
    for raw in text.splitlines():
        m = LINE.match(raw)
        if m:
            d, t, who, txt = m.groups()
            out.append([d, t.replace(' ', ' '), who, txt])
        elif out:
            out[-1][3] += '\n' + raw
    return out


def ts(d, t):
    return datetime.datetime.strptime(d + ' ' + t.replace(' ', ' '), '%m/%d/%y %I:%M:%S %p')


def day(d):
    p = d.split('/')
    return datetime.date(2000 + int(p[2]), int(p[0]), int(p[1]))


# ---------- message cleanup (matches the existing desk) ----------
URL = re.compile(r'(https?://[^\s<>]+|www\.[^\s<>]+)')
MENTION = re.compile(r'@⁨[^⁩]*⁩|@\+?\d[\d\s]{6,}\d')
MEDIA = re.compile(r'\s*‎?(?:[^\n]*• [^\n]*)?‎?(?:image|video|GIF|sticker|audio|document|Contact card) omitted\s*$')
EDITED = re.compile(r'\s*‎?<This message was edited>\s*$')
# Links that can reveal private documents, meetings or invites stay hidden.
PRIVATE = re.compile(r'milaap\.org|gofundme\.com|ketto\.org|(docs|drive|meet|maps)\.google\.|chat\.whatsapp\.com|wa\.me/|zoom\.us|forms\.gle|maps\.app\.goo\.gl|goo\.gl/maps|calendly\.com|icloud\.com|dropbox\.com', re.I)
host = lambda u: re.sub(r'^(https?://)?(www\.)?', '', u).split('/')[0]
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
SOCIAL = re.compile(r'(^|\.)(instagram\.com|facebook\.com|fb\.watch|x\.com|twitter\.com|tiktok\.com|threads\.net|linkedin\.com|reddit\.com|newsbreakapp\.com|newsbreak\.com|search\.app|youtube\.com|youtu\.be)$', re.I)
TRACK = re.compile(r'^(utm_.*|fbclid|gclid|igshid|igsh|si|mibextid|share.*|ref|ref_src|ref_url|s|fs|t|pd|send_user_id|lang|sender.*|smid|sh)$', re.I)


def scrub_url(u):
    """Drop share/tracking parameters that can identify who shared a link."""
    try:
        p = urlsplit(u if '://' in u else 'https://' + u)
    except ValueError:
        return u
    host = p.netloc.lower()
    keep = []
    for k, v in parse_qsl(p.query, keep_blank_values=True):
        if 'youtu' in host and k in ('v', 't', 'list'):
            keep.append((k, v))
        elif SOCIAL.search(host) or TRACK.match(k):
            continue
        else:
            keep.append((k, v))
    out = urlunsplit((p.scheme, p.netloc, p.path, urlencode(keep), ''))
    return out if '://' in u else out.split('://', 1)[1]


FLAG = re.compile(r'\b(wife|husband|son|daughter|kids?|children|mom|mother|dad|father|family|parents?|hospital|patient|surgery|sick|password|passcode|address|ssn)\b'
                  r'|\+?\d[\d\-\s().]{9,}\d|[\w.+-]+@[\w-]+\.[\w.]+', re.I)


def clean(txt):
    """Return cleaned text, or None when the line is a system notice or media-only."""
    if txt.startswith('‎'):
        return None  # media, deleted, joined/left, disappearing-message notices
    txt = EDITED.sub('', txt)
    txt = MEDIA.sub('', txt)
    txt = MENTION.sub('[mention]', txt)
    txt = URL.sub(lambda m: scrub_url(m.group(0)) if not PRIVATE.search(m.group(0)) else '[link: ' + host(m.group(0)) + ']', txt)
    txt = txt.strip()
    if not txt or re.fullmatch(r'(\[mention\]\s*)+', txt) or txt in ('This message was deleted', 'You deleted this message'):
        return None
    return txt


def initials(name, taken):
    words = [w for w in re.findall(r"[A-Za-z]+", name.replace('~', ''))]
    base = ''.join(w[0].upper() + '.' for w in words) or 'X.'
    if base not in taken:
        return base
    n = 2
    while base[:-1] + f'{n}.' in taken:
        n += 1
    return base[:-1] + f'{n}.'


def name_aliases(names):
    """Member first/last names (4+ letters) -> initials, for names typed inside messages."""
    al = {}
    for full, ini in names.items():
        for w in re.findall(r"[A-Za-z]{4,}", full):
            al.setdefault(w.lower(), set()).add(ini)
    return {w: s.pop() for w, s in al.items() if len(s) == 1}


# Real names are never stored: the bundle keeps only salted hashes of them.
import hashlib
norm = lambda s: re.sub(r'[~\s\u202f\u00a0]+', ' ', s).strip().lower()


def nh(salt, s):
    return hashlib.sha256((salt + norm(s)).encode()).hexdigest()[:20]


def hashed_aliases(salt, names, stop):
    """Hashes of member first/last names (4+ letters) -> initials, skipping ordinary words."""
    al = {}
    for full, ini in names.items():
        for w in re.findall(r"[A-Za-z]{4,}", full):
            if w.lower() not in stop:
                al.setdefault(nh(salt, w), set()).add(ini)
    return {h: s.pop() for h, s in al.items() if len(s) == 1}


def redact_names_h(txt, salt, aliases):
    return re.sub(r"\b[A-Za-z]{4,}\b", lambda m: aliases.get(nh(salt, m.group(0)), m.group(0)), txt)


def redact_names(txt, aliases):
    if not aliases:
        return txt
    rx = re.compile(r'\b(' + '|'.join(sorted(map(re.escape, aliases), key=len, reverse=True)) + r')\b', re.I)
    return rx.sub(lambda m: aliases[m.group(1).lower()], txt)


# ---------- ticker board ----------
def make_board(D, WL):
    WS = set(WL)
    TR = re.compile(r'\$([A-Za-z]{1,5})\b|\b(' + '|'.join(x for x in WL if x != 'MU') + r')\b')
    tick = lambda x: {(m.group(1) or m.group(2)).upper() for m in TR.finditer(x)} & WS
    nd = day(D[-1][0])
    out = {'new': D[-1][0]}
    for k, days in (('w', 7), ('m', 30), ('a', None)):
        c, ld = {}, {}
        for m in D:
            if days is not None and (nd - day(m[0])).days > days:
                continue
            for t in tick(m[3]):
                c[t] = c.get(t, 0) + 1
                ld[t] = m[0]
        out[k] = sorted(([t, n, ld[t]] for t, n in c.items()), key=lambda x: -x[1])[:30]
    return out


# ---------- the desk page (original unpatched form, kept inside m/src.bin) ----------
def _span(html, name):
    i = html.index('const ' + name + '=') + len('const ' + name + '=')
    obj, end = json.JSONDecoder().raw_decode(html, i)
    return obj, i, end


def desk_parts(html):
    return _span(html, 'D')[0], _span(html, 'WL')[0], _span(html, 'MD')[0]


def desk_with(html, D, MD):
    WL = _span(html, 'WL')[0]
    for name, val in (('BOARD', make_board(D, WL)), ('MD', MD), ('D', D)):
        _, i, end = _span(html, name)
        html = html[:i] + J(val) + html[end:]
    return html
