# Main script to tie everything together
import json
from input_builders import *
from prompt_builder import build_prompt

from model_runner import query_llm
from output_formatter import format_output
from config import CONFIG
import fasttext
#LID_MODEL = fasttext.load_model("models/lid.176.bin")  # load once globally


INPUT_BUILDERS = {
    "raw_text": build_input_raw_text,
    "tokenized": build_input_tokenized,
    "dominant_lang": build_input_dominant_lang,
    "token_lid": build_input_token_lid,
    "fasttext_lid": build_input_fasttext_lid
}

# Loading few-shot blocks
def load_few_shot_block(path: str) -> str:
    if Path(path).exists():
        return Path(path).read_text(encoding="utf-8").strip()
    return ""

# Analyzing language distribution-fasttext
def analyze_languages(text: str, top_k: int = 3):
    predictions = LID_MODEL.predict(text, k=top_k)
    labels = [label.replace("__label__", "") for label in predictions[0]]
    probs = predictions[1]
    return {label: round(prob * 100, 2) for label, prob in zip(labels, probs)}


def main():
    input_fn = INPUT_BUILDERS[CONFIG["input_mode"]]
    #few_shot_block = load_few_shot_block(CONFIG.get("few_shot_path", ""))  # optional

    with open(CONFIG["input_path"], "r", encoding="utf-8") as f_in, \
         open(CONFIG["output_path"], "w", encoding="utf-8") as f_out:

        for line in f_in:
            print("-------------------------------\n")
            entry = json.loads(line)
            input_data = input_fn(entry)

            # Run FastText to get lang composition
            #lang_composition = analyze_languages(entry["text"])

            # Build the prompt using all available context
            prompt = build_prompt(
                input_data=input_data,
                prompt_id=CONFIG["prompt_id"],
            #    lang_composition=lang_composition,
            #    few_shot_block=few_shot_block
            )

            print(f"\nProcessing: {entry['id']}")
            print(f"\n--- Prompt ID: {CONFIG['prompt_id']} ---")
            print(prompt)
            llm_output = query_llm(prompt)
            print(llm_output, "\n")

            result = format_output(entry["id"], entry["text"], llm_output)

            f_out.write(json.dumps(result) + "\n")
            print("-------------------------------\n")

if __name__ == "__main__":
    main()

'''
def main():
    input_fn = INPUT_BUILDERS[CONFIG["input_mode"]]

    with open(CONFIG["input_path"], "r", encoding="utf-8") as f_in, \
         open(CONFIG["output_path"], "w", encoding="utf-8") as f_out:

        for line in f_in:
            print("-------------------------------\n")
            entry = json.loads(line)
            input_data = input_fn(entry)
            prompt = build_prompt(input_data, CONFIG["prompt_id"])
            #prompt = build_prompt(entry["text"], CONFIG["prompt_id"])

            print(f"\nProcessing: {entry['id']}")
            print(f"\n--- Prompt ID: {CONFIG['prompt_id']} ---")
            print(prompt)
            llm_output = query_llm(prompt)
            print(llm_output, "\n")

            result = format_output(entry["id"], entry["text"], llm_output)

            f_out.write(json.dumps(result) + "\n")
            print("-------------------------------\n")
if __name__ == "__main__":
    main()
'''