import { Section } from "@/lib/types";
import { NewsCard } from "./NewsCard";
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

const SECTION_COLORS: Record<string, string> = {
  top_stories: "text-red-500",
  models_releases: "text-violet-500",
  tools_frameworks: "text-emerald-500",
  research_papers: "text-amber-600",
  business_regulation: "text-sky-500",
};

export function SectionGrid({ section }: { section: Section }) {
  const Icon = ICONS[section.category] || Newspaper;
  const color = SECTION_COLORS[section.category] || "text-ink-muted";

  return (
    <section className="mb-10">
      {/* Section header */}
      <div className="flex items-center gap-2.5 mb-4">
        <Icon className={`w-5 h-5 ${color}`} />
        <h2 className="font-bold text-lg tracking-tight">
          {section.label}
        </h2>
        <span className="text-xs text-ink-muted bg-paper-100 px-2 py-0.5 rounded-full">
          {section.articles.length}
        </span>
      </div>

      {/* Cards grid */}
      {section.category === "top_stories" ? (
        // Top stories: hero card + 2-column grid
        <div className="space-y-3">
          {section.articles.length > 0 && (
            <NewsCard article={section.articles[0]} size="hero" />
          )}
          {section.articles.length > 1 && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {section.articles.slice(1).map((article) => (
                <NewsCard key={article.id} article={article} size="medium" />
              ))}
            </div>
          )}
        </div>
      ) : (
        // Other sections: responsive grid
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {section.articles.map((article) => (
            <NewsCard key={article.id} article={article} size="medium" />
          ))}
        </div>
      )}
    </section>
  );
}
