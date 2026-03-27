import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Article
from llm.client import llm_client, HAIKU

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You assess the confidence level of news articles. Respond with ONLY valid JSON.

Levels:
- "confirmed": Official announcement, press release, or verified by multiple credible sources
- "interpretation": Analysis, opinion, editorial, or commentary based on confirmed events
- "rumor": Unverified claim, single anonymous source, leaked information, speculation"""

BATCH_PROMPT_TEMPLATE = """Assess the confidence level of each article.

Articles:
{articles}

Respond as JSON array:
[{{"id": 1, "confidence": "confirmed"}}, ...]"""


async def score_confidence(db: AsyncSession, batch_size: int = 20) -> int:
    """Score article confidence (confirmed/interpretation/rumor)."""
    result = await db.execute(
        select(Article)
        .where(Article.status == "summarized")
        .order_by(Article.crawled_at.desc())
        .limit(batch_size)
    )
    articles = list(result.scalars().all())

    if not articles:
        return 0

    # Tier 1 sources automatically get "confirmed"
    auto_confirmed = []
    needs_scoring = []

    for a in articles:
        if a.source and a.source.tier == 1:
            a.confidence = "confirmed"
            a.status = "scored"
            auto_confirmed.append(a)
        else:
            needs_scoring.append(a)

    if needs_scoring:
        article_texts = []
        for i, a in enumerate(needs_scoring):
            content_preview = (a.clean_content or a.title)[:200]
            article_texts.append(
                f"{i + 1}. Title: \"{a.title}\"\n   Source: {a.source.name if a.source else 'Unknown'}\n   Content: {content_preview}"
            )

        prompt = BATCH_PROMPT_TEMPLATE.format(articles="\n".join(article_texts))

        try:
            results = await llm_client.complete_json(
                prompt=prompt,
                system=SYSTEM_PROMPT,
                model=HAIKU,
                max_tokens=512,
                db=db,
                task="confidence",
            )

            valid_levels = {"confirmed", "interpretation", "rumor"}
            for item in results:
                idx = item.get("id", 0) - 1
                if 0 <= idx < len(needs_scoring):
                    conf = item.get("confidence", "interpretation")
                    needs_scoring[idx].confidence = conf if conf in valid_levels else "interpretation"
                    needs_scoring[idx].status = "scored"

        except Exception as e:
            logger.error(f"Confidence scorer error: {e}")
            for a in needs_scoring:
                a.confidence = "interpretation"
                a.status = "scored"

    await db.commit()
    total = len(auto_confirmed) + len(needs_scoring)
    logger.info(f"Scored {total} articles ({len(auto_confirmed)} auto-confirmed)")
    return total
