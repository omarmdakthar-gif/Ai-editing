import React, {useEffect, useMemo, useState} from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, continueRender, delayRender, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import '@fontsource/inter-tight/500.css';
import '@fontsource/inter-tight/700.css';
import '@fontsource/sora/800.css';
import '@fontsource/instrument-serif/400-italic.css';
import {Card, CardView, CaptionLine, Captions, EndCard, Headline, HeadlineView, Speaker, glass} from './ShowcaseReel';
import {Sound} from './styles';

// A story reel built from scenes on a timeline: a glowing world map with money flowing between cities,
// a card reveal, a profit dial, a bank/network diagram, pre-rendered map clips and still renders with camera moves.

const W = 1080;
const H = 1920;
const SANS = 'Inter Tight';
const SERIF = 'Instrument Serif';
const DISPLAY = 'Sora';
const GOLD = '#FFC940';
const SEA = '#03060D';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const easeOut = (x: number) => 1 - (1 - x) ** 3;
const easeInOut = (x: number) => (x < 0.5 ? 4 * x * x * x : 1 - (-2 * x + 2) ** 3 / 2);

type WorldCam = {t: number; lon: number; lat: number; zoom: number};
export type Scene =
	| {kind: 'world'; start: number; end: number; camera: WorldCam[]; busy?: number[]; fees?: number[]}
	| {kind: 'wallet'; start: number; end: number; revealAt: number}
	| {kind: 'profit'; start: number; end: number; source: string}
	| {kind: 'bank'; start: number; end: number; steps: number[]}
	| {kind: 'video'; start: number; end: number; src: string; from?: number}
	| {kind: 'image'; start: number; end: number; src: string; zoom?: number[]; pan?: number[][]; title?: {kicker: string; lines: string[]}};
export type StoryProps = {
	durationSeconds: number;
	scenes: Scene[];
	captions: CaptionLine[];
	headlines?: Headline[];
	cards?: Card[];
	speaker: {video: string; hide?: number[][]};
	// Full-screen speaker at the start; it shrinks into the corner box over 0.45 s from `end`.
	speakerIntro?: {video: string; end: number};
	// Logos that appear behind the cut-out speaker during the full-screen hook. `src` 'oil' draws an oil-drop icon.
	hookLogos?: {person: string; items: {src: string; at: number; x: number; y: number; width: number; strike?: boolean}[]};
	voice: string;
	music?: {file: string; volume: number};
	sounds?: Sound[];
	endCard: {start: number; keyword: string; phone: string; detail: string};
	credits?: {start: number; end: number; text: string}[];
};

const fade = (time: number, s: {start: number; end: number}, d = 0.35) =>
	interpolate(time, [s.start - d, s.start, s.end, s.end + d], [0, 1, 1, 0], clamp);

// ---------- World map ----------
const HUBS: Record<string, number[]> = {
	ny: [-74.0, 40.7], london: [-0.13, 51.5], dubai: [55.27, 25.2], mumbai: [72.88, 19.08], singapore: [103.8, 1.35], tokyo: [139.7, 35.7],
	saopaulo: [-46.6, -23.5], lagos: [3.4, 6.5], sydney: [151.2, -33.9], frankfurt: [8.68, 50.1], hongkong: [114.2, 22.3], la: [-118.2, 34.0],
	toronto: [-79.4, 43.7], johannesburg: [28.0, -26.2], paris: [2.35, 48.85], chennai: [80.27, 13.08], riyadh: [46.7, 24.7], mexico: [-99.1, 19.4],
};
const ROUTES = [
	['ny', 'london'], ['london', 'dubai'], ['dubai', 'mumbai'], ['mumbai', 'singapore'], ['singapore', 'tokyo'], ['la', 'tokyo'], ['ny', 'saopaulo'],
	['london', 'lagos'], ['singapore', 'sydney'], ['frankfurt', 'dubai'], ['hongkong', 'london'], ['toronto', 'paris'], ['dubai', 'chennai'],
	['johannesburg', 'dubai'], ['riyadh', 'london'], ['mexico', 'ny'], ['paris', 'singapore'], ['la', 'ny'], ['dubai', 'hongkong'], ['saopaulo', 'lagos'],
	['chennai', 'singapore'], ['frankfurt', 'ny'], ['tokyo', 'sydney'], ['mumbai', 'london'],
];

