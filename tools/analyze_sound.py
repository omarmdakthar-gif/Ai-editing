#!/usr/bin/env python3
"""Measure sound design around cuts: music level under speech, whooshes and low impacts.

Usage: analyze_sound.py <video> <analysis dir holding report.json and transcript.json>
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import librosa
import numpy as np

SR = 22050
WHOOSH_RATIO, IMPACT_RATIO = 1.8, 1.8


def band_energy(spectrum, freqs, low, high):
    return spectrum[(freqs >= low) & (freqs < high)].mean(axis=0)


def main():
    video, folder = sys.argv[1], Path(sys.argv[2])
    report = json.loads((folder / 'report.json').read_text())
    transcript = json.loads((folder / 'transcript.json').read_text())
    with tempfile.TemporaryDirectory() as tmp:
        wav = str(Path(tmp) / 'a.wav')
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', video, '-ac', '1', '-ar', str(SR), wav])
        y, _ = librosa.load(wav, sr=SR)
    stft = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    freqs = librosa.fft_frequencies(sr=SR, n_fft=2048)
    times = librosa.frames_to_time(np.arange(stft.shape[1]), sr=SR, hop_length=512)
    high = band_energy(stft, freqs, 3000, 9000)
    low = band_energy(stft, freqs, 30, 120)
    rms = librosa.feature.rms(S=stft, frame_length=2048)[0]

    words = [w for s in transcript.get('segments', []) for w in s.get('words', [])]
    in_word = np.zeros_like(times, dtype=bool)
    for w in words:
        in_word |= (times >= w['start']) & (times <= w['end'])
    gaps = []
    for a, b in zip(words, words[1:]):
        if b['start'] - a['end'] >= 0.25:
            gaps.append((times >= a['end'] + 0.05) & (times <= b['start'] - 0.05))
    gap_mask = np.any(gaps, axis=0) if gaps else np.zeros_like(in_word)
    speech_db = 20 * np.log10(rms[in_word].mean() + 1e-9) if in_word.any() else None
    gap_db = 20 * np.log10(rms[gap_mask].mean() + 1e-9) if gap_mask.any() else None

    whoosh, impact = 0, 0
    for cut in report['cuts']:
        before = (times >= cut - 0.3) & (times < cut + 0.05)
        after = (times >= cut) & (times < cut + 0.25)
        base = (times >= cut - 1.0) & (times < cut - 0.4)
        if not base.any():
            continue
        whoosh += high[before].max() > WHOOSH_RATIO * (np.median(high[base]) + 1e-9)
        impact += low[after].max() > IMPACT_RATIO * (np.median(low[base]) + 1e-9)
    count = max(len(report['cuts']), 1)
    result = {
        'gap_below_speech_db': round(float(speech_db - gap_db), 1) if speech_db and gap_db else None,
        'gap_count': len(gaps),
        'cuts_with_rising_high_end_pct': round(100 * whoosh / count),
        'cuts_with_low_impact_pct': round(100 * impact / count),
    }
    (folder / 'sound.json').write_text(json.dumps(result, indent=1))
    print(folder.name, result)


if __name__ == '__main__':
    main()
