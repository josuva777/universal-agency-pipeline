export interface BrandTheme {
  primary: string;
  secondary: string;
  accent: string;
  background: string;
}

export interface VideoScene {
  id: number;
  type: 'hero' | 'tension' | 'mockup_3d' | 'metrics' | 'cta';
  headline: string;
  subtext: string;
  duration_seconds: number;
  vfx_type?: 'particles' | 'chromatic' | 'glow';
}

export interface CaptionWord {
  word: string;
  start_seconds: number;
  end_seconds: number;
}

export interface CommercialProps {
  projectName?: string;
  brandName?: string;
  tagline?: string;
  theme?: BrandTheme;
  scenes?: VideoScene[];
  voiceoverAudioPath?: string;
  subtitles?: CaptionWord[];
  logoSvgPath?: string;
}
