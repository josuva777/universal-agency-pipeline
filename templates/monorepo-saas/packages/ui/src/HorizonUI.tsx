'use client';
import React from 'react';
import { useTheme } from './ThemeEngine';

export interface HorizonMetricCardProps {
  title: string;
  value: string;
  trend: string;
  isPositive?: boolean;
  icon?: string;
  subtitle?: string;
}

/**
 * Horizon UI Enterprise Metric Card (Horizon Standard)
 * Clean mathematical optical balance, trend pills, and OKLCH dynamic theme styling.
 */
export const HorizonMetricCard: React.FC<HorizonMetricCardProps> = ({
  title,
  value,
  trend,
  isPositive = true,
  icon = '📈',
  subtitle = 'vs. previous 30-day window'
}) => {
  const { currentTheme } = useTheme();

  return (
    <div
      className="p-5 rounded-2xl border transition-all duration-200 hover:scale-[1.01] shadow-lg flex flex-col justify-between"
      style={{
        backgroundColor: currentTheme.surfaceRaised,
        borderColor: currentTheme.border
      }}
    >
      <div className="flex items-center justify-between">
        <span className="text-xs font-mono font-medium text-slate-400 uppercase tracking-wider">{title}</span>
        <div
          className="w-8 h-8 rounded-xl flex items-center justify-center text-sm shadow-inner"
          style={{ backgroundColor: `${currentTheme.accent}15`, color: currentTheme.accent }}
        >
          {icon}
        </div>
      </div>

      <div className="my-3">
        <div className="text-2xl sm:text-3xl font-extrabold font-mono tracking-tight text-white">{value}</div>
      </div>

      <div className="flex items-center justify-between text-xs font-mono pt-2 border-t border-slate-800/60">
        <span
          className={`px-2 py-0.5 rounded-full text-[10px] font-bold flex items-center gap-1 ${
            isPositive ? 'bg-emerald-500/15 text-emerald-400' : 'bg-rose-500/15 text-rose-400'
          }`}
        >
          {isPositive ? '↑' : '↓'} {trend}
        </span>
        <span className="text-[10px] text-slate-500">{subtitle}</span>
      </div>
    </div>
  );
};

export interface HorizonTableColumn<T> {
  header: string;
  accessor: keyof T | ((row: T) => React.ReactNode);
  className?: string;
}

export interface HorizonDataTableProps<T> {
  title: string;
  columns: HorizonTableColumn<T>[];
  data: T[];
  actionLabel?: string;
  onAction?: () => void;
}

/**
 * Horizon UI High-Density Enterprise Data Table
 */
export function HorizonDataTable<T extends { id: string | number }>({
  title,
  columns,
  data,
  actionLabel,
  onAction
}: HorizonDataTableProps<T>) {
  const { currentTheme } = useTheme();

  return (
    <div
      className="rounded-2xl border overflow-hidden shadow-xl"
      style={{
        backgroundColor: currentTheme.surfaceRaised,
        borderColor: currentTheme.border
      }}
    >
      <div className="px-6 py-4 border-b flex items-center justify-between" style={{ borderColor: currentTheme.border }}>
        <h3 className="text-sm font-bold font-mono text-white tracking-wide">{title}</h3>
        {actionLabel && (
          <button
            onClick={onAction}
            className="px-3 py-1.5 rounded-lg text-xs font-mono font-bold transition shadow"
            style={{ backgroundColor: currentTheme.accent, color: '#020617' }}
          >
            {actionLabel}
          </button>
        )}
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead className="bg-slate-950/60 border-b text-slate-400" style={{ borderColor: currentTheme.border }}>
            <tr>
              {columns.map((col, idx) => (
                <th key={idx} className={`py-3 px-6 font-semibold uppercase tracking-wider text-[11px] ${col.className || ''}`}>
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-300">
            {data.map((row) => (
              <tr key={row.id} className="hover:bg-slate-800/30 transition-colors">
                {columns.map((col, cIdx) => (
                  <td key={cIdx} className={`py-3.5 px-6 ${col.className || ''}`}>
                    {typeof col.accessor === 'function' ? col.accessor(row) : (row[col.accessor] as React.ReactNode)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
