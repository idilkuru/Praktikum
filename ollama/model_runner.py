# Sends prompt to Ollama and gets response
import requests

def query_llm(prompt, model="qwen3:8b"): # llama3, qwen3:8b, deepseek-r1:8b, mistral:7b, command-r7b:7b, phi3:3.8b
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json().get("response", "")