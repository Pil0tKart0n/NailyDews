import { listDigests } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import Link from "next/link";
import { Calendar } from "lucide-react";

export const revalidate = 300;

export default async function ArchivePage() {
  let digests: Awaited<ReturnType<typeof listDigests>> = [];

  try {
    digests = await listDigests(60);
  } catch {
    digests = [];
  }

  return (
    <div>
      <h1 className="font-serif text-3xl font-black mb-6 border-b-2 border-ink pb-3">
        Archive
      </h1>

      {digests.length === 0 ? (
        <p className="text-ink-muted py-8 text-center">
          No past digests available yet. The first edition is coming soon!
        </p>
      ) : (
        <div className="space-y-3">
          {digests.map((d) => (
            <Link
              key={d.date}
              href={`/digest/${d.date}`}
              className="flex items-center gap-4 p-4 border border-ink/5 rounded hover:border-ink/20 hover:bg-paper-100 transition-all group"
            >
              <Calendar className="w-5 h-5 text-ink-muted group-hover:text-ink transition-colors" />
              <div className="flex-1">
                <h3 className="font-serif font-bold group-hover:text-accent-blue transition-colors">
                  {d.editorial_headline || formatDate(d.date)}
                </h3>
                <p className="text-sm text-ink-muted">
                  {formatDate(d.date)} -- {d.total_articles} articles
                </p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
