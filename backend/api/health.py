from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import get_db
from db.models import Article, Digest, Source, LLMUsage

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint."""
    try:
        await db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    return {
        "status": "healthy" if db_ok else "degraded",
        "database": "connected" if db_ok else "disconnected",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/api/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Get system stats."""
    sources_count = (await db.execute(select(func.count(Source.id)).where(Source.is_active == True))).scalar()
    articles_count = (await db.execute(select(func.count(Article.id)))).scalar()
    digests_count = (await db.execute(select(func.count(Digest.id)).where(Digest.status == "published"))).scalar()

    # Today's LLM costs
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    today_cost = (await db.execute(
        select(func.sum(LLMUsage.cost_usd)).where(LLMUsage.created_at >= today_start)
    )).scalar() or 0

    return {
        "active_sources": sources_count,
        "total_articles": articles_count,
        "published_digests": digests_count,
        "today_llm_cost_usd": float(today_cost),
    }