const worldCamAt = (keys: WorldCam[], t: number) => {
	if (t <= keys[0].t) return keys[0];
	const i = keys.findIndex((k) => k.t > t);
	if (i === -1) return keys[keys.length - 1];
	const a = keys[i - 1];
	const b = keys[i];
	const p = easeInOut((t - a.t) / (b.t - a.t));
	return {t, lon: a.lon + (b.lon - a.lon) * p, lat: a.lat + (b.lat - a.lat) * p, zoom: a.zoom * (b.zoom / a.zoom) ** p};
};

const WorldScene: React.FC<{scene: Extract<Scene, {kind: 'world'}>; rings: number[][][]; time: number}> = ({scene, rings, time}) => {
	const cam = worldCamAt(scene.camera, time);
	const k = (W / 360) * cam.zoom; // pixels per degree
	const proj = (p: number[]) => [W / 2 + (p[0] - cam.lon) * k, H * 0.46 - (p[1] - cam.lat) * k * 1.12];
	const land = rings.map((r) => 'M' + r.map((p) => proj(p).map((v) => v.toFixed(1)).join(' ')).join('L') + 'Z').join('');
	// How many routes are live: grows with the 'busy' ramp [t0, t1].
	const busy = scene.busy ? interpolate(time, scene.busy, [3, ROUTES.length], clamp) : 3;
	const arcs = ROUTES.slice(0, Math.round(busy)).map(([a, b], i) => {
		const pa = proj(HUBS[a]);
		const pb = proj(HUBS[b]);
		const mx = (pa[0] + pb[0]) / 2;
		const my = (pa[1] + pb[1]) / 2 - Math.hypot(pb[0] - pa[0], pb[1] - pa[1]) * 0.32;
		const d = `M${pa[0]} ${pa[1]}Q${mx} ${my} ${pb[0]} ${pb[1]}`;
		const speed = 0.45 + (i % 5) * 0.08;
		const phase = (time * speed + i * 0.37) % 1;
		const q = (u: number) => [(1 - u) ** 2 * pa[0] + 2 * (1 - u) * u * mx + u * u * pb[0], (1 - u) ** 2 * pa[1] + 2 * (1 - u) * u * my + u * u * pb[1]];
		const dots = [phase, (phase + 0.5) % 1].map((u) => q(u));
		return {d, dots, i};
	});
	const cities = Object.entries(HUBS).map(([name, p]) => ({name, p: proj(p)}));
	const pulse = (time * 1.4) % 1;
	return (
		<AbsoluteFill style={{background: `radial-gradient(120% 80% at 50% 45%, #0A1630 0%, ${SEA} 70%)`}}>
			<svg width={W} height={H} style={{position: 'absolute'}}>
				<defs>
					<pattern id="wgrid" width="54" height="54" patternUnits="userSpaceOnUse"><path d="M54 0H0V54" fill="none" stroke="rgba(90,130,220,0.06)" strokeWidth="1" /></pattern>
				</defs>
				<rect width={W} height={H} fill="url(#wgrid)" />
				<path d={land} fill="#0E1A33" stroke="#4FA8FF" strokeOpacity={0.55} strokeWidth={1.2} />
			</svg>
			<svg width={W} height={H} style={{position: 'absolute', filter: 'blur(8px)'}}>
				{arcs.map((a) => <path key={a.i} d={a.d} fill="none" stroke={GOLD} strokeOpacity={0.45} strokeWidth={6} />)}
			</svg>
			<svg width={W} height={H} style={{position: 'absolute'}}>
				{arcs.map((a) => <path key={a.i} d={a.d} fill="none" stroke={GOLD} strokeOpacity={0.75} strokeWidth={1.8} />)}
				{arcs.flatMap((a) => a.dots.map(([x, y], j) => <circle key={`${a.i}-${j}`} cx={x} cy={y} r={5} fill="#FFF3C4" style={{filter: `drop-shadow(0 0 8px ${GOLD})`}} />))}
				{cities.map((c) => (
					<g key={c.name}>
						<circle cx={c.p[0]} cy={c.p[1]} r={6 + pulse * 22} fill="none" stroke={GOLD} strokeOpacity={(1 - pulse) * 0.6} strokeWidth={2} />
						<circle cx={c.p[0]} cy={c.p[1]} r={5} fill={GOLD} />
					</g>
				))}
			</svg>
			{/* Swipe fees: a small "+fee" chip pops at a few cities on each beat. */}
			{(scene.fees ?? []).map((t0, i) => {
				if (time < t0 || time > t0 + 1.1) return null;
				const c = cities[(i * 5 + 2) % cities.length];
				const p = interpolate(time, [t0, t0 + 1.1], [0, 1], clamp);
				return (
					<div key={i} style={{position: 'absolute', left: c.p[0], top: c.p[1] - 30 - p * 60, transform: 'translateX(-50%)', opacity: 1 - p,
						background: GOLD, color: '#120E02', fontFamily: SANS, fontWeight: 700, fontSize: 24, padding: '4px 12px', borderRadius: 8}}>+ fee</div>
				);
			})}
		</AbsoluteFill>
	);
};

