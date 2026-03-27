import logging
from datetime import datetime, timezone

from crawlers.base import BaseCrawler

logger = logging.getLogger(__name__)

# Top AI/ML subreddits where the elite discuss
SUBREDDITS = [
    "MachineLearning",      # Academic ML, paper discussions, industry news
    "LocalLLaMA",           # Open-source LLM community, model releases, benchmarks
    "artificial",           # General AI news and discussion
    "ChatGPT",              # ChatGPT news, updates, use cases
    "OpenAI",               # OpenAI-specific news
    "ClaudeAI",             # Anthropic/Claude community
    "singularity",          # AGI discussions, future of AI
    "StableDiffusion",      # Image generation, diffusion models
    "mlops",                # ML operations, deployment, infrastructure
    "LanguageTechnology",   # NLP research and tools
    "deeplearning",         # Deep learning research
    "LLMDevs",             # LLM developer community
]


class RedditCrawler(BaseCrawler):
    """Crawler for Reddit AI/ML subreddits via JSON API (no auth needed)."""

    async def fetch_articles(self) -> list[dict]:
        articles = []

        # The source URL contains the subreddit name
        # Format: https://www.reddit.com/r/{subreddit}/hot.json?limit=25
        subreddit = self.source.slug.replace("reddit-", "")
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=25"

        try:
            response = await self.client.get(
                url,
                headers={
                    "User-Agent": "NailyDews/1.0 (AI News Aggregator; contact@nailydews.com)",
                },
            )
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            logger.error(f"Reddit fetch error for r/{subreddit}: {e}")
            return []

        for post in data.get("data", {}).get("children", []):
            post_data = post.get("data", {})

            # Skip pinned/stickied posts
            if post_data.get("stickied"):
                continue

            # Only posts with decent engagement
            score = post_data.get("score", 0)
            if score < 20:
                continue

            url = post_data.get("url", "")
            permalink = f"https://www.reddit.com{post_data.get('permalink', '')}"

            # If it's a self-post, use the Reddit permalink
            is_self = post_data.get("is_self", False)
            article_url = permalink if is_self else url

            # Content: selftext for self-posts, or title + link for link posts
            content = post_data.get("selftext", "") or ""
            if not is_self and url:
                content = f"Link: {url}\n\n{content}"

            # Add engagement context
            num_comments = post_data.get("num_comments", 0)
            content += f"\n\n[Reddit Score: {score}, Comments: {num_comments}]"

            published_at = None
            created_utc = post_data.get("created_utc")
            if created_utc:
                published_at = datetime.fromtimestamp(created_utc, tz=timezone.utc)

            # Extract thumbnail/preview image
            image_url = None
            preview = post_data.get("preview", {})
            if preview and "images" in preview:
                images = preview["images"]
                if images:
                    image_url = images[0].get("source", {}).get("url", "").replace("&amp;", "&")

            articles.append({
                "url": article_url,
                "title": f"[r/{subreddit}] {post_data.get('title', 'Untitled')}",
                "raw_content": content,
                "author": post_data.get("author"),
                "published_at": published_at,
                "external_id": post_data.get("name", ""),  # Reddit fullname e.g. t3_abc123
                "image_url": image_url,
            })

        return articles
