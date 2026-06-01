"use client";

import { useState, useRef, useEffect } from "react";
import { FileTextIcon } from "lucide-react";
import MessageBubble, { type Message } from "@/components/MessageBubble";
import ChatInput from "@/components/ChatInput";

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

  // 1. Define the Ref for the WebSocket connection
  const socketRef = useRef<WebSocket | null>(null);

  // Auto-scroll to the latest message whenever messages change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // 2. Define the Effect to manage the WebSocket connection lifecycle
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/chat");
    socketRef.current = ws;

    ws.onopen = () => {
      console.log("Connected to Chat WebSocket");
    };

    ws.onmessage = (event) => {
      const chunk = event.data;

      // Turn off loading animation once chunks start coming in
      setIsLoading(false);

      // The Secret for Streaming: Functional updates + updating the last item
      setMessages((prev) => {
        const lastMessage = prev[prev.length - 1];

        // If the last message is already from the assistant, append text to it
        if (lastMessage && lastMessage.role === "assistant" && lastMessage.id !== "1") {
          return [
            ...prev.slice(0, -1), // Everything except the last message
            { ...lastMessage, content: lastMessage.content + chunk }, // Append chunk
          ];
        }

        // If it's a brand new response stream, create a new assistant message object
        const newAiMsg: Message = {
          id: Date.now().toString(),
          role: "assistant",
          content: chunk,
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        };
        return [...prev, newAiMsg];
      });
    };

    ws.onerror = (error) => {
      console.error("WebSocket Error:", error);
      setIsLoading(false);
    };

    ws.onclose = () => {
      console.log("WebSocket Disconnected");
      setIsLoading(false);
    };

    // Clean up connection when the component unmounts
    return () => {
      ws.close();
    };
  }, []);

  // 3. Update handleSend to stream data out via WebSocket
  const handleSend = () => {
    const text = inputValue.trim();
    if (!text || isLoading) return;

    // Append the user message immediately
    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInputValue("");
    setIsLoading(true);

    // Send the message text over the established WebSocket connection
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(text);
    } else {
      console.error("WebSocket is not connected.");
      setIsLoading(false);
    }
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