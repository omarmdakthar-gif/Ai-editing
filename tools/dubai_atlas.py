#!/usr/bin/env python3
"""Build the Dubai atlas: every named community in OpenStreetMap with boundary, centre, size and parent area.

Usage: dubai_atlas.py [output folder, default atlas/dubai] [--offline]
Writes atlas.geojson (shapes), atlas.csv (one row per place) and A-Z.md (readable index).
--offline rebuilds from the cached download. Outlines in manual.geojson (traced from the user's screenshots) win.
Data is (c) OpenStreetMap contributors under the ODbL. Boundaries are community-mapped, not official DLD plots.
"""
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from pyproj import Geod
from shapely.geometry import LineString, Point, mapping
from shapely.geometry import shape as shape_geometry
from shapely.ops import linemerge, polygonize, unary_union

SERVERS = ['https://overpass-api.de/api/interpreter', 'https://overpass.kumi.systems/api/interpreter']
DUBAI = 'area["ISO3166-2"="AE-DU"]->.d;'
PLACES = 'suburb|neighbourhood|quarter|village|town|city_block|island'
# Developer projects are often mapped as named land use rather than as places.
DEVELOPMENTS = 'residential|construction|commercial|retail|mixed_use'
MIN_DEVELOPMENT_KM2 = 0.2
MIN_ISLET_KM2 = 0.3
MERGE_GAP = 0.0006
QUERY = (f'[out:json][timeout:300];{DUBAI}('
         f'relation["boundary"="administrative"]["admin_level"~"^(7|8|9|10|11)$"](area.d);'
         f'relation["place"~"{PLACES}"](area.d);way["place"~"{PLACES}"](area.d);'
         f'way["boundary"="administrative"]["admin_level"~"^(9|10|11)$"](area.d);'
         f'node["place"~"{PLACES}"](area.d);'
         f'relation["place"~"islet|island"]["name"](area.d);way["place"~"islet|island"]["name"](area.d);'
         f'relation["landuse"~"{DEVELOPMENTS}"]["name"](area.d);way["landuse"~"{DEVELOPMENTS}"]["name"](area.d););out geom;')
GEOD = Geod(ellps='WGS84')
# The user wants English only, so places named only in Arabic script are left out.
ARABIC = re.compile('[\u0600-\u06FF]')


def fetch():
    for attempt in range(3):
        for server in SERVERS:
            request = urllib.request.Request(server, data=urllib.parse.urlencode({'data': QUERY}).encode(),
                                             headers={'User-Agent': 'reel-editor/1.0'})
            try:
                with urllib.request.urlopen(request, timeout=320) as response:
                    return json.load(response)['elements']
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
                print('retrying after', server, error, file=sys.stderr)
        time.sleep(10)
    raise SystemExit('No OpenStreetMap server responded')


def shape_of(element):
    if element['type'] == 'node':
        return Point(element['lon'], element['lat'])
    if element['type'] == 'way':
        points = [(p['lon'], p['lat']) for p in element.get('geometry', [])]
        if len(points) >= 4 and points[0] == points[-1]:
            return unary_union(list(polygonize([LineString(points)])))
        return None
    outers = [LineString([(p['lon'], p['lat']) for p in m['geometry']])
              for m in element.get('members', []) if m.get('role') in ('outer', '') and len(m.get('geometry', [])) > 1]
    inners = [LineString([(p['lon'], p['lat']) for p in m['geometry']])
              for m in element.get('members', []) if m.get('role') == 'inner' and len(m.get('geometry', [])) > 1]
    if not outers:
        return None
    shape = unary_union(list(polygonize(linemerge(outers))))
    if inners:
        shape = shape.difference(unary_union(list(polygonize(linemerge(inners)))))
    return shape if not shape.is_empty else None


def square_km(shape):
    if shape.geom_type not in ('Polygon', 'MultiPolygon'):
        return 0.0
    return abs(GEOD.geometry_area_perimeter(shape)[0]) / 1e6


def merge_parts(places):
    """Build a parent outline from parts named like "Maple, Dubai Hills Estate" when the parent has no boundary."""
    groups = {}
    for place in list(places.values()):
        if ', ' not in place['name'] or not place['area']:
            continue
        parent = place['name'].split(', ')[1].strip()
        groups.setdefault(parent, []).append(place)
    for parent, parts in groups.items():
        existing = places.get(parent.lower())
        if len(parts) < 2 or parent.lower() in ('dubai', 'uae') or (existing and existing['area']):
            continue
        # A fuller boundary may exist under a longer name, such as "Town Square Dubai".
        if any(key.startswith(parent.lower() + ' ') and place['area'] for key, place in places.items()):
            continue
        # Close the small gaps between neighbouring parts, then shrink back to the original edge.
        shape = unary_union([p['shape'] for p in parts]).buffer(MERGE_GAP).buffer(-MERGE_GAP)
        places[parent.lower()] = {'name': parent, 'also': '', 'kind': f'merged from {len(parts)} mapped parts (may be partial)',
                                  'level': '', 'osm': ';'.join(p['osm'] for p in parts), 'shape': shape, 'area': square_km(shape)}


