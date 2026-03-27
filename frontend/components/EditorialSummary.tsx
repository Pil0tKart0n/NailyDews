import { Digest } from "@/lib/types";
import { formatDate } from "@/lib/utils";

export function EditorialSummary({ digest }: { digest: Digest }) {
  return (
    <div className="border-b-2 border-ink/10 pb-8 mb-8">
      {/* Date line */}
      <div className="flex items-center justify-between text-sm text-ink-muted mb-4">
        <time>{formatDate(digest.date)}</time>
        <span>
          {digest.total_articles} articles from {digest.total_sources} sources
        </span>
      </div>

      {/* Editorial headline */}
      {digest.editorial_headline && (
        <h2 className="font-serif text-3xl md:text-4xl font-black leading-tight mb-4">
          {digest.editorial_headline}
        </h2>
      )}

      {/* Editorial summary */}
      {digest.editorial_summary && (
        <div className="bg-paper-100 border-l-4 border-ink/20 p-4 md:p-6">
          <p className="font-serif text-base md:text-lg text-ink-light leading-relaxed italic">
            {digest.editorial_summary}
          </p>
        </div>
      )}
    </div>
  );
}