// ---------- Wallet and card ----------
const CardFace: React.FC<{width: number}> = ({width}) => (
	<div style={{width, height: width * 0.63, borderRadius: width * 0.055, position: 'relative', overflow: 'hidden',
		background: 'linear-gradient(135deg, #1B2A55 0%, #0B1226 55%, #2A1E05 100%)', border: '1.5px solid rgba(255,255,255,0.25)',
		boxShadow: `0 30px 80px rgba(0,0,0,0.6), 0 0 60px ${GOLD}33`}}>
		<div style={{position: 'absolute', inset: 0, background: 'linear-gradient(115deg, rgba(255,255,255,0) 30%, rgba(255,255,255,0.14) 45%, rgba(255,255,255,0) 60%)'}} />
		<div style={{position: 'absolute', left: width * 0.08, top: width * 0.2, width: width * 0.14, height: width * 0.105, borderRadius: 8,
			background: 'linear-gradient(135deg, #F7D774, #B38A2E)'}} />
		<div style={{position: 'absolute', left: width * 0.08, top: width * 0.37, fontFamily: SANS, fontWeight: 500, fontSize: width * 0.06, letterSpacing: '0.12em', color: 'rgba(255,255,255,0.85)'}}>
			•••• •••• •••• 2026
		</div>
		<div style={{position: 'absolute', right: width * 0.08, bottom: width * 0.06, fontFamily: DISPLAY, fontWeight: 800, fontStyle: 'italic', fontSize: width * 0.12, color: 'white', letterSpacing: '0.02em'}}>
			VISA
		</div>
	</div>
);

