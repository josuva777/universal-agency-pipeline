import React from 'react';

export const metadata = {
  title: 'Client AI Application',
  description: 'Enterprise AI Agent & Full-Stack Web Application',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-50 antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}

