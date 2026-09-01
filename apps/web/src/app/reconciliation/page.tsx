import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Reconciliation Explorer | AI Finance Controller',
};

export default function Reconciliation() {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col gap-2">
        <h1 className="text-4xl font-bold tracking-tight">Reconciliation Explorer</h1>
        <p className="text-muted-foreground">
          View matching cases across payments, routes, and settlements.
        </p>
      </div>

      <div className="glass-card rounded-2xl p-6">
        <div className="flex justify-between items-center mb-6">
          <div className="flex gap-4">
            <input type="text" placeholder="Search by ID or reference..." className="bg-background border border-white/10 rounded-lg px-4 py-2 text-sm w-64 focus:outline-none focus:ring-2 focus:ring-primary/50" />
            <select className="bg-background border border-white/10 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50">
              <option>All Statuses</option>
              <option>Matched</option>
              <option>Exception</option>
            </select>
          </div>
          <button className="bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
            Run Manual Sync
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-muted-foreground uppercase bg-secondary/50">
              <tr>
                <th className="px-6 py-4 rounded-tl-lg font-semibold">Case ID</th>
                <th className="px-6 py-4 font-semibold">Source (PG)</th>
                <th className="px-6 py-4 font-semibold">Target (Bank)</th>
                <th className="px-6 py-4 font-semibold">Amount</th>
                <th className="px-6 py-4 font-semibold">Route Type</th>
                <th className="px-6 py-4 rounded-tr-lg font-semibold">Status</th>
              </tr>
            </thead>
            <tbody>
              {[
                { id: "CASE-000001", src: "PAY-000001", tgt: "SET-000001", amt: "₹45,670.00", route: "Direct", status: "MATCHED" },
                { id: "CASE-000002", src: "PAY-000002", tgt: "SET-000002", amt: "₹12,400.00", route: "Split (Vendor)", status: "MATCHED" },
                { id: "CASE-000003", src: "PAY-000003", tgt: "SET-000003", amt: "₹8,900.00", route: "Direct", status: "EXCEPTION" },
                { id: "CASE-000004", src: "PAY-000004", tgt: "SET-000004", amt: "₹56,000.00", route: "Split (Platform)", status: "MATCHED" },
              ].map((row, i) => (
                <tr key={i} className="border-b border-white/5 hover:bg-white/5 transition-colors cursor-pointer">
                  <td className="px-6 py-4 font-medium text-primary hover:underline">{row.id}</td>
                  <td className="px-6 py-4 font-mono text-xs">{row.src}</td>
                  <td className="px-6 py-4 font-mono text-xs">{row.tgt}</td>
                  <td className="px-6 py-4">{row.amt}</td>
                  <td className="px-6 py-4">{row.route}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                      row.status === 'MATCHED' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'
                    }`}>
                      {row.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
