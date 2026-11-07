"""Synthesise an original cinematic music bed for the reel, so there is no licence to check.

Usage: make_music.py <out.wav> <seconds>
Slow minor progression (Am, F, C, G) on soft detuned pads, a sub swell, and a gentle pulse that
builds into the corridor reveal (~47 s) and the launch section (~78 s).
"""
import sys

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
out, total = sys.argv[1], float(sys.argv[2])
n = int(SR * total)
t = np.arange(n) / SR
rng = np.random.default_rng(3)

BPM = 96
beat = 60 / BPM
bar = beat * 4
chords = [[57, 60, 64], [53, 57, 60], [48, 55, 60], [55, 59, 62]]  # Am F C G (MIDI)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)


def env(x0, x1, attack, release):
    e = np.zeros(n)
    i0, i1 = int(x0 * SR), min(n, int(x1 * SR))
    seg = np.arange(i1 - i0) / SR
    e[i0:i1] = np.minimum(1, seg / attack) * np.minimum(1, (x1 - x0 - seg) / release).clip(0)
    return e


# Intensity curve: calm verse, lift at the corridor, dip, lift into the launch, settle at the end.
pts = [(0, 0.55), (6, 0.7), (40, 0.75), (47, 1.0), (58, 0.8), (67, 0.75), (78, 1.0), (88.5, 1.05), (total, 0.7)]
intensity = np.interp(t, [p[0] for p in pts], [p[1] for p in pts])

pad = np.zeros(n)
k = 0
x = 0.0
while x < total:
    for m in chords[k % 4]:
        for det in (-0.08, 0.08):
            f = hz(m) * 2 ** (det / 12)
            ph = rng.uniform(0, 2 * np.pi)
            wave = np.sin(2 * np.pi * f * t + ph) + 0.35 * np.sin(4 * np.pi * f * t + ph) + 0.15 * np.sin(6 * np.pi * f * t)
            pad += wave * env(x, min(total, x + bar * 2 + 1.2), 1.6, 1.4) * 0.05
    bass = np.sin(2 * np.pi * hz(chords[k % 4][0] - 24) * t)
    pad += bass * env(x, min(total, x + bar * 2 + 0.6), 0.8, 1.0) * 0.12
    k += 1
    x += bar * 2
pad = sosfilt(butter(2, 2400, fs=SR, output='sos'), pad)

# Soft pulse: muted sub thump on every beat, airy hat on off-beats, both following the intensity.
pulse = np.zeros(n)
kick_len = int(0.25 * SR)
kt = np.arange(kick_len) / SR
kick = np.sin(2 * np.pi * (48 + 60 * np.exp(-kt * 30)) * kt) * np.exp(-kt * 14)
hat_len = int(0.06 * SR)
hat = sosfilt(butter(2, 7000, btype='high', fs=SR, output='sos'), rng.standard_normal(hat_len)) * np.exp(-np.arange(hat_len) / SR * 60)
b = 0
while b * beat < total:
    i = int(b * beat * SR)
    g = max(0, intensity[min(i, n - 1)] - 0.6) * 2.2
    if i + kick_len < n:
        pulse[i:i + kick_len] += kick * 0.5 * g
    j = int((b + 0.5) * beat * SR)
    if j + hat_len < n:
        pulse[j:j + hat_len] += hat * 0.06 * g
    b += 1

# Risers into the two lifts.
def riser(at, length):
    r = np.zeros(n)
    i0, i1 = int((at - length) * SR), int(at * SR)
    noise = rng.standard_normal(i1 - i0)
    ramp = np.linspace(0, 1, i1 - i0) ** 2
    r[i0:i1] = sosfilt(butter(2, 3000, btype='high', fs=SR, output='sos'), noise) * ramp * 0.05
    return r

mix = pad * intensity + pulse + riser(47.0, 3.0) + riser(78.0, 3.0)
fade = np.minimum(1, t / 1.5) * np.minimum(1, (total - t) / 2.0)
mix *= fade
mix /= np.max(np.abs(mix)) + 1e-9
stereo = np.stack([mix, np.roll(mix, int(0.012 * SR))], axis=1) * 0.8
sf.write(out, stereo.astype(np.float32), SR)
print(out, round(total, 1), 's')
