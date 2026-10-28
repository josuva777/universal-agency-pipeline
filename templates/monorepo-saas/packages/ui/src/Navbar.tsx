'use client';
import React, { useState } from 'react';
import { useTheme, ThemeSwitcher } from './ThemeEngine';
import { AppDistributionModal } from './AppDistributionModal';

export const Navbar: React.FC<{ projectName?: string }> = ({ projectName = 'SentinelOps' }) => {
  const { currentTheme } = useTheme();
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <>
      <header
        className="sticky top-0 z-40 w-full border-b transition-colors duration-200"
        style={{
          backgroundColor: currentTheme.surface,
          borderColor: currentTheme.border,
        }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          {/* Brand Logo & Name */}
          <a href="/" className="flex items-center gap-3">
            <div
              className="w-9 h-9 rounded-xl flex items-center justify-center font-bold font-mono text-slate-950 shadow-lg"
              style={{ backgroundColor: currentTheme.accent }}
            >
              {projectName.charAt(0)}
            </div>
            <span className="font-extrabold text-lg tracking-tight font-mono whitespace-nowrap">
              {projectName}
            </span>
          </a>

          {/* Clean Single-Line Navigation Links (Rule 10) */}
          <nav className="hidden md:flex items-center gap-8 text-sm font-medium">
            <a
              href="#features"
              className="whitespace-nowrap transition-colors hover:text-white text-slate-400"
            >
              Features
            </a>
            <a
              href="#architecture"
              className="whitespace-nowrap transition-colors hover:text-white text-slate-400"
            >
              Architecture
            </a>
            <a
              href="#pricing"
              className="whitespace-nowrap transition-colors hover:text-white text-slate-400"
            >
              Pricing & SLA
            </a>
            <a
              href="/dashboard"
              className="whitespace-nowrap transition-colors hover:text-white text-slate-400"
            >
              Live Console
            </a>
          </nav>

          {/* Action CTAs & Unified App Distribution Modal */}
          <div className="flex items-center gap-3">
            <ThemeSwitcher />

            <button
              onClick={() => setModalOpen(true)}
              className="hidden sm:inline-flex items-center gap-2 px-3 py-1.5 text-xs font-semibold rounded-lg border transition-all whitespace-nowrap"
              style={{
                borderColor: currentTheme.border,
                backgroundColor: currentTheme.surfaceRaised,
                color: currentTheme.textPrimary,
              }}
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Desktop & Mobile
            </button>

            <a
              href="/login"
              className="px-4 py-1.5 text-xs font-bold rounded-lg transition-all shadow-md whitespace-nowrap text-slate-950"
              style={{ backgroundColor: currentTheme.accent }}
            >
              Sign In
            </a>
          </div>
        </div>
      </header>

      <AppDistributionModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        projectName={projectName}
      />
    </>
  );
};
