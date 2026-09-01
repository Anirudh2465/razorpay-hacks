import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'AI Q&A | AI Finance Controller',
};

export default function QA() {
  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col gap-6 animate-in fade-in duration-500">
      <div className="flex flex-col gap-1">
        <h1 className="text-3xl font-bold tracking-tight">AI Finance Assistant</h1>
        <p className="text-muted-foreground text-sm">
          Ask questions about discrepancies, vendor payouts, or Razorpay Route rules.
        </p>
      </div>

      <div className="flex-1 glass-card rounded-2xl flex flex-col overflow-hidden">
        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          <div className="flex justify-center">
            <span className="text-xs text-muted-foreground bg-white/5 px-3 py-1 rounded-full">Today</span>
          </div>
          
          <div className="flex gap-4 max-w-3xl">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-blue-600 flex items-center justify-center shrink-0">
              <span className="font-bold text-white text-xs">AI</span>
            </div>
            <div className="glass px-5 py-4 rounded-2xl rounded-tl-sm">
              <p className="text-sm">Hello! I am your AI Finance Controller. I can investigate reconciliation exceptions, query the financial graph, and answer questions about Razorpay payouts. How can I help you today?</p>
            </div>
          </div>
          
          <div className="flex gap-4 max-w-3xl self-end ml-auto flex-row-reverse">
             <div className="w-8 h-8 rounded-full bg-secondary border border-white/10 flex items-center justify-center shrink-0">
              <span className="text-xs font-semibold">FC</span>
            </div>
            <div className="bg-primary/20 border border-primary/30 px-5 py-4 rounded-2xl rounded-tr-sm">
              <p className="text-sm">Why did vendor VEND-402 receive a negative balance adjustment yesterday?</p>
            </div>
          </div>
          
          <div className="flex gap-4 max-w-3xl">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-blue-600 flex items-center justify-center shrink-0">
              <span className="font-bold text-white text-xs">AI</span>
            </div>
            <div className="glass px-5 py-4 rounded-2xl rounded-tl-sm space-y-4 w-full">
              <p className="text-sm">I've analyzed the graph for vendor <strong>VEND-402</strong>.</p>
              <p className="text-sm">The negative balance adjustment was caused by a post-payout refund for payment <strong>PAY-000042</strong>.</p>
              
              <div className="bg-background/50 border border-white/10 rounded-xl p-4 mt-2">
                <h4 className="text-xs font-semibold uppercase text-muted-foreground mb-3">Evidence Path</h4>
                <div className="space-y-2 font-mono text-xs text-primary/80">
                  <div>(Customer) -[ISSUED]-&gt; (INV-000042)</div>
                  <div>(INV-000042) &lt;-[PAYS]- (PAY-000042)</div>
                  <div>(PAY-000042) -[TRANSFERRED_TO]-&gt; (VEND-402 linked_account)</div>
                  <div className="text-rose-400 border-l-2 border-rose-500 pl-2 ml-2 my-2 py-1">
                    (PAY-000042) -[REFUNDED]-&gt; (REF-000042)<br/>
                    Status: processed | Amount: ₹25,000.00
                  </div>
                  <div>(REF-000042) -[RECOVERS_FROM]-&gt; (VEND-402 future_settlement)</div>
                </div>
              </div>
              
              <p className="text-sm">Since the vendor's split was already paid out via RazorpayX, the Route split calculator generated a negative balance of ₹25,000.00 to be recovered from their next settlement.</p>
            </div>
          </div>
        </div>
        
        {/* Input Area */}
        <div className="p-4 bg-background/50 border-t border-white/5">
          <div className="relative">
            <input 
              type="text" 
              placeholder="Ask anything about your financial data..." 
              className="w-full bg-secondary/30 border border-white/10 rounded-xl pl-4 pr-12 py-4 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
            />
            <button className="absolute right-2 top-1/2 -translate-y-1/2 w-8 h-8 bg-primary rounded-lg flex items-center justify-center hover:bg-primary/90 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
            </button>
          </div>
          <div className="flex gap-2 mt-3 overflow-x-auto pb-1">
            <span className="text-xs bg-white/5 hover:bg-white/10 cursor-pointer px-3 py-1.5 rounded-full transition-colors whitespace-nowrap">Investigate Exception CASE-000003</span>
            <span className="text-xs bg-white/5 hover:bg-white/10 cursor-pointer px-3 py-1.5 rounded-full transition-colors whitespace-nowrap">Show Route split rules for PG Fee</span>
            <span className="text-xs bg-white/5 hover:bg-white/10 cursor-pointer px-3 py-1.5 rounded-full transition-colors whitespace-nowrap">Summarize yesterday's settlements</span>
          </div>
        </div>
      </div>
    </div>
  );
}
