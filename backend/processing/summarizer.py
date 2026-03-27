import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Article
from llm.client import llm_client, QUALITY

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a concise AI news editor. Summarize articles in exactly 3 sentences and generate a compelling newspaper-style headline.

Rules:
- Summarize ONLY what is stated in the article. Do not add context or speculation.
- The headline should be informative and engaging, like a quality newspaper.
- Respond with ONLY valid JSON."""

PROMPT_TEMPLATE = """Summarize this article and generate a headline.

Title: {title}
Source: {source}
Content: {content}

Respond as JSON:
{{"headline": "Your Generated Headline Here", "summary": "Three sentence summary here."}}"""


async def summarize_articles(db: AsyncSession, batch_size: int = 10) -> int:
    """Generate summaries and headlines for categorized articles."""
    result = await db.execute(
        select(Article)
        .where(Article.status == "categorized")
        .order_by(Article.crawled_at.desc())
        .limit(batch_size)
    )
    articles = list(result.scalars().all())

    if not articles:
        return 0

    count = 0
    for article in articles:
        try:
            content = (article.clean_content or article.title)[:2000]

            prompt = PROMPT_TEMPLATE.format(
                title=article.title,
                source=article.source.name if article.source else "Unknown",
                content=content,
            )

            data = await llm_client.complete_json(
                prompt=prompt,
                system=SYSTEM_PROMPT,
                model=QUALITY,
                max_tokens=512,
                db=db,
                task="summarize",
                article_id=article.id,
            )

            article.generated_headline = data.get("headline", article.title)
            article.summary = data.get("summary", "")
            article.status = "summarized"
            count += 1

        except Exception as e:
            logger.error(f"Summary error for article {article.id}: {e}")
            # Still advance status so we don't get stuck
            article.status = "summarized"

    await db.commit()
    logger.info(f"Summarized {count} articles")
    return count
