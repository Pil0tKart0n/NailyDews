import logging
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Article, Digest, DigestArticle
from llm.client import llm_client, SONNET

logger = logging.getLogger(__name__)

CATEGORY_LIMITS = {
    "top_stories": 5,
    "models_releases": 5,
    "tools_frameworks": 5,
    "research_papers": 5,
    "business_regulation": 5,
}

EDITORIAL_SYSTEM = """You are a senior AI news editor writing the daily editorial summary for an AI newspaper called "NailyDews".
Write a concise, engaging 2-paragraph editorial summarizing the most important AI developments of the day.
Focus on what matters and why. Be factual, not speculative. Respond with ONLY valid JSON."""

EDITORIAL_PROMPT = """Write today's editorial summary based on these top stories:

{stories}

Respond as JSON:
{{"headline": "One-line editorial headline", "summary": "Two paragraph editorial summary."}}"""


async def generate_digest(db: AsyncSession, target_date: date | None = None) -> Digest | None:
    """Generate the daily digest. Returns the created Digest or None."""
    if target_date is None:
        target_date = date.today()

    # Check if digest already exists
    existing = await db.execute(
        select(Digest).where(Digest.digest_date == target_date)
    )
    if existing.scalar_one_or_none():
        logger.info(f"Digest for {target_date} already exists")
        return None

    # Get articles from the last 24 hours that are fully processed
    cutoff = datetime.now(timezone.utc) - timedelta(hours=28)  # 28h buffer
    articles_query = (
        select(Article)
        .where(
            and_(
                Article.status == "ranked",
                Article.is_ai_relevant == True,
                Article.is_cluster_primary == True,
                Article.published_at >= cutoff,
            )
        )
        .order_by(Article.importance_score.desc())
    )
    result = await db.execute(articles_query)
    all_articles = list(result.scalars().all())

    if not all_articles:
        logger.warning(f"No articles available for digest on {target_date}")
        return None

    # Select articles per category
    selected = {}
    for category, limit in CATEGORY_LIMITS.items():
        cat_articles = [a for a in all_articles if a.category == category]
        selected[category] = cat_articles[:limit]

    # Also pick overall top stories regardless of category
    top_stories = all_articles[:5]
    for a in top_stories:
        if a not in selected.get("top_stories", []):
            if len(selected.get("top_stories", [])) < 5:
                selected.setdefault("top_stories", []).append(a)

    # Generate editorial
    story_texts = []
    for a in top_stories[:5]:
        story_texts.append(f"- {a.generated_headline or a.title}: {a.summary or ''}")

    editorial_headline = f"AI Daily Digest - {target_date.strftime('%B %d, %Y')}"
    editorial_summary = ""

    if story_texts:
        try:
            prompt = EDITORIAL_PROMPT.format(stories="\n".join(story_texts))
            data = await llm_client.complete_json(
                prompt=prompt,
                system=EDITORIAL_SYSTEM,
                model=SONNET,
                max_tokens=512,
                db=db,
                task="editorial",
            )
            editorial_headline = data.get("headline", editorial_headline)
            editorial_summary = data.get("summary", "")
        except Exception as e:
            logger.error(f"Editorial generation error: {e}")

    # Create digest
    total_articles = sum(len(arts) for arts in selected.values())
    source_ids = set()
    for arts in selected.values():
        for a in arts:
            if a.source_id:
                source_ids.add(a.source_id)

    digest = Digest(
        digest_date=target_date,
        slug=target_date.isoformat(),
        status="published",
        editorial_headline=editorial_headline,
        editorial_summary=editorial_summary,
        total_articles=total_articles,
        total_sources=len(source_ids),
        published_at=datetime.now(timezone.utc),
    )
    db.add(digest)
    await db.flush()

    # Create digest_articles entries
    for category, arts in selected.items():
        for position, article in enumerate(arts):
            is_top = article in top_stories
            da = DigestArticle(
                digest_id=digest.id,
                article_id=article.id,
                category=category,
                position=position,
                is_top_story=is_top,
            )
            db.add(da)

    await db.commit()
    logger.info(f"Generated digest for {target_date}: {total_articles} articles from {len(source_ids)} sources")
    return digest
