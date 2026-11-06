import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import '@fontsource/inter-tight/700.css';
import '@fontsource/instrument-serif/400-italic.css';
import {Bounds, Camera, SCREEN, cameraAt, centroid, planeTransform, project, toMapPixels} from './mapMath';
import {Sound} from './styles';

export const MAP_COLOURS = {plot: '#D45CF0', palm: '#45E8EC', green: '#4FD08A', blue: '#6C8CFF', red: '#FF5C70', amber: '#F5B042', beach: '#BDF23C'};

export type Shape = {
	kind: 'area' | 'line';
	lines: number[][][];
	color: string;
	start: number;
	end?: number;
	drawSeconds?: number;
	label?: string;
	chip?: string;
	anchor?: number[];
};
type CaptionWord = {text: string; start: number; accent?: boolean};
export type PillCaption = {end: number; words: CaptionWord[]};
export type CountCard = {start: number; end: number; value: number; prefix?: string; unit: string; color?: string};

export type MapReelProps = {
	durationSeconds: number;
	handle: string;
	map: Bounds & {image: string; credit: string; grade?: string};
	camera: Camera[];
	shapes: Shape[];
	captions: PillCaption[];
	counts?: CountCard[];
	speaker?: string;
	speakerStart?: number;
	sounds?: Sound[];
	music?: {file: string; volume: number};
};

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const SANS = 'Inter Tight';
const SERIF = 'Instrument Serif';
// Sentinel-2 is pale over desert, so deepen it to match the richer imagery in the references.
const DEFAULT_GRADE = 'brightness(0.66) contrast(1.12) saturate(1.25)';

type Point = {x: number; y: number};

export const ShapeLayer: React.FC<{shape: Shape; place: (c: number[]) => Point; zoom: number; time: number}> = ({shape, place, zoom, time}) => {
	if (time < shape.start) return null;
	const draw = interpolate(time, [shape.start, shape.start + (shape.drawSeconds ?? 0.8)], [0, 1], clamp);
	const leave = shape.end === undefined ? 1 : interpolate(time, [shape.end, shape.end + 0.3], [1, 0.35], clamp);
	const fill = shape.kind === 'area' ? interpolate(draw, [0.5, 1], [0, 0.42], clamp) * leave : 0;
	const paths = shape.lines.map((line) => {
		const points = line.map(place);
		return `M${points.map((p) => `${p.x} ${p.y}`).join('L')}${shape.kind === 'area' ? 'Z' : ''}`;
	});
	const stroke = (width: number, color: string, opacity: number) =>
		paths.map((d, i) => (
			<path key={i} d={d} pathLength={1} fill="none" stroke={color} strokeOpacity={opacity * leave} strokeWidth={width / zoom}
				strokeLinecap="round" strokeLinejoin="round" strokeDasharray="1 1" strokeDashoffset={1 - draw} />
		));
	return (
		<>
			{shape.kind === 'area' ? paths.map((d, i) => <path key={i} d={d} fill={shape.color} fillOpacity={fill} />) : null}
			<g style={{filter: `blur(${9 / zoom}px)`}}>{stroke(24, shape.color, 0.75)}</g>
			{stroke(8, shape.color, 0.9)}
			{stroke(4, '#FFFFFF', 0.9)}
		</>
	);
};

export const Label: React.FC<{shape: Shape; place: (c: number[]) => Point; time: number}> = ({shape, place, time}) => {
	if (!shape.label || time < shape.start + 0.3) return null;
	const leave = shape.end === undefined ? 1 : interpolate(time, [shape.end, shape.end + 0.25], [1, 0], clamp);
	const opacity = interpolate(time, [shape.start + 0.3, shape.start + 0.5], [0, 1], clamp) * leave;
	const anchor = place(shape.anchor ?? centroid(shape.lines[0]));
	const rise = 90;
	return (
		<div style={{position: 'absolute', left: anchor.x, top: anchor.y, opacity}}>
			<div style={{position: 'absolute', left: -1, top: -rise, width: 2, height: rise, background: 'rgba(255,255,255,0.8)'}} />
			<div style={{position: 'absolute', left: -7, top: -7, width: 14, height: 14, borderRadius: 7, background: shape.color, border: '2px solid white'}} />
			<div style={{position: 'absolute', top: -rise - 40, transform: 'translateX(-50%)', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6}}>
				<div style={{background: 'white', color: '#111', fontFamily: SANS, fontWeight: 700, fontSize: 25, letterSpacing: '0.09em', padding: '8px 16px', borderRadius: 9, whiteSpace: 'nowrap', textTransform: 'uppercase'}}>
					{shape.label}
				</div>
				{shape.chip ? (
					<div style={{background: shape.color, color: 'white', fontFamily: SANS, fontWeight: 700, fontSize: 24, padding: '4px 14px', borderRadius: 8, whiteSpace: 'nowrap'}}>{shape.chip}</div>
				) : null}
			</div>
		</div>
	);
};

