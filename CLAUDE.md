# NailyDews - AI Daily Newspaper

## Project Overview
Automated AI news aggregator that collects, filters, and prioritizes AI news from 20+ sources throughout the day, then publishes a daily digest at 19:00 CET in newspaper style.

## Tech Stack
- **Backend:** Python 3.12, FastAPI, APScheduler, rq (Redis Queue)
- **Frontend:** Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui
- **Database:** PostgreSQL 16 + pgvector
- **Cache/Queue:** Redis 7
- **LLM:** Claude API (Haiku for filtering, Sonnet for summaries)
- **Deploy:** Docker Compose on VPS, Nginx reverse proxy

## Conventions
- Code language: English
- Communication language: German
- Commit messages: English, conventional commits
- Python: type hints, async where possible, ruff for linting
- TypeScript: strict mode, no any types
- All LLM prompts in `backend/prompts/` as .txt files
- Every article MUST have a source URL - never generate facts

## Key Commands
```bash
# Development
docker compose up -d                    # Start all services
docker compose logs -f backend          # Watch backend logs
docker compose exec db psql -U nailydews nailydews  # DB shell

# Deploy
python scripts/deploy.py                # Deploy to VPS
```

## Architecture
Crawler → Normalizer → Redis Queue → LLM Pipeline (Filter→Categorize→Summarize→Cluster→Rank) → Digest Generator → Frontend
