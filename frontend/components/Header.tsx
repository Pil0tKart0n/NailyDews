import Link from "next/link";
import { Clock } from "lucide-react";

export function Header() {
  const today = new Date().toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <header className="bg-white border-b border-ink/10">
      <div className="max-w-6xl mx-auto px-4">
        {/* Top bar */}
        <div className="flex items-center justify-between py-2.5 text-xs text-ink-muted border-b border-ink/5">
          <div className="flex items-center gap-2">
            <Clock className="w-3 h-3" />
            <time>{today}</time>
          </div>
          <nav className="flex gap-5">
            <Link href="/" className="hover:text-ink transition-colors font-medium">
              Today
            </Link>
            <Link href="/archive" className="hover:text-ink transition-colors">
              Archive
            </Link>
            <Link href="/about" className="hover:text-ink transition-colors">
              How It Works
            </Link>
          </nav>
        </div>

        {/* Masthead */}
        <div className="text-center py-4 md:py-5">
          <Link href="/" className="inline-block">
            <h1 className="font-serif text-3xl md:text-5xl font-black tracking-tight text-navy-900">
              NailyDews
            </h1>
          </Link>
          <p className="text-[10px] md:text-xs text-ink-muted mt-1 tracking-[0.2em] uppercase">
            50+ Sources. One Digest. Every Evening at 19:00 CET.
          </p>
        </div>
      </div>
    </header>
  );
}
