import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {DepthHeadline, ReelProps, STYLES} from './styles';

// Instagram covers the top, the bottom and the right edge, so everything sits inside this band.
const clampRange = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

export const HandleTag: React.FC<{handle: string}> = ({handle}) => (
	<div
		style={{
			position: 'absolute',
			top: '25%',
			right: 150,
			fontFamily: 'Inter Tight',
			fontWeight: 700,
			fontSize: 22,
			letterSpacing: '0.02em',
			color: 'white',
			textTransform: 'uppercase',
			textShadow: '0 2px 10px rgba(0,0,0,0.5)',
		}}
	>
		@{handle}
	</div>
);

export const DepthText: React.FC<{item: DepthHeadline}> = ({item}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const time = frame / fps;
	if (time < item.start || time >= item.end) return null;
	const enter = interpolate(time, [item.start, item.start + 0.25], [0, 1], clampRange);
	const leave = interpolate(time, [item.end - 0.2, item.end], [1, 0], clampRange);
	return (
		<AbsoluteFill style={{top: `${item.y ?? 16}%`, alignItems: 'center'}}>
			{item.lines.map((line, i) => (
				<div
					key={i}
					style={{
						fontFamily: 'Sora',
						fontWeight: 800,
						fontSize: 200,
						letterSpacing: '-0.05em',
						lineHeight: 0.95,
						color: line.color ?? 'white',
						opacity: enter * leave,
						filter: `blur(${(1 - enter) * 16}px)`,
						transform: `scale(${interpolate(enter, [0, 1], [1.12, 1])})`,
					}}
				>
					{line.text}
				</div>
			))}
		</AbsoluteFill>
	);
};

export const EndCard: React.FC<{card: NonNullable<ReelProps['endCard']>; props: ReelProps}> = ({card, props}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const time = frame / fps;
	if (time < card.start) return null;
	const enter = interpolate(time, [card.start, card.start + 0.4], [0, 1], clampRange);
	return (
		<AbsoluteFill
			style={{
				background: props.style === 'editorial' ? STYLES.editorial.surface : 'rgba(5,8,12,0.82)',
				backdropFilter: `blur(${enter * 30}px)`,
				opacity: enter,
				alignItems: 'center',
				justifyContent: 'center',
				padding: '0 130px',
				textAlign: 'center',
				color: 'white',
				gap: 28,
			}}
		>
			<div style={{fontFamily: 'Playfair Display', fontWeight: 800, fontSize: 100, lineHeight: 1, letterSpacing: '-0.04em'}}>{card.headline}</div>
			{card.detail ? <div style={{fontFamily: 'Inter Tight', fontWeight: 500, fontSize: 42}}>{card.detail}</div> : null}
			<div style={{fontFamily: 'Inter Tight', fontWeight: 700, fontSize: 38, marginTop: 30}}>@{props.handle}</div>
			{card.permit ? <div style={{fontFamily: 'Inter Tight', fontWeight: 500, fontSize: 26, opacity: 0.8}}>{card.permit}</div> : null}
		</AbsoluteFill>
	);
};
