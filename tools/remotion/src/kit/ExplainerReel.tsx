import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import '@fontsource/plus-jakarta-sans/500.css';
import '@fontsource/plus-jakarta-sans/700.css';
import '@fontsource/plus-jakarta-sans/800.css';
import '@fontsource/instrument-serif/400-italic.css';
import {EarthFrame, earthProjector} from './earthCamera';
import {PillCaption, Shape, ShapeLayer} from './MapReel';
import {Sound} from './styles';

// A map explainer that cuts between full-screen talking shots and several Earth Studio shots.
// Times are seconds on the reel's timeline; `from` is seconds into the source.
export type Clip =
	| {kind: 'speaker'; start: number; end: number; video: string; from: number}
	| {kind: 'earth'; start: number; end: number; earth: string; from: number; cutout?: {video: string; from: number; edge?: number}};

export type ExplainerShape = Shape & {hide?: number};
export type Card = {start: number; end: number; value: number; prefix?: string; suffix?: string; unit: string; color: string; source?: string};

export type ExplainerReelProps = {
	durationSeconds: number;
	handle: string;
	name: string;
	voice: string;
	clips: Clip[];
	earths: Record<string, {video: string; frames: EarthFrame[]}>;
	credit: string;
	shapes: ExplainerShape[];
	captions: PillCaption[];
	cards?: Card[];
	headlines?: {start: number; end: number; lines: string[]; y?: number}[];
	flashWords?: {start: number; end: number; text: string}[];
	comment?: {start: number; end: number; keyword: string; detail: string; avatar: string};
	endCard?: {start: number; headline: string; detail: string; permit?: string; credits?: string};
	sounds?: Sound[];
	music?: {file: string; volume: number};
	layout?: Layout;
};

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
// One family for everything, with a serif italic for emphasis: modern, clean and easy to read at speed.
const SANS = 'Plus Jakarta Sans';
const SERIF = 'Instrument Serif';
const GOLD = 'linear-gradient(180deg, #FFF4CF 0%, #F4CB72 52%, #C88A2B 100%)';
// Dark glass with a top sheen, so white text stays readable over bright desert and pale water.
export const GLASS = {
	background: 'linear-gradient(180deg, rgba(255,255,255,0.26) 0%, rgba(255,255,255,0.07) 46%, rgba(255,255,255,0) 54%), rgba(12,15,26,0.46)',
	backdropFilter: 'blur(22px) saturate(170%)',
	WebkitBackdropFilter: 'blur(22px) saturate(170%)',
	border: '1.5px solid rgba(255,255,255,0.42)',
	boxShadow: 'inset 0 1px 1px rgba(255,255,255,0.65), inset 0 -10px 22px rgba(0,0,0,0.18), 0 14px 36px rgba(0,0,0,0.32)',
} as const;
export const goldText = {backgroundImage: GOLD, WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent'} as const;

// Matches the Earth Studio render setting (Custom, X 80, Y 360, Left), so the source credit sits under Google's logo.
const CREDIT_LEFT = 108;
// Where the logo (from that render setting) and the credit text sit, at 1080x1920.
const LOGO_ZONE = {x: 70, y: 215, width: 560, height: 170};
// A thin white edge makes the cut-out read as a deliberate sticker and hides window halo.
export const STICKER = 'drop-shadow(3px 0 0 #fff) drop-shadow(-3px 0 0 #fff) drop-shadow(0 3px 0 #fff) drop-shadow(0 -3px 0 #fff) drop-shadow(0 18px 30px rgba(0,0,0,0.45))';

type Point = {x: number; y: number};
type EarthClip = Extract<Clip, {kind: 'earth'}>;

// Video and overlays must use the same whole-frame maths, or outlines run a frame ahead of the footage.
const toFrame = (seconds: number, fps: number) => Math.round(seconds * fps);

export const GlassLabel: React.FC<{shape: ExplainerShape; place: (c: number[]) => Point; time: number}> = ({shape, place, time}) => {
	const {width, height} = useVideoConfig();
	if (!shape.label || time < shape.start + 0.3) return null;
	const anchor = place(shape.anchor ?? shape.lines[0][Math.floor(shape.lines[0].length / 2)]);
	// Labels stay locked to the ground. Near an edge or Google's logo they fade out instead of being pushed around.
	const inside = anchor.x > 150 && anchor.x < width - 150 && anchor.y > 300 && anchor.y < height - 300;
	const underLogo = anchor.x < LOGO_ZONE.x + LOGO_ZONE.width + 150 && anchor.y < LOGO_ZONE.y + LOGO_ZONE.height + 170;
	if (!inside || underLogo) return null;
	const leave = shape.end === undefined ? 1 : interpolate(time, [shape.end, shape.end + 0.25], [1, 0], clamp);
	const enter = interpolate(time, [shape.start + 0.3, shape.start + 0.55], [0, 1], clamp);
	const rise = 84;
	return (
		<div style={{position: 'absolute', left: anchor.x, top: anchor.y, opacity: enter * leave}}>
			<div style={{position: 'absolute', left: -1, top: -rise, width: 2, height: rise, background: 'linear-gradient(rgba(255,255,255,0.95), rgba(255,255,255,0.2))'}} />
			<div style={{position: 'absolute', left: -8, top: -8, width: 16, height: 16, borderRadius: 8, background: shape.color, border: '2.5px solid white', boxShadow: `0 0 16px ${shape.color}`}} />
			<div style={{position: 'absolute', top: -rise - 46, transform: `translateX(-50%) translateY(${(1 - enter) * 10}px)`, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6}}>
				<div style={{...GLASS, borderRadius: 14, padding: '9px 18px', fontFamily: SANS, fontWeight: 800, fontSize: 24, letterSpacing: '0.08em', color: 'white', whiteSpace: 'nowrap', textTransform: 'uppercase'}}>
					{shape.label}
				</div>
				{shape.chip ? (
					<div style={{background: shape.color, color: '#0d0f18', fontFamily: SANS, fontWeight: 800, fontSize: 22, padding: '5px 14px', borderRadius: 10, whiteSpace: 'nowrap', boxShadow: `0 6px 18px ${shape.color}66`}}>{shape.chip}</div>
				) : null}
			</div>
		</div>
	);
};

const EarthLayer: React.FC<{clip: EarthClip; props: ExplainerReelProps; time: number}> = ({clip, props, time}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const earth = props.earths[clip.earth];
	const startFrom = toFrame(clip.from, fps);
	// `frame` is relative to this clip's Sequence, exactly as OffthreadVideo counts it.
	const index = Math.min(Math.max(startFrom + frame, 0), earth.frames.length - 1);
	const place = earthProjector(earth.frames[index], width, height);
	const shapes = props.shapes.filter((s) => s.hide === undefined || time < s.hide);
	return (
		<AbsoluteFill>
			<OffthreadVideo src={staticFile(earth.video)} startFrom={startFrom} muted style={{width: '100%', height: '100%'}} />
			<svg width={width} height={height} style={{position: 'absolute', left: 0, top: 0}}>
				{/* Google's logo and the imagery credit must never be covered, so shapes are masked out of that corner. */}
				<mask id={`keep-logo-clear-${clip.start}`}>
					<rect width={width} height={height} fill="white" />
					<rect x={LOGO_ZONE.x} y={LOGO_ZONE.y} width={LOGO_ZONE.width} height={LOGO_ZONE.height} rx={24} fill="black" />
				</mask>
				<g mask={`url(#keep-logo-clear-${clip.start})`}>
					{shapes.map((shape, i) => <ShapeLayer key={i} shape={shape} place={place} zoom={1} time={time} />)}
				</g>
			</svg>
			{shapes.map((shape, i) => <GlassLabel key={i} shape={shape} place={place} time={time} />)}
		</AbsoluteFill>
	);
};

export type Layout = 'right' | 'center' | 'left' | 'mirror-left' | 'bottom' | 'v1';

const Cutout: React.FC<{clip: EarthClip; previous?: Clip; time: number; layout: Layout}> = ({clip, previous, time, layout}) => {
	const {fps} = useVideoConfig();
	if (!clip.cutout) return null;
	// Slide in only when the speaker was not already on screen.
	const continues = previous?.kind === 'earth' && previous.cutout;
	const enter = continues ? 1 : interpolate(time, [clip.start, clip.start + 0.35], [0, 1], clamp);
	const person = (
		<div style={{width: '100%', height: '100%', filter: STICKER}}>
			<OffthreadVideo src={staticFile(clip.cutout.video)} startFrom={toFrame(clip.cutout.from, fps)} muted transparent style={{width: '100%', height: '100%'}} />
		</div>
	);
	const slide = {transform: `translateY(${(1 - enter) * 220}px)`, opacity: enter};
	// The source frame cuts the arm at its right edge. Each layout hides that edge rather than fading it.
	if (layout === 'left') {
		// `edge` is how far down the source frame (0-1) the shoulder first touches the frame's side.
		// Sizing so that point lands on the bottom of the screen keeps the cut edge off-screen, with no fade.
		const boxHeight = 2200;
		const top = 1920 - (clip.cutout.edge ?? 0.56) * boxHeight;
		return <div style={{position: 'absolute', left: -289, top, width: boxHeight * 9 / 16, height: boxHeight, ...slide}}>{person}</div>;
	}
	if (layout === 'bottom') {
		// Large and centred, wide enough that both side edges of the source frame sit off-screen.
		return <div style={{position: 'absolute', left: -80, top: 430, width: 1240, height: 2204, ...slide}}>{person}</div>;
	}
	if (layout === 'v1') {
		// The v1 position: bottom left, partly off the left edge.
		return <div style={{position: 'absolute', left: -150, top: '41%', width: 720, height: 1280, ...slide}}>{person}</div>;
	}
	if (layout === 'mirror-left') {
		// Mirrored, so the cut edge of the source frame is on the left and sits off-screen.
		return <div style={{position: 'absolute', left: -110, top: '41%', width: 720, height: 1280, ...slide}}><div style={{width: '100%', height: '100%', transform: 'scaleX(-1)'}}>{person}</div></div>;
	}
	if (layout === 'center') {
		return <div style={{position: 'absolute', left: 180, top: '41%', width: 720, height: 1280, ...slide}}>{person}</div>;
	}
	return <div style={{position: 'absolute', left: 470, top: '41%', width: 720, height: 1280, ...slide}}>{person}</div>;
};

const SpeakerLayer: React.FC<{clip: Extract<Clip, {kind: 'speaker'}>; time: number}> = ({clip, time}) => {
	const {fps} = useVideoConfig();
	const push = interpolate(time, [clip.start, clip.end], [1, 1.05], clamp);
	return (
		<AbsoluteFill style={{transform: `scale(${push})`}}>
			<OffthreadVideo src={staticFile(clip.video)} startFrom={toFrame(clip.from, fps)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
		</AbsoluteFill>
	);
};

// Captions are bare type, not glass, so they never read as one of the number or place cards.
const Captions: React.FC<{captions: PillCaption[]; time: number; top: number}> = ({captions, time, top}) => {
	const caption = captions.find((c) => time >= c.words[0].start && time < c.end);
	if (!caption) return null;
	const start = caption.words[0].start;
	const enter = interpolate(time, [start, start + 0.14], [0, 1], clamp);
	const current = caption.words.reduce((last, w, i) => (time >= w.start ? i : last), 0);
	return (
		<div style={{position: 'absolute', top: `${top}%`, left: 70, right: 70, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', columnGap: 16, alignItems: 'baseline', opacity: enter, transform: `translateY(${(1 - enter) * 12}px)`}}>
			{caption.words.map((word, i) => {
				const shown = interpolate(time, [word.start - 0.03, word.start + 0.1], [0, 1], clamp);
				const active = i === current;
				const pop = active ? interpolate(time, [word.start, word.start + 0.12], [1.12, 1.04], clamp) : 1;
				// A tight dark halo works like an outline, so the bare words stay readable over bright sand and pale water.
				const shadow = 'drop-shadow(0 0 1.5px rgba(0,0,0,0.95)) drop-shadow(0 0 3px rgba(0,0,0,0.7)) drop-shadow(0 6px 16px rgba(0,0,0,0.6))';
				return (
					<span key={i} style={{
						display: 'inline-block',
						fontFamily: word.accent ? SERIF : SANS,
						fontStyle: word.accent ? 'italic' : 'normal',
						fontWeight: word.accent ? 400 : 800,
						fontSize: word.accent ? 74 : 60,
						letterSpacing: word.accent ? '0' : '-0.035em',
						lineHeight: 1.08,
						opacity: 0.62 + shown * 0.38,
						transform: `scale(${pop})`,
						filter: shadow,
						...(active || word.accent ? goldText : {color: 'white'}),
					}}>
						{word.text}
					</span>
				);
			})}
		</div>
	);
};

const CardView: React.FC<{card: Card; time: number}> = ({card, time}) => {
	if (time < card.start || time > card.end) return null;
	const value = interpolate(time, [card.start, card.start + 0.8], [0, card.value], clamp);
	const shown = card.value >= 100 ? Math.round(value).toLocaleString('en-US') : Math.round(value).toString();
	const enter = interpolate(time, [card.start, card.start + 0.2], [0, 1], clamp);
	const leave = interpolate(time, [card.end - 0.2, card.end], [1, 0], clamp);
	return (
		<div style={{position: 'absolute', top: '32%', left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: enter * leave, transform: `translateY(${(1 - enter) * 24}px) scale(${0.95 + enter * 0.05})`}}>
			<div style={{...GLASS, borderRadius: 32, padding: '20px 56px 18px', textAlign: 'center', minWidth: 420}}>
				<div style={{fontFamily: SANS, fontWeight: 800, fontSize: 96, lineHeight: 1, letterSpacing: '-0.04em', fontVariantNumeric: 'tabular-nums', whiteSpace: 'nowrap', color: 'white', textShadow: '0 4px 18px rgba(0,0,0,0.35)'}}>{card.prefix ?? ''}{shown}{card.suffix ?? ''}</div>
				<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 40, marginTop: 6, ...goldText}}>{card.unit}</div>
				<div style={{height: 4, width: 110, margin: '10px auto 0', borderRadius: 2, background: card.color, boxShadow: `0 0 14px ${card.color}`}} />
				{card.source ? <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 15, color: 'rgba(255,255,255,0.6)', marginTop: 10, letterSpacing: '0.1em'}}>{card.source}</div> : null}
			</div>
		</div>
	);
};

