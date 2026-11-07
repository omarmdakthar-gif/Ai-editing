"""Turn the raw OpenStreetMap downloads in work/osm into simplified map layers for the ShowcaseReel.

Writes tools/remotion/public/mr1/map.json:
  base: land polygons, water, roads by class, runways, district outlines, each at two levels of detail
  feat: story geometry (palms, Sheikh Zayed Road, plots, islands, airport, districts)
All coordinates are [lon, lat] rounded to 5 decimals (about 1 m).
"""
import json
from pathlib import Path

from shapely.geometry import LineString, MultiPolygon, Point, Polygon, box, shape
from shapely.ops import linemerge, polygonize, unary_union

HERE = Path(__file__).parent
OSM = HERE / 'work' / 'osm'
ROOT = HERE.parent.parent
OUT = ROOT / 'tools' / 'remotion' / 'public' / 'mr1' / 'map.json'

BBOX = (54.25, 24.30, 55.60, 25.40)  # west, south, east, north
FINE, COARSE = 0.00004, 0.00035      # simplification tolerances in degrees (about 4 m and 35 m)

load = lambda name: json.loads((OSM / name).read_text())['elements']
ways = lambda name, **tags: [e for e in load(name) if e['type'] == 'way' and 'geometry' in e and all(e.get('tags', {}).get(k) == v for k, v in tags.items())]
coords = lambda e: [(p['lon'], p['lat']) for p in e['geometry']]
rnd = lambda pts: [[round(x, 5), round(y, 5)] for x, y in pts]


def rings(geom):
    """Exterior rings of a polygon or multipolygon as coordinate lists."""
    polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    return [list(p.exterior.coords) for p in polys if not p.is_empty]


def lines_out(lines, tol, min_len=0.0):
    out = []
    for line in lines:
        s = line.simplify(tol, preserve_topology=False)
        if s.length >= min_len and len(s.coords) >= 2:
            out.append(rnd(s.coords))
    return out


# ---------- Land from the coastline ----------
coast = linemerge([LineString(coords(e)) for e in ways('coast.json')])
frame = box(*BBOX)
faces = list(polygonize(unary_union([coast, frame.exterior]).intersection(frame.buffer(1e-9))))
sea_points = [Point(55.00, 25.35), Point(54.60, 24.75), Point(55.40, 25.39), Point(54.30, 24.62)]
land = [f for f in faces if not any(f.contains(p) for p in sea_points) and f.area > 2e-7]
print('coast faces', len(faces), 'land faces', len(land))
land_union = unary_union(land)


def polys_out(geom, tol, min_area):
    out = []
    for p in (geom.geoms if isinstance(geom, MultiPolygon) else [geom]):
        if p.area < min_area:
            continue
        s = p.simplify(tol, preserve_topology=True)
        if not s.is_empty:
            out.append(rnd(s.exterior.coords))
            out.extend(rnd(h.coords) for h in s.interiors if Polygon(h).area > min_area)
    return out


# ---------- Water bodies (lakes, canal, creek) ----------
water_polys = []
for e in ways('water.json'):
    c = coords(e)
    if len(c) > 3 and c[0] == c[-1]:
        p = Polygon(c)
        if p.is_valid and p.area > 3e-7:
            water_polys.append(p)
water = unary_union(water_polys) if water_polys else Polygon()

# ---------- Roads ----------
def road_lines(name, classes):
    return [LineString(coords(e)) for e in load(name) if e['type'] == 'way' and 'geometry' in e and e.get('tags', {}).get('highway') in classes]

major = road_lines('major.json', {'motorway', 'trunk'}) + road_lines('ad_roads.json', {'motorway', 'trunk'})
primary = road_lines('roads.json', {'primary'}) + road_lines('ad_roads.json', {'primary'})
secondary = road_lines('roads.json', {'secondary'})
major_m, primary_m, secondary_m = (linemerge(x) for x in (major, primary, secondary))
as_list = lambda g: list(g.geoms) if hasattr(g, 'geoms') else [g]
runways = [LineString(coords(e)) for e in ways('runways.json')]

