import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Dashboard | AI Finance Controller',
};

export default function Dashboard() {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col gap-2">
        <h1 className="text-4xl font-bold tracking-tight">Overview</h1>
        <p className="text-muted-foreground">
          Real-time financial reconciliation and AI insights.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Total Processed" value="₹24.5M" trend="+12%" isPositive />
        <MetricCard title="Reconciliation Rate" value="98.2%" trend="+0.5%" isPositive />
        <MetricCard title="Active Exceptions" value="14" trend="-3" isPositive />
        <MetricCard title="Route Split Fee" value="₹1.2M" trend="Expected" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 glass-card rounded-2xl p-6 h-[400px] flex flex-col relative overflow-hidden">
          <div className="absolute top-0 right-0 p-32 bg-primary/10 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none" />
          <h2 className="text-lg font-semibold mb-4">Reconciliation Flow</h2>
          <div className="flex-1 border border-white/10 rounded-xl bg-background/50 flex items-center justify-center">
            <span className="text-muted-foreground">Graph / Chart Visualization Area</span>
          </div>
        </div>

        <div className="glass-card rounded-2xl p-6 h-[400px] flex flex-col">
          <h2 className="text-lg font-semibold mb-4">Recent Exceptions</h2>
          <div className="flex-1 space-y-4 overflow-auto pr-2">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="p-4 rounded-xl bg-secondary/50 border border-white/5 hover:bg-secondary/80 transition-colors cursor-pointer group">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-sm font-medium text-rose-400 group-hover:text-rose-300">Fee Mismatch</span>
                  <span className="text-xs text-muted-foreground">2m ago</span>
                </div>
                <p className="text-sm">Payment PAY-00{i} settlement differs by ₹20.50 from expected.</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ title, value, trend, isPositive }: { title: string, value: string, trend: string, isPositive?: boolean }) {
  return (
    <div className="glass-card p-6 rounded-2xl relative overflow-hidden group hover:scale-[1.02] transition-transform duration-300 cursor-pointer">
      <div className="absolute -right-12 -top-12 w-32 h-32 bg-primary/10 rounded-full blur-2xl group-hover:bg-primary/20 transition-colors" />
      <h3 className="text-sm font-medium text-muted-foreground mb-2">{title}</h3>
      <div className="flex items-baseline gap-3">
        <span className="text-3xl font-bold">{value}</span>
        <span className={`text-xs font-semibold px-2 py-1 rounded-full ${
          isPositive === true ? 'bg-emerald-500/10 text-emerald-400' : 
          isPositive === false ? 'bg-rose-500/10 text-rose-400' : 
          'bg-white/5 text-muted-foreground'
        }`}>
          {trend}
        </span>
      </div>
    </div>
  );
}
