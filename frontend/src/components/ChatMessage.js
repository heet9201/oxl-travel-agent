"use client";
import ReactMarkdown from 'react-markdown';

export default function ChatMessage({ message }) {
  const { role, content } = message;

  if (role === "typing") {
    return (
      <div className="message assistant">
        <div className="message-avatar">🧭</div>
        <div className="message-content">
          <div className="typing-indicator">
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`message ${role}`}>
      <div className="message-avatar">
        {role === "assistant" ? "🧭" : "👤"}
      </div>
      <div className="message-content">
        {role === "assistant" ? (
          <ReactMarkdown>{content}</ReactMarkdown>
        ) : (
          content
        )}
      </div>
    </div>
  );
}
