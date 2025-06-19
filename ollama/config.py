# Stores experiment configuration

# rawText: raw text input
# tokenized: tokenized input using spaCy
# fasttext_lid: uses FastText for sentence-level LID
# maskLid: uses MaskLID for token-level LID

CONFIG = {
    "input_mode": "tokenized",  # Options: rawText, tokenized, fasttext_lid, maskLid
    "prompt_id": 3,
    "input_path": "../Praktikum/Data/merged_dataset_4.jsonl",
    "output_path": "../Praktikum/Data/llama3_merged_dataset_4_04.jsonl"
}