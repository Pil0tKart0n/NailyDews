import logging
from datetime import datetime, timezone
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from crawlers.base import BaseCrawler

logger = logging.getLogger(__name__)


# Scraper configs for specific sites
SCRAPER_CONFIGS = {
    # Meta AI Blog
    "meta-ai": {
        "article_selector": "a[href*='/blog/']",
        "title_selector": "h3, h2, span",
        "link_selector": "self",  # The article_selector itself is the link
        "content_selector": "p, span",
        "base_url": "https://ai.meta.com",
    },
    # Stability AI Blog
    "stability-ai": {
        "article_selector": "article, .blog-post, a[href*='/blog/']",
        "title_selector": "h2, h3, .title",
        "link_selector": "a",
        "content_selector": "p, .excerpt, .description",
        "base_url": "https://stability.ai",
    },
    # LMSYS / Chatbot Arena
    "lmsys": {
        "article_selector": ".post-card, article, li a[href*='/blog/']",
        "title_selector": "h2, h3, .post-title, span",
        "link_selector": "a",
        "content_selector": "p, .post-excerpt, .description",
        "base_url": "https://lmsys.org",
    },
    # The Batch (DeepLearning.AI)
    "the-batch": {
        "article_selector": "article, .post-card, a[href*='/the-batch/']",
        "title_selector": "h2, h3, .title",
        "link_selector": "a",
        "content_selector": "p, .excerpt",
        "base_url": "https://www.deeplearning.ai",
    },
    # LessWrong
    "lesswrong": {
        "article_selector": "div.posts-item",
        "title_selector": "a.posts-item-title-link",
        "link_selector": "a.posts-item-title-link",
        "content_selector": "div.posts-item-meta",
        "base_url": "https://www.lesswrong.com",
    },
    # AI Alignment Forum
    "ai-alignment-forum": {
        "article_selector": "div.posts-item",
        "title_selector": "a.posts-item-title-link",
        "link_selector": "a.posts-item-title-link",
        "content_selector": "div.posts-item-meta",
        "base_url": "https://www.alignmentforum.org",
    },
    # Generic fallback
    "generic": {
        "article_selector": "article, .post, .entry, .item, .card",
        "title_selector": "h2 a, h3 a, .title a, .post-title a, h2, h3",
        "link_selector": "h2 a, h3 a, .title a, .post-title a, a",
        "content_selector": "p, .excerpt, .summary, .description",
        "base_url": "",
    },
}


class WebScraper(BaseCrawler):
    """Generic web scraper for sites without RSS/API."""

    def _get_config(self) -> dict:
        """Get scraper config based on source slug."""
        for key, config in SCRAPER_CONFIGS.items():
            if key in self.source.slug:
                return config
        return SCRAPER_CONFIGS["generic"]

    async def fetch_articles(self) -> list[dict]:
        try:
            response = await self.client.get(self.source.url)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Web scrape error for {self.source.slug}: {e}")
            return []

        soup = BeautifulSoup(response.text, "lxml")
        config = self._get_config()
        base_url = config["base_url"] or self.source.url

        articles = []
        items = soup.select(config["article_selector"])[:30]

        for item in items:
            # Extract title
            title_elem = item.select_one(config["title_selector"])
            if not title_elem:
                continue
            title = title_elem.get_text(strip=True)
            if not title:
                continue

            # Extract link
            if config["link_selector"] == "self":
                # The item itself is an <a> tag
                href = item.get("href", "")
            else:
                link_elem = item.select_one(config["link_selector"])
                href = link_elem.get("href", "") if link_elem else ""
            if not href:
                continue
            url = urljoin(base_url, href)

            # Extract content/excerpt
            content_parts = []
            for sel in config["content_selector"].split(", "):
                elems = item.select(sel)
                for elem in elems[:3]:
                    text = elem.get_text(strip=True)
                    if text and len(text) > 20:
                        content_parts.append(text)
            content = " ".join(content_parts)

            articles.append({
                "url": url,
                "title": title,
                "raw_content": content,
                "author": None,
                "published_at": datetime.now(timezone.utc),  # Best guess for scraped content
                "external_id": url,
                "image_url": None,
            })

        return articles
