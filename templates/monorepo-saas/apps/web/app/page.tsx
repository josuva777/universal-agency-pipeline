import React from 'react';
import { Button } from '@repo/ui';

export default function HomePage() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen px-4 text-center">
      <div className="inline-flex items-center gap-2 px-3 py-1 mb-8 text-xs font-mono font-bold tracking-wider uppercase border rounded-full bg-emerald-500/10 border-emerald-500/20 text-emerald-400">
        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
        Enterprise Monorepo v2.0
      </div>

      <h1 className="max-w-4xl text-5xl font-extrabold tracking-tight sm:text-7xl">
        Next-Generation Autonomous{' '}
        <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400">
          Agent Security
        </span>
      </h1>

      <p className="max-w-2xl mt-6 text-lg text-slate-400">
        Deterministic scope containment, real-time cryptographic audit ledgers, and zero-leak identity verification.
      </p>

      <div className="flex flex-wrap items-center justify-center gap-4 mt-10">
        <Button variant="primary" size="lg">
          Launch Console
        </Button>
        <Button variant="outline" size="lg">
          Read Architecture
        </Button>
      </div>
    </main>
  );
}