const Headline: React.FC<{item: NonNullable<ExplainerReelProps['headlines']>[number]; time: number}> = ({item, time}) => {
	if (time < item.start || time >= item.end) return null;
	const enter = interpolate(time, [item.start, item.start + 0.25], [0, 1], clamp);
	const leave = interpolate(time, [item.end - 0.15, item.end], [1, 0], clamp);
	return (
		<div style={{position: 'absolute', top: `${item.y ?? 26}%`, left: 60, right: 60, textAlign: 'center', opacity: enter * leave, filter: `blur(${(1 - enter) * 12}px)`}}>
			{item.lines.map((line, i) => (
				<div key={i} style={{fontFamily: SANS, fontWeight: 800, fontSize: 86, lineHeight: 1, letterSpacing: '-0.045em', color: 'white', textShadow: '0 6px 26px rgba(0,0,0,0.6)'}}>{line}</div>
			))}
		</div>
	);
};

const FlashWord: React.FC<{item: NonNullable<ExplainerReelProps['flashWords']>[number]; time: number}> = ({item, time}) => {
	if (time < item.start || time >= item.end) return null;
	const scale = interpolate(time, [item.start, item.start + 0.12], [1.25, 1], clamp);
	return (
		<div style={{position: 'absolute', top: '52%', left: 0, right: 0, textAlign: 'center', transform: `scale(${scale})`}}>
			<span style={{fontFamily: SANS, fontWeight: 800, fontSize: 168, letterSpacing: '-0.05em', lineHeight: 1, ...goldText, filter: 'drop-shadow(0 4px 0 rgba(0,0,0,0.35)) drop-shadow(0 10px 30px rgba(0,0,0,0.7))'}}>{item.text}</span>
		</div>
	);
};

