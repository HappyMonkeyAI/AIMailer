import json
import os
from typing import Optional, Tuple, Dict

class FeedCache:
    def __init__(self, cache_file: str):
        self.cache_file = cache_file
        self.data: Dict[str, Dict[str, str]] = self._load_cache()

    def _load_cache(self) -> Dict[str, Dict[str, str]]:
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def get(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        entry = self.data.get(url, {})
        return entry.get('etag'), entry.get('modified')

    def update(self, url: str, etag: Optional[str], modified: Optional[str]):
        if not etag and not modified:
            return

        self.data[url] = {'etag': etag, 'modified': modified}
        self._save_cache()

    def _save_cache(self):
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception:
            pass
