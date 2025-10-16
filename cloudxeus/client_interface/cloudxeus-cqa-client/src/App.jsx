import { useState } from "react";
import "./App.css";

const API_BASE = import.meta.env.VITE_API_BASE;

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);

  const send = async () => {
    const q = input.trim();
    if (!q) return;
    setMessages(m => [...m, { role: "user", text: q }]);
    setInput(""); setBusy(true);

    try {
      const res = await fetch(`${API_BASE}/api/ask?code=${import.meta.env.VITE_FUNCTION_KEY}`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ question: q })
      });
      const data = await res.json();
      const text = data.answer || "🤔 I’m not sure about that. Please contact support@cloudxeus.com.";
      setMessages(m => [...m, { role: "bot", text }]);
    } catch (e) {
      setMessages(m => [...m, { role: "bot", text: "⚠️ Network error. Try again." }]);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">CloudXeus Support Chat</div>

      <div className="chat-messages">
        {messages.map((m,i)=>(
          <div key={i} className={`message ${m.role}`}>
            <div className="message-bubble">{m.text}</div>
          </div>
        ))}
        {busy && <div className="message bot"><div className="message-bubble">Bot is typing…</div></div>}
      </div>

      <div className="chat-input">
        <input
          value={input}
          onChange={e=>setInput(e.target.value)}
          onKeyDown={e=>e.key==='Enter' && send()}
          placeholder="Ask about courses, refunds, access…"
        />
        <button onClick={send} disabled={busy || !input.trim()}>Send</button>
      </div>
    </div>
  );
}
