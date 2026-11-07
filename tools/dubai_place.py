#!/usr/bin/env python3
"""Look up a Dubai place in the atlas and print or save its outline for a map reel.

Usage: dubai_place.py <name> [--save outline.json]
Matches loosely, so "jvc", "jumeirah village circle" or "Al Furjan" all work. Saved outlines are lists of
[lon, lat] rings, ready for a `shapes` entry in MapReel or EarthReel props.
"""
import difflib
import json
import sys
from pathlib import Path

ATLAS = Path(__file__).resolve().parent.parent / 'atlas' / 'dubai' / 'atlas.geojson'
SHORT_NAMES = {'jvc': 'jumeirah village circle', 'jvt': 'jumeirah village triangle', 'jlt': 'jumeirah lakes towers',
               'jumeirah lake towers': 'jumeirah lakes towers', 'jbr': 'jumeirah beach residence',
               'difc': 'dubai international financial centre', 'dip': 'dubai investments park',
               'mbr': 'mohammed bin rashid city', 'mbr city': 'mohammed bin rashid city', 'dso': 'dubai silicon oasis',
               'jge': 'jumeirah golf estates', 'dsc': 'dubai sports city', 'tecom': 'barsha heights',
               'the sustainable city': 'dubai sustainable city', 'dlrc': 'dubai residence complex', 'world islands': 'the world islands'}


def rings(geometry):
    polygons = geometry['coordinates'] if geometry['type'] == 'MultiPolygon' else [geometry['coordinates']]
    return [polygon[0] for polygon in polygons] if geometry['type'] in ('Polygon', 'MultiPolygon') else []


def main():
    query = ' '.join(a for a in sys.argv[1:] if not a.startswith('--') and a != (sys.argv[sys.argv.index('--save') + 1] if '--save' in sys.argv else None))
    features = json.loads(ATLAS.read_text())['features']
    wanted = SHORT_NAMES.get(query.lower(), query.lower())
    names = {f['properties']['name'].lower(): f for f in features}
    for f in features:
        for alias in filter(None, [f['properties']['also'].lower()]):
            names.setdefault(alias, f)
    exact = names.get(wanted)
    contains = [n for n in names if wanted in n]
    close = difflib.get_close_matches(wanted, list(names), n=8, cutoff=0.55)
    candidates = [names[n] for n in dict.fromkeys(contains + close)]
    # Prefer names that start with the query, then the biggest area, so "town square" finds the whole community.
    candidates.sort(key=lambda f: (not f['properties']['name'].lower().removeprefix('the ').startswith(wanted),
                                   -f['properties']['area_km2']))
    matches = [exact] if exact else candidates[:8]
    if not matches:
        raise SystemExit(f'No match for "{query}" in the atlas')
    for f in matches:
        p = f['properties']
        print(f"{p['name']} | {p['kind']} | {p['area_km2']} km² | in {p['parent'] or '-'} | centre {p['lat']}, {p['lon']} | {p['osm']}")
    if '--save' in sys.argv:
        target = Path(sys.argv[sys.argv.index('--save') + 1])
        outline = rings(matches[0]['geometry'])
        target.write_text(json.dumps({'name': matches[0]['properties']['name'], 'lines': outline,
                                      'anchor': [matches[0]['properties']['lon'], matches[0]['properties']['lat']]}))
        print('saved', matches[0]['properties']['name'], 'with', len(outline), 'ring(s) ->', target)


if __name__ == '__main__':
    main()
