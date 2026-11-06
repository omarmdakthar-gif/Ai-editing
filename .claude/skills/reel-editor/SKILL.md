---
name: reel-editor
description: Plan, storyboard, edit and export short-form real estate reels for a Dubai agent who speaks Tamil and English, in three studied styles (Spotlight, Editorial and Map Explainer). Use this whenever the user shares raw footage, asks to edit, cut or caption a reel, Instagram video, TikTok or short, wants a hook, storyboard, b-roll, map animation, location or project comparison, sound effects or English captions for Tamil speech, or adds new reference reels to study, even if they never say "skill" or "reel-editor".
---

# Reel editor

Turns raw footage into a finished reel that holds attention and brings leads. The goal is enquiries, so judge every choice by whether it keeps the right viewer watching and gets them to reach out, not by views alone.

Everything runs from the project folder `/Users/maccy/Ai Editing`. Run `source tools/env.sh` before any tool.

## Standing rules

- **On-screen captions are always fully in English.** The user speaks mostly Tamil, with some English. Translate the meaning naturally rather than word for word, and keep Dubai terms, prices and numbers exact.
- **Storyboard first.** Nothing is rendered for export until the user approves the storyboard, because re-editing costs far more than changing a plan.
- **4K output.** Render finished reels with `--scale=2` for 2160×3840, and use source imagery sharp enough to justify it. Soft or upscaled-looking maps get rejected.
- **Folders.** Reference reels go in `references/`, working files in `projects/<reel-name>/`, finished videos in `export/`.
- **Real sources only.** Never recreate, alter or invent a tweet, headline, statistic or document. If a claim can't be verified, flag it in the storyboard instead of showing it.
- **Dubai advertising.** A reel promoting a property generally needs a Trakheesi permit shown on the ad, and off-plan listings may need more. Ask for the permit number and put it on the end card. If it's missing, flag it before export.

## Workflow

### 1. Take in the footage
Copy raw clips to `projects/<reel-name>/raw/` and measure them with `ffprobe`. Pull a frame sheet to see what was shot. Work out what the reel is: a talking-head opinion, a property tour, a deal breakdown or an explainer.

### 2. Transcribe and translate
```bash
mlx_whisper <clip> --model mlx-community/whisper-large-v3-turbo --language ta --word-timestamps True --output-format json --output-dir projects/<reel-name>/work
```
Always pass `--language ta`. On auto-detect, Whisper dropped Tamil speech entirely in testing, and its built-in translate task returned nothing, so translate the transcript yourself. Forced Tamil still handled English sentences correctly. Whisper can invent repeated phrases over music-only sections, so discard any words where nobody is speaking. If a whole clip comes back as one word repeated (it happened on 2 of 5 iPhone clips), transcribe it in overlapping 6-second windows with `condition_on_previous_text=False`, or run `python tools/transcribe_chunks.py <wav> <out.json>`. Keep the turbo model: full large-v3 did worse on this speaker's mixed Tamil and English, because it switched to Tamil script and translated the English. Save the translation beside the transcript and keep the Tamil, so the user can check meaning.

### Before filming
When the user has a topic but no footage yet, read [references/formats-and-shots.md](references/formats-and-shots.md). Match the topic to a format, then send them that format's shot list.

### 3. Choose the style
Read the reference for the chosen style. Recommend one and say why in a line.
- **Spotlight** ([references/style-spotlight.md](references/style-spotlight.md)): the agent on camera or the property itself. Default for authority, deals, listings and tours.
- **Editorial** ([references/style-editorial.md](references/style-editorial.md)): idea-led explainers with cutaways, diagrams and colour cards. Best for market education, stories and "why" reels.
- **Map Explainer** ([references/style-map.md](references/style-map.md)): Google Earth 4K fly-overs with glowing plots, real road routes, glass number cards, a sticker cut-out of the speaker and borderless gold-highlight captions. Best for location, what's nearby, and comparing projects. It only needs a simple selfie recording. **The house style is locked:** start from `projects/palm-springs-trial/build_edit.py` and the `ExplainerReel` composition, and change only the content. Get the map footage with the `dubai-map-footage` skill.

