export type EarthFrame = {p: number[]; r: number[]; fov: number};

// Earth Studio places cameras on a sphere of this radius, not the WGS84 ellipsoid.
const EARTH_RADIUS = 6371010;

const toRadians = (degrees: number) => (degrees * Math.PI) / 180;

const worldPoint = ([lon, lat]: number[]) => {
	const a = toRadians(lon);
	const b = toRadians(lat);
	return [EARTH_RADIUS * Math.cos(b) * Math.cos(a), EARTH_RADIUS * Math.cos(b) * Math.sin(a), EARTH_RADIUS * Math.sin(b)];
};

const multiply = (a: number[][], b: number[][]) =>
	a.map((row) => b[0].map((_, c) => row.reduce((sum, value, r) => sum + value * b[r][c], 0)));

const rotation = ([x, y, z]: number[]) => {
	const [cx, sx] = [Math.cos(toRadians(x)), Math.sin(toRadians(x))];
	const [cy, sy] = [Math.cos(toRadians(y)), Math.sin(toRadians(y))];
	const [cz, sz] = [Math.cos(toRadians(z)), Math.sin(toRadians(z))];
	const rx = [[1, 0, 0], [0, cx, -sx], [0, sx, cx]];
	const ry = [[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]];
	const rz = [[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]];
	return multiply(multiply(rx, ry), rz);
};

// Camera axes from Earth Studio's JSON: x right, y down, z forward.
export const earthProjector = (frame: EarthFrame, width: number, height: number) => {
	const axes = rotation(frame.r);
	const focal = height / 2 / Math.tan(toRadians(frame.fov) / 2);
	return (point: number[]) => {
		const world = worldPoint(point);
		const d = world.map((value, i) => value - frame.p[i]);
		const [x, y, z] = [0, 1, 2].map((c) => axes.reduce((sum, row, r) => sum + row[c] * d[r], 0));
		const depth = Math.max(z, 1);
		return {x: width / 2 + (x / depth) * focal, y: height / 2 + (y / depth) * focal};
	};
};
