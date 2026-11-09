"""Build edit.json for the Rockefeller reel (StoryReel). Times are seconds in the speaker's own pre-cut recording."""
import json
from pathlib import Path

HERE = Path(__file__).parent
TOTAL = 63.78
GOLD, BLUE, RED = '#FFC940', '#6C8CFF', '#FF5C70'

wc = lambda t, lon, lat, zoom: {'t': t, 'lon': lon, 'lat': lat, 'zoom': zoom}
scenes = [
    {'kind': 'world', 'start': 0.0, 'end': 5.6, 'camera': [wc(0, 25, 18, 1.55), wc(5.6, 45, 20, 1.9)]},
    {'kind': 'wallet', 'start': 5.6, 'end': 10.2, 'revealAt': 9.0},
    {'kind': 'profit', 'start': 10.2, 'end': 14.6, 'source': 'VISA FISCAL YEAR 2025 · $20.06B NET INCOME ON $40.0B REVENUE'},
    {'kind': 'bank', 'start': 14.6, 'end': 22.0, 'steps': [14.8, 16.7, 19.6]},
    {'kind': 'world', 'start': 22.0, 'end': 32.6, 'camera': [wc(22, 30, 22, 2.6), wc(27, 50, 20, 2.1), wc(32.6, 55.3, 25.2, 3.4)], 'busy': [22.0, 27.5],
     'fees': [26.5 + 0.42 * i for i in range(14)]},
    {'kind': 'video', 'start': 32.6, 'end': 45.0, 'src': 'rk/dubai.mp4'},
    {'kind': 'image', 'start': 40.1, 'end': 41.75, 'src': 'rk/tower_clouds.jpg', 'zoom': [1.0, 1.08],
     'title': {'kicker': 'INTRODUCING', 'lines': ['Christian A. Rockefeller', 'BUSINESS TOWER']}},
    {'kind': 'image', 'start': 44.85, 'end': 47.05, 'src': 'rk/tower_night.jpg', 'zoom': [1.05, 1.16], 'pan': [[0, 0.02], [0, -0.02]]},
    {'kind': 'image', 'start': 47.05, 'end': 51.25, 'src': 'rk/nyc_legacy.jpg', 'zoom': [1.0, 1.12]},
    {'kind': 'image', 'start': 51.25, 'end': 53.0, 'src': 'rk/tower_clouds2.jpg', 'zoom': [1.12, 1.0]},
    {'kind': 'image', 'start': 53.0, 'end': 54.7, 'src': 'rk/boardroom.jpg', 'zoom': [1.0, 1.1]},
    {'kind': 'image', 'start': 54.7, 'end': 56.7, 'src': 'rk/tower_top_sunset.jpg', 'zoom': [1.0, 1.12], 'pan': [[0, -0.02], [0, 0.02]]},
    {'kind': 'image', 'start': 56.7, 'end': 59.1, 'src': 'rk/rooftop_pool.jpg', 'zoom': [1.0, 1.1]},
    {'kind': 'image', 'start': 59.1, 'end': TOTAL + 0.5, 'src': 'rk/lobby.jpg', 'zoom': [1.0, 1.08]},
]

captions_src = [
    (0.00, 1.75, 'Do you know the *most *profitable company in the world?'), (1.75, 3.45, 'Not Apple, not Nvidia,'),
    (3.45, 5.40, 'not even an *oil company.'), (5.45, 7.95, 'This company is in your *pocket right now.'),
    (7.95, 9.00, 'Open your wallet…'), (9.00, 10.35, '*Visa, or Mastercard!'),
    (10.35, 13.45, 'Visa makes *50% net profit on every dollar it makes.'), (13.55, 14.65, "Here's the *interesting part:"),
    (14.65, 16.60, "Visa doesn't give you your debit or credit card. The *bank does."), (16.60, 19.50, "Visa doesn't give you a loan. The *bank does."),
    (19.55, 21.95, 'No risk for Visa. *Easy *profits.'), (22.00, 23.20, "They're like a *bridge."),
    (23.20, 26.30, 'Wherever money moves in the world, it crosses *this *bridge.'), (26.35, 28.70, 'Every time you swipe your card, a small *fee.'),
    (28.75, 32.50, 'Every day, silently, *billions of transactions around the world, and they make profits from it.'),
    (32.55, 34.90, 'Dubai real estate has the same kind of *silent *opportunity:'), (34.90, 36.20, '*commercial real estate.'),
    (36.20, 40.10, 'Invest 13 crores and earn up to *1.3 *crore in rent, in this project:'),
    (40.10, 41.85, '*Christian *A. *Rockefeller Business Tower.'), (41.85, 44.75, '400 metres, *87 *floors, on Sheikh Zayed Road.'),
    (44.75, 46.95, "This is Dubai's *tallest *commercial tower."), (46.95, 51.30, "The world's first billionaire, the Rockefeller family's *sixth *generation, Christian Rockefeller is the brand."),
    (51.50, 52.95, 'Easy *50-50 payment plan.'), (52.95, 54.65, 'Offices start from *13 *crores.'),
    (54.65, 56.80, 'If you want silent, massive profits like *Visa,'), (56.80, 58.80, 'this project should be on your *watch *list.'),
    (58.95, 61.45, 'For more information, comment *ROCKEFELLER'), (61.45, 62.85, 'or contact the number on screen.'), (62.85, TOTAL - 0.1, "*I'll get in touch."),
]
captions = [{'start': a, 'end': b, 'text': t} for a, b, t in captions_src]

