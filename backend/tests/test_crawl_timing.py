#!/usr/bin/env python3
"""
Timing test for all crawlers/scrapers.
Measures how long each source takes to fetch, how many articles it returns,
and whether the source is reachable at all.

Run standalone: python -m tests.test_crawl_timing
No database needed - this test only measures network fetch performance.
"""

import asyncio
import time
import sys
from dataclasses import dataclass

import httpx

# Test sources: (name, url, type, method)
TEST_SOURCES = [
    # === TIER 1: Official Blogs (RSS) ===
    ("OpenAI Blog", "https://openai.com/blog/rss.xml", "rss"),
    ("Anthropic Blog (community RSS)", "https://raw.githubusercontent.com/taobojlen/anthropic-rss-feed/main/anthropic_news_rss.xml", "rss"),
    ("Google AI Blog", "https://blog.google/technology/ai/rss/", "rss"),
    ("Meta AI Blog (scraper)", "https://ai.meta.com/blog/", "scraper"),
    ("DeepMind Blog", "https://deepmind.google/blog/rss.xml", "rss"),
    ("Hugging Face Blog", "https://huggingface.co/blog/feed.xml", "rss"),
    ("HF Daily Papers (community)", "https://raw.githubusercontent.com/huangboming/huggingface-daily-paper-feed/refs/heads/main/feed.xml", "rss"),
    ("Microsoft AI Blog", "https://blogs.microsoft.com/ai/feed/", "rss"),
    ("Mistral AI (community RSS)", "https://raw.githubusercontent.com/0xSMW/rss-feeds/main/feeds/feed_mistral_news.xml", "rss"),
    ("Nvidia AI Blog", "https://blogs.nvidia.com/feed/", "rss"),
    ("Cohere Blog", "https://cohere.com/blog/rss.xml", "rss"),
    ("Stability AI (scraper)", "https://stability.ai/blog", "scraper"),
    ("Together AI Blog", "https://www.together.ai/blog/rss.xml", "rss"),
    ("Replicate Blog", "https://replicate.com/blog/rss", "rss"),

    # === TIER 2: Tech Media (RSS) ===
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/", "rss"),
    ("The Verge AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "rss"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/technology-lab", "rss"),
    ("VentureBeat AI", "https://venturebeat.com/category/ai/feed/", "rss"),
    ("MIT Technology Review", "https://www.technologyreview.com/feed/", "rss"),
    ("Wired AI", "https://www.wired.com/feed/tag/ai/latest/rss", "rss"),

    # === TIER 2.5: Expert Blogs (RSS) ===
    ("Simon Willison", "https://simonwillison.net/atom/everything/", "rss"),
    ("Chip Huyen", "https://huyenchip.com/feed.xml", "rss"),
    ("Lilian Weng", "https://lilianweng.github.io/index.xml", "rss"),
    ("The Gradient", "https://thegradient.pub/rss/", "rss"),
    ("LangChain Blog", "https://blog.langchain.dev/rss/", "rss"),
    ("W&B Blog", "https://wandb.ai/fully-connected/rss.xml", "rss"),
    ("Towards Data Science", "https://towardsdatascience.com/feed", "rss"),

    # === TIER 3: Academic/Research (API) ===
    ("arXiv cs.AI", "http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=50", "api"),
    ("arXiv cs.LG", "http://export.arxiv.org/api/query?search_query=cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=50", "api"),
    ("arXiv cs.CL", "http://export.arxiv.org/api/query?search_query=cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=50", "api"),

    # === TIER 3.5: AI Safety (RSS) ===
    ("LessWrong", "https://www.lesswrong.com/feed.xml?view=curated", "rss"),
    ("AI Alignment Forum", "https://www.alignmentforum.org/feed.xml?view=curated", "rss"),
    ("LMSYS Blog (scraper)", "https://lmsys.org/blog/", "scraper"),
    ("EleutherAI Blog", "https://blog.eleuther.ai/index.xml", "rss"),

    # === TIER 4: Reddit (JSON API) ===
    ("Reddit r/MachineLearning", "https://www.reddit.com/r/MachineLearning/hot.json?limit=25", "reddit"),
    ("Reddit r/LocalLLaMA", "https://www.reddit.com/r/LocalLLaMA/hot.json?limit=25", "reddit"),
    ("Reddit r/artificial", "https://www.reddit.com/r/artificial/hot.json?limit=25", "reddit"),
    ("Reddit r/ChatGPT", "https://www.reddit.com/r/ChatGPT/hot.json?limit=25", "reddit"),
    ("Reddit r/OpenAI", "https://www.reddit.com/r/OpenAI/hot.json?limit=25", "reddit"),
    ("Reddit r/ClaudeAI", "https://www.reddit.com/r/ClaudeAI/hot.json?limit=25", "reddit"),
    ("Reddit r/singularity", "https://www.reddit.com/r/singularity/hot.json?limit=25", "reddit"),
    ("Reddit r/LLMDevs", "https://www.reddit.com/r/LLMDevs/hot.json?limit=20", "reddit"),
    ("Reddit r/mlops", "https://www.reddit.com/r/mlops/hot.json?limit=20", "reddit"),

    # === TIER 4: Hacker News (API) ===
    ("HN AI", "https://hn.algolia.com/api/v1/search?tags=story&query=AI+LLM+GPT+machine+learning&hitsPerPage=30", "api"),
    ("HN Agents", "https://hn.algolia.com/api/v1/search?tags=story&query=AI+agent+autonomous&hitsPerPage=20", "api"),

    # === TIER 4: Newsletters (RSS) ===
    ("The Batch (scraper)", "https://www.deeplearning.ai/the-batch/", "scraper"),
    ("Import AI", "https://importai.substack.com/feed", "rss"),
    ("Interconnects", "https://www.interconnects.ai/feed", "rss"),
    ("One Useful Thing", "https://www.oneusefulthing.org/feed", "rss"),
    ("Ahead of AI", "https://magazine.sebastianraschka.com/feed", "rss"),
    ("Latent Space", "https://www.latent.space/feed", "rss"),
    ("Algorithmic Bridge", "https://thealgorithmicbridge.substack.com/feed", "rss"),

    # === GitHub API ===
    ("GitHub Trending AI", "https://api.github.com/search/repositories?q=topic:machine-learning+created:>2026-03-20+stars:>10&sort=stars&order=desc&per_page=30", "api"),
]


