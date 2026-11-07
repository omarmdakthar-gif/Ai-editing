import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, staticFile, useVideoConfig} from 'remotion';
import {Captions} from './Captions';
import {DepthText, EndCard, HandleTag} from './Frames';
import {ReelProps} from './styles';

// Layer order matters: depth headlines sit between the footage and the cut-out person.
export const Reel: React.FC<ReelProps> = (props) => {
	const {fps} = useVideoConfig();
	return (
		<AbsoluteFill style={{background: '#000'}}>
			{props.background ? <Img src={staticFile(props.background)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /> : null}
			{props.video ? (
				<OffthreadVideo
					src={staticFile(props.video)}
					startFrom={Math.round((props.videoStart ?? 0) * fps)}
					style={{width: '100%', height: '100%', objectFit: 'cover'}}
				/>
			) : null}
			{props.depthHeadlines?.map((item, i) => <DepthText key={i} item={item} />)}
			{props.personVideo ? (
				<AbsoluteFill>
					<OffthreadVideo src={staticFile(props.personVideo)} transparent muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
				</AbsoluteFill>
			) : null}
			<HandleTag handle={props.handle} />
			<Captions captions={props.captions} style={props.style} />
			{props.endCard ? <EndCard card={props.endCard} props={props} /> : null}
			{props.music ? <Audio src={staticFile(props.music.file)} volume={props.music.volume} /> : null}
			{props.sounds?.map((sound, i) => (
				<Sequence key={i} from={Math.round(sound.at * fps)}>
					<Audio src={staticFile(sound.file)} volume={sound.volume ?? 0.5} />
				</Sequence>
			))}
		</AbsoluteFill>
	);
};
