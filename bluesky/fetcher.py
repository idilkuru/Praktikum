from atproto import Client
import time

class BlueskyFetcher:
    def __init__(self, handle, app_password):
        self.client = Client()
        self.client.login(handle, app_password)
        print("Logged in to Bluesky.")
'''
    def fetch_diverse_posts(self, queries, max_total_posts=400000, sleep_time=1, seen_uris=None):
        from itertools import cycle

        all_posts = []
        seen_ids = set(seen_uris) if seen_uris else set()
        total = 0
        cursor_map = {query: None for query in queries}
        query_cycle = cycle(queries)

        print(f" Starting round-robin collection for {len(queries)} queries...")

        while total < max_total_posts:
            query = next(query_cycle)
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
                print(f" No more posts for query '{query}' — skipping")
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
'''

def fetch_diverse_posts(self, queries, max_total_posts=200000, sleep_time=1):
    from itertools import cycle

    all_posts = []
    seen_ids = set()
    total = 0
    cursor_map = {query: None for query in queries}
    query_cycle = cycle(queries)
    inactive_queries = set()  # To track queries that yielded no posts

    print(f" Starting round-robin collection for {len(queries)} queries...")

    while total < max_total_posts and len(inactive_queries) < len(queries):
        query = next(query_cycle)
        if query in inactive_queries:
            continue

        cursor = cursor_map[query]
        print(f"\n Query: '{query}' (Total so far: {total})")

        try:
        print("✅ Logged in to Bluesky.")

    def fetch_posts(self, query='a', max_posts=1000, sleep_time=1):
        cursor = None
        total = 0
        all_posts = []

        while total < max_posts:
            resp = self.client.app.bsky.feed.search_posts({
                'q': query,
                'limit': 100,
                'cursor': cursor
            })

        posts = resp.posts
        if not posts:
            print(f" No more posts for query '{query}' — skipping future rounds")
            inactive_queries.add(query)

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
