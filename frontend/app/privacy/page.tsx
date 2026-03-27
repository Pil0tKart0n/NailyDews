export const metadata = {
  title: "Privacy Policy - NailyDews",
};

export default function PrivacyPage() {
  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="font-serif text-3xl font-black mb-6 border-b-2 border-ink pb-3">
        Privacy Policy
      </h1>

      <div className="prose prose-neutral max-w-none font-serif text-ink-light leading-relaxed space-y-6">
        <p>Last updated: March 2026</p>

        <h2 className="font-serif text-xl font-bold text-ink mt-8 mb-3">
          Overview
        </h2>
        <p>
          NailyDews is committed to protecting your privacy. This policy
          explains what data we collect and how we use it.
        </p>

        <h2 className="font-serif text-xl font-bold text-ink mt-8 mb-3">
          Data We Collect
        </h2>
        <p>
          For anonymous visitors (no account required): We collect no personal
          data. We do not use tracking cookies, Google Analytics, or any
          third-party tracking services.
        </p>
        <p>
          We may use privacy-focused, self-hosted analytics that collect only
          aggregate page view counts without identifying individual visitors.
        </p>

        <h2 className="font-serif text-xl font-bold text-ink mt-8 mb-3">
          Cookies
        </h2>
        <p>
          Anonymous visitors: No cookies are set. If you create an account in
          the future, essential session cookies will be used to keep you logged
          in. No advertising or tracking cookies are ever used.
        </p>

        <h2 className="font-serif text-xl font-bold text-ink mt-8 mb-3">
          Your Rights (GDPR/DSGVO)
        </h2>
        <ul className="space-y-2">
          <li>Right of access to your personal data</li>
          <li>Right to rectification of inaccurate data</li>
          <li>Right to erasure (&quot;right to be forgotten&quot;)</li>
          <li>Right to data portability</li>
          <li>Right to withdraw consent at any time</li>
        </ul>

        <h2 className="font-serif text-xl font-bold text-ink mt-8 mb-3">
          Contact
        </h2>
        <p>
          For privacy-related inquiries, please contact us at the address listed
          in our Impressum.
        </p>
      </div>
    </div>
  );
}
