import { getTodayDigest } from "@/lib/api";
import { EditorialSummary } from "@/components/EditorialSummary";
import { CategorySection } from "@/components/CategorySection";
import { Newspaper } from "lucide-react";

export const revalidate = 300; // Revalidate every 5 minutes

export default async function HomePage() {
  let digest;

  try {
    digest = await getTodayDigest();
  } catch {
    return (
      <div className="text-center py-20">
        <Newspaper className="w-16 h-16 mx-auto text-ink-muted mb-4" />
        <h2 className="font-serif text-2xl font-bold mb-2">
          Today&apos;s Edition Is Being Prepared
        </h2>
        <p className="text-ink-muted max-w-md mx-auto">
          Our AI editors are collecting and processing the latest news.
          The daily digest is published every evening at 19:00 CET.
          Check back soon!
        </p>
      </div>
    );
  }

  return (
    <div>
      <EditorialSummary digest={digest} />

      {digest.sections.map((section) => (
        <div key={section.category} id={section.category}>
          <CategorySection section={section} />
        </div>
      ))}

      {digest.sections.length === 0 && (
        <div className="text-center py-12 text-ink-muted">
          <p>No articles in today&apos;s digest yet. Check back later!</p>
        </div>
      )}
    </div>
  );
}
