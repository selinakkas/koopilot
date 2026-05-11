import { useEffect, useState } from "react";

function App() {
  const [dashboard, setDashboard] = useState(null);
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [aiSummary, setAiSummary] = useState("");
  const [isAsking, setIsAsking] = useState(false);

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

    fetch("http://127.0.0.1:8000/dashboard/ai-summary")
      .then((res) => res.json())
      .then((data) => setAiSummary(data.summary))
      .catch((err) => console.error(err));
  }, []);

  const handleChat = async () => {
    if (!message.trim() || isAsking) return;

    const userMessage = message;

    setIsAsking(true);
    setMessage("");

    setChatHistory((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
        }),
      });

      const data = await response.json();

      setChatHistory((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch (error) {
      console.error(error);

      setChatHistory((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Something went wrong.",
        },
      ]);
    } finally {
      setIsAsking(false);
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
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                </div>
              </div>
            </div>

            <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-800">
              <h2 className="text-2xl font-semibold mb-4">
                Daily AI Summary
              </h2>

              <p className="text-zinc-300 leading-relaxed">
                {aiSummary || dashboard.daily_summary}
              </p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                <div className="bg-zinc-800 rounded-xl p-4 border border-zinc-700">
                  <p className="text-sm text-zinc-400 mb-1">
                    Recommended Action
                  </p>

                  <p className="font-semibold">
                    Restock critical products
                  </p>
                </div>

                <div className="bg-zinc-800 rounded-xl p-4 border border-zinc-700">
                  <p className="text-sm text-zinc-400 mb-1">
                    Priority
                  </p>

                  <p className="font-semibold text-yellow-300">
                    Medium
                  </p>
                </div>

                <div className="bg-zinc-800 rounded-xl p-4 border border-zinc-700">
                  <p className="text-sm text-zinc-400 mb-1">
                    Shipment Follow-up
                  </p>

                  <p className="font-semibold text-red-300">
                    1 delayed order
                  </p>
                </div>
              </div>
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
                      const isCritical =
                        product.stock <= product.critical_stock;

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
              <div className="flex flex-wrap gap-3 mb-4">
                {[
                  "Where is order 128?",
                  "Which products are low in stock?",
                  "Which orders are delayed?",
                ].map((prompt) => (
                  <button
                    key={prompt}
                    onClick={() => setMessage(prompt)}
                    className="bg-zinc-800 border border-zinc-700 text-zinc-300 px-4 py-2 rounded-full text-sm hover:bg-zinc-700 transition"
                  >
                    {prompt}
                  </button>
                ))}
              </div>

              <div className="flex gap-4"></div>

              <div className="flex gap-4">
                <input
                  type="text"
                  placeholder="Ask about orders, stock or shipments..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      handleChat();
                    }
                  }}
                  className="flex-1 bg-zinc-800 border border-zinc-700 rounded-xl px-4 py-3 outline-none"
                />

                <button
                  onClick={handleChat}
                  disabled={isAsking}
                  className="bg-white text-black px-6 py-3 rounded-xl font-semibold hover:bg-zinc-300 transition disabled:opacity-60"
                >
                  {isAsking ? "Thinking..." : "Ask AI"}
                </button>
              </div>

              <div className="mt-6 space-y-4 max-h-96 overflow-y-auto pr-2">
                {chatHistory.map((chat, index) => (
                  <div
                    key={index}
                    className={`p-4 rounded-xl border ${
                      chat.role === "user"
                        ? "bg-zinc-800 border-zinc-700"
                        : "bg-white text-black border-white"
                    }`}
                  >
                    <p className="text-sm font-semibold mb-1">
                      {chat.role === "user" ? "You" : "Koopilot AI"}
                    </p>

                    <p>{chat.content}</p>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;