const WalletScene: React.FC<{scene: Extract<Scene, {kind: 'wallet'}>; time: number}> = ({scene, time}) => {
	const open = easeOut(interpolate(time, [scene.start + 0.2, scene.start + 1.0], [0, 1], clamp));
	const rise = easeOut(interpolate(time, [scene.revealAt - 0.6, scene.revealAt + 0.3], [0, 1], clamp));
	const flash = interpolate(time, [scene.revealAt, scene.revealAt + 0.15, scene.revealAt + 0.6], [0, 1, 0], clamp);
	return (
		<AbsoluteFill style={{background: `radial-gradient(90% 60% at 50% 55%, #14223F 0%, ${SEA} 75%)`}}>
			<div style={{position: 'absolute', left: '50%', top: 1080, transform: `translate(-50%, ${-rise * 330}px) rotate(${-6 + rise * 6}deg) scale(${0.9 + rise * 0.25})`}}>
				<CardFace width={620} />
			</div>
			{/* Wallet: a leather pocket the card rises out of. */}
			<div style={{position: 'absolute', left: '50%', top: 1150, width: 760, height: 520, transform: 'translateX(-50%)', borderRadius: 40,
				background: 'linear-gradient(180deg, #3A2414, #22140A)', boxShadow: '0 40px 90px rgba(0,0,0,0.7), inset 0 2px 0 rgba(255,255,255,0.08)'}}>
				<div style={{position: 'absolute', left: 30, right: 30, top: 34, height: 6, borderRadius: 3, background: 'rgba(255,220,170,0.15)'}} />
				<div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 120, borderRadius: '40px 40px 0 0', transformOrigin: '50% 0%',
					transform: `perspective(900px) rotateX(${-open * 110}deg)`, background: 'linear-gradient(180deg, #4A2E1A, #2C1A0D)'}} />
			</div>
			<AbsoluteFill style={{background: 'white', opacity: flash * 0.5}} />
		</AbsoluteFill>
	);
};

// ---------- Profit dial ----------
const ProfitScene: React.FC<{scene: Extract<Scene, {kind: 'profit'}>; time: number}> = ({scene, time}) => {
	const p = 0.5 * easeOut(interpolate(time, [scene.start + 0.3, scene.start + 1.6], [0, 1], clamp));
	const R = 250;
	const C = 2 * Math.PI * R;
	const cents = Math.round(p * 100);
	return (
		<AbsoluteFill style={{background: `radial-gradient(90% 60% at 50% 50%, #14223F 0%, ${SEA} 75%)`}}>
			<div style={{position: 'absolute', top: 545, left: 0, right: 0, textAlign: 'center', fontFamily: SANS, fontWeight: 700, fontSize: 28, letterSpacing: '0.3em', color: GOLD}}>
				OF EVERY $1 VISA EARNS
			</div>
			<svg width={W} height={760} style={{position: 'absolute', top: 650}}>
				<circle cx={W / 2} cy={380} r={R} fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth={56} />
				<circle cx={W / 2} cy={380} r={R} fill="none" stroke={GOLD} strokeWidth={56} strokeDasharray={`${C * p} ${C}`} transform={`rotate(-90 ${W / 2} 380)`}
					style={{filter: `drop-shadow(0 0 24px ${GOLD}88)`}} strokeLinecap="butt" />
			</svg>
			<div style={{position: 'absolute', top: 900, left: 0, right: 0, textAlign: 'center'}}>
				<div style={{fontFamily: DISPLAY, fontWeight: 800, fontSize: 150, color: 'white', lineHeight: 1, fontVariantNumeric: 'tabular-nums'}}>{cents}¢</div>
				<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 52, color: '#DCE6FF', marginTop: 6}}>is net profit</div>
			</div>
			<div style={{position: 'absolute', top: 612, left: 120, right: 120, textAlign: 'center', fontFamily: SANS, fontWeight: 700, fontSize: 19, letterSpacing: '0.1em',
				color: 'rgba(255,255,255,0.55)'}}>{scene.source}</div>
		</AbsoluteFill>
	);
};

