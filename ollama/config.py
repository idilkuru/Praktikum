# Stores experiment configuration

CONFIG = {
    "input_mode": "GlotLid",  # Options: raw_text, raw_tokens, GlotLid, tokenized, dominant_lang, token_lid, fasttext_lid
    "prompt_id": 9,
    "few_shot_path": "../ollama/prompts/few_shot_examples.txt",
    "input_path": "/Users/faisal/PycharmProjects/PythonProject/Praktikum/Data/new.jsonl",
    "output_path": "/Users/faisal/PycharmProjects/PythonProject/Praktikum/Data/9_groq_r1_merged_dataset_new.jsonl",
# NEW for Groq
    "llm_provider": "groq",  # Options: "groq", "ollama"
    "llm_model": "deepseek-r1-distill-llama-70b",  # Example: deepseek-r1-distill-llama-70b, "qwen1.5-7b-chat", "deepseek-coder", "mixtral-8x7b", qwen/qwen3-32b, llama3-70b-8192

}