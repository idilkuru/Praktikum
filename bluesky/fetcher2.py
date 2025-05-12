from atproto import Client
import time

class BlueskyFetcher:
    def __init__(self, handle, app_password):
        self.client = Client()
        self.client.login(handle, app_password)
        print("✅ Logged in to Bluesky.")

    def transform_post(self, post):
       record = post.record
       author = post.author
       language = record.langs[0] if record.langs else None
       external_link = (
            record.embed.external.uri
            if record.embed and hasattr(record.embed, "external")
            else None
        )

       return {
            'uri': post.uri,
            'text': record.text,
            'language': language,
            'created_at': record.created_at,
            'author_handle': author.handle,
            'author_display_name': author.display_name,
            'external_link': external_link
       }

    def fetch_posts(self, query='a', max_posts=10, sleep_time=1):
        cursor = None
        total = 0
        all_posts = []

        while total < max_posts:
            resp = self.client.app.bsky.feed.search_posts({
                'q': query,
                'limit': 100,
                'cursor': cursor
            })

            raw_posts = resp.posts
            if not raw_posts:
                break

            for post in raw_posts:
                all_posts.append(self.transform_post(post))

            total += len(raw_posts)
            print(f'Collected {total} posts...')

            cursor = resp.cursor
            if not cursor:
                break

            time.sleep(sleep_time)

        return all_posts