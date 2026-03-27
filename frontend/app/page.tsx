import { getTodayDigest } from "@/lib/api";
import { EditorialSummary } from "@/components/EditorialSummary";
import { CategorySection } from "@/components/CategorySection";
import { Newspaper, Rss, Brain, Clock, Shield } from "lucide-react";
import Link from "next/link";

export const revalidate = 300;

function HeroExplainer() {
  return (
    <div className="text-center py-16 md:py-24">
      <Newspaper className="w-12 h-12 mx-auto text-ink-muted mb-5" />
      <h2 className="font-serif text-3xl md:text-4xl font-black mb-3">
        Your AI News. Curated Daily.
      </h2>
      <p className="text-ink-muted max-w-lg mx-auto mb-8 leading-relaxed">
        Every evening at 19:00 CET, we publish one clean digest of everything
        that happened in AI today. No noise. No clickbait. Just what matters.
      </p>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-2xl mx-auto mb-10">
        <div className="text-center p-3">
          <Rss className="w-5 h-5 mx-auto mb-2 text-accent-blue" />
          <p className="text-2xl font-black">50+</p>
          <p className="text-xs text-ink-muted">Sources</p>
        </div>
        <div className="text-center p-3">
          <Brain className="w-5 h-5 mx-auto mb-2 text-accent-blue" />
          <p className="text-2xl font-black">5</p>
          <p className="text-xs text-ink-muted">Sections</p>
        </div>
        <div className="text-center p-3">
          <Clock className="w-5 h-5 mx-auto mb-2 text-accent-blue" />
          <p className="text-2xl font-black">19:00</p>
          <p className="text-xs text-ink-muted">Daily at CET</p>
        </div>
        <div className="text-center p-3">
          <Shield className="w-5 h-5 mx-auto mb-2 text-accent-blue" />
          <p className="text-2xl font-black">100%</p>
          <p className="text-xs text-ink-muted">Source-linked</p>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
        <Link
          href="/about"
          className="inline-block px-5 py-2.5 bg-ink text-paper-50 font-medium rounded hover:bg-ink-light transition-colors text-sm"
        >
          Learn How It Works
        </Link>
        <Link
          href="/archive"
          className="inline-block px-5 py-2.5 border border-ink/20 font-medium rounded hover:border-ink/40 transition-colors text-sm"
        >
          Browse Past Digests
        </Link>
      </div>
    </div>
  );
}

export default async function HomePage() {
  let digest;

  try {
    digest = await getTodayDigest();
  } catch {
    return <HeroExplainer />;
  }

  return (
    <div>
      <EditorialSummary digest={digest} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main content: Top Stories + other sections */}
        <div className="lg:col-span-2">
          {digest.sections
            .filter((s) => s.category === "top_stories")
            .map((section) => (
              <div key={section.category} id={section.category}>
                <CategorySection section={section} />
              </div>
            ))}

          {digest.sections
            .filter(
              (s) =>
                s.category !== "top_stories" &&
                s.category !== "business_regulation"
            )
            .map((section) => (
              <div key={section.category} id={section.category}>
                <CategorySection section={section} />
              </div>
            ))}
        </div>

        {/* Sidebar: Business & lighter sections */}
        <aside className="lg:border-l lg:border-ink/5 lg:pl-8">
          {digest.sections
            .filter((s) => s.category === "business_regulation")
            .map((section) => (
              <div key={section.category} id={section.category}>
                <CategorySection section={section} compact />
              </div>
            ))}

          {/* Source transparency box */}
          <div className="mt-8 p-4 bg-paper-100 rounded border border-ink/5">
            <h3 className="font-serif font-bold text-sm mb-2">
              About This Digest
            </h3>
            <p className="text-xs text-ink-muted leading-relaxed">
              {digest.total_articles} articles from {digest.total_sources}{" "}
              sources were processed today. Every headline links to its original
              source. Confidence badges indicate verification level.
            </p>
            <Link
              href="/about"
              className="text-xs text-accent-blue hover:underline mt-2 inline-block"
            >
              How we select and rank articles
            </Link>
          </div>
        </aside>
      </div>

      {digest.sections.length === 0 && <HeroExplainer />}
    </div>
  );
}
