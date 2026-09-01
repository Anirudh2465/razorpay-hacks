import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Financial Graph | AI Finance Controller',
};

export default function Graph() {
  return (
    <div className="space-y-6 h-[calc(100vh-8rem)] flex flex-col animate-in fade-in duration-500">
      <div className="flex flex-col gap-1">
        <h1 className="text-3xl font-bold tracking-tight">Financial Knowledge Graph</h1>
        <p className="text-muted-foreground text-sm">
          Interactive graph visualization of entities and their relationships. Powered by Neo4j.
        </p>
      </div>

      <div className="flex-1 glass-card rounded-2xl relative overflow-hidden flex flex-col">
        {/* Mock Toolbar */}
        <div className="absolute top-4 left-4 z-10 glass px-4 py-2 rounded-lg flex items-center gap-4 text-sm">
          <div className="flex items-center gap-2 cursor-pointer hover:text-primary transition-colors">
            <div className="w-3 h-3 rounded-full bg-blue-500" />
            <span>Customer</span>
          </div>
          <div className="flex items-center gap-2 cursor-pointer hover:text-primary transition-colors">
            <div className="w-3 h-3 rounded-full bg-purple-500" />
            <span>Invoice</span>
          </div>
          <div className="flex items-center gap-2 cursor-pointer hover:text-primary transition-colors">
            <div className="w-3 h-3 rounded-full bg-emerald-500" />
            <span>Payment</span>
          </div>
          <div className="flex items-center gap-2 cursor-pointer hover:text-primary transition-colors">
            <div className="w-3 h-3 rounded-full bg-amber-500" />
            <span>Settlement</span>
          </div>
        </div>

        {/* Search */}
        <div className="absolute top-4 right-4 z-10">
          <input type="text" placeholder="Cypher query or ID search..." className="glass rounded-lg px-4 py-2 text-sm w-80 focus:outline-none focus:ring-2 focus:ring-primary/50" />
        </div>

        {/* Mock Visualization Area */}
        <div className="flex-1 flex items-center justify-center bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-repeat opacity-20" />
        
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="text-center">
            <p className="text-2xl font-bold text-white/40 mb-2">Graph Visualization Area</p>
            <p className="text-sm text-white/30">Connects to Neo4j to render nodes (React Flow / D3.js)</p>
          </div>
        </div>
        
        {/* Connected Nodes Mock Example */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex items-center gap-16 pointer-events-none">
           <div className="w-16 h-16 rounded-full bg-blue-500/20 border-2 border-blue-500 shadow-[0_0_15px_rgba(59,130,246,0.5)] flex items-center justify-center text-xs font-mono">CUS</div>
           <div className="w-16 h-16 rounded-full bg-purple-500/20 border-2 border-purple-500 shadow-[0_0_15px_rgba(168,85,247,0.5)] flex items-center justify-center text-xs font-mono">INV</div>
           <div className="w-16 h-16 rounded-full bg-emerald-500/20 border-2 border-emerald-500 shadow-[0_0_15px_rgba(16,185,129,0.5)] flex items-center justify-center text-xs font-mono">PAY</div>
           <div className="w-16 h-16 rounded-full bg-amber-500/20 border-2 border-amber-500 shadow-[0_0_15px_rgba(245,158,11,0.5)] flex items-center justify-center text-xs font-mono">SET</div>
        </div>
      </div>
    </div>
  );
}
