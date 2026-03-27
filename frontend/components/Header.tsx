import Link from "next/link";
import { Newspaper } from "lucide-react";

export function Header() {
  return (
    <header className="border-b-4 border-double border-ink">
      <div className="max-w-6xl mx-auto px-4">
        {/* Top bar */}
        <div className="flex items-center justify-between py-2 text-xs text-ink-muted border-b border-ink/10">
          <span>Your Daily AI Intelligence Brief</span>
          <nav className="flex gap-4">
            <Link href="/archive" className="hover:text-ink transition-colors">
              Archive
            </Link>
            <Link href="/about" className="hover:text-ink transition-colors">
              About
            </Link>
          </nav>
        </div>

        {/* Masthead */}
        <div className="text-center py-6">
          <Link href="/" className="inline-block">
            <h1 className="font-serif text-5xl md:text-6xl font-black tracking-tight">
              NailyDews
            </h1>
            <p className="font-serif text-sm text-ink-muted mt-1 italic">
              AI News That Matters -- Delivered Daily
            </p>
          </Link>
        </div>

        {/* Category nav */}
        <nav className="flex items-center justify-center gap-6 py-3 text-sm font-medium border-t border-ink/10 overflow-x-auto">
          <a href="#top_stories" className="whitespace-nowrap hover:text-accent-blue transition-colors">
            Top Stories
          </a>
          <span className="text-ink/20">|</span>
          <a href="#models_releases" className="whitespace-nowrap hover:text-accent-blue transition-colors">
            Models & Releases
          </a>
          <span className="text-ink/20">|</span>
          <a href="#tools_frameworks" className="whitespace-nowrap hover:text-accent-blue transition-colors">
            Tools & Frameworks
          </a>
          <span className="text-ink/20">|</span>
          <a href="#research_papers" className="whitespace-nowrap hover:text-accent-blue transition-colors">
            Research
          </a>
          <span className="text-ink/20">|</span>
          <a href="#business_regulation" className="whitespace-nowrap hover:text-accent-blue transition-colors">
            Business
          </a>
        </nav>
      </div>
    </header>
  );
}
