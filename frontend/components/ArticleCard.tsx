import { Article } from "@/lib/types";
import { timeAgo } from "@/lib/utils";
import { ConfidenceBadge } from "./ConfidenceBadge";
import { ExternalLink } from "lucide-react";

interface ArticleCardProps {
  article: Article;
  featured?: boolean;
  compact?: boolean;
}

export function ArticleCard({ article, featured = false, compact = false }: ArticleCardProps) {
  if (compact) {
    return (
      <article className="border-b border-ink/5 pb-3 mb-3 last:border-0 last:pb-0 last:mb-0">
        <div className="flex items-start gap-2">
          <div className="flex-1">
            <h3 className="font-serif font-bold text-sm leading-snug mb-1">
              <a
                href={article.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-accent-blue transition-colors"
              >
                {article.headline}
              </a>
            </h3>
            <div className="flex items-center gap-2 text-xs text-ink-muted">
              <ConfidenceBadge confidence={article.confidence} />
              <span>{article.source_name}</span>
            </div>
          </div>
          <a
            href={article.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-1 text-ink-muted hover:text-accent-blue transition-colors shrink-0"
          >
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </article>
    );
  }

  return (
    <article
      className={`group ${
        featured
          ? "border-b-2 border-ink/10 pb-6 mb-6"
          : "border-b border-ink/5 pb-4 mb-4 last:border-0 last:pb-0 last:mb-0"
      }`}
    >
      <div className="flex items-center gap-2 mb-2">
        <ConfidenceBadge confidence={article.confidence} />
        <span className="text-xs text-ink-muted">{article.source_name}</span>
        {article.published_at && (
          <>
            <span className="text-ink/15 text-xs">&#183;</span>
            <span className="text-xs text-ink-muted">
              {timeAgo(article.published_at)}
            </span>
          </>
        )}
      </div>

      <h3
        className={`font-serif font-bold leading-tight mb-2 ${
          featured ? "text-2xl md:text-3xl" : "text-lg"
        }`}
      >
        <a
          href={article.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="hover:text-accent-blue transition-colors"
        >
          {article.headline}
        </a>
      </h3>

      {article.summary && (
        <p
          className={`text-ink-light leading-relaxed ${
            featured ? "text-base md:text-lg" : "text-sm"
          }`}
        >
          {article.summary}
        </p>
      )}

      <div className="flex items-center gap-3 mt-3">
        <a
          href={article.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-xs text-accent-blue hover:underline font-medium"
        >
          <ExternalLink className="w-3 h-3" />
          Source
        </a>
        {article.author && (
          <span className="text-xs text-ink-muted">by {article.author}</span>
        )}
      </div>
    </article>
  );
}
