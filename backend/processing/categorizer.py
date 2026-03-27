import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Article
from llm.client import llm_client, HAIKU

logger = logging.getLogger(__name__)

CATEGORIES = [
    "top_stories",
    "models_releases",
    "tools_frameworks",
    "research_papers",
    "business_regulation",
]

SYSTEM_PROMPT = """You categorize AI news articles into exactly one category. Respond with ONLY valid JSON.

Categories:
- top_stories: Major breaking news, frontier model launches, industry-shaking announcements
- models_releases: New AI models, version updates, benchmarks, model comparisons
- tools_frameworks: New tools, libraries, frameworks, APIs, developer resources
- research_papers: Academic papers, research findings, theoretical advances
- business_regulation: Funding, acquisitions, partnerships, regulation, policy, EU AI Act"""

BATCH_PROMPT_TEMPLATE = """Categorize each article into exactly one category.

Articles:
{articles}

Respond as JSON array:
[{{"id": 1, "category": "models_releases"}}, ...]"""


async def categorize_articles(db: AsyncSession, batch_size: int = 20) -> int:
    """Categorize filtered articles. Returns count processed."""
    result = await db.execute(
        select(Article)
        .where(Article.status == "filtered")
        .order_by(Article.crawled_at.desc())
        .limit(batch_size)
    )
    articles = list(result.scalars().all())

    if not articles:
        return 0

    article_texts = []
    for i, a in enumerate(articles):
        content_preview = (a.clean_content or a.title)[:200]
        article_texts.append(f"{i + 1}. Title: \"{a.title}\"\n   Content: {content_preview}")

    prompt = BATCH_PROMPT_TEMPLATE.format(articles="\n".join(article_texts))

    try:
        results = await llm_client.complete_json(
            prompt=prompt,
            system=SYSTEM_PROMPT,
            model=HAIKU,
            max_tokens=512,
            db=db,
            task="categorize",
        )

        for item in results:
            idx = item.get("id", 0) - 1
            if 0 <= idx < len(articles):
                category = item.get("category", "")
                if category in CATEGORIES:
                    articles[idx].category = category
                else:
                    articles[idx].category = "tools_frameworks"  # fallback
                articles[idx].status = "categorized"

        await db.commit()
        logger.info(f"Categorized {len(articles)} articles")
        return len(articles)

    except Exception as e:
        logger.error(f"Categorizer error: {e}")
        await db.rollback()
        return 0
