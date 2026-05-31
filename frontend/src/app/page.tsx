"use client";

import { useState, useRef, useEffect } from "react";
import { FileTextIcon, SparklesIcon } from "lucide-react";
import MessageBubble, { type Message } from "@/components/MessageBubble";
import ChatInput from "@/components/ChatInput";

// ── Seed data so the UI isn't empty on first load ──────────────────────────
const INITIAL_MESSAGES: Message[] = [
  {
    id: "1",
    role: "assistant",
    content:
      "Hello! I'm CogniFlow. Upload a document or select one from the sidebar, then ask me anything about its contents.",
    timestamp: "Just now",
  },
];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>(INITIAL_MESSAGES);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to the latest message whenever messages change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    const text = inputValue.trim();
    if (!text || isLoading) return;

    // 1. Append the user message immediately
    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInputValue("");
    setIsLoading(true);

    // 2. Simulate an AI response (replace with real WebSocket / API call later)
    await new Promise((r) => setTimeout(r, 1200));
    const aiMsg: Message = {
      id: (Date.now() + 1).toString(),
      role: "assistant",
      content: `You asked: "${text}". This is a placeholder response — wire up your API here!`,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };
    setMessages((prev) => [...prev, aiMsg]);
    setIsLoading(false);
  };

  return (
    <>
      {/* ── Top bar ─────────────────────────────────────────── */}
      <header className="flex items-center gap-3 border-b border-slate-800 bg-slate-950 px-6 py-3.5">
        <div className="flex items-center gap-2 rounded-lg bg-slate-800 px-3 py-1.5">
          <FileTextIcon className="h-4 w-4 text-indigo-400" />
          <span className="text-sm font-medium text-slate-300">
            No document selected
          </span>
        </div>
      </header>

      {/* ── Scrollable message feed ─────────────────────────── */}
      <div className="messages-scroll flex flex-1 flex-col gap-6 overflow-y-auto px-6 py-6">
        <div className="mx-auto w-full max-w-3xl flex flex-col gap-6">
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}

          {/* Typing indicator */}
          {isLoading && (
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-slate-700">
                <span className="h-4 w-4 text-white text-xs">AI</span>
              </div>
              <div className="flex gap-1 rounded-2xl rounded-tl-sm bg-slate-800 px-4 py-3">
                {[0, 150, 300].map((delay) => (
                  <span
                    key={delay}
                    className="h-1.5 w-1.5 rounded-full bg-slate-400 animate-bounce"
                    style={{ animationDelay: `${delay}ms` }}
                  />
                ))}
              </div>
            </div>
          )}

          {/* Invisible anchor — scroll target */}
          <div ref={bottomRef} />
        </div>
      </div>

      {/* ── Fixed input bar ─────────────────────────────────── */}
      <ChatInput
        value={inputValue}
        onChange={setInputValue}
        onSend={handleSend}
        isLoading={isLoading}
      />
    </>
  );
}