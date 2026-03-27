import Link from "next/link";
import { Newspaper, Clock, BookOpen } from "lucide-react";

export function Header() {
  const today = new Date().toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <header className="border-b-4 border-double border-ink">
      <div className="max-w-6xl mx-auto px-4">
        {/* Top bar with date and nav */}
        <div className="flex items-center justify-between py-2 text-xs text-ink-muted border-b border-ink/10">
          <div className="flex items-center gap-2">
            <Clock className="w-3 h-3" />
            <time>{today}</time>
          </div>
          <nav className="flex gap-4">
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
        <div className="text-center py-5 md:py-6">
          <Link href="/" className="inline-block">
            <h1 className="font-serif text-4xl md:text-6xl font-black tracking-tight">
              NailyDews
            </h1>
          </Link>
          <p className="text-xs md:text-sm text-ink-muted mt-1 tracking-widest uppercase">
            50+ Sources. One Digest. Every Evening at 19:00 CET.
          </p>
        </div>

        {/* Category nav */}
        <nav className="flex items-center justify-center gap-4 md:gap-6 py-3 text-xs md:text-sm font-medium border-t border-ink/10 overflow-x-auto">
          <a href="#top_stories" className="flex items-center gap-1.5 whitespace-nowrap hover:text-accent-blue transition-colors">
            <span className="hidden md:inline text-accent-red">&#9679;</span>
            Top Stories
          </a>
          <span className="text-ink/15">|</span>
          <a href="#models_releases" className="whitespace-nowrap hover:text-accent-blue transition-colors">
            Models & Releases
          </a>
          <span className="text-ink/15">|</span>
          <a href="#tools_frameworks" className="whitespace-nowrap hover:text-accent-blue transition-colors">
            Tools & Frameworks
          </a>
          <span className="text-ink/15">|</span>
          <a href="#research_papers" className="whitespace-nowrap hover:text-accent-blue transition-colors">
            Research
          </a>
          <span className="text-ink/15">|</span>
          <a href="#business_regulation" className="whitespace-nowrap hover:text-accent-blue transition-colors">
            Business & Policy
          </a>
        </nav>
      </div>
    </header>
  );
}
