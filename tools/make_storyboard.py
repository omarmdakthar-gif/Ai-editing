#!/usr/bin/env python3
"""Turn a storyboard.json into one self-contained HTML page for review.

Usage: make_storyboard.py <storyboard.json> <output.html>
Each beat: time, frame (image path, relative to the json), spoken, caption, visual, sound, purpose.
"""
import base64
import html
import json
import sys
from pathlib import Path

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><style>
:root{{--bg:#f6f5f2;--ink:#191919;--muted:#66625c;--line:#dfdbd3;--card:#fff}}
@media (prefers-color-scheme:dark){{:root{{--bg:#141414;--ink:#f1efea;--muted:#a5a199;--line:#333;--card:#1e1e1e}}}}
*{{box-sizing:border-box}}body{{margin:0;padding:32px 16px;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Segoe UI,sans-serif}}
main{{max-width:980px;margin:auto}}h1{{font-size:30px;margin:0 0 4px}}.meta{{color:var(--muted);margin:0 0 28px}}
.beat{{display:grid;grid-template-columns:150px 1fr;gap:20px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin-bottom:14px}}
.beat img,.empty{{width:150px;aspect-ratio:9/16;object-fit:cover;border-radius:6px;background:var(--line)}}
.time{{font-weight:700;font-variant-numeric:tabular-nums}}.purpose{{color:var(--muted);margin-left:8px}}
dl{{display:grid;grid-template-columns:90px 1fr;gap:4px 12px;margin:10px 0 0}}dt{{color:var(--muted)}}dd{{margin:0}}
.notes{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin-top:22px}}
@media (max-width:560px){{.beat{{grid-template-columns:1fr}}.beat img,.empty{{width:100%;max-width:240px}}}}
</style></head><body><main><h1>{title}</h1><p class="meta">{meta}</p>{beats}{notes}</main></body></html>"""


def image_tag(root, name):
    path = root / name if name else None
    if not path or not path.exists():
        return '<div class="empty"></div>'
    data = base64.b64encode(path.read_bytes()).decode()
    return f'<img alt="" src="data:image/jpeg;base64,{data}">'


def main():
    source, output = Path(sys.argv[1]), Path(sys.argv[2])
    board = json.loads(source.read_text())
    rows = []
    for beat in board['beats']:
        details = ''.join(
            f'<dt>{label}</dt><dd>{html.escape(beat[key])}</dd>'
            for label, key in (('Spoken', 'spoken'), ('Caption', 'caption'), ('Visual', 'visual'), ('Sound', 'sound'))
            if beat.get(key)
        )
        rows.append(
            f'<section class="beat">{image_tag(source.parent, beat.get("frame"))}<div>'
            f'<span class="time">{html.escape(beat["time"])}</span>'
            f'<span class="purpose">{html.escape(beat.get("purpose", ""))}</span><dl>{details}</dl></div></section>'
        )
    notes = ''.join(f'<li>{html.escape(n)}</li>' for n in board.get('notes', []))
    page = PAGE.format(
        title=html.escape(board['title']),
        meta=html.escape(f"{board['style']} style · {board['length']} · goal: {board['goal']}"),
        beats=''.join(rows),
        notes=f'<div class="notes"><strong>To check</strong><ul>{notes}</ul></div>' if notes else '',
    )
    output.write_text(page)
    print(output)


if __name__ == '__main__':
    main()
