import json

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
        "ne": "other",
        "un": "other",
        "other": "other",
        "OTHER": "other"
    }
    return lang_map.get(label, "other")  # default to "other" if unknown

def parse_dataset_03(filepath):
    parsed_data = []
    sentence = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == "":
                if sentence:
                    full_text = " ".join([token for token, _, _ in sentence])
                    entry = {
                        "id": f"ds3_{str(len(parsed_data)+1).zfill(6)}",
                        "text": full_text,
                        "tokens": [token for token, _, _ in sentence],
                        "labels_unified": [map_label(lang) for _, lang, _ in sentence],
                        "langs": [lang for _, lang, _ in sentence],
                        "labels": [label for _, _, label in sentence],

                    }
                    parsed_data.append(entry)
                    sentence = []
            else:
                parts = line.split('\t')
                if len(parts) == 3:
                    token, lang, label = parts
                    sentence.append((token, lang, label))
                else:
                    raise ValueError(f"Unexpected line format: {line}")
        # handle last sentence if file doesn't end with newline
        if sentence:
            full_text = " ".join([token for token, _, _ in sentence])
            entry = {
                "id": f"ds3_{str(len(parsed_data)+1).zfill(6)}",
                "text": full_text,
                "tokens": [token for token, _, _ in sentence],
                "labels_unified": [map_label(lang) for _, lang, _ in sentence],
                "langs": [lang for _, lang, _ in sentence],
                "labels": [label for _, _, label in sentence],
            }
            parsed_data.append(entry)
    return parsed_data

if __name__ == "__main__":
    filepath = "../Data/dataset_03.txt"
    parsed_data = parse_dataset_03(filepath)

    print("Sample entries:")
    for entry in parsed_data[:2]:
        print(json.dumps(entry, indent=2, ensure_ascii=False))

    output_path = "../Data/parsed_dataset_03.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in parsed_data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"\n✅ Saved to {output_path}")
