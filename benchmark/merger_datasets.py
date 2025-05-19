import json

def load_jsonl(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def merge_datasets(datasets):
    merged = []
    for dataset in datasets:
        merged.extend(dataset)
    return merged

if __name__ == "__main__":
    # Paths to your parsed dataset jsonl files
    paths = [
        "/Users/eliasmac/PycharmProjects/Praktikum/Data/parsed_dataset_01.jsonl",
        "/Users/eliasmac/PycharmProjects/Praktikum/Data/parsed_dataset_02.jsonl",
        "/Users/eliasmac/PycharmProjects/Praktikum/Data/parsed_dataset_03.jsonl",
        "/Users/eliasmac/PycharmProjects/Praktikum/Data/parsed_dataset_04.jsonl",
    ]

    # Load all datasets
    all_datasets = [load_jsonl(p) for p in paths]

    # Merge them
    merged_dataset = merge_datasets(all_datasets)

    # Save merged dataset
    output_path = "/Users/eliasmac/PycharmProjects/Praktikum/Data/merged_dataset.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in merged_dataset:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"\n✅ Merged dataset saved to {output_path}")
