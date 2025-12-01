DEFAULT_SOURCES = [
    'https://huggingface.co/blog/feed.xml',
    'https://openai.com/blog/rss.xml',
    'https://www.anthropic.com/news/rss.xml',
    'https://blog.google/technology/ai/rss/',
    'https://blogs.microsoft.com/ai/feed/',
    'https://arxiv.org/rss/cs.AI',
    'https://arxiv.org/rss/cs.CL',
    'https://github.blog/feed/',
]
KEYWORDS = [
    'model', 'release', 'llm', 'gpt', 'gemini', 'claude', 'opus', 'grok',
    'coding', 'code', 'programming', 'software', 'developer', 'api',
    'fine-tuning', 'training', 'inference', 'deployment', 'benchmark',
    'open-source', 'huggingface', 'transformers', 'pytorch', 'tensorflow',
    'business', 'enterprise', 'tooling', 'automation', 'qa', 'testing'
]
SCHEDULE = 'Daily 15:00'
RECIPIENTS = [
    'stephen.z.phillips@sparktsl.com',
]
EMAIL_SUBJECT = 'Daily AI Models & Releases Roundup'
EMAIL_TITLE = 'Daily AI Models & Releases Roundup'
CACHE_FILE = '/var/www/html/happymonkey.ai/AIMailer/sent_articles_models.json'
