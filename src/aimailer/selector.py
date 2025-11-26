from typing import List, Dict, Optional
from datetime import datetime, timezone
from dateutil import parser as dateparser
from difflib import SequenceMatcher
import math


def parse_date(datestr: Optional[str]) -> Optional[datetime]:
    if not datestr:
        return None
    try:
        dt = dateparser.parse(datestr)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, a or '', b or '').ratio()


def dedupe(items: List[Dict]) -> List[Dict]:
    out: List[Dict] = []
    seen_urls = set()
    for it in items:
        url = (it.get('url') or '').split('?')[0]
        if url and url in seen_urls:
            continue
        dup = False
        for e in out:
            eu = (e.get('url') or '').split('?')[0]
            if url and eu and eu == url:
                dup = True
                break
            if similar(e.get('title',''), it.get('title','')) > 0.88:
                dup = True
                break
        if dup:
            continue
        if url:
            seen_urls.add(url)
        out.append(it)
    return out


def score_item(item: Dict, keywords: List[str], source_weight_map: Optional[Dict[str, float]] = None) -> float:
    score = 0.0
    date = None
    if item.get('date'):
        date = parse_date(item.get('date'))
    if date:
        seconds = (date - datetime(1970,1,1, tzinfo=timezone.utc)).total_seconds()
        try:
            score += float(math.log1p(float(seconds)) / 100000.0)
        except Exception:
            pass
    text = (item.get('title','') + ' ' + item.get('summary','')).lower()
    for kw in keywords or []:
        if kw.lower() in text:
            score += 1.0
    src = (item.get('source') or '').lower()
    if source_weight_map:
        for k, v in source_weight_map.items():
            try:
                if k.lower() in src:
                    score += float(v)
            except Exception:
                continue
    if item.get('confidence') is not None:
        try:
            score += float(item.get('confidence'))
        except Exception:
            pass
    return score


def select_top(items: List[Dict], keywords: List[str], source_weight_map: Optional[Dict[str, float]] = None, n: int = 12) -> List[Dict]:
    items = dedupe(items)
    scored = []
    for it in items:
        s = score_item(it, keywords, source_weight_map)
        scored.append((s, it))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [it for _, it in scored[:n]]
