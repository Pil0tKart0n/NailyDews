import { getTodayDigest } from "@/lib/api";
import { EditorialSummary } from "@/components/EditorialSummary";
import { CategorySection } from "@/components/CategorySection";
import { Rss, Brain, Clock, Shield, Zap, ArrowRight } from "lucide-react";
import Link from "next/link";

export const revalidate = 300;

function HeroLanding() {
  return (
    <>
      {/* Full-width hero - breaks out of the max-w container */}
      <div className="-mx-4 -mt-8 mb-12">
        <div className="hero-gradient text-white">
          <div className="max-w-6xl mx-auto px-4 py-16 md:py-24">
            <div className="max-w-3xl">
              <div className="flex items-center gap-2 mb-6">
                <span className="inline-block w-2 h-2 rounded-full bg-green-400 animate-pulse-dot" />
                <span className="text-sm text-blue-200 font-medium">
                  Collecting from 50+ sources right now
                </span>
              </div>

              <h2 className="text-4xl md:text-6xl font-serif font-black leading-tight mb-6">
                All of AI.{" "}
                <span className="gradient-text">One Daily Read.</span>
              </h2>

              <p className="text-lg md:text-xl text-blue-100 leading-relaxed mb-8 max-w-2xl">
                Every evening at 19:00 CET, we publish one curated digest of everything
                that happened in AI today. 50+ sources filtered, ranked, and summarized.
                No noise. No ads. Just what matters.
              </p>

              <div className="flex flex-col sm:flex-row gap-3">
                <Link
                  href="/about"
                  className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-white text-navy-900 font-semibold rounded-lg hover:bg-blue-50 transition-colors"
                >
                  See How It Works
                  <ArrowRight className="w-4 h-4" />
                </Link>
                <Link
                  href="/archive"
                  className="inline-flex items-center justify-center gap-2 px-6 py-3 border border-white/25 text-white font-medium rounded-lg hover:bg-white/10 transition-colors"
                >
                  Browse Past Digests
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Stats bar */}
        <div className="bg-white border-b border-ink/5 shadow-sm">
          <div className="max-w-6xl mx-auto px-4 py-5">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center">
                  <Rss className="w-5 h-5 text-accent-blue" />
                </div>
                <div>
                  <p className="text-2xl font-black">50+</p>
                  <p className="text-xs text-ink-muted">Sources Monitored</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center">
                  <Brain className="w-5 h-5 text-accent-blue" />
                </div>
                <div>
                  <p className="text-2xl font-black">5</p>
                  <p className="text-xs text-ink-muted">News Sections</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center">
                  <Clock className="w-5 h-5 text-accent-blue" />
                </div>
                <div>
                  <p className="text-2xl font-black">19:00</p>
                  <p className="text-xs text-ink-muted">Published Daily CET</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center">
                  <Shield className="w-5 h-5 text-accent-blue" />
                </div>
                <div>
                  <p className="text-2xl font-black">100%</p>
                  <p className="text-xs text-ink-muted">Source-Linked</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* What you get section */}
      <div className="mb-16">
        <h3 className="font-serif text-2xl font-bold text-center mb-8">
          Five sections. Everything you need.
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {[
            { icon: Zap, title: "Top Stories", desc: "The biggest AI news of the day" },
            { icon: Brain, title: "Models", desc: "New releases, benchmarks, capabilities" },
            { icon: Rss, title: "Tools", desc: "Frameworks, APIs, developer resources" },
            { icon: Shield, title: "Research", desc: "Papers, breakthroughs, findings" },
            { icon: Clock, title: "Business", desc: "Funding, regulation, partnerships" },
          ].map(({ icon: Icon, title, desc }) => (
            <div key={title} className="text-center p-5 rounded-xl border border-ink/5 bg-white hover:shadow-md transition-shadow">
              <Icon className="w-6 h-6 mx-auto mb-3 text-accent-blue" />
              <h4 className="font-bold text-sm mb-1">{title}</h4>
              <p className="text-xs text-ink-muted">{desc}</p>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default async function HomePage() {
  let digest;

  try {
    digest = await getTodayDigest();
  } catch {
    return <HeroLanding />;
  }

  return (
    <div>
      <EditorialSummary digest={digest} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main content */}
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

        {/* Sidebar */}
        <aside className="lg:border-l lg:border-ink/5 lg:pl-8">
          {digest.sections
            .filter((s) => s.category === "business_regulation")
            .map((section) => (
              <div key={section.category} id={section.category}>
                <CategorySection section={section} compact />
              </div>
            ))}

          <div className="mt-8 p-4 bg-paper-100 rounded-lg border border-ink/5">
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

      {digest.sections.length === 0 && <HeroLanding />}
    </div>
  );
}
