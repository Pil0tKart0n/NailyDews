-- ============================================================
-- TIER 1: Official AI Company Blogs (trust 0.90)
-- These are primary sources - announcements come from here first
-- ============================================================
INSERT INTO sources (name, slug, url, source_type, tier, trust_score, crawl_interval_minutes) VALUES
('OpenAI Blog', 'openai-blog', 'https://openai.com/blog/rss.xml', 'rss', 1, 0.90, 120),
('Anthropic Blog', 'anthropic-blog', 'https://raw.githubusercontent.com/taobojlen/anthropic-rss-feed/main/anthropic_news_rss.xml', 'rss', 1, 0.90, 120),
('Google AI Blog', 'google-ai-blog', 'https://blog.google/technology/ai/rss/', 'rss', 1, 0.90, 120),
('Meta AI Blog', 'meta-ai-blog', 'https://ai.meta.com/blog/', 'scraper', 1, 0.90, 240),
('DeepMind Blog', 'deepmind-blog', 'https://deepmind.google/blog/rss.xml', 'rss', 1, 0.90, 120),
('Hugging Face Blog', 'huggingface-blog', 'https://huggingface.co/blog/feed.xml', 'rss', 1, 0.90, 120),
('HF Daily Papers', 'hf-daily-papers', 'https://raw.githubusercontent.com/huangboming/huggingface-daily-paper-feed/refs/heads/main/feed.xml', 'rss', 1, 0.85, 240),
('Microsoft AI Blog', 'microsoft-ai-blog', 'https://blogs.microsoft.com/ai/feed/', 'rss', 1, 0.90, 120),
('Mistral AI Blog', 'mistral-blog', 'https://raw.githubusercontent.com/0xSMW/rss-feeds/main/feeds/feed_mistral_news.xml', 'rss', 1, 0.90, 180),
('Nvidia AI Blog', 'nvidia-ai-blog', 'https://blogs.nvidia.com/feed/', 'rss', 1, 0.90, 120),
('Cohere Blog', 'cohere-blog', 'https://cohere.com/blog/rss.xml', 'rss', 1, 0.90, 180),
('Stability AI Blog', 'stability-ai-blog', 'https://stability.ai/news', 'scraper', 1, 0.90, 360),
('Together AI Blog', 'together-ai-blog', 'https://www.together.ai/blog/rss.xml', 'rss', 1, 0.90, 180),
('Replicate Blog', 'replicate-blog', 'https://replicate.com/blog/rss', 'rss', 1, 0.90, 240),
('AI21 Labs Blog', 'ai21-blog', 'https://www.ai21.com/blog/rss.xml', 'rss', 1, 0.90, 240);

-- ============================================================
-- TIER 2: Tech Media & Established Journalists (trust 0.80)
-- Professional journalism with editorial standards
-- ============================================================
INSERT INTO sources (name, slug, url, source_type, tier, trust_score, crawl_interval_minutes) VALUES
('TechCrunch AI', 'techcrunch-ai', 'https://techcrunch.com/category/artificial-intelligence/feed/', 'rss', 2, 0.80, 60),
('The Verge AI', 'theverge-ai', 'https://www.theverge.com/rss/ai-artificial-intelligence/index.xml', 'rss', 2, 0.80, 60),
('Ars Technica', 'arstechnica-ai', 'https://feeds.arstechnica.com/arstechnica/technology-lab', 'rss', 2, 0.80, 120),
('VentureBeat AI', 'venturebeat-ai', 'https://venturebeat.com/category/ai/feed/', 'rss', 2, 0.80, 120),
('MIT Technology Review', 'mit-tech-review', 'https://www.technologyreview.com/feed/', 'rss', 2, 0.80, 240),
('Wired AI', 'wired-ai', 'https://www.wired.com/feed/tag/ai/latest/rss', 'rss', 2, 0.80, 120),
('The Information', 'the-information', 'https://www.theinformation.com/feed', 'rss', 2, 0.80, 240),
('Bloomberg AI', 'bloomberg-ai', 'https://feeds.bloomberg.com/technology/news.rss', 'rss', 2, 0.80, 120),
('Reuters Tech', 'reuters-tech', 'https://www.reuters.com/technology/rss', 'rss', 2, 0.80, 120),
('Semafor Tech', 'semafor-tech', 'https://www.semafor.com/vertical/technology/rss', 'rss', 2, 0.80, 180);

