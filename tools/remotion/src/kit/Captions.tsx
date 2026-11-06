import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Caption, STYLES, StyleName, Token} from './styles';

const ENTER_FRAMES = 6;
const EXIT_FRAMES = 5;
const SHADOW = '0 4px 24px rgba(0,0,0,0.45)';

const Word: React.FC<{token: Token; style: StyleName; hide: number}> = ({token, style, hide}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const local = frame - token.start * fps;
	const role = token.role ?? 'small';
	const look = STYLES[style].roles[role];
	const reveal = interpolate(local, [0, ENTER_FRAMES], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const pop = role === 'small' ? 1 : spring({frame: local, fps, config: {damping: 13, stiffness: 180}});

	return (
		<span
			style={{
				...look,
				display: 'inline-block',
				lineHeight: 0.92,
				marginRight: '0.22em',
				color: token.color ?? 'white',
				opacity: reveal * hide,
				filter: `blur(${(1 - reveal) * 10 + (1 - hide) * 10}px)`,
				transform: `translateY(${(1 - reveal) * 14}px) scale(${interpolate(pop, [0, 1], [0.88, 1])})`,
				textShadow: SHADOW,
			}}
		>
			{token.text}
		</span>
	);
};

const Group: React.FC<{caption: Caption; style: StyleName}> = ({caption, style}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const endFrame = caption.end * fps;
	const hide = interpolate(frame, [endFrame - EXIT_FRAMES, endFrame], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const rows: Token[][] = [[]];
	caption.tokens.forEach((token) => {
		if (token.newline) rows.push([]);
		rows[rows.length - 1].push(token);
	});

	return (
		<AbsoluteFill style={{top: `${caption.y ?? 42}%`, height: 'auto', alignItems: 'center', padding: '0 110px'}}>
			{rows.map((row, i) => (
				<div key={i} style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', alignItems: 'baseline'}}>
					{row.map((token, j) => (
						<Word key={j} token={token} style={style} hide={hide} />
					))}
				</div>
			))}
		</AbsoluteFill>
	);
};

export const Captions: React.FC<{captions: Caption[]; style: StyleName}> = ({captions, style}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const time = frame / fps;
	return (
		<>
			{captions
				.filter((c) => time >= c.tokens[0].start && time < c.end)
				.map((c, i) => (
					<Group key={i} caption={c} style={style} />
				))}
		</>
	);
};
