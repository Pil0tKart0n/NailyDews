import logging
from datetime import datetime, timezone

import feedparser

from crawlers.base import BaseCrawler

logger = logging.getLogger(__name__)


class ArxivCrawler(BaseCrawler):
    """Crawler for arXiv API (returns Atom feed)."""

    async def fetch_articles(self) -> list[dict]:
        response = await self.client.get(self.source.url)
        response.raise_for_status()

        feed = feedparser.parse(response.text)
        articles = []

        for entry in feed.entries:
            # arXiv entries have id like http://arxiv.org/abs/2403.12345v1
            arxiv_id = entry.get("id", "")
            url = arxiv_id

            # Parse date
            published_at = None
            raw_date = entry.get("published")
            if raw_date:
                try:
                    published_at = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
                except (ValueError, TypeError):
                    pass

            # Authors
            authors = []
            if hasattr(entry, "authors"):
                authors = [a.get("name", "") for a in entry.authors]
            author_str = ", ".join(authors[:5])
            if len(authors) > 5:
                author_str += f" et al. ({len(authors)} authors)"

            # Content is the abstract
            summary = entry.get("summary", "")

            articles.append({
                "url": url,
                "title": entry.get("title", "Untitled").replace("\n", " "),
                "raw_content": summary,
                "author": author_str,
                "published_at": published_at,
                "external_id": arxiv_id,
                "image_url": None,
            })

        return articles
