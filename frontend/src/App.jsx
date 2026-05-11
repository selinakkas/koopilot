import { useEffect, useState } from "react";

function App() {
  const [dashboard, setDashboard] = useState(null);
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [message, setMessage] = useState("");
  const [chatResponse, setChatResponse] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/dashboard/summary")
      .then((res) => res.json())
      .then((data) => setDashboard(data))
      .catch((err) => console.error(err));

    fetch("http://127.0.0.1:8000/orders/")
      .then((res) => res.json())
      .then((data) => setOrders(data))
      .catch((err) => console.error(err));

    fetch("http://127.0.0.1:8000/products/")
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error(err));
  }, []);

  const handleChat = async () => {
    if (!message.trim()) return;

    try {
      const response = await fetch("http://127.0.0.1:8000/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      setChatResponse(data.answer);
    } catch (error) {
      console.error(error);
      setChatResponse("Something went wrong while contacting the assistant.");
    }
  };

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
                <h2 className="text-zinc-400 text-sm mb-2">Total Orders</h2>
                <p className="text-4xl font-bold">{dashboard.total_orders}</p>
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
              <h2 className="text-2xl font-semibold mb-4">Daily AI Summary</h2>
              <p className="text-zinc-300 leading-relaxed">
                {dashboard.daily_summary}
              </p>
            </div>

            <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800 mt-8">
              <h2 className="text-2xl font-semibold mb-4">Recent Orders</h2>

              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="text-zinc-400 border-b border-zinc-800">
                      <th className="py-3">Order ID</th>
                      <th className="py-3">Customer</th>
                      <th className="py-3">Product</th>
                      <th className="py-3">Quantity</th>
                      <th className="py-3">Status</th>
                    </tr>
                  </thead>

                  <tbody>
                    {orders.map((order) => (
                      <tr key={order.id} className="border-b border-zinc-800">
                        <td className="py-3">#{order.id}</td>
                        <td className="py-3">{order.customer}</td>
                        <td className="py-3">{order.product}</td>
                        <td className="py-3">{order.quantity}</td>
                        <td className="py-3">
                          <span
                            className={`px-3 py-1 rounded-full text-sm ${
                              order.status === "Delayed"
                                ? "bg-red-500/20 text-red-300"
                                : order.status === "Shipped"
                                ? "bg-blue-500/20 text-blue-300"
                                : "bg-zinc-800 text-zinc-300"
                            }`}
                            >
                              {order.status}
                            </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800 mt-8">
              <h2 className="text-2xl font-semibold mb-4">Inventory Status</h2>

              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="text-zinc-400 border-b border-zinc-800">
                      <th className="py-3">Product</th>
                      <th className="py-3">Stock</th>
                      <th className="py-3">Critical Level</th>
                      <th className="py-3">Status</th>
                    </tr>
                  </thead>

                  <tbody>
                    {products.map((product) => {
                      const isCritical = product.stock <= product.critical_stock;

                      return (
                        <tr
                          key={product.id}
                          className="border-b border-zinc-800"
                        >
                          <td className="py-3">{product.name}</td>
                          <td className="py-3">{product.stock}</td>
                          <td className="py-3">{product.critical_stock}</td>
                          <td className="py-3">
                            <span
                              className={`px-3 py-1 rounded-full text-sm ${
                                isCritical
                                  ? "bg-yellow-500/20 text-yellow-300"
                                  : "bg-green-500/20 text-green-300"
                              }`}
                            >
                              {isCritical ? "Critical" : "Healthy"}
                            </span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800 mt-8">
              <h2 className="text-2xl font-semibold mb-4">
                AI Operations Assistant
              </h2>

              <div className="flex gap-4">
                <input
                  type="text"
                  placeholder="Ask about orders, stock or shipments..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  className="flex-1 bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 outline-none"
                />

                <button
                  onClick={handleChat}
                  className="bg-white text-black px-6 py-3 rounded-xl font-semibold hover:bg-zinc-300 transition"
                >
                  Ask AI
                </button>
              </div>

              {chatResponse && (
                <div className="mt-6 bg-zinc-800 rounded-xl p-4 border border-zinc-700">
                  <p className="text-zinc-200 leading-relaxed">
                    {chatResponse}
                  </p>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;