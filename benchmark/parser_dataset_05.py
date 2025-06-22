import json

def parse_dataset_05(filepath):
    parsed_data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        sentence = []
        for line in file:
            line = line.strip()
            if line.startswith('#') or line == "":
                if sentence:
                    full_text = " ".join([token for token, _ in sentence])
                    entry = {
                        "id": f"ds5_{str(len(parsed_data)+1).zfill(6)}",
                        "text": full_text,
                        "tokens": [token for token, _ in sentence],
                        "labels_unified": [map_label(label) for _, label in sentence],
                        "labels": [label for _, label in sentence],
                        "source": "LinCE (msa-ea)"
                    }
                    parsed_data.append(entry)
                    sentence = []
                continue
            parts = line.split('\t')
            if len(parts) == 2:
                token, label = parts
                sentence.append((token, label))
        # handle last sentence
        if sentence:
            full_text = " ".join([token for token, _ in sentence])
            entry = {
                #"id": f"ds2_{str(len(parsed_data)+1).zfill(6)}",
                "id": f"ds5_{str(len(parsed_data) + 1).zfill(6)}",
                "text": full_text,
                "tokens": [token for token, _ in sentence],
                "labels_unified": [map_label(label) for _, label in sentence],
                "labels": [label for _, label in sentence],
                "source": "LinCE (msa-ea)"
            }
            parsed_data.append(entry)
    return parsed_data

def map_label(label):
    label = label.lower()
    lang_map = {
        "lang1": "arb",
        "lang2": "arz",
        "ne": "other",
        "other": "other",
        "un": "other"
    }
    return lang_map.get(label, "other")

if __name__ == "__main__":
    filepath = "../Data/dataset_05.conll"
    parsed_data = parse_dataset_05(filepath)

    print("Sample entries:")
    for entry in parsed_data[:2]:
        print(json.dumps(entry, indent=2, ensure_ascii=False))

    output_path = "../Data/parsed_dataset_05.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in parsed_data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"\n Saved to {output_path}")
