# Stores experiment configuration

CONFIG = {
    "input_mode": "raw_tokens",  # Options: raw_text, raw_tokens, tokenized, dominant_lang, token_lid, fasttext_lid
    "prompt_id": 2,
    "few_shot_path": "../ollama/prompts/few_shot_examples.txt",
    "input_path": "../Data/merged_dataset_500.jsonl",
    "output_path": "../Data/llama3_merged_dataset_500_2.jsonl"
}