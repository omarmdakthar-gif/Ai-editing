#!/usr/bin/env python3
"""Draw lon/lat lines onto one Earth Studio frame, to check routes and outlines against the real imagery.

Usage: earth_overlay_check.py <render folder> <frame number> <lines.json> <out.jpg>
lines.json: {"name": [[lon, lat], ...], ...}. Uses the same camera maths as earthCamera.ts.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

R = 6371010
COLOURS = ['#FF3B6B', '#3BE8FF', '#FFD23B', '#7CFF5B', '#C77DFF', '#FFFFFF']


def rotation(x, y, z):
    x, y, z = map(math.radians, (x, y, z))
    rx = np.array([[1, 0, 0], [0, math.cos(x), -math.sin(x)], [0, math.sin(x), math.cos(x)]])
    ry = np.array([[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])
    rz = np.array([[math.cos(z), -math.sin(z), 0], [math.sin(z), math.cos(z), 0], [0, 0, 1]])
    return rx @ ry @ rz


def main():
    render, index, lines_path, out = Path(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
    tracking = next(render.glob('*.json'))
    data = json.loads(tracking.read_text())
    frame = data['cameraFrames'][index]
    image = Image.open(render / 'footage' / f'{tracking.stem}_{index:03d}.jpeg').convert('RGB')
    w, h = image.size
    axes = rotation(*[frame['rotation'][k] for k in 'xyz'])
    pos = np.array([frame['position'][k] for k in 'xyz'])
    focal = h / 2 / math.tan(math.radians(frame['fovVertical']) / 2)

    def project(lon, lat):
        a, b = math.radians(lon), math.radians(lat)
        d = np.array([R * math.cos(b) * math.cos(a), R * math.cos(b) * math.sin(a), R * math.sin(b)]) - pos
        x, y, z = axes.T @ d
        z = max(z, 1)
        return (w / 2 + x / z * focal, h / 2 + y / z * focal)

    draw = ImageDraw.Draw(image)
    for i, (name, line) in enumerate(json.loads(Path(lines_path).read_text()).items()):
        pts = [project(*p) for p in line]
        draw.line(pts, fill=COLOURS[i % len(COLOURS)], width=10)
        draw.text((40, 40 + i * 60), name, fill=COLOURS[i % len(COLOURS)], font_size=50)
    image.resize((w // 2, h // 2)).save(out, quality=88)
    print(out)


if __name__ == '__main__':
    main()
