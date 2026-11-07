import '@fontsource/sora/300.css';
import '@fontsource/sora/800.css';
import '@fontsource/inter-tight/500.css';
import '@fontsource/inter-tight/700.css';
import '@fontsource/playfair-display/800.css';
import '@fontsource/playfair-display/800-italic.css';

export type StyleName = 'spotlight' | 'editorial';
export type Role = 'small' | 'big' | 'serif' | 'italic';

export type Token = {text: string; start: number; role?: Role; color?: string; newline?: boolean};
export type Caption = {end: number; y?: number; tokens: Token[]};
export type DepthHeadline = {start: number; end: number; lines: {text: string; color?: string}[]; y?: number};
export type Sound = {file: string; at: number; volume?: number};

export type ReelProps = {
	style: StyleName;
	video?: string;
	videoStart?: number;
	personVideo?: string;
	background?: string;
	durationSeconds: number;
	handle: string;
	captions: Caption[];
	depthHeadlines?: DepthHeadline[];
	sounds?: Sound[];
	music?: {file: string; volume: number};
	endCard?: {start: number; headline: string; detail?: string; permit?: string};
};

type RoleStyle = {fontFamily: string; fontWeight: number; fontStyle?: string; fontSize: number; letterSpacing: string};

export const STYLES: Record<StyleName, {roles: Record<Role, RoleStyle>; accents: string[]; surface: string}> = {
	spotlight: {
		roles: {
			small: {fontFamily: 'Sora', fontWeight: 300, fontSize: 58, letterSpacing: '-0.03em'},
			big: {fontFamily: 'Sora', fontWeight: 800, fontSize: 132, letterSpacing: '-0.045em'},
			serif: {fontFamily: 'Playfair Display', fontWeight: 800, fontSize: 118, letterSpacing: '-0.04em'},
			italic: {fontFamily: 'Playfair Display', fontWeight: 800, fontStyle: 'italic', fontSize: 118, letterSpacing: '-0.04em'},
		},
		accents: ['#39E6E0', '#FF8A1E', '#FFE14D', '#E23FD0'],
		surface: '#0D1216',
	},
	editorial: {
		roles: {
			small: {fontFamily: 'Inter Tight', fontWeight: 500, fontSize: 46, letterSpacing: '-0.04em'},
			big: {fontFamily: 'Inter Tight', fontWeight: 700, fontSize: 112, letterSpacing: '-0.06em'},
			serif: {fontFamily: 'Playfair Display', fontWeight: 800, fontSize: 118, letterSpacing: '-0.07em'},
			italic: {fontFamily: 'Playfair Display', fontWeight: 800, fontStyle: 'italic', fontSize: 118, letterSpacing: '-0.07em'},
		},
		accents: ['#1F6BFF'],
		surface: '#1F6BFF',
	},
};
