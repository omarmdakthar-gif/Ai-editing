export type Bounds = {west: number; east: number; north: number; south: number; width: number; height: number};
export type Camera = {t: number; lon: number; lat: number; zoom: number; tilt: number; bearing: number};

export const SCREEN = {width: 1080, height: 1920, focusY: 1000, perspective: 1500};

const mercatorY = (lat: number) => Math.log(Math.tan(Math.PI / 4 + (lat * Math.PI) / 360));

export const toMapPixels = ([lon, lat]: number[], b: Bounds) => ({
	x: ((lon - b.west) / (b.east - b.west)) * b.width,
	y: ((mercatorY(b.north) - mercatorY(lat)) / (mercatorY(b.north) - mercatorY(b.south))) * b.height,
});

const ease = (x: number) => (x < 0.5 ? 2 * x * x : 1 - (-2 * x + 2) ** 2 / 2);

export const cameraAt = (keys: Camera[], time: number): Camera => {
	if (time <= keys[0].t) return keys[0];
	const next = keys.findIndex((k) => k.t > time);
	if (next === -1) return keys[keys.length - 1];
	const a = keys[next - 1];
	const b = keys[next];
	const p = ease((time - a.t) / (b.t - a.t));
	const mix = (u: number, v: number) => u + (v - u) * p;
	return {
		t: time,
		lon: mix(a.lon, b.lon),
		lat: mix(a.lat, b.lat),
		zoom: a.zoom * (b.zoom / a.zoom) ** p,
		tilt: mix(a.tilt, b.tilt),
		bearing: mix(a.bearing, b.bearing),
	};
};

export const planeTransform = (camera: Camera, b: Bounds) => {
	const centre = toMapPixels([camera.lon, camera.lat], b);
	return `translate3d(${SCREEN.width / 2}px, ${SCREEN.focusY}px, 0) rotateX(${camera.tilt}deg) rotateZ(${-camera.bearing}deg) scale(${camera.zoom}) translate(${-centre.x}px, ${-centre.y}px)`;
};

// Same maths as planeTransform, so screen-space labels stay pinned to the tilted map.
export const project = (point: number[], camera: Camera, b: Bounds) => {
	const p = toMapPixels(point, b);
	const c = toMapPixels([camera.lon, camera.lat], b);
	const dx = (p.x - c.x) * camera.zoom;
	const dy = (p.y - c.y) * camera.zoom;
	const r = (-camera.bearing * Math.PI) / 180;
	const x = dx * Math.cos(r) - dy * Math.sin(r);
	const y = dx * Math.sin(r) + dy * Math.cos(r);
	const t = (camera.tilt * Math.PI) / 180;
	const flatY = y * Math.cos(t);
	const depth = y * Math.sin(t);
	const f = SCREEN.perspective / (SCREEN.perspective - depth);
	return {x: SCREEN.width / 2 + x * f, y: SCREEN.focusY + flatY * f};
};

export const centroid = (coords: number[][]) => [
	coords.reduce((sum, c) => sum + c[0], 0) / coords.length,
	coords.reduce((sum, c) => sum + c[1], 0) / coords.length,
];
