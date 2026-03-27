from datetime import datetime
from decimal import Decimal
from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text,
    UniqueConstraint, func
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    url = Column(String(500), nullable=False)
    source_type = Column(String(20), nullable=False, default="rss")
    tier = Column(Integer, nullable=False, default=2)
    trust_score = Column(Numeric(3, 2), default=Decimal("0.70"))
    crawl_interval_minutes = Column(Integer, default=120)
    is_active = Column(Boolean, default=True)
    last_crawled_at = Column(DateTime(timezone=True))
    error_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    articles = relationship("Article", back_populates="source")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    external_id = Column(String(500))
    url = Column(String(1000), nullable=False, unique=True)
    title = Column(String(500), nullable=False)
    raw_content = Column(Text)
    clean_content = Column(Text)
    author = Column(String(200))
    published_at = Column(DateTime(timezone=True))
    crawled_at = Column(DateTime(timezone=True), server_default=func.now())

    status = Column(String(20), default="raw")
    is_ai_relevant = Column(Boolean)

    category = Column(String(50))
    summary = Column(Text)
    generated_headline = Column(String(300))
    confidence = Column(String(20))
    importance_score = Column(Numeric(5, 2), default=Decimal("0"))

    cluster_id = Column(Integer)
    is_cluster_primary = Column(Boolean, default=False)

    word_count = Column(Integer)
    language = Column(String(5), default="en")
    image_url = Column(String(1000))
    content_hash = Column(String(64))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    source = relationship("Source", back_populates="articles", lazy="selectin")


class Digest(Base):
    __tablename__ = "digests"

    id = Column(Integer, primary_key=True)
    digest_date = Column(DateTime, unique=True, nullable=False)
    slug = Column(String(20), nullable=False)
    status = Column(String(20), default="draft")
    editorial_summary = Column(Text)
    editorial_headline = Column(String(300))
    total_articles = Column(Integer, default=0)
    total_sources = Column(Integer, default=0)
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    digest_articles = relationship("DigestArticle", back_populates="digest", cascade="all, delete-orphan", lazy="selectin")


class DigestArticle(Base):
    __tablename__ = "digest_articles"
    __table_args__ = (UniqueConstraint("digest_id", "article_id"),)

    id = Column(Integer, primary_key=True)
    digest_id = Column(Integer, ForeignKey("digests.id", ondelete="CASCADE"))
    article_id = Column(Integer, ForeignKey("articles.id"))
    category = Column(String(50), nullable=False)
    position = Column(Integer, nullable=False)
    is_top_story = Column(Boolean, default=False)

    digest = relationship("Digest", back_populates="digest_articles")
    article = relationship("Article", lazy="selectin")


class LLMUsage(Base):
    __tablename__ = "llm_usage"

    id = Column(Integer, primary_key=True)
    model = Column(String(50), nullable=False)
    task = Column(String(30), nullable=False)
    input_tokens = Column(Integer, nullable=False)
    output_tokens = Column(Integer, nullable=False)
    cost_usd = Column(Numeric(10, 6))
    article_id = Column(Integer, ForeignKey("articles.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CrawlLog(Base):
    __tablename__ = "crawl_logs"

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    status = Column(String(20), nullable=False)
    articles_found = Column(Integer, default=0)
    articles_new = Column(Integer, default=0)
    error_message = Column(Text)
    duration_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
