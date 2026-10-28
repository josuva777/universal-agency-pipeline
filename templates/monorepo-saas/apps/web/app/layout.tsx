import React from 'react';
import { ThemeProvider } from '@repo/ui';

export const metadata = {
  title: 'SentinelOps | Autonomous Agent Guardrails & Enterprise Governance',
  description: 'Deterministic scope containment, real-time cryptographic audit ledgers, and zero-leak identity verification.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased selection:bg-emerald-500 selection:text-black">
        <ThemeProvider defaultTheme="cyberpunk-matrix">
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
