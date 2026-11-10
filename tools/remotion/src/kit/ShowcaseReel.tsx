import React, {useEffect, useMemo, useState} from 'react';
import {AbsoluteFill, Audio, OffthreadVideo, Sequence, continueRender, delayRender, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import '@fontsource/inter-tight/500.css';
import '@fontsource/inter-tight/700.css';
import '@fontsource/sora/800.css';
import '@fontsource/instrument-serif/400-italic.css';
import {Sound} from './styles';

// A cinematic map explainer drawn live from OpenStreetMap geometry. Every frame projects the map
// through a tilted 3D camera, so lines stay sharp at any zoom and overlays stay pinned to places.

type LonLat = number[];
export type CamKey = {t: number; lon: number; lat: number; km: number; tilt: number; bearing: number};
export type Feature = {
	kind: 'area' | 'line' | 'pin';
	lines?: LonLat[][];
	at?: LonLat;
	color: string;
	start: number;
	end?: number;
	labelEnd?: number;
	draw?: number;
	label?: string;
	chip?: string;
	anchor?: LonLat;
	side?: 'up' | 'down';
	pulse?: boolean;
	dim?: boolean;
	fill?: number;
};
export type CaptionLine = {start: number; end: number; text: string; speech?: number};
export type Headline = {start: number; end: number; kicker?: string; lines: string[]; y?: number; align?: 'left' | 'center'};
export type Card =
	| {type: 'badges'; start: number; end: number; items: {name: string; sub: string; color: string}[]}
	| {type: 'count'; start: number; end: number; value: number; prefix?: string; suffix?: string; unit: string; note?: string; color: string; y?: number}
	| {type: 'compare'; start: number; end: number; columns: {name: string; color: string; place: string}[]; rows: {at: number; label: string; value: string; note?: string}[]}
	| {type: 'list'; start: number; end: number; title: string; color: string; items: {at: number; text: string}[]; y?: number}
	| {type: 'meter'; start: number; end: number; label: string; level: number; color: string; caption: string}
	| {type: 'stamp'; start: number; end: number; text: string; sub?: string; color: string; y?: number};
export type ShowcaseProps = {
	durationSeconds: number;
	mapFile: string;
	camera: CamKey[];
	features: Feature[];
	captions: CaptionLine[];
	headlines?: Headline[];
	cards?: Card[];
	speaker?: {video: string; hide?: number[][]};
	voice?: string;
	music?: {file: string; volume: number};
	sounds?: Sound[];
	endCard?: {start: number; keyword: string; phone: string; detail: string};
	hideBase?: boolean;
	noScrim?: boolean;
	credit: string;
	disclaimer?: {start: number; end: number; text: string}[];
};

type MapData = {
	base: Record<'fine' | 'coarse', Record<string, LonLat[][]>>;
};

const W = 1080;
const H = 1920;
const FOCUS_Y = 1010;
const PERSPECTIVE = 1700;
const SANS = 'Inter Tight';
const SERIF = 'Instrument Serif';
const DISPLAY = 'Sora';
const GOLD = '#FFC940';
const SEA = '#03060D';
const LAND = '#0C1426';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const easeInOut = (x: number) => (x < 0.5 ? 4 * x * x * x : 1 - (-2 * x + 2) ** 3 / 2);
const easeOut = (x: number) => 1 - (1 - x) ** 3;

// ---------- Camera ----------
const LAT0 = 25.0;
const M_LON = 111320 * Math.cos((LAT0 * Math.PI) / 180);
const M_LAT = 110540;
const toM = (p: LonLat) => [(p[0] - 55) * M_LON, -(p[1] - LAT0) * M_LAT];

type Cam = {x: number; y: number; scale: number; tilt: number; bearing: number};

const cameraAt = (keys: CamKey[], time: number): Cam => {
	const make = (k: CamKey): Cam => {
		const [x, y] = toM([k.lon, k.lat]);
		return {x, y, scale: W / (k.km * 1000), tilt: k.tilt, bearing: k.bearing};
	};
	if (time <= keys[0].t) return make(keys[0]);
	const i = keys.findIndex((k) => k.t > time);
	if (i === -1) return make(keys[keys.length - 1]);
	const a = make(keys[i - 1]);
	const b = make(keys[i]);
	const p = easeInOut((time - keys[i - 1].t) / (keys[i].t - keys[i - 1].t));
	const mix = (u: number, v: number) => u + (v - u) * p;
	return {x: mix(a.x, b.x), y: mix(a.y, b.y), scale: a.scale * (b.scale / a.scale) ** p, tilt: mix(a.tilt, b.tilt), bearing: mix(a.bearing, b.bearing)};
};

const makeProjector = (cam: Cam) => {
	const r = (-cam.bearing * Math.PI) / 180;
	const cr = Math.cos(r);
	const sr = Math.sin(r);
	const t = (cam.tilt * Math.PI) / 180;
	const ct = Math.cos(t);
	const st = Math.sin(t);
	const project = (mx: number, my: number) => {
		const dx = (mx - cam.x) * cam.scale;
		const dy = (my - cam.y) * cam.scale;
		const x = dx * cr - dy * sr;
		const y = dx * sr + dy * cr;
		const f = PERSPECTIVE / Math.max(120, PERSPECTIVE - y * st);
		return [W / 2 + x * f, FOCUS_Y + y * ct * f];
	};
	// Visible region on the ground, found by unprojecting the screen corners, in rotated plane pixels.
	const unproject = (X: number, Y: number) => {
		const v = Y - FOCUS_Y;
		const y = (v * PERSPECTIVE) / Math.max(1, ct * PERSPECTIVE + v * st);
		const f = PERSPECTIVE / Math.max(120, PERSPECTIVE - y * st);
		return [(X - W / 2) / f, y];
	};
	const corners = [unproject(-80, -80), unproject(W + 80, -80), unproject(-80, H + 80), unproject(W + 80, H + 80)];
	const box = {
		x0: Math.min(...corners.map((c) => c[0])), x1: Math.max(...corners.map((c) => c[0])),
		y0: Math.min(...corners.map((c) => c[1])), y1: Math.max(...corners.map((c) => c[1])),
	};
	// Is a circle (plane metres) on screen?
	const visible = (mx: number, my: number, radiusM: number) => {
		const dx = (mx - cam.x) * cam.scale;
		const dy = (my - cam.y) * cam.scale;
		const x = dx * cr - dy * sr;
		const y = dx * sr + dy * cr;
		const rad = radiusM * cam.scale;
		return x + rad > box.x0 && x - rad < box.x1 && y + rad > box.y0 && y - rad < box.y1;
	};
	return {project, visible, box};
};

type Prepared = {pts: Float64Array; cx: number; cy: number; r: number}[];
const prepare = (lines: LonLat[][]): Prepared =>
	lines.map((line) => {
		const pts = new Float64Array(line.length * 2);
		let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
		line.forEach((p, i) => {
			const [x, y] = toM(p);
			pts[i * 2] = x;
			pts[i * 2 + 1] = y;
			x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y);
		});
		return {pts, cx: (x0 + x1) / 2, cy: (y0 + y1) / 2, r: Math.hypot(x1 - x0, y1 - y0) / 2};
	});

