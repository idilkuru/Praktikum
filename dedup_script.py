import json

def deduplicate_by_uri(input_path='Data/bluesky_posts.json', output_path='Data/bluesky_posts_deduped.json'):
    with open(input_path, 'r', encoding='utf-8') as f:
        posts = json.load(f)

    seen_uris = set()
    deduped = []

    for post in posts:
        uri = post.get('uri')
        if uri and uri not in seen_uris:
            seen_uris.add(uri)
            deduped.append(post)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(deduped, f, ensure_ascii=False, indent=2)

    print(f" Deduplicated {len(posts)} → {len(deduped)} posts.")