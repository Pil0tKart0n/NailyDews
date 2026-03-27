-- Enable extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Sources: where we crawl from
CREATE TABLE sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    url VARCHAR(500) NOT NULL,
    source_type VARCHAR(20) NOT NULL DEFAULT 'rss',
    tier INTEGER NOT NULL DEFAULT 2,
    trust_score DECIMAL(3,2) DEFAULT 0.70,
    crawl_interval_minutes INTEGER DEFAULT 120,
    is_active BOOLEAN DEFAULT true,
    last_crawled_at TIMESTAMPTZ,
    error_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Articles
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES sources(id),
    external_id VARCHAR(500),
    url VARCHAR(1000) NOT NULL UNIQUE,
    title VARCHAR(500) NOT NULL,
    raw_content TEXT,
    clean_content TEXT,
    author VARCHAR(200),
    published_at TIMESTAMPTZ,
    crawled_at TIMESTAMPTZ DEFAULT NOW(),

    -- Processing status: raw -> normalized -> filtered -> processed -> ranked
    status VARCHAR(20) DEFAULT 'raw',
    is_ai_relevant BOOLEAN,

    -- LLM-generated fields
    category VARCHAR(50),
    summary TEXT,
    generated_headline VARCHAR(300),
    confidence VARCHAR(20),
    importance_score DECIMAL(5,2) DEFAULT 0,

    -- Clustering
    cluster_id INTEGER,
    embedding vector(384),
    is_cluster_primary BOOLEAN DEFAULT false,

    -- Metadata
    word_count INTEGER,
    language VARCHAR(5) DEFAULT 'en',
    image_url VARCHAR(1000),
    content_hash VARCHAR(64),

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_articles_status ON articles(status);
CREATE INDEX idx_articles_published ON articles(published_at DESC);
CREATE INDEX idx_articles_category ON articles(category);
CREATE INDEX idx_articles_cluster ON articles(cluster_id);
CREATE INDEX idx_articles_hash ON articles(content_hash);
CREATE INDEX idx_articles_url ON articles(url);

-- Daily digests
CREATE TABLE digests (
    id SERIAL PRIMARY KEY,
    digest_date DATE UNIQUE NOT NULL,
    slug VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',
    editorial_summary TEXT,
    editorial_headline VARCHAR(300),
    total_articles INTEGER DEFAULT 0,
    total_sources INTEGER DEFAULT 0,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Digest <-> Article junction
CREATE TABLE digest_articles (
    id SERIAL PRIMARY KEY,
    digest_id INTEGER REFERENCES digests(id) ON DELETE CASCADE,
    article_id INTEGER REFERENCES articles(id),
    category VARCHAR(50) NOT NULL,
    position INTEGER NOT NULL,
    is_top_story BOOLEAN DEFAULT false,
    UNIQUE(digest_id, article_id)
);

-- Users (extended feature)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    preferred_language VARCHAR(5) DEFAULT 'en',
    preferences JSONB DEFAULT '{
        "categories": ["top_stories", "models_releases", "tools_frameworks", "research_papers", "business_regulation"],
        "boost_keywords": [],
        "mute_keywords": [],
        "email_digest": false
    }'::jsonb,
    email_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_login_at TIMESTAMPTZ,
    consent_given_at TIMESTAMPTZ,
    data_deletion_requested_at TIMESTAMPTZ
);

-- LLM usage tracking
CREATE TABLE llm_usage (
    id SERIAL PRIMARY KEY,
    model VARCHAR(50) NOT NULL,
    task VARCHAR(30) NOT NULL,
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    cost_usd DECIMAL(10,6),
    article_id INTEGER REFERENCES articles(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_llm_usage_date ON llm_usage(created_at);

-- Crawl logs
CREATE TABLE crawl_logs (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES sources(id),
    status VARCHAR(20) NOT NULL,
    articles_found INTEGER DEFAULT 0,
    articles_new INTEGER DEFAULT 0,
    error_message TEXT,
    duration_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
