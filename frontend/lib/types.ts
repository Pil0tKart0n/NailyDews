export interface Article {
  id: number;
  headline: string;
  original_title: string;
  summary: string;
  source_name: string;
  source_url: string;
  confidence: "confirmed" | "interpretation" | "rumor";
  importance_score: number;
  published_at: string | null;
  category: string;
  is_top_story: boolean;
  image_url: string | null;
  author: string | null;
}

export interface Section {
  category: string;
  label: string;
  articles: Article[];
}

export interface Digest {
  date: string;
  slug: string;
  editorial_headline: string;
  editorial_summary: string;
  total_articles: number;
  total_sources: number;
  published_at: string | null;
  sections: Section[];
}

export interface DigestListItem {
  date: string;
  slug: string;
  editorial_headline: string;
  total_articles: number;
  published_at: string | null;
}
