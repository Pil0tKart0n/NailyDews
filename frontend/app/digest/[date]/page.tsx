import { getDigestByDate } from "@/lib/api";
import { EditorialSummary } from "@/components/EditorialSummary";
import { CategorySection } from "@/components/CategorySection";
import { notFound } from "next/navigation";

export const revalidate = 3600; // Cache for 1 hour (past digests don't change)

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
      <EditorialSummary digest={digest} />

      {digest.sections.map((section) => (
        <div key={section.category} id={section.category}>
          <CategorySection section={section} />
        </div>
      ))}
    </div>
  );
}
