import requests
import time
import random

PANLEX_BASE_URL = "https://api.panlex.org"
MAX_RETRIES = 5
REQUEST_CACHE = {}  # simple in-memory cache


def safe_request(url, method="GET", headers=None, json=None):
    """
    Makes a request to the given URL with retry handling.
    Retries on 429 and 502 errors, with exponential backoff.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.request(method, url, headers=headers, json=json)

            if response.status_code == 429:
                wait = min(2 ** attempt, 10)
                print(f"[PanLex] 429 Too Many Requests. Retrying in {wait}s...")
                time.sleep(wait)
                continue

            if response.status_code == 502:
                wait = 1 + random.random()
                print(f"[PanLex] 502 Bad Gateway. Retrying in {wait:.2f}s...")
                time.sleep(wait)
                continue

            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            print(f"[PanLex] Request failed (attempt {attempt}/{MAX_RETRIES}): {e}")
            time.sleep(1)

    raise Exception("[PanLex] Max retries exceeded.")


def get_iso_from_lv(lv_id):
    """Fetch ISO 639-3 code from PanLex language variety ID (lv)."""
    if lv_id in REQUEST_CACHE:
        return REQUEST_CACHE[lv_id]

    url = f"{PANLEX_BASE_URL}/lv/{lv_id}"
    try:
        response = safe_request(url)
        data = response.json()
        iso_code = data.get("lv", {}).get("lc")
        REQUEST_CACHE[lv_id] = iso_code
        return iso_code
    except Exception as e:
        print(f"[PanLex] Error getting ISO code for LV {lv_id}: {e}")
        return None


def get_panlex_candidates_api(token):
    """
    Query PanLex for up to 5 ISO language codes for a token.
    Uses POST /ex endpoint. Caches and limits to max 5 languages.
    """
    if len(token) < 3:
        return []  # exclude short/irrelevant tokens

    token_key = f"ex::{token}"
    if token_key in REQUEST_CACHE:
        return REQUEST_CACHE[token_key]

    url = f"{PANLEX_BASE_URL}/ex"
    headers = {"Content-Type": "application/json"}
    payload = {"tt": [token]}

    try:
        response = safe_request(url, method="POST", headers=headers, json=payload)
        data = response.json()

        iso_codes = []
        for entry in data.get("result", []):
            lv_id = entry.get("lv")
            if lv_id is not None:
                iso = get_iso_from_lv(lv_id)
                if iso and iso not in iso_codes:
                    iso_codes.append(iso)
                if len(iso_codes) >= 5:
                    break

        REQUEST_CACHE[token_key] = iso_codes
        return iso_codes

    except Exception as e:
        print(f"[PanLex] Error for token '{token}': {e}")
        return []


# offline access to PanLex

import os
import pickle

PANLEX_INDEX_FILE = "panlex/panlex_indexed.pkl"
PANLEX_INDEX_URL = "https://huggingface.co/datasets/elias-bonk/panlex_indexed/resolve/main/panlex_indexed.pkl"

_panlex_vocab_index = None


def _download_if_missing(file_path, url):
    if not os.path.exists(file_path):
        print(f"[PanLex] File '{file_path}' not found. Downloading from {url}...")

        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive chunks
                            f.write(chunk)
            print(f"[PanLex] Download completed.")
        except Exception as e:
            print(f"[PanLex] Failed to download file: {e}")
            raise


def _load_panlex_index():
    global _panlex_vocab_index
    if _panlex_vocab_index is None:
        _download_if_missing(PANLEX_INDEX_FILE, PANLEX_INDEX_URL)
        print("[PanLex] Loading PanLex index...")
        with open(PANLEX_INDEX_FILE, "rb") as f:
            _panlex_vocab_index = pickle.load(f)
    return _panlex_vocab_index


def get_panlex_candidates_offline(token):
    _load_panlex_index()
    token = token.strip().lower()
    return list(_panlex_vocab_index.get(token, []))[:5]
