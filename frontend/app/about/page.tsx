export const metadata = {
  title: "About - NailyDews",
};

export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="font-serif text-3xl font-black mb-6 border-b-2 border-ink pb-3">
        About NailyDews
      </h1>

      <div className="prose prose-neutral max-w-none font-serif text-ink-light leading-relaxed space-y-6">
        <p className="text-lg">
          NailyDews is an automated AI news aggregator that delivers a curated
          daily digest of the most important developments in artificial
          intelligence.
        </p>

        <h2 className="font-serif text-xl font-bold text-ink mt-8 mb-3">
          How It Works
        </h2>
        <p>
          Throughout the day, our system crawls over 20 trusted sources --
          official AI company blogs, academic preprint servers, tech media, and
          developer communities. Every article is automatically filtered,
          categorized, and summarized using AI technology.
        </p>
        <p>
          Each evening at 19:00 CET, the daily digest is published. Articles are
          ranked by importance, grouped into five sections, and presented in a
          clean newspaper-style layout.
        </p>

        <h2 className="font-serif text-xl font-bold text-ink mt-8 mb-3">
          Our Sources
        </h2>
        <p>
          We aggregate from official blogs (OpenAI, Anthropic, Google AI, Meta
          AI, Mistral, Hugging Face), tech media (TechCrunch, The Verge, Ars
          Technica), academic repositories (arXiv), and developer platforms
          (GitHub, Hacker News).
        </p>

        <h2 className="font-serif text-xl font-bold text-ink mt-8 mb-3">
          Confidence Badges
        </h2>
        <ul className="space-y-2">
          <li>
            <strong className="text-accent-green">Confirmed</strong> -- Official
            announcements or verified by multiple credible sources.
          </li>
          <li>
            <strong className="text-accent-yellow">Analysis</strong> -- Editorial
            commentary, analysis, or interpretation of confirmed events.
          </li>
          <li>
            <strong className="text-accent-orange">Rumor</strong> -- Unverified
            claims, leaks, or speculation. Treat with appropriate skepticism.
          </li>
        </ul>

        <h2 className="font-serif text-xl font-bold text-ink mt-8 mb-3">
          Transparency
        </h2>
        <p>
          Every article on NailyDews links directly to its original source. We
          do not generate facts -- our AI only summarizes and categorizes content
          from established publishers. When information is uncertain, it is
          clearly marked.
        </p>
      </div>
    </div>
  );
}
