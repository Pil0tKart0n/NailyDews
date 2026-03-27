import { getDigestByDate } from "@/lib/api";
import { SectionGrid } from "@/components/SectionGrid";
import { formatDate } from "@/lib/utils";
import { notFound } from "next/navigation";
import { Sparkles } from "lucide-react";

export const revalidate = 3600;

export default async function DigestPage({
  params,
}: {
  params: { date: string };
}) {
  let digest;

  try {
    digest = await getDigestByDate(params.date);
  } catch {
    notFound();
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

      {digest.sections.map((section) => (
        <div key={section.category} id={section.category}>
          <SectionGrid section={section} />
        </div>
      ))}
    </div>
  );
}
