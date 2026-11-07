#!/usr/bin/env python3
"""Measure one reference reel: cuts, motion, palette, speech, loudness, tempo, sound hits, frame sheets.

Usage: analyze_reel.py <video> <output dir> [--language ta]
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import librosa
import numpy as np

SCENE_THRESHOLD = 0.25
SHEET_COLUMNS, SHEET_ROWS = 6, 3


def run(*args):
    return subprocess.run(args, capture_output=True, text=True, errors='replace')


def detect_cuts(video):
    log = run('ffmpeg', '-hide_banner', '-i', video, '-vf',
              f"select='gt(scene,{SCENE_THRESHOLD})',showinfo", '-an', '-f', 'null', '-').stderr
    return [round(float(t), 2) for t in re.findall(r'pts_time:([\d.]+)', log)]


def frame_stats(video, out):
    """Per-frame brightness, saturation and motion, sampled at every frame."""
    log = run('ffmpeg', '-hide_banner', '-i', video, '-vf',
              'signalstats,metadata=print:file=-', '-an', '-f', 'null', '-').stdout
    luma = [float(v) for v in re.findall(r'lavfi\.signalstats\.YAVG=([\d.]+)', log)]
    sat = [float(v) for v in re.findall(r'lavfi\.signalstats\.SATAVG=([\d.]+)', log)]
    diff = [float(v) for v in re.findall(r'lavfi\.signalstats\.YDIF=([\d.]+)', log)]
    return {
        'frames_measured': len(luma),
        'luma_mean': round(float(np.mean(luma)), 1) if luma else None,
        'saturation_mean': round(float(np.mean(sat)), 1) if sat else None,
        'motion_mean': round(float(np.mean(diff)), 2) if diff else None,
    }


def palette(video, out):
    """Dominant colours from an ffmpeg palette of the whole reel."""
    png = out / 'palette.png'
    run('ffmpeg', '-hide_banner', '-y', '-i', video, '-vf',
        'fps=1,scale=160:-1,palettegen=max_colors=8:stats_mode=full', str(png))
    raw = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(png), '-f', 'rawvideo',
                          '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    colours = {raw[i:i + 3].hex().upper() for i in range(0, len(raw), 3)}
    return sorted(colours)


def contact_sheets(video, out):
    every = f'tile={SHEET_COLUMNS}x{SHEET_ROWS}'
    label = "drawtext=text='%{pts\\:hms}':x=8:y=8:fontsize=26:fontcolor=yellow:box=1:boxcolor=black@0.7"
    # Hook: 3 frames a second over the first 6 seconds. Body: one frame every 2 seconds.
    run('ffmpeg', '-hide_banner', '-y', '-t', '6', '-i', video, '-vf',
        f'fps=3,scale=300:-2,{label},{every}', str(out / 'hook_%02d.jpg'))
    run('ffmpeg', '-hide_banner', '-y', '-i', video, '-vf',
        f'fps=1/2,scale=300:-2,{label},{every}', str(out / 'body_%02d.jpg'))


def audio_stats(video, out, cuts):
    wav = out / 'audio.wav'
    run('ffmpeg', '-hide_banner', '-y', '-i', video, '-ac', '1', '-ar', '22050', str(wav))
    y, sr = librosa.load(wav, sr=22050, mono=True)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')
    harmonic, percussive = librosa.effects.hpss(y)
    onset_env = librosa.onset.onset_strength(y=percussive, sr=sr)
    threshold = np.percentile(onset_env, 97)
    hits = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units='time')
    strong = [round(float(t), 2) for t in hits
              if onset_env[librosa.time_to_frames(t, sr=sr)] >= threshold]
    near_beat = sum(any(abs(c - b) <= 0.08 for b in beats) for c in cuts)
    near_hit = sum(any(abs(c - h) <= 0.1 for h in strong) for c in cuts)
    rms = librosa.feature.rms(y=y)[0]
    quiet = float(np.percentile(rms, 10))
    loud = run('ffmpeg', '-hide_banner', '-i', str(wav), '-af', 'ebur128=framelog=quiet',
               '-f', 'null', '-').stderr
    lufs = re.findall(r'I:\s+(-?[\d.]+) LUFS', loud)
    wav.unlink()
    return {
        'tempo_bpm': round(float(np.atleast_1d(tempo)[0]), 1),
        'integrated_lufs': float(lufs[-1]) if lufs else None,
        'noise_floor_rms': round(quiet, 5),
        'strong_hits': strong,
        'cuts_on_beat': near_beat,
        'cuts_on_sound_hit': near_hit,
    }


def transcribe(video, out, language):
    command = ['mlx_whisper', video, '--model', 'mlx-community/whisper-large-v3-turbo',
               '--word-timestamps', 'True', '--output-format', 'json', '--output-dir', str(out),
               '--output-name', 'transcript']
    if language:
        command += ['--language', language]
    run(*command)
    path = out / 'transcript.json'
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    words = [w for s in data.get('segments', []) for w in s.get('words', [])]
    speech = sum(w['end'] - w['start'] for w in words)
    return {'language': data.get('language'), 'word_count': len(words),
            'words_per_minute_of_speech': round(len(words) / speech * 60) if speech else None}


def main():
    video, out = sys.argv[1], Path(sys.argv[2])
    language = sys.argv[sys.argv.index('--language') + 1] if '--language' in sys.argv else None
    out.mkdir(parents=True, exist_ok=True)
    duration = float(run('ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                         '-of', 'csv=p=0', video).stdout.strip())
    cuts = detect_cuts(video)
    report = {
        'duration': round(duration, 2),
        'cut_count': len(cuts),
        'average_shot_seconds': round(duration / (len(cuts) + 1), 2),
        'first_cut': cuts[0] if cuts else None,
        'cuts': cuts,
        'visual': frame_stats(video, out),
        'palette': palette(video, out),
        'audio': audio_stats(video, out, cuts),
        'speech': transcribe(video, out, language),
    }
    contact_sheets(video, out)
    (out / 'report.json').write_text(json.dumps(report, indent=1))
    print(video, report['cut_count'], 'cuts', report['audio']['tempo_bpm'], 'bpm',
          report['speech'].get('language'))


if __name__ == '__main__':
    main()
