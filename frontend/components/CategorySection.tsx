import { Section } from "@/lib/types";
import { ArticleCard } from "./ArticleCard";
import {
  Zap,
  Cpu,
  Wrench,
  BookOpen,
  Briefcase,
  Newspaper,
} from "lucide-react";

const ICONS: Record<string, React.ComponentType<{ className?: string }>> = {
  top_stories: Zap,
  models_releases: Cpu,
  tools_frameworks: Wrench,
  research_papers: BookOpen,
  business_regulation: Briefcase,
};

interface CategorySectionProps {
  section: Section;
  compact?: boolean;
}

export function CategorySection({ section, compact = false }: CategorySectionProps) {
  const Icon = ICONS[section.category] || Newspaper;

  return (
    <section className={compact ? "mb-8" : "mb-10"}>
      <div className={`flex items-center gap-2 border-b-2 border-ink pb-2 ${compact ? "mb-3" : "mb-5"}`}>
        <Icon className={compact ? "w-4 h-4" : "w-5 h-5"} />
        <h2 className={`font-serif font-bold uppercase tracking-wide ${compact ? "text-base" : "text-xl"}`}>
          {section.label}
        </h2>
        <span className="text-xs text-ink-muted ml-auto">
          {section.articles.length}
        </span>
      </div>

      <div className="space-y-0">
        {section.articles.map((article, i) => (
          <ArticleCard
            key={article.id}
            article={article}
            featured={!compact && section.category === "top_stories" && i === 0}
            compact={compact}
          />
        ))}
      </div>
    </section>
  );
}