-- ============================================================
-- TIER 2.5: Expert Blogs & Developer-Focused Media (trust 0.75)
-- Written by recognized experts in the field
-- ============================================================
INSERT INTO sources (name, slug, url, source_type, tier, trust_score, crawl_interval_minutes) VALUES
('Simon Willison Blog', 'simonwillison', 'https://simonwillison.net/atom/everything/', 'rss', 2, 0.85, 120),
('Chip Huyen Blog', 'chip-huyen', 'https://huyenchip.com/feed.xml', 'rss', 2, 0.80, 360),
('Lilian Weng Blog', 'lilian-weng', 'https://lilianweng.github.io/index.xml', 'rss', 2, 0.85, 360),
('Jay Alammar Blog', 'jay-alammar', 'https://jalammar.github.io/feed.xml', 'rss', 2, 0.80, 360),
('Sebastian Raschka Blog', 'sebastian-raschka', 'https://sebastianraschka.com/rss_feed.xml', 'rss', 2, 0.80, 360),
('Andrej Karpathy Blog', 'karpathy-blog', 'https://karpathy.github.io/feed.xml', 'rss', 2, 0.85, 360),
('Eugene Yan Blog', 'eugene-yan', 'https://eugeneyan.com/rss/', 'rss', 2, 0.75, 360),
('Weights & Biases Blog', 'wandb-blog', 'https://wandb.ai/fully-connected/rss.xml', 'rss', 2, 0.75, 240),
('LangChain Blog', 'langchain-blog', 'https://blog.langchain.dev/rss/', 'rss', 2, 0.75, 180),
('LlamaIndex Blog', 'llamaindex-blog', 'https://www.llamaindex.ai/blog/rss', 'rss', 2, 0.75, 240),
('Towards Data Science', 'towards-ds', 'https://towardsdatascience.com/feed', 'rss', 2, 0.70, 120),
('The Gradient', 'the-gradient', 'https://thegradient.pub/rss/', 'rss', 2, 0.80, 360),
('Distill.pub', 'distill', 'https://distill.pub/rss.xml', 'rss', 2, 0.85, 720);

-- ============================================================
-- TIER 3: Academic & Research (trust 0.70)
-- Papers, preprints, research discussions
-- ============================================================
INSERT INTO sources (name, slug, url, source_type, tier, trust_score, crawl_interval_minutes) VALUES
('arXiv cs.AI', 'arxiv-cs-ai', 'http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=50', 'api', 3, 0.70, 360),
('arXiv cs.LG', 'arxiv-cs-lg', 'http://export.arxiv.org/api/query?search_query=cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=50', 'api', 3, 0.70, 720),
('arXiv cs.CL', 'arxiv-cs-cl', 'http://export.arxiv.org/api/query?search_query=cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=50', 'api', 3, 0.70, 720),
('arXiv cs.CV', 'arxiv-cs-cv', 'http://export.arxiv.org/api/query?search_query=cat:cs.CV&sortBy=submittedDate&sortOrder=descending&max_results=30', 'api', 3, 0.70, 720),
('Papers With Code', 'papers-with-code', 'https://paperswithcode.com/latest', 'rss', 3, 0.70, 360),
('Semantic Scholar AI', 'semantic-scholar', 'https://api.semanticscholar.org/graph/v1/paper/search?query=large+language+model&year=2026&limit=20&fields=title,url,abstract,publicationDate,authors', 'api', 3, 0.70, 720),
('GitHub Trending AI', 'github-trending', 'https://api.github.com/search/repositories?q=topic:machine-learning+created:>2026-03-20+stars:>10&sort=stars&order=desc&per_page=30', 'api', 3, 0.70, 360);

