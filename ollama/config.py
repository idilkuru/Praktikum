# Stores experiment configuration

CONFIG = {
    "input_mode": "panlex_offline",  # Options: raw_text, raw_tokens, GlotLid, tokenized, dominant_lang, token_lid, fasttext_lid, panlex_api, panlex_offline
    "prompt_id": 16,
    "few_shot_path": "../ollama/prompts/few_shot_examples.txt",
    "input_path": "Data/merged_dataset_1800.jsonl",
    "output_path": "Data/test.jsonl",
# NEW for Groq
    "llm_provider": "groq",  # Options: "groq", "ollama"
    "llm_model": "qwen/qwen3-32b",  # Example: deepseek-r1-distill-llama-70b, "qwen1.5-7b-chat", "mixtral-8x7b", qwen/qwen3-32b, llama3-70b-8192

}