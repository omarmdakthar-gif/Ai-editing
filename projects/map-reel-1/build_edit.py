"""Build edit.json for map reel 1 (ShowcaseReel): Nakheel's Palm Springs and Aldar's Silicon Oasis community.

Times are seconds on the reel's timeline, which is the editor's cut (the voice and speaker clip keep its timing).
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
PUBLIC = HERE.parent.parent / 'tools' / 'remotion' / 'public'
feat = json.loads((PUBLIC / 'mr1' / 'map.json').read_text())['feat']

NAK, ALD = '#C77DFF', '#2EE6A8'          # Nakheel purple, Aldar emerald
PALM, AIR, ZONE, ROAD, WHITE, RED = '#45E8EC', '#FF8A3D', '#6C8CFF', '#FF5C70', '#FFFFFF', '#FF5C70'

ps = feat['palmSprings'][0]
ps_c = [sum(p[0] for p in ps) / len(ps), sum(p[1] for p in ps) / len(ps)]
ALDAR_PIN = [55.401, 25.107]               # approximate: "near Silicon Oasis", no published boundary
PJA_C, PJ_C = [54.985, 25.008], [55.132, 25.117]
PORT, JAFZA_C = [55.058, 25.007], [55.086, 24.984]
OTHERS = [[55.21, 25.06], [55.27, 25.05], [55.25, 25.02], [55.30, 25.08], [55.16, 25.04], [55.33, 25.03]]

cam = lambda t, lon, lat, km, tilt, bearing: {'t': t, 'lon': lon, 'lat': lat, 'km': km, 'tilt': tilt, 'bearing': bearing}
camera = [
    cam(0.0, 55.18, 25.12, 70, 30, -25), cam(3.4, 55.15, 25.08, 52, 38, -10), cam(7.3, 55.10, 25.05, 40, 42, 8),
    cam(8.7, 55.06, 25.06, 26, 45, 20),                          # both Palms
    cam(10.6, 55.04, 24.975, 13, 46, 30), cam(12.4, 55.02, 24.985, 15, 46, 32), cam(15.8, 55.015, 24.99, 14, 46, 38),
    cam(17.7, 55.21, 25.06, 44, 36, 10),                         # flight east
    cam(19.9, 55.392, 25.114, 11, 46, -10), cam(23.3, 55.392, 25.114, 9, 47, -24),
    cam(24.9, 55.22, 25.04, 52, 40, 0), cam(35.8, 55.20, 25.04, 46, 42, 14),   # both sites under the comparison card
    cam(38.3, ps_c[0], ps_c[1] + 0.004, 9, 46, 30), cam(41.0, ps_c[0], ps_c[1] + 0.004, 8, 47, 38),
    cam(43.4, 55.19, 25.05, 38, 40, 20), cam(46.8, 55.19, 25.05, 34, 42, 28),
    cam(49.4, 55.085, 24.965, 32, 44, 40), cam(53.4, 55.095, 24.96, 32, 44, 44),   # growth corridor, NE up
    cam(55.2, 55.10, 24.99, 44, 40, 40), cam(58.8, 55.08, 24.98, 38, 42, 46),
    cam(60.6, PJ_C[0], PJ_C[1], 11, 45, 20), cam(62.8, PJ_C[0] - 0.005, PJ_C[1] - 0.005, 10, 46, 0),
    cam(64.6, PJA_C[0], PJA_C[1], 13, 45, 10), cam(67.3, PJA_C[0] + 0.01, PJA_C[1], 16, 45, 20),
    cam(68.5, 54.80, 24.78, 120, 28, 10),                        # flight to Abu Dhabi
    cam(69.9, 54.61, 24.49, 15, 44, 0), cam(71.3, 54.44, 24.55, 18, 44, -10), cam(73.0, 54.52, 24.52, 36, 42, -4), cam(77.9, 54.53, 24.52, 32, 44, 8),
    cam(80.2, 54.85, 24.78, 120, 28, 10),                        # flight back
    cam(82.4, 55.21, 25.04, 48, 42, 10), cam(88.4, 55.20, 25.04, 40, 44, 22), cam(94.8, 55.20, 25.05, 46, 40, 30),
]

F = lambda **k: k
features = [
    # Nakheel: both Palms, then Sheikh Zayed Road and the plot.
    F(kind='area', lines=feat['palmJumeirah'], color=PALM, start=7.5, end=12.0, draw=1.0, label='Palm Jumeirah', anchor=PJ_C),
    F(kind='line', lines=feat['palmJebelAli'], color=PALM, start=7.9, end=16.0, draw=1.0, label='Palm Jebel Ali', anchor=PJA_C, dim=True, labelEnd=12.3),
    F(kind='line', lines=feat['szr'], color=ROAD, start=10.0, end=16.0, draw=1.4, label='Sheikh Zayed Road', anchor=[55.058, 24.951], side='down', labelEnd=12.3),
    F(kind='area', lines=[ps], color=NAK, start=10.8, end=16.0, draw=0.9, label='Palm Springs', chip='Nakheel · approx. site', anchor=ps_c, dim=True, labelEnd=12.3),
    F(kind='line', lines=[[ps_c, PJA_C]], color=WHITE, start=12.4, end=16.0, draw=1.0, label='Next to Palm Jebel Ali', anchor=[(ps_c[0] + PJA_C[0]) / 2, (ps_c[1] + PJA_C[1]) / 2], pulse=False),
    # Aldar near Silicon Oasis.
    F(kind='area', lines=feat['dso'], color=WHITE, start=20.4, end=24.6, draw=0.9, label='Dubai Silicon Oasis', anchor=[55.383, 25.123], dim=True),
    F(kind='pin', at=ALDAR_PIN, color=ALD, start=21.3, end=24.6, label='Aldar community', chip='approx. site', side='down'),
    # Both sites on the wide map while the comparison card runs.
    F(kind='pin', at=ps_c, color=NAK, start=24.9, end=36.0),
    F(kind='pin', at=ALDAR_PIN, color=ALD, start=24.9, end=36.0),
    # Nakheel emphasis, then other developers.
    F(kind='area', lines=[ps], color=NAK, start=38.2, end=42.0, draw=0.8, label="Nakheel's project", chip='Palm Springs', anchor=ps_c),
    *[F(kind='pin', at=p, color=RED, start=44.4 + 0.18 * i, end=47.0) for i, p in enumerate(OTHERS)],
    F(kind='pin', at=[55.24, 25.075], color=RED, start=45.6, end=47.0, label='Other private developers', chip='illustrative', pulse=False),
    F(kind='pin', at=ps_c, color=NAK, start=43.4, end=47.0, label='Nakheel', side='down'),
    # Growth corridor.
    F(kind='line', lines=feat['szr'], color='#FFC940', start=47.1, end=55.0, draw=1.6, dim=True),
    F(kind='area', lines=[ps], color=NAK, start=47.4, end=59.0, draw=0.6, dim=True),
    F(kind='line', lines=feat['palmJebelAli'], color=PALM, start=49.5, end=59.0, draw=0.9, label='Palm Jebel Ali', anchor=PJA_C, dim=True, labelEnd=55.0),
    F(kind='area', lines=feat['airport'], color=AIR, start=50.4, end=59.0, draw=0.9, label='Al Maktoum Airport', anchor=[55.15, 24.915], dim=True, labelEnd=55.0),
    F(kind='area', lines=feat['jafza'], color=ZONE, start=51.3, end=59.0, draw=0.9, label='Jebel Ali Free Zone', anchor=JAFZA_C, side='down', dim=True, labelEnd=55.0),
    F(kind='pin', at=PORT, color=ZONE, start=52.2, end=55.0, label='Jebel Ali Port'),
    # Nakheel's record.
    F(kind='area', lines=feat['palmJumeirah'], color=PALM, start=60.5, end=64.4, draw=1.2, anchor=PJ_C),
    F(kind='line', lines=feat['palmJebelAli'], color=PALM, start=63.4, end=67.6, draw=1.2, anchor=PJA_C),
    # Aldar's record in Abu Dhabi.
    F(kind='area', lines=feat['yas'], color=ALD, start=69.3, end=78.2, draw=1.0, label='Yas Island', anchor=[54.605, 24.49], dim=True, side='down'),
    F(kind='area', lines=feat['saadiyat'], color=ALD, start=70.6, end=78.2, draw=1.0, label='Saadiyat Island', anchor=[54.44, 24.55], dim=True, side='down'),
    # Launch: both sites.
    F(kind='area', lines=[ps], color=NAK, start=82.2, end=88.6, draw=0.7),
    F(kind='pin', at=ps_c, color=NAK, start=82.4, end=88.6, label='Nakheel', chip='Phase 1 · launching soon'),
    F(kind='area', lines=feat['dso'], color=WHITE, start=82.2, end=88.6, draw=0.7, dim=True),
    F(kind='pin', at=ALDAR_PIN, color=ALD, start=82.8, end=88.6, label='Aldar', chip='Phase 1 · launching soon', side='down'),
]

captions = [
    (3.40, 5.45, 'Because two *government-backed developers'), (5.50, 7.38, 'are going to bring about a *major *change.'),
    (7.45, 9.00, 'Palm Jumeirah and Palm Jebel Ali'), (9.00, 10.00, 'is launching a *townhouse'), (10.00, 12.00, 'and villa community on Sheikh Zayed Road,'),
    (12.00, 16.00, 'just *five *minutes away from Palm Jebel Ali.'),
    (16.00, 17.50, 'And *Aldar, an Abu Dhabi government-backed'), (17.50, 19.00, 'developer, is going to'), (19.00, 20.50, 'launch a *beautiful community'),
    (20.50, 22.00, 'spread across *40 *million square'), (22.00, 23.45, 'feet near Silicon Oasis.'),
    (23.50, 25.45, 'Both projects will have 3 and 4-bedroom *townhouses.'), (25.50, 27.40, 'They will also have 3, 4 and 5-bedroom *villas.'),
    (27.40, 31.50, 'Prices are expected to start around *3 *million for a 3-bedroom townhouse,'),
    (31.55, 35.70, 'with around *10% down payment and flexible payment plans.'),
    (36.00, 39.45, 'Getting a unit in either project is going to be a very, very *difficult task,'), (39.50, 41.00, "especially in *Nakheel's project,"),
    (41.00, 43.40, 'because the price per square foot they are launching at'), (43.40, 46.95, 'is very, very *attractive compared to other private developers in Dubai.'),
    (47.00, 49.45, "And Nakheel's project is in Dubai's *growth *corridor."), (49.50, 50.40, 'That means *Palm *Jebel *Ali,'),
    (50.40, 53.45, 'Al Maktoum Airport, Jebel Ali Free Zone and Dubai Port'), (53.50, 55.00, 'are all on *this *side of Dubai.'),
    (55.00, 58.95, 'And there is not much *supply of townhouses and villas on this side of Dubai.'),
    (59.00, 60.45, 'Okay, so talking about *Nakheel,'), (60.50, 64.45, 'they have built *world-famous projects like Palm Jumeirah and Palm Jebel Ali,'),
    (64.50, 67.45, 'and many, many more *ultra-luxury projects in Dubai.'),
    (67.50, 69.00, 'And Aldar is the *master *developer behind'), (69.00, 72.95, "Abu Dhabi's *Yas *Island, *Saadiyat *Island and many other islands."),
    (73.00, 76.00, 'They hold *major *land *banks in Abu Dhabi,'), (76.00, 77.95, 'and they can easily execute *multi-billion-dollar projects.'),
    (78.00, 82.95, 'The *first *phases of both projects are going to launch in just a few weeks.'),
    (83.00, 86.45, 'People who invest in the first phase can see *maximum *returns,'), (86.50, 88.45, 'especially in a *government-backed project like this.'),
    (89.00, 90.45, 'To know more about these projects,'), (90.50, 92.40, 'comment *INVEST.'),
]

H = lambda start, end, lines, kicker=None, y=250, align='left': {'start': start, 'end': end, 'lines': lines, 'kicker': kicker, 'y': y, 'align': align}
headlines = [
    H(0.25, 3.35, ["DON'T BUY", 'PROPERTY IN', '*DUBAI'], 'WATCH THIS FIRST'),
    H(3.45, 5.40, ['2 DEVELOPERS', '*govt-backed'], 'A MAJOR CHANGE'),
    H(16.0, 19.6, ['ALDAR', '*Abu Dhabi'], 'GOVERNMENT-BACKED'),
    H(41.2, 46.8, ['PRICE PER', 'SQ FT', '*attractive'], 'LAUNCH PRICING'),
    H(47.0, 49.4, ["DUBAI'S", '*growth', 'corridor'], "NAKHEEL'S LOCATION"),
    H(59.0, 60.5, ['NAKHEEL'], 'TRACK RECORD'),
    H(67.5, 69.3, ['ALDAR'], 'MASTER DEVELOPER'),
    H(83.1, 88.4, ['PHASE 1', '*advantage'], 'EARLY INVESTORS'),
]

cards = [
    {'type': 'badges', 'start': 3.6, 'end': 7.3, 'items': [
        {'name': 'NAKHEEL', 'sub': 'Dubai government-backed', 'color': NAK},
        {'name': 'ALDAR', 'sub': 'Abu Dhabi government-backed', 'color': ALD}]},
    {'type': 'count', 'start': 20.6, 'end': 23.4, 'value': 40, 'suffix': 'M', 'unit': 'square feet', 'note': 'AS STATED · NEAR DUBAI SILICON OASIS', 'color': ALD, 'y': 370},
    {'type': 'compare', 'start': 23.5, 'end': 35.8,
     'columns': [{'name': 'NAKHEEL', 'color': NAK, 'place': 'Palm Springs · Jebel Ali'}, {'name': 'ALDAR', 'color': ALD, 'place': 'Near Dubai Silicon Oasis'}],
     'rows': [
         {'at': 23.7, 'label': 'TOWNHOUSES', 'value': '3 & 4 bedrooms'},
         {'at': 25.6, 'label': 'STANDALONE VILLAS', 'value': '3, 4 & 5 bedrooms'},
         {'at': 27.8, 'label': 'EXPECTED FROM', 'value': '~ AED 3 million', 'note': '3-bedroom townhouse'},
         {'at': 31.9, 'label': 'DOWN PAYMENT', 'value': '~ 10%', 'note': 'flexible payment plans'},
     ]},
    {'type': 'stamp', 'start': 36.5, 'end': 39.4, 'text': 'HIGH DEMAND', 'sub': 'UNITS WILL BE HARD TO GET', 'color': '#FF5C70', 'y': 600},
    {'type': 'meter', 'start': 55.2, 'end': 58.9, 'label': 'VILLA & TOWNHOUSE SUPPLY', 'level': 0.22, 'color': '#FF5C70', 'caption': 'on this side of Dubai'},
    {'type': 'list', 'start': 60.5, 'end': 67.4, 'title': 'NAKHEEL HAS BUILT', 'color': PALM, 'y': 560, 'items': [
        {'at': 61.6, 'text': 'Palm Jumeirah'}, {'at': 63.3, 'text': 'Palm Jebel Ali'}, {'at': 64.9, 'text': 'Ultra-luxury projects'}]},
    {'type': 'list', 'start': 73.0, 'end': 78.0, 'title': 'ALDAR IN ABU DHABI', 'color': ALD, 'y': 560, 'items': [
        {'at': 73.3, 'text': 'Major land banks'}, {'at': 76.2, 'text': 'Multi-billion-dollar projects'}]},
    {'type': 'stamp', 'start': 78.6, 'end': 82.8, 'text': 'PHASE 1', 'sub': 'LAUNCHING IN WEEKS', 'color': '#FFC940', 'y': 600},
]

S = lambda f, at, v=0.4: {'file': f'sfx/{f}.wav', 'at': at, 'volume': v}
sounds = [
    S('impact', 0.25, 0.35), S('tick', 0.9, 0.4), S('tick', 1.6, 0.4), S('whoosh', 3.3, 0.3), S('impact', 3.6, 0.3), S('pop', 3.75, 0.4), S('pop', 3.9, 0.4),
    S('whoosh', 7.25, 0.35), S('shimmer', 7.6, 0.25), S('whoosh_soft', 9.9, 0.25), S('shimmer', 10.9, 0.3), S('pop', 11.2, 0.4), S('tick', 12.5, 0.4),
    S('whoosh', 16.0, 0.35), S('riser', 18.2, 0.2), S('impact', 20.6, 0.3), S('pop', 21.6, 0.4),
    S('whoosh', 23.4, 0.3), S('tick', 23.7, 0.45), S('tick', 25.6, 0.45), S('pop', 27.8, 0.45), S('pop', 31.9, 0.45),
    S('impact', 36.5, 0.35), S('whoosh', 36.2, 0.3), S('shimmer', 38.6, 0.25), S('whoosh_soft', 41.1, 0.25),
    *[S('tick', 44.4 + 0.18 * i, 0.3) for i in range(6)], S('riser', 44.6, 0.22),
    S('impact', 47.0, 0.3), S('whoosh_soft', 47.2, 0.25), S('pop', 49.6, 0.4), S('pop', 50.5, 0.4), S('pop', 51.4, 0.4), S('pop', 52.3, 0.4),
    S('whoosh', 53.6, 0.25), S('tick', 55.4, 0.4),
    S('whoosh', 59.1, 0.3), S('shimmer', 60.7, 0.25), S('pop', 61.6, 0.4), S('pop', 63.3, 0.4), S('pop', 64.9, 0.4),
    S('whoosh', 67.4, 0.4), S('riser', 67.6, 0.2), S('impact', 69.4, 0.25), S('shimmer', 70.7, 0.25), S('pop', 73.3, 0.4), S('pop', 76.2, 0.4),
    S('whoosh', 78.3, 0.35), S('impact', 78.6, 0.35), S('whoosh_soft', 80.4, 0.25), S('pop', 82.5, 0.4), S('pop', 82.9, 0.4),
    S('shimmer', 83.2, 0.25), S('whoosh', 88.6, 0.35), S('pop', 89.0, 0.4),
    *[S('tick', 90.2 + 0.17 * i, 0.35) for i in range(6)], S('pop', 91.6, 0.45), S('shimmer', 91.9, 0.3),
]

edit = {
    'durationSeconds': 94.76,
    'mapFile': 'mr1/map.json',
    'camera': camera,
    'features': features,
    'captions': [{'start': a, 'end': b, 'text': t} for a, b, t in captions],
    'headlines': headlines,
    'cards': cards,
    'speaker': {'video': 'mr1/speaker.mp4', 'hide': [[7.43, 7.70]]},
    'voice': 'mr1/voice.wav',
    'music': {'file': 'mr1/music.wav', 'volume': 0.13},
    'sounds': sounds,
    'endCard': {'start': 88.8, 'keyword': 'INVEST', 'phone': '+971 56 837 6676', 'detail': 'and get the full details on both projects'},
    'credit': 'Map data © OpenStreetMap contributors · Outlines and sites approximate',
    'disclaimer': [{'start': 27.4, 'end': 35.8, 'text': 'EXPECTED FIGURES · NOT YET OFFICIAL · SUBJECT TO LAUNCH'}],
}
(HERE / 'edit.json').write_text(json.dumps(edit))
print('edit.json', len(camera), 'camera keys', len(features), 'features', len(captions), 'captions', len(cards), 'cards')