@dataclass
class TestResult:
    name: str
    url: str
    source_type: str
    status: str  # "ok", "error", "timeout"
    http_status: int
    duration_ms: int
    response_size_kb: float
    items_found: int
    error: str


async def test_source(client: httpx.AsyncClient, name: str, url: str, source_type: str) -> TestResult:
    """Test a single source and measure timing."""
    start = time.monotonic()

    headers = {"User-Agent": "NailyDews/1.0 (AI News Aggregator; Timing Test)"}
    if "reddit.com" in url:
        headers["User-Agent"] = "NailyDews/1.0 (AI News Aggregator; contact@nailydews.com)"

    try:
        response = await client.get(url, headers=headers, timeout=30.0)
        duration_ms = int((time.monotonic() - start) * 1000)

        body = response.text
        size_kb = len(body.encode()) / 1024

        # Count items based on type
        items = 0
        if source_type == "rss":
            items = body.count("<item>") + body.count("<entry>")
        elif source_type == "reddit":
            import json
            try:
                data = json.loads(body)
                items = len(data.get("data", {}).get("children", []))
            except Exception:
                items = 0
        elif source_type == "api":
            if "arxiv" in url:
                items = body.count("<entry>")
            elif "algolia" in url or "github" in url:
                import json
                try:
                    data = json.loads(body)
                    items = len(data.get("hits", data.get("items", [])))
                except Exception:
                    items = 0

        return TestResult(
            name=name,
            url=url,
            source_type=source_type,
            status="ok" if response.status_code < 400 else "error",
            http_status=response.status_code,
            duration_ms=duration_ms,
            response_size_kb=round(size_kb, 1),
            items_found=items,
            error="" if response.status_code < 400 else f"HTTP {response.status_code}",
        )

    except httpx.TimeoutException:
        duration_ms = int((time.monotonic() - start) * 1000)
        return TestResult(
            name=name, url=url, source_type=source_type,
            status="timeout", http_status=0, duration_ms=duration_ms,
            response_size_kb=0, items_found=0, error="Timeout (30s)",
        )
    except Exception as e:
        duration_ms = int((time.monotonic() - start) * 1000)
        return TestResult(
            name=name, url=url, source_type=source_type,
            status="error", http_status=0, duration_ms=duration_ms,
            response_size_kb=0, items_found=0, error=str(e)[:100],
        )


