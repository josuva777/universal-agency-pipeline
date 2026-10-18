import React from 'react';
import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen px-4 text-center">
      <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-indigo-500/30 bg-indigo-500/10 text-indigo-400 text-xs font-semibold tracking-wider uppercase mb-8">
        Enterprise AI Application
      </div>

      <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight max-w-4xl bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
        Intelligence Engineered for Production
      </h1>

      <p className="mt-6 text-lg text-slate-400 max-w-2xl leading-relaxed">
        Full-stack web application with streaming AI agent, grounded vector search, and strict schema validation built right in.
      </p>

      <div className="mt-10 flex flex-wrap gap-4 justify-center">
        <Link
          href="/chat"
          className="px-8 py-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold transition-all shadow-lg shadow-indigo-600/30"
        >
          Launch AI Copilot →
        </Link>
        <a
          href="/creative/brand_kit.html"
          className="px-8 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 font-semibold border border-slate-800 transition-all"
        >
          Brand & Media Kit
        </a>
      </div>
    </main>
  );
}

