'use client';
import React, { useState, useEffect } from 'react';
import { useTheme } from '@repo/ui';

export default function DashboardPage() {
  const { currentTheme } = useTheme();
  const [tourDismissed, setTourDismissed] = useState(true);
  const [alertsCount, setAlertsCount] = useState(3);
  const [sessions, setSessions] = useState([
    { id: 'sess_1', ip: '192.168.1.104', device: 'Chrome / Windows 11', location: 'San Francisco, CA', current: true },
    { id: 'sess_2', ip: '10.0.4.82', device: 'Safari / iPhone 16 Pro', location: 'Austin, TX', current: false },
  ]);

  useEffect(() => {
    const isDismissed = localStorage.getItem('agency-tour-dismissed');
    if (!isDismissed) setTourDismissed(false);
  }, []);

  const dismissTour = () => {
    setTourDismissed(true);
    localStorage.setItem('agency-tour-dismissed', 'true');
  };

  const killSession = (id: string) => {
    setSessions((prev) => prev.filter((s) => s.id !== id));
  };

  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: currentTheme.surface, color: currentTheme.textPrimary }}>
      {/* Dashboard Header */}
      <header className="border-b h-16 flex items-center justify-between px-6 sticky top-0 z-40" style={{ backgroundColor: currentTheme.surface, borderColor: currentTheme.border }}>
        <div className="flex items-center gap-4">
          <a href="/" className="font-extrabold font-mono text-lg tracking-tight">SentinelOps</a>
          <span className="text-xs px-2.5 py-0.5 rounded-full font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            ★ SecOps Team Tier
          </span>
        </div>

        <div className="flex items-center gap-4">
          {/* Reactive Notification Counter */}
          <button
            onClick={() => setAlertsCount(0)}
            className="relative p-2 rounded-lg hover:bg-slate-800 transition-all text-slate-300"
            title="Clear Notifications"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            {alertsCount > 0 && (
              <span className="absolute top-1.5 right-1.5 w-4 h-4 rounded-full bg-red-500 text-white text-[10px] font-bold flex items-center justify-center">
                {alertsCount}
              </span>
            )}
          </button>

          <a
            href="/dashboard/admin"
            className="px-3.5 py-1.5 rounded-lg text-xs font-mono font-bold border border-slate-700 hover:border-emerald-400 text-slate-300 transition-all"
          >
            Admin Center
          </a>

          <a href="/login" className="text-xs text-slate-400 hover:text-white transition-colors">
            Logout
          </a>
        </div>
      </header>

      {/* Guided Tour Banner (Rule 5) */}
      {!tourDismissed && (
        <div className="px-6 py-3 border-b flex items-center justify-between text-xs" style={{ backgroundColor: currentTheme.surfaceRaised, borderColor: currentTheme.border }}>
          <div className="flex items-center gap-2">
            <span className="text-emerald-400 font-bold">✨ Guided Tour:</span>
            <span>Welcome to your live SecOps console. All agent tool calls are monitored with sliding-window quota limits and distributed OpenTelemetry traces.</span>
          </div>
          <button onClick={dismissTour} className="px-2 py-1 rounded hover:bg-slate-800 text-slate-400 hover:text-white">
            ✕ Dismiss
          </button>
        </div>
      )}

      {/* Main Content Area */}
      <main className="flex-1 p-6 max-w-7xl mx-auto w-full space-y-8">
        {/* Metric Cards Row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-5 rounded-2xl border" style={{ backgroundColor: currentTheme.surfaceRaised, borderColor: currentTheme.border }}>
            <span className="text-xs text-slate-400 font-mono">ACTIVE AGENT FLEET</span>
            <div className="text-3xl font-extrabold font-mono mt-2">12 / 12</div>
            <span className="text-[11px] text-emerald-400 mt-1 inline-block">100% Operational Status</span>
          </div>

          <div className="p-5 rounded-2xl border" style={{ backgroundColor: currentTheme.surfaceRaised, borderColor: currentTheme.border }}>
            <span className="text-xs text-slate-400 font-mono">OWASP LLM01 INTERCEPTIONS</span>
            <div className="text-3xl font-extrabold font-mono mt-2">142</div>
            <span className="text-[11px] text-slate-400 mt-1 inline-block">0 Prompt Injections Leaked</span>
          </div>

          <div className="p-5 rounded-2xl border" style={{ backgroundColor: currentTheme.surfaceRaised, borderColor: currentTheme.border }}>
            <span className="text-xs text-slate-400 font-mono">AVG LATENCY (P99)</span>
            <div className="text-3xl font-extrabold font-mono mt-2">38ms</div>
            <span className="text-[11px] text-emerald-400 mt-1 inline-block">Edge V8 Isolate Cached</span>
          </div>

          <div className="p-5 rounded-2xl border" style={{ backgroundColor: currentTheme.surfaceRaised, borderColor: currentTheme.border }}>
            <span className="text-xs text-slate-400 font-mono">MONTHLY QUOTA METERING</span>
            <div className="text-3xl font-extrabold font-mono mt-2">15,420</div>
            <span className="text-[11px] text-slate-400 mt-1 inline-block">of 1,000,000 monthly calls</span>
          </div>
        </div>

        {/* Quota Progress Bar (Rule 7) */}
        <div className="p-6 rounded-2xl border" style={{ backgroundColor: currentTheme.surfaceRaised, borderColor: currentTheme.border }}>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-mono font-bold">Monthly Tool Calls Allocation</span>
            <span className="text-xs font-mono text-emerald-400">1.54% Consumed</span>
          </div>
          <div className="w-full h-3 rounded-full bg-slate-950 overflow-hidden border border-slate-800">
            <div className="h-full rounded-full transition-all duration-500" style={{ width: '1.54%', backgroundColor: currentTheme.accent }} />
          </div>
        </div>

        {/* Active Hardware Sessions & Kill-Switch (Rule 7) */}
        <div className="p-6 rounded-2xl border" style={{ backgroundColor: currentTheme.surfaceRaised, borderColor: currentTheme.border }}>
          <h2 className="text-lg font-bold font-mono mb-4">Active Hardware Sessions</h2>
          <div className="space-y-3">
            {sessions.map((s) => (
              <div key={s.id} className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-sm font-mono">{s.device}</span>
                    {s.current && (
                      <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono">
                        THIS DEVICE
                      </span>
                    )}
                  </div>
                  <div className="text-xs text-slate-400 mt-1 font-mono">
                    IP: {s.ip} · {s.location}
                  </div>
                </div>

                {!s.current && (
                  <button
                    onClick={() => killSession(s.id)}
                    className="px-3 py-1.5 rounded-lg text-xs font-bold text-red-400 bg-red-500/10 border border-red-500/20 hover:bg-red-500/20 transition-all font-mono"
                  >
                    Kill Session
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
