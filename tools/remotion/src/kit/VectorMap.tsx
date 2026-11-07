import React from 'react';
import {AbsoluteFill} from 'remotion';

// A dark, stylised map drawn only from OpenStreetMap geometry, so it carries no imagery watermark.
// The flat map is tilted in 3D for the same aerial feel as the Earth shots.
export type VectorLayer = {lines: number[][][]; color: string; width: number; glow?: boolean; fill?: number; closed?: boolean};
export type VectorMapProps = {center: number[]; pixelsPerDegree: number; tilt: number; layers: VectorLayer[]; labels?: {at: number[]; text: string; color: string}[]};

const PLANE = 2600;

export const VectorMap: React.FC<VectorMapProps> = ({center, pixelsPerDegree, tilt, layers, labels}) => {
	const cos = Math.cos((center[1] * Math.PI) / 180);
	const xy = ([lon, lat]: number[]) => [PLANE / 2 + (lon - center[0]) * pixelsPerDegree * cos, PLANE / 2 - (lat - center[1]) * pixelsPerDegree];
	const path = (line: number[][], closed?: boolean) => `M${line.map((p) => xy(p).join(' ')).join('L')}${closed ? 'Z' : ''}`;
	return (
		<AbsoluteFill style={{background: 'radial-gradient(120% 80% at 50% 40%, #13213f 0%, #070b18 70%)', perspective: 1400, perspectiveOrigin: '50% 30%', overflow: 'hidden'}}>
			<div style={{position: 'absolute', left: (1080 - PLANE) / 2, top: (1920 - PLANE) / 2 + 120, width: PLANE, height: PLANE, transform: `rotateX(${tilt}deg)`, transformOrigin: '50% 60%'}}>
				<svg width={PLANE} height={PLANE}>
					<defs>
						<pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
							<path d="M60 0H0V60" fill="none" stroke="rgba(120,160,255,0.07)" strokeWidth="1.5" />
						</pattern>
					</defs>
					<rect width={PLANE} height={PLANE} fill="url(#grid)" />
					{layers.map((layer, i) => (
						<g key={i}>
							{layer.fill ? layer.lines.map((l, j) => <path key={j} d={path(l, true)} fill={layer.color} fillOpacity={layer.fill} />) : null}
							{layer.glow ? (
								<g style={{filter: 'blur(10px)'}}>
									{layer.lines.map((l, j) => <path key={j} d={path(l, layer.closed)} fill="none" stroke={layer.color} strokeOpacity={0.8} strokeWidth={layer.width * 3.5} strokeLinecap="round" strokeLinejoin="round" />)}
								</g>
							) : null}
							{layer.lines.map((l, j) => <path key={j} d={path(l, layer.closed)} fill="none" stroke={layer.color} strokeWidth={layer.width} strokeLinecap="round" strokeLinejoin="round" />)}
						</g>
					))}
					{/* Labels lie on the ground plane, like street names on a printed map. */}
					{labels?.map((label, i) => {
						const [x, y] = xy(label.at);
						return (
							<text key={i} x={x} y={y} textAnchor="middle" fontFamily="Plus Jakarta Sans" fontWeight={800} fontSize={44} letterSpacing="0.12em" fill={label.color} style={{filter: `drop-shadow(0 0 10px ${label.color})`}}>
								{label.text.toUpperCase()}
							</text>
						);
					})}
				</svg>
			</div>
		</AbsoluteFill>
	);
};
