import { Digest } from "@/lib/types";
import { formatDate } from "@/lib/utils";
import { Sparkles } from "lucide-react";

export function EditorialSummary({ digest }: { digest: Digest }) {
  return (
    <div className="border-b-2 border-ink/10 pb-8 mb-8">
      {/* Date + stats line */}
      <div className="flex items-center justify-between text-sm text-ink-muted mb-5">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-accent-blue" />
          <time className="font-medium">{formatDate(digest.date)}</time>
        </div>
        <span className="text-xs">
          {digest.total_articles} articles | {digest.total_sources} sources
        </span>
      </div>

      {/* Editorial headline */}
      {digest.editorial_headline && (
        <h2 className="font-serif text-3xl md:text-4xl font-black leading-tight mb-5">
          {digest.editorial_headline}
        </h2>
      )}

      {/* Editorial summary */}
      {digest.editorial_summary && (
        <div className="bg-paper-100 border-l-4 border-accent-blue/30 p-4 md:p-6 rounded-r">
          <p className="text-xs text-accent-blue font-semibold uppercase tracking-wider mb-2">
            Editor&apos;s Brief
          </p>
          <p className="font-serif text-base md:text-lg text-ink-light leading-relaxed">
            {digest.editorial_summary}
          </p>
        </div>
      )}
    </div>
  );
}
