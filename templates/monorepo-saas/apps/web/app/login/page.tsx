'use client';
import React, { useState } from 'react';
import { useTheme } from '@repo/ui';

export default function LoginPage() {
  const { currentTheme } = useTheme();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [otpMode, setOtpMode] = useState(false);
  const [otpSent, setOtpSent] = useState(false);
  const [otpCode, setOtpCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSendOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) {
      setError('Please enter your work email.');
      return;
    }
    setLoading(true);
    setError('');
    // Simulate real SMTP dispatch call
    await new Promise((r) => setTimeout(r, 600));
    setLoading(false);
    setOtpSent(true);
  };

  const handleVerifyOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (otpCode.length !== 6) {
      setError('Please enter the 6-digit verification code.');
      return;
    }
    setLoading(true);
    // Verified: redirect to dashboard
    window.location.href = '/dashboard';
  };

  const handlePasswordLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setError('Please fill in your email and password.');
      return;
    }
    setLoading(true);
    await new Promise((r) => setTimeout(r, 500));
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
          <div
            className="w-12 h-12 rounded-xl mx-auto flex items-center justify-center font-mono font-bold text-slate-950 text-xl shadow-lg mb-3"
            style={{ backgroundColor: currentTheme.accent }}
          >
            S
          </div>
          <h1 className="text-2xl font-bold font-mono">Sign In to SentinelOps</h1>
          <p className="text-xs text-slate-400 mt-1">Zero-Trust Enterprise Console</p>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-xs">
            {error}
          </div>
        )}

        {/* Tab Toggle: Password vs 6-Digit Email OTP */}
        <div className="flex border-b mb-6 text-xs font-mono" style={{ borderColor: currentTheme.border }}>
          <button
            onClick={() => { setOtpMode(false); setError(''); }}
            className={`flex-1 py-2 font-bold border-b-2 transition-all ${
              !otpMode ? 'border-emerald-400 text-white' : 'border-transparent text-slate-400'
            }`}
          >
            Password Sign In
          </button>
          <button
            onClick={() => { setOtpMode(true); setError(''); }}
            className={`flex-1 py-2 font-bold border-b-2 transition-all ${
              otpMode ? 'border-emerald-400 text-white' : 'border-transparent text-slate-400'
            }`}
          >
            Passwordless OTP
          </button>
        </div>

        {!otpMode ? (
          <form onSubmit={handlePasswordLogin} className="space-y-4">
            <div>
              <label className="block text-xs font-mono text-slate-400 mb-1">Work Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@company.com"
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
                placeholder="••••••••"
                required
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
              {loading ? 'Authenticating...' : 'Sign In'}
            </button>
          </form>
        ) : !otpSent ? (
          <form onSubmit={handleSendOtp} className="space-y-4">
            <div>
              <label className="block text-xs font-mono text-slate-400 mb-1">Work Email for OTP</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@company.com"
                required
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
              {loading ? 'Dispatching OTP...' : 'Send 6-Digit Code'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleVerifyOtp} className="space-y-4">
            <p className="text-xs text-slate-400">
              A 6-digit cryptographic code was sent to <strong className="text-white">{email}</strong>.
            </p>
            <div>
              <label className="block text-xs font-mono text-slate-400 mb-1">Enter 6-Digit Code</label>
              <input
                type="text"
                maxLength={6}
                value={otpCode}
                onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, ''))}
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
              Verify Code & Enter
            </button>
          </form>
        )}

        <div className="mt-6 text-center text-xs text-slate-400">
          Don&apos;t have an account?{' '}
          <a href="/signup" className="text-emerald-400 hover:underline font-mono">
            Create tenant account
          </a>
        </div>
      </div>
    </div>
  );
}

