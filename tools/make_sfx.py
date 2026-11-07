#!/usr/bin/env python3
"""Generate the reel sound effects from scratch, so there is no licence to check.

Usage: make_sfx.py <output dir>
"""
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
rng = np.random.default_rng(7)


def seconds(duration):
    return np.linspace(0, duration, int(SR * duration), endpoint=False)


def sweep_noise(duration, start_hz, end_hz):
    """White noise through a low-pass filter whose cutoff glides, updated in short blocks."""
    noise = rng.standard_normal(int(SR * duration))
    output = np.zeros_like(noise)
    blocks = np.array_split(np.arange(len(noise)), 80)
    cutoffs = np.geomspace(start_hz, end_hz, len(blocks))
    for block, cutoff in zip(blocks, cutoffs):
        output[block] = sosfilt(butter(2, cutoff, fs=SR, output='sos'), noise[block])
    return output


def fade(signal, attack, release):
    envelope = np.ones_like(signal)
    a, r = int(SR * attack), int(SR * release)
    envelope[:a] = np.linspace(0, 1, a) ** 2
    envelope[-r:] = np.linspace(1, 0, r) ** 2
    return signal * envelope


def normalise(signal, peak=0.8):
    return signal / (np.abs(signal).max() + 1e-9) * peak


def whoosh(duration=0.45):
    rise = sweep_noise(duration, 300, 7000)
    return fade(rise, duration * 0.7, duration * 0.3)


def whoosh_soft(duration=0.7):
    return fade(sweep_noise(duration, 200, 2500), duration * 0.55, duration * 0.45)


def impact(duration=0.9):
    t = seconds(duration)
    body = np.sin(2 * np.pi * (45 * t + 40 * (1 - np.exp(-t * 30)) / 30)) * np.exp(-t * 5)
    click = sweep_noise(duration, 3000, 300) * np.exp(-t * 60) * 0.35
    return body + click


def riser(duration=2.5):
    t = seconds(duration)
    tone = sum(np.sin(2 * np.pi * np.cumsum(np.geomspace(f, f * 4, len(t))) / SR) for f in (110, 165, 220))
    air = sweep_noise(duration, 400, 9000)
    return fade(0.25 * tone + 0.75 * air, duration * 0.9, 0.05)


def pop(duration=0.12):
    t = seconds(duration)
    return np.sin(2 * np.pi * (900 - 2500 * t) * t) * np.exp(-t * 45)


def tick(duration=0.05):
    t = seconds(duration)
    return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 180)


def shimmer(duration=1.2):
    t = seconds(duration)
    notes = (1320, 1760, 2217, 2637)
    return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (3 + i)) for i, f in enumerate(notes))


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    effects = {'whoosh': whoosh, 'whoosh_soft': whoosh_soft, 'impact': impact, 'riser': riser,
               'pop': pop, 'tick': tick, 'shimmer': shimmer}
    for name, make in effects.items():
        sf.write(out / f'{name}.wav', normalise(make()), SR, subtype='PCM_24')
    print(sorted(p.name for p in out.glob('*.wav')))


if __name__ == '__main__':
    main()