def load_manual(places, path):
    """Outlines traced from the user's marked screenshots replace OpenStreetMap shapes of the same name."""
    if not path.exists():
        return
    for feature in json.loads(path.read_text())['features']:
        props = feature['properties']
        shape = shape_geometry(feature['geometry'])
        places[props['name'].lower()] = {'name': props['name'], 'also': props.get('also', ''),
                                         'kind': f"traced ({props.get('source', 'user screenshot')})", 'level': '',
                                         'osm': 'manual', 'shape': shape, 'area': square_km(shape)}


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 'atlas/dubai')
    out.mkdir(parents=True, exist_ok=True)
    cache = out / 'osm-raw.json'
    if '--offline' in sys.argv and cache.exists():
        elements = json.loads(cache.read_text())
    else:
        elements = fetch()
        cache.write_text(json.dumps(elements))
    places = {}
    for element in elements:
        tags = element.get('tags', {})
        name = tags.get('name:en') or tags.get('name')
        if not name or ARABIC.search(name):
            continue
        shape = shape_of(element)
        if shape is None or shape.is_empty:
            continue
        key = name.strip().lower()
        record = {
            'name': name.strip(), 'also': tags.get('alt_name:en') or '',
            'kind': tags.get('place') or f"admin {tags.get('admin_level', '')}".strip(),
            'level': tags.get('admin_level', ''), 'osm': f"{element['type']}/{element['id']}", 'shape': shape,
            'area': square_km(shape),
        }
        if 'landuse' in tags and 'place' not in tags and 'boundary' not in tags:
            if record['area'] < MIN_DEVELOPMENT_KM2:
                continue
            record['kind'] = f"development ({tags['landuse']})"
        if tags.get('place') == 'islet' and record['area'] < MIN_ISLET_KM2:
            continue
        # Keep the best version of each name: a boundary beats a point, a larger boundary beats a sliver.
        best = places.get(key)
        if best is None or (record['area'] > best['area']):
            places[key] = record

    merge_parts(places)
    load_manual(places, out / 'manual.geojson')

    areas = sorted((p for p in places.values() if p['area'] > 0), key=lambda p: p['area'])
    for place in places.values():
        centre = place['shape'].representative_point() if place['area'] else place['shape']
        place['lon'], place['lat'] = round(centre.x, 6), round(centre.y, 6)
        west, south, east, north = place['shape'].bounds
        place['bbox'] = [round(v, 6) for v in (west, south, east, north)]
        point = Point(place['lon'], place['lat'])
        parents = [a for a in areas if a is not place and a['area'] > place['area'] * 1.5 and a['area'] < 900
                   and a['shape'].contains(point)]
        place['parent'] = parents[0]['name'] if parents else ''

    ordered = sorted(places.values(), key=lambda p: p['name'].lower())
    features = [{'type': 'Feature', 'geometry': mapping(p['shape']),
                 'properties': {k: p[k] for k in ('name', 'also', 'kind', 'level', 'parent', 'osm', 'lon', 'lat', 'bbox')}
                 | {'area_km2': round(p['area'], 3)}} for p in ordered]
    (out / 'atlas.geojson').write_text(json.dumps({'type': 'FeatureCollection', 'features': features}))
    with open(out / 'atlas.csv', 'w', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(['name', 'also', 'kind', 'parent', 'area_km2', 'lon', 'lat', 'has_boundary', 'osm'])
        for p in ordered:
            writer.writerow([p['name'], p['also'], p['kind'], p['parent'], round(p['area'], 3),
                             p['lon'], p['lat'], 'yes' if p['area'] else 'point only', p['osm']])
    lines = ['# Dubai atlas A to Z', '',
             f'{len(ordered)} named places from OpenStreetMap ({sum(1 for p in ordered if p["area"])} with boundaries). '
             'Data (c) OpenStreetMap contributors, ODbL. Community-mapped, not official DLD boundaries.', '']
    letter = ''
    for p in ordered:
        first = p['name'][0].upper()
        if first != letter:
            letter = first
            lines += ['', f'## {letter}', '']
        size = f"{p['area']:.2f} km²" if p['area'] else 'point only'
        inside = f" · in {p['parent']}" if p['parent'] else ''
        lines.append(f"- **{p['name']}** · {size}{inside} · {p['lat']}, {p['lon']}")
    (out / 'A-Z.md').write_text('\n'.join(lines) + '\n')
    print(len(ordered), 'places,', sum(1 for p in ordered if p['area']), 'with boundaries ->', out)


if __name__ == '__main__':
    main()
