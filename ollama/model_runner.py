# Sends prompt to Ollama and gets response
import requests

def query_llm(prompt, model="llama3"):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json().get("response", "")