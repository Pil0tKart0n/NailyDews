# NailyDews - AI Daily Newspaper

Automated AI news aggregator that delivers a curated daily digest of the most important developments in artificial intelligence.

## Features

- Crawls 20+ AI news sources (OpenAI, Anthropic, Google AI, arXiv, TechCrunch, etc.)
- LLM-powered filtering, categorization, and summarization
- Daily digest published at 19:00 CET
- Newspaper-style frontend with 5 sections
- Confidence badges (Confirmed / Analysis / Rumor)
- Every article links to its original source

## Tech Stack

- **Backend:** Python 3.12, FastAPI, APScheduler
- **Frontend:** Next.js 14, Tailwind CSS
- **Database:** PostgreSQL 16 + pgvector
- **Queue:** Redis
- **LLM:** Claude API (Haiku + Sonnet)
- **Deploy:** Docker Compose

## Quick Start

```bash
cp .env.example .env
# Edit .env with your Anthropic API key
docker compose up -d
```

Visit http://localhost:3000

## Architecture

```
RSS/API Sources -> Crawler -> Redis Queue -> LLM Pipeline -> PostgreSQL -> Digest Generator -> Next.js Frontend
```