-- ============================================================
-- TIER 3.5: AI Safety & Alignment Community (trust 0.65)
-- Where the deep thinkers and alignment researchers hang out
-- ============================================================
INSERT INTO sources (name, slug, url, source_type, tier, trust_score, crawl_interval_minutes) VALUES
('LessWrong AI', 'lesswrong', 'https://www.lesswrong.com/feed.xml?view=curated', 'rss', 3, 0.75, 240),
('AI Alignment Forum', 'ai-alignment-forum', 'https://www.alignmentforum.org/feed.xml?view=curated', 'rss', 3, 0.80, 360),
('LMSYS Org Blog', 'lmsys', 'https://lmsys.org/blog/', 'scraper', 3, 0.80, 720),
('EleutherAI Blog', 'eleutherai', 'https://blog.eleuther.ai/index.xml', 'rss', 3, 0.75, 360),
('MIRI Blog', 'miri', 'https://intelligence.org/feed/', 'rss', 3, 0.75, 720);

-- ============================================================
-- TIER 4: Reddit Communities (trust 0.55)
-- Where ML engineers and AI enthusiasts discuss in real-time
-- ============================================================
INSERT INTO sources (name, slug, url, source_type, tier, trust_score, crawl_interval_minutes) VALUES
('Reddit r/MachineLearning', 'reddit-MachineLearning', 'https://www.reddit.com/r/MachineLearning/hot.json?limit=25', 'api', 4, 0.60, 120),
('Reddit r/LocalLLaMA', 'reddit-LocalLLaMA', 'https://www.reddit.com/r/LocalLLaMA/hot.json?limit=25', 'api', 4, 0.55, 120),
('Reddit r/artificial', 'reddit-artificial', 'https://www.reddit.com/r/artificial/hot.json?limit=25', 'api', 4, 0.50, 180),
('Reddit r/ChatGPT', 'reddit-ChatGPT', 'https://www.reddit.com/r/ChatGPT/hot.json?limit=25', 'api', 4, 0.45, 180),
('Reddit r/OpenAI', 'reddit-OpenAI', 'https://www.reddit.com/r/OpenAI/hot.json?limit=25', 'api', 4, 0.50, 180),
('Reddit r/ClaudeAI', 'reddit-ClaudeAI', 'https://www.reddit.com/r/ClaudeAI/hot.json?limit=25', 'api', 4, 0.50, 180),
('Reddit r/singularity', 'reddit-singularity', 'https://www.reddit.com/r/singularity/hot.json?limit=25', 'api', 4, 0.40, 240),
('Reddit r/StableDiffusion', 'reddit-StableDiffusion', 'https://www.reddit.com/r/StableDiffusion/hot.json?limit=20', 'api', 4, 0.45, 240),
('Reddit r/mlops', 'reddit-mlops', 'https://www.reddit.com/r/mlops/hot.json?limit=20', 'api', 4, 0.55, 240),
('Reddit r/LLMDevs', 'reddit-LLMDevs', 'https://www.reddit.com/r/LLMDevs/hot.json?limit=20', 'api', 4, 0.55, 180),
('Reddit r/deeplearning', 'reddit-deeplearning', 'https://www.reddit.com/r/deeplearning/hot.json?limit=20', 'api', 4, 0.50, 240),
('Reddit r/LanguageTechnology', 'reddit-LanguageTechnology', 'https://www.reddit.com/r/LanguageTechnology/hot.json?limit=20', 'api', 4, 0.55, 360);

-- ============================================================
-- TIER 4: Hacker News (trust 0.55)
-- The original tech community - still where big news breaks fast
-- ============================================================
INSERT INTO sources (name, slug, url, source_type, tier, trust_score, crawl_interval_minutes) VALUES
('Hacker News AI', 'hackernews-ai', 'https://hn.algolia.com/api/v1/search?tags=story&query=AI+LLM+GPT+machine+learning&hitsPerPage=30', 'api', 4, 0.55, 60),
('Hacker News AI Agents', 'hackernews-agents', 'https://hn.algolia.com/api/v1/search?tags=story&query=AI+agent+autonomous&hitsPerPage=20', 'api', 4, 0.55, 120),
('Hacker News ML', 'hackernews-ml', 'https://hn.algolia.com/api/v1/search?tags=story&query=transformer+neural+network+deep+learning&hitsPerPage=20', 'api', 4, 0.55, 120);

