import logging

import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Article

logger = logging.getLogger(__name__)

# Load model once (384-dim embeddings, fast)
_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    dot = np.dot(a, b)
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    return float(dot / norm) if norm > 0 else 0.0


async def cluster_articles(db: AsyncSession, similarity_threshold: float = 0.80) -> int:
    """Cluster similar articles together. Uses simple greedy clustering."""
    # Get articles that need clustering (ranked but no cluster)
    result = await db.execute(
        select(Article)
        .where(Article.status == "ranked", Article.cluster_id.is_(None))
        .order_by(Article.importance_score.desc())
        .limit(200)
    )
    articles = list(result.scalars().all())

    if not articles:
        return 0

    model = get_model()

    # Generate embeddings
    texts = [f"{a.title}. {(a.summary or a.clean_content or '')[:200]}" for a in articles]
    embeddings = model.encode(texts, normalize_embeddings=True)

    # Get next cluster ID
    max_cluster = await db.execute(select(func.max(Article.cluster_id)))
    next_cluster_id = (max_cluster.scalar() or 0) + 1

    # Greedy clustering
    assigned = set()
    clusters_formed = 0

    for i, article in enumerate(articles):
        if i in assigned:
            continue

        # Start new cluster
        cluster_members = [i]
        assigned.add(i)

        for j in range(i + 1, len(articles)):
            if j in assigned:
                continue
            sim = cosine_similarity(embeddings[i], embeddings[j])
            if sim >= similarity_threshold:
                cluster_members.append(j)
                assigned.add(j)

        # Assign cluster IDs
        cluster_id = next_cluster_id
        next_cluster_id += 1

        # First article (highest importance) is primary
        for k, member_idx in enumerate(cluster_members):
            articles[member_idx].cluster_id = cluster_id
            articles[member_idx].is_cluster_primary = (k == 0)

        if len(cluster_members) > 1:
            clusters_formed += 1

    await db.commit()
    logger.info(f"Clustered {len(articles)} articles into groups, {clusters_formed} multi-article clusters")
    return len(articles)
