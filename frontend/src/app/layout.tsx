import type { Metadata } from "next";
import { Geist_Mono } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/Sidebar";

const geistMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "CogniFlow",
  description: "AI-powered document chat",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning={true} className={geistMono.variable}>
      <body className="bg-slate-950 text-slate-100 antialiased" suppressHydrationWarning={true}>
        {/*
          Full-screen flex container — no page-level scroll.
          Sidebar is fixed-width on the left; main area fills the rest.
        */}
        <div className="flex h-screen overflow-hidden">
          <Sidebar />
          <main className="flex flex-1 flex-col overflow-hidden">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}