// ---------- Bank / network diagram ----------
const Node: React.FC<{x: number; y: number; title: string; sub?: string; color: string; on: number; glow?: number}> = ({x, y, title, sub, color, on, glow = 0}) => (
	<div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%, -50%) scale(${0.85 + 0.15 * on})`, opacity: on}}>
		<div style={{...glass, padding: '26px 34px', minWidth: 260, textAlign: 'center', borderColor: color, boxShadow: `0 0 ${20 + glow * 50}px ${color}${glow ? 'AA' : '44'}, 0 30px 80px rgba(0,0,0,0.5)`}}>
			<div style={{fontFamily: DISPLAY, fontWeight: 800, fontSize: 52, color: 'white', letterSpacing: '0.04em'}}>{title}</div>
			{sub ? <div style={{fontFamily: SANS, fontWeight: 500, fontSize: 24, color: 'rgba(255,255,255,0.75)', marginTop: 6}}>{sub}</div> : null}
		</div>
	</div>
);

const BankScene: React.FC<{scene: Extract<Scene, {kind: 'bank'}>; time: number}> = ({scene, time}) => {
	const [s1, s2, s3] = scene.steps;
	const on = (t: number) => easeOut(interpolate(time, [t, t + 0.4], [0, 1], clamp));
	const travel = (t: number) => easeInOut(interpolate(time, [t + 0.3, t + 1.3], [0, 1], clamp));
	const bank = {x: 290, y: 1020};
	const you = {x: 790, y: 1020};
	const visa = {x: 540, y: 660};
	const item = (t: number, label: string, y: number) => {
		const p = travel(t);
		if (time < t) return null;
		return (
			<div style={{position: 'absolute', left: bank.x + (you.x - bank.x) * p, top: y, transform: 'translate(-50%, -50%)',
				background: GOLD, color: '#120E02', fontFamily: SANS, fontWeight: 700, fontSize: 26, padding: '8px 16px', borderRadius: 10, whiteSpace: 'nowrap'}}>{label}</div>
		);
	};
	return (
		<AbsoluteFill style={{background: `radial-gradient(90% 60% at 50% 50%, #14223F 0%, ${SEA} 75%)`}}>
			<svg width={W} height={H} style={{position: 'absolute'}}>
				<line x1={bank.x} y1={bank.y} x2={you.x} y2={you.y} stroke="rgba(255,255,255,0.25)" strokeWidth={3} strokeDasharray="8 10" />
				<line x1={visa.x} y1={visa.y + 70} x2={540} y2={bank.y - 10} stroke={GOLD} strokeOpacity={0.5 * on(s3)} strokeWidth={3} />
			</svg>
			<Node x={bank.x} y={bank.y} title="BANK" sub="issues cards, gives loans" color="#6C8CFF" on={on(s1)} />
			<Node x={you.x} y={you.y} title="YOU" color="#FFFFFF" on={on(s1)} />
			{item(s1, 'Debit / credit card', 1140)}
			{item(s2, 'Loan', 1210)}
			<Node x={visa.x} y={visa.y} title="VISA" sub="the network in between" color={GOLD} on={on(s3)} glow={on(s3)} />
			{time > s3 + 0.5 ? (
				<div style={{position: 'absolute', top: 830, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 18, opacity: on(s3 + 0.5)}}>
					{['No card to issue', 'No loans', 'No credit risk'].map((t) => (
						<div key={t} style={{border: `2px solid ${GOLD}`, color: GOLD, fontFamily: SANS, fontWeight: 700, fontSize: 24, padding: '8px 14px', borderRadius: 10}}>{t}</div>
					))}
				</div>
			) : null}
		</AbsoluteFill>
	);
};

