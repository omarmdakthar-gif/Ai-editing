"""Props for the Dubai map clip (ShowcaseReel, no speaker/voice/captions), used inside the Rockefeller reel.

Clip time 0 = reel time 32.6 s. Wide Dubai, business districts light up, then a dive along Sheikh Zayed Road to the tower site.
"""
import json
from pathlib import Path

from shapely.geometry import shape

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
feat = json.loads((ROOT / 'tools' / 'remotion' / 'public' / 'mr1' / 'map.json').read_text())['feat']
atlas = json.loads((ROOT / 'atlas' / 'dubai' / 'atlas.geojson').read_text())['features']


def outline(name):
    for f in atlas:
        if f['properties'].get('name') == name and f['geometry']['type'] in ('Polygon', 'MultiPolygon'):
            g = shape(f['geometry'])
            g = max(g.geoms, key=lambda p: p.area) if g.geom_type == 'MultiPolygon' else g
            return [[[round(x, 5), round(y, 5)] for x, y in g.simplify(0.00004).exterior.coords]]
    raise KeyError(name)


GOLD, BLUE, CYAN, WHITE, RED = '#FFC940', '#6C8CFF', '#45E8EC', '#FFFFFF', '#FF5C70'
TOWER = [55.2648, 25.1963]   # approximate: on Sheikh Zayed Road between Burj Khalifa/Dubai Mall and Business Bay metro stations
cam = lambda t, lon, lat, km, tilt, bearing: {'t': t, 'lon': lon, 'lat': lat, 'km': km, 'tilt': tilt, 'bearing': bearing}
camera = [
    cam(0.0, 55.20, 25.12, 48, 32, -20), cam(3.5, 55.27, 25.19, 13, 44, 10), cam(7.4, 55.272, 25.195, 11, 45, 22),
    cam(9.3, TOWER[0], TOWER[1] + 0.004, 5.5, 47, 40), cam(12.4, TOWER[0], TOWER[1] + 0.003, 4.2, 48, 52),
]
F = lambda **k: k
features = [
    F(kind='area', lines=outline('Dubai International Financial Centre'), color=BLUE, start=1.2, end=7.6, draw=0.8, label='DIFC', dim=True),
    F(kind='area', lines=outline('Downtown Dubai'), color=CYAN, start=1.8, end=7.6, draw=0.8, label='Downtown', side='down', dim=True),
    F(kind='area', lines=outline('Business Bay'), color=BLUE, start=2.4, end=7.6, draw=0.8, dim=True),
    F(kind='area', lines=outline('Trade Centre'), color=CYAN, start=3.0, end=7.6, draw=0.8, dim=True),
    F(kind='line', lines=feat['szr'], color=RED, start=8.6, draw=1.2, label='Sheikh Zayed Road', anchor=[55.282, 25.214], side='down', labelEnd=9.2),
    F(kind='pin', at=TOWER, color=GOLD, start=9.4, label='Rockefeller Tower', chip='approx. site'),
]
edit = {
    'durationSeconds': 12.4,
    'mapFile': 'mr1/map.json',
    'camera': camera,
    'features': features,
    'captions': [],
    'credit': '',
}
(HERE / 'dubai.json').write_text(json.dumps(edit))
print('dubai.json written')
