import json
import os
import tempfile
import pathlib
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
            except json.JSONDecodeError as e:
                # Corrupted cache file, ignore
                print(f"JSONDecodeError reading cache {self.cache_file}: {e}")
                pass
            except OSError as e:
                print(f"OSError reading cache {self.cache_file}: {e}")
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
            # Ensure directory exists
            cache_path = pathlib.Path(self.cache_file)
            cache_dir = cache_path.parent
            cache_dir.mkdir(parents=True, exist_ok=True)

            # Atomic write using temp file + replace
            with tempfile.NamedTemporaryFile(mode='w', dir=str(cache_dir), delete=False) as tf:
                json.dump(self.data, tf, indent=2)
                temp_name = tf.name

            os.replace(temp_name, self.cache_file)
        except OSError as e:
            print(f"Error saving cache to {self.cache_file}: {e}")
            # If replacement fails, try to cleanup temp file
            try:
                if 'temp_name' in locals() and os.path.exists(temp_name):
                    os.remove(temp_name)
            except OSError:
                pass
