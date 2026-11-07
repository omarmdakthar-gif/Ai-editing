"""Build edit.json for the Palm Springs reel (ExplainerReel). Times are seconds on the reel's timeline."""
import json
from pathlib import Path

HERE = Path(__file__).parent
WORK = HERE / 'work'
PUBLIC = HERE.parent.parent / 'tools' / 'remotion' / 'public'
C = {'plot': '#D45CF0', 'palm': '#45E8EC', 'green': '#4FD08A', 'blue': '#6C8CFF', 'amber': '#F5B042', 'beach': '#BDF23C', 'white': '#FFFFFF'}

osm = lambda name: json.loads((WORK / 'osm' / name).read_text())
ways = lambda name: [[[p['lon'], p['lat']] for p in e['geometry']] for e in osm(name)['elements'] if 'geometry' in e]
plot = json.loads((HERE.parent.parent / 'atlas/dubai/manual.geojson').read_text())['features'][0]['geometry']['coordinates'][0]
harbour = ways('harbour.json')
airport = ways('airport.json')
szr = ways('szr.json')
palm = osm('palm.json')
beach = osm('beach_line.json')
route = osm('route_airport.json')['routes'][0]['geometry']['coordinates']
route_marina = osm('route_marina.json')['routes'][0]['geometry']['coordinates']
route_expo = osm('route_expo.json')['routes'][0]['geometry']['coordinates']
pin = lambda lon, lat: [[[lon, lat], [lon, lat]]]

# Earth shots. `from` is seconds into each Earth Studio render.
clips = [
    {'kind': 'earth', 'start': 0.00, 'end': 0.75, 'earth': 'plot', 'from': 19.0},
    {'kind': 'earth', 'start': 0.75, 'end': 1.45, 'earth': 'airport', 'from': 6.0},
    {'kind': 'earth', 'start': 1.45, 'end': 2.45, 'earth': 'coast', 'from': 8.5},
    {'kind': 'earth', 'start': 2.45, 'end': 2.95, 'earth': 'coast', 'from': 1.0},
    {'kind': 'speaker', 'start': 2.95, 'end': 3.95, 'video': 'ps/b.mp4', 'from': 0},
    {'kind': 'earth', 'start': 3.95, 'end': 9.15, 'earth': 'plot', 'from': 0, 'cutout': {'edge': 0.64, 'video': 'ps/b.webm', 'from': 1.0}},
    {'kind': 'earth', 'start': 9.15, 'end': 23.85, 'earth': 'plot', 'from': 5.2, 'cutout': {'edge': 0.57, 'video': 'ps/c.webm', 'from': 0}},
    {'kind': 'speaker', 'start': 23.85, 'end': 25.35, 'video': 'ps/d.mp4', 'from': 0},
    {'kind': 'earth', 'start': 25.35, 'end': 31.5, 'earth': 'airport', 'from': 0, 'cutout': {'edge': 0.55, 'video': 'ps/d.webm', 'from': 1.5}},
    {'kind': 'earth', 'start': 31.5, 'end': 36.7, 'earth': 'coast', 'from': 0, 'cutout': {'edge': 0.55, 'video': 'ps/d.webm', 'from': 7.65}},
    {'kind': 'earth', 'start': 36.7, 'end': 49.1, 'earth': 'coast', 'from': 5.2, 'cutout': {'edge': 0.6, 'video': 'ps/e.webm', 'from': 0}},
    {'kind': 'earth', 'start': 49.1, 'end': 52.8, 'earth': 'coast', 'from': 17.6, 'cutout': {'edge': 0.58, 'video': 'ps/f.webm', 'from': 0}},
    {'kind': 'speaker', 'start': 52.8, 'end': 60.4, 'video': 'ps/g.mp4', 'from': 0},
    {'kind': 'speaker', 'start': 60.4, 'end': 62.2, 'video': 'ps/g.mp4', 'from': 7.5},
]

