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

export function CategorySection({ section }: { section: Section }) {
  const Icon = ICONS[section.category] || Newspaper;

  return (
    <section className="mb-10">
      <div className="flex items-center gap-2 border-b-2 border-ink pb-2 mb-5">
        <Icon className="w-5 h-5" />
        <h2 className="font-serif text-xl font-bold uppercase tracking-wide">
          {section.label}
        </h2>
        <span className="text-xs text-ink-muted ml-auto">
          {section.articles.length} {section.articles.length === 1 ? "article" : "articles"}
        </span>
      </div>

      <div className="space-y-0">
        {section.articles.map((article, i) => (
          <ArticleCard
            key={article.id}
            article={article}
            featured={section.category === "top_stories" && i === 0}
          />
        ))}
      </div>
    </section>
  );
}
