# Stores experiment configuration

# rawText: raw text input
# tokenized: tokenized input using spaCy
# fasttext_lid: uses FastText for sentence-level LID
# maskLid: uses MaskLID for token-level LID

CONFIG = {
    "input_mode": "rawText",  # Options: rawText, tokenized, fasttext_lid, maskLid
    "prompt_id": 7,
    #"few_shot_path": "../ollama/prompts/few_shot_example.txt",
    "input_path": "../Data/merged_data_4.jsonl",
    "output_path": "../Data/llama3_merged_dataset_4_04.jsonl"
}