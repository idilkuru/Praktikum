import json

def parse_dataset_06(filepath):
    parsed_data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        sentence = []
        for line in file:
            line = line.strip()
            if line.startswith('#') or line == "":
                if sentence:
                    full_text = " ".join([token for token, _ in sentence])
                    entry = {
                        "id": f"ds2_{str(len(parsed_data)+1).zfill(6)}",
                        "text": full_text,
                        "tokens": [token for token, _ in sentence],
                        "labels_unified": [map_label(label) for _, label in sentence],
                        "labels": [label for _, label in sentence],
                        "source": "LinCE (nep-eng)"
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
                "id": f"ds1_{str(len(parsed_data) + 1).zfill(6)}",
                "text": full_text,
                "tokens": [token for token, _ in sentence],
                "labels_unified": [map_label(label) for _, label in sentence],
                "labels": [label for _, label in sentence],
                "source": "LinCE (nep-eng)"
            }
            parsed_data.append(entry)
    return parsed_data

def map_label(label):
    label = label.lower()
    lang_map = {
        "lang1": "eng",
        "lang2": "nep",
        "ne": "named_entity",
        "other": "other",
        "un": "other"
    }
    return lang_map.get(label, "other")

if __name__ == "__main__":
    filepath = "/Users/faisal/PycharmProjects/PythonProject/Praktikum/Data/dataset_06.conll"
    parsed_data = parse_dataset_06(filepath)

    print("Sample entries:")
    for entry in parsed_data[:2]:
        print(json.dumps(entry, indent=2, ensure_ascii=False))

    output_path = "/Users/faisal/PycharmProjects/PythonProject/Praktikum/Data/parsed_dataset_06.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in parsed_data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"\n Saved to {output_path}")