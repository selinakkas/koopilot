import { useEffect, useState } from "react";

function App() {
  const [dashboard, setDashboard] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/dashboard/summary")
      .then((res) => res.json())
      .then((data) => setDashboard(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="min-h-screen bg-zinc-950 text-white p-8">
      <div className="max-w-7xl mx-auto">
        
        <div className="mb-10">
          <h1 className="text-5xl font-bold">Koopilot</h1>
          <p className="text-zinc-400 mt-2">
            AI-powered operations copilot for small businesses
          </p>
        </div>

        {!dashboard ? (
          <p>Loading dashboard...</p>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">

              <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800">
                <h2 className="text-zinc-400 text-sm mb-2">
                  Total Orders
                </h2>

                <p className="text-4xl font-bold">
                  {dashboard.total_orders}
                </p>
              </div>

              <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800">
                <h2 className="text-zinc-400 text-sm mb-2">
                  Delayed Shipments
                </h2>

                <p className="text-4xl font-bold text-red-400">
                  {dashboard.delayed_shipments}
                </p>
              </div>

              <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800">
                <h2 className="text-zinc-400 text-sm mb-2">
                  Critical Products
                </h2>

                <p className="text-4xl font-bold text-yellow-400">
                  {dashboard.critical_products}
                </p>
              </div>

            </div>

            <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800">
              <h2 className="text-2xl font-semibold mb-4">
                Daily AI Summary
              </h2>

              <p className="text-zinc-300 leading-relaxed">
                {dashboard.daily_summary}
              </p>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;