import json
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
from tqdm import tqdm

model_name = "sagorsarker/codeswitch-spaeng-lid-lince"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

input_path = "Data/merged_dataset_1800.jsonl"
output_path = "Data/merged_dataset_1800_spa.jsonl"


def predict_labels(tokens):
    encoding = tokenizer(tokens, is_split_into_words=True, return_offsets_mapping=True, return_tensors=None,
                         padding=True, truncation=True)

    word_ids = encoding.word_ids()
    inputs = tokenizer(tokens, is_split_into_words=True, return_tensors="pt", padding=True, truncation=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    predictions = torch.argmax(logits, dim=2)[0].cpu().numpy()
    id2label = model.config.id2label

    token_predictions = []
    prev_word_id = None
    for idx, word_id in enumerate(word_ids):
        if word_id is None or word_id == prev_word_id:
            continue
        label = id2label[predictions[idx]]
        token_predictions.append(label)
        prev_word_id = word_id

    return token_predictions

with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
    for line in tqdm(infile, desc="Processing"):
        example = json.loads(line.strip())
        tokens = example["tokens"]
        predicted_labels = predict_labels(tokens)

        # Ensure length match
        if len(predicted_labels) != len(tokens):
            print(f"[WARN] Token-prediction length mismatch in ID {example.get('id')}")

        example["predicted_labels"] = predicted_labels
        outfile.write(json.dumps(example, ensure_ascii=False) + "\n")