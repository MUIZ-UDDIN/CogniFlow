"use client";

/**
 * ChatInput — Client Component.
 *
 * Handles controlled textarea input and fires onSend when the user
 * submits (button click or Cmd/Ctrl + Enter).
 */

import { SendIcon } from "lucide-react";
import { useRef, KeyboardEvent } from "react";

interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  isLoading: boolean;
}

export default function ChatInput({
  value = "",
  onChange,
  onSend,
  isLoading,
}: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Cmd/Ctrl + Enter → send
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <div className="border-t border-slate-800 bg-slate-950 px-6 py-4">
      <div className="mx-auto flex max-w-3xl items-end gap-3">

        {/* Textarea */}
        <div className="flex-1 rounded-xl border border-slate-700 bg-slate-900 focus-within:border-indigo-500 transition-colors duration-150">
          <textarea
            ref={textareaRef}
            rows={2}
            placeholder="Ask anything about your documents…"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
            className="
              w-full resize-none bg-transparent px-4 py-3
              text-sm text-slate-200 placeholder:text-slate-600
              focus:outline-none disabled:opacity-50
            "
          />
          <div className="flex items-center justify-between px-3 pb-2">
            <span className="text-[11px] text-slate-600">
              ⌘ + Enter to send
            </span>
          </div>
        </div>

        {/* Ask button */}
        <button
          type="button"
          onClick={onSend}
          disabled={isLoading || !value.trim()}
          className="
            flex h-12 w-12 shrink-0 items-center justify-center
            rounded-xl bg-indigo-600 text-white
            transition-all duration-150
            hover:bg-indigo-500
            active:scale-95
            disabled:opacity-40 disabled:cursor-not-allowed
          "
          aria-label="Send message"
        >
          {isLoading
            ? <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
            : <SendIcon className="h-4 w-4" strokeWidth={2.5} />
          }
        </button>

      </div>
    </div>
  );
}
