#!/usr/bin/env python3
"""Prepare an Earth Studio render for the EarthReel composition.

Usage: earth_import.py <render folder> <output name>
Writes tools/remotion/public/earth/<name>/map.mp4 and camera.json, keeping per-frame camera data and credits.
"""
import json
import subprocess
import sys
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent / 'remotion' / 'public' / 'earth'


def main():
    render, name = Path(sys.argv[1]), sys.argv[2]
    tracking = next(render.glob('*.json'))
    data = json.loads(tracking.read_text())
    stem = tracking.stem
    out = PUBLIC / name
    out.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-framerate', str(data['frameRate']),
                    '-start_number', '0', '-i', str(render / 'footage' / f'{stem}_%03d.jpeg'),
                    '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p',
                    str(out / 'map.mp4')], check=True)
    sources = render / 'ImagerySources.txt'
    camera = {
        'width': data['width'], 'height': data['height'], 'frameRate': data['frameRate'],
        'frames': [{'p': [f['position'][k] for k in 'xyz'], 'r': [f['rotation'][k] for k in 'xyz'], 'fov': f['fovVertical']}
                   for f in data['cameraFrames']],
        'sources': sources.read_text().strip() if sources.exists() else '',
    }
    (out / 'camera.json').write_text(json.dumps(camera))
    print(out, len(camera['frames']), 'frames |', camera['sources'])


if __name__ == '__main__':
    main()
