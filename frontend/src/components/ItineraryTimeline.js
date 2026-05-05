"use client";

export default function ItineraryTimeline({ itinerary }) {
  if (!itinerary || !itinerary.days) return null;

  const getTypeClass = (type) => {
    const map = { sightseeing: "type-sightseeing", food: "type-food", transport: "type-transport" };
    return map[type] || "type-activity";
  };

  return (
    <div className="itinerary-container">
      <div className="itinerary-header">
        <h1>🗺️ {itinerary.destination}</h1>
        <p>{itinerary.start_date} → {itinerary.end_date} · {itinerary.total_days} days</p>
        <div style={{ marginTop: "16px", fontFamily: "var(--font-heading)", fontSize: "1.5rem", fontWeight: 700, color: "var(--success)" }}>
          Total: ₹{Number(itinerary.total_estimated_cost || 0).toLocaleString("en-IN")}
        </div>
      </div>

      {itinerary.days.map((day) => (
        <div key={day.day} className="day-card">
          <div className="day-card-header">
            <div className="day-number">{day.day}</div>
            <div className="day-info">
              <h3>{day.title}</h3>
              <p>{day.date}</p>
            </div>
            <div className="day-cost">₹{Number(day.estimated_cost || 0).toLocaleString("en-IN")}</div>
          </div>

          {day.activities && day.activities.map((act, i) => (
            <div key={i} className="activity-item">
              <div className="activity-time">{act.time}</div>
              <div className="activity-details">
                <div className="activity-name">
                  {act.name}
                  {act.type && <span className={`activity-type-tag ${getTypeClass(act.type)}`}>{act.type}</span>}
                </div>
                {act.description && <div className="activity-desc">{act.description}</div>}
                {act.cost > 0 && <div className="activity-cost">₹{Number(act.cost).toLocaleString("en-IN")} · {act.duration || ""}</div>}
              </div>
            </div>
          ))}

          {day.meals && day.meals.length > 0 && (
            <div style={{ marginTop: "12px", paddingTop: "12px", borderTop: "1px solid var(--border-glass)" }}>
              <div style={{ fontSize: "0.82rem", color: "var(--text-muted)", marginBottom: "8px" }}>🍽️ Meals</div>
              {day.meals.map((meal, i) => (
                <div key={i} className="activity-item">
                  <div className="activity-time">{meal.time}</div>
                  <div className="activity-details">
                    <div className="activity-name">{meal.type} — {meal.suggestion}</div>
                    {meal.cost > 0 && <div className="activity-cost">₹{Number(meal.cost).toLocaleString("en-IN")}</div>}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      ))}

      {itinerary.tips && itinerary.tips.length > 0 && (
        <div className="budget-tips">
          <h3>💡 Pro Tips</h3>
          {itinerary.tips.map((tip, i) => (
            <div key={i} className="budget-tip-item">
              <span>✦</span> {tip}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
