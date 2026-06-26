import type { Metadata } from "next";
import { Geist_Mono } from "next/font/google";
import "./globals.css";


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
        {children}
      </body>
    </html>
  );
}

