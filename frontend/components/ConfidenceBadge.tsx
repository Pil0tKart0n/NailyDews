import { cn } from "@/lib/utils";

const BADGE_CONFIG = {
  confirmed: {
    label: "Confirmed",
    className: "bg-accent-green/10 text-accent-green border-accent-green/30",
  },
  interpretation: {
    label: "Analysis",
    className: "bg-accent-yellow/10 text-accent-yellow border-accent-yellow/30",
  },
  rumor: {
    label: "Rumor",
    className: "bg-accent-orange/10 text-accent-orange border-accent-orange/30",
  },
};

export function ConfidenceBadge({ confidence }: { confidence: string }) {
  const config = BADGE_CONFIG[confidence as keyof typeof BADGE_CONFIG] || BADGE_CONFIG.interpretation;

  return (
    <span
      className={cn(
        "inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-full border",
        config.className
      )}
    >
      {config.label}
    </span>
  );
}
