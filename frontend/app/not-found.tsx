import Link from "next/link";

export default function NotFound() {
  return (
    <div className="text-center py-20">
      <h2 className="font-serif text-4xl font-black mb-4">404</h2>
      <p className="text-ink-muted mb-6">
        This page could not be found. Perhaps the digest you&apos;re looking for
        hasn&apos;t been published yet.
      </p>
      <Link
        href="/"
        className="inline-block px-6 py-2 bg-ink text-paper-50 font-medium rounded hover:bg-ink-light transition-colors"
      >
        Back to Today&apos;s Digest
      </Link>
    </div>
  );
}
