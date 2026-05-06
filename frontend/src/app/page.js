"use client";
import { useState, useRef, useEffect } from "react";
import Sidebar from "@/components/Sidebar";
import ChatMessage from "@/components/ChatMessage";
import FlightCard from "@/components/FlightCard";
import HotelCard from "@/components/HotelCard";
import ItineraryTimeline from "@/components/ItineraryTimeline";
import BudgetBreakdown from "@/components/BudgetBreakdown";
import { sendChatMessage } from "@/lib/api";

export default function Home() {
  const [activeTab, setActiveTab] = useState("chat");
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hello! I'm your AI travel assistant 🧭\n\nI can help you plan your perfect trip — from finding flights and hotels to creating detailed itineraries and managing your budget.\n\nWhere would you like to go? Just tell me your dream destination!" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [tripContext, setTripContext] = useState(null);
  const [flightsData, setFlightsData] = useState(null);
  const [hotelsData, setHotelsData] = useState(null);
  const [itineraryData, setItineraryData] = useState(null);
  const [budgetData, setBudgetData] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    const msg = input.trim();
    if (!msg || loading) return;
    setInput("");
    const userMsg = { role: "user", content: msg };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const history = [...messages, userMsg].map((m) => ({
        role: m.role === "typing" ? "assistant" : m.role,
        content: m.content,
        message_type: "text",
      }));
      const res = await sendChatMessage(msg, history, tripContext);
      setMessages((prev) => [...prev, { role: "assistant", content: res.reply }]);
      if (res.trip_context) setTripContext(res.trip_context);

      // Store data and auto-switch to the relevant tab
      if (res.message_type === "flights" && res.data) {
        setFlightsData(res.data);
        setActiveTab("flights");
      } else if (res.message_type === "hotels" && res.data) {
        setHotelsData(res.data);
        setActiveTab("hotels");
      } else if (res.message_type === "itinerary" && res.data) {
        setItineraryData(res.data);
        setActiveTab("itinerary");
      } else if (res.message_type === "budget" && res.data) {
        setBudgetData(res.data);
        setActiveTab("budget");
      }
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: "Something went wrong while processing your request. Please try again." }]);
    }
    setLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleQuickAction = (text) => {
    setInput(text);
    inputRef.current?.focus();
  };

  const quickActions = [
    "🗺️ Plan a trip to Goa",
    "✈️ Search flights to Delhi",
    "🏨 Find hotels in Manali",
    "💰 Budget for 5 days in Jaipur",
    "📋 Create itinerary for Kerala",
  ];

  const renderWelcome = () => (
    <div className="welcome-container">
      <div className="welcome-icon">🧭</div>
      <h1 className="welcome-title">Welcome to <span>OXL Travel</span></h1>
      <p className="welcome-subtitle">
        Your AI-powered travel concierge. Plan trips, find flights, discover hotels, and manage budgets — all through conversation.
      </p>
      <div className="welcome-features">
        <div className="welcome-feature" onClick={() => setActiveTab("chat")}>
          <div className="icon">💬</div>
          <div className="label">Smart Chat</div>
        </div>
        <div className="welcome-feature" onClick={() => setActiveTab("chat")}>
          <div className="icon">✈️</div>
          <div className="label">Flight Search</div>
        </div>
        <div className="welcome-feature" onClick={() => setActiveTab("chat")}>
          <div className="icon">🏨</div>
          <div className="label">Hotel Finder</div>
        </div>
        <div className="welcome-feature" onClick={() => setActiveTab("chat")}>
          <div className="icon">📋</div>
          <div className="label">Itineraries</div>
        </div>
        <div className="welcome-feature" onClick={() => setActiveTab("chat")}>
          <div className="icon">💰</div>
          <div className="label">Budget Planner</div>
        </div>
      </div>
      <button className="start-btn" onClick={() => setActiveTab("chat")} id="start-planning">
        Start Planning ✨
      </button>
    </div>
  );

  const renderChat = () => (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((msg, i) => (
          <ChatMessage key={i} message={msg} />
        ))}
        {loading && <ChatMessage message={{ role: "typing" }} />}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input-area">
        <div className="quick-actions">
          {messages.length <= 1 && quickActions.map((q, i) => (
            <button key={i} className="quick-action-btn" onClick={() => handleQuickAction(q.slice(2).trim())}>
              {q}
            </button>
          ))}
        </div>
        <div className="chat-input-wrapper">
          <textarea
            ref={inputRef}
            className="chat-input"
            placeholder="Ask me anything about your trip..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            id="chat-input"
          />
          <button className="chat-send-btn" onClick={handleSend} disabled={!input.trim() || loading} id="send-btn">
            ➤
          </button>
        </div>
      </div>
    </div>
  );

  const renderFlights = () => (
    <div style={{ padding: "24px", overflowY: "auto", flex: 1 }}>
      <h2 style={{ marginBottom: "8px" }}>✈️ Flight Results</h2>
      {flightsData && flightsData.flights ? (
        <>
          <p style={{ color: "var(--text-secondary)", marginBottom: "16px", fontSize: "0.9rem" }}>{flightsData.search_summary}</p>
          <div className="results-grid">
            {flightsData.flights.map((f, i) => <FlightCard key={i} flight={f} />)}
          </div>
        </>
      ) : (
        <div className="welcome-container">
          <div style={{ fontSize: "3rem", marginBottom: "16px" }}>✈️</div>
          <p style={{ color: "var(--text-secondary)" }}>No flight results yet. Ask me to search flights in the chat!</p>
          <button className="start-btn" style={{ marginTop: "16px" }} onClick={() => { setActiveTab("chat"); handleQuickAction("Search flights to Goa from Delhi"); }}>
            Search Flights
          </button>
        </div>
      )}
    </div>
  );

  const renderHotels = () => (
    <div style={{ padding: "24px", overflowY: "auto", flex: 1 }}>
      <h2 style={{ marginBottom: "8px" }}>🏨 Hotel Results</h2>
      {hotelsData && hotelsData.hotels ? (
        <>
          <p style={{ color: "var(--text-secondary)", marginBottom: "16px", fontSize: "0.9rem" }}>{hotelsData.search_summary}</p>
          <div className="results-grid">
            {hotelsData.hotels.map((h, i) => <HotelCard key={i} hotel={h} />)}
          </div>
        </>
      ) : (
        <div className="welcome-container">
          <div style={{ fontSize: "3rem", marginBottom: "16px" }}>🏨</div>
          <p style={{ color: "var(--text-secondary)" }}>No hotel results yet. Ask me to find hotels in the chat!</p>
          <button className="start-btn" style={{ marginTop: "16px" }} onClick={() => { setActiveTab("chat"); handleQuickAction("Find hotels in Goa"); }}>
            Find Hotels
          </button>
        </div>
      )}
    </div>
  );

  const renderItinerary = () => (
    itineraryData && itineraryData.days ? (
      <ItineraryTimeline itinerary={itineraryData} />
    ) : (
      <div className="welcome-container">
        <div style={{ fontSize: "3rem", marginBottom: "16px" }}>🗺️</div>
        <h3 style={{ marginBottom: "8px" }}>No Itinerary Yet</h3>
        <p style={{ color: "var(--text-secondary)" }}>Ask me to create an itinerary in the chat!</p>
        <button className="start-btn" style={{ marginTop: "16px" }} onClick={() => { setActiveTab("chat"); handleQuickAction("Create a 5-day itinerary for Goa under ₹50000"); }}>
          Generate Itinerary
        </button>
      </div>
    )
  );

  const renderBudget = () => (
    budgetData && budgetData.categories ? (
      <BudgetBreakdown budget={budgetData} />
    ) : (
      <div className="welcome-container">
        <div style={{ fontSize: "3rem", marginBottom: "16px" }}>💰</div>
        <h3 style={{ marginBottom: "8px" }}>No Budget Analysis Yet</h3>
        <p style={{ color: "var(--text-secondary)" }}>Ask me about budget estimation in the chat!</p>
        <button className="start-btn" style={{ marginTop: "16px" }} onClick={() => { setActiveTab("chat"); handleQuickAction("Estimate budget for 5 days in Jaipur for 2 people"); }}>
          Estimate Budget
        </button>
      </div>
    )
  );

  const tabContent = {
    welcome: renderWelcome,
    chat: renderChat,
    flights: renderFlights,
    hotels: renderHotels,
    itinerary: renderItinerary,
    budget: renderBudget,
  };

  const tabTitles = {
    welcome: "Welcome",
    chat: "Chat with AI Assistant",
    flights: "Flight Search",
    hotels: "Hotel Finder",
    itinerary: "Trip Itinerary",
    budget: "Budget Planner",
  };

  return (
    <div className="app-layout">
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
      <main className="main-content">
        <header className="header">
          <div className="header-title">{tabTitles[activeTab]}</div>
          <div className="header-actions">
            {tripContext?.destination && (
              <span style={{ fontSize: "0.82rem", color: "var(--accent-primary)", background: "rgba(99,102,241,0.1)", padding: "6px 14px", borderRadius: "var(--radius-full)" }}>
                📍 {tripContext.destination}
              </span>
            )}
          </div>
        </header>
        {(tabContent[activeTab] || renderChat)()}
      </main>
    </div>
  );
}