const pathOf = (layer: Prepared, proj: ReturnType<typeof makeProjector>, closed: boolean) => {
	let d = '';
	for (const line of layer) {
		if (!proj.visible(line.cx, line.cy, line.r)) continue;
		const n = line.pts.length / 2;
		for (let i = 0; i < n; i++) {
			const [x, y] = proj.project(line.pts[i * 2], line.pts[i * 2 + 1]);
			d += `${i ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)}`;
		}
		if (closed) d += 'Z';
	}
	return d;
};

// ---------- Base map ----------
const BaseMap: React.FC<{layers: Record<string, Prepared>; proj: ReturnType<typeof makeProjector>; cam: Cam; time: number}> = ({layers, proj, cam, time}) => {
	const land = pathOf(layers.land, proj, true);
	const water = pathOf(layers.water, proj, true);
	const districts = layers.districts ? pathOf(layers.districts, proj, false) : '';
	const secondary = layers.secondary ? pathOf(layers.secondary, proj, false) : '';
	const primary = pathOf(layers.primary, proj, false);
	const major = pathOf(layers.major, proj, false);
	const runways = pathOf(layers.runways, proj, false);
	// Ground grid every 2 km (5 km when wide), for depth.
	const step = cam.scale > 0.05 ? 2000 : 5000;
	let grid = '';
	const reach = Math.max(Math.abs(proj.box.x0), Math.abs(proj.box.x1), Math.abs(proj.box.y0), Math.abs(proj.box.y1)) / cam.scale;
	const gx0 = Math.floor((cam.x - reach) / step) * step;
	const gy0 = Math.floor((cam.y - reach) / step) * step;
	for (let gx = gx0; gx <= cam.x + reach; gx += step) {
		const a = proj.project(gx, cam.y - reach);
		const b = proj.project(gx, cam.y + reach);
		grid += `M${a[0].toFixed(1)} ${a[1].toFixed(1)}L${b[0].toFixed(1)} ${b[1].toFixed(1)}`;
	}
	for (let gy = gy0; gy <= cam.y + reach; gy += step) {
		const a = proj.project(cam.x - reach, gy);
		const b = proj.project(cam.x + reach, gy);
		grid += `M${a[0].toFixed(1)} ${a[1].toFixed(1)}L${b[0].toFixed(1)} ${b[1].toFixed(1)}`;
	}
	const shimmer = 0.5 + 0.5 * Math.sin(time * 0.8);
	return (
		<>
			<svg width={W} height={H} style={{position: 'absolute'}}>
				<path d={grid} stroke="rgba(90,130,220,0.07)" strokeWidth={1} fill="none" />
				<path d={land} fill={LAND} fillRule="evenodd" />
				<path d={districts} stroke="rgba(140,165,220,0.10)" strokeWidth={1} fill="none" strokeDasharray="3 5" />
				<path d={water} fill={SEA} />
				<path d={secondary} stroke="rgba(92,118,170,0.35)" strokeWidth={1.1} fill="none" />
				<path d={primary} stroke="rgba(120,148,205,0.5)" strokeWidth={1.5} fill="none" />
				<path d={runways} stroke="rgba(160,180,220,0.55)" strokeWidth={3} fill="none" strokeLinecap="round" />
			</svg>
			<svg width={W} height={H} style={{position: 'absolute', filter: 'blur(6px)'}}>
				<path d={land} fill="none" stroke="#2C8CFF" strokeOpacity={0.28 + 0.08 * shimmer} strokeWidth={5} />
				<path d={major} stroke="#E9B872" strokeOpacity={0.35} strokeWidth={6} fill="none" />
			</svg>
			<svg width={W} height={H} style={{position: 'absolute'}}>
				<path d={land} fill="none" stroke="#6FC3FF" strokeOpacity={0.55} strokeWidth={1.2} />
				<path d={major} stroke="#F2C987" strokeOpacity={0.85} strokeWidth={1.8} fill="none" strokeLinecap="round" />
			</svg>
		</>
	);
};

