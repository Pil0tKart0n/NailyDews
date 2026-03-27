import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Article
from llm.client import llm_client, HAIKU

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an AI news relevance filter. Your job is to determine if articles are primarily about artificial intelligence, machine learning, large language models, or closely related AI topics.

Respond with ONLY valid JSON, no other text."""

BATCH_PROMPT_TEMPLATE = """Classify each article as AI-relevant or not. Only mark as relevant if the article is PRIMARILY about AI/ML topics (not just mentions AI in passing).

Articles:
{articles}

Respond as a JSON array:
[{{"id": 1, "relevant": true, "confidence": 0.95}}, ...]"""


async def filter_relevance(db: AsyncSession, batch_size: int = 20) -> int:
    """Filter articles for AI relevance. Returns count of relevant articles."""
    result = await db.execute(
        select(Article)
        .where(Article.status == "raw")
        .order_by(Article.crawled_at.desc())
        .limit(batch_size)
    )
    articles = list(result.scalars().all())

    if not articles:
        return 0

    # Build batch prompt
    article_texts = []
    for i, a in enumerate(articles):
        content_preview = (a.clean_content or a.title)[:300]
        article_texts.append(f"{i + 1}. Title: \"{a.title}\"\n   Content: {content_preview}")

    prompt = BATCH_PROMPT_TEMPLATE.format(articles="\n".join(article_texts))

    try:
        results = await llm_client.complete_json(
            prompt=prompt,
            system=SYSTEM_PROMPT,
            model=HAIKU,
            max_tokens=512,
            db=db,
            task="filter",
        )

        relevant_count = 0
        for item in results:
            idx = item.get("id", 0) - 1
            if 0 <= idx < len(articles):
                is_relevant = item.get("relevant", False)
                articles[idx].is_ai_relevant = is_relevant
                articles[idx].status = "filtered" if is_relevant else "filtered_out"
                if is_relevant:
                    relevant_count += 1

        await db.commit()
        logger.info(f"Filtered {len(articles)} articles, {relevant_count} relevant")
        return relevant_count

    except Exception as e:
        logger.error(f"Relevance filter error: {e}")
        await db.rollback()
        return 0
