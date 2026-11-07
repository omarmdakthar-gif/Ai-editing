# Map Explainer style

Studied from ref11 and ref12. The map is the star. The speaker sits in a small corner window, and every place they name lights up as they say it. It explains location and value faster than any talking head, and it suits comparing projects.

Best for: why a location matters, one project against another, what's nearby, price per square foot comparisons, and correcting a common sales claim.

## Filming
Very easy. The speaker films a plain selfie to camera in front of a clean wall, in good light. The reel does the rest.

## Layout (1080×1920)
- **Map:** full frame, tilted about 45–55°, with the sea or haze fading out at the top.
- **Speaker window:** square, about 286px, top right, 15–30% down the frame, rounded corners and a thin white border.
- **Caption pill:** navy `#20264A`, centred about 67% down. Short, 2–5 words.
- **Handle:** tiny white pill below the caption, about 78% down.
- **Pop-up cards:** centre of the frame, around 50–55% down, kept clear of the place being discussed.

## Colour code
Each place keeps one colour for the whole reel, so viewers learn the map.
| Use | Colour |
|---|---|
| The main project or plot | Purple `#D45CF0` |
| Palm or waterfront landmark | Cyan `#45E8EC` |
| Free zone or jobs area | Green `#4FD08A` |
| Port or major roads | Blue `#6C8CFF` |
| Sheikh Zayed Road, downtown | Red `#FF5C70` |
| Airport | Amber `#F5B042` |
| Beach | Lime `#BDF23C` |

## Map graphics
- **Plot outline:** a neon line draws around the plot with a white core, then the fill fades in at about 40%.
- **Labels:** white pill, bold uppercase, wide letter spacing, with a thin stem to a dot on the plot.
- **Chips:** small coloured tag below the label for one fact: "200 hectares", "AED 128 billion", "80+ resorts & hotels", "6.6 km".
- **Road lines:** glow lines draw on along real roads and coastlines.
- **Landmark trace:** the Palm is traced in cyan as if drawn with light.
- **Distance line:** white bracket line between two places, with a label such as "Inland" or "almost 3 km".
- **Size overlay:** one shape dropped onto another to compare, like Palm Jumeirah in amber sitting on Palm Jebel Ali.

## Camera
The map never stops moving. There's a slow drift and rotation between beats, then a fast fly to the next place as it's named. Zoom right out once near the end to show everything together, then fly back to the plot for the call to action. This reel repeats that structure: plot, each nearby place, wide view of them all, back to the plot.

## Cards on top of the map
- **Count-up card:** a white card where the number rolls up: "1,750 AED per sq ft" with a coloured underline.
- **News card:** a real headline with the publisher's logo, shown while the fact is spoken. Use a real capture, cropped clean, and keep the publisher readable. Never retype or alter one.
- **Compare card:** "Palm Springs = Palm Jebel Ali", then the equals flips to a red ≠.
- **Message card:** a sample sales message that gets a red strike. If it isn't a real message, it must read as illustrative.
- **Comment card:** a checklist of what viewers get, then "PALM" typed into a comment box with a reply appearing.

## Light scenes between maps
Every 15–30 seconds, cut to a pale blue-white `#F3F7FF` screen with blue `#2F6BFF` accents and a soft isometric 3D drawing. A sea of small buildings for "12,000 companies", towers with one filled for "1 in 4 jobs", a ring gauge for "36% of GDP". The stat is big and bold at the top with an italic serif word below it. These reset attention. Build them in HyperFrames.

## Fonts
Closest free matches, chosen by eye.
- Caption: Inter Tight 700, with key words in Instrument Serif italic in pale blue `#C9D6FF`.
- Words brighten from dim to white as they're spoken.
- Numbers: Inter Tight 700 with even-width digits, so they don't jitter while counting.

## Timing and sound
- Scene-cut detection found only 1–2 cuts per reel because the map moves continuously. Expect something new on screen every 2–4 seconds.
- Speech pace is about 200 words a minute.
- Voice-led mix. Gaps sit 11–12.5 dB below speech, the quietest music of all the references. Keep music low and let soft pops and whooshes mark each new place.
- Master around -17 LUFS.

## Script shape
1. Claim or question, straight onto the map.
2. Nearby places one by one, each with one number and one source.
3. "So this isn't the edge of Dubai", the wide view that pays it all off.
4. Comment keyword, saying exactly what they'll receive.

