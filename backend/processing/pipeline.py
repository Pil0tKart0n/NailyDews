import logging

from sqlalchemy.ext.asyncio import AsyncSession

from processing.relevance_filter import filter_relevance
from processing.categorizer import categorize_articles
from processing.summarizer import summarize_articles
from processing.confidence_scorer import score_confidence
from processing.ranker import rank_articles
from processing.clusterer import cluster_articles

logger = logging.getLogger(__name__)


async def run_pipeline(db: AsyncSession) -> dict:
    """Run the full article processing pipeline. Returns stats."""
    stats = {}

    logger.info("Pipeline: Starting relevance filter...")
    stats["filtered"] = await filter_relevance(db, batch_size=50)

    logger.info("Pipeline: Categorizing articles...")
    stats["categorized"] = await categorize_articles(db, batch_size=50)

    logger.info("Pipeline: Summarizing articles...")
    stats["summarized"] = await summarize_articles(db, batch_size=20)

    logger.info("Pipeline: Scoring confidence...")
    stats["scored"] = await score_confidence(db, batch_size=50)

    logger.info("Pipeline: Ranking articles...")
    stats["ranked"] = await rank_articles(db, batch_size=100)

    logger.info("Pipeline: Clustering articles...")
    stats["clustered"] = await cluster_articles(db)

    logger.info(f"Pipeline complete: {stats}")
    return stats
