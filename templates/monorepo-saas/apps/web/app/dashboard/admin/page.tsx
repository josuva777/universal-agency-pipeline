'use client';
import React, { useState } from 'react';
import { useTheme } from '@repo/ui';

export default function AdminCenterPage() {
  const { currentTheme } = useTheme();
  // Simulated logged-in user email
  const [currentUserEmail, setCurrentUserEmail] = useState('josuva732006@gmail.com');
  const [emergencyKillActive, setEmergencyKillActive] = useState(false);

  const isMasterAdmin = currentUserEmail === 'josuva732006@gmail.com';

  // Rule 7 & 9: HTTP 403 Access Denied Lockscreen for Non-Admins
  if (!isMasterAdmin) {
    return (
      <div
        className="min-h-screen flex items-center justify-center p-4 text-center"
        style={{ backgroundColor: currentTheme.surface, color: currentTheme.textPrimary }}
      >
        <div
          className="max-w-md w-full p-8 rounded-2xl border shadow-2xl"
          style={{ backgroundColor: currentTheme.surfaceRaised, borderColor: currentTheme.border }}
        >
          <div className="w-16 h-16 rounded-full mx-auto mb-4 bg-red-500/10 border border-red-500/20 text-red-400 flex items-center justify-center text-2xl font-bold font-mono">
            403
          </div>
          <h1 className="text-xl font-bold font-mono text-red-400">Access Denied</h1>
          <p className="text-xs text-slate-400 mt-2 leading-relaxed">
            Enterprise Admin Center requires Supreme Master Admin authority (<code className="text-white">josuva732006@gmail.com</code>). Your current role does not possess elevation privileges.
          </p>
          <div className="mt-6 flex flex-col gap-2">
            <button
              onClick={() => setCurrentUserEmail('josuva732006@gmail.com')}
              className="text-xs text-slate-500 hover:text-slate-400 font-mono"
            >
              (Simulate Login as Master Admin)
            </button>
            <a
              href="/dashboard"
              className="px-4 py-2.5 rounded-xl text-xs font-bold font-mono text-slate-950 transition-all shadow"
              style={{ backgroundColor: currentTheme.accent }}
            >
              Return to User Dashboard
            </a>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: currentTheme.surface, color: currentTheme.textPrimary }}>
      {/* Admin Header */}
      <header className="border-b h-16 flex items-center justify-between px-6 sticky top-0 z-40" style={{ backgroundColor: currentTheme.surface, borderColor: currentTheme.border }}>
        <div className="flex items-center gap-3">
          <a href="/dashboard" className="text-xs text-slate-400 hover:text-white font-mono">← Dashboard</a>
          <span className="text-slate-600">/</span>
          <h1 className="font-extrabold font-mono text-sm tracking-tight text-red-400">
            Supreme Master Admin Center
          </h1>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xs font-mono text-slate-400">Logged in: <strong className="text-white">josuva732006@gmail.com</strong></span>
          <button
            onClick={() => setCurrentUserEmail('dev@external.com')}
            className="text-xs text-slate-500 hover:text-red-400 font-mono"
          >
            Test Lockout
          </button>
        </div>
      </header>

      {/* Admin Panel Body */}
      <main className="flex-1 p-6 max-w-7xl mx-auto w-full space-y-8">
        {/* Emergency Kill-Switch Bar */}
        <div className="p-6 rounded-2xl border border-red-500/30 bg-red-500/5 flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-red-500 animate-ping" />
              <h2 className="text-base font-bold font-mono text-red-400">Global Fleet Kill-Switch</h2>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Immediately revokes all active tenant agent sessions and freezes automated tool calls globally.
            </p>
          </div>

          <button
            onClick={() => setEmergencyKillActive(!emergencyKillActive)}
            className={`px-5 py-2.5 rounded-xl font-mono font-bold text-xs uppercase tracking-wider transition-all shadow-lg ${
              emergencyKillActive ? 'bg-red-500 text-white animate-pulse' : 'bg-red-500/20 text-red-400 border border-red-500/30 hover:bg-red-500/30'
            }`}
          >
            {emergencyKillActive ? 'EMERGENCY SHUTDOWN ACTIVE' : 'Arm Global Kill-Switch'}
          </button>
        </div>

        {/* Multi-Tenant Governance Table */}
        <div className="p-6 rounded-2xl border" style={{ backgroundColor: currentTheme.surfaceRaised, borderColor: currentTheme.border }}>
          <h3 className="text-base font-bold font-mono mb-4">Enterprise Tenants & Roles</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead>
                <tr className="border-b text-slate-400" style={{ borderColor: currentTheme.border }}>
                  <th className="pb-3">Tenant Name</th>
                  <th className="pb-3">Admin Email</th>
                  <th className="pb-3">Active Tier</th>
                  <th className="pb-3">Calls Used</th>
                  <th className="pb-3">Status</th>
                  <th className="pb-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y" style={{ borderColor: currentTheme.border }}>
                <tr>
                  <td className="py-3 font-bold text-white">Acme Corp Security</td>
                  <td className="py-3 text-slate-300">security@acmecorp.com</td>
                  <td className="py-3 text-emerald-400">ENTERPRISE</td>
                  <td className="py-3 text-slate-300">842,100 / 1,000,000</td>
                  <td className="py-3"><span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400">ACTIVE</span></td>
                  <td className="py-3 text-right">
                    <button className="text-xs text-red-400 hover:underline">Suspend</button>
                  </td>
                </tr>
                <tr>
                  <td className="py-3 font-bold text-white">Apex FinTech</td>
                  <td className="py-3 text-slate-300">dev@apexfinance.io</td>
                  <td className="py-3 text-blue-400">TEAM</td>
                  <td className="py-3 text-slate-300">124,500 / 500,000</td>
                  <td className="py-3"><span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400">ACTIVE</span></td>
                  <td className="py-3 text-right">
                    <button className="text-xs text-red-400 hover:underline">Suspend</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
