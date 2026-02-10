import sys
import os
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from email.utils import formatdate

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from aimailer import fetchers

PORT = 8999
FEED_FILE = 'tests/sample_feed.xml'
CACHE_FILE = 'tests/benchmark_feed_cache.json'
ETAG = '"12345"'
LAST_MODIFIED = formatdate(time.time(), usegmt=True)

# Clean up previous cache
if os.path.exists(CACHE_FILE):
    os.remove(CACHE_FILE)

class ConditionalRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('sample_feed.xml'):
            # Check headers
            if_none_match = self.headers.get('If-None-Match')
            if_modified_since = self.headers.get('If-Modified-Since')

            if if_none_match == ETAG or if_modified_since == LAST_MODIFIED:
                self.send_response(304)
                self.end_headers()
                return

            self.send_response(200)
            self.send_header('Content-type', 'application/xml')
            self.send_header('ETag', ETAG)
            self.send_header('Last-Modified', LAST_MODIFIED)
            self.end_headers()

            # Serve file content
            with open(FEED_FILE, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass  # Suppress logging

def run_server():
    # Allow reuse address to avoid "Address already in use"
    HTTPServer.allow_reuse_address = True
    server = HTTPServer(('localhost', PORT), ConditionalRequestHandler)
    server.serve_forever()

def benchmark():
    # Start server
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1) # Wait for server

    url = f'http://localhost:{PORT}/tests/sample_feed.xml'

    print("--- First Fetch (Cold Cache) ---")
    start = time.time()
    items1 = fetchers.fetch_rss(url, cache_file=CACHE_FILE)
    duration1 = time.time() - start
    print(f"Items fetched: {len(items1)}")
    print(f"Duration: {duration1:.4f}s")

    print("\n--- Second Fetch (Warm Cache) ---")
    start = time.time()
    items2 = fetchers.fetch_rss(url, cache_file=CACHE_FILE)
    duration2 = time.time() - start
    print(f"Items fetched: {len(items2)}")
    print(f"Duration: {duration2:.4f}s")

    if len(items2) == 0 and len(items1) > 0:
         print("\nSUCCESS: Second fetch returned 0 items (Conditional GET working)")
    elif len(items2) == len(items1):
         print("\nFAILURE: Second fetch returned same items (Conditional GET NOT working)")
    else:
         print(f"\nUNKNOWN: Second fetch returned {len(items2)} items")

    # Cleanup
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)

if __name__ == "__main__":
    benchmark()
