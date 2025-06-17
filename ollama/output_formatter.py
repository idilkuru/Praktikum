# Converts LLM response into desired structure

import re

def format_output(entry_id, original_text, llm_response):
    tokens = []
    labels = []

    lines = llm_response.strip().splitlines()
    for line in lines:
        # Match lines like "1. Hi: en" or "Hi: en"
        match = re.search(r"(?:\d+\.\s*)?([^:]+):\s*([a-z]{2,3})", line.strip())
        if match:
            token = match.group(1).strip()
            label = match.group(2).strip()
            tokens.append(token)
            labels.append(label)

    return {
        "id": entry_id,
        "text": original_text,
        "llama_tokens": tokens,
        "llama_labels": labels
    }

