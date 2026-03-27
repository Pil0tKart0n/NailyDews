import logging
from datetime import datetime, timezone

from crawlers.base import BaseCrawler

logger = logging.getLogger(__name__)


class HackerNewsCrawler(BaseCrawler):
    """Crawler for Hacker News via Algolia API."""

    async def fetch_articles(self) -> list[dict]:
        response = await self.client.get(self.source.url)
        response.raise_for_status()

        data = response.json()
        articles = []

        for hit in data.get("hits", []):
            url = hit.get("url")
            if not url:
                # Self-posts link to HN itself
                url = f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}"

            published_at = None
            created_at_str = hit.get("created_at")
            if created_at_str:
                try:
                    published_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                except (ValueError, TypeError):
                    pass

            # Use HN points as a rough quality signal
            points = hit.get("points", 0)
            # Only include stories with decent engagement
            if points < 10:
                continue

            articles.append({
                "url": url,
                "title": hit.get("title", "Untitled"),
                "raw_content": hit.get("story_text", "") or "",
                "author": hit.get("author"),
                "published_at": published_at,
                "external_id": str(hit.get("objectID", "")),
                "image_url": None,
            })

        return articles
