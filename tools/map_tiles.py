#!/usr/bin/env python3
"""Stitch satellite tiles into one image for a map reel.

Usage: map_tiles.py <west> <south> <east> <north> <zoom> <output prefix> [tile url template]
Writes <prefix>.jpg and <prefix>.json holding the exact bounds of the stitched image.
The default source is the 2016 Sentinel-2 cloudless layer, CC BY 4.0, which allows commercial use.
"""
import io
import json
import math
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

DEFAULT_URL = 'https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/g/{z}/{y}/{x}.jpg'
ATTRIBUTION = 'Sentinel-2 cloudless by EOX IT Services GmbH (Contains modified Copernicus Sentinel data 2016 & 2017)'
TILE = 256
PAUSE_SECONDS = 0.05


def tile_x(lon, zoom):
    return (lon + 180) / 360 * 2 ** zoom


def tile_y(lat, zoom):
    rad = math.radians(lat)
    return (1 - math.log(math.tan(rad) + 1 / math.cos(rad)) / math.pi) / 2 * 2 ** zoom


def lon_of(x, zoom):
    return x / 2 ** zoom * 360 - 180


def lat_of(y, zoom):
    return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / 2 ** zoom))))


def main():
    west, south, east, north = map(float, sys.argv[1:5])
    zoom, prefix = int(sys.argv[5]), Path(sys.argv[6])
    url = sys.argv[7] if len(sys.argv) > 7 else DEFAULT_URL
    x0, x1 = int(tile_x(west, zoom)), int(tile_x(east, zoom))
    y0, y1 = int(tile_y(north, zoom)), int(tile_y(south, zoom))
    canvas = Image.new('RGB', ((x1 - x0 + 1) * TILE, (y1 - y0 + 1) * TILE))
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            request = urllib.request.Request(url.format(z=zoom, x=x, y=y), headers={'User-Agent': 'reel-editor/1.0'})
            with urllib.request.urlopen(request, timeout=30) as response:
                canvas.paste(Image.open(io.BytesIO(response.read())), ((x - x0) * TILE, (y - y0) * TILE))
            time.sleep(PAUSE_SECONDS)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(prefix.with_suffix('.jpg'), quality=90)
    bounds = {'image': prefix.with_suffix('.jpg').name, 'width': canvas.width, 'height': canvas.height,
              'west': lon_of(x0, zoom), 'east': lon_of(x1 + 1, zoom),
              'north': lat_of(y0, zoom), 'south': lat_of(y1 + 1, zoom), 'attribution': ATTRIBUTION}
    prefix.with_suffix('.json').write_text(json.dumps(bounds, indent=1))
    print(prefix, canvas.size)


if __name__ == '__main__':
    main()
