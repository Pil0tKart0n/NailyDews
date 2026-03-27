import { listDigests } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import Link from "next/link";
import { Calendar, ArrowRight, Newspaper } from "lucide-react";

export const revalidate = 300;

export const metadata = {
  title: "Archive",
  description: "Browse past editions of the NailyDews AI daily digest.",
};

export default async function ArchivePage() {
  let digests: Awaited<ReturnType<typeof listDigests>> = [];

  try {
    digests = await listDigests(60);
  } catch {
    digests = [];
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="font-serif text-3xl md:text-4xl font-black mb-2">
          Archive
        </h1>
        <p className="text-ink-muted">
          Every evening edition, preserved. Browse past digests to catch up on what you missed.
        </p>
      </div>

      {digests.length === 0 ? (
        <div className="text-center py-16 rounded-xl border-2 border-dashed border-ink/10 bg-white">
          <Newspaper className="w-12 h-12 mx-auto text-ink-muted/40 mb-4" />
          <h2 className="font-serif text-xl font-bold mb-2 text-ink-light">
            The First Edition Is Coming
          </h2>
          <p className="text-ink-muted max-w-md mx-auto mb-6">
            Our AI editors are collecting and processing news from 50+ sources.
            The first daily digest will be published at 19:00 CET.
          </p>
          <Link
            href="/about"
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-accent-blue text-white font-medium rounded-lg hover:bg-blue-700 transition-colors text-sm"
          >
            Learn How It Works
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      ) : (
        <div className="space-y-2">
          {digests.map((d) => (
            <Link
              key={d.date}
              href={`/digest/${d.date}`}
              className="flex items-center gap-4 p-4 bg-white border border-ink/5 rounded-lg hover:border-accent-blue/30 hover:shadow-sm transition-all group"
            >
              <div className="w-10 h-10 rounded-lg bg-navy-50 flex items-center justify-center shrink-0">
                <Calendar className="w-5 h-5 text-accent-blue" />
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="font-serif font-bold truncate group-hover:text-accent-blue transition-colors">
                  {d.editorial_headline || formatDate(d.date)}
                </h3>
                <p className="text-sm text-ink-muted">
                  {formatDate(d.date)} &middot; {d.total_articles} articles
                </p>
              </div>
              <ArrowRight className="w-4 h-4 text-ink-muted group-hover:text-accent-blue transition-colors shrink-0" />
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