H = lambda a, b, lines, kicker, y=250: {'start': a, 'end': b, 'lines': lines, 'kicker': kicker, 'y': y, 'align': 'left'}
headlines = [
    H(0.15, 1.65, ['WHICH', '*company?'], 'QUICK QUESTION'),
    H(22.0, 26.2, ['A BRIDGE', '*for money'], 'THE NETWORK'),
    H(28.8, 32.5, ['BILLIONS OF', '*transactions'], 'EVERY DAY'),
    H(32.6, 36.2, ['COMMERCIAL', '*property'], "DUBAI'S SILENT OPPORTUNITY"),
]

cards = [
    {'type': 'list', 'start': 42.0, 'end': 44.75, 'title': 'THE TOWER', 'color': GOLD, 'y': 560, 'items': [
        {'at': 42.9, 'text': '87 floors'}, {'at': 44.0, 'text': 'Sheikh Zayed Road'}]},
    {'type': 'list', 'start': 45.0, 'end': 46.95, 'title': "DEVELOPER'S PLAN", 'color': GOLD, 'y': 560, 'items': [
        {'at': 45.4, 'text': "Dubai's tallest commercial tower"}]},
    {'type': 'count', 'start': 48.6, 'end': 51.2, 'value': 6, 'suffix': 'th', 'unit': 'generation Rockefeller', 'note': 'CHRISTIAN A. ROCKEFELLER · BRAND PARTNER', 'color': GOLD, 'y': 560},
    {'type': 'list', 'start': 51.5, 'end': 52.95, 'title': 'PAYMENT PLAN', 'color': GOLD, 'y': 560, 'items': [
        {'at': 51.7, 'text': '50% during construction'}, {'at': 52.2, 'text': '50% on handover'}]},
    {'type': 'list', 'start': 53.1, 'end': 54.65, 'title': 'GRADE A OFFICES', 'color': GOLD, 'y': 560, 'items': [
        {'at': 53.3, 'text': 'From 1,077 sq ft'}]},
]

S = lambda f, at, v=0.4: {'file': f'sfx/{f}.wav', 'at': at, 'volume': v}
# Essential moments only (about half of the first cut): scene changes, the card and tower reveals, the dial landing,
# a few swipe-fee ticks and a short typing burst on the comment card.
sounds = sorted([
    S('impact', 0.15, 0.3),
    S('whoosh', 5.5, 0.3),
    S('riser', 7.6, 0.2), S('impact', 9.0, 0.4), S('shimmer', 9.1, 0.3),
    S('whoosh', 10.1, 0.3), S('pop', 11.8, 0.45),
    S('whoosh', 14.5, 0.3), S('impact', 19.6, 0.3),
    S('whoosh', 21.9, 0.35), *[S('tick', 26.5 + 0.84 * i, 0.2) for i in range(5)],
    S('riser', 31.0, 0.2), S('whoosh', 32.5, 0.35),
    S('whoosh', 40.0, 0.35), S('impact', 40.15, 0.35),
    S('pop', 42.9, 0.4), S('whoosh_soft', 44.8, 0.25), S('whoosh_soft', 47.0, 0.25), S('impact', 48.6, 0.25),
    S('whoosh_soft', 51.2, 0.25), S('whoosh_soft', 54.7, 0.25),
    S('whoosh', 59.0, 0.35), *[S('tick', 60.5 + 0.2 * i, 0.3) for i in range(4)], S('pop', 61.8, 0.45),
], key=lambda s: s['at'])

edit = {
    'durationSeconds': TOTAL,
    'scenes': scenes,
    'captions': captions,
    'headlines': headlines,
    'cards': cards,
    'speaker': {'video': 'rk/speaker.mp4', 'hide': [[0, 5.9]]},
    'speakerIntro': {'video': 'rk/speaker_intro.mp4', 'end': 5.45},
    'hookLogos': {'person': 'rk/person.webm', 'items': [
        {'src': 'rk/apple.svg', 'at': 1.80, 'x': 300, 'y': 720, 'width': 230, 'strike': True},
        {'src': 'rk/nvidia.svg', 'at': 2.62, 'x': 885, 'y': 760, 'width': 320, 'strike': True},
        {'src': 'oil', 'at': 4.35, 'x': 540, 'y': 470, 'width': 180, 'strike': True},
    ]},
    'voice': 'rk/voice.wav',
    'music': {'file': 'rk/music.wav', 'volume': 0.12},
    'sounds': sounds,
    'endCard': {'start': 59.0, 'keyword': 'ROCKEFELLER', 'phone': '+971 56 837 6676', 'detail': "and I'll get in touch"},
    'credits': [
        {'start': 32.6, 'end': 40.1, 'text': 'Map data © OpenStreetMap contributors'},
        {'start': 41.75, 'end': 45.0, 'text': 'Map data © OpenStreetMap contributors · Site approximate'},
        {'start': 40.1, 'end': 41.75, 'text': "Renders: LMD factsheet, artist's impressions"},
        {'start': 45.0, 'end': 59.0, 'text': "Renders: LMD factsheet, artist's impressions · Expected handover Q2 2031"},
    ],
}
(HERE / 'edit.json').write_text(json.dumps(edit))
(HERE / 'work' / 'music_points.json').write_text(json.dumps({'lifts': [22.0, 40.1], 'total': TOTAL}))
print('edit.json', len(scenes), 'scenes,', len(captions), 'captions,', len(cards), 'cards')
