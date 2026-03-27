import logging
from datetime import datetime, timezone

from crawlers.base import BaseCrawler

logger = logging.getLogger(__name__)


class DiscordScraper(BaseCrawler):
    """Scraper for public Discord channels via Bot API.

    Requires DISCORD_BOT_TOKEN in environment.
    The source URL format: discord://{channel_id}
    The source name should describe the server/channel.

    Only scrapes channels where the bot has been invited and has read permissions.
    """

    async def fetch_articles(self) -> list[dict]:
        from config import settings

        token = getattr(settings, "discord_bot_token", "")
        if not token:
            logger.warning(f"No DISCORD_BOT_TOKEN set, skipping {self.source.slug}")
            return []

        # Extract channel ID from URL (format: discord://{channel_id})
        channel_id = self.source.url.replace("discord://", "")
        if not channel_id.isdigit():
            logger.error(f"Invalid Discord channel ID: {channel_id}")
            return []

        api_url = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit=50"

        try:
            response = await self.client.get(
                api_url,
                headers={"Authorization": f"Bot {token}"},
            )
            response.raise_for_status()
            messages = response.json()
        except Exception as e:
            logger.error(f"Discord fetch error for {self.source.slug}: {e}")
            return []

        articles = []

        for msg in messages:
            content = msg.get("content", "").strip()
            if not content or len(content) < 50:
                continue

            # Skip bot messages
            author = msg.get("author", {})
            if author.get("bot"):
                continue

            # Extract links from message
            links = []
            for word in content.split():
                if word.startswith("http://") or word.startswith("https://"):
                    links.append(word)

            # Build a pseudo-article from the message
            author_name = author.get("username", "Unknown")
            msg_id = msg.get("id", "")

            # Use embedded links as the article URL, or fall back to Discord message link
            article_url = links[0] if links else f"https://discord.com/channels/{channel_id}/{msg_id}"

            # Parse timestamp
            published_at = None
            timestamp = msg.get("timestamp")
            if timestamp:
                try:
                    published_at = datetime.fromisoformat(timestamp.replace("+00:00", "+00:00"))
                except (ValueError, TypeError):
                    pass

            # Include embeds
            embeds = msg.get("embeds", [])
            embed_texts = []
            for embed in embeds:
                if embed.get("title"):
                    embed_texts.append(embed["title"])
                if embed.get("description"):
                    embed_texts.append(embed["description"])

            full_content = content
            if embed_texts:
                full_content += "\n\n" + "\n".join(embed_texts)

            # Extract title: first line or first 100 chars
            title_line = content.split("\n")[0][:150]
            if len(title_line) < 10:
                title_line = content[:150]

            articles.append({
                "url": article_url,
                "title": f"[Discord/{self.source.name}] {title_line}",
                "raw_content": full_content,
                "author": author_name,
                "published_at": published_at,
                "external_id": msg_id,
                "image_url": None,
            })

        return articles
