export const metadata = {
  title: "Impressum - NailyDews",
};

export default function ImpressumPage() {
  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="font-serif text-3xl font-black mb-6 border-b-2 border-ink pb-3">
        Impressum
      </h1>

      <div className="prose prose-neutral max-w-none font-serif text-ink-light leading-relaxed space-y-6">
        <h2 className="font-serif text-xl font-bold text-ink mt-8 mb-3">
          Angaben gem. &sect; 5 TMG
        </h2>
        <p>
          [Name]<br />
          [Address]<br />
          [City, ZIP]<br />
          Germany
        </p>

        <h2 className="font-serif text-xl font-bold text-ink mt-8 mb-3">
          Kontakt
        </h2>
        <p>
          E-Mail: [email]
        </p>

        <h2 className="font-serif text-xl font-bold text-ink mt-8 mb-3">
          Haftungsausschluss
        </h2>
        <p>
          NailyDews aggregiert und fasst Nachrichteninhalte aus
          &ouml;ffentlich zug&auml;nglichen Quellen zusammen. Alle Artikel
          verlinken auf die Originalquelle. F&uuml;r die Richtigkeit und
          Vollst&auml;ndigkeit der verlinkten Inhalte &uuml;bernehmen wir keine
          Haftung.
        </p>

        <h2 className="font-serif text-xl font-bold text-ink mt-8 mb-3">
          Urheberrecht
        </h2>
        <p>
          Die durch NailyDews erstellten Zusammenfassungen stellen eine
          transformative Nutzung dar. Alle Originalinhalte geh&ouml;ren ihren
          jeweiligen Urhebern und Verlagen.
        </p>
      </div>
    </div>
  );
}
