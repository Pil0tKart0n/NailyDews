-- Tier 1: Official AI Company Blogs (trust 0.90)
INSERT INTO sources (name, slug, url, source_type, tier, trust_score, crawl_interval_minutes) VALUES
('OpenAI Blog', 'openai-blog', 'https://openai.com/blog/rss.xml', 'rss', 1, 0.90, 120),
('Anthropic Blog', 'anthropic-blog', 'https://www.anthropic.com/feed', 'rss', 1, 0.90, 120),
('Google AI Blog', 'google-ai-blog', 'https://blog.google/technology/ai/rss/', 'rss', 1, 0.90, 120),
('Meta AI Blog', 'meta-ai-blog', 'https://ai.meta.com/blog/rss/', 'rss', 1, 0.90, 120),
('DeepMind Blog', 'deepmind-blog', 'https://deepmind.google/blog/rss.xml', 'rss', 1, 0.90, 120),
('Hugging Face Blog', 'huggingface-blog', 'https://huggingface.co/blog/feed.xml', 'rss', 1, 0.90, 120),
('Microsoft AI Blog', 'microsoft-ai-blog', 'https://blogs.microsoft.com/ai/feed/', 'rss', 1, 0.90, 120);

-- Tier 2: Tech Media (trust 0.80)
INSERT INTO sources (name, slug, url, source_type, tier, trust_score, crawl_interval_minutes) VALUES
('TechCrunch AI', 'techcrunch-ai', 'https://techcrunch.com/category/artificial-intelligence/feed/', 'rss', 2, 0.80, 60),
('The Verge AI', 'theverge-ai', 'https://www.theverge.com/rss/ai-artificial-intelligence/index.xml', 'rss', 2, 0.80, 60),
('Ars Technica AI', 'arstechnica-ai', 'https://feeds.arstechnica.com/arstechnica/technology-lab', 'rss', 2, 0.80, 120),
('VentureBeat AI', 'venturebeat-ai', 'https://venturebeat.com/category/ai/feed/', 'rss', 2, 0.80, 120),
('MIT Technology Review', 'mit-tech-review', 'https://www.technologyreview.com/feed/', 'rss', 2, 0.80, 240);

-- Tier 3: Academic/Technical (trust 0.70)
INSERT INTO sources (name, slug, url, source_type, tier, trust_score, crawl_interval_minutes) VALUES
('arXiv cs.AI', 'arxiv-cs-ai', 'http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=50', 'api', 3, 0.70, 360),
('arXiv cs.LG', 'arxiv-cs-lg', 'http://export.arxiv.org/api/query?search_query=cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=50', 'api', 3, 0.70, 360),
('arXiv cs.CL', 'arxiv-cs-cl', 'http://export.arxiv.org/api/query?search_query=cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=50', 'api', 3, 0.70, 360),
('Papers With Code', 'papers-with-code', 'https://paperswithcode.com/latest', 'rss', 3, 0.70, 360);

-- Tier 4: Community (trust 0.50)
INSERT INTO sources (name, slug, url, source_type, tier, trust_score, crawl_interval_minutes) VALUES
('Hacker News AI', 'hackernews-ai', 'https://hn.algolia.com/api/v1/search?tags=story&query=AI+LLM+GPT+machine+learning', 'api', 4, 0.50, 120),
('The Batch (Andrew Ng)', 'the-batch', 'https://www.deeplearning.ai/the-batch/feed/', 'rss', 4, 0.50, 720),
('Import AI Newsletter', 'import-ai', 'https://importai.substack.com/feed', 'rss', 4, 0.50, 720);
