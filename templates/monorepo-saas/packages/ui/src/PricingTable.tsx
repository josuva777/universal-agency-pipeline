'use client';
import React, { useState } from 'react';
import { useTheme } from './ThemeEngine';

export interface PricingPlan {
  id: string;
  name: string;
  badge?: string;
  monthlyPrice: number;
  annualPrice: number;
  description: string;
  features: string[];
  cta: string;
  highlighted?: boolean;
}

export const PRICING_PLANS: PricingPlan[] = [
  {
    id: 'starter',
    name: 'Starter Plan',
    monthlyPrice: 0,
    annualPrice: 0,
    description: 'For individual researchers, developers, and pilot projects.',
    features: [
      '50,000 monthly agent tool calls',
      'Local pure-python vector RAG',
      'Community Slack support',
      'Single tenant isolation',
      'Standard 6-digit Email OTP auth',
    ],
    cta: 'Get Started Free',
  },
  {
    id: 'team',
    name: 'SecOps Team',
    badge: 'MOST POPULAR',
    monthlyPrice: 99,
    annualPrice: 79,
    description: 'For fast-moving security and engineering teams running autonomous fleets.',
    features: [
      '1,000,000 monthly agent tool calls',
      'OWASP 56-vector adversarial guardrails',
      'Distributed OpenTelemetry tracing',
      'Priority email & Discord SLA (4h)',
      'Immutable SHA-256 financial ledger',
      'Custom model provider failover chain',
    ],
    cta: 'Upgrade to Team',
    highlighted: true,
  },
  {
    id: 'enterprise',
    name: 'Enterprise Defense',
    badge: 'UNLIMITED FLEET',
    monthlyPrice: 499,
    annualPrice: 399,
    description: 'Mission-critical autonomous fleet governance for regulated industries.',
    features: [
      'Unlimited monthly agent tool calls',
      'Custom fine-tuned domain models',
      'Dedicated private VPC deployment',
      '15-minute 24/7 dedicated security engineer',
      'SOC2 Type II & HIPAA audit attestations',
      'Master Admin exclusivity & RBAC kill-switches',
    ],
    cta: 'Contact Architecture Team',
  },
];

export const PricingTable: React.FC<{ onSelectPlan?: (planId: string) => void }> = ({ onSelectPlan }) => {
  const { currentTheme } = useTheme();
  const [isAnnual, setIsAnnual] = useState(true);

  return (
    <section id="pricing" className="py-24 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      {/* Title & Billing Toggle */}
      <div className="text-center max-w-3xl mx-auto mb-16">
        <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight font-mono">
          Transparent, Predictable Enterprise Pricing
        </h2>
        <p className="mt-4 text-base text-slate-400">
          Zero hidden surcharges. All tiers include full zero-trust scope containment and hardware session security.
        </p>

        {/* Toggle Bar */}
        <div className="mt-8 inline-flex items-center gap-3 p-1.5 rounded-full bg-slate-900 border border-slate-800">
          <button
            onClick={() => setIsAnnual(false)}
            className={`px-5 py-2 text-xs font-bold rounded-full transition-all ${
              !isAnnual ? 'bg-slate-800 text-white shadow' : 'text-slate-400 hover:text-white'
            }`}
          >
            Monthly Billing
          </button>
          <button
            onClick={() => setIsAnnual(true)}
            className={`px-5 py-2 text-xs font-bold rounded-full transition-all flex items-center gap-2 ${
              isAnnual ? 'bg-slate-800 text-white shadow' : 'text-slate-400 hover:text-white'
            }`}
          >
            Annual Billing
            <span
              className="text-[10px] font-mono px-2 py-0.5 rounded-full font-bold text-slate-950"
              style={{ backgroundColor: currentTheme.accent }}
            >
              SAVE 20%
            </span>
          </button>
        </div>
      </div>

      {/* Pricing Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {PRICING_PLANS.map((plan) => {
          const price = isAnnual ? plan.annualPrice : plan.monthlyPrice;
          const isHighlighted = plan.highlighted;

          return (
            <div
              key={plan.id}
              className={`rounded-2xl p-8 flex flex-col justify-between border transition-all duration-200 relative ${
                isHighlighted ? 'scale-105 shadow-2xl' : 'hover:border-slate-700'
              }`}
              style={{
                backgroundColor: currentTheme.surfaceRaised,
                borderColor: isHighlighted ? currentTheme.accent : currentTheme.border,
              }}
            >
              {plan.badge && (
                <div
                  className="absolute -top-3.5 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full text-[10px] font-mono font-extrabold tracking-wider text-slate-950 shadow-md"
                  style={{ backgroundColor: currentTheme.accent }}
                >
                  {plan.badge}
                </div>
              )}

              <div>
                <h3 className="text-xl font-bold font-mono">{plan.name}</h3>
                <p className="text-xs text-slate-400 mt-2 min-h-[36px]">{plan.description}</p>

                <div className="mt-6 mb-8 flex items-baseline gap-2">
                  <span className="text-5xl font-extrabold tracking-tight font-mono">${price}</span>
                  <span className="text-xs text-slate-400 font-mono">/ user / month</span>
                </div>

                <div className="space-y-3 border-t pt-6" style={{ borderColor: currentTheme.border }}>
                  {plan.features.map((feat, i) => (
                    <div key={i} className="flex items-center gap-3 text-xs text-slate-300">
                      <svg
                        className="w-4 h-4 shrink-0"
                        fill="none"
                        stroke={currentTheme.accent}
                        viewBox="0 0 24 24"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                      </svg>
                      <span>{feat}</span>
                    </div>
                  ))}
                </div>
              </div>

              <button
                onClick={() => onSelectPlan?.(plan.id)}
                className="mt-8 w-full py-3 rounded-xl font-bold text-xs tracking-wider uppercase transition-all shadow-lg"
                style={{
                  backgroundColor: isHighlighted ? currentTheme.accent : currentTheme.surface,
                  color: isHighlighted ? '#020617' : currentTheme.textPrimary,
                  border: isHighlighted ? 'none' : `1px solid ${currentTheme.border}`,
                }}
              >
                {plan.cta}
              </button>
            </div>
          );
        })}
      </div>
    </section>
  );
};

