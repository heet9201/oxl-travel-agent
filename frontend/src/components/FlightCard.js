"use client";

export default function FlightCard({ flight }) {
  const stops = flight.stops === 0 ? "Non-stop" : `${flight.stops} stop${flight.stops > 1 ? "s" : ""}`;

  return (
    <div className="flight-card">
      <div className="flight-card-header">
        <div>
          <div className="flight-airline">{flight.airline}</div>
          <div style={{ fontSize: "0.78rem", color: "var(--text-muted)" }}>{flight.flight_number}</div>
        </div>
        <div className="flight-price">
          ₹{Number(flight.price).toLocaleString("en-IN")}
          <span> /person</span>
        </div>
      </div>
      <div className="flight-route">
        <div className="flight-point">
          <div className="time">{flight.departure_time}</div>
          <div className="code">{flight.origin_airport || flight.origin}</div>
        </div>
        <div className="flight-line">
          <div className="duration">{flight.duration}</div>
          <div className="flight-line-bar"></div>
          <div className="stops">{stops}</div>
        </div>
        <div className="flight-point">
          <div className="time">{flight.arrival_time}</div>
          <div className="code">{flight.destination_airport || flight.destination}</div>
        </div>
      </div>
      <div className="flight-meta">
        <span className="flight-tag">{flight.travel_class || "Economy"}</span>
        {flight.baggage && <span className="flight-tag">🧳 {flight.baggage}</span>}
      </div>
    </div>
  );
}