async def run_all_tests():
    """Run timing tests for all sources."""
    print("=" * 100)
    print("NailyDews Crawler Timing Test")
    print(f"Testing {len(TEST_SOURCES)} sources...")
    print("=" * 100)
    print()

    client = httpx.AsyncClient(follow_redirects=True)

    results: list[TestResult] = []

    # Run tests in batches of 5 to avoid overwhelming
    batch_size = 5
    for i in range(0, len(TEST_SOURCES), batch_size):
        batch = TEST_SOURCES[i:i + batch_size]
        tasks = [test_source(client, name, url, stype) for name, url, stype in batch]
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)

        # Small delay between batches to be polite
        if i + batch_size < len(TEST_SOURCES):
            await asyncio.sleep(1)

    await client.aclose()

    # Print results table
    print(f"{'Source':<35} {'Type':<8} {'Status':<8} {'HTTP':<6} {'Time':<8} {'Size':<8} {'Items':<6} {'Error'}")
    print("-" * 120)

    total_time = 0
    ok_count = 0
    error_count = 0
    timeout_count = 0

    for r in results:
        status_icon = "OK" if r.status == "ok" else ("TIMEOUT" if r.status == "timeout" else "ERROR")
        error_short = r.error[:40] if r.error else ""

        print(
            f"{r.name:<35} {r.source_type:<8} {status_icon:<8} {r.http_status:<6} "
            f"{r.duration_ms:>5}ms  {r.response_size_kb:>6.1f}kb {r.items_found:>5}  {error_short}"
        )

        total_time += r.duration_ms
        if r.status == "ok":
            ok_count += 1
        elif r.status == "timeout":
            timeout_count += 1
        else:
            error_count += 1

    # Summary
    print()
    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print(f"Total sources tested: {len(results)}")
    print(f"  OK:      {ok_count}")
    print(f"  Errors:  {error_count}")
    print(f"  Timeout: {timeout_count}")
    print()
    print(f"Total fetch time (sequential): {total_time}ms ({total_time/1000:.1f}s)")
    print(f"Average per source: {total_time // len(results)}ms")
    print()

    # Timing analysis
    ok_results = [r for r in results if r.status == "ok"]
    if ok_results:
        sorted_by_time = sorted(ok_results, key=lambda r: r.duration_ms, reverse=True)
        print("SLOWEST 10 SOURCES:")
        for r in sorted_by_time[:10]:
            print(f"  {r.duration_ms:>5}ms  {r.name} ({r.response_size_kb}kb, {r.items_found} items)")

        print()
        print("FASTEST 10 SOURCES:")
        for r in sorted(ok_results, key=lambda r: r.duration_ms)[:10]:
            print(f"  {r.duration_ms:>5}ms  {r.name} ({r.response_size_kb}kb, {r.items_found} items)")

    # Recommended intervals
    print()
    print("=" * 100)
    print("RECOMMENDED INTERVALS (based on response time + items)")
    print("=" * 100)
    for r in sorted(ok_results, key=lambda r: r.name):
        if r.duration_ms < 2000:
            interval = "30-60 min"
        elif r.duration_ms < 5000:
            interval = "60-120 min"
        elif r.duration_ms < 10000:
            interval = "120-240 min"
        else:
            interval = "240-720 min"
        print(f"  {r.name:<35} {r.duration_ms:>5}ms -> {interval}")

    # Sources that need attention
    problem_sources = [r for r in results if r.status != "ok"]
    if problem_sources:
        print()
        print("=" * 100)
        print("SOURCES THAT NEED ATTENTION:")
        print("=" * 100)
        for r in problem_sources:
            print(f"  {r.name}: {r.error}")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
