# Stores experiment configuration

CONFIG = {
    "input_mode": "raw_tokens",  # Options: raw_text, raw_tokens, tokenized, dominant_lang, token_lid, fasttext_lid
    "prompt_id": 4,
    "few_shot_path": "../ollama/prompts/few_shot_examples.txt",
    "input_path": "/Users/faisal/PycharmProjects/PythonProject/Praktikum/Data/merged_dataset_1800.jsonl",
    "output_path": "/Users/faisal/PycharmProjects/PythonProject/Praktikum/Data/8_groq_r1_merged_dataset_1800.jsonl",
# NEW for Groq
    "llm_provider": "groq",  # Options: "groq", "ollama"
    "llm_model": "qwen/qwen3-32b",  # Example: "qwen1.5-7b-chat", "deepseek-coder", "mixtral-8x7b", qwen/qwen3-32b, llama3-70b-8192

}