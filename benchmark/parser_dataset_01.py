import json

def parse_dataset_01(filepath):
    parsed_data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        sentence = []
        for line in file:
            line = line.strip()
            if line.startswith('#') or line == "":
                if sentence:
                    full_text = " ".join([token for token, _ in sentence])
                    entry = {
                        "id": f"ds1_{str(len(parsed_data)+1).zfill(6)}",
                        "text": full_text,
                        "tokens": [token for token, _ in sentence],
                        "labels_unified": [map_label(label) for _, label in sentence],  # moved here
                        "labels": [label for _, label in sentence],# moved after labels_unified
                        "source": "LinCE (spa-eng)"
                    }
                    parsed_data.append(entry)
                    sentence = []
                continue
            parts = line.split()
            if len(parts) == 2:
                token, label = parts
                sentence.append((token, label))
        # handle last sentence if file doesn't end with newline
        if sentence:
            full_text = " ".join([token for token, _ in sentence])
            entry = {
                "id": f"ds1_{str(len(parsed_data)+1).zfill(6)}",
                "text": full_text,
                "tokens": [token for token, _ in sentence],
                "labels_unified": [map_label(label) for _, label in sentence],  # moved here
                "labels": [label for _, label in sentence],                      # moved after labels_unified
                "source": "LinCE (spa-eng)"
            }
            parsed_data.append(entry)
    return parsed_data


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
    return lang_map.get(label, "other")  # default to "other" if unknown

# 🔽 Insert this block at the end to run and save the result
if __name__ == "__main__":
    # ⬅️ Use your correct path here
    filepath = "/Users/faisal/PycharmProjects/PythonProject/Praktikum/Data/dataset_01.conll"
    parsed_data = parse_dataset_01(filepath)

    # Show a few examples to check
    print("Sample entries:")
    for entry in parsed_data[:2]:
        print(json.dumps(entry, indent=2, ensure_ascii=False))

    # Save as JSONL
    output_path = "/Users/faisal/PycharmProjects/PythonProject/Praktikum/Data/parsed_dataset_01.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in parsed_data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"\n✅ Saved to {output_path}")
