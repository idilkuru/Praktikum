from bluesky.fetcher import BlueskyFetcher
import json

# Recursive function to convert non-serializable objects to dictionaries
def convert_to_serializable(obj):
    if isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif hasattr(obj, "__dict__"):  # For objects with a __dict__ attribute
        return convert_to_serializable(obj.__dict__)
    else:
        return obj

def save_posts(posts, filename='data/bluesky_posts.json'):
    """
    Save collected posts to a JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        # Convert posts and their nested objects to serializable dicts
        serializable_posts = [convert_to_serializable(post) for post in posts]
        json.dump(serializable_posts, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved {len(posts)} posts to {filename}")

def main():
    handle = 'fayysal.bsky.social'
    app_password = 'dckj-gzaf-ocrr-zavc'

    fetcher = BlueskyFetcher(handle, app_password)
    posts = fetcher.fetch_posts(query='a', max_posts=10)

    save_posts(posts)
    print(f"✅ Saved {len(posts)} posts to 'data/bluesky_posts.json'.")


if __name__ == '__main__':
    main()