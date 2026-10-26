import React from 'react';

export const metadata = {
  title: 'SentinelOps AI | Enterprise Autonomous Fleet Guardrails',
  description: 'Deterministic in-line guardrails, cryptographic financial ledger, and multi-tenant security architecture.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark bg-slate-950 text-slate-100 antialiased">
      <body className="min-h-screen selection:bg-emerald-500 selection:text-slate-950">
        {children}
      </body>
    </html>
  );
}

