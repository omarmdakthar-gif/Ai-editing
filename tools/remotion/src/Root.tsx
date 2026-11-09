import React from 'react';
import {Composition} from 'remotion';
import {EarthReel, EarthReelProps} from './kit/EarthReel';
import {ExplainerReel, ExplainerReelProps} from './kit/ExplainerReel';
import {Cover} from './kit/Cover';
import {MapReel, MapReelProps} from './kit/MapReel';
import {Reel} from './kit/Reel';
import {ShowcaseReel, ShowcaseProps} from './kit/ShowcaseReel';
import {StoryReel, StoryProps} from './kit/StoryReel';
import {ReelProps} from './kit/styles';

const defaults: ReelProps = {style: 'spotlight', durationSeconds: 5, handle: 'yourhandle', captions: []};
const FPS = 30;

export const Root: React.FC = () => (
	<>
		<Composition
			id="Reel"
			component={Reel as unknown as React.FC<Record<string, unknown>>}
			fps={FPS}
			width={1080}
			height={1920}
			durationInFrames={150}
			defaultProps={defaults as unknown as Record<string, unknown>}
			calculateMetadata={({props}) => ({durationInFrames: Math.round((props.durationSeconds as number) * FPS)})}
		/>
		<Composition
			id="MapReel"
			component={MapReel as unknown as React.FC<Record<string, unknown>>}
			fps={FPS}
			width={1080}
			height={1920}
			durationInFrames={150}
			defaultProps={{} as unknown as Record<string, unknown>}
			calculateMetadata={({props}) => ({durationInFrames: Math.round(((props as unknown as MapReelProps).durationSeconds) * FPS)})}
		/>
		<Composition
			id="EarthReel"
			component={EarthReel as unknown as React.FC<Record<string, unknown>>}
			fps={FPS}
			width={1080}
			height={1920}
			durationInFrames={150}
			defaultProps={{} as unknown as Record<string, unknown>}
			calculateMetadata={({props}) => ({durationInFrames: Math.round(((props as unknown as EarthReelProps).durationSeconds) * FPS)})}
		/>
		<Composition
			id="ExplainerReel"
			component={ExplainerReel as unknown as React.FC<Record<string, unknown>>}
			fps={FPS}
			width={1080}
			height={1920}
			durationInFrames={150}
			defaultProps={{} as unknown as Record<string, unknown>}
			calculateMetadata={({props}) => ({durationInFrames: Math.round(((props as unknown as ExplainerReelProps).durationSeconds) * FPS)})}
		/>
		<Composition
			id="ShowcaseReel"
			component={ShowcaseReel as unknown as React.FC<Record<string, unknown>>}
			fps={FPS}
			width={1080}
			height={1920}
			durationInFrames={150}
			defaultProps={{} as unknown as Record<string, unknown>}
			calculateMetadata={({props}) => ({durationInFrames: Math.round(((props as unknown as ShowcaseProps).durationSeconds) * FPS)})}
		/>
		<Composition
			id="StoryReel"
			component={StoryReel as unknown as React.FC<Record<string, unknown>>}
			fps={FPS}
			width={1080}
			height={1920}
			durationInFrames={150}
			defaultProps={{} as unknown as Record<string, unknown>}
			calculateMetadata={({props}) => ({durationInFrames: Math.round(((props as unknown as StoryProps).durationSeconds) * FPS)})}
		/>
		<Composition
			id="Cover"
			component={Cover as unknown as React.FC<Record<string, unknown>>}
			fps={FPS}
			width={1080}
			height={1920}
			durationInFrames={1}
			defaultProps={{} as unknown as Record<string, unknown>}
		/>
	</>
);
