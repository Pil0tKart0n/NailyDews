import logging
import math
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Article

logger = logging.getLogger(__name__)

IMPACT_KEYWORDS = {"launch", "release", "announce", "breakthrough", "introduces", "unveils", "open-source"}
PENALTY_KEYWORDS = {"reportedly", "rumored", "sources say", "allegedly", "unconfirmed"}


async def rank_articles(db: AsyncSession, batch_size: int = 100) -> int:
    """Calculate importance scores for scored articles."""
    result = await db.execute(
        select(Article)
        .where(Article.status == "scored")
        .order_by(Article.crawled_at.desc())
        .limit(batch_size)
    )
    articles = list(result.scalars().all())

    if not articles:
        return 0

    now = datetime.now(timezone.utc)

    # Pre-fetch all cluster counts in one query (avoid N+1)
    cluster_ids = {a.cluster_id for a in articles if a.cluster_id}
    cluster_counts: dict[int, int] = {}
    if cluster_ids:
        counts_result = await db.execute(
            select(Article.cluster_id, func.count(Article.id))
            .where(Article.cluster_id.in_(cluster_ids))
            .group_by(Article.cluster_id)
        )
        for cid, cnt in counts_result:
            cluster_counts[cid] = cnt

    for article in articles:
        score = 0.0

        # Source trust (0-30 points)
        trust = float(article.source.trust_score) if article.source else 0.5
        score += trust * 30

        # Recency (0-20 points) - exponential decay over 24h
        if article.published_at:
            hours_old = (now - article.published_at).total_seconds() / 3600
            hours_old = max(0, hours_old)
        else:
            hours_old = 24  # Unknown age = assume old
        score += max(0, 20 * math.exp(-hours_old / 12))

        # Category boost (0-10 points)
        if article.category == "top_stories":
            score += 10

        # Cluster size (0-15 points) - more sources = bigger story
        if article.cluster_id:
            cluster_count = cluster_counts.get(article.cluster_id, 1)
            score += min(15, cluster_count * 3)

        # Content signals (0-15 points)
        title_lower = article.title.lower()
        if any(kw in title_lower for kw in IMPACT_KEYWORDS):
            score += 5
        if article.source and article.source.tier == 1:
            score += 5
        if article.confidence == "confirmed":
            score += 5

        # Penalty for rumors
        if article.confidence == "rumor":
            score -= 5
        if any(kw in title_lower for kw in PENALTY_KEYWORDS):
            score -= 3

        # Freshness tie-breaker (0-10 points)
        score += max(0, min(10, 10 * (1 - hours_old / 24)))

        article.importance_score = Decimal(str(round(min(100, max(0, score)), 2)))
        article.status = "ranked"

    await db.commit()
    logger.info(f"Ranked {len(articles)} articles")
    return len(articles)
