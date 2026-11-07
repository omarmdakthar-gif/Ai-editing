#!/usr/bin/env python3
"""Write Google Earth Studio project files (.esp) from a shot list, for import into Earth Studio.

Usage: earth_esp.py <shots.json> <output folder>
shots.json: [{"name": "PS 1 Plot", "frames": 615,
              "keys": [{"t": 0, "lat": 24.95, "lon": 55.04, "alt": 70000}, ...]}]
Each key is in seconds and names the ground point the camera looks at, plus camera altitude in metres.
The camera looks north at a 45-degree tilt, so it sits `alt` metres south of that point.
Values are stored as Earth Studio's 0-1 "relative" numbers, decoded from a real project:
longitude (lon+180)/360, latitude (lat+90)/180, altitude (alt+500)/65117981.
"""
import json
import sys
from pathlib import Path

FPS = 30
ALT_MIN, ALT_MAX = -500, 65117481
METRES_PER_DEGREE_LAT = 111320
# Pan 0 (north) and tilt 45 degrees, copied from a project whose tracking data confirmed both.
PAN_NORTH = 0.9999999999914944
TILT_45 = 0.25000000000593464


def keyframes(keys, frames, value):
    duration = (frames - 1) / FPS
    return [{"time": min(k["t"] / duration, 1), "value": value(k)} for k in keys]


def project(shot):
    frames, keys = shot["frames"], shot["keys"]
    lon = lambda k: (k["lon"] + 180) / 360
    lat = lambda k: (k["lat"] - k["alt"] / METRES_PER_DEGREE_LAT + 90) / 180
    alt = lambda k: (k["alt"] - ALT_MIN) / (ALT_MAX - ALT_MIN)
    position = [
        {"type": "longitude", "value": {"relative": lon(keys[0])}, "keyframes": keyframes(keys, frames, lon), "inTimeline": True},
        {"type": "latitude", "value": {"relative": lat(keys[0])}, "keyframes": keyframes(keys, frames, lat), "inTimeline": True},
        {"type": "altitude", "value": {"maxValueRange": ALT_MAX, "minValueRange": ALT_MIN, "relative": alt(keys[0]), "logarithmic": False},
         "keyframes": keyframes(keys, frames, alt), "inTimeline": True},
    ]
    camera = {"type": "cameraGroup", "inTimeline": True, "attributes": [
        {"type": "cameraPositionGroup", "inTimeline": True, "attributes": [{"type": "position", "inTimeline": True, "attributes": position}]},
        {"type": "cameraTargetEffect", "attributes": [
            {"type": "enabled", "value": {}},
            {"type": "poi", "attributes": [{"type": "longitudePOI", "value": {}}, {"type": "latitudePOI", "value": {}},
                                           {"type": "altitudePOI", "value": {"maxValueRange": ALT_MAX, "minValueRange": ALT_MIN, "logarithmic": False}}]},
            {"type": "influence", "value": {}}]},
        {"type": "cameraRotationGroup", "inTimeline": True, "attributes": [
            {"type": "rotationX", "value": {"relative": PAN_NORTH}, "keyframes": [{"time": 0, "value": PAN_NORTH}], "inTimeline": True},
            {"type": "rotationY", "value": {"relative": TILT_45}, "keyframes": [{"time": 0, "value": TILT_45}], "inTimeline": True},
            {"type": "rotationZ", "value": {}}]},
        {"type": "cameraLensGroup", "attributes": [{"type": "fov", "value": {}}, {"type": "exposure", "value": {}},
                                                    {"type": "aperture", "value": {}}, {"type": "minFocusLength", "value": {}}]},
    ]}
    environment = {"type": "environmentGroup", "attributes": [
        {"type": "sunGroup", "attributes": [{"type": "sunVisibility", "value": {}}, {"type": "worldTime", "value": {}}]},
        {"type": "cloudGroup", "attributes": [{"type": "cloudVisibility", "value": {}}, {"type": "cloudopacity", "value": {}},
                                              {"type": "cloudheight", "value": {}}, {"type": "clouddate", "value": {}}]},
        {"type": "starsPlanetsGroup", "attributes": [{"type": "starsEnabled", "value": {}}]},
        {"type": "seawaterGroup", "attributes": [{"type": "seawater", "value": {}}, {"type": "influence", "value": {"relative": 1}}]},
        {"type": "buildingsEnabled", "value": {}},
    ]}
    return {
        "modelVersion": 18,
        "settings": {"name": shot["name"], "frameRate": FPS, "dimensions": {"width": 2160, "height": 3840}, "duration": frames, "timeFormat": "frames"},
        "scenes": [{"animationModel": {"roving": False, "logarithmic": False, "groupedPosition": True}, "duration": frames,
                    "attributes": [camera, environment], "cameraExport": {"logarithmic": False, "modelVersion": 2}}],
        "playbackManager": {"range": {"start": 0, "end": frames}},
    }


def main():
    shots = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for shot in shots:
        path = out / f"{shot['name']}.esp"
        path.write_text(json.dumps(project(shot)))
        print(path, shot["frames"], "frames")


if __name__ == "__main__":
    main()