-- ============================================================
-- TIER 4: Newsletters & Substacks (trust 0.55)
-- Curated by respected AI commentators
-- ============================================================
INSERT INTO sources (name, slug, url, source_type, tier, trust_score, crawl_interval_minutes) VALUES
('The Batch (Andrew Ng)', 'the-batch', 'https://www.deeplearning.ai/the-batch/', 'scraper', 4, 0.65, 720),
('Import AI (Jack Clark)', 'import-ai', 'https://importai.substack.com/feed', 'rss', 4, 0.65, 720),
('The Algorithmic Bridge', 'algorithmic-bridge', 'https://thealgorithmicbridge.substack.com/feed', 'rss', 4, 0.55, 720),
('AI Supremacy', 'ai-supremacy', 'https://aisupremacy.substack.com/feed', 'rss', 4, 0.50, 720),
('Interconnects (Nathan Lambert)', 'interconnects', 'https://www.interconnects.ai/feed', 'rss', 4, 0.65, 360),
('One Useful Thing (Ethan Mollick)', 'one-useful-thing', 'https://www.oneusefulthing.org/feed', 'rss', 4, 0.65, 360),
('Ahead of AI (Sebastian Raschka)', 'ahead-of-ai', 'https://magazine.sebastianraschka.com/feed', 'rss', 4, 0.65, 720),
('The Neuron', 'the-neuron', 'https://www.theneurondaily.com/feed', 'rss', 4, 0.50, 360),
('Ben Batchelor AI', 'ben-ai', 'https://bensbites.beehiiv.com/feed', 'rss', 4, 0.50, 360),
('Davis Summarizes Papers', 'davis-papers', 'https://dblalock.substack.com/feed', 'rss', 4, 0.60, 720),
('Latent Space Podcast', 'latent-space', 'https://www.latent.space/feed', 'rss', 4, 0.60, 360);

-- ============================================================
-- TIER 4.5: Discord Communities (trust 0.40)
-- Real-time discussions among practitioners
-- Requires DISCORD_BOT_TOKEN, initially set is_active=false
-- ============================================================
INSERT INTO sources (name, slug, url, source_type, tier, trust_score, crawl_interval_minutes, is_active) VALUES
('Discord: Hugging Face #announcements', 'discord-hf-announcements', 'discord://879548962464493619', 'discord', 4, 0.50, 360, false),
('Discord: EleutherAI #general', 'discord-eleutherai-general', 'discord://729741769192767510', 'discord', 4, 0.45, 360, false),
('Discord: LangChain #announcements', 'discord-langchain', 'discord://1038097195422978059', 'discord', 4, 0.45, 360, false),
('Discord: Midjourney #announcements', 'discord-midjourney', 'discord://662267976984297473', 'discord', 4, 0.40, 720, false),
('Discord: Stability AI #announcements', 'discord-stability', 'discord://1002292111942635562', 'discord', 4, 0.45, 360, false),
('Discord: NVIDIA AI #general', 'discord-nvidia-ai', 'discord://1081662955026649288', 'discord', 4, 0.50, 360, false),
('Discord: Together AI', 'discord-together', 'discord://1044790182850433085', 'discord', 4, 0.45, 480, false),
('Discord: Ollama #general', 'discord-ollama', 'discord://1103672645616975962', 'discord', 4, 0.40, 360, false),
('Discord: LM Studio', 'discord-lmstudio', 'discord://1110598183144399058', 'discord', 4, 0.40, 360, false);

-- ============================================================
-- TIER 5: Aggregators & Product Discovery (trust 0.45)
-- ============================================================
INSERT INTO sources (name, slug, url, source_type, tier, trust_score, crawl_interval_minutes) VALUES
('Product Hunt AI', 'producthunt-ai', 'https://www.producthunt.com/feed?category=artificial-intelligence', 'rss', 5, 0.40, 360);