// ---------- Still render with a slow camera move ----------
const ImageScene: React.FC<{scene: Extract<Scene, {kind: 'image'}>; time: number}> = ({scene, time}) => {
	const p = interpolate(time, [scene.start, scene.end], [0, 1], clamp);
	const [z0, z1] = scene.zoom ?? [1.0, 1.12];
	const [[x0, y0], [x1, y1]] = scene.pan ?? [[0, 0], [0, 0]];
	const z = z0 + (z1 - z0) * p;
	const titleIn = easeOut(interpolate(time, [scene.start + 0.2, scene.start + 0.8], [0, 1], clamp));
	return (
		<AbsoluteFill style={{background: SEA, overflow: 'hidden'}}>
			<Img src={staticFile(scene.src)} style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover',
				transform: `scale(${z}) translate(${(x0 + (x1 - x0) * p) * 100}%, ${(y0 + (y1 - y0) * p) * 100}%)`}} />
			<div style={{position: 'absolute', inset: 0, background: 'linear-gradient(rgba(3,6,13,0.55), rgba(3,6,13,0) 30%, rgba(3,6,13,0) 55%, rgba(3,6,13,0.75))'}} />
			{scene.title ? (
				<div style={{position: 'absolute', top: 560, left: 64, right: 64, textAlign: 'center', opacity: titleIn, transform: `translateY(${(1 - titleIn) * 30}px)`}}>
					<div style={{fontFamily: SANS, fontWeight: 700, fontSize: 26, letterSpacing: '0.32em', color: GOLD}}>{scene.title.kicker}</div>
					{scene.title.lines.map((l, i) => (
						<div key={i} style={{fontFamily: SERIF, fontSize: i === 0 ? 92 : 64, lineHeight: 1.0, color: 'white', marginTop: i === 0 ? 14 : 4,
							textShadow: '0 6px 30px rgba(0,0,0,0.6)', letterSpacing: i === 0 ? '0.02em' : '0.08em'}}>{l}</div>
					))}
				</div>
			) : null}
		</AbsoluteFill>
	);
};

