import "./globals.css";

export const metadata = {
  title: "OXL Travel Agent — AI-Powered Travel Assistant",
  description: "Your intelligent multi-agent travel concierge. Plan, optimize, and book entire journeys with AI.",
  keywords: "travel, AI, itinerary, flights, hotels, budget, travel planner",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
