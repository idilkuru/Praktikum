from bluesky.fetcher import BlueskyFetcher
import json
import time

# Modified BlueskyFetcher with skip-zero-post queries logic
class BlueskyFetcher:
    def __init__(self, handle, app_password):
        from atproto import Client
        self.client = Client()
        self.client.login(handle, app_password)
        print("Logged in to Bluesky.")

    def fetch_diverse_posts(self, queries, max_total_posts=400000, sleep_time=1):
        from itertools import cycle

        all_posts = []
        seen_ids = set()
        total = 0
        cursor_map = {query: None for query in queries}
        query_cycle = cycle(queries)
        inactive_queries = set()

        print(f" Starting round-robin collection for {len(queries)} queries...")

        while total < max_total_posts and len(inactive_queries) < len(queries):
            query = next(query_cycle)
            if query in inactive_queries:
                continue

            cursor = cursor_map[query]
            print(f"\n Query: '{query}' (Total so far: {total})")

            try:
                resp = self.client.app.bsky.feed.search_posts({
                    'q': query,
                    'limit': 100,
                    'cursor': cursor
                })
            except Exception as e:
                print(f" Error for query '{query}': {e}")
                continue

            posts = resp.posts
            if not posts:
                print(f" No more posts for query '{query}' — skipping future rounds")
                inactive_queries.add(query)
                continue

            new_posts_this_query = 0
            for post in posts:
                if post.uri not in seen_ids:
                    all_posts.append(post)
                    seen_ids.add(post.uri)
                    total += 1
                    new_posts_this_query += 1

                    if total >= max_total_posts:
                        break

            print(f" {new_posts_this_query} new posts for '{query}' (Total: {total})")
            cursor_map[query] = resp.cursor
            time.sleep(sleep_time)

        print(f"\n Done: Collected {total} total posts from {len(seen_ids)} unique URIs.")
        return all_posts

# Recursive function to convert non-serializable objects to dictionaries
def convert_to_serializable(obj):
    if isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif hasattr(obj, "__dict__"):
        return convert_to_serializable(obj.__dict__)
    else:
        return obj

def save_posts(posts, filename='data/bluesky_posts2.json'):
    """
    Save collected posts to a JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        serializable_posts = [convert_to_serializable(post) for post in posts]
        json.dump(serializable_posts, f, ensure_ascii=False, indent=2)
    print(f" Saved {len(posts)} posts to {filename}")

def main():
    handle = 'fayysal.bsky.social'
    app_password = 'dckj-gzaf-ocrr-zavc'

    fetcher = BlueskyFetcher(handle, app_password)
    queries = [ 'the', 'a','yes','am','i','lol','in','of','usa']

    posts = []
    try:
        posts = fetcher.fetch_diverse_posts(queries, max_total_posts=400000)
    except KeyboardInterrupt:
        print(f"\n Interrupted manually. Saving {len(posts)} collected posts...")
    finally:
        save_posts(posts)
        print(f" Finished. {len(posts)} posts saved.")

if __name__ == '__main__':
    main()