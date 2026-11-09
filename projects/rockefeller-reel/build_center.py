"""Centre-layout version of the Rockefeller reel: edit_center.json from the re-timed edit.json.

The speaker stays full-size in the middle (a cut-out over the scenes) instead of shrinking to the corner box.
Graphics move above the head; the speaker steps aside only for the tower reveal.
Run after build_edit.py and retime.py:  python build_center.py
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
edit = json.loads((HERE / 'edit.json').read_text())

edit.pop('speaker', None)
reveal = next(s for s in edit['scenes'] if s['kind'] == 'image' and s.get('title'))
edit['center'] = {'person': 'rk/person_full.webm', 'scale': 0.86, 'hide': [[reveal['start'], reveal['end']]]}
# Foreground of these scenes moves above the head: [scale, translateY px], origin top centre.
edit['fit'] = {'wallet': [0.62, -250], 'profit': [0.62, -170], 'bank': [0.7, -230], 'video': [1.2, -480]}
for s in edit['scenes']:
    if s['kind'] == 'world':
        s['cy'] = 0.30
for c in edit['cards']:
    if 'y' in c:
        c['y'] = 300

(HERE / 'edit_center.json').write_text(json.dumps(edit))
print('edit_center.json: person steps aside', edit['center']['hide'])
