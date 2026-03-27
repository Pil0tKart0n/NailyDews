import type { Metadata } from "next";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import "./globals.css";

export const metadata: Metadata = {
  title: "NailyDews - AI News That Matters",
  description:
    "Your daily AI intelligence brief. Curated, summarized, and ranked AI news from 20+ sources, delivered every evening.",
  openGraph: {
    title: "NailyDews - AI News That Matters",
    description: "Your daily AI intelligence brief.",
    type: "website",
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
