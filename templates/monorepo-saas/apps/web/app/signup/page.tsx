'use client';
import React, { useState } from 'react';
import { useTheme } from '@repo/ui';

const DISPOSABLE_DOMAINS = ['mailinator.com', 'tempmail.com', 'guerrillamail.com', 'throwaway.email'];

export default function SignupPage() {
  const { currentTheme } = useTheme();
  const [step, setStep] = useState<'info' | 'otp'>('info');
  const [fullName, setFullName] = useState('');
  const [company, setCompany] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [otp, setOtp] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleInfoSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const domain = email.split('@')[1]?.toLowerCase();
    if (domain && DISPOSABLE_DOMAINS.includes(domain)) {
      setError('Anti-Sybil Defense: Disposable email domains are not allowed.');
      return;
    }

    setLoading(true);
    await new Promise((r) => setTimeout(r, 600));
    setLoading(false);
    setStep('otp');
  };

  const handleOtpVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    if (otp.length !== 6) {
      setError('Please enter the 6-digit verification code.');
      return;
    }
    setLoading(true);
    await new Promise((r) => setTimeout(r, 600));
    window.location.href = '/dashboard';
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center p-4"
      style={{ backgroundColor: currentTheme.surface, color: currentTheme.textPrimary }}
    >
      <div
        className="w-full max-w-md p-8 rounded-2xl border shadow-2xl"
        style={{ backgroundColor: currentTheme.surfaceRaised, borderColor: currentTheme.border }}
      >
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold font-mono">Create Tenant Account</h1>
          <p className="text-xs text-slate-400 mt-1">Universal Agency Pipeline Security Protocol</p>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-xs">
            {error}
          </div>
        )}

        {step === 'info' ? (
          <form onSubmit={handleInfoSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-mono text-slate-400 mb-1">Full Name</label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
                className="w-full bg-slate-950 border rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500"
                style={{ borderColor: currentTheme.border }}
              />
            </div>
            <div>
              <label className="block text-xs font-mono text-slate-400 mb-1">Company / Organization</label>
              <input
                type="text"
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                required
                className="w-full bg-slate-950 border rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500"
                style={{ borderColor: currentTheme.border }}
              />
            </div>
            <div>
              <label className="block text-xs font-mono text-slate-400 mb-1">Work Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full bg-slate-950 border rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500"
                style={{ borderColor: currentTheme.border }}
              />
            </div>
            <div>
              <label className="block text-xs font-mono text-slate-400 mb-1">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={8}
                className="w-full bg-slate-950 border rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-emerald-500"
                style={{ borderColor: currentTheme.border }}
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-xl font-bold text-xs uppercase tracking-wider text-slate-950 transition-all shadow-lg"
              style={{ backgroundColor: currentTheme.accent }}
            >
              {loading ? 'Validating...' : 'Continue to 6-Digit OTP'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleOtpVerify} className="space-y-4">
            <p className="text-xs text-slate-400">
              Enter the 6-digit security code sent to <strong className="text-white">{email}</strong>.
            </p>
            <div>
              <label className="block text-xs font-mono text-slate-400 mb-1">6-Digit Verification Code</label>
              <input
                type="text"
                maxLength={6}
                value={otp}
                onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
                placeholder="123456"
                required
                className="w-full text-center tracking-[0.5em] font-mono text-xl bg-slate-950 border rounded-lg px-3.5 py-2.5 text-white focus:outline-none focus:border-emerald-500"
                style={{ borderColor: currentTheme.border }}
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-xl font-bold text-xs uppercase tracking-wider text-slate-950 transition-all shadow-lg"
              style={{ backgroundColor: currentTheme.accent }}
            >
              Confirm Code & Activate
            </button>
          </form>
        )}

        <div className="mt-6 text-center text-xs text-slate-400">
          Already have an account?{' '}
          <a href="/login" className="text-emerald-400 hover:underline font-mono">
            Sign in
          </a>
        </div>
      </div>
    </div>
  );
}

