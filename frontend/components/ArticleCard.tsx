import { Article } from "@/lib/types";
import { timeAgo } from "@/lib/utils";
import { ConfidenceBadge } from "./ConfidenceBadge";

interface ArticleCardProps {
  article: Article;
  featured?: boolean;
}

export function ArticleCard({ article, featured = false }: ArticleCardProps) {
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
          <span className="text-xs text-ink-muted">
            {timeAgo(article.published_at)}
          </span>
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
          className="text-xs text-accent-blue hover:underline font-medium"
        >
          Read original source
        </a>
        {article.author && (
          <span className="text-xs text-ink-muted">by {article.author}</span>
        )}
      </div>
    </article>
  );
}
