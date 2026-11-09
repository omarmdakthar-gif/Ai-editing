"""Re-time edit.json to the forced-aligned voice (work/aligned.json).

The first cut's times came from windowed Whisper timestamps, which ran up to 1.3 s early. This maps every time in
edit.json through a piecewise-linear warp (old caption start -> aligned line start), pins the key moments to the
exact aligned word, and rebuilds the captions from the aligned lines.
Run after build_edit.py:  python retime.py
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
edit = json.loads((HERE / 'edit.json').read_text())
lines = json.loads((HERE / 'work' / 'aligned.json').read_text())
caps = edit['captions']
assert len(caps) == len(lines), (len(caps), len(lines))
TOTAL = edit['durationSeconds']

old = [0.0] + [c['start'] for c in caps] + [TOTAL]
new = [0.0] + [l['start'] for l in lines] + [TOTAL]
# Keep the warp monotonic: if an old anchor is not after the previous one, drop it.
pairs = []
for o, n in zip(old, new):
    if not pairs or (o > pairs[-1][0] and n > pairs[-1][1]):
        pairs.append((o, n))
xo, xn = np.array([p[0] for p in pairs]), np.array([p[1] for p in pairs])
warp = lambda t: round(float(np.interp(t, xo, xn)), 3)


def word(line, w, nth=0):
    hits = [x for x in lines[line]['words'] if x['w'] == w]
    return hits[nth]['s']


TIME_KEYS = {'start', 'end', 'at', 'revealAt', 't'}


def walk(node):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in TIME_KEYS and isinstance(v, (int, float)):
                node[k] = warp(v)
            elif k in ('steps', 'fees', 'busy') and isinstance(v, list):
                node[k] = [warp(x) for x in v]
            elif k == 'hide' and isinstance(v, list):
                node[k] = [[warp(a), warp(b)] for a, b in v]
            else:
                walk(v)
    elif isinstance(node, list):
        for v in node:
            walk(v)


for key in ('scenes', 'headlines', 'cards', 'sounds', 'credits', 'hookLogos', 'endCard'):
    walk(edit[key])
# World-map camera keys are times too ('t'), handled by walk via scenes.

# ---- Pin the key moments to the exact word. ----
apple, nvidia, oil = word(1, 'apple'), word(1, 'nvidia'), word(2, 'oil')
for item, t in zip(edit['hookLogos']['items'], (apple, nvidia, oil)):
    item['at'] = round(t, 3)
hook_end = lines[2]['end']                       # the face stays big until "...kidaiyadhu" ends
edit['speakerIntro']['end'] = round(hook_end + 0.05, 3)
edit['speaker']['hide'] = [[0, round(hook_end + 0.5, 3)]]
visa = word(5, 'visa')
scene = {s['kind'] + str(i): s for i, s in enumerate(edit['scenes'])}
for s in edit['scenes']:
    if s['kind'] == 'world' and s['start'] == 0:
        s['end'] = round(hook_end + 0.15, 3)
    if s['kind'] == 'wallet':
        s['start'], s['revealAt'], s['end'] = round(hook_end + 0.15, 3), round(visa, 3), round(lines[6]['start'] - 0.1, 3)
    if s['kind'] == 'profit':
        s['start'] = round(lines[6]['start'] - 0.1, 3)
    if s['kind'] == 'bank':
        s['steps'] = [round(word(8, 'debit'), 3), round(word(9, 'loan'), 3), round(word(10, 'risk'), 3)]
    if s['kind'] == 'world' and s['start'] > 10:
        s['fees'] = [round(word(13, 'fee') - 0.4 + 0.84 * i, 3) for i in range(14)]
    if s['kind'] == 'image' and s.get('title'):
        s['start'] = round(word(18, 'christian') - 0.05, 3)
for c in edit['cards']:
    if c.get('title') == 'THE TOWER':
        c['items'][0]['at'] = round(word(19, 'eighty'), 3)
        c['items'][1]['at'] = round(word(19, 'sheikh'), 3)
    if c.get('title') == 'PAYMENT PLAN':
        c['start'] = round(lines[22]['start'], 3)
        c['items'][0]['at'] = round(word(22, 'fifty'), 3)
        c['items'][1]['at'] = round(word(22, 'fifty', 1), 3)
    if c.get('type') == 'count':
        c['start'] = round(word(21, 'sixth') - 0.1, 3)
edit['endCard']['start'] = round(word(26, 'rockefeller') - 1.45, 3)   # "ROCKEFELLER" types in as it is said
for snd in edit['sounds']:
    if snd['file'].endswith('impact.wav') and abs(snd['at'] - visa) < 1.0:
        snd['at'] = round(visa, 3)
    if snd['file'].endswith('pop.wav') and snd['at'] > 60:
        snd['at'] = round(word(27, 'number'), 3)
    if snd['file'].endswith('whoosh.wav') and abs(snd['at'] - hook_end) < 1.0:
        snd['at'] = round(hook_end + 0.05, 3)

# ---- Captions straight from the aligned lines: on screen from the first word until the next line starts. ----
for i, (c, l) in enumerate(zip(caps, lines)):
    c['start'] = round(l['start'], 3)
    nxt = lines[i + 1]['start'] if i + 1 < len(lines) else TOTAL
    c['end'] = round(max(l['end'] + 0.15, min(nxt, l['end'] + 0.6)) if nxt - l['end'] > 0.6 else nxt, 3)
    c['speech'] = round(l['end'], 3)

(HERE / 'edit.json').write_text(json.dumps(edit))
(HERE / 'work' / 'music_points.json').write_text(json.dumps({'lifts': [warp(22.0), warp(40.1)], 'total': TOTAL}))
print('retimed. hook ends', hook_end, '| apple', apple, 'nvidia', nvidia, 'oil', oil, '| visa', visa)
