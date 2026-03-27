import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t-2 border-ink mt-16 bg-paper-100">
      <div className="max-w-6xl mx-auto px-4 py-10">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-sm text-ink-muted">
          {/* Brand */}
          <div className="md:col-span-2">
            <h3 className="font-serif text-xl font-black text-ink mb-2">NailyDews</h3>
            <p className="leading-relaxed mb-3">
              AI news from 50+ sources, distilled into one daily digest.
              Every article links to its original source. No tracking.
              No ads. Just signal.
            </p>
            <p className="text-xs">
              Published daily at 19:00 CET.
            </p>
          </div>

          {/* Navigation */}
          <div>
            <h4 className="font-bold text-ink mb-3 text-xs uppercase tracking-wider">Navigate</h4>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="hover:text-ink transition-colors">
                  Today&apos;s Digest
                </Link>
              </li>
              <li>
                <Link href="/archive" className="hover:text-ink transition-colors">
                  Archive
                </Link>
              </li>
              <li>
                <Link href="/about" className="hover:text-ink transition-colors">
                  How It Works
                </Link>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="font-bold text-ink mb-3 text-xs uppercase tracking-wider">Legal</h4>
            <ul className="space-y-2">
              <li>
                <Link href="/privacy" className="hover:text-ink transition-colors">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/impressum" className="hover:text-ink transition-colors">
                  Impressum
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-ink/10 mt-8 pt-4 text-xs text-ink-muted flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>
            &copy; {new Date().getFullYear()} NailyDews. All news sourced
            and linked to original publishers.
          </span>
          <span>
            Built with AI. Powered by transparency.
          </span>
        </div>
      </div>
    </footer>
  );
}
