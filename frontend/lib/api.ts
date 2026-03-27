import { Digest, DigestListItem } from "./types";

const API_URL = process.env.API_URL || "http://localhost:8000";

async function fetchAPI<T>(path: string): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    next: { revalidate: 300 }, // Cache for 5 minutes
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }

  const json = await res.json();
  return json.data;
}

export async function getTodayDigest(): Promise<Digest> {
  return fetchAPI<Digest>("/api/digests/today");
}

export async function getDigestByDate(date: string): Promise<Digest> {
  return fetchAPI<Digest>(`/api/digests/${date}`);
}

export async function listDigests(limit = 30): Promise<DigestListItem[]> {
  return fetchAPI<DigestListItem[]>(`/api/digests?limit=${limit}`);
}
