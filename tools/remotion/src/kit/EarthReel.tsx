import React from 'react';
import {AbsoluteFill, Audio, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {EarthFrame, earthProjector} from './earthCamera';
import {Count, CountCard, Label, Pill, PillCaption, Shape, ShapeLayer} from './MapReel';
import {Sound} from './styles';

export type EarthReelProps = {
	durationSeconds: number;
	handle: string;
	earth: {video: string; frames: EarthFrame[]; credit: string};
	shapes: Shape[];
	captions: PillCaption[];
	counts?: CountCard[];
	speaker?: string;
	speakerStart?: number;
	sounds?: Sound[];
	music?: {file: string; volume: number};
};

// Matches the Earth Studio render setting (Custom, X 80, Y 360, Left), so the source credit sits under Google's logo.
const CREDIT_LEFT = 108;

// Google's watermark is burned into each rendered frame, so these layers must stay clear of it.
export const EarthReel: React.FC<EarthReelProps> = (props) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const time = frame / fps;
	const camera = props.earth.frames[Math.min(frame, props.earth.frames.length - 1)];
	const place = earthProjector(camera, width, height);
	return (
		<AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
			<OffthreadVideo src={staticFile(props.earth.video)} muted style={{width: '100%', height: '100%'}} />
			<svg width={width} height={height} style={{position: 'absolute', left: 0, top: 0}}>
				{props.shapes.map((shape, i) => <ShapeLayer key={i} shape={shape} place={place} zoom={1} time={time} />)}
			</svg>
			{props.shapes.map((shape, i) => <Label key={i} shape={shape} place={place} time={time} />)}
			{props.speaker ? (
				<div style={{position: 'absolute', top: '15.5%', right: 70, width: 286, height: 286, borderRadius: 28, overflow: 'hidden', border: '4px solid rgba(255,255,255,0.75)', boxShadow: '0 10px 30px rgba(0,0,0,0.3)'}}>
					<OffthreadVideo src={staticFile(props.speaker)} startFrom={Math.round((props.speakerStart ?? 0) * fps)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
				</div>
			) : null}
			{props.counts?.map((card, i) => <Count key={i} card={card} time={time} />)}
			<Pill time={time} captions={props.captions} />
			<div style={{position: 'absolute', top: '77%', left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
				<div style={{background: 'rgba(255,255,255,0.92)', borderRadius: 20, padding: '6px 18px', fontFamily: 'Inter Tight', fontWeight: 700, fontSize: 22, color: '#222'}}>@{props.handle}</div>
			</div>
			<div style={{position: 'absolute', top: '17.3%', left: CREDIT_LEFT, width: '42%', fontFamily: 'Inter Tight', fontWeight: 700, fontSize: 15, lineHeight: 1.3, color: 'rgba(255,255,255,0.95)', textShadow: '0 1px 4px rgba(0,0,0,0.85)'}}>{props.earth.credit}</div>
			{props.music ? <Audio src={staticFile(props.music.file)} volume={props.music.volume} /> : null}
			{props.sounds?.map((sound, i) => (
				<Sequence key={i} from={Math.round(sound.at * fps)}>
					<Audio src={staticFile(sound.file)} volume={sound.volume ?? 0.4} />
				</Sequence>
			))}
		</AbsoluteFill>
	);
};
