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
    matcher = SequenceMatcher(isjunk=None)
    
    # Pre-compute word sets for accepted items to allow fast pruning
    accepted_word_sets: List[set] = []

    def get_word_set(text: str) -> set:
        return set(text.lower().split())

    for it in items:
        url = (it.get('url') or '').split('?')[0]
        if url and url in seen_urls:
            continue

        it_title = it.get('title', '') or ''
        it_words = get_word_set(it_title)
        
        # SequenceMatcher: set_seq2 is expensive (indexing), do it once per new item
        matcher.set_seq2(it_title)

        dup = False

        # Compare against ALL accepted items (fixed correctness regression)
        for i in range(len(out) - 1, -1, -1):
            e_title = out[i].get('title', '') or ''
            e_words = accepted_word_sets[i]
            
            # Fast pruning: skip if word sets are too different
            if not it_words or not e_words:
                if it_title == e_title:
                    dup = True
                    break
                continue
                
            intersection = len(it_words.intersection(e_words))
            # If less than 40% of words overlap, they are unlikely to be duplicates
            if intersection / max(len(it_words), len(e_words)) < 0.4:
                continue

            matcher.set_seq1(e_title)
            # Fast guards
            if matcher.real_quick_ratio() > 0.88 and matcher.quick_ratio() > 0.88:
                if matcher.ratio() > 0.88:
                    dup = True
                    break

        if dup:
            continue

        if url:
            seen_urls.add(url)
        out.append(it)
        accepted_word_sets.append(it_words)
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


def select_top_diverse(items: List[Dict], keywords: List[str], source_weight_map: Optional[Dict[str, float]] = None, n: int = 12) -> List[Dict]:
    """Select top items ensuring source diversity."""
    items = dedupe(items)
    
    # Group by source
    by_source = {}
    for item in items:
        source = item.get('source', 'unknown')
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(item)
    
    # Score items within each source
    for source, source_items in by_source.items():
        scored = []
        for item in source_items:
            score = score_item(item, keywords, source_weight_map)
            scored.append((score, item))
        scored.sort(key=lambda x: x[0], reverse=True)
        by_source[source] = [item for _, item in scored]
    
    # Select items round-robin from sources
    selected = []
    sources = list(by_source.keys())
    source_idx = 0
    
    while len(selected) < n and any(by_source.values()):
        source = sources[source_idx % len(sources)]
        if by_source[source]:
            selected.append(by_source[source].pop(0))
        source_idx += 1
        
        # Remove empty sources
        if not by_source[source]:
            sources.remove(source)
            if not sources:
                break
    
    return selected


def select_top(items: List[Dict], keywords: List[str], source_weight_map: Optional[Dict[str, float]] = None, n: int = 12) -> List[Dict]:
    """Use diverse selection by default."""
    return select_top_diverse(items, keywords, source_weight_map, n)