shapes = [
    # Cold-open flashes, each gone when its shot ends.
    {'kind': 'area', 'lines': harbour, 'color': C['blue'], 'start': 0.0, 'hide': 0.75, 'drawSeconds': 0.35},
    {'kind': 'area', 'lines': airport, 'color': C['amber'], 'start': 0.75, 'hide': 1.45, 'drawSeconds': 0.35},
    {'kind': 'line', 'lines': [beach], 'color': C['beach'], 'start': 1.45, 'hide': 2.45, 'drawSeconds': 0.5},
    {'kind': 'line', 'lines': palm, 'color': C['palm'], 'start': 2.45, 'hide': 2.95, 'drawSeconds': 0.35},
    # Main story.
    # The plot's south edge is Sheikh Zayed Road itself, so a pin there reads better than the long road line.
    {'kind': 'line', 'lines': pin(55.044, 24.9426), 'color': C['white'], 'start': 6.0, 'label': 'Sheikh Zayed Road', 'end': 8.1},
    {'kind': 'area', 'lines': [plot], 'color': C['plot'], 'start': 8.2, 'drawSeconds': 0.9, 'label': 'Palm Springs', 'anchor': [55.039, 24.951]},
    {'kind': 'line', 'lines': pin(55.072, 24.985), 'color': C['green'], 'start': 10.3, 'label': 'Jafza', 'chip': 'Jebel Ali Free Zone'},
    {'kind': 'area', 'lines': harbour, 'color': C['blue'], 'start': 14.4, 'drawSeconds': 1.0, 'label': 'Jebel Ali Port', 'anchor': [55.050, 25.005]},
    {'kind': 'line', 'lines': [route], 'color': C['white'], 'start': 25.4, 'drawSeconds': 2.6, 'label': 'Passenger terminal', 'chip': '20\u201325 min drive', 'anchor': route[-1]},
    {'kind': 'area', 'lines': airport, 'color': C['amber'], 'start': 26.4, 'drawSeconds': 1.0, 'label': 'Al Maktoum Airport', 'anchor': [55.150, 24.905]},
    {'kind': 'line', 'lines': palm, 'color': C['palm'], 'start': 32.8, 'drawSeconds': 1.6, 'label': 'Palm Jebel Ali', 'chip': '2x Palm Jumeirah', 'anchor': [54.988, 25.008]},
    {'kind': 'line', 'lines': [beach], 'color': C['beach'], 'start': 37.6, 'drawSeconds': 1.6, 'label': 'Jebel Ali Beach', 'chip': '6.6 km · planned, illustrative', 'anchor': beach[len(beach) // 2]},
    # Real road routes from the plot (OSRM, no traffic): Marina about 19 min, Expo City about 18 min.
    {'kind': 'line', 'lines': [route_marina], 'color': C['amber'], 'start': 49.2, 'drawSeconds': 1.6, 'label': 'Dubai Marina', 'chip': '~20 min', 'anchor': route_marina[-1]},
    {'kind': 'line', 'lines': [route_expo], 'color': C['palm'], 'start': 50.3, 'drawSeconds': 1.6, 'label': 'Expo City', 'chip': '~20 min', 'anchor': route_expo[-1]},
]
# Labels from the plot and airport beats crowd the wide shots, so drop the earlier ones' text once the camera pulls out.
for s in shapes:
    if s.get('label') in ('Jafza', 'Jebel Ali Port') and 'end' not in s:
        s['end'] = 23.85
    if s.get('label') in ('Passenger terminal', 'Al Maktoum Airport'):
        s['end'] = 31.5
    if s.get('label') == 'Palm Jebel Ali':
        s['end'] = 36.9
    if s.get('label') == 'Jebel Ali Beach':
        s['end'] = 43.3

# Phrase captions: (start, end, text). Words with * are accents.
phrases = [
    (2.95, 4.55, "Nakheel's *new"), (4.55, 6.05, 'townhouse and villa community,'), (6.07, 7.80, 'right on Sheikh Zayed Road:'),
    (8.20, 9.15, '*Palm *Springs.'),
    (9.21, 10.39, 'Look where it is:'), (10.39, 11.71, 'right by *Jafza,'), (11.71, 12.79, '*11,000 businesses'), (12.79, 13.77, 'running today.'),
    (13.77, 16.09, 'Jafza and Jebel Ali Port'), (16.09, 17.37, 'alone have created'), (17.37, 19.21, 'over a *million jobs,'),
    (19.21, 20.95, 'and provide *36%'), (20.95, 23.85, "of Dubai's GDP."),
    (23.92, 25.82, 'About *25 *minutes away'), (26.00, 27.06, 'is Al Maktoum'), (27.06, 28.12, 'International Airport,'),
    (28.30, 30.30, 'with a *128 *billion dirham'), (30.30, 31.54, 'budget approved.'),
    (31.54, 32.96, 'And right next to it,'), (32.96, 33.98, '*Palm *Jebel *Ali,'), (33.98, 35.30, '*twice the size'), (35.30, 36.70, 'of Palm Jumeirah.'),
    (36.77, 37.91, 'Jebel Ali Beach'), (37.91, 39.15, "is planned as Dubai's"), (39.15, 40.35, '*longest public beach,'), (40.35, 42.85, 'around *6.6 km.'),
    (43.45, 44.85, 'Jobs, an airport,'), (44.87, 46.35, 'beaches, an island,'), (46.43, 47.91, 'all around *one'), (47.91, 49.10, 'single *community.'),
    (49.20, 51.10, 'Dubai Marina and Expo City,'), (51.10, 52.80, 'about *20 minutes away.'),
    (52.88, 54.46, 'Just imagine the *potential'), (54.46, 55.34, 'of this project.'), (55.34, 56.54, 'All of Dubai is'),
    (56.54, 57.56, 'growing towards it.'), (57.56, 58.36, 'Comment *SPRINGS'), (58.36, 60.40, "and I'll send you the details."),
]


def caption(start, end, text):
    words = text.split()
    step = (end - start) * 0.8 / len(words)
    return {'end': end, 'words': [{'text': w.lstrip('*'), 'start': round(start + i * step, 2), 'accent': w.startswith('*')} for i, w in enumerate(words)]}


cards = [
    {'start': 11.6, 'end': 14.3, 'value': 11000, 'suffix': '+', 'unit': 'businesses in Jafza', 'color': C['green'], 'source': 'DUBAI MEDIA OFFICE, MAY 2025'},
    {'start': 17.3, 'end': 19.9, 'value': 1, 'suffix': 'M+', 'unit': 'jobs, Jafza + Jebel Ali Port', 'color': C['blue'], 'source': 'DUBAI MEDIA OFFICE'},
    {'start': 20.0, 'end': 23.6, 'value': 36, 'suffix': '%', 'unit': "of Dubai's GDP", 'color': C['blue'], 'source': 'DUBAI MEDIA OFFICE'},
    {'start': 28.2, 'end': 31.3, 'value': 128, 'prefix': 'AED ', 'suffix': 'B', 'unit': 'new passenger terminal, approved 2024', 'color': C['amber'], 'source': 'WAM · THE NATIONAL'},
]

S = lambda f, at, v=0.4: {'file': f'sfx/{f}.wav', 'at': at, 'volume': v}
sounds = [
    S('tick', 0.0, 0.6), S('tick', 0.75, 0.6), S('tick', 1.45, 0.6), S('tick', 2.45, 0.6), S('whoosh', 2.6, 0.35), S('impact', 2.95, 0.35),
    S('whoosh', 3.9, 0.35), S('whoosh_soft', 6.0, 0.25), S('shimmer', 8.6, 0.3), S('pop', 10.5, 0.4), S('tick', 11.6, 0.4),
    S('whoosh_soft', 14.4, 0.25), S('pop', 17.3, 0.4), S('pop', 20.0, 0.4),
    S('whoosh', 23.75, 0.3), S('whoosh', 25.3, 0.3), S('riser', 25.8, 0.22), S('impact', 28.3, 0.35),
    S('whoosh', 31.45, 0.3), S('shimmer', 33.6, 0.3), S('whoosh_soft', 36.7, 0.25), S('whoosh_soft', 37.6, 0.25),
    S('tick', 43.5, 0.5), S('tick', 44.2, 0.5), S('tick', 44.9, 0.5), S('tick', 45.9, 0.5), S('riser', 46.4, 0.2), S('impact', 48.9, 0.25),
    S('pop', 49.3, 0.4), S('pop', 50.4, 0.4), S('whoosh', 52.7, 0.3), S('pop', 57.5, 0.5), S('shimmer', 60.4, 0.3),
]

earths = {}
credits = set()
for key in ('plot', 'airport', 'coast'):
    cam = json.loads((PUBLIC / 'earth' / f'ps-{key}' / 'camera.json').read_text())
    earths[key] = {'video': f'earth/ps-{key}/map.mp4', 'frames': cam['frames']}
    credits.update(s.strip() for s in cam['sources'].replace('\n', ',').split(',') if s.strip())

edit = {
    'durationSeconds': 62.2,
    'handle': 'sanjayram.dxb',
    'name': 'Sanjay Ram',
    'voice': 'ps/voice.wav',
    'clips': clips,
    'earths': earths,
    'credit': 'Google Earth · Imagery: ' + ', '.join(sorted(credits)),
    'shapes': shapes,
    'captions': [caption(*p) for p in phrases],
    'cards': cards,
    'headlines': [{'start': 0.0, 'end': 2.95, 'lines': ['ALL AROUND', 'ONE COMMUNITY'], 'y': 26}, {'start': 46.4, 'end': 49.1, 'lines': ['ONE', 'COMMUNITY'], 'y': 26}],
    'flashWords': [{'start': 0.0, 'end': 0.75, 'text': 'JOBS'}, {'start': 0.75, 'end': 1.45, 'text': 'AIRPORT'}, {'start': 1.45, 'end': 2.45, 'text': 'BEACH'}, {'start': 2.45, 'end': 2.95, 'text': 'ISLAND'}],
    'comment': {'start': 57.5, 'end': 60.4, 'keyword': 'SPRINGS', 'detail': 'and I’ll send you the details', 'avatar': 'ps/avatar.jpg'},
    'endCard': {'start': 60.4, 'headline': 'Palm Springs', 'detail': 'Comment SPRINGS for the details',
                'credits': 'Outlines and routes: map data \u00a9 OpenStreetMap contributors, openstreetmap.org/copyright. Routes by OSRM. Imagery: Google Earth.'},
    'sounds': sounds,
    'music': {'file': 'ps/music.wav', 'volume': 0.11},
    'layout': 'v1',
}
(HERE / 'edit.json').write_text(json.dumps(edit))
print('edit.json', len(clips), 'clips', len(shapes), 'shapes', len(phrases), 'captions')
