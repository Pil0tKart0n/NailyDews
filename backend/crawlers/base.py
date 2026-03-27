import hashlib
import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone

import httpx
from bs4 import BeautifulSoup
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Article, CrawlLog, Source

logger = logging.getLogger(__name__)


class BaseCrawler(ABC):
    """Base class for all news source crawlers."""

    def __init__(self, source: Source):
        self.source = source
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={"User-Agent": "NailyDews/1.0 (AI News Aggregator)"},
            follow_redirects=True,
        )

    @abstractmethod
    async def fetch_articles(self) -> list[dict]:
        """Fetch raw article data from source. Returns list of dicts with keys:
        url, title, raw_content, author, published_at, external_id, image_url
        """
        pass

    async def crawl(self, db: AsyncSession) -> int:
        """Run full crawl cycle. Returns number of new articles."""
        start = time.monotonic()
        new_count = 0
        found_count = 0

        try:
            raw_articles = await self.fetch_articles()
            found_count = len(raw_articles)

            for raw in raw_articles:
                # Skip if URL already exists
                existing = await db.execute(
                    select(Article).where(Article.url == raw["url"]).limit(1)
                )
                if existing.scalar_one_or_none():
                    continue

                clean = self.strip_html(raw.get("raw_content", "") or "")
                content_hash = hashlib.sha256(clean.encode()).hexdigest() if clean else None

                # Skip if content hash already exists (duplicate content, different URL)
                if content_hash:
                    dup = await db.execute(
                        select(Article).where(Article.content_hash == content_hash).limit(1)
                    )
                    if dup.scalar_one_or_none():
                        continue

                article = Article(
                    source_id=self.source.id,
                    url=raw["url"],
                    title=raw.get("title", "Untitled"),
                    raw_content=raw.get("raw_content"),
                    clean_content=clean,
                    author=raw.get("author"),
                    published_at=raw.get("published_at"),
                    external_id=raw.get("external_id"),
                    image_url=raw.get("image_url"),
                    content_hash=content_hash,
                    word_count=len(clean.split()) if clean else 0,
                    status="raw",
                )
                db.add(article)
                new_count += 1

            # Update source
            self.source.last_crawled_at = datetime.now(timezone.utc)
            self.source.error_count = 0

            duration_ms = int((time.monotonic() - start) * 1000)
            db.add(CrawlLog(
                source_id=self.source.id,
                status="success",
                articles_found=found_count,
                articles_new=new_count,
                duration_ms=duration_ms,
            ))

            await db.commit()
            logger.info(f"[{self.source.slug}] Found {found_count}, new {new_count} ({duration_ms}ms)")

        except Exception as e:
            await db.rollback()
            self.source.error_count = (self.source.error_count or 0) + 1
            duration_ms = int((time.monotonic() - start) * 1000)
            db.add(CrawlLog(
                source_id=self.source.id,
                status="error",
                error_message=str(e)[:1000],
                duration_ms=duration_ms,
            ))
            await db.commit()
            logger.error(f"[{self.source.slug}] Crawl error: {e}")

        return new_count

    @staticmethod
    def strip_html(html: str) -> str:
        """Strip HTML tags and normalize whitespace."""
        if not html:
            return ""
        soup = BeautifulSoup(html, "lxml")
        # Remove script and style elements
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator=" ")
        # Normalize whitespace
        return " ".join(text.split()).strip()

    async def close(self):
        await self.client.aclose()