// Looks like a real comment being typed, so the call to action reads as something to copy.
const CommentCard: React.FC<{item: NonNullable<ExplainerReelProps['comment']>; time: number; handle: string}> = ({item, time, handle}) => {
	if (time < item.start || time >= item.end) return null;
	const enter = interpolate(time, [item.start, item.start + 0.3], [0, 1], clamp);
	const typed = Math.floor(interpolate(time, [item.start + 0.25, item.start + 0.95], [0, item.keyword.length], clamp));
	const caret = typed < item.keyword.length || Math.floor(time * 2.5) % 2 === 0;
	const heart = interpolate(time, [item.start + 1.15, item.start + 1.35, item.start + 1.5], [0, 1.3, 1], clamp);
	return (
		<div style={{position: 'absolute', top: '27%', left: 80, right: 80, opacity: enter, transform: `translateY(${(1 - enter) * 40}px) scale(${0.94 + enter * 0.06})`}}>
			<div style={{...GLASS, background: 'linear-gradient(180deg, rgba(255,255,255,0.22) 0%, rgba(255,255,255,0.05) 46%, rgba(255,255,255,0) 54%), rgba(10,12,22,0.7)', borderRadius: 34, padding: '26px 30px', display: 'flex', gap: 22, alignItems: 'center'}}>
				<Img src={staticFile(item.avatar)} style={{width: 92, height: 92, borderRadius: 46, objectFit: 'cover', border: '3px solid rgba(255,255,255,0.85)', flexShrink: 0}} />
				<div style={{flex: 1}}>
					<div style={{fontFamily: SANS, fontWeight: 700, fontSize: 22, color: 'rgba(255,255,255,0.7)'}}>Comment on @{handle}&apos;s reel</div>
					<div style={{fontFamily: SANS, fontWeight: 800, fontSize: 72, letterSpacing: '-0.03em', lineHeight: 1.05, color: 'white', whiteSpace: 'nowrap'}}>
						{item.keyword.slice(0, typed)}
						<span style={{opacity: caret ? 1 : 0, color: '#F4CB72', fontWeight: 500}}>|</span>
					</div>
					<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 34, ...goldText}}>{item.detail}</div>
				</div>
				<svg width={52} height={52} viewBox="0 0 24 24" style={{transform: `scale(${heart})`, flexShrink: 0}}>
					<path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.6 3 5 6.6 5c2 0 3.4 1.1 4.2 2.4h2.4C14 6.1 15.4 5 17.4 5 21 5 23.1 8.6 21.6 11.8 19.5 16.4 12 21 12 21z" fill="#FF4F6D" />
				</svg>
			</div>
		</div>
	);
};

