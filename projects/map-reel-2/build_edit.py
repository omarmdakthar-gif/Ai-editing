"""Build edit.json for map reel 2 (ShowcaseReel), cut from the raw take.

Every time below is in SOURCE seconds (the raw take). T() maps it through work/edl.json onto the reel timeline,
so captions and visuals stay on the words even when the cut changes.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
PUBLIC = ROOT / 'tools' / 'remotion' / 'public'
edl = json.loads((HERE / 'work' / 'edl.json').read_text())
PIECES, TOTAL = edl['pieces'], edl['total']
feat = json.loads((PUBLIC / 'mr1' / 'map.json').read_text())['feat']


def T(src):
    """Reel time for a source time. Inside a piece: exact. In a removed pause: the start of the next kept piece."""
    best = None
    for p in PIECES:
        a, b = p['src']
        if a <= src <= b:
            return round(p['out'][0] + (src - a), 3)
        if a > src and src > a - 2.0 and (best is None or a < best['src'][0]):
            best = p
    if best is not None:
        return best['out'][0]
    # Just after the end of a take: snap to that take's last moment.
    for p in PIECES:
        if p['src'][1] < src <= p['src'][1] + 2.0:
            return p['out'][1]
    raise ValueError(f'source time {src} is not in the cut')


NAK, ALD = '#C77DFF', '#2EE6A8'
PALM, AIR, ZONE, ROAD, WHITE, RED, GOLD = '#45E8EC', '#FF8A3D', '#6C8CFF', '#FF5C70', '#FFFFFF', '#FF5C70', '#FFC940'
ps = feat['palmSprings'][0]
ps_c = [sum(p[0] for p in ps) / len(ps), sum(p[1] for p in ps) / len(ps)]
ALDAR_PIN = [55.401, 25.107]
PJA_C, PJ_C = [54.985, 25.008], [55.132, 25.117]
PORT, JAFZA_C = [55.058, 25.007], [55.086, 24.984]
OTHERS = [[55.21, 25.06], [55.27, 25.05], [55.25, 25.02], [55.30, 25.08], [55.16, 25.04], [55.33, 25.03]]

# ---------- Camera (source time, lon, lat, visible km, tilt, bearing) ----------
cam_src = [
    (120.10, 55.18, 25.12, 70, 30, -25), (124.45, 55.15, 25.08, 52, 38, -10), (112.70, 55.10, 25.05, 40, 42, 8),
    (180.00, 55.06, 25.06, 26, 45, 20), (181.90, 55.04, 24.975, 13, 46, 30), (184.00, 55.02, 24.985, 15, 46, 32), (187.60, 55.015, 24.99, 14, 46, 38),
    (189.30, 55.21, 25.06, 44, 36, 10), (191.20, 55.392, 25.114, 11, 46, -10), (195.40, 55.392, 25.114, 9, 47, -24),
    (196.80, 55.22, 25.04, 52, 40, 0), (209.40, 55.20, 25.04, 46, 42, 14),
    (291.40, 55.20, 25.04, 44, 42, 16), (293.90, ps_c[0], ps_c[1] + 0.004, 9, 46, 30), (295.60, ps_c[0], ps_c[1] + 0.004, 8, 47, 38),
    (297.60, 55.19, 25.05, 38, 40, 20), (300.10, 55.19, 25.05, 34, 42, 28),
    (302.30, 55.085, 24.965, 32, 44, 40), (307.50, 55.095, 24.96, 32, 44, 44), (309.20, 55.10, 24.99, 44, 40, 40), (313.50, 55.08, 24.98, 38, 42, 46),
    (365.90, PJ_C[0], PJ_C[1], 11, 45, 20), (369.60, PJ_C[0] - 0.005, PJ_C[1] - 0.005, 10, 46, 0),
    (370.70, PJA_C[0], PJA_C[1], 13, 45, 10), (373.40, PJA_C[0] + 0.01, PJA_C[1], 16, 45, 20),
    (487.30, 54.80, 24.78, 120, 28, 10), (488.90, 54.61, 24.49, 15, 44, 0), (490.10, 54.44, 24.55, 18, 44, -10),
    (492.40, 54.52, 24.52, 36, 42, -4), (498.50, 54.53, 24.52, 32, 44, 8),
    (523.90, 54.85, 24.78, 120, 28, 10), (525.40, 55.21, 25.04, 48, 42, 10), (532.60, 55.20, 25.04, 40, 44, 22),
    (546.30, 55.20, 25.05, 46, 40, 30), (585.10, 55.21, 25.06, 50, 38, 40),
]
camera = sorted(({'t': T(s), 'lon': lo, 'lat': la, 'km': km, 'tilt': ti, 'bearing': be} for s, lo, la, km, ti, be in cam_src), key=lambda k: k['t'])
camera.insert(0, {**camera[0], 't': 0.0})


def F(start, end=None, label_end=None, **k):
    out = {**k, 'start': T(start)}
    if end is not None:
        out['end'] = T(end)
    if label_end is not None:
        out['labelEnd'] = T(label_end)
    return out


features = [
    F(179.85, 184.0, kind='area', lines=feat['palmJumeirah'], color=PALM, draw=1.0, label='Palm Jumeirah', anchor=PJ_C),
    F(180.20, 188.0, 184.0, kind='line', lines=feat['palmJebelAli'], color=PALM, draw=1.0, label='Palm Jebel Ali', anchor=PJA_C, dim=True),
    F(181.70, 188.0, 184.0, kind='line', lines=feat['szr'], color=ROAD, draw=1.4, label='Sheikh Zayed Road', anchor=[55.058, 24.951], side='down'),
    F(182.40, 188.0, 184.0, kind='area', lines=[ps], color=NAK, draw=0.9, label='Palm Springs', chip='Nakheel · approx. site', anchor=ps_c, dim=True),
    F(184.10, 188.0, kind='line', lines=[[ps_c, PJA_C]], color=WHITE, draw=1.0, label='5 min from Palm Jebel Ali', chip='as stated',
      anchor=[(ps_c[0] + PJA_C[0]) / 2, (ps_c[1] + PJA_C[1]) / 2], pulse=False),
    F(190.90, 196.6, kind='area', lines=feat['dso'], color=WHITE, draw=0.9, label='Dubai Silicon Oasis', anchor=[55.383, 25.123], dim=True),
    F(191.60, 196.6, kind='pin', at=ALDAR_PIN, color=ALD, label='Aldar community', chip='approx. site', side='down'),
    F(196.80, 209.5, kind='pin', at=ps_c, color=NAK),
    F(196.80, 209.5, kind='pin', at=ALDAR_PIN, color=ALD),
    F(293.50, 297.6, kind='area', lines=[ps], color=NAK, draw=0.8, label="Nakheel's project", chip='Palm Springs', anchor=ps_c),
    *[F(297.9 + 0.15 * i, 300.2, kind='pin', at=p, color=RED) for i, p in enumerate(OTHERS)],
    F(298.6, 300.2, kind='pin', at=[55.24, 25.075], color=RED, label='Other private developers', chip='illustrative', pulse=False),
    F(297.6, 300.2, kind='pin', at=ps_c, color=NAK, label='Nakheel', side='down'),
    F(301.10, 309.6, kind='line', lines=feat['szr'], color=GOLD, draw=1.6, dim=True),
    F(301.30, 313.5, kind='area', lines=[ps], color=NAK, draw=0.6, dim=True),
    F(303.84, 313.5, 309.6, kind='line', lines=feat['palmJebelAli'], color=PALM, draw=0.9, label='Palm Jebel Ali', anchor=PJA_C, dim=True),
    F(304.60, 313.5, 309.6, kind='area', lines=feat['airport'], color=AIR, draw=0.9, label='Al Maktoum Airport', anchor=[55.15, 24.915], dim=True),
    F(305.80, 313.5, 309.6, kind='area', lines=feat['jafza'], color=ZONE, draw=0.9, label='Jebel Ali Free Zone', anchor=JAFZA_C, side='down', dim=True),
    F(306.70, 309.6, kind='pin', at=PORT, color=ZONE, label='Jebel Ali Port'),
    F(365.90, 370.6, kind='area', lines=feat['palmJumeirah'], color=PALM, draw=1.2, anchor=PJ_C),
    F(370.20, 373.6, kind='line', lines=feat['palmJebelAli'], color=PALM, draw=1.2, anchor=PJA_C),
    F(488.80, 498.6, kind='area', lines=feat['yas'], color=ALD, draw=1.0, label='Yas Island', anchor=[54.605, 24.49], dim=True, side='down'),
    F(489.70, 498.6, kind='area', lines=feat['saadiyat'], color=ALD, draw=1.0, label='Saadiyat Island', anchor=[54.44, 24.55], dim=True, side='down'),
    F(525.20, 539.9, kind='area', lines=[ps], color=NAK, draw=0.7),
    F(525.40, 539.9, kind='pin', at=ps_c, color=NAK, label='Nakheel', chip='Phase 1 · launching soon'),
    F(525.20, 539.9, kind='area', lines=feat['dso'], color=WHITE, draw=0.7, dim=True),
    F(525.80, 539.9, kind='pin', at=ALDAR_PIN, color=ALD, label='Aldar', chip='Phase 1 · launching soon', side='down'),
    F(575.80, kind='pin', at=ps_c, color=NAK),
    F(576.00, kind='pin', at=ALDAR_PIN, color=ALD),
]

captions_src = [
    (108.55, 110.60, 'Because in Dubai, two *government-backed developers'), (110.60, 112.75, 'are bringing a *major *change!'),
    (179.80, 181.70, '*Nakheel, who built Palm Jumeirah and Palm Jebel Ali,'), (181.70, 184.00, 'is launching on *Sheikh *Zayed *Road,'),
    (184.00, 186.00, 'just *5 *minutes from Palm Jebel Ali,'), (186.00, 188.20, 'a new townhouse and *villa community.'),
    (188.20, 190.90, "And Abu Dhabi's government-backed *Aldar"), (190.90, 192.54, 'is launching next to *Silicon *Oasis'),
    (192.54, 195.70, 'a brand-new *40 *million sq ft community.'), (195.70, 198.08, 'Both have 3 & 4-bedroom *townhouses'),
    (198.08, 200.00, 'and 3, 4 & 5-bedroom *villas.'), (200.00, 203.96, 'Prices are expected to start around *AED *3 *million for a 3-bed townhouse,'),
    (203.96, 209.50, 'with around *10% down payment and flexible payment plans for both projects.'),
    (286.50, 291.48, 'Getting a unit in either of these projects'), (291.48, 293.44, 'will be a very, very *tough task,'),
    (293.44, 295.22, "especially in *Nakheel's project, because the launch"), (295.22, 297.82, 'price per square foot is very, very *attractive'),
    (297.82, 300.14, 'compared to even other private developers in Dubai.'), (300.98, 303.84, "And Nakheel's project is in Dubai's *growth *corridor:"),
    (303.84, 305.80, '*Palm *Jebel *Ali, *Al *Maktoum *Airport,'), (305.80, 307.66, '*Jebel *Ali *Free *Zone, Dubai Port,'),
    (307.66, 309.58, 'all on *this *side of Dubai.'), (309.58, 313.58, "And on this side of Dubai, there's very little townhouse and villa *supply."),
    (364.85, 367.70, 'Okay, so talking about *Nakheel, like I said,'), (367.70, 370.95, "they've built world-famous *Palm *Jumeirah and *Palm *Jebel *Ali"),
    (370.95, 373.45, 'and many more *ultra-luxury projects in Dubai.'),
    (486.25, 488.40, 'And talking about *Aldar,'), (488.40, 490.30, "they're the master developer of Abu Dhabi's *Yas *Island,"),
    (490.30, 492.50, '*Saadiyat *Island and many more islands.'), (492.50, 495.50, "They hold Abu Dhabi's *major *land *banks"),
    (495.50, 498.55, 'and easily execute *multi-billion-dollar projects.'),
    (522.75, 526.60, 'Both projects launch their *first *phase in just a few weeks.'), (526.60, 530.40, 'First-phase investors can see *maximum *returns,'),
    (530.40, 532.62, 'especially in a *government-backed project like this.'),
    (539.95, 543.40, 'To know more, comment *INVEST'), (543.40, 544.80, 'or contact me on this number.'), (544.80, 546.35, "I'll personally get in touch with you."),
    (575.75, 579.40, 'Two government-backed developers, *brand-new communities in Dubai.'), (579.40, 583.40, 'A *first-phase opportunity like this is very important.'),
    (583.40, 585.15, "*Don't *miss it!"),
]
captions = [{'start': T(a), 'end': T(b) if b != 585.15 else TOTAL - 0.1, 'text': t} for a, b, t in captions_src]
# Keep each caption until the next one starts if the gap is short, so the screen never blinks empty mid-sentence.
for c, n in zip(captions, captions[1:]):
    if 0 < n['start'] - c['end'] < 0.5:
        c['end'] = n['start']


def H(a, b, lines, kicker=None, y=250, align='left'):
    return {'start': T(a), 'end': T(b), 'lines': lines, 'kicker': kicker, 'y': y, 'align': align}


headlines = [
    {'start': 0.15, 'end': T(124.40), 'lines': ["DON'T BUY", 'PROPERTY IN', '*DUBAI'], 'kicker': 'WATCH THIS FIRST', 'y': 250, 'align': 'left'},
    H(108.60, 110.55, ['2 DEVELOPERS', '*govt-backed'], 'A MAJOR CHANGE'),
    H(188.20, 190.80, ['ALDAR', '*Abu Dhabi'], 'GOVERNMENT-BACKED'),
    H(295.25, 300.10, ['PRICE PER', 'SQ FT', '*attractive'], 'LAUNCH PRICING'),
    H(300.98, 303.80, ["DUBAI'S", '*growth', 'corridor'], "NAKHEEL'S LOCATION"),
    H(364.85, 367.60, ['NAKHEEL'], 'TRACK RECORD'),
    H(486.25, 488.30, ['ALDAR'], 'MASTER DEVELOPER'),
    H(526.60, 532.60, ['PHASE 1', '*advantage'], 'EARLY INVESTORS'),
    H(575.75, 585.10, ['FIRST PHASE', '*opportunity'], "DON'T MISS IT"),
]

cards = [
    {'type': 'badges', 'start': T(108.70), 'end': T(112.70), 'items': [
        {'name': 'NAKHEEL', 'sub': 'Dubai government-backed', 'color': NAK},
        {'name': 'ALDAR', 'sub': 'Abu Dhabi government-backed', 'color': ALD}]},
    {'type': 'count', 'start': T(192.60), 'end': T(195.60), 'value': 40, 'suffix': 'M', 'unit': 'square feet', 'note': 'AS STATED · NEXT TO DUBAI SILICON OASIS', 'color': ALD, 'y': 370},
    {'type': 'compare', 'start': T(195.70), 'end': T(209.45),
     'columns': [{'name': 'NAKHEEL', 'color': NAK, 'place': 'Palm Springs · Jebel Ali'}, {'name': 'ALDAR', 'color': ALD, 'place': 'Next to Dubai Silicon Oasis'}],
     'rows': [
         {'at': T(195.80), 'label': 'TOWNHOUSES', 'value': '3 & 4 bedrooms'},
         {'at': T(198.10), 'label': 'VILLAS', 'value': '3, 4 & 5 bedrooms'},
         {'at': T(200.10), 'label': 'EXPECTED FROM', 'value': '~ AED 3 million', 'note': '3-bedroom townhouse'},
         {'at': T(204.00), 'label': 'DOWN PAYMENT', 'value': '~ 10%', 'note': 'flexible payment plans'},
     ]},
    {'type': 'stamp', 'start': T(291.40), 'end': T(293.40), 'text': 'HIGH DEMAND', 'sub': 'UNITS WILL BE HARD TO GET', 'color': RED, 'y': 600},
    {'type': 'meter', 'start': T(309.60), 'end': T(313.55), 'label': 'VILLA & TOWNHOUSE SUPPLY', 'level': 0.22, 'color': RED, 'caption': 'on this side of Dubai'},
    {'type': 'list', 'start': T(367.70), 'end': T(373.45), 'title': 'NAKHEEL HAS BUILT', 'color': PALM, 'y': 560, 'items': [
        {'at': T(368.00), 'text': 'Palm Jumeirah'}, {'at': T(370.30), 'text': 'Palm Jebel Ali'}, {'at': T(371.80), 'text': 'Ultra-luxury projects'}]},
    {'type': 'list', 'start': T(492.60), 'end': T(498.55), 'title': 'ALDAR IN ABU DHABI', 'color': ALD, 'y': 560, 'items': [
        {'at': T(493.00), 'text': 'Major land banks'}, {'at': T(495.70), 'text': 'Multi-billion-dollar projects'}]},
    {'type': 'stamp', 'start': T(522.80), 'end': T(526.50), 'text': 'PHASE 1', 'sub': 'LAUNCHING IN WEEKS', 'color': GOLD, 'y': 600},
]

S = lambda f, src, v=0.4: {'file': f'sfx/{f}.wav', 'at': T(src), 'volume': v}
sounds = sorted([
    {'file': 'sfx/impact.wav', 'at': 0.15, 'volume': 0.35}, S('tick', 123.6, 0.4), S('whoosh', 108.4, 0.3), S('impact', 108.7, 0.3), S('pop', 108.85), S('pop', 109.0),
    S('whoosh', 179.7, 0.35), S('shimmer', 180.0, 0.25), S('whoosh_soft', 181.6, 0.25), S('shimmer', 182.5, 0.3), S('tick', 184.1, 0.4),
    S('whoosh', 188.3, 0.35), S('riser', 189.4, 0.2), S('impact', 192.6, 0.3), S('pop', 191.7),
    S('whoosh', 195.6, 0.3), S('tick', 195.8, 0.45), S('tick', 198.1, 0.45), S('pop', 200.1, 0.45), S('pop', 204.0, 0.45),
    S('impact', 291.4, 0.35), S('whoosh', 293.4, 0.3), S('shimmer', 293.6, 0.25), S('whoosh_soft', 295.3, 0.25),
    *[S('tick', 297.9 + 0.15 * i, 0.3) for i in range(6)], S('riser', 298.4, 0.2),
    S('impact', 301.0, 0.3), S('whoosh_soft', 301.2, 0.25), S('pop', 303.9), S('pop', 304.7), S('pop', 305.9), S('pop', 306.8),
    S('whoosh', 307.7, 0.25), S('tick', 309.7, 0.4),
    S('whoosh', 365.0, 0.3), S('shimmer', 366.0, 0.25), S('pop', 369.7), S('pop', 370.5), S('pop', 371.8),
    S('whoosh', 486.4, 0.4), S('riser', 486.6, 0.2), S('impact', 488.9, 0.25), S('shimmer', 489.8, 0.25), S('pop', 493.8), S('pop', 495.7),
    S('whoosh', 522.9, 0.35), S('impact', 523.0, 0.35), S('whoosh_soft', 524.6, 0.25), S('pop', 525.5), S('pop', 525.9), S('shimmer', 526.7, 0.25),
    S('whoosh', 539.9, 0.35), *[S('tick', 541.4 + 0.17 * i, 0.35) for i in range(6)], S('pop', 542.9, 0.45), S('shimmer', 543.2, 0.3),
    S('whoosh', 575.7, 0.3), S('impact', 583.5, 0.3),
], key=lambda s: s['at'])

edit = {
    'durationSeconds': TOTAL,
    'mapFile': 'mr1/map.json',
    'camera': camera,
    'features': features,
    'captions': captions,
    'headlines': headlines,
    'cards': cards,
    'speaker': {'video': 'mr2/speaker.mp4', 'hide': []},
    'voice': 'mr2/voice.wav',
    'music': {'file': 'mr2/music.wav', 'volume': 0.13},
    'sounds': sounds,
    'endCard': {'start': T(539.95), 'keyword': 'INVEST', 'phone': '+971 56 837 6676', 'detail': "and I'll personally get in touch with you"},
    'credit': 'Map data © OpenStreetMap contributors · Outlines and sites approximate',
    'disclaimer': [{'start': T(200.0), 'end': T(209.45), 'text': 'EXPECTED FIGURES · NOT YET OFFICIAL · SUBJECT TO LAUNCH'}],
}
(HERE / 'edit.json').write_text(json.dumps(edit))
# Music lifts: into the corridor reveal and into the launch section.
(HERE / 'work' / 'music_points.json').write_text(json.dumps({'lifts': [T(300.98), T(522.75)], 'total': TOTAL}))
print('edit.json', TOTAL, 's,', len(camera), 'camera keys,', len(features), 'features,', len(captions), 'captions')
print('section starts:', {k: T(v) for k, v in [('projects', 179.8), ('demand', 286.5), ('corridor', 300.98), ('nakheel', 364.85), ('aldar', 486.25), ('phase', 522.75), ('cta', 539.95), ('close', 575.75)]})