// ---------- Story features ----------
const FeatureLayer: React.FC<{f: Feature; prepared: Prepared; proj: ReturnType<typeof makeProjector>; time: number}> = ({f, prepared, proj, time}) => {
	if (time < f.start || f.kind === 'pin') return null;
	const draw = easeOut(interpolate(time, [f.start, f.start + (f.draw ?? 0.9)], [0, 1], clamp));
	const leave = f.end === undefined ? 1 : interpolate(time, [f.end, f.end + 0.4], [1, f.dim ? 0.25 : 0], clamp);
	if (leave <= 0) return null;
	const closed = f.kind === 'area';
	const d = prepared.map((line) => {
		let s = '';
		const n = line.pts.length / 2;
		for (let i = 0; i < n; i++) {
			const [x, y] = proj.project(line.pts[i * 2], line.pts[i * 2 + 1]);
			s += `${i ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)}`;
		}
		return s + (closed ? 'Z' : '');
	});
	const fill = closed ? interpolate(draw, [0.6, 1], [0, f.fill ?? 0.22], clamp) * leave : 0;
	const pulse = 0.75 + 0.25 * Math.sin(time * 5);
	const stroke = (width: number, color: string, opacity: number) =>
		d.map((p, i) => <path key={i} d={p} pathLength={1} fill="none" stroke={color} strokeOpacity={opacity * leave} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" strokeDasharray="1 1" strokeDashoffset={1 - draw} />);
	return (
		<>
			<svg width={W} height={H} style={{position: 'absolute'}}>{closed ? d.map((p, i) => <path key={i} d={p} fill={f.color} fillOpacity={fill} />) : null}</svg>
			<svg width={W} height={H} style={{position: 'absolute', filter: 'blur(10px)'}}>{stroke(16, f.color, 0.7 * pulse)}</svg>
			<svg width={W} height={H} style={{position: 'absolute'}}>
				{stroke(5, f.color, 0.95)}
				{stroke(1.8, '#FFFFFF', 0.95)}
			</svg>
		</>
	);
};

const centroid = (line: LonLat[]) => [line.reduce((s, p) => s + p[0], 0) / line.length, line.reduce((s, p) => s + p[1], 0) / line.length];

const LabelPin: React.FC<{f: Feature; proj: ReturnType<typeof makeProjector>; time: number}> = ({f, proj, time}) => {
	const at = f.anchor ?? f.at ?? (f.lines ? centroid(f.lines[0]) : null);
	if (!at || time < f.start) return null;
	const showLabel = !!f.label;
	const t0 = f.kind === 'pin' ? f.start : f.start + 0.35;
	const stop = f.labelEnd ?? f.end;
	const leave = stop === undefined ? 1 : interpolate(time, [stop, stop + 0.3], [1, 0], clamp);
	if (leave <= 0) return null;
	const [mx, my] = toM(at);
	const [x, y] = proj.project(mx, my);
	if (x < -300 || x > W + 300 || y < -200 || y > H + 200) return null;
	const pop = easeOut(interpolate(time, [t0, t0 + 0.45], [0, 1], clamp));
	const rise = (f.side === 'down' ? -1 : 1) * 105 * pop;
	const ring = (time - f.start) % 1.6;
	return (
		<div style={{position: 'absolute', left: x, top: y, opacity: leave}}>
			{f.pulse !== false ? (
				<div style={{position: 'absolute', left: -40, top: -40, width: 80, height: 80, borderRadius: 40, border: `3px solid ${f.color}`,
					transform: `scale(${0.3 + ring / 1.6})`, opacity: (1 - ring / 1.6) * pop}} />
			) : null}
			<div style={{position: 'absolute', left: -9, top: -9, width: 18, height: 18, borderRadius: 9, background: f.color, border: '3px solid white',
				boxShadow: `0 0 18px ${f.color}`, transform: `scale(${pop})`}} />
			{showLabel ? (
				<>
					<div style={{position: 'absolute', left: -1, top: rise > 0 ? -rise : 0, width: 2, height: Math.abs(rise),
						background: `linear-gradient(${rise > 0 ? '0deg' : '180deg'}, ${f.color}, rgba(255,255,255,0.9))`}} />
					<div style={{position: 'absolute', top: rise > 0 ? -rise - 12 : -rise + 12, transform: `translate(-50%, ${rise > 0 ? '-100%' : '0'}) scale(${0.85 + 0.15 * pop})`,
						opacity: pop, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 7}}>
						<div style={{background: 'linear-gradient(180deg, rgba(20,28,48,0.92), rgba(8,12,24,0.92))', border: `1.5px solid ${f.color}`,
							boxShadow: `0 0 24px ${f.color}55, inset 0 1px 0 rgba(255,255,255,0.15)`, color: 'white', fontFamily: SANS, fontWeight: 700,
							fontSize: 26, letterSpacing: '0.1em', padding: '10px 20px', borderRadius: 12, whiteSpace: 'nowrap', textTransform: 'uppercase'}}>
							{f.label}
						</div>
						{f.chip ? (
							<div style={{background: f.color, color: '#0A0F1C', fontFamily: SANS, fontWeight: 700, fontSize: 22, letterSpacing: '0.04em',
								padding: '5px 14px', borderRadius: 8, whiteSpace: 'nowrap'}}>{f.chip}</div>
						) : null}
					</div>
				</>
			) : null}
		</div>
	);
};

// ---------- Type ----------
export const Captions: React.FC<{captions: CaptionLine[]; time: number}> = ({captions, time}) => {
	const c = captions.find((x) => time >= x.start && time < x.end);
	if (!c) return null;
	const words = c.text.split(' ');
	// Reveal words across the time the line is actually spoken (speech end), not the time it stays on screen.
	const span = ((c.speech ?? c.end) - c.start) * 0.9;
	const fadeOut = interpolate(time, [c.end - 0.12, c.end], [1, 0], clamp);
	return (
		<div style={{position: 'absolute', top: 1335, left: 70, right: 70, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '4px 16px', opacity: fadeOut}}>
			{words.map((w, i) => {
				const at = c.start + (i / words.length) * span;
				const on = interpolate(time, [at - 0.05, at + 0.12], [0, 1], clamp);
				const accent = w.startsWith('*');
				return (
					<span key={i} style={{
						fontFamily: accent ? SERIF : SANS, fontStyle: accent ? 'italic' : 'normal', fontWeight: accent ? 400 : 700,
						fontSize: accent ? 66 : 54, lineHeight: 1.15, color: accent ? GOLD : 'white', letterSpacing: accent ? 0 : '-0.01em',
						textShadow: accent ? `0 0 22px ${GOLD}88, 0 3px 10px rgba(0,0,0,0.9)` : '0 3px 12px rgba(0,0,0,0.95), 0 0 2px rgba(0,0,0,0.9)',
						opacity: 0.35 + 0.65 * on, transform: `translateY(${(1 - on) * 10}px)`,
					}}>{accent ? w.slice(1) : w}</span>
				);
			})}
		</div>
	);
};

export const HeadlineView: React.FC<{h: Headline; time: number}> = ({h, time}) => {
	if (time < h.start || time > h.end + 0.4) return null;
	const out = interpolate(time, [h.end, h.end + 0.35], [1, 0], clamp);
	const align = h.align ?? 'left';
	return (
		<div style={{position: 'absolute', top: h.y ?? 250, left: 64, right: align === 'center' ? 64 : 360, textAlign: align, opacity: out}}>
			{h.kicker ? (
				<div style={{fontFamily: SANS, fontWeight: 700, fontSize: 26, letterSpacing: '0.3em', color: GOLD, marginBottom: 14,
					opacity: interpolate(time, [h.start, h.start + 0.3], [0, 1], clamp)}}>{h.kicker}</div>
			) : null}
			{h.lines.map((line, i) => {
				const t0 = h.start + 0.12 * i;
				const p = easeOut(interpolate(time, [t0, t0 + 0.5], [0, 1], clamp));
				const gold = line.startsWith('*');
				return (
					<div key={i} style={{overflow: 'hidden', paddingBottom: 6}}>
						<div style={{fontFamily: DISPLAY, fontWeight: 800, fontSize: gold ? 96 : 84, lineHeight: 1.0, letterSpacing: '-0.035em',
							color: gold ? GOLD : 'white', textShadow: gold ? `0 0 40px ${GOLD}66` : '0 6px 30px rgba(0,0,0,0.6)',
							transform: `translateY(${(1 - p) * 110}%)`}}>{gold ? line.slice(1) : line}</div>
					</div>
				);
			})}
			<div style={{height: 6, width: 160 * easeOut(interpolate(time, [h.start + 0.3, h.start + 0.9], [0, 1], clamp)), background: GOLD, borderRadius: 3, marginTop: 16,
				marginLeft: align === 'center' ? 'auto' : 0, marginRight: align === 'center' ? 'auto' : 0, boxShadow: `0 0 20px ${GOLD}`}} />
		</div>
	);
};

export const glass: React.CSSProperties = {
	background: 'linear-gradient(160deg, rgba(30,40,66,0.88), rgba(8,12,24,0.92))',
	border: '1.5px solid rgba(255,255,255,0.14)', borderRadius: 30,
	boxShadow: '0 30px 80px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.18)',
};

export const CardView: React.FC<{card: Card; time: number}> = ({card, time}) => {
	if (time < card.start || time > card.end + 0.4) return null;
	const inP = easeOut(interpolate(time, [card.start, card.start + 0.45], [0, 1], clamp));
	const out = interpolate(time, [card.end, card.end + 0.3], [1, 0], clamp);
	const enter: React.CSSProperties = {opacity: inP * out, transform: `translateY(${(1 - inP) * 40}px) scale(${0.94 + 0.06 * inP})`};
	if (card.type === 'badges') {
		return (
			<div style={{position: 'absolute', top: 650, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 28, ...enter}}>
				{card.items.map((it, i) => {
					const p = easeOut(interpolate(time, [card.start + 0.15 * i, card.start + 0.15 * i + 0.5], [0, 1], clamp));
					return (
						<div key={i} style={{...glass, width: 400, padding: '30px 26px', textAlign: 'center', borderColor: it.color, transform: `translateY(${(1 - p) * 60}px)`, opacity: p,
							boxShadow: `0 0 40px ${it.color}44, 0 30px 80px rgba(0,0,0,0.5)`}}>
							<div style={{fontFamily: DISPLAY, fontWeight: 800, fontSize: 64, letterSpacing: '0.04em', color: 'white'}}>{it.name}</div>
							<div style={{height: 4, width: 70, background: it.color, margin: '14px auto', borderRadius: 2}} />
							<div style={{fontFamily: SANS, fontWeight: 500, fontSize: 25, color: 'rgba(255,255,255,0.8)', letterSpacing: '0.05em'}}>{it.sub}</div>
						</div>
					);
				})}
			</div>
		);
	}
	if (card.type === 'count') {
		const v = card.value * easeOut(interpolate(time, [card.start + 0.1, card.start + 1.2], [0, 1], clamp));
		const shown = card.value >= 100 ? Math.round(v).toLocaleString('en-US') : v.toFixed(Number.isInteger(card.value) ? 0 : 1);
		return (
			<div style={{position: 'absolute', top: card.y ?? 800, left: 0, right: 0, display: 'flex', justifyContent: 'center', ...enter}}>
				<div style={{...glass, padding: '30px 64px 26px', textAlign: 'center', borderColor: `${card.color}88`}}>
					<div style={{fontFamily: DISPLAY, fontWeight: 800, fontSize: 104, lineHeight: 1, color: 'white', fontVariantNumeric: 'tabular-nums', letterSpacing: '-0.03em'}}>
						<span style={{color: card.color}}>{card.prefix ?? ''}</span>{shown}<span style={{color: card.color}}>{card.suffix ?? ''}</span>
					</div>
					<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 44, color: '#DCE6FF', marginTop: 8}}>{card.unit}</div>
					{card.note ? <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 18, letterSpacing: '0.14em', color: 'rgba(255,255,255,0.55)', marginTop: 12}}>{card.note}</div> : null}
				</div>
			</div>
		);
	}
	if (card.type === 'compare') {
		return (
			<div style={{position: 'absolute', top: 560, left: 54, right: 54, ...enter}}>
				<div style={{...glass, padding: '30px 30px 22px'}}>
					<div style={{display: 'flex', gap: 18}}>
						{card.columns.map((c, i) => (
							<div key={i} style={{flex: 1, textAlign: 'center', paddingBottom: 18, borderBottom: `3px solid ${c.color}`}}>
								<div style={{fontFamily: DISPLAY, fontWeight: 800, fontSize: 46, color: 'white', letterSpacing: '0.05em'}}>{c.name}</div>
								<div style={{fontFamily: SANS, fontWeight: 500, fontSize: 22, color: 'rgba(255,255,255,0.7)', marginTop: 4}}>{c.place}</div>
							</div>
						))}
					</div>
					{card.rows.map((r, i) => {
						const p = easeOut(interpolate(time, [r.at, r.at + 0.4], [0, 1], clamp));
						return (
							<div key={i} style={{marginTop: 18, opacity: p, transform: `translateX(${(1 - p) * -30}px)`}}>
								<div style={{fontFamily: SANS, fontWeight: 700, fontSize: 20, letterSpacing: '0.2em', color: GOLD, textAlign: 'center'}}>{r.label}</div>
								<div style={{fontFamily: DISPLAY, fontWeight: 800, fontSize: 42, color: 'white', textAlign: 'center', marginTop: 4, letterSpacing: '-0.01em'}}>{r.value}</div>
								{r.note ? <div style={{fontFamily: SANS, fontWeight: 500, fontSize: 20, color: 'rgba(255,255,255,0.6)', textAlign: 'center', marginTop: 2}}>{r.note}</div> : null}
							</div>
						);
					})}
				</div>
			</div>
		);
	}
	if (card.type === 'list') {
		return (
			<div style={{position: 'absolute', top: card.y ?? 640, left: 64, right: 64, ...enter}}>
				<div style={{...glass, padding: '30px 40px', borderColor: `${card.color}77`}}>
					<div style={{fontFamily: SANS, fontWeight: 700, fontSize: 24, letterSpacing: '0.28em', color: card.color, marginBottom: 12}}>{card.title}</div>
					{card.items.map((it, i) => {
						const p = easeOut(interpolate(time, [it.at, it.at + 0.4], [0, 1], clamp));
						return (
							<div key={i} style={{display: 'flex', alignItems: 'center', gap: 18, marginTop: 14, opacity: p, transform: `translateX(${(1 - p) * 40}px)`}}>
								<div style={{width: 14, height: 14, borderRadius: 7, background: card.color, boxShadow: `0 0 14px ${card.color}`}} />
								<div style={{fontFamily: DISPLAY, fontWeight: 800, fontSize: 44, color: 'white', letterSpacing: '-0.015em'}}>{it.text}</div>
							</div>
						);
					})}
				</div>
			</div>
		);
	}
	if (card.type === 'meter') {
		const fill = card.level * easeOut(interpolate(time, [card.start + 0.3, card.start + 1.3], [0, 1], clamp));
		return (
			<div style={{position: 'absolute', top: 820, left: 110, right: 110, ...enter}}>
				<div style={{...glass, padding: '28px 36px'}}>
					<div style={{display: 'flex', justifyContent: 'space-between', fontFamily: SANS, fontWeight: 700, fontSize: 24, letterSpacing: '0.2em', color: 'rgba(255,255,255,0.8)'}}>
						<span>{card.label}</span><span style={{color: card.color}}>LOW</span>
					</div>
					<div style={{height: 22, borderRadius: 11, background: 'rgba(255,255,255,0.08)', marginTop: 18, overflow: 'hidden'}}>
						<div style={{height: '100%', width: `${fill * 100}%`, background: `linear-gradient(90deg, ${card.color}, #FF8A5C)`, borderRadius: 11, boxShadow: `0 0 20px ${card.color}`}} />
					</div>
					<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 38, color: '#DCE6FF', marginTop: 14, textAlign: 'center'}}>{card.caption}</div>
				</div>
			</div>
		);
	}
	// stamp
	const s = card;
	const p = easeOut(interpolate(time, [s.start, s.start + 0.35], [0, 1], clamp));
	return (
		<div style={{position: 'absolute', top: s.y ?? 760, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: out * p}}>
			<div style={{transform: `scale(${1.4 - 0.4 * p}) rotate(-3deg)`, border: `5px solid ${s.color}`, borderRadius: 18, padding: '18px 40px', textAlign: 'center',
				background: 'rgba(6,10,20,0.75)', boxShadow: `0 0 50px ${s.color}66`}}>
				<div style={{fontFamily: DISPLAY, fontWeight: 800, fontSize: 70, color: s.color, letterSpacing: '0.06em'}}>{s.text}</div>
				{s.sub ? <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 24, letterSpacing: '0.22em', color: 'white', marginTop: 6}}>{s.sub}</div> : null}
			</div>
		</div>
	);
};

