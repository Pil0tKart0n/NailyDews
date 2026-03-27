import asyncio
import logging
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from crawlers.rss_crawler import RSSCrawler
from crawlers.arxiv_crawler import ArxivCrawler
from crawlers.hackernews_crawler import HackerNewsCrawler
from crawlers.github_crawler import GitHubCrawler
from crawlers.reddit_crawler import RedditCrawler
from crawlers.web_scraper import WebScraper
from crawlers.discord_scraper import DiscordScraper
from db.connection import async_session
from db.models import Source
from digest.generator import generate_digest
from processing.pipeline import run_pipeline

logger = logging.getLogger(__name__)

CRAWLER_MAP = {
    "rss": RSSCrawler,
    "api": None,  # Determined by slug
}


def get_crawler_class(source: Source):
    """Get the appropriate crawler class for a source."""
    if source.source_type == "rss":
        return RSSCrawler
    if source.source_type == "scraper":
        return WebScraper
    if source.source_type == "discord":
        return DiscordScraper
    if "arxiv" in source.slug:
        return ArxivCrawler
    if "hackernews" in source.slug:
        return HackerNewsCrawler
    if "github" in source.slug:
        return GitHubCrawler
    if "reddit" in source.slug:
        return RedditCrawler
    return RSSCrawler  # fallback


async def crawl_all_sources():
    """Crawl all active sources that are due."""
    logger.info("Starting crawl cycle...")
    async with async_session() as db:
        result = await db.execute(
            select(Source).where(Source.is_active == True)
        )
        sources = list(result.scalars().all())

        now = datetime.now(timezone.utc)
        total_new = 0

        for source in sources:
            # Check if it's time to crawl this source
            if source.last_crawled_at:
                minutes_since = (now - source.last_crawled_at).total_seconds() / 60
                if minutes_since < source.crawl_interval_minutes:
                    continue

            # Skip sources with too many consecutive errors
            if source.error_count and source.error_count >= 5:
                logger.warning(f"Skipping {source.slug}: {source.error_count} consecutive errors")
                continue

            crawler_class = get_crawler_class(source)
            crawler = crawler_class(source)
            try:
                new = await crawler.crawl(db)
                total_new += new
            finally:
                await crawler.close()

        logger.info(f"Crawl cycle complete: {total_new} new articles from {len(sources)} sources")


async def process_articles():
    """Run the processing pipeline on unprocessed articles."""
    logger.info("Starting processing pipeline...")
    async with async_session() as db:
        stats = await run_pipeline(db)
        logger.info(f"Processing complete: {stats}")


async def generate_daily_digest():
    """Generate the daily digest."""
    logger.info("Generating daily digest...")
    async with async_session() as db:
        digest = await generate_digest(db)
        if digest:
            logger.info(f"Digest published: {digest.slug}")
        else:
            logger.warning("No digest generated (already exists or no articles)")


def run_async(coro):
    """Helper to run async functions from sync APScheduler."""
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(coro)
    finally:
        loop.close()


def job_crawl():
    run_async(crawl_all_sources())


def job_process():
    run_async(process_articles())


def job_digest():
    run_async(generate_daily_digest())
