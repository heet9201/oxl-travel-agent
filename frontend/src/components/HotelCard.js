"use client";

export default function HotelCard({ hotel }) {
  return (
    <div className="hotel-card">
      <div className="hotel-card-top">
        <div>
          <div className="hotel-name">{hotel.name}</div>
          <div className="hotel-location">📍 {hotel.location || hotel.distance_to_center}</div>
        </div>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: "8px" }}>
          <div className="hotel-rating">⭐ {hotel.rating}</div>
          <div className="hotel-price">
            <div className="amount">₹{Number(hotel.price_per_night).toLocaleString("en-IN")}</div>
            <div className="per-night">/night</div>
          </div>
        </div>
      </div>
      {hotel.room_type && (
        <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: "8px" }}>
          🛏️ {hotel.room_type}
        </div>
      )}
      {hotel.amenities && hotel.amenities.length > 0 && (
        <div className="hotel-amenities">
          {hotel.amenities.slice(0, 6).map((a, i) => (
            <span key={i} className="hotel-amenity">{a}</span>
          ))}
        </div>
      )}
      {hotel.review_highlight && (
        <div className="hotel-review">"{hotel.review_highlight}"</div>
      )}
    </div>
  );
}
