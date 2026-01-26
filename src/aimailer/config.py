DEFAULT_SOURCES = [
    'https://openai.com/blog/rss.xml',
    'https://blog.google/technology/developers/rss/',
    'https://github.blog/feed/',
    'https://huggingface.co/blog/feed.xml',
    'https://aws.amazon.com/blogs/machine-learning/feed/',
    'https://blog.langchain.dev/feed/',
]
KEYWORDS = ['mcp', 'agent', 'cli', 'opencode', 'gemini', 'gpt-5.1', 'ai', 'llm', 'model', 'langchain', 'huggingface']
SCHEDULE = 'Daily 12:00'
RECIPIENTS = [
    'stephen.phillips.work@gmail.com',
]
EMAIL_SUBJECT = 'Daily AI Tooling Roundup'
EMAIL_TITLE = 'Daily AI Tooling Roundup'
CACHE_FILE = '/var/www/html/happymonkey.ai/AIMailer/sent_articles.json'