## Variant: top-down master plan (ref13)
Same idea with a different finish. Use it when the project has a master plan image.
- **Camera:** straight down with no tilt, plus slow zooms and fast moves between places.
- **Master plan on the map:** the developer's plan sits exactly over the empty plot, so the viewer sees the future community on real land.
- **Speaker:** a wide rounded panel across the bottom third, and sometimes full screen for a personal point.
- **Colour:** one colour only, magenta pink, around `#D6005C`, for labels, pins and thin outlines. It looks cleaner than the multicolour version.
- **Hook banner:** bold pink box with white capitals, top of frame: "NEW CHEAP VILLAS IN DUBAI".
- **Place labels:** pink boxes, white Montserrat-style bold text, with pink pins.
- **Thin outlines:** a single thin pink line that draws around the area, with no glow.
- **Price cards:** cream card with property photo, bold green USD price, then AED, EUR, GBP and INR below it. This suits international buyers.
- **Stat chip:** white card, green bold number, "200,000+ people working".
- **Captions:** small white bold text just above the speaker, one or two words at a time.
- **Logo grid:** pale grey screen where logos arrive one by one to show a developer's track record.
- **Compliance:** a QR code with "We are licensed and regulated in the UAE" while the speaker is on screen.
- **End:** pale screen with "comment SPRINGS" in a pink box and what they'll receive.
- Timing: 6 detected cuts in 60 seconds, 184 words a minute, music closer to the voice at about 3 dB below speech.

## Dubai atlas
`atlas/dubai` holds every named Dubai place in OpenStreetMap: 717 places, 581 with boundaries, with size, parent area and centre. English only, at the user's request: no Arabic names, and places named only in Arabic are left out. Use it before guessing any location.
- **Find a place:** `python tools/dubai_place.py <name>` matches loosely and knows JVC, JLT, JBR, DIFC, MBR City and similar short names. Add `--save outline.json` to get `lines` and `anchor`, ready for a `shapes` entry.
- **Browse:** `atlas/dubai/A-Z.md` is the readable index, and `atlas.csv` is a spreadsheet of the same data.
- **Rebuild:** `python tools/dubai_atlas.py atlas/dubai` downloads fresh data, which can take up to 5 minutes when the free server is busy. Add `--offline` to rebuild from the cache in under a second.
- **Your traced outlines win:** save outlines traced from the user's marked screenshots in `atlas/dubai/manual.geojson`. Each needs a `name` and optionally `source`. They replace OpenStreetMap shapes of the same name and stay for future reels.
- **Limits:** these are volunteer-mapped community areas, not official DLD plots or project boundaries. Some places are points only, such as JVT, Damac Hills, Dubai South, Deira, Karama and Mudon. Some are missing, such as Palm Jebel Ali as an area, Tilal Al Ghaf, La Mer and Al Habtoor City. "Merged" outlines like Dubai Hills Estate join the mapped parts and may cover only part of the community. Always compare with the user's screenshot before showing a boundary.
- **Credit:** anything drawn from the atlas needs "© OpenStreetMap contributors" in the on-screen credit.

## Map data
- **Quality bar:** the user requires sharp, 4K-looking imagery. They rejected the soft Sentinel-2 test, so `tools/map_tiles.py` with its default source isn't good enough for finished reels.
- **Imagery source:** Google Earth, through Google Earth Studio. The user treats these reels as educational, and that's their decision. Google's credit must stay visible on every frame: never crop, cover or remove it. Earth Studio writes it onto each rendered frame, and its position can be set in Render Settings, so keep it clear of the Instagram interface.
- **Never pull Google imagery by scraping tiles or scripts.** Earth Studio's own render is the route.
- **Reminder for the user:** if a reel carries a comment-for-leads call to action or promotes a specific project, flag once in the storyboard notes that it may read as promotional under Google's rules. Don't argue it further. It's their call.
- **Earth Studio access:** it needs the user's own Google account in Chrome. Access is by request, and only the user can sign in.
- **Locations:** the user sends a marked screenshot of each location. Treat that as the source of truth for boundaries, and ask rather than guess when a mark is unclear.
- **Exact overlays on moving footage:** this is solved. Export Earth Studio's 3D tracking data as JSON with Global coordinates. The `EarthReel` composition projects any longitude and latitude onto every frame, tested against real coastlines at both ends of a moving shot. Earth Studio uses a sphere of radius 6,371,010m, which `earthCamera.ts` handles.
- **Traced landmarks:** OpenStreetMap coastlines can draw the neon Palm trace automatically. Coverage varies, and the first test missed the left fronds, so check every trace before showing it.
- **Imagery seams:** Google's mosaic can show colour bands, especially over water. Check the frames and move the camera if a seam falls in the hero area.
- **Roads:** `tools/map_roads.py` fetches OpenStreetMap geometry, which needs on-screen credit.
- **Project claims:** mark anything approximate as "illustrative", as ref12 does with "Water features (illustrative)".

## House style for map reels (locked 2026-11-02)
The user approved `export/palm-springs-final.mp4` as the template for every map reel. Start each new map reel by copying `projects/palm-springs-trial/build_edit.py`, keeping `layout: 'v1'`, the boxless gold-highlight captions, the glass cards and labels, the comment card with the IG profile photo, and the sound setup. Change only the places, shapes, routes, facts and timings. Don't redesign the look unless the user asks.

