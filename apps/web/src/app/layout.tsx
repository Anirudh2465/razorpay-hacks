import type { Metadata } from 'next';
import { Inter, Geist } from 'next/font/google';
import './globals.css';
import Link from 'next/link';
import { cn } from "@/lib/utils";

const geist = Geist({subsets:['latin'],variable:'--font-sans'});

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'AI Finance Controller',
  description: 'Graph-powered finance-operations platform',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={cn("dark", "font-sans", geist.variable)}>
      <body className={`${inter.className} min-h-screen flex flex-col`}>
        <nav className="glass sticky top-0 z-50 w-full px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-blue-600 flex items-center justify-center shadow-lg shadow-primary/20">
              <span className="font-bold text-white text-xl">A</span>
            </div>
            <span className="font-bold text-xl tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-white/70">
              Finance Controller
            </span>
          </div>
          <div className="flex items-center gap-6">
            <Link href="/" className="text-sm font-medium text-white/70 hover:text-white transition-colors">Dashboard</Link>
            <Link href="/reconciliation" className="text-sm font-medium text-white/70 hover:text-white transition-colors">Reconciliation</Link>
            <Link href="/graph" className="text-sm font-medium text-white/70 hover:text-white transition-colors">Graph</Link>
            <Link href="/qa" className="text-sm font-medium text-white/70 hover:text-white transition-colors">AI Q&A</Link>
            <div className="w-8 h-8 rounded-full bg-secondary border border-white/10 flex items-center justify-center">
              <span className="text-xs font-semibold">FC</span>
            </div>
          </div>
        </nav>
        <main className="flex-1 max-w-7xl w-full mx-auto p-6 md:p-8">
          {children}
        </main>
      </body>
    </html>
  );
}
