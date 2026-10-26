import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'danger';
  size?: 'sm' | 'md' | 'lg';
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  className,
  ...props
}) => {
  const base = 'inline-flex items-center justify-center font-semibold transition-all rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 min-h-[44px] min-w-[44px] select-none';
  
  const variants = {
    primary: 'bg-emerald-500 hover:bg-emerald-400 text-slate-950 focus-visible:ring-emerald-400 active:scale-98 shadow-sm',
    secondary: 'bg-slate-800 hover:bg-slate-700 text-slate-100 focus-visible:ring-slate-500 active:scale-98',
    outline: 'border border-slate-700 hover:border-slate-500 text-slate-200 bg-transparent active:scale-98',
    danger: 'bg-rose-600 hover:bg-rose-500 text-white focus-visible:ring-rose-400 active:scale-98',
  };

  const sizes = {
    sm: 'text-xs px-3 py-1.5',
    md: 'text-sm px-4 py-2',
    lg: 'text-base px-6 py-3',
  };

  return (
    <button
      className={twMerge(clsx(base, variants[variant], sizes[size], className))}
      {...props}
    >
      {children}
    </button>
  );
};

