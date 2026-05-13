import { useEffect, useState } from "react";
import API_BASE from "./config";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell, LabelList
} from "recharts";

function App() {
  // Selin'in Tüm State Altyapısı (Eksiksiz)
  const [dashboard, setDashboard] = useState(null);
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [aiSummary, setAiSummary] = useState("");
  const [predictions, setPredictions] = useState([]);
  const [actionPlan, setActionPlan] = useState([]);
  const [isAsking, setIsAsking] = useState(false);
  const [complaint, setComplaint] = useState("");
  const [complaintResult, setComplaintResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [selectedRole, setSelectedRole] = useState("owner");
  
  // UI Kontrol State'leri
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [showWelcomeMessage, setShowWelcomeMessage] = useState(false);
  const [showAllOrderNotifs, setShowAllOrderNotifs] = useState(false);
  const [showAllStockNotifs, setShowAllStockNotifs] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [dashRes, ordersRes, productsRes, aiRes, predRes, planRes] = await Promise.all([
          fetch(`${API_BASE}/dashboard/summary`),
          fetch(`${API_BASE}/orders/`),
          fetch(`${API_BASE}/products/`),
          fetch(`${API_BASE}/dashboard/ai-summary`),
          fetch(`${API_BASE}/predictions/`),
          fetch(`${API_BASE}/dashboard/action-plan`)
        ]);

        setDashboard(await dashRes.json());
        setOrders(await ordersRes.json());
        setProducts(await productsRes.json());
        const aiData = await aiRes.json();
        setAiSummary(aiData.summary);
        setPredictions(await predRes.json());
        setActionPlan(await planRes.json());
      } catch (err) { console.error("API Connection Error:", err); }
    };

    if (isLoggedIn) {
      fetchData();
      const timer = setTimeout(() => {
        const audio = new Audio("https://assets.mixkit.co/active_storage/sfx/2358/2358-preview.mp3");
        audio.play().catch(() => {});
        setShowWelcomeMessage(true);
        setTimeout(() => setShowWelcomeMessage(false), 8000);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [isLoggedIn]);

  // Selin'in Fonksiyonları (Eksiksiz)
  const handleChat = async (q = null) => {
    const msg = q || message;
    if (!msg.trim() || isAsking) return;
    setIsAsking(true); setMessage("");
    setChatHistory(prev => [...prev, { role: "user", content: msg }]);
    try {
      const res = await fetch(`${API_BASE}/chat/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg }),
      });
      const data = await res.json();
      setChatHistory(prev => [...prev, { role: "assistant", content: data.answer }]);
    } finally { setIsAsking(false); }
  };

  const handleSimulateComplaint = async () => {
    if (!complaint) return;
    setIsAnalyzing(true);
    try {
      const res = await fetch(`${API_BASE}/complaints/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: complaint })
      });
      setComplaintResult(await res.json());
    } finally { setIsAnalyzing(false); }
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-[#0f172a]/95 border border-[#A5D8FF]/30 p-4 rounded-2xl backdrop-blur-md shadow-2xl">
          <p className="text-[#A5D8FF] font-black text-xs uppercase mb-1">{payload[0].payload.name}</p>
          <p className="text-white text-lg font-bold italic">Stock: {payload[0].value}</p>
        </div>
      );
    }
    return null;
  };

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-[#020617] text-white flex flex-col items-center justify-center p-8 font-sans overflow-hidden">
        <div className="fixed top-12 left-12 text-6xl font-black tracking-tighter text-white">Koo.</div>
        <div className="relative z-10 text-center animate-in fade-in duration-1000">
          <h1 className="text-8xl font-extralight tracking-tighter mb-4 text-white">Welcome to <span className="font-bold">Koopilot</span></h1>
          <p className="text-slate-500 mb-20 text-sm font-light tracking-[0.6em] uppercase italic">Intelligence for Excellence</p>
          <div className="flex flex-row gap-10">
            {[
              { id: "owner", label: "Executive Dashboard", desc: "Full Operational Intelligence & AI Action Plans" },
              { id: "warehouse", label: "Warehouse View", desc: "Inventory Management & Predictive Stock Alerts" },
              { id: "support", label: "Support View", desc: "Customer Sentiment & Complaint Simulation" },
            ].map((role) => (
              <button
                key={role.id}
                onClick={() => { setSelectedRole(role.id); setIsLoggedIn(true); }}
                className="group relative w-80 bg-white/[0.03] border border-white/10 rounded-[3rem] p-12 transition-all duration-700 hover:bg-[#A5D8FF]/5 hover:border-[#A5D8FF]/50 hover:shadow-[0_0_60px_rgba(165,216,255,0.2)] hover:-translate-y-4 backdrop-blur-3xl active:scale-95"
              >
                <p className="relative font-bold text-xl mb-4 text-white group-hover:text-[#A5D8FF] transition-colors">{role.label}</p>
                <p className="relative text-[12px] text-slate-300 font-medium leading-relaxed tracking-tight group-hover:text-slate-100">{role.desc}</p>
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#020617] text-slate-200 p-12 font-sans selection:bg-[#A5D8FF]/30">
      <div className="fixed top-12 left-12 text-6xl font-black tracking-tighter text-white z-50">Koo.</div>
      
      <div className="max-w-6xl mx-auto pt-14 pb-32">
        <header className="flex justify-between items-end mb-16 border-b border-white/5 pb-10">
          <div>
            <h1 className="text-3xl font-black tracking-tighter text-white capitalize">{selectedRole.replace('-', ' ')}</h1>
            <p className="text-[#A5D8FF]/40 text-[9px] font-bold uppercase tracking-[0.3em] mt-1 italic">Operations Intelligence</p>
          </div>
          <div className="flex gap-2 p-1 bg-white/5 rounded-full border border-white/5">
             {["owner", "warehouse", "support"].map(role => (
               <button key={role} onClick={() => setSelectedRole(role)} className={`px-5 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest transition-all ${selectedRole === role ? 'bg-[#A5D8FF] text-[#020617] shadow-lg shadow-[#A5D8FF]/20' : 'text-slate-500 hover:text-white'}`}>{role}</button>
             ))}
          </div>
        </header>

        <main className="space-y-12">
          {/* TOP STATS */}
          <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white/5 border border-white/10 p-8 rounded-[2.5rem] backdrop-blur-sm">
               <p className="text-slate-500 text-[9px] font-black uppercase tracking-widest mb-4">Total Orders</p>
               <p className="text-7xl font-extralight tracking-tighter text-white">{dashboard?.total_orders || 0}</p>
            </div>
            <div className="bg-red-500/5 border border-red-500/10 p-8 rounded-[2.5rem] group hover:bg-red-500/10 transition-all cursor-pointer">
               <p className="text-red-400 text-[9px] font-black uppercase tracking-widest mb-4 group-hover:animate-pulse">Delayed Shipments</p>
               <p className="text-7xl font-extralight tracking-tighter text-red-500">{dashboard?.delayed_shipments || 0}</p>
            </div>
            <div className="bg-yellow-500/5 border border-yellow-500/10 p-8 rounded-[2.5rem] group hover:bg-yellow-500/10 transition-all cursor-pointer">
               <p className="text-yellow-400 text-[9px] font-black uppercase tracking-widest mb-4 group-hover:animate-pulse">Critical Products</p>
               <p className="text-7xl font-extralight tracking-tighter text-yellow-500">{dashboard?.critical_products || 0}</p>
            </div>
          </section>

          {/* SMART NOTIFICATIONS (Selin'in Verileri) */}
          <section className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="space-y-4 text-center">
              <div className="bg-[#1e293b] border border-[#A5D8FF]/20 p-5 rounded-2xl text-[10px] font-black uppercase tracking-[0.3em] text-[#A5D8FF]">Smart Notification for Orders</div>
              <div className="space-y-2 text-left">
                {orders.filter(o => o.status === 'Delayed').slice(0, showAllOrderNotifs ? undefined : 3).map(o => (
                  <div key={o.id} className="bg-red-500/5 border border-red-500/10 p-4 rounded-xl flex justify-between items-center group transition-all">
                    <span className="text-[11px] font-medium text-red-100/70">Order #{o.id} — {o.customer}</span>
                    <span className="bg-red-600/20 text-red-400 text-[7px] font-black px-2 py-0.5 rounded-full uppercase italic">Delayed</span>
                  </div>
                ))}
                {orders.filter(o => o.status === 'Delayed').length > 3 && (
                  <button onClick={() => setShowAllOrderNotifs(!showAllOrderNotifs)} className="w-full text-center text-[9px] font-bold text-slate-500 uppercase tracking-widest pt-2 hover:text-white transition-all underline underline-offset-4 decoration-white/10">
                    {showAllOrderNotifs ? "Show Less" : "Show All Delayed Orders"}
                  </button>
                )}
              </div>
            </div>

            <div className="space-y-4 text-center">
              <div className="bg-[#1e293b] border border-[#A5D8FF]/20 p-5 rounded-2xl text-[10px] font-black uppercase tracking-[0.3em] text-[#A5D8FF]">Smart Notification for Stocks</div>
              <div className="space-y-2 text-left">
                {products.filter(p => p.stock <= p.critical_stock).slice(0, showAllStockNotifs ? undefined : 3).map(p => (
                  <div key={p.id} className="bg-yellow-500/5 border border-yellow-500/10 p-4 rounded-xl flex justify-between items-center group transition-all hover:bg-yellow-500/10">
                    <span className="text-[11px] font-medium text-yellow-100/60">{p.name}</span>
                    <span className="bg-yellow-600/20 text-yellow-400 text-[7px] font-black px-2 py-0.5 rounded-full uppercase italic">Low Stock: {p.stock}</span>
                  </div>
                ))}
                {products.filter(p => p.stock <= p.critical_stock).length > 3 && (
                  <button onClick={() => setShowAllStockNotifs(!showAllStockNotifs)} className="w-full text-center text-[9px] font-bold text-slate-500 uppercase tracking-widest pt-2 hover:text-white transition-all underline underline-offset-4 decoration-white/10">
                    {showAllStockNotifs ? "Show Less" : "Show All Stock Alerts"}
                  </button>
                )}
              </div>
            </div>
          </section>

          {/* SELİN'İN AI INSIGHTS BÖLÜMÜ (OWNER ÖZEL) */}
          {selectedRole === "owner" && (
            <section className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="bg-white/5 border border-white/5 p-10 rounded-[3rem]">
                <h2 className="text-xl font-black mb-6 text-white underline decoration-[#A5D8FF]/30 underline-offset-4 font-sans">Daily AI Summary</h2>
                <p className="text-slate-300 text-lg font-light italic leading-relaxed">
                  {aiSummary.split(' ').map((word, i) => i % 6 === 0 ? <b key={i} className="text-white font-bold">{word} </b> : word + ' ')}
                </p>
                <button
                  onClick={async () => {
                    const res = await fetch(`${API_BASE}/dashboard/report`);
                    const blob = await res.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = `koopilot_report_${new Date().toISOString().slice(0,10)}.pdf`;
                    a.click();
                    window.URL.revokeObjectURL(url);
                  }}
                  className="mt-8 bg-white text-[#020617] px-6 py-2.5 rounded-2xl font-black uppercase text-[10px] hover:bg-[#A5D8FF] transition-all">
                  Download Report
                </button>
              </div>
              <div className="bg-white/5 border border-white/5 p-10 rounded-[3rem]">
                <h2 className="text-xl font-black mb-6 text-white underline decoration-[#A5D8FF]/30 underline-offset-4 font-sans">AI Daily Action Plan</h2>
                <div className="space-y-4">
                  {actionPlan.slice(0, 3).map((item, i) => (
                    <div key={i} className={`p-5 rounded-2xl border flex justify-between items-center ${item.priority === 'High' ? 'bg-red-500/5 border-red-500/10' : 'bg-[#A5D8FF]/5 border-[#A5D8FF]/10'}`}>
                      <p className="text-sm font-semibold italic text-slate-200"><span className="mr-3">{i === 0 ? '🚀' : '📋'}</span>{item.action}</p>
                      <span className={`text-[8px] font-black px-2 py-1 rounded-full uppercase ${item.priority === 'High' ? 'bg-red-500 text-white' : 'bg-[#A5D8FF] text-[#020617]'}`}>{item.priority}</span>
                    </div>
                  ))}
                </div>
              </div>
            </section>
          )}

          {/* INVENTORY ANALYTICS - Yazılar Tam Tepede */}
          <section className="bg-white/5 border border-white/5 p-10 rounded-[3rem]">
            <h2 className="text-xl font-black mb-16 tracking-tighter italic text-white underline decoration-white/10 underline-offset-8">Inventory Analytics</h2>
            <div className="h-[500px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={products} margin={{ top: 30, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} opacity={0.2} />
                  <XAxis axisLine={false} tick={false} />
                  <YAxis stroke="#475569" fontSize={10} tickLine={false} axisLine={false} />
                  <Tooltip content={<CustomTooltip />} cursor={{fill: 'rgba(165, 216, 255, 0.05)'}} />
                  <Bar dataKey="stock" radius={[4, 4, 0, 0]}>
                    <LabelList 
                      dataKey="name" 
                      position="top" 
                      content={(props) => {
                        const { x, y, width, value, index } = props;
                        const product = products[index];
                        const isCritical = product && product.stock <= product.critical_stock;
                        const words = value.split(' ');
                        const firstWord = words[0];
                        const secondWord = words.slice(1).join(' ');
                        return (
                          <text x={x + width / 2} y={y - 5} textAnchor="middle" fontSize={11.5} fontWeight={isCritical ? "bold" : "600"}>
                            <tspan x={x + width / 2} dy={0} fill={isCritical ? "#ef4444" : "#A5D8FF"}>{firstWord}</tspan>
                            {secondWord && <tspan x={x + width / 2} dy={12} fill={isCritical ? "#ef4444" : "#A5D8FF"}>{secondWord}</tspan>}
                          </text>
                        );
                      }}
                    />
                    {products.map((e, i) => <Cell key={i} fill={e.stock <= e.critical_stock ? '#ef4444' : '#06b6d4'} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </section>

          {/* PREDICTIVE INTELLIGENCE (Selin'in Verileri) */}
          <section className="bg-white/[0.02] border border-white/5 p-12 rounded-[3.5rem] backdrop-blur-2xl">
            <h2 className="text-base font-black uppercase tracking-[0.5em] mb-12 text-center text-white italic underline decoration-white/20 underline-offset-8">Predictive Intelligence</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
              <div><p className="text-red-400/50 text-[10px] font-black uppercase tracking-[0.2em] border-b border-red-500/30 pb-3 mb-6">Critical Alerts</p>{predictions.filter(p => p.type === 'critical').slice(0, 3).map((p, i) => <p key={i} className="text-sm text-slate-200 font-medium mb-3 leading-relaxed italic">{p.message}</p>)}</div>
              <div><p className="text-yellow-400/50 text-[10px] font-black uppercase tracking-[0.2em] border-b border-yellow-500/30 pb-3 mb-6">Standard Warnings</p>{predictions.filter(p => p.type !== 'critical').slice(0, 3).map((p, i) => <p key={i} className="text-sm text-slate-200 font-medium mb-3 leading-relaxed italic">{p.message}</p>)}</div>
              <div className="bg-[#A5D8FF]/5 p-8 rounded-3xl border border-[#A5D8FF]/10 flex flex-col items-center justify-center"><p className="text-[#A5D8FF] text-[10px] font-black uppercase tracking-widest mb-4 italic">Recommend Action</p><p className="text-sm text-[#A5D8FF] font-medium italic">"Koosistan recommends real-time cargo optimization for delayed batches."</p></div>
            </div>
          </section>

          {/* SUPPORT VIEW (Selin'in Şikayet Simülatörü) */}
          {selectedRole === "support" && (
            <section className="bg-white/5 border border-white/10 p-12 rounded-[3.5rem] animate-in slide-in-from-bottom-5">
              <h2 className="text-xl font-black mb-1 text-white underline decoration-[#A5D8FF]/30 underline-offset-4 tracking-tighter font-sans">Customer Complaint Simulator</h2>
              <p className="text-slate-500 text-[10px] mb-8 uppercase tracking-widest italic font-sans">Simulate with <span className="text-[#A5D8FF] font-bold">Koosistan</span> Intelligence</p>
              <div className="max-w-2xl mx-auto space-y-6 text-center">
                <textarea value={complaint} onChange={(e) => setComplaint(e.target.value)} placeholder="Type customer complaint here..." className="w-full h-32 bg-black/40 border border-white/5 rounded-2xl p-6 text-slate-300 outline-none text-sm font-light mb-6 focus:border-[#A5D8FF]/30 transition-all italic" />
                <button onClick={handleSimulateComplaint} className="bg-[#A5D8FF] text-[#020617] px-10 py-3 rounded-full font-black uppercase tracking-widest text-[9px] hover:scale-105 active:scale-95 transition-all">Ask Koosistan</button>
                {complaintResult && (
                  <div className="mt-8 p-8 bg-black/40 rounded-2xl border border-white/5 text-left animate-in fade-in">
                    <div className="flex gap-4 mb-4">
                      <span className={`px-4 py-1 rounded-full text-[9px] font-black uppercase tracking-widest ${complaintResult.severity === 'High' ? 'bg-red-500 text-white' : 'bg-green-500 text-black'}`}>Severity: {complaintResult.severity}</span>
                      <span className="bg-slate-800 text-slate-400 px-4 py-1 rounded-full text-[9px] font-black uppercase tracking-widest italic">Category: {complaintResult.category}</span>
                    </div>
                    <p className="text-[#A5D8FF] font-medium italic italic leading-relaxed font-sans">"{complaintResult.ai_response || complaintResult.suggested_action}"</p>
                  </div>
                )}
              </div>
            </section>
          )}
        </main>
      </div>

      {/* KOOSİSTAN GLOBAL CHATBOT */}
      <div className="fixed bottom-10 right-10 z-[100] flex flex-col items-end">
        {showWelcomeMessage && (
          <div className="bg-[#A5D8FF] text-[#020617] px-8 py-5 rounded-[2rem] rounded-br-none mb-6 shadow-2xl animate-in fade-in slide-in-from-right-10 duration-500 font-black text-xs border-4 border-white/20 tracking-tight italic">
            Hi, I'm Koosistan. I'm here if you need any help! 👋
          </div>
        )}
        <button onClick={() => setIsChatOpen(!isChatOpen)} className="w-16 h-16 bg-[#A5D8FF] rounded-full shadow-[0_10px_60px_rgba(165,216,255,0.3)] flex items-center justify-center hover:scale-110 active:scale-95 transition-all duration-300 group"><span className="text-3xl group-hover:rotate-12 transition-transform">🤖</span></button>
        {isChatOpen && (
          <div className="absolute bottom-20 right-0 w-[420px] bg-[#020617] border border-white/10 rounded-[2.5rem] shadow-2xl overflow-hidden flex flex-col animate-in slide-in-from-bottom-10 duration-500 backdrop-blur-3xl">
            <div className="bg-[#A5D8FF] p-8 flex justify-between items-center text-[#020617]">
              <div><p className="font-black text-2xl tracking-tighter">Koosistan</p><p className="text-[9px] font-bold uppercase tracking-widest opacity-60">Ops Intelligence</p></div>
              <button onClick={() => setIsChatOpen(false)} className="bg-black/10 p-2 rounded-full hover:bg-black/20 transition-all">✕</button>
            </div>
            <div className="h-[400px] p-8 overflow-y-auto space-y-4 bg-white/[0.02] text-[11px]">
              <div className="flex flex-wrap gap-2 mb-6 text-center">
                {["Check critical stocks", "Check delayed orders", "Get daily summary"].map(q => <button key={q} onClick={() => handleChat(q)} className="text-[8px] bg-white/5 border border-white/10 px-3 py-1.5 rounded-full hover:bg-[#A5D8FF] hover:text-[#020617] transition-all font-black uppercase tracking-widest">{q}</button>)}
              </div>
              {chatHistory.map((chat, i) => (
                <div key={i} className={`flex ${chat.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`p-4 rounded-[1.5rem] ${chat.role === 'user' ? 'bg-[#A5D8FF] text-[#020617] rounded-tr-none font-bold' : 'bg-white/5 text-slate-100 rounded-tl-none font-light italic border border-white/5 leading-relaxed'}`}>{chat.content}</div>
                </div>
              ))}
            </div>
            <div className="p-6 bg-[#020617] border-t border-white/5 flex gap-3">
              <input value={message} onChange={(e) => setMessage(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && handleChat()} placeholder="Ask Koosistan..." className="flex-1 bg-white/5 border border-white/5 rounded-xl px-5 py-3 text-[11px] outline-none text-slate-300 font-light italic" />
              <button onClick={() => handleChat()} className="bg-[#A5D8FF] text-[#020617] px-6 py-3 rounded-xl font-black uppercase tracking-widest text-[9px] hover:bg-white transition-all active:scale-95 shadow-md">Ask</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;