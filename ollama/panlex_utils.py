import requests
import time

PANLEX_BASE_URL = "https://api.panlex.org"

def get_iso_from_lv(lv_id, retries=1, delay=0.5):
    """Fetch ISO 639-3 code from PanLex language variety ID, with retry."""
    for attempt in range(retries + 1):
        try:
            url = f"{PANLEX_BASE_URL}/lv/{lv_id}"
            response = requests.get(url, timeout=90)
            response.raise_for_status()
            data = response.json()
            return data.get("lv", {}).get("lc")
        except Exception as e:
            print(f"[PanLex] Attempt {attempt + 1} failed for LV {lv_id}: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                return None


def get_panlex_candidates(token):
    """
    Query PanLex for up to 5 possible ISO language codes for a token.
    Uses POST /ex endpoint.
    """
    try:
        url = f"{PANLEX_BASE_URL}/ex"
        headers = {"Content-Type": "application/json"}
        payload = {"tt": [token]}

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
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

        return iso_codes

    except Exception as e:
        print(f"[PanLex] Error for token '{token}': {e}")
        return []