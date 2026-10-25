"""Add new WhatsApp messages to the Thaggedele Traders desk.

  python3 tools/update.py preview <export .zip or .txt> <pending.json>   # new messages, cleaned, for review
  python3 tools/update.py apply <pending.json>                           # add them and rebuild the site
  python3 tools/update.py rebuild                                        # rebuild only (e.g. after a code change)
  python3 tools/recap.py                                                 # weekly WhatsApp recap (also printed by apply)

The password comes from the DESK_PASSWORD environment variable. Keep pending.json OUTSIDE
the repo: it holds chat text. In pending.json, set "drop": true on a message to leave it out,
or edit its "txt". New senders get initials automatically; edit "new_names" to change them.
"""
import json, os, re, sys, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from desk import (key_for, load_json, parse_export, clean, initials, nh, hashed_aliases, redact_names_h,
                  ts, desk_parts, desk_with, FLAG)
from build import build
from recap import recap

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, 'm', 'src.bin')
# First names that are also ordinary words: never auto-replaced inside messages.
STOP = {'fitness', 'matters', 'sunny', 'concord', 'chris', 'tharun', 'deep', 'dallas'}


def read_export(path):
    if path.endswith('.zip'):
        with zipfile.ZipFile(path) as z:
            name = next(n for n in z.namelist() if n.endswith('.txt'))
            return z.read(name).decode('utf-8')
    return open(path, encoding='utf-8').read()


def preview(key, src, export, out):
    D, _, _ = desk_parts(src['desk'])
    salt, names = src['salt'], src['names']
    ini = lambda who: names.get(nh(salt, who))
    E = parse_export(read_export(export))
    last = D[-1]
    lt = ts(last[0], last[1])
    start = None
    for i in range(len(E) - 1, -1, -1):
        e = E[i]
        if abs((ts(e[0], e[1]) - lt).total_seconds()) <= 3 and ini(e[2]) == last[2]:
            c = clean(e[3])
            if c is not None and (c == last[3] or c[:40] == last[3][:40]):
                start = i + 1
                break
        if ts(e[0], e[1]) < lt.replace(hour=0, minute=0, second=0):
            break
    if start is None:  # fall back to time order
        start = next((i for i, e in enumerate(E) if ts(e[0], e[1]) > lt), len(E))
    taken = set(names.values())
    new_names = {}
    al = src['aliases']
    msgs = []
    for e in E[start:]:
        c = clean(e[3])
        if c is None:
            continue
        who = e[2]
        if ini(who) is None and who not in new_names:
            new_names[who] = initials(who, taken)
            taken.add(new_names[who])
        txt = redact_names_h(c, salt, dict(al, **hashed_aliases(salt, new_names, STOP)))
        txt = re.sub(re.escape(os.environ['DESK_PASSWORD']), '[password]', txt, flags=re.I)
        f = sorted({m.group(0).lower() for m in FLAG.finditer(txt)})
        msgs.append({'d': e[0], 't': e[1], 'who': who, 'txt': txt, 'flags': f, 'drop': False})
    json.dump({'after': last[:2], 'new_names': new_names, 'messages': msgs}, open(out, 'w'), ensure_ascii=False, indent=1)
    print(f'{len(msgs)} new messages after {last[0]} {last[1]}; '
          f'{sum(1 for m in msgs if m["flags"])} flagged; new senders: {new_names or "none"}')


def apply(key, src, pending):
    P = json.load(open(pending, encoding='utf-8'))
    D, _, MD = desk_parts(src['desk'])
    salt = src['salt']
    for who, i in P['new_names'].items():
        src['names'][nh(salt, who)] = i
    src['aliases'].update(hashed_aliases(salt, P['new_names'], STOP))
    added = 0
    for m in P['messages']:
        if m.get('drop'):
            continue
        D.append([m['d'], m['t'], src['names'][nh(salt, m['who'])], m['txt']])
        added += 1
    src['desk'] = desk_with(src['desk'], D, MD)
    total, cut = build(REPO, key, src)
    print(f'added {added}; desk now has {total} messages ({total - cut} in the fast first load)')
    print('\n--- WhatsApp recap ---\n' + recap(src))


if __name__ == '__main__':
    pw = os.environ.get('DESK_PASSWORD')
    if not pw:
        sys.exit('Set DESK_PASSWORD first.')
    key = key_for(REPO, pw)
    src = load_json(key, SRC)
    cmd = sys.argv[1]
    if cmd == 'preview':
        preview(key, src, sys.argv[2], sys.argv[3])
    elif cmd == 'apply':
        apply(key, src, sys.argv[2])
    elif cmd == 'rebuild':
        print(build(REPO, key, src))
    else:
        sys.exit(__doc__)