export const EndCard: React.FC<{e: NonNullable<ShowcaseProps['endCard']>; time: number}> = ({e, time}) => {
	if (time < e.start) return null;
	const p = easeOut(interpolate(time, [e.start, e.start + 0.6], [0, 1], clamp));
	const typed = Math.floor(interpolate(time, [e.start + 1.4, e.start + 2.4], [0, e.keyword.length], clamp));
	const reply = interpolate(time, [e.start + 2.7, e.start + 3.1], [0, 1], clamp);
	const phone = easeOut(interpolate(time, [e.start + 3.0, e.start + 3.6], [0, 1], clamp));
	const caret = Math.floor(time * 2.5) % 2 === 0;
	return (
		<AbsoluteFill style={{background: `rgba(3,6,13,${0.55 * p})`}}>
			<div style={{position: 'absolute', top: 560, left: 70, right: 70, opacity: p, transform: `translateY(${(1 - p) * 50}px)`}}>
				<div style={{fontFamily: SANS, fontWeight: 700, fontSize: 28, letterSpacing: '0.3em', color: GOLD, textAlign: 'center'}}>WANT THE DETAILS?</div>
				<div style={{fontFamily: DISPLAY, fontWeight: 800, fontSize: 88, color: 'white', textAlign: 'center', letterSpacing: '-0.03em', marginTop: 12}}>Comment</div>
				<div style={{...glass, marginTop: 30, padding: '26px 34px', display: 'flex', alignItems: 'center', gap: 20, borderRadius: 60}}>
					<div style={{width: 64, height: 64, borderRadius: 32, background: 'linear-gradient(135deg, #FFC940, #FF8A3D)'}} />
					<div style={{flex: 1, fontFamily: DISPLAY, fontWeight: 800, fontSize: 64, color: GOLD, letterSpacing: '0.06em'}}>
						{e.keyword.slice(0, typed)}<span style={{opacity: caret && typed < e.keyword.length + 1 ? 1 : 0, color: 'white'}}>|</span>
					</div>
					<div style={{fontFamily: SANS, fontWeight: 700, fontSize: 28, color: '#2F9BFF'}}>Post</div>
				</div>
				<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 44, color: '#DCE6FF', textAlign: 'center', marginTop: 26, opacity: reply}}>{e.detail}</div>
				<div style={{display: 'flex', justifyContent: 'center', marginTop: 40, opacity: phone, transform: `scale(${0.9 + 0.1 * phone})`}}>
					<div style={{background: GOLD, color: '#0A0F1C', fontFamily: DISPLAY, fontWeight: 800, fontSize: 52, padding: '18px 44px', borderRadius: 50,
						boxShadow: `0 0 50px ${GOLD}88`, letterSpacing: '0.02em'}}>{e.phone}</div>
				</div>
			</div>
		</AbsoluteFill>
	);
};

// ---------- Speaker ----------
export const Speaker: React.FC<{video: string; hide?: number[][]; time: number; fps: number}> = ({video, hide, time, fps}) => {
	let vis = 1;
	for (const [a, b] of hide ?? []) {
		vis = Math.min(vis, a <= time && time < b ? 0 : 1);
		if (time >= b && time < b + 0.35) vis = Math.min(vis, easeOut((time - b) / 0.35));
	}
	const intro = easeOut(interpolate(time, [0, 0.4], [0, 1], clamp));
	const s = vis * intro;
	return (
		<div style={{position: 'absolute', top: 270, right: 56, width: 250, height: 230, borderRadius: 26, overflow: 'hidden',
			border: '3px solid rgba(255,255,255,0.88)', boxShadow: `0 16px 40px rgba(0,0,0,0.55), 0 0 30px ${GOLD}33`,
			transform: `scale(${0.6 + 0.4 * s})`, opacity: s, transformOrigin: '100% 0%'}}>
			<OffthreadVideo src={staticFile(video)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
		</div>
	);
};

// ---------- Composition ----------
export const ShowcaseReel: React.FC<ShowcaseProps> = (props) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const time = frame / fps;
	const [data, setData] = useState<MapData | null>(null);
	const [handle] = useState(() => delayRender('map data'));
	useEffect(() => {
		fetch(staticFile(props.mapFile)).then((r) => r.json()).then((d) => { setData(d); continueRender(handle); });
	}, [props.mapFile, handle]);

	const layers = useMemo(() => {
		if (!data) return null;
		const out: Record<string, Record<string, Prepared>> = {};
		for (const level of ['fine', 'coarse'] as const) {
			out[level] = {};
			for (const [k, v] of Object.entries(data.base[level])) out[level][k] = prepare(v);
		}
		return out;
	}, [data]);
	const features = useMemo(() => props.features.map((f) => (f.lines ? prepare(f.lines) : [])), [props.features]);

	if (!layers) return <AbsoluteFill style={{background: SEA}} />;
	const cam = cameraAt(props.camera, time);
	const proj = makeProjector(cam);
	const wideKm = W / cam.scale / 1000;
	const level = wideKm > 22 ? 'coarse' : 'fine';
	const sweep = (time * 0.22) % 1;
	const grain = (frame * 37) % 200;

	return (
		<AbsoluteFill style={{background: `radial-gradient(130% 90% at 50% 60%, #071022 0%, ${SEA} 70%)`, overflow: 'hidden'}}>
			<BaseMap layers={layers[level]} proj={proj} cam={cam} time={time} />
			{props.features.map((f, i) => <FeatureLayer key={i} f={f} prepared={features[i]} proj={proj} time={time} />)}
			{/* Haze toward the horizon, and a slow light sweep across the map. */}
			<div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 760, background: `linear-gradient(${SEA} 18%, rgba(3,6,13,0.75) 45%, rgba(3,6,13,0))`}} />
			<div style={{position: 'absolute', left: '-50%', width: '60%', top: 0, bottom: 0, transform: `translateX(${sweep * 330}%) skewX(-18deg)`,
				background: 'linear-gradient(90deg, rgba(120,170,255,0), rgba(120,170,255,0.05), rgba(120,170,255,0))'}} />
			{props.features.map((f, i) => <LabelPin key={i} f={f} proj={proj} time={time} />)}
			<div style={{position: 'absolute', inset: 0, background: 'radial-gradient(120% 85% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.6) 100%)'}} />
			<div style={{position: 'absolute', inset: 0, opacity: 0.05, backgroundImage: `url(${staticFile('mr1/grain.png')})`, backgroundPosition: `${grain}px ${grain * 1.7}px`}} />
			{props.headlines?.map((h, i) => <HeadlineView key={i} h={h} time={time} />)}
			{props.cards?.map((c, i) => <CardView key={i} card={c} time={time} />)}
			{props.endCard ? <EndCard e={props.endCard} time={time} /> : null}
			{props.noScrim ? null : <div style={{position: 'absolute', left: 0, right: 0, top: 1180, height: 520, background: 'linear-gradient(rgba(3,6,13,0), rgba(3,6,13,0.72) 40%, rgba(3,6,13,0.72) 70%, rgba(3,6,13,0))', pointerEvents: 'none'}} />}
			<Captions captions={props.captions} time={time} />
			{props.disclaimer?.filter((d) => time >= d.start && time < d.end).map((d, i) => (
				<div key={i} style={{position: 'absolute', top: 1530, left: 120, right: 120, textAlign: 'center', fontFamily: SANS, fontWeight: 700, fontSize: 20,
					letterSpacing: '0.08em', color: 'rgba(255,255,255,0.7)'}}>{d.text}</div>
			))}
			{props.speaker ? <Speaker video={props.speaker.video} hide={props.speaker.hide} time={time} fps={fps} /> : null}
			<div style={{position: 'absolute', bottom: 70, left: 60, fontFamily: SANS, fontWeight: 500, fontSize: 15, color: 'rgba(255,255,255,0.5)'}}>{props.credit}</div>
			{props.voice ? <Audio src={staticFile(props.voice)} /> : null}
			{props.music ? <Audio src={staticFile(props.music.file)} volume={props.music.volume} /> : null}
			{props.sounds?.map((s, i) => (
				<Sequence key={i} from={Math.round(s.at * fps)}>
					<Audio src={staticFile(s.file)} volume={s.volume ?? 0.4} />
				</Sequence>
			))}
		</AbsoluteFill>
	);
};