### Cover (every reel)
Use the `Cover` composition with a stylised OpenStreetMap background (`vector` props, template `projects/palm-springs-trial/cover_vector.json`). It has no satellite imagery, so there's no Google watermark. Show the user frame options for the face, cut out the chosen 4K frame with rembg, clean any background leftovers by hand, and put the speaker on the right so the clip's cut edge is off-screen. Render with `--scale=2`. Write the caption, hashtags and posting tips to `projects/<reel>/post.md`.

### 4. Build the retention plan
Read [references/retention.md](references/retention.md). Pick the hook, map the pattern interrupts, re-hooks and call to action against the real transcript. Cut the weakest lines rather than speeding everything up.

### 5. Research b-roll for any claim
For each fact, stat or news reference, find the original source. Use Claude in Chrome if it's connected; otherwise search the web and capture public pages:
```bash
tools/capture.sh <output.png> <url> [width,height]
```
For tweets, use `https://platform.twitter.com/embed/Tweet.html?id=<tweet id>` at size `540,400`. News pages can show ad overlays, so crop to the headline, and check the image by eye. Keep the source name visible and hold it only long enough to read. Save the source URL in the storyboard.

### 6. Storyboard, then stop
Write `projects/<reel-name>/storyboard.json`, with a real frame for every beat, and build the page:
```json
{"title": "...", "style": "Spotlight", "length": "45s", "goal": "DMs for off-plan advice",
 "beats": [{"time": "0:00-0:03", "frame": "work/beat1.jpg", "purpose": "Hook",
   "spoken": "Tamil line", "caption": "English caption", "visual": "...", "sound": "..."}],
 "notes": ["Anything the user must confirm, such as a fact or permit number"]}
```
```bash
python tools/make_storyboard.py projects/<reel-name>/storyboard.json projects/<reel-name>/storyboard.html
```
Show the page and ask for changes. Do not start the final render until the user approves. Apply any changes and show it again if they were substantial.

### 7. Edit
1. **Clean audio:** run `deep-filter` on 48kHz WAV if there's background noise.
2. **Cut:** use `auto-editor` for dead air, then cut by hand from the word timings. A cut that lands mid-thought feels wrong however tight it is.
3. **Cut-out for depth text:** `python tools/matte.py <clip> <person.mov> --start <s> --duration <s>`. It takes about a second per frame, so use it only on the moments that need it.
4. **Assemble:** copy media to `tools/remotion/public/`, write `projects/<reel-name>/edit.json`, then render. The `ReelProps` type in `tools/remotion/src/kit/styles.ts` lists every field. Use HyperFrames (`tools/hyperframes`) for one-off motion graphics, such as a price breakdown chart, and bring the result in as footage.
```bash
cd tools/remotion && npx remotion render src/index.ts Reel ../../projects/<reel-name>/work/draft.mp4 --props=../../projects/<reel-name>/edit.json
```
5. **Sound:** effects are in `public/sfx/` (`whoosh`, `whoosh_soft`, `impact`, `riser`, `pop`, `tick`, `shimmer`), all generated here with no licence to worry about. For music, ask the user to choose a track. Check any downloaded track's licence.
6. **Master and export:** the references average about -17 LUFS, so match that.
```bash
ffmpeg -i projects/<reel-name>/work/draft.mp4 -af loudnorm=I=-17:TP=-1.5:LRA=9 -c:v copy -c:a aac -b:a 256k export/<reel-name>.mp4
```

### 8. Check before handing over
Pull frames from the export and look at them. Check caption spelling, that nothing sits in Instagram's covered zones, that numbers match the source, that the permit is shown where required, and that the audio doesn't clip. Report honestly what was checked. You can't hear the mix, so ask the user to listen to it.

### 9. Learn
Turn every correction into a rule, either in the relevant style reference or in memory. When the user shares a post's results, compare watch time, shares and DMs against earlier reels and update the guidance from what actually worked.

## Studying new references
```bash
python tools/analyze_reel.py references/<name>.mp4 references/analysis/<name>
python tools/analyze_sound.py references/<name>.mp4 references/analysis/<name>
```
Then read the `hook_*.jpg` and `body_*.jpg` sheets and the `report.json`. Add what's new to the style reference, or start a new style if it doesn't fit either one.
