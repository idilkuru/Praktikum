from atproto import Client
import time

class BlueskyFetcher:
    def __init__(self, handle, app_password):
        self.client = Client()
        self.client.login(handle, app_password)
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
                break

            all_posts.extend(posts)
            total += len(posts)
            print(f'Collected {total} posts...')

            cursor = resp.cursor
            if not cursor:
                break

            time.sleep(sleep_time)

        return all_posts
