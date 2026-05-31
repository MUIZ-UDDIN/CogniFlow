/**
 * Sidebar — Server Component (no interactivity needed here).
 *
 * Layout role:
 *   • Fixed width  : w-80  (320 px)
 *   • Full height  : h-full (inherits h-screen from parent flex)
 *   • Flex column  : stacks logo → doc list → footer
 */

import { PlusIcon, FileTextIcon, MessageSquareIcon } from "lucide-react";

const RECENT_DOCS = [
  { id: "1", title: "Product Requirements v2.pdf" },
  { id: "2", title: "Q3 Research Notes.docx" },
  { id: "3", title: "Architecture Overview.md" },
  { id: "4", title: "Meeting Transcript — June.txt" },
];

export default function Sidebar() {
  return (
    <aside className="flex h-full w-80 shrink-0 flex-col bg-slate-900 border-r border-slate-800">

      {/* ── Brand header ─────────────────────────────────── */}
      <div className="flex items-center gap-2.5 px-5 py-5 border-b border-slate-800">
        {/* Logo mark */}
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600">
          <MessageSquareIcon className="h-4 w-4 text-white" strokeWidth={2.5} />
        </div>
        <span className="text-lg font-semibold tracking-tight text-white font-mono">
          CogniFlow
        </span>
      </div>

      {/* ── New Chat button ───────────────────────────────── */}
      <div className="px-4 pt-4">
        <button
          type="button"
          className="
            flex w-full items-center justify-center gap-2
            rounded-lg border border-dashed border-indigo-500/60
            px-4 py-2.5
            text-sm font-medium text-indigo-400
            transition-colors duration-150
            hover:bg-indigo-500/10 hover:border-indigo-400 hover:text-indigo-300
            active:scale-[0.98]
          "
        >
          <PlusIcon className="h-4 w-4" strokeWidth={2.5} />
          New Chat
        </button>
      </div>

      {/* ── Recent documents list ────────────────────────── */}
      <div className="mt-6 flex flex-1 flex-col overflow-hidden px-4">
        <p className="mb-2 px-1 text-xs font-semibold uppercase tracking-widest text-slate-500">
          Recent Documents
        </p>
        <ul className="flex flex-col gap-1 overflow-y-auto">
          {RECENT_DOCS.map((doc) => (
            <li key={doc.id}>
              <button
                type="button"
                className="
                  flex w-full items-center gap-3 rounded-md px-3 py-2.5
                  text-left text-sm text-slate-300
                  transition-colors duration-100
                  hover:bg-slate-800 hover:text-slate-100
                "
              >
                <FileTextIcon className="h-4 w-4 shrink-0 text-slate-500" />
                <span className="truncate">{doc.title}</span>
              </button>
            </li>
          ))}
        </ul>
      </div>

      {/* ── Footer ───────────────────────────────────────── */}
      <div className="border-t border-slate-800 px-5 py-4">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-indigo-600 text-xs font-bold text-white">
            U
          </div>
          <div className="min-w-0">
            <p className="truncate text-sm font-medium text-slate-200">User</p>
            <p className="truncate text-xs text-slate-500">Free Plan</p>
          </div>
        </div>
      </div>

    </aside>
  );
}
