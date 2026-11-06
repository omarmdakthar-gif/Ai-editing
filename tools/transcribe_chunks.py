"""Transcribe a clip in pause-split chunks, for when whole-file Whisper loops on one word.

Usage: python tools/transcribe_chunks.py <audio.wav> <out.json> [--language ta] [--max 12]
Splits at silences (ffmpeg silencedetect), transcribes each chunk separately,
and writes one JSON with segments and words on the original clip's timeline.
"""
import argparse, json, re, subprocess, tempfile, os

import mlx_whisper

MODEL = os.environ.get("WHISPER_MODEL", "mlx-community/whisper-large-v3-turbo")


def silences(path, noise="-35dB", dur=0.35):
    out = subprocess.run(["ffmpeg", "-i", path, "-af", f"silencedetect=n={noise}:d={dur}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    return list(zip(starts, ends))


def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True).stdout)


def cut_points(path, max_len):
    total = duration(path)
    mids = [(s + e) / 2 for s, e in silences(path)]
    points, last = [0.0], 0.0
    for i, m in enumerate(mids):
        nxt = mids[i + 1] if i + 1 < len(mids) else total
        if nxt - last > max_len and m - last > 1.0:
            points.append(m)
            last = m
    points.append(total)
    return points


def looped(text):
    words = text.split()
    return len(words) > 8 and len(set(words)) < len(words) / 4


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("out")
    ap.add_argument("--language", default="ta")
    ap.add_argument("--max", type=float, default=12)
    a = ap.parse_args()

    pts = cut_points(a.audio, a.max)
    segments = []
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(len(pts) - 1):
            s, e = pts[i], pts[i + 1]
            chunk = os.path.join(tmp, f"c{i}.wav")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(s), "-to", str(e), "-i", a.audio, chunk], check=True)
            r = mlx_whisper.transcribe(chunk, path_or_hf_repo=MODEL, language=a.language, word_timestamps=True,
                                       condition_on_previous_text=False)
            for seg in r["segments"]:
                if looped(seg["text"]):
                    seg = dict(seg, text="[unclear]", words=[])
                seg["start"] += s
                seg["end"] += s
                for w in seg.get("words", []):
                    w["start"] += s
                    w["end"] += s
                segments.append(seg)
    json.dump({"segments": segments, "chunks": pts}, open(a.out, "w"), ensure_ascii=False, indent=1)
    for seg in segments:
        print(f"{seg['start']:6.2f}-{seg['end']:6.2f} {seg['text'].strip()}")


if __name__ == "__main__":
    main()
