# Sanjay Ram reel skills

Two Claude Code skills, plus the scripts and templates they use.

| Skill | What it does |
|---|---|
| `reel-editor` | Turns your Tamil and English footage into finished reels: transcription, English captions, storyboard, edit, sound, 4K export, cover and post caption. Three styles: Spotlight, Editorial and Map Explainer. The map style is locked to the Palm Springs look. |
| `dubai-map-footage` | Gets the map part: 4K Google Earth fly-overs generated as Earth Studio projects, camera tracking, plot outlines, coastline and real road routes, checked against the imagery. Also makes covers with no watermark, from a stylised OpenStreetMap map. |

## Install
Unzip into your project folder, so that you get:
```
<project>/.claude/skills/reel-editor/
<project>/.claude/skills/dubai-map-footage/
<project>/tools/...                       (scripts)
<project>/tools/remotion/src/...          (video compositions)
<project>/atlas/dubai/...                 (Dubai A–Z places)
<project>/projects/palm-springs-trial/... (worked example, templates only)
```
Claude Code picks the skills up automatically from `.claude/skills/`.

## Also needed (not in this zip)
- ffmpeg, Python 3.11 with the packages in `tools/requirements.txt` (installed into `tools/venv`; see the comments in that file), and the `deep-filter` binary in `tools/bin/` (from the DeepFilterNet GitHub releases).
- Run `npm install` in `tools/` and in `tools/remotion` (the fonts are already listed in its `package.json`).
- A Google account with Earth Studio access, and Claude in Chrome connected.
- `tools/env.sh` sets the paths. Edit it if your folders differ.

Video, audio, Earth renders and other media are left out to keep the download small.
