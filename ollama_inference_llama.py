import json
import requests
from pathlib import Path
from time import sleep

# === Configuration ===
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:8b"
FEW_SHOT_PATH = "prompts/few_shot_examples.txt"
INPUT_PATH = "Data/merged_dataset_100.jsonl"
OUTPUT_PATH = "Data/benchmark_predictions_100.jsonl"

# === Load few-shot examples ===
def load_few_shot_prompt():
    with open(FEW_SHOT_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()

# === Build the prompt ===
def build_prompt(few_shot_text: str, input_text: str) -> str:
    return f"""{few_shot_text}

Input: {input_text}
Output:"""

# === Call Ollama API ===
def query_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        print("[ERROR] Ollama request failed:", e)
        return None

# === Align predicted tokens to match original if needed ===
def postprocess_prediction(response_text):
    try:
        prediction = json.loads(response_text)
        return prediction if isinstance(prediction, list) else []
    except json.JSONDecodeError:
        print("[WARN] Could not parse Ollama output:", response_text)
        return []

# === Main batch processing ===
def run_batch():
    few_shot_text = load_few_shot_prompt()
    input_path = Path(INPUT_PATH)
    output_path = Path(OUTPUT_PATH)

    with input_path.open("r", encoding="utf-8") as infile, output_path.open("w", encoding="utf-8") as outfile:
        for line_num, line in enumerate(infile, 1):
            data = json.loads(line)
            input_text = data["text"]

            prompt = build_prompt(few_shot_text, input_text)
            print(f"[INFO] Processing line {line_num}: {data['id']}")

            response = query_ollama(prompt)
            if response:
                prediction = postprocess_prediction(response)
                data["predicted_labels"] = prediction
            else:
                data["predicted_labels"] = []

            outfile.write(json.dumps(data, ensure_ascii=False) + "\n")
            sleep(0.25)  # throttle requests if needed

if __name__ == "__main__":
    run_batch()