// ---------- Composition ----------
export const StoryReel: React.FC<StoryProps> = (props) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const time = frame / fps;
	const [rings, setRings] = useState<number[][][] | null>(null);
	const [handle] = useState(() => delayRender('world data'));
	useEffect(() => {
		fetch(staticFile('rk/world.json')).then((r) => r.json()).then((d) => { setRings(d); continueRender(handle); });
	}, [handle]);
	const scenes = useMemo(() => props.scenes, [props.scenes]);
	if (!rings) return <AbsoluteFill style={{background: SEA}} />;
	const grain = (frame * 37) % 200;
	return (
		<AbsoluteFill style={{background: SEA, overflow: 'hidden'}}>
			{scenes.map((s, i) => {
				const o = fade(time, s);
				if (o <= 0) return null;
				let body: React.ReactNode = null;
				if (s.kind === 'world') body = <WorldScene scene={s} rings={rings} time={time} />;
				if (s.kind === 'wallet') body = <WalletScene scene={s} time={time} />;
				if (s.kind === 'profit') body = <ProfitScene scene={s} time={time} />;
				if (s.kind === 'bank') body = <BankScene scene={s} time={time} />;
				if (s.kind === 'image') body = <ImageScene scene={s} time={time} />;
				if (s.kind === 'video') body = (
					<Sequence from={Math.round(s.start * fps)} layout="none">
						<OffthreadVideo src={staticFile(s.src)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
					</Sequence>
				);
				return <AbsoluteFill key={i} style={{opacity: o}}>{body}</AbsoluteFill>;
			})}
			{props.speakerIntro && time < props.speakerIntro.end + 0.5 ? (() => {
				const e = props.speakerIntro.end;
				const p = easeInOut(interpolate(time, [e, e + 0.45], [0, 1], clamp));
				const mix = (a: number, b: number) => a + (b - a) * p;
				return (
					<div style={{position: 'absolute', left: mix(0, W - 56 - 250), top: mix(0, 270), width: mix(W, 250), height: mix(H, 230), borderRadius: mix(0, 26),
						overflow: 'hidden', border: `${mix(0, 3)}px solid rgba(255,255,255,${0.88 * p})`, boxShadow: `0 16px 40px rgba(0,0,0,${0.55 * p})`}}>
						<OffthreadVideo src={staticFile(props.speakerIntro.video)} muted style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', objectPosition: '50% 38%'}} />
						{props.hookLogos ? (
							<>
								{props.hookLogos.items.map((it, i) => {
									const pop = easeOut(interpolate(time, [it.at, it.at + 0.35], [0, 1], clamp));
									const strike = easeOut(interpolate(time, [it.at + 0.3, it.at + 0.6], [0, 1], clamp));
									const out = 1 - p;
									if (time < it.at) return null;
									return (
										<div key={i} style={{position: 'absolute', left: it.x, top: it.y, width: it.width, transform: `translate(-50%, -50%) scale(${0.7 + 0.3 * pop})`, opacity: pop * out}}>
											{it.src === 'oil' ? (
												<svg viewBox="0 0 100 130" width={it.width} style={{display: 'block', filter: 'drop-shadow(0 10px 30px rgba(0,0,0,0.5))'}}>
													<path d="M50 4 C50 4 10 58 10 84 a40 40 0 0 0 80 0 C90 58 50 4 50 4Z" fill="#14161C" stroke="#E8C15A" strokeWidth="4" />
													<text x="50" y="96" textAnchor="middle" fontFamily={SANS} fontWeight={700} fontSize="20" fill="#E8C15A">OIL</text>
												</svg>
											) : (
												<Img src={staticFile(it.src)} style={{width: '100%', display: 'block', filter: 'drop-shadow(0 10px 30px rgba(0,0,0,0.55))'}} />
											)}
											{it.strike ? (
												<div style={{position: 'absolute', left: '-12%', top: '50%', height: 12, width: `${124 * strike}%`, background: '#FF3B4E', borderRadius: 6,
													transform: 'rotate(-18deg)', transformOrigin: '0 50%', boxShadow: '0 0 20px rgba(255,59,78,0.7)'}} />
											) : null}
										</div>
									);
								})}
								<OffthreadVideo src={staticFile(props.hookLogos.person)} muted transparent style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover'}} />
							</>
						) : null}
						<div style={{position: 'absolute', inset: 0, background: 'linear-gradient(rgba(3,6,13,0.45), rgba(3,6,13,0) 28%, rgba(3,6,13,0) 55%, rgba(3,6,13,0.55))', opacity: 1 - p}} />
					</div>
				);
			})() : null}
			<div style={{position: 'absolute', inset: 0, background: 'radial-gradient(120% 85% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)'}} />
			<div style={{position: 'absolute', inset: 0, opacity: 0.05, backgroundImage: `url(${staticFile('mr1/grain.png')})`, backgroundPosition: `${grain}px ${grain * 1.7}px`}} />
			{props.headlines?.map((h, i) => <HeadlineView key={i} h={h} time={time} />)}
			{props.cards?.map((c, i) => <CardView key={i} card={c} time={time} />)}
			<EndCard e={props.endCard} time={time} />
			<div style={{position: 'absolute', left: 0, right: 0, top: 1180, height: 520, background: 'linear-gradient(rgba(3,6,13,0), rgba(3,6,13,0.72) 40%, rgba(3,6,13,0.72) 70%, rgba(3,6,13,0))'}} />
			<Captions captions={props.captions} time={time} />
			{props.credits?.filter((c) => time >= c.start && time < c.end).map((c, i) => (
				<div key={i} style={{position: 'absolute', bottom: 70, left: 60, right: 60, fontFamily: SANS, fontWeight: 500, fontSize: 15, color: 'rgba(255,255,255,0.55)'}}>{c.text}</div>
			))}
			<Speaker video={props.speaker.video} hide={props.speaker.hide} time={time} fps={fps} />
			<Audio src={staticFile(props.voice)} />
			{props.music ? <Audio src={staticFile(props.music.file)} volume={props.music.volume} /> : null}
			{props.sounds?.map((s, i) => (
				<Sequence key={i} from={Math.round(s.at * fps)}>
					<Audio src={staticFile(s.file)} volume={s.volume ?? 0.4} />
				</Sequence>
			))}
		</AbsoluteFill>
	);
};
