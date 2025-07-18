# Main script to tie everything together
import json
from input_builders import *
from prompt_builder import build_prompt
import numpy as np
from model_runner import query_llm
from output_formatter import format_output
from config import CONFIG
from pathlib import Path
#LID_MODEL = fasttext.load_model("../models/lid.176.bin")


INPUT_BUILDERS = {
    "raw_text": build_input_raw_text,
    "raw_tokens":build_input_raw_tokens,
    "tokenized": build_input_tokenized,
    "dominant_lang": build_input_dominant_lang,
    "fasttext_lid": build_input_fasttext_lid,
    "maskLid": build_input_token_lid,
    "GlotLid": build_input_glotlid,
    "panlex_api": build_input_panlex_api,
    "panlex_offline": build_input_panlex_offline
}

# Loading few-shot blocks
def load_few_shot_block(path: str) -> str:
    if Path(path).exists():
        return Path(path).read_text(encoding="utf-8").strip()
    return ""

def main():
    input_fn = INPUT_BUILDERS[CONFIG["input_mode"]]
    few_shot_block = load_few_shot_block(CONFIG.get("few_shot_path", ""))  # optional

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
                #lang_composition=lang_composition,
                few_shot_block=few_shot_block
            )

            print(f"\nProcessing: {entry['id']}")
            print(f"\n--- Prompt ID: {CONFIG['prompt_id']} ---")
            print(prompt)
            llm_output = query_llm(prompt)
            print(llm_output, "\n")

            #result = format_output(entry["id"], entry["text"], llm_output)
            result = format_output(entry["id"], entry["text"], llm_output, input_data=input_data)
            f_out.write(json.dumps(result) + "\n")
            print("-------------------------------\n")

if __name__ == "__main__":
    main()
