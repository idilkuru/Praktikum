# Converts LLM response into desired structure

import re

def format_output(entry_id, original_text, llm_response):
    tokens = []
    labels = []

    lines = llm_response.strip().splitlines()
    for line in lines:
        line = line.strip()

        # Match lines like:
        # "token": "label"
        # "token": label
        # token: "label"
        # token: label
        match = re.match(r'^["“]?(.+?)["”]?\s*:\s*["“]?([a-z]{2,5})["”]?\s*$', line)
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

