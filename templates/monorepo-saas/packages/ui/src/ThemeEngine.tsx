'use client';
import React, { createContext, useContext, useEffect, useState } from 'react';

export type ThemePaletteId =
  | 'cyberpunk-matrix'
  | 'swiss-bauhaus'
  | 'avionics-amber'
  | 'oceanic-cobalt'
  | 'lockdown-crimson';

export interface ThemePalette {
  id: ThemePaletteId;
  name: string;
  surface: string;
  surfaceRaised: string;
  accent: string;
  accentGlow: string;
  textPrimary: string;
  textSecondary: string;
  border: string;
}

export const THEMES: Record<ThemePaletteId, ThemePalette> = {
  'cyberpunk-matrix': {
    id: 'cyberpunk-matrix',
    name: 'Cyberpunk Matrix',
    surface: '#020617',
    surfaceRaised: '#0f172a',
    accent: '#10b981',
    accentGlow: 'rgba(16, 185, 129, 0.35)',
    textPrimary: '#f8fafc',
    textSecondary: '#94a3b8',
    border: '#1e293b',
  },
  'swiss-bauhaus': {
    id: 'swiss-bauhaus',
    name: 'Swiss Bauhaus',
    surface: '#030712',
    surfaceRaised: '#111827',
    accent: '#ef4444',
    accentGlow: 'rgba(239, 68, 68, 0.35)',
    textPrimary: '#ffffff',
    textSecondary: '#9ca3af',
    border: '#1f2937',
  },
  'avionics-amber': {
    id: 'avionics-amber',
    name: 'Avionics Amber',
    surface: '#09090b',
    surfaceRaised: '#18181b',
    accent: '#f59e0b',
    accentGlow: 'rgba(245, 158, 11, 0.35)',
    textPrimary: '#fafafa',
    textSecondary: '#a1a1aa',
    border: '#27272a',
  },
  'oceanic-cobalt': {
    id: 'oceanic-cobalt',
    name: 'Oceanic Cobalt',
    surface: '#020617',
    surfaceRaised: '#0b132b',
    accent: '#3b82f6',
    accentGlow: 'rgba(59, 130, 246, 0.35)',
    textPrimary: '#f8fafc',
    textSecondary: '#94a3b8',
    border: '#1e293b',
  },
  'lockdown-crimson': {
    id: 'lockdown-crimson',
    name: 'Lockdown Crimson',
    surface: '#0f172a',
    surfaceRaised: '#1e293b',
    accent: '#f43f5e',
    accentGlow: 'rgba(244, 63, 94, 0.35)',
    textPrimary: '#ffffff',
    textSecondary: '#94a3b8',
    border: '#334155',
  },
};

interface ThemeContextType {
  currentTheme: ThemePalette;
  themeId: ThemePaletteId;
  setTheme: (id: ThemePaletteId) => void;
}

const ThemeContext = createContext<ThemeContextType>({
  currentTheme: THEMES['cyberpunk-matrix'],
  themeId: 'cyberpunk-matrix',
  setTheme: () => {},
});

export const ThemeProvider: React.FC<{ children: React.ReactNode; defaultTheme?: ThemePaletteId }> = ({
  children,
  defaultTheme = 'cyberpunk-matrix',
}) => {
  const [themeId, setThemeId] = useState<ThemePaletteId>(defaultTheme);

  useEffect(() => {
    const saved = localStorage.getItem('agency-theme') as ThemePaletteId | null;
    if (saved && THEMES[saved]) {
      setThemeId(saved);
    }
  }, []);

  const setTheme = (id: ThemePaletteId) => {
    if (THEMES[id]) {
      setThemeId(id);
      localStorage.setItem('agency-theme', id);
    }
  };

  const currentTheme = THEMES[themeId];

  useEffect(() => {
    const root = document.documentElement;
    root.setAttribute('data-theme', themeId);
    root.style.setProperty('--color-surface', currentTheme.surface);
    root.style.setProperty('--color-surface-raised', currentTheme.surfaceRaised);
    root.style.setProperty('--color-accent', currentTheme.accent);
    root.style.setProperty('--color-accent-glow', currentTheme.accentGlow);
    root.style.setProperty('--color-text-primary', currentTheme.textPrimary);
    root.style.setProperty('--color-text-secondary', currentTheme.textSecondary);
    root.style.setProperty('--color-border', currentTheme.border);
  }, [themeId, currentTheme]);

  return (
    <ThemeContext.Provider value={{ currentTheme, themeId, setTheme }}>
      <div style={{ backgroundColor: currentTheme.surface, color: currentTheme.textPrimary, minHeight: '100vh' }}>
        {children}
      </div>
    </ThemeContext.Provider>
  );
};

export const useTheme = () => useContext(ThemeContext);

export const ThemeSwitcher: React.FC = () => {
  const { currentTheme, themeId, setTheme } = useTheme();

  return (
    <div className="flex items-center gap-1.5 p-1 rounded-full bg-slate-900 border border-slate-800">
      {(Object.keys(THEMES) as ThemePaletteId[]).map((id) => {
        const t = THEMES[id];
        const isActive = id === themeId;
        return (
          <button
            key={id}
            onClick={() => setTheme(id)}
            title={t.name}
            className={`w-6 h-6 rounded-full transition-all flex items-center justify-center ${
              isActive ? 'ring-2 ring-white scale-110' : 'opacity-60 hover:opacity-100'
            }`}
            style={{ backgroundColor: t.accent }}
          >
            {isActive && <span className="w-1.5 h-1.5 rounded-full bg-slate-950" />}
          </button>
        );
      })}
    </div>
  );
};

