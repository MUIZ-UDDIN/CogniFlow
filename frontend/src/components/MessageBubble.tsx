/**
 * MessageBubble — purely presentational, renders one chat turn.
 */

import { BotIcon, UserIcon } from "lucide-react";

export type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
};

interface MessageBubbleProps {
  message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex gap-3 ${isUser ? "flex-row-reverse" : "flex-row"}`}>

      {/* Avatar */}
      <div
        className={`
          flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-white
          ${isUser ? "bg-indigo-600" : "bg-slate-700"}
        `}
      >
        {isUser
          ? <UserIcon className="h-4 w-4" />
          : <BotIcon className="h-4 w-4" />
        }
      </div>

      {/* Bubble */}
      <div className={`flex max-w-[75%] flex-col gap-1 ${isUser ? "items-end" : "items-start"}`}>
        <div
          className={`
            rounded-2xl px-4 py-2.5 text-sm leading-relaxed
            ${isUser
              ? "bg-indigo-600 text-white rounded-tr-sm"
              : "bg-slate-800 text-slate-200 rounded-tl-sm"
            }
          `}
        >
          {message.content}
        </div>
        <span className="text-[11px] text-slate-600">{message.timestamp}</span>
      </div>

    </div>
  );
}
