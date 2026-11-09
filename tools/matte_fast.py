#!/usr/bin/env python3
"""Faster person cut-out for long clips: the mask is computed at reduced size, upscaled and applied to full-res frames.

Usage: matte_fast.py <input video> <output.webm> [--start S --duration D --mask-width 432]
Writes VP9 with alpha (yuva420p), which Remotion plays with <OffthreadVideo transparent>.
Masks are blended across frames to reduce edge flicker. Run several in parallel on time ranges for long clips.
"""
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter
from rembg import new_session, remove

MODEL = 'u2net_human_seg'
TEMPORAL_BLEND = 0.55


def option(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    source, output = sys.argv[1], sys.argv[2]
    start, duration = option('--start', '0'), option('--duration', None)
    mask_w = int(option('--mask-width', '432'))
    probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate',
                            '-of', 'csv=p=0', source], capture_output=True, text=True).stdout.strip().split(',')
    width, height, rate = int(probe[0]), int(probe[1]), probe[2]
    mask_h = round(height * mask_w / width)
    session = new_session(MODEL)
    decode = ['ffmpeg', '-loglevel', 'error', '-ss', start, *(['-t', duration] if duration else []), '-i', source,
              '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    reader = subprocess.Popen(decode, stdout=subprocess.PIPE)
    writer = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{width}x{height}',
                               '-r', rate, '-i', '-', '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-crf', '24', '-b:v', '0',
                               '-row-mt', '1', '-deadline', 'good', '-cpu-used', '4', output], stdin=subprocess.PIPE)
    frame_bytes = width * height * 3
    previous = None
    count = 0
    while True:
        raw = reader.stdout.read(frame_bytes)
        if len(raw) < frame_bytes:
            break
        frame = Image.frombuffer('RGB', (width, height), raw)
        small = frame.resize((mask_w, mask_h), Image.BILINEAR)
        mask = np.asarray(remove(small, session=session, only_mask=True), dtype=np.float32) / 255.0
        if previous is not None:
            mask = TEMPORAL_BLEND * mask + (1 - TEMPORAL_BLEND) * previous
        previous = mask
        alpha = Image.fromarray((mask * 255).astype(np.uint8)).resize((width, height), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1.2))
        rgba = np.dstack([np.asarray(frame), np.asarray(alpha)])
        writer.stdin.write(rgba.tobytes())
        count += 1
    writer.stdin.close()
    writer.wait()
    reader.wait()
    print(output, count, 'frames')


if __name__ == '__main__':
    main()
