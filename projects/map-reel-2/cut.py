"""Cut the raw take into the final talk track for map reel 2.

Picks the best take of each script line (TAKES, in source seconds), removes pauses inside them, then writes:
  work/edl.json                 kept source ranges and where each lands on the reel timeline
  tools/remotion/public/mr2/voice.wav    denoised voice, 48 kHz
  tools/remotion/public/mr2/speaker.mp4  tone-mapped head-and-shoulders crop for the small window, 30 fps
"""
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
RAW = HERE / 'raw' / 'raw.mov'
WORK = HERE / 'work'
PUBLIC = HERE.parent.parent / 'tools' / 'remotion' / 'public' / 'mr2'
PUBLIC.mkdir(parents=True, exist_ok=True)

TAKES = [
    ('hook-1', 120.10, 122.26),   # Nilathoda mattum Dubai-la oru veedu vangadheenga
    ('hook-2', 123.55, 124.45),   # indha video-va paakama
    ('hook-3', 108.55, 112.75),   # Yenna Dubai-la rendu government-backed developers ... kondu vara poraanga
    ('projects', 179.80, 209.50), # Nakheel, Aldar, homes, prices
    ('demand', 286.50, 313.58),   # tough task, price per sq ft, growth corridor, supply
    ('nakheel', 364.85, 373.45),  # Ok so talking about Nakheel ...
    ('aldar', 486.25, 498.55),    # Talking about Aldar ...
    ('phase', 522.75, 532.62),    # first phase ... like this
    ('cta', 539.95, 546.35),      # Invest nu comment panunga ...
    ('close', 575.75, 585.15),    # Dubai-la 2 government-backed developers ... don't miss
]
GAP = 0.12          # pause kept where one was removed
PAD = 0.10          # audio kept either side of speech
MIN_PAUSE = 0.28    # pauses longer than this are removed


def speech_ranges(a, b):
    log = subprocess.run(['ffmpeg', '-hide_banner', '-ss', str(a), '-to', str(b), '-i', str(WORK / 'voice48.wav'),
                          '-af', f'silencedetect=n=-33dB:d={MIN_PAUSE}', '-f', 'null', '-'], capture_output=True, text=True).stderr
    starts = [float(v) + a for v in re.findall(r'silence_start: ([\d.]+)', log)]
    ends = [float(v) + a for v in re.findall(r'silence_end: ([\d.]+)', log)]
    keep, cur = [], a
    for s, e in zip(starts, ends + [b] * (len(starts) - len(ends))):
        if s - cur > 0.05:
            keep.append([max(a, cur - PAD), min(b, s + PAD)])
        cur = e
    if b - cur > 0.05:
        keep.append([max(a, cur - PAD), b])
    merged = []
    for r in keep:
        if merged and r[0] <= merged[-1][1] + 0.02:
            merged[-1][1] = max(merged[-1][1], r[1])
        else:
            merged.append(r)
    return merged


edl, t = [], 0.0
for name, a, b in TAKES:
    for i, (s, e) in enumerate(speech_ranges(a, b)):
        if edl:
            t += GAP if i else 0.22   # a slightly longer beat between script lines
        edl.append({'take': name, 'src': [round(s, 3), round(e, 3)], 'out': [round(t, 3), round(t + e - s, 3)]})
        t += e - s
total = round(t + 0.6, 2)
(WORK / 'edl.json').write_text(json.dumps({'total': total, 'pieces': edl}, indent=1))
print(len(edl), 'pieces, reel length', total, 's')

# ---- Audio: trim each piece with 12 ms fades, place it at its reel time, mix, then denoise. ----
parts, labels = [], []
for i, p in enumerate(edl):
    s, e = p['src']
    d = e - s
    parts.append(f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={max(0, d - 0.012):.3f}:d=0.012,adelay={int(p['out'][0] * 1000)}:all=1[a{i}]")
    labels.append(f'[a{i}]')
graph = f"[0:a]asplit={len(edl)}" + ''.join(f'[s{i}]' for i in range(len(edl))) + ';' + ';'.join(x.replace('[0:a]', f'[s{i}]', 1) for i, x in enumerate(parts)) + f";{''.join(labels)}amix=inputs={len(labels)}:normalize=0,apad=whole_dur={total}[out]"
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(WORK / 'voice48.wav'), '-filter_complex', graph, '-map', '[out]', '-ar', '48000', '-ac', '1',
                str(WORK / 'voice_cut.wav')], check=True)
subprocess.run(['deep-filter', '-o', str(WORK / 'df'), str(WORK / 'voice_cut.wav')], check=True, capture_output=True)
(WORK / 'df' / 'voice_cut.wav').replace(PUBLIC / 'voice.wav')

# ---- Video: same pieces, tone-mapped from HLG HDR to SDR, cropped to head and shoulders, 30 fps. ----
TONE = 'zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p'
CROP = 'crop=1300:1196:40:1680,scale=500:460:flags=lanczos,setsar=1'
pieces_dir = WORK / 'pieces'
pieces_dir.mkdir(exist_ok=True)
lines = []
for i, p in enumerate(edl):
    s, e = p['src']
    # Hold the last frame through the gap that follows, so the picture stays in sync with the audio timeline.
    nxt = edl[i + 1]['out'][0] if i + 1 < len(edl) else total
    hold = max(0.0, nxt - p['out'][1])
    out = pieces_dir / f'p{i:03d}.mp4'
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{s:.3f}', '-t', f'{e - s:.3f}', '-i', str(RAW), '-an',
                    '-vf', f'fps=30,{CROP},{TONE},tpad=stop_mode=clone:stop_duration={hold:.3f}',
                    '-c:v', 'libx264', '-crf', '15', '-preset', 'medium', '-pix_fmt', 'yuv420p', str(out)], check=True)
    lines.append(f"file '{out}'")
(pieces_dir / 'list.txt').write_text('\n'.join(lines))
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(pieces_dir / 'list.txt'), '-c', 'copy', str(PUBLIC / 'speaker.mp4')], check=True)
print('wrote voice.wav and speaker.mp4')