## Faster route: generate the shots (used for the Palm Springs trial)
1. Write a shot list (`projects/<reel>/earth-shots.json`: per shot `name`, `frames`, and keys of `t` seconds, target `lat`/`lon`, camera `alt` in metres), then run `python tools/earth_esp.py <shots.json> projects/<reel>/earth`. The camera always looks north at a 45° tilt. At that tilt the default 20° vertical field of view shows a strip about 0.28 × altitude wide, so a 4.5 km plot needs about 16–20 km of altitude.
2. In Earth Studio, go to File → Import → Earth Studio Project. That opens a Mac file window, so first run this page script, which captures the file input instead: patch `HTMLInputElement.prototype.click` so that file inputs are attached to the page as `window.__fi` and not opened. Then click the menu item through its `find` ref, because hovering closes the submenu. Locate the input with `find` and attach the `.esp` with `file_upload`. If `__fi` shows as disconnected, re-append it to `document.body`.
3. Render as in step 2 below, setting the attribution every time. Only the first render of a session needed the user to allow the `Maps` folder. Speed is about 1 frame per second at 4K.
4. Compose with the `ExplainerReel` composition (`tools/remotion/src/kit/ExplainerReel.tsx`). It cuts between full-screen speaker clips and several Earth shots, shows a sticker-style cut-out over the map, and adds phrase captions, count cards, headline and flash words, a comment card and an end card. A per-reel `build_edit.py` writes the props (see `projects/palm-springs-trial/build_edit.py`).
5. **Logo position from the next reel on** (the user asked for it at the bottom, 2026-11-02): set Attribution to Custom, X 80, Y 3343, Left, which puts it at bottom left about 87% down, clear of the speaker cut-out at bottom right. Then move `LOGO_ZONE` and the credit text in `ExplainerReel` to match. **Never scale or crop the footage so the logo falls out of frame.** The user asked for that, and it was declined, because Google requires "Google Earth" and the imagery providers on screen for as long as the footage shows. Cropping it off counts as removing it.
6. **Logo clearance:** an outline once ran straight through the "Google Earth" logo. `ExplainerReel` now masks all shapes out of `LOGO_ZONE` and keeps label anchors below it. Still check a frame from every Earth beat for this.
6. Shapes: OpenStreetMap through `curl` with a User-Agent header (the Python fetch kept getting 502 errors), plus driving routes from OSRM. Fragmented coastline works as `line` shapes. Jafza has no boundary in OpenStreetMap, so use a pin, never a guessed outline.

## Building one with Google Earth (finished reels)
1. **In Earth Studio** (the user is signed in, and Claude in Chrome can drive it): create a project at 2160×3840, 30 FPS. Set keyframes for position, altitude, pan and tilt. At 45° tilt the camera looks north, so place it south of the target by roughly its altitude.
2. **Render:** Image sequence, Advanced → 3D Tracking Data → JSON, Global. Destination is `Ai Editing/Maps`, which Earth Studio remembers. If it ever asks again, the user must click Choose folder, because it's a Mac window.
   - **Attribution, set on every render** because Earth Studio resets it to Bottom right: Attribution Position **Custom**, X **80**, Y **360**, Text Alignment **Left**. Google's logo then sits top left, about 10–49% across and 13–16% down, clear of the speaker window, captions and Instagram's buttons.
   - **Don't remove, blur, crop or cover it**, which the user has agreed to. Only the logo is written into frames. The imagery sources come in `ImagerySources.txt` and must be shown as the on-screen `credit`, which `EarthReel` places just under the logo.
   - **Keep the top-left corner clear** from 10% to 24% down. In the top-down variant, put the hook banner below that, or top right if there's no speaker window.
3. **Import:** `python tools/earth_import.py "Maps/<project>" <name>` creates `public/earth/<name>/map.mp4` and `camera.json`.
4. **Compose:** write props with `earth: {video, frames, credit}` and copy `frames` from `camera.json`. The credit lists Google Earth, the imagery sources from `ImagerySources.txt`, and OpenStreetMap if it's used. `shapes` use `[lon, lat]` points, and the optional `anchor` sets the label position.
5. **Render:** `npx remotion render src/index.ts EarthReel <out.mp4> --props=<props.json> --scale=2 --crf=16`
6. Delete `public/earth/<name>` afterwards, because everything in `public` is copied on every render.

Five seconds of test footage rendered in about 43 seconds. Each Earth Studio shot is about 4MB a frame, so plan disk space, at roughly 590MB per 5 seconds.

## Layout tests with Sentinel imagery
```bash
python tools/map_tiles.py <west> <south> <east> <north> 14 tools/remotion/public/<reel>/map
python tools/map_roads.py "Sheikh Zayed|E ?11" <west> <south> <east> <north> projects/<reel>/work/szr.json motorway
cd tools/remotion && npx remotion render src/index.ts MapReel ../../projects/<reel>/work/draft.mp4 --props=../../projects/<reel>/edit.json
```
Add `--scale=2` to any render for 4K output (2160×3840). These `map_tiles.py` commands are for layout tests only. Finished reels use Earth Studio imagery. Download about 20% more area north than needed, so the tilted map fills the frame. The `MapReelProps` type in `tools/remotion/src/kit/MapReel.tsx` lists every field, and `camera` keyframes set `lon`, `lat`, `zoom`, `tilt` and `bearing`. Zoom of about 0.5–0.9 suits z14 imagery. Beyond 1 it turns visibly soft.
