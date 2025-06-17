# Main script to tie everything together
import json
from input_builders import *
from prompt_builder import build_prompt

from model_runner import query_llm
from output_formatter import format_output
from config import CONFIG

INPUT_BUILDERS = {
    "raw_text": build_input_raw_text,
    "tokenized": build_input_tokenized,
    "dominant_lang": build_input_dominant_lang,
    "token_lid": build_input_token_lid
}

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