#!/usr/bin/env python3
"""Cut the person out of a video so text can sit behind them.

Usage: matte.py <input video> <output person.mov> [--start 0 --duration 5]
Writes ProRes 4444 with alpha. Masks are blended across frames to reduce edge flicker.
"""
import subprocess
import sys

import numpy as np
from PIL import Image
from rembg import new_session, remove

MODEL = 'u2net_human_seg'
TEMPORAL_BLEND = 0.6


def option(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    source, output = sys.argv[1], sys.argv[2]
    start, duration = option('--start', '0'), option('--duration', None)
    probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                            'stream=width,height,r_frame_rate', '-of', 'csv=p=0', source],
                           capture_output=True, text=True).stdout.strip().split(',')
    width, height, rate = int(probe[0]), int(probe[1]), probe[2]
    session = new_session(MODEL)

    decode = ['ffmpeg', '-loglevel', 'error', '-ss', start]
    if duration:
        decode += ['-t', duration]
    decode += ['-i', source, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    reader = subprocess.Popen(decode, stdout=subprocess.PIPE)
    writer = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba',
                               '-s', f'{width}x{height}', '-r', rate, '-i', '-', '-c:v', 'prores_ks',
                               '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', output], stdin=subprocess.PIPE)
    previous = None
    frames = 0
    frame_bytes = width * height * 3
    while True:
        raw = reader.stdout.read(frame_bytes)
        if len(raw) < frame_bytes:
            break
        rgb = np.frombuffer(raw, np.uint8).reshape(height, width, 3)
        mask = np.array(remove(Image.fromarray(rgb), session=session, only_mask=True), dtype=np.float32)
        if previous is not None:
            mask = TEMPORAL_BLEND * mask + (1 - TEMPORAL_BLEND) * previous
        previous = mask
        writer.stdin.write(np.dstack([rgb, mask.astype(np.uint8)]).tobytes())
        frames += 1
    writer.stdin.close()
    writer.wait()
    print(f'{frames} frames -> {output}')


if __name__ == '__main__':
    main()
