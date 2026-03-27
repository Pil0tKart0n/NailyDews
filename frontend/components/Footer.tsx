import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t-2 border-ink/10 mt-16">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-sm text-ink-muted">
          <div>
            <h3 className="font-serif font-bold text-ink mb-2">NailyDews</h3>
            <p className="leading-relaxed">
              AI news aggregator that collects, filters, and summarizes the most
              important AI developments every day.
            </p>
          </div>

          <div>
            <h4 className="font-bold text-ink mb-2">Navigation</h4>
            <ul className="space-y-1">
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
                  About
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-bold text-ink mb-2">Legal</h4>
            <ul className="space-y-1">
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

        <div className="border-t border-ink/10 mt-6 pt-4 text-xs text-ink-muted text-center">
          NailyDews &copy; {new Date().getFullYear()} -- All news sourced from
          original publishers. Every article links to its original source.
        </div>
      </div>
    </footer>
  );
}
