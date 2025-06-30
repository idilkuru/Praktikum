import os
import requests
import time
from config import CONFIG
import subprocess

def query_llm(prompt: str) -> str:
    provider = CONFIG.get("llm_provider", "groq")
    model = CONFIG.get("llm_model", "qwen/qwen3-32b")
    api_key = "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"

    if provider == "groq":
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0
        }

        max_retries = 10
        for attempt in range(max_retries):
            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

            if response.status_code == 200:
                time.sleep(0.2)  # Add delay between requests
                return response.json()["choices"][0]["message"]["content"].strip()

            elif response.status_code == 429:
                print(f"[{attempt+1}/{max_retries}] Rate limit hit. Sleeping before retry...")
                time.sleep(2 ** attempt)  # Exponential backoff

            else:
                print(f"Error from Groq API ({response.status_code}): {response.text}")
                response.raise_for_status()

        raise RuntimeError("Max retries exceeded due to rate limits.")

    elif provider == "ollama":
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")


'''
def query_llm(prompt, model="phi3:3.8b"): # llama3, qwen3:8b, deepseek-r1:8b, mistral:7b, command-r7b:7b, phi3:3.8b
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json().get("response", "")
'''