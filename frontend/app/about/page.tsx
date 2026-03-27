import { Rss, Brain, Shield, Clock, Filter, Layers } from "lucide-react";

export const metadata = {
  title: "How It Works - NailyDews",
  description: "Learn how NailyDews collects, filters, and ranks AI news from 50+ sources into one daily digest.",
};

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="font-serif text-3xl md:text-4xl font-black mb-3 text-center">
        How NailyDews Works
      </h1>
      <p className="text-center text-ink-muted mb-10 max-w-xl mx-auto">
        One daily digest. 50+ sources. Zero noise.
        Here&apos;s how we turn hundreds of articles into the 20 that matter.
      </p>

      {/* Pipeline visual */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-14">
        <div className="text-center p-6 border border-ink/5 rounded-lg bg-paper-100">
          <Rss className="w-8 h-8 mx-auto mb-3 text-accent-blue" />
          <h3 className="font-serif font-bold mb-2">1. Collect</h3>
          <p className="text-sm text-ink-muted">
            Our crawlers check 50+ sources every 30 minutes: official AI blogs,
            arXiv papers, Reddit, Hacker News, tech media, expert newsletters.
          </p>
        </div>
        <div className="text-center p-6 border border-ink/5 rounded-lg bg-paper-100">
          <Filter className="w-8 h-8 mx-auto mb-3 text-accent-blue" />
          <h3 className="font-serif font-bold mb-2">2. Process</h3>
          <p className="text-sm text-ink-muted">
            AI filters non-relevant content, categorizes articles into 5 sections,
            generates concise summaries, and clusters related stories together.
          </p>
        </div>
        <div className="text-center p-6 border border-ink/5 rounded-lg bg-paper-100">
          <Layers className="w-8 h-8 mx-auto mb-3 text-accent-blue" />
          <h3 className="font-serif font-bold mb-2">3. Publish</h3>
          <p className="text-sm text-ink-muted">
            At 19:00 CET, the top stories are ranked by importance and published
            as a clean, newspaper-style digest with an editorial summary.
          </p>
        </div>
      </div>

      {/* Sources */}
      <section className="mb-12">
        <h2 className="font-serif text-2xl font-bold border-b-2 border-ink pb-2 mb-5">
          Our Sources
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-bold text-sm uppercase tracking-wider text-ink-muted mb-3">
              Official AI Labs
            </h3>
            <p className="text-sm text-ink-light leading-relaxed">
              OpenAI, Anthropic, Google DeepMind, Meta AI, Mistral, Nvidia,
              Hugging Face, Cohere, Together AI, Replicate, Stability AI,
              Microsoft AI, AI21 Labs.
            </p>
          </div>
          <div>
            <h3 className="font-bold text-sm uppercase tracking-wider text-ink-muted mb-3">
              Tech Media
            </h3>
            <p className="text-sm text-ink-light leading-relaxed">
              TechCrunch, The Verge, Wired, Ars Technica, VentureBeat,
              MIT Technology Review, Bloomberg, Reuters, Semafor.
            </p>
          </div>
          <div>
            <h3 className="font-bold text-sm uppercase tracking-wider text-ink-muted mb-3">
              Expert Blogs & Research
            </h3>
            <p className="text-sm text-ink-light leading-relaxed">
              Simon Willison, Andrej Karpathy, Lilian Weng, Chip Huyen,
              Sebastian Raschka, arXiv (4 categories), LessWrong,
              AI Alignment Forum, EleutherAI, LMSYS.
            </p>
          </div>
          <div>
            <h3 className="font-bold text-sm uppercase tracking-wider text-ink-muted mb-3">
              Communities & Newsletters
            </h3>
            <p className="text-sm text-ink-light leading-relaxed">
              12 Reddit communities (r/MachineLearning, r/LocalLLaMA, r/ClaudeAI...),
              Hacker News, Latent Space, Interconnects, One Useful Thing,
              Import AI, The Batch, and more.
            </p>
          </div>
        </div>
      </section>

      {/* Confidence system */}
      <section className="mb-12">
        <h2 className="font-serif text-2xl font-bold border-b-2 border-ink pb-2 mb-5">
          Confidence Badges
        </h2>
        <p className="text-sm text-ink-muted mb-4">
          Every article is assessed for reliability. You always know what you&apos;re reading:
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-lg border border-accent-green/20 bg-accent-green/5">
            <span className="inline-block px-2 py-0.5 text-xs font-medium rounded-full border border-accent-green/30 text-accent-green bg-accent-green/10 mb-2">
              Confirmed
            </span>
            <p className="text-sm text-ink-light">
              Official announcements or facts verified by multiple credible sources.
            </p>
          </div>
          <div className="p-4 rounded-lg border border-accent-yellow/20 bg-accent-yellow/5">
            <span className="inline-block px-2 py-0.5 text-xs font-medium rounded-full border border-accent-yellow/30 text-accent-yellow bg-accent-yellow/10 mb-2">
              Analysis
            </span>
            <p className="text-sm text-ink-light">
              Editorial commentary or interpretation based on confirmed events.
            </p>
          </div>
          <div className="p-4 rounded-lg border border-accent-orange/20 bg-accent-orange/5">
            <span className="inline-block px-2 py-0.5 text-xs font-medium rounded-full border border-accent-orange/30 text-accent-orange bg-accent-orange/10 mb-2">
              Rumor
            </span>
            <p className="text-sm text-ink-light">
              Unverified claims, leaks, or speculation. Read with appropriate skepticism.
            </p>
          </div>
        </div>
      </section>

      {/* Transparency */}
      <section className="mb-12">
        <h2 className="font-serif text-2xl font-bold border-b-2 border-ink pb-2 mb-5">
          Transparency
        </h2>
        <div className="bg-paper-100 p-6 rounded-lg border border-ink/5">
          <ul className="space-y-3 text-sm text-ink-light">
            <li className="flex items-start gap-3">
              <Shield className="w-4 h-4 text-accent-blue mt-0.5 shrink-0" />
              <span>Every article links directly to its original source. We never generate facts.</span>
            </li>
            <li className="flex items-start gap-3">
              <Shield className="w-4 h-4 text-accent-blue mt-0.5 shrink-0" />
              <span>AI summaries are extractive: they only restate what the original article says.</span>
            </li>
            <li className="flex items-start gap-3">
              <Shield className="w-4 h-4 text-accent-blue mt-0.5 shrink-0" />
              <span>Uncertain information is always marked. No invented quotes or fabricated details.</span>
            </li>
            <li className="flex items-start gap-3">
              <Shield className="w-4 h-4 text-accent-blue mt-0.5 shrink-0" />
              <span>No tracking, no ads, no third-party cookies. Privacy by design.</span>
            </li>
          </ul>
        </div>
      </section>
    </div>
  );
}
