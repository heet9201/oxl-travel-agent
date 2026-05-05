"use client";

export default function Sidebar({ activeTab, onTabChange }) {
  const navItems = [
    { id: "chat", icon: "💬", label: "Chat" },
    { id: "itinerary", icon: "🗺️", label: "Itinerary" },
    { id: "flights", icon: "✈️", label: "Flights" },
    { id: "hotels", icon: "🏨", label: "Hotels" },
    { id: "budget", icon: "💰", label: "Budget" },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">🧭</div>
        <h1>OXL Travel</h1>
      </div>
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <button
            key={item.id}
            className={`sidebar-nav-item ${activeTab === item.id ? "active" : ""}`}
            onClick={() => onTabChange(item.id)}
            id={`nav-${item.id}`}
          >
            <span className="icon">{item.icon}</span>
            {item.label}
          </button>
        ))}
      </nav>
      <div className="sidebar-footer">
        <div style={{ fontSize: "0.78rem", color: "var(--text-muted)", textAlign: "center" }}>
          Powered by Gemini AI ✨
        </div>
      </div>
    </aside>
  );
}
