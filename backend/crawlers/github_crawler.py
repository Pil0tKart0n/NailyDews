import logging
from datetime import datetime, timezone

from crawlers.base import BaseCrawler

logger = logging.getLogger(__name__)

# AI-related topics to search for
AI_TOPICS = [
    "llm", "large-language-model", "gpt", "transformer", "diffusion",
    "machine-learning", "deep-learning", "neural-network", "ai-agent",
    "rag", "fine-tuning", "embedding", "vector-database",
]


class GitHubCrawler(BaseCrawler):
    """Crawler for trending AI repositories on GitHub."""

    async def fetch_articles(self) -> list[dict]:
        articles = []

        # Search for recently created AI repos with stars
        from datetime import timedelta
        cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
        query = "topic:machine-learning OR topic:llm OR topic:artificial-intelligence"
        url = "https://api.github.com/search/repositories"
        params = {
            "q": f"{query} created:>{cutoff} stars:>10",
            "sort": "stars",
            "order": "desc",
            "per_page": 30,
        }

        response = await self.client.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        for repo in data.get("items", []):
            full_name = repo.get("full_name", "")
            html_url = repo.get("html_url", "")

            description = repo.get("description", "") or ""
            topics = repo.get("topics", [])
            stars = repo.get("stargazers_count", 0)
            language = repo.get("language", "")

            # Build content from repo info
            content_parts = [description]
            if topics:
                content_parts.append(f"Topics: {', '.join(topics)}")
            if language:
                content_parts.append(f"Language: {language}")
            content_parts.append(f"Stars: {stars}")

            published_at = None
            created_at_str = repo.get("created_at")
            if created_at_str:
                try:
                    published_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                except (ValueError, TypeError):
                    pass

            articles.append({
                "url": html_url,
                "title": f"[GitHub] {full_name}: {description[:100]}" if description else f"[GitHub] {full_name}",
                "raw_content": " | ".join(content_parts),
                "author": repo.get("owner", {}).get("login", ""),
                "published_at": published_at,
                "external_id": str(repo.get("id", "")),
                "image_url": repo.get("owner", {}).get("avatar_url"),
            })

        return articles
