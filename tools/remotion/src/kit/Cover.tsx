import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, staticFile, useVideoConfig} from 'remotion';
import {EarthFrame, earthProjector} from './earthCamera';
import {ShapeLayer} from './MapReel';
import {ExplainerShape, GLASS, GlassLabel, STICKER, goldText} from './ExplainerReel';
import {VectorMap, VectorMapProps} from './VectorMap';

// A reel cover in the map-reel house style. Everything that matters sits inside the 4:5 area
// (y 285-1635 at 1080x1920) that Instagram shows on the profile grid.
export type CoverProps = {
	// Either a Google Earth frame (which must keep its credit) or a stylised OpenStreetMap map.
	earth?: {video: string; frames: EarthFrame[]; frame: number};
	vector?: VectorMapProps;
	credit: string;
	shapes: ExplainerShape[];
	person: string;
	kicker: string;
	title: string;
	chips: string[];
	handle: string;
	personSide?: 'left' | 'right';
};

const SANS = 'Plus Jakarta Sans';
const SERIF = 'Instrument Serif';

export const Cover: React.FC<CoverProps> = (props) => {
	const {width, height} = useVideoConfig();
	const earth = props.earth;
	const place = earth ? earthProjector(earth.frames[earth.frame], width, height) : null;
	return (
		<AbsoluteFill style={{background: '#0b0d16'}}>
			{props.vector ? <VectorMap {...props.vector} /> : null}
			{earth && place ? (
				<>
					<OffthreadVideo src={staticFile(earth.video)} startFrom={earth.frame} muted style={{width: '100%', height: '100%'}} />
					<svg width={width} height={height} style={{position: 'absolute', left: 0, top: 0}}>
						{props.shapes.map((shape, i) => <ShapeLayer key={i} shape={shape} place={place} zoom={1} time={99} />)}
					</svg>
					{props.shapes.map((shape, i) => <GlassLabel key={i} shape={shape} place={place} time={99} />)}
				</>
			) : null}
			{/* Darkens behind the title and the person so the type pops, without hiding the map. */}
			<div style={{position: 'absolute', left: 0, right: 0, top: 330, height: 480, background: 'linear-gradient(rgba(8,10,18,0), rgba(8,10,18,0.55) 35%, rgba(8,10,18,0.55) 65%, rgba(8,10,18,0))'}} />
			<div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 760, background: 'linear-gradient(rgba(8,10,18,0), rgba(8,10,18,0.7))'}} />
			<div style={{position: 'absolute', top: 410, left: 60, right: 60, textAlign: 'center'}}>
				<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 64, lineHeight: 1, ...goldText, filter: 'drop-shadow(0 4px 12px rgba(0,0,0,0.6))'}}>{props.kicker}</div>
				<div style={{fontFamily: SANS, fontWeight: 800, fontSize: 128, lineHeight: 1, letterSpacing: '-0.055em', color: 'white', marginTop: 8, whiteSpace: 'nowrap', textShadow: '0 8px 30px rgba(0,0,0,0.6)'}}>{props.title}</div>
				<div style={{display: 'flex', justifyContent: 'center', gap: 12, marginTop: 30, flexWrap: 'wrap'}}>
					{props.chips.map((chip, i) => (
						<div key={i} style={{...GLASS, borderRadius: 999, padding: '10px 24px', fontFamily: SANS, fontWeight: 800, fontSize: 32, color: 'white'}}>{chip}</div>
					))}
				</div>
			</div>
			{/* On the right, the cut edge of the source frame falls off-screen. */}
			<div style={{position: 'absolute', left: props.personSide === 'right' ? 250 : -150, top: 600, width: 900, height: 1600, filter: STICKER}}>
				<Img src={staticFile(props.person)} style={{width: '100%', height: '100%'}} />
			</div>
			<div style={earth ? {position: 'absolute', top: '17.3%', left: 108, width: '44%', fontFamily: SANS, fontWeight: 700, fontSize: 14, lineHeight: 1.3, color: 'rgba(255,255,255,0.88)', textShadow: '0 1px 4px rgba(0,0,0,0.85)'} : {position: 'absolute', bottom: 40, left: 50, fontFamily: SANS, fontWeight: 500, fontSize: 15, color: 'rgba(255,255,255,0.55)'}}>{props.credit}</div>
			<div style={{position: 'absolute', top: 1540, ...(props.personSide === 'right' ? {left: 70} : {right: 70}), fontFamily: SANS, fontWeight: 700, fontSize: 30, color: 'rgba(255,255,255,0.75)', textShadow: '0 2px 8px rgba(0,0,0,0.5)'}}>@{props.handle}</div>
		</AbsoluteFill>
	);
};
