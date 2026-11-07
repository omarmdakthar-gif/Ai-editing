#!/usr/bin/env python3
"""Fetch a road from OpenStreetMap as lists of [lon, lat] points.

Usage: map_roads.py <name or road number regex> <west> <south> <east> <north> <output.json> [highway filter]
Pass a raw tag filter as the first argument for anything else, for example '["natural"="coastline"]'.
Matches the local name, the English name and the road number, because Dubai roads are often named in Arabic.
Data is (c) OpenStreetMap contributors under the ODbL, so credit it on screen.
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SERVERS = ['https://overpass-api.de/api/interpreter', 'https://overpass.kumi.systems/api/interpreter']
ATTEMPTS = 3
RETRY_SECONDS = 5


def fetch(query):
    for attempt in range(ATTEMPTS):
        for server in SERVERS:
            request = urllib.request.Request(server, data=urllib.parse.urlencode({'data': query}).encode(),
                                             headers={'User-Agent': 'reel-editor/1.0'})
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    return json.load(response)['elements']
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
                print('retrying after', server, error, file=sys.stderr)
        time.sleep(RETRY_SECONDS)
    raise SystemExit('No OpenStreetMap server responded')


def main():
    name, west, south, east, north, output = sys.argv[1:7]
    road = sys.argv[7] if len(sys.argv) > 7 else 'motorway|trunk|primary'
    box = f'({south},{west},{north},{east})'
    if name.startswith('['):
        clauses = f'way{name}{box};'
    else:
        clauses = ''.join(f'way["{key}"~"{name}",i]["highway"~"^({road})$"]{box};' for key in ('name', 'name:en', 'ref'))
    lines = [[[p['lon'], p['lat']] for p in way['geometry']] for way in fetch(f'[out:json][timeout:40];({clauses});out geom;')]
    with open(output, 'w') as handle:
        json.dump(lines, handle)
    print(len(lines), 'lines', sum(map(len, lines)), 'points')


if __name__ == '__main__':
    main()
