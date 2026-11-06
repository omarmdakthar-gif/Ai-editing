---
name: dubai-map-footage
description: Get sharp 4K map footage of any Dubai location for reels, using Google Earth Studio camera moves generated as project files, plus exact overlay data (plot outlines, coastline, port, airport and real road routes) and frame-locked camera tracking. Use this whenever the user wants map shots, a fly-over, a location or nearby-places reel, drive-time routes, a community outline, or "the map part" of a reel, even if they don't name Earth Studio.
---

# Dubai map footage

Produces the map half of a map-explainer reel: 4K Google Earth fly-overs with per-frame camera tracking, and real-world geometry to draw on top. The editing half lives in the `reel-editor` skill (`ExplainerReel` composition). Work from `/Users/maccy/Ai Editing`, after running `source tools/env.sh`.

## Rules that never bend
- **Google's credit stays on screen** for every frame of Earth footage. Never erase, blur, cover, or scale or crop it out of frame. The user has asked for all of these, and each was declined. From now on, set the attribution to bottom left: Custom, X 80, Y 3343, Left. Keep every overlay and the speaker cut-out clear of it, and list the imagery providers from `ImagerySources.txt` as on-screen text.
- **A clean frame with no watermark is only possible with non-Google imagery.** For covers, use the stylised OpenStreetMap map (`Cover` with `vector`).
- **No Arabic** anywhere. Plot outlines that aren't official are approximate: say so in the post caption, not as an on-screen label.
- **Real data only.** Outlines come from OpenStreetMap or the user's marked screenshot. Jafza has no OpenStreetMap boundary, so use a pin, never a guessed outline.

## 1. Places
- **Atlas lookup:** `python tools/dubai_place.py "<name>"` (data in `atlas/dubai/`). Add a custom plot to `atlas/dubai/manual.geojson`.
- **Marked screenshot from the user:** that is the source of truth for the plot. Georeference it against the map before tracing.
- **OpenStreetMap geometry:** use `curl` with a User-Agent header against overpass-api.de (the Python fetcher kept getting 502 errors), with `out geom`. Useful queries:
  - `way["natural"="coastline"](S,W,N,E)` for coastline. The Palm comes as fragments, so draw it as `line` shapes.
  - `way(<id>)` for a known airport or harbour polygon.
  - `way["highway"="motorway"]["ref"~"E ?11"](…)` for Sheikh Zayed Road.

## 2. Drive-time routes
```bash
curl -s "https://router.project-osrm.org/route/v1/driving/<lon,lat>;<lon,lat>?overview=full&geometries=geojson"
```
Start from a road on the plot's edge, not its centre. Then **check that the route follows roads visible in the imagery**:
```bash
python tools/earth_overlay_check.py "Maps/<shot>" <frame> lines.json out.jpg
```
OSRM can route over roads newer than Google's imagery, or end inside an airfield. Fix the destination (for example the airport's passenger terminal) or add waypoints until the route sits on visible roads. Times are without traffic, so round up honestly ("20–25 min").

## 3. Camera moves (no hand keyframing)
Write `projects/<reel>/earth-shots.json`. Each shot has a `name`, `frames` (30fps, about 0.5 s longer than its beat), and `keys` of `{t, lat, lon, alt}`, where `lat`/`lon` is the ground point the camera looks at. The camera looks north at a 45° tilt, sitting `alt` metres south.
```bash
python tools/earth_esp.py projects/<reel>/earth-shots.json projects/<reel>/earth
```
**Framing guide:** the default vertical field of view is 20°, so the visible width is about 0.28 × altitude. A 4–5 km plot needs about 16–20 km of altitude, and a whole-area view (Palm, port and Marina) about 80–90 km. Plan three shots or fewer per reel. Earth Studio renders about 1 frame per second at 4K, about 4 MB per frame.

## 4. Render in Earth Studio (Claude in Chrome)
1. Open `earth.google.com/studio`. File → Import is a Mac file dialog, so first run a page script that patches `HTMLInputElement.prototype.click` to capture file inputs as `window.__fi` instead of opening them. Click the menu item through its `find` ref, because hovering closes the submenu. Then use `find` for the file input and `file_upload` to attach the `.esp`. If `__fi` is disconnected, re-append it to `document.body`.
2. **Render settings:**
   - Image sequence, 2160×3840.
   - Attribution Custom, X 80, Y 3343, Left. Earth Studio resets this on every project, so set it every time.
   - Advanced: 3D Tracking Data JSON, Global coordinates.
   - Destination `Maps`.
3. Click Start. Only the first render of a session needs the user to allow the folder.
4. Import each render: `python tools/earth_import.py "Maps/<shot>" <name>`, which writes `tools/remotion/public/earth/<name>/map.mp4` and `camera.json`.

## 5. Overlays that stay locked
- `ExplainerReel` projects every `[lon, lat]` with that frame's tracked camera (`earthCamera.ts`). Earth Studio uses a sphere of radius 6,371,010 m.
- Footage and overlays must use **the same whole-frame index** (`startFrom + sequence frame`). Times that fall on half-frames once caused a one-frame lag, which looked like jitter.
- Labels stay locked to the ground and fade near the frame edges and the logo zone. Never push them around to keep them on screen.
- Check consecutive frames during a camera move, and a frame from every map beat for logo clearance.

## 6. Covers with no watermark
Use the `Cover` composition with `vector` (`VectorMap.tsx`): a dark, tilted, glowing map built from the same OpenStreetMap lines and routes, with labels on the ground and a small OpenStreetMap credit. Template: `projects/palm-springs-trial/cover_vector.json`.

## Files
- **Tools:** `tools/earth_esp.py`, `tools/earth_import.py`, `tools/earth_overlay_check.py`, `tools/map_roads.py`, `tools/dubai_place.py`, `tools/dubai_atlas.py`.
- **Code:** `tools/remotion/src/kit/earthCamera.ts`, `ExplainerReel.tsx`, `Cover.tsx`, `VectorMap.tsx`.
- **Worked example:** `projects/palm-springs-trial/` (`earth-shots.json`, `build_edit.py`, `cover_vector.json`, `post.md`).
