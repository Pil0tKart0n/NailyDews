import { getTodayDigest } from "@/lib/api";
import { SectionGrid } from "@/components/SectionGrid";
import { Rss, Brain, Clock, Shield, ArrowRight, Sparkles } from "lucide-react";
import { formatDate } from "@/lib/utils";
import Link from "next/link";

export const revalidate = 300;

function HeroLanding() {
  return (
    <>
      <div className="-mx-4 -mt-8 mb-10">
        <div className="hero-gradient text-white">
          <div className="max-w-6xl mx-auto px-4 py-14 md:py-20">
            <div className="max-w-2xl">
              <div className="flex items-center gap-2 mb-5">
                <span className="inline-block w-2 h-2 rounded-full bg-green-400 animate-pulse-dot" />
                <span className="text-sm text-blue-200 font-medium">
                  Collecting from 50+ sources right now
                </span>
              </div>

              <h2 className="text-3xl md:text-5xl font-serif font-black leading-tight mb-5">
                All of AI.{" "}
                <span className="gradient-text">One Daily Read.</span>
              </h2>

              <p className="text-base md:text-lg text-blue-100 leading-relaxed mb-7 max-w-xl">
                Every evening at 19:00 CET, we distill hundreds of articles into
                one clean dashboard. AI-filtered, ranked, and summarized.
              </p>

              <div className="flex flex-col sm:flex-row gap-3">
                <Link
                  href="/about"
                  className="inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-white text-navy-900 font-semibold rounded-lg hover:bg-blue-50 transition-colors text-sm"
                >
                  How It Works
                  <ArrowRight className="w-4 h-4" />
                </Link>
                <Link
                  href="/archive"
                  className="inline-flex items-center justify-center gap-2 px-5 py-2.5 border border-white/25 text-white font-medium rounded-lg hover:bg-white/10 transition-colors text-sm"
                >
                  Past Digests
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="bg-white border-b border-ink/5 shadow-sm">
          <div className="max-w-6xl mx-auto px-4 py-4">
            <div className="grid grid-cols-4 gap-4 text-center">
              {[
                { icon: Rss, num: "50+", label: "Sources" },
                { icon: Brain, num: "5", label: "Sections" },
                { icon: Clock, num: "19:00", label: "Daily CET" },
                { icon: Shield, num: "100%", label: "Sourced" },
              ].map(({ icon: Icon, num, label }) => (
                <div key={label} className="flex items-center justify-center gap-2">
                  <Icon className="w-4 h-4 text-accent-blue hidden sm:block" />
                  <span className="font-black text-lg">{num}</span>
                  <span className="text-xs text-ink-muted hidden sm:block">{label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Preview cards */}
      <h3 className="font-bold text-center text-ink-muted text-sm uppercase tracking-widest mb-6">
        What you get every evening
      </h3>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-10">
        {[
          { color: "border-l-red-500", title: "Top Stories", desc: "The day's biggest AI news" },
          { color: "border-l-violet-500", title: "Models", desc: "Releases & benchmarks" },
          { color: "border-l-emerald-500", title: "Tools", desc: "Frameworks & APIs" },
          { color: "border-l-amber-500", title: "Research", desc: "Papers & findings" },
          { color: "border-l-sky-500", title: "Business", desc: "Deals & regulation" },
        ].map(({ color, title, desc }) => (
          <div key={title} className={`bg-white rounded-lg border border-ink/5 border-l-4 ${color} p-4`}>
            <h4 className="font-bold text-sm mb-0.5">{title}</h4>
            <p className="text-xs text-ink-muted">{desc}</p>
          </div>
        ))}
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
      {/* Digest header */}
      <div className="flex items-center justify-between mb-6 pb-4 border-b border-ink/5">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Sparkles className="w-4 h-4 text-accent-blue" />
            <time className="text-sm font-medium text-ink-muted">{formatDate(digest.date)}</time>
          </div>
          {digest.editorial_headline && (
            <h2 className="font-serif text-2xl md:text-3xl font-black leading-tight">
              {digest.editorial_headline}
            </h2>
          )}
        </div>
        <div className="text-right text-xs text-ink-muted hidden md:block">
          <p>{digest.total_articles} articles</p>
          <p>{digest.total_sources} sources</p>
        </div>
      </div>

      {/* Editorial brief */}
      {digest.editorial_summary && (
        <div className="bg-navy-50 border border-navy-100 rounded-xl p-4 md:p-5 mb-8">
          <p className="text-xs text-accent-blue font-semibold uppercase tracking-wider mb-2">
            Editor&apos;s Brief
          </p>
          <p className="text-sm text-ink-light leading-relaxed">
            {digest.editorial_summary}
          </p>
        </div>
      )}

      {/* All sections as card grids */}
      {digest.sections.map((section) => (
        <div key={section.category} id={section.category}>
          <SectionGrid section={section} />
        </div>
      ))}

      {digest.sections.length === 0 && <HeroLanding />}
    </div>
  );
}
