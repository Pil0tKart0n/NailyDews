from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import get_db
from db.models import Article, Digest, DigestArticle

router = APIRouter(prefix="/api/digests", tags=["digests"])


def serialize_article(article: Article, da: DigestArticle) -> dict:
    return {
        "id": article.id,
        "headline": article.generated_headline or article.title,
        "original_title": article.title,
        "summary": article.summary or "",
        "source_name": article.source.name if article.source else "Unknown",
        "source_url": article.url,
        "confidence": article.confidence or "interpretation",
        "importance_score": float(article.importance_score) if article.importance_score else 0,
        "published_at": article.published_at.isoformat() if article.published_at else None,
        "category": da.category,
        "is_top_story": da.is_top_story,
        "image_url": article.image_url,
        "author": article.author,
    }


def serialize_digest(digest: Digest, articles_by_category: dict) -> dict:
    CATEGORY_LABELS = {
        "top_stories": "Top Stories",
        "models_releases": "Models & Releases",
        "tools_frameworks": "Tools & Frameworks",
        "research_papers": "Research & Papers",
        "business_regulation": "Business & Regulation",
    }

    sections = []
    for cat_key in ["top_stories", "models_releases", "tools_frameworks", "research_papers", "business_regulation"]:
        items = articles_by_category.get(cat_key, [])
        if items:
            sections.append({
                "category": cat_key,
                "label": CATEGORY_LABELS.get(cat_key, cat_key),
                "articles": items,
            })

    return {
        "date": digest.digest_date.isoformat() if hasattr(digest.digest_date, "isoformat") else str(digest.digest_date),
        "slug": digest.slug,
        "editorial_headline": digest.editorial_headline or "",
        "editorial_summary": digest.editorial_summary or "",
        "total_articles": digest.total_articles or 0,
        "total_sources": digest.total_sources or 0,
        "published_at": digest.published_at.isoformat() if digest.published_at else None,
        "sections": sections,
    }


async def _load_digest(digest: Digest, db: AsyncSession) -> dict:
    """Load a digest with all its articles grouped by category."""
    result = await db.execute(
        select(DigestArticle, Article)
        .join(Article, DigestArticle.article_id == Article.id)
        .where(DigestArticle.digest_id == digest.id)
        .order_by(DigestArticle.category, DigestArticle.position)
    )
    rows = result.all()

    articles_by_category = {}
    for da, article in rows:
        serialized = serialize_article(article, da)
        articles_by_category.setdefault(da.category, []).append(serialized)

    return serialize_digest(digest, articles_by_category)


@router.get("")
async def list_digests(limit: int = 30, db: AsyncSession = Depends(get_db)):
    """List recent digests (metadata only)."""
    result = await db.execute(
        select(Digest)
        .where(Digest.status == "published")
        .order_by(Digest.digest_date.desc())
        .limit(limit)
    )
    digests = result.scalars().all()

    return {
        "data": [
            {
                "date": d.digest_date.isoformat() if hasattr(d.digest_date, "isoformat") else str(d.digest_date),
                "slug": d.slug,
                "editorial_headline": d.editorial_headline or "",
                "total_articles": d.total_articles or 0,
                "published_at": d.published_at.isoformat() if d.published_at else None,
            }
            for d in digests
        ]
    }


@router.get("/today")
async def get_today_digest(db: AsyncSession = Depends(get_db)):
    """Get today's digest (or latest available)."""
    result = await db.execute(
        select(Digest)
        .where(Digest.status == "published")
        .order_by(Digest.digest_date.desc())
        .limit(1)
    )
    digest = result.scalar_one_or_none()

    if not digest:
        raise HTTPException(status_code=404, detail="No digest available yet")

    return {"data": await _load_digest(digest, db)}


@router.get("/{digest_date}")
async def get_digest_by_date(digest_date: str, db: AsyncSession = Depends(get_db)):
    """Get digest for a specific date (YYYY-MM-DD)."""
    try:
        target = date.fromisoformat(digest_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    result = await db.execute(
        select(Digest).where(Digest.digest_date == target, Digest.status == "published")
    )
    digest = result.scalar_one_or_none()

    if not digest:
        raise HTTPException(status_code=404, detail=f"No digest for {digest_date}")

    return {"data": await _load_digest(digest, db)}
