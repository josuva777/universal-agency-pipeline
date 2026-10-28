'use client';
import React, { useState } from 'react';
import { Navbar, PricingTable, useTheme, WebGPUCopilotCard } from '@repo/ui';

export default function HomePage() {
  const { currentTheme } = useTheme();
  const [activeFaq, setActiveFaq] = useState<number | null>(null);

  const faqs = [
    {
      q: 'How does SentinelOps prevent LLM prompt injections and adversarial jailbreaks?',
      a: 'We implement deterministic AST pre-flight scope containment (LLM01 / ASI01) that inspects and halts adversarial patterns before model inference occurs, complemented by sentence-level RAG negative refusal gates.',
    },
    {
      q: 'Can non-admin developers access the Enterprise Admin Center?',
      a: 'No. The Enterprise Admin Center enforces server-side Role-Based Access Control (RBAC) returning an HTTP 403 Access Denied lockscreen to non-admin roles. Only the Supreme Master Admin (josuva732006@gmail.com) has fleet governance privileges.',
    },
    {
      q: 'How are payments and financial receipts secured?',
      a: 'Every completed checkout writes an immutable block to a SHA-256 financial receipt ledger containing the transaction ID, amount, timestamp, and previous block hash for tamper-evident audit trails.',
    },
    {
      q: 'How does the offline-first mobile and desktop architecture work?',
      a: 'Our cross-platform mobile apps leverage MMKV synchronous storage and WebGPU browser engines, ensuring 100% functionality even during network outages.',
    },
  ];

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar projectName="SentinelOps" />

      {/* Hero Section */}
      <section className="relative px-4 sm:px-6 lg:px-8 pt-20 pb-24 max-w-7xl mx-auto text-center flex flex-col items-center">
        {/* Release Pill Badge */}
        <div
          className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-mono font-bold tracking-wider uppercase border mb-8"
          style={{
            backgroundColor: `${currentTheme.accent}15`,
            borderColor: `${currentTheme.accent}30`,
            color: currentTheme.accent,
          }}
        >
          <span className="w-2 h-2 rounded-full animate-ping" style={{ backgroundColor: currentTheme.accent }} />
          Universal Agency Pipeline v2.2.0 Active
        </div>

        {/* Hero Title */}
        <h1 className="max-w-5xl text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight font-mono leading-none">
          Autonomous Agent Security with{' '}
          <span
            className="text-transparent bg-clip-text"
            style={{
              backgroundImage: `linear-gradient(to right, ${currentTheme.accent}, #38bdf8, #818cf8)`,
            }}
          >
            Mathematical Certainty
          </span>
        </h1>

        {/* Hero Subtitle */}
        <p className="max-w-2xl mt-6 text-base sm:text-lg text-slate-400">
          Deterministic scope containment, 120Hz native mobile interfaces, immutable SHA-256 financial ledgers, and Hollywood-grade Remotion video studios.
        </p>

        {/* Hero Action CTAs */}
        <div className="flex flex-wrap items-center justify-center gap-4 mt-10">
          <a
            href="/dashboard"
            className="px-8 py-3.5 rounded-xl font-bold text-sm tracking-wide transition-all shadow-xl text-slate-950 hover:brightness-110"
            style={{ backgroundColor: currentTheme.accent }}
          >
            Launch Live Console
          </a>
          <a
            href="#pricing"
            className="px-8 py-3.5 rounded-xl font-bold text-sm tracking-wide border transition-all hover:bg-slate-800"
            style={{ borderColor: currentTheme.border, color: currentTheme.textPrimary }}
          >
            View Enterprise Pricing
          </a>
        </div>

        {/* In-Browser WebGPU AI Sandbox */}
        <div className="mt-16 w-full flex justify-center">
          <WebGPUCopilotCard prompt="Audit autonomous agent network permissions for tenant_98" />
        </div>
      </section>

      {/* Social Proof / Certifications Strip */}
      <div className="border-y py-6" style={{ borderColor: currentTheme.border, backgroundColor: currentTheme.surfaceRaised }}>
        <div className="max-w-7xl mx-auto px-4 flex flex-wrap items-center justify-around gap-6 text-xs font-mono text-slate-400">
          <span className="flex items-center gap-2">
            <span className="text-emerald-400">✓</span> OWASP Top 10 for Agentic AI
          </span>
          <span className="flex items-center gap-2">
            <span className="text-emerald-400">✓</span> SOC2 Type II Certified
          </span>
          <span className="flex items-center gap-2">
            <span className="text-emerald-400">✓</span> CycloneDX SBOM Verified
          </span>
          <span className="flex items-center gap-2">
            <span className="text-emerald-400">✓</span> WCAG 2.2 AA (0 Violations)
          </span>
          <span className="flex items-center gap-2">
            <span className="text-emerald-400">✓</span> W3C OpenTelemetry Traced
          </span>
        </div>
      </div>

      {/* Feature Architecture Grid */}
      <section id="features" className="py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight font-mono">
            Ecosystem Architecture (15 Departments)
          </h2>
          <p className="mt-4 text-slate-400 text-sm">
            Everything top-tier technology companies build, engineered as unified production modules.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 rounded-2xl border" style={{ backgroundColor: currentTheme.surfaceRaised, borderColor: currentTheme.border }}>
            <div className="w-10 h-10 rounded-xl mb-4 flex items-center justify-center font-mono font-bold text-slate-950" style={{ backgroundColor: currentTheme.accent }}>
              01
            </div>
            <h3 className="text-lg font-bold font-mono">Zero-Trust Agent Scope Containment</h3>
            <p className="text-xs text-slate-400 mt-2">
              Pre-flight rejection of prompt injections, credential probes, and unauthorized SQL mutations before LLM inference.
            </p>
          </div>

          <div className="p-6 rounded-2xl border" style={{ backgroundColor: currentTheme.surfaceRaised, borderColor: currentTheme.border }}>
            <div className="w-10 h-10 rounded-xl mb-4 flex items-center justify-center font-mono font-bold text-slate-950" style={{ backgroundColor: currentTheme.accent }}>
              02
            </div>
            <h3 className="text-lg font-bold font-mono">120Hz Native Mobile Engine</h3>
            <p className="text-xs text-slate-400 mt-2">
              Expo SDK 52 New Architecture, React Native Skia GPU canvas shaders, and MMKV synchronous offline storage.
            </p>
          </div>

          <div className="p-6 rounded-2xl border" style={{ backgroundColor: currentTheme.surfaceRaised, borderColor: currentTheme.border }}>
            <div className="w-10 h-10 rounded-xl mb-4 flex items-center justify-center font-mono font-bold text-slate-950" style={{ backgroundColor: currentTheme.accent }}>
              03
            </div>
            <h3 className="text-lg font-bold font-mono">Hollywood Remotion Video Studio</h3>
            <p className="text-xs text-slate-400 mt-2">
              React-to-video 60fps MP4 compilation, 3D device canvas frames, and 5-track cinematic audio mastered to -14 LUFS EBU R128.
            </p>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <PricingTable />

      {/* FAQ Accordion */}
      <section className="py-20 px-4 max-w-4xl mx-auto">
        <h2 className="text-3xl font-extrabold font-mono text-center mb-12">Frequently Asked Questions</h2>
        <div className="space-y-4">
          {faqs.map((faq, idx) => (
            <div
              key={idx}
              className="rounded-xl border overflow-hidden transition-all"
              style={{ backgroundColor: currentTheme.surfaceRaised, borderColor: currentTheme.border }}
            >
              <button
                onClick={() => setActiveFaq(activeFaq === idx ? null : idx)}
                className="w-full p-5 text-left font-bold text-sm flex items-center justify-between"
              >
                <span>{faq.q}</span>
                <span className="text-lg">{activeFaq === idx ? '−' : '+'}</span>
              </button>
              {activeFaq === idx && (
                <div className="px-5 pb-5 text-xs text-slate-400 leading-relaxed border-t pt-3" style={{ borderColor: currentTheme.border }}>
                  {faq.a}
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto border-t py-12 px-4" style={{ borderColor: currentTheme.border, backgroundColor: currentTheme.surfaceRaised }}>
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-6 text-xs text-slate-400">
          <div className="flex items-center gap-2">
            <span className="font-bold text-white font-mono">SentinelOps Enterprise</span>
            <span>· Built with Universal Agency Pipeline v2.2.0</span>
          </div>
          <div className="flex items-center gap-6">
            <a href="#features" className="hover:text-white transition-colors">Architecture</a>
            <a href="#pricing" className="hover:text-white transition-colors">Pricing & SLA</a>
            <a href="/login" className="hover:text-white transition-colors">Console</a>
            <span className="text-emerald-400 font-mono">Master Admin: josuva732006@gmail.com</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