export const Pill: React.FC<{time: number; captions: PillCaption[]}> = ({time, captions}) => {
	const caption = captions.find((c) => time >= c.words[0].start && time < c.end);
	if (!caption) return null;
	return (
		<div style={{position: 'absolute', top: '67%', left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
			<div style={{background: 'rgba(32,38,74,0.92)', borderRadius: 40, padding: '13px 34px', display: 'flex', gap: 13, alignItems: 'baseline', boxShadow: '0 8px 24px rgba(0,0,0,0.3)'}}>
				{caption.words.map((word, i) => (
					<span key={i} style={{
						fontFamily: word.accent ? SERIF : SANS,
						fontStyle: word.accent ? 'italic' : 'normal',
						fontWeight: word.accent ? 400 : 700,
						fontSize: word.accent ? 48 : 41,
						color: word.accent ? '#C9D6FF' : 'white',
						opacity: interpolate(time, [word.start - 0.02, word.start + 0.12], [0.3, 1], clamp),
					}}>
						{word.text}
					</span>
				))}
			</div>
		</div>
	);
};

export const Count: React.FC<{card: CountCard; time: number}> = ({card, time}) => {
	if (time < card.start || time > card.end) return null;
	const value = Math.round(interpolate(time, [card.start, card.start + 0.9], [0, card.value], clamp));
	const opacity = interpolate(time, [card.start, card.start + 0.15, card.end - 0.2, card.end], [0, 1, 1, 0], clamp);
	return (
		<div style={{position: 'absolute', top: '52%', left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity}}>
			<div style={{background: 'white', borderRadius: 28, padding: '20px 72px 16px', textAlign: 'center', boxShadow: '0 14px 40px rgba(0,0,0,0.25)'}}>
				<div style={{fontFamily: SANS, fontWeight: 700, fontSize: 92, lineHeight: 1, color: '#111', fontVariantNumeric: 'tabular-nums'}}>{card.prefix ?? ''}{value.toLocaleString('en-US')}</div>
				<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 36, color: '#2F6BFF', marginTop: 6}}>{card.unit}</div>
				<div style={{height: 6, width: 130, margin: '8px auto 0', borderRadius: 3, background: card.color ?? MAP_COLOURS.plot}} />
			</div>
		</div>
	);
};

export const MapReel: React.FC<MapReelProps> = (props) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const time = frame / fps;
	const camera = cameraAt(props.camera, time);
	const {map} = props;
	return (
		<AbsoluteFill style={{background: '#16363A', overflow: 'hidden'}}>
			<AbsoluteFill style={{perspective: SCREEN.perspective, perspectiveOrigin: `${SCREEN.width / 2}px ${SCREEN.focusY}px`}}>
				<div style={{position: 'absolute', left: 0, top: 0, width: map.width, height: map.height, transformOrigin: '0 0', transform: planeTransform(camera, map)}}>
					<Img src={staticFile(map.image)} style={{position: 'absolute', width: map.width, height: map.height, filter: map.grade ?? DEFAULT_GRADE}} />
					<svg width={map.width} height={map.height} style={{position: 'absolute', overflow: 'visible'}}>
						{props.shapes.map((shape, i) => <ShapeLayer key={i} shape={shape} place={(c) => toMapPixels(c, map)} zoom={camera.zoom} time={time} />)}
					</svg>
				</div>
			</AbsoluteFill>
			{/* Fades the far edge of the tilted map into sea colour, so the image never shows a hard end. */}
			<div style={{position: 'absolute', left: 0, right: 0, top: 0, height: '34%', background: 'linear-gradient(#16363A 45%, rgba(22,54,58,0))'}} />
			{props.shapes.map((shape, i) => <Label key={i} shape={shape} place={(c) => project(c, camera, map)} time={time} />)}
			{props.speaker ? (
				<div style={{position: 'absolute', top: '15.5%', right: 70, width: 286, height: 286, borderRadius: 28, overflow: 'hidden', border: '4px solid rgba(255,255,255,0.75)', boxShadow: '0 10px 30px rgba(0,0,0,0.3)'}}>
					<OffthreadVideo src={staticFile(props.speaker)} startFrom={Math.round((props.speakerStart ?? 0) * fps)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
				</div>
			) : null}
			{props.counts?.map((card, i) => <Count key={i} card={card} time={time} />)}
			<Pill time={time} captions={props.captions} />
			<div style={{position: 'absolute', top: '78.5%', left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
				<div style={{background: 'rgba(255,255,255,0.92)', borderRadius: 20, padding: '6px 18px', fontFamily: SANS, fontWeight: 700, fontSize: 22, color: '#222'}}>@{props.handle}</div>
			</div>
			<div style={{position: 'absolute', top: '81.5%', left: 120, right: 120, textAlign: 'center', fontFamily: SANS, fontWeight: 700, fontSize: 15, lineHeight: 1.25, color: 'rgba(255,255,255,0.9)', textShadow: '0 1px 4px rgba(0,0,0,0.8)'}}>{map.credit}</div>
			{props.music ? <Audio src={staticFile(props.music.file)} volume={props.music.volume} /> : null}
			{props.sounds?.map((sound, i) => (
				<Sequence key={i} from={Math.round(sound.at * fps)}>
					<Audio src={staticFile(sound.file)} volume={sound.volume ?? 0.4} />
				</Sequence>
			))}
		</AbsoluteFill>
	);
};
