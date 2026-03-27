import logging
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import feedparser

from crawlers.base import BaseCrawler

logger = logging.getLogger(__name__)


class RSSCrawler(BaseCrawler):
    """Generic RSS/Atom feed crawler."""

    async def fetch_articles(self) -> list[dict]:
        response = await self.client.get(self.source.url)
        response.raise_for_status()

        feed = feedparser.parse(response.text)
        articles = []

        for entry in feed.entries:
            url = entry.get("link", "")
            if not url:
                continue

            # Parse published date
            published_at = None
            for date_field in ("published", "updated", "created"):
                raw_date = entry.get(date_field)
                if raw_date:
                    try:
                        published_at = parsedate_to_datetime(raw_date)
                        if published_at.tzinfo is None:
                            published_at = published_at.replace(tzinfo=timezone.utc)
                        break
                    except (ValueError, TypeError):
                        try:
                            # Try ISO format
                            published_at = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
                            break
                        except (ValueError, TypeError):
                            continue

            # Extract content
            content = ""
            if hasattr(entry, "content") and entry.content:
                content = entry.content[0].get("value", "")
            elif hasattr(entry, "summary"):
                content = entry.summary or ""
            elif hasattr(entry, "description"):
                content = entry.description or ""

            # Extract image
            image_url = None
            if hasattr(entry, "media_content") and entry.media_content:
                image_url = entry.media_content[0].get("url")
            elif hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
                image_url = entry.media_thumbnail[0].get("url")

            articles.append({
                "url": url,
                "title": entry.get("title", "Untitled"),
                "raw_content": content,
                "author": entry.get("author"),
                "published_at": published_at,
                "external_id": entry.get("id", url),
                "image_url": image_url,
            })

        return articles
