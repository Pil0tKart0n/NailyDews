import { Article } from "@/lib/types";
import { timeAgo } from "@/lib/utils";
import { ConfidenceBadge } from "./ConfidenceBadge";
import { ExternalLink } from "lucide-react";

const CATEGORY_COLORS: Record<string, string> = {
  top_stories: "border-l-red-500",
  models_releases: "border-l-violet-500",
  tools_frameworks: "border-l-emerald-500",
  research_papers: "border-l-amber-500",
  business_regulation: "border-l-sky-500",
};

const CATEGORY_DOTS: Record<string, string> = {
  top_stories: "bg-red-500",
  models_releases: "bg-violet-500",
  tools_frameworks: "bg-emerald-500",
  research_papers: "bg-amber-500",
  business_regulation: "bg-sky-500",
};

interface NewsCardProps {
  article: Article;
  size?: "hero" | "medium" | "small";
}

export function NewsCard({ article, size = "medium" }: NewsCardProps) {
  const borderColor = CATEGORY_COLORS[article.category] || "border-l-gray-300";
  const dotColor = CATEGORY_DOTS[article.category] || "bg-gray-400";

  if (size === "hero") {
    return (
      <a
        href={article.source_url}
        target="_blank"
        rel="noopener noreferrer"
        className={`block bg-white rounded-xl border border-ink/5 border-l-4 ${borderColor} p-6 hover:shadow-lg hover:-translate-y-0.5 transition-all group`}
      >
        <div className="flex items-center gap-2 mb-3">
          <span className={`w-2 h-2 rounded-full ${dotColor}`} />
          <ConfidenceBadge confidence={article.confidence} />
          <span className="text-xs text-ink-muted">{article.source_name}</span>
          {article.published_at && (
            <>
              <span className="text-ink/15 text-xs">&middot;</span>
              <span className="text-xs text-ink-muted">{timeAgo(article.published_at)}</span>
            </>
          )}
          <ExternalLink className="w-3.5 h-3.5 text-ink-muted ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />
        </div>

        <h3 className="font-serif text-xl md:text-2xl font-bold leading-tight mb-3 group-hover:text-accent-blue transition-colors">
          {article.headline}
        </h3>

        {article.summary && (
          <p className="text-sm text-ink-light leading-relaxed line-clamp-3">
            {article.summary}
          </p>
        )}
      </a>
    );
  }

  if (size === "small") {
    return (
      <a
        href={article.source_url}
        target="_blank"
        rel="noopener noreferrer"
        className={`block bg-white rounded-lg border border-ink/5 border-l-4 ${borderColor} p-3.5 hover:shadow-md hover:-translate-y-0.5 transition-all group`}
      >
        <div className="flex items-center gap-1.5 mb-1.5">
          <span className={`w-1.5 h-1.5 rounded-full ${dotColor}`} />
          <span className="text-[10px] text-ink-muted font-medium">{article.source_name}</span>
          {article.published_at && (
            <span className="text-[10px] text-ink-muted/60">{timeAgo(article.published_at)}</span>
          )}
        </div>
        <h3 className="font-semibold text-sm leading-snug group-hover:text-accent-blue transition-colors line-clamp-2">
          {article.headline}
        </h3>
      </a>
    );
  }

  // Medium (default)
  return (
    <a
      href={article.source_url}
      target="_blank"
      rel="noopener noreferrer"
      className={`block bg-white rounded-xl border border-ink/5 border-l-4 ${borderColor} p-4 hover:shadow-md hover:-translate-y-0.5 transition-all group`}
    >
      <div className="flex items-center gap-2 mb-2">
        <span className={`w-1.5 h-1.5 rounded-full ${dotColor}`} />
        <ConfidenceBadge confidence={article.confidence} />
        <span className="text-xs text-ink-muted">{article.source_name}</span>
        {article.published_at && (
          <span className="text-xs text-ink-muted/60">{timeAgo(article.published_at)}</span>
        )}
        <ExternalLink className="w-3 h-3 text-ink-muted ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />
      </div>

      <h3 className="font-semibold text-base leading-snug mb-2 group-hover:text-accent-blue transition-colors line-clamp-2">
        {article.headline}
      </h3>

      {article.summary && (
        <p className="text-xs text-ink-muted leading-relaxed line-clamp-2">
          {article.summary}
        </p>
      )}
    </a>
  );
}
