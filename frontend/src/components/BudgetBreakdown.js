"use client";

const CATEGORY_COLORS = {
  flights: "#6366f1",
  accommodation: "#8b5cf6",
  food: "#f59e0b",
  transport: "#10b981",
  activities: "#3b82f6",
  shopping: "#ec4899",
  miscellaneous: "#64748b",
};

const CATEGORY_ICONS = {
  flights: "✈️",
  accommodation: "🏨",
  food: "🍽️",
  transport: "🚕",
  activities: "🎯",
  shopping: "🛍️",
  miscellaneous: "📦",
};

export default function BudgetBreakdown({ budget }) {
  if (!budget || !budget.categories) return null;

  const totalEstimated = budget.total_estimated || Object.values(budget.categories).reduce((a, b) => a + b, 0);
  const withinBudget = budget.total_budget ? totalEstimated <= budget.total_budget : true;
  const maxCategory = Math.max(...Object.values(budget.categories));

  return (
    <div className="budget-container">
      <div className="budget-header">
        <div style={{ fontSize: "0.9rem", color: "var(--text-muted)", marginBottom: "8px" }}>Estimated Total</div>
        <div className={`budget-total ${withinBudget ? "within" : "over"}`}>
          ₹{Number(totalEstimated).toLocaleString("en-IN")}
        </div>
        {budget.total_budget > 0 && (
          <div style={{ fontSize: "0.9rem", color: "var(--text-secondary)", marginTop: "8px" }}>
            Budget: ₹{Number(budget.total_budget).toLocaleString("en-IN")}
            <span style={{ marginLeft: "8px", color: withinBudget ? "var(--success)" : "var(--danger)" }}>
              {withinBudget ? "✓ Within budget" : "⚠ Over budget"}
            </span>
          </div>
        )}
      </div>

      <div className="budget-categories">
        {Object.entries(budget.categories).map(([cat, amount]) => (
          <div key={cat} className="budget-cat-card">
            <div className="budget-cat-label">
              {CATEGORY_ICONS[cat] || "📊"} {cat}
            </div>
            <div className="budget-cat-amount" style={{ color: CATEGORY_COLORS[cat] || "var(--text-primary)" }}>
              ₹{Number(amount).toLocaleString("en-IN")}
            </div>
            <div className="budget-bar">
              <div
                className="budget-bar-fill"
                style={{
                  width: `${maxCategory > 0 ? (amount / maxCategory) * 100 : 0}%`,
                  background: CATEGORY_COLORS[cat] || "var(--accent-gradient)",
                }}
              />
            </div>
          </div>
        ))}
      </div>

      {budget.savings_tips && budget.savings_tips.length > 0 && (
        <div className="budget-tips">
          <h3>💡 Money-Saving Tips</h3>
          {budget.savings_tips.map((tip, i) => (
            <div key={i} className="budget-tip-item">
              <span style={{ color: "var(--success)" }}>✦</span> {tip}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
