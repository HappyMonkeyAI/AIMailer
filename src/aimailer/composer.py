from typing import List, Dict


def compose_html(title: str, items: List[Dict]) -> str:
    parts = [f"<div style='font-family:Arial,sans-serif;max-width:680px;margin:0 auto;'>",
             f"<h1>{title}</h1>"]
    for i, it in enumerate(items, start=1):
        parts.append(f"<h3 style='margin-bottom:6px;'>{i}. {it.get('title')}</h3>")
        parts.append(f"<p style='color:#374151;'>{it.get('summary')}</p>")
        parts.append(f"<p><a href=\"{it.get('url')}\">Read more →</a></p>")
        parts.append("<hr />")
    parts.append('</div>')
    return '<html><body>' + '\n'.join(parts) + '</body></html>'
