import csv
import ast
import json
import re

def map_label(label):
    label = label.lower()
    lang_map = {
        "lang1": "eng",
        "lang2": "spa",
        "en": "eng",
        "english": "eng",
        "es": "spa",
        "spanish": "spa",
        "de": "deu",
        "tr": "tur",
        "hi": "hin",
        "id": "ind",
        "ne": "named_entity",
        "un": "other",
        "other": "other",
        "OTHER": "Other"
    }
    return lang_map.get(label, "other")  # default "other" if unknown

def extract_tokens(tokens_str):
    """
    Extract the token list from the 'tokens' column string.
    This finds the 'list([...])' substring and parses it safely.
    """
    match = re.search(r'list\(\[.*?\]\)', tokens_str)
    if not match:
        raise ValueError(f"Could not find list(...) pattern in: {tokens_str}")

    list_expr = match.group(0)  # e.g. "list(['@minamin2403', 'not', ...])"
    inner_list_str = list_expr[len("list("):-1]
    tokens = ast.literal_eval(inner_list_str)
    return tokens

def parse_dataset_02(filepath):
    parsed_data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tokens = extract_tokens(row['tokens'])
            langs = ast.literal_eval(row['langs'])
            norm_tokens = ast.literal_eval(row['norm_tokens'])
            clean_tweets = ast.literal_eval(row['clean_tweets'])
            bio_tags = row['bio_tags']

            if not (len(tokens) == len(langs) == len(norm_tokens)):
                print(f"Row no: {row['no']}")
                print(f"tokens ({len(tokens)}): {tokens}")
                print(f"bio_tags ({len(bio_tags)}): {bio_tags}")
                print(f"langs ({len(langs)}): {langs}")
                print(f"norm_tokens ({len(norm_tokens)}): {norm_tokens}")
                raise ValueError(f"Length mismatch at row {row['no']}")

            labels_unified = [map_label(l) for l in langs]

            entry = {
                "id": f"ds2_{str(row['no']).zfill(6)}",
                "text": row['raw_tweet'],          # renamed here
                "tokens": tokens,
                "labels_unified": labels_unified,  # moved here as 4th variable
                # other fields after these 4
                #"bio_tags": bio_tags,
                "langs": langs,
                #"norm_tokens": norm_tokens,
                #"clean_tweets": clean_tweets
            }
            parsed_data.append(entry)
    return parsed_data

if __name__ == "__main__":
    filepath = "/Users/faisal/PycharmProjects/PythonProject/Praktikum/Data/dataset_02.csv"
    parsed_data = parse_dataset_02(filepath)

    print("Sample entries:")
    for entry in parsed_data[:2]:
        print(json.dumps(entry, indent=2, ensure_ascii=False))

    output_path = "/Users/faisal/PycharmProjects/PythonProject/Praktikum/Data/parsed_dataset_02.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in parsed_data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"\n Saved to {output_path}")