const EndCardView: React.FC<{card: NonNullable<ExplainerReelProps['endCard']>; time: number; props: ExplainerReelProps}> = ({card, time, props}) => {
	if (time < card.start) return null;
	const enter = interpolate(time, [card.start, card.start + 0.4], [0, 1], clamp);
	return (
		<AbsoluteFill style={{background: 'radial-gradient(120% 80% at 50% 30%, #1d2440 0%, #0b0d16 70%)', opacity: enter, alignItems: 'center', justifyContent: 'center', textAlign: 'center', color: 'white', gap: 18, padding: '0 110px'}}>
			<div style={{fontFamily: SANS, fontWeight: 800, fontSize: 96, letterSpacing: '-0.045em', lineHeight: 1}}>{card.headline}</div>
			<div style={{fontFamily: SERIF, fontStyle: 'italic', fontSize: 50, ...goldText}}>{card.detail}</div>
			<div style={{fontFamily: SANS, fontWeight: 700, fontSize: 34, marginTop: 34}}>{props.name} · @{props.handle}</div>
			{card.permit ? <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 24, opacity: 0.75}}>{card.permit}</div> : null}
			{card.credits ? <div style={{position: 'absolute', bottom: 330, left: 120, right: 120, fontFamily: SANS, fontWeight: 500, fontSize: 18, lineHeight: 1.4, opacity: 0.6}}>{card.credits}</div> : null}
		</AbsoluteFill>
	);
};

export const ExplainerReel: React.FC<ExplainerReelProps> = (props) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const time = frame / fps;
	const index = props.clips.findIndex((c) => frame >= toFrame(c.start, fps) && frame < toFrame(c.end, fps));
	const clip = props.clips[index] ?? props.clips[props.clips.length - 1];
	const previous = index > 0 ? props.clips[index - 1] : undefined;
	return (
		<AbsoluteFill style={{background: '#0b0d16', overflow: 'hidden'}}>
			{props.clips.map((c, i) => (
				<Sequence key={i} from={toFrame(c.start, fps)} durationInFrames={toFrame(c.end, fps) - toFrame(c.start, fps)}>
					{c.kind === 'earth' ? <EarthLayer clip={c} props={props} time={time} /> : <SpeakerLayer clip={c} time={time} />}
				</Sequence>
			))}
			{clip.kind === 'earth' ? (
				<>
					<Sequence from={toFrame(clip.start, fps)} durationInFrames={toFrame(clip.end, fps) - toFrame(clip.start, fps)}>
						<Cutout clip={clip} previous={previous} time={time} layout={props.layout ?? 'right'} />
					</Sequence>
					<div style={{position: 'absolute', top: '17.3%', left: CREDIT_LEFT, width: '44%', fontFamily: SANS, fontWeight: 700, fontSize: 14, lineHeight: 1.3, color: 'rgba(255,255,255,0.88)', textShadow: '0 1px 4px rgba(0,0,0,0.85)'}}>{props.credit}</div>
				</>
			) : null}
			{props.headlines?.map((h, i) => <Headline key={i} item={h} time={time} />)}
			{props.flashWords?.map((w, i) => <FlashWord key={i} item={w} time={time} />)}
			{props.cards?.map((c, i) => <CardView key={i} card={c} time={time} />)}
			{props.comment ? <CommentCard item={props.comment} time={time} handle={props.handle} /> : null}
			<Captions captions={props.captions} time={time} top={clip.kind === 'earth' && props.layout === 'bottom' ? 50 : clip.kind === 'earth' && props.layout === 'left' ? 52 : 56} />
			<div style={{position: 'absolute', top: '21.5%', right: 66, fontFamily: SANS, fontWeight: 700, fontSize: 24, letterSpacing: '0.01em', color: 'rgba(255,255,255,0.55)', textShadow: '0 1px 6px rgba(0,0,0,0.35)'}}>@{props.handle}</div>
			{props.endCard ? <EndCardView card={props.endCard} time={time} props={props} /> : null}
			<Audio src={staticFile(props.voice)} />
			{props.music ? <Audio src={staticFile(props.music.file)} volume={props.music.volume} /> : null}
			{props.sounds?.map((sound, i) => (
				<Sequence key={i} from={toFrame(sound.at, fps)}>
					<Audio src={staticFile(sound.file)} volume={sound.volume ?? 0.4} />
				</Sequence>
			))}
		</AbsoluteFill>
	);
};