# ---------- Districts from the Dubai atlas (faint data texture) ----------
atlas = json.loads((ROOT / 'atlas' / 'dubai' / 'atlas.geojson').read_text())['features']
district_lines = []
for f in atlas:
    g = shape(f['geometry'])
    if g.geom_type in ('Polygon', 'MultiPolygon') and g.area > 2e-6:
        district_lines += [LineString(r) for r in rings(g)]


def atlas_ring(name):
    for f in atlas:
        if f['properties'].get('name') == name and f['geometry']['type'] in ('Polygon', 'MultiPolygon'):
            return rnd(Polygon(rings(shape(f['geometry']))[0]).simplify(0.00005).exterior.coords)
    raise KeyError(name)


# ---------- Story features ----------
def land_face_at(lon, lat, tol=0.00006):
    for p in (land_union.geoms if isinstance(land_union, MultiPolygon) else [land_union]):
        if p.contains(Point(lon, lat)):
            return [rnd(p.simplify(tol).exterior.coords)]
    raise ValueError(f'no land at {lon},{lat}')


def coast_rings_near(lon, lat, radius):
    """Island rings of the coastline near a point, for tracing a Palm."""
    area = Point(lon, lat).buffer(radius)
    polys = land_union.geoms if isinstance(land_union, MultiPolygon) else [land_union]
    return [rnd(p.simplify(0.00003).exterior.coords) for p in polys if area.contains(p) and p.area > 1e-8]


manual = json.loads((ROOT / 'atlas' / 'dubai' / 'manual.geojson').read_text())['features']
palm_springs = [rnd(f['geometry']['coordinates'][0]) for f in manual if f['properties']['name'] == 'Palm Springs'][0]

szr = [LineString(coords(e)) for e in load('major.json') if e['type'] == 'way' and 'geometry' in e
       and ('E 11' in e.get('tags', {}).get('ref', '') or 'E11' in e.get('tags', {}).get('ref', ''))]
szr_lines = lines_out(as_list(linemerge(szr)), 0.0001, 0.01)

dwc = [e for e in load('dwc.json') if 'geometry' in e or 'members' in e][0]
if dwc['type'] == 'way':
    airport = [rnd(LineString(coords(dwc)).simplify(0.0001).coords)]
else:
    outer = [LineString([(p['lon'], p['lat']) for p in m['geometry']]) for m in dwc['members'] if m.get('role') == 'outer' and 'geometry' in m]
    merged = linemerge(outer)
    airport = [rnd(g.simplify(0.0001).coords) for g in as_list(merged)]

feat = {
    'palmJumeirah': coast_rings_near(55.133, 25.118, 0.035),
    # Palm Jebel Ali joins the mainland polygon at its bridge, so trace the coastline inside a circle around it.
    'palmJebelAli': lines_out(as_list(land_union.boundary.intersection(Point(54.984, 25.012).buffer(0.036))), 0.00003, 0.002),
    'szr': szr_lines,
    'palmSprings': [palm_springs],
    'dso': [atlas_ring('Dubai Silicon Oasis')],
    'yas': land_face_at(54.605, 24.49),
    'saadiyat': land_face_at(54.435, 24.545),
    'airport': airport,
    'runways': lines_out(runways, 0.0001),
    'jafza': [atlas_ring('Jebel Ali North Free Zone')],
}

base = {}
for level, tol in (('fine', FINE), ('coarse', COARSE)):
    base[level] = {
        'land': polys_out(land_union, tol, 2e-7 if level == 'fine' else 4e-6),
        'water': polys_out(water, tol, 3e-7 if level == 'fine' else 3e-6) if not water.is_empty else [],
        'major': lines_out(as_list(major_m), tol, 0.0),
        'primary': lines_out(as_list(primary_m), tol, 0.002 if level == 'fine' else 0.01),
        'secondary': lines_out(as_list(secondary_m), tol, 0.003) if level == 'fine' else [],
        'districts': lines_out(district_lines, tol * 2) if level == 'fine' else [],
        'runways': lines_out(runways, tol),
    }

data = {'bbox': BBOX, 'base': base, 'feat': feat}
OUT.write_text(json.dumps(data, separators=(',', ':')))
count = lambda layer: sum(len(l) for l in layer)
for level in base:
    print(level, {k: (len(v), count(v)) for k, v in base[level].items()})
print({k: (len(v), count(v)) for k, v in feat.items()})
print(OUT, round(OUT.stat().st_size / 1e6, 2), 'MB')
