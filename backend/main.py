import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.digests import router as digests_router
from api.health import router as health_router
from config import settings
from scheduler.jobs import job_crawl, job_process, job_digest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start scheduler on app startup, stop on shutdown."""
    # Crawl every 30 minutes
    scheduler.add_job(job_crawl, IntervalTrigger(minutes=30), id="crawl", replace_existing=True)

    # Process every 15 minutes
    scheduler.add_job(job_process, IntervalTrigger(minutes=15), id="process", replace_existing=True)

    # Generate digest at configured time (default 19:00 CET)
    hour, minute = settings.digest_time.split(":")
    scheduler.add_job(
        job_digest,
        CronTrigger(hour=int(hour), minute=int(minute), timezone=settings.digest_timezone),
        id="digest",
        replace_existing=True,
    )

    scheduler.start()
    logger.info(f"Scheduler started: crawl=30min, process=15min, digest={settings.digest_time} {settings.digest_timezone}")

    yield

    scheduler.shutdown()
    logger.info("Scheduler stopped")


app = FastAPI(
    title="NailyDews API",
    description="AI Daily Newspaper - Backend API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restricted by Nginx in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health_router)
app.include_router(digests_router)


@app.get("/")
async def root():
    return {"name": "NailyDews API", "version": "1.0.0", "status": "running"}
