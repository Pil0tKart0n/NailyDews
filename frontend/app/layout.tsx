import type { Metadata } from "next";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "NailyDews - AI News, Curated Daily",
    template: "%s | NailyDews",
  },
  description:
    "Your daily AI digest. 50+ sources distilled into one clean newspaper every evening at 19:00 CET. No noise. No ads. Just what matters in AI.",
  keywords: [
    "AI news", "artificial intelligence", "daily digest", "LLM news",
    "machine learning", "AI newsletter", "OpenAI", "Anthropic", "Claude",
    "GPT", "AI research", "AI tools",
  ],
  openGraph: {
    title: "NailyDews - AI News, Curated Daily",
    description:
      "50+ sources. One digest. Every evening. The AI newspaper for people who build.",
    type: "website",
    siteName: "NailyDews",
  },
  twitter: {
    card: "summary_large_image",
    title: "NailyDews - AI News, Curated Daily",
    description: "50+ sources. One digest. Every evening at 19:00 CET.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-1 max-w-6xl mx-auto px-4 py-8 w-full">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
