import json
import random
from collections import Counter


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


def has_labels(instance, required_labels):
    labels = instance.get("labels_unified", [])
    return all(label in labels for label in required_labels)


def select_subset(dataset, required_labels=None, percentage=1.0):
    if required_labels:
        matching = [inst for inst in dataset if has_labels(inst, required_labels)]
        non_matching = [inst for inst in dataset if not has_labels(inst, required_labels)]
        target_count = int(len(dataset) * percentage)
        if len(matching) >= target_count:
            selected = random.sample(matching, target_count)
        else:
            selected = matching + random.sample(non_matching, target_count - len(matching))
    else:
        # Random sample from entire dataset
        target_count = int(len(dataset) * percentage)
        selected = random.sample(dataset, target_count)
    return selected


# choose Percentage of dataset to keep in the short version
def merge_custom_datasets(datasets):
    merged = []
    for i, dataset in enumerate(datasets):
        if i == 0:
            # Dataset 01: keep 20% with eng+spa
            subset = select_subset(dataset, ["eng", "spa"], 0.015* 0.50)
            merged.extend(subset)
        elif i == 1:
            # Dataset 02: keep 11% with eng+ind
            subset = select_subset(dataset, ["eng", "ind"], 0.20)
            merged.extend(subset)
        elif i == 3:
            # Dataset 04: keep 11% with tur+deu
            subset = select_subset(dataset, ["tur", "deu"], 0.040* 0.6667)
            merged.extend(subset)
        elif i == 4:
            # Dataset 05: keep 35% with arb+arz
            subset = select_subset(dataset, ["arb", "arz"], 0.033* 0.6667)
            merged.extend(subset)
        elif i == 5:
            # Dataset 06: keep 45% random
            subset = select_subset(dataset, None, 0.033* 0.60)
            merged.extend(subset)
        elif i == 6:
            # Dataset 07: keep 60% random
            subset = select_subset(dataset, None, 0.050* 0.6667)
            merged.extend(subset)
        else:
            # All others: keep full dataset
            merged.extend(dataset)
    return merged


def count_subdatasets(filepath):
    counts = Counter()
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line)
            id_prefix = entry.get("id", "")[:3]  # e.g. 'ds1', 'ds2'
            counts[id_prefix] += 1
    return counts


if __name__ == "__main__":
    paths = [
        "../Data/parsed_dataset_01.jsonl",
        "../Data/parsed_dataset_02.jsonl",
        "../Data/parsed_dataset_03.jsonl",
        "../Data/parsed_dataset_04.jsonl",
        "../Data/parsed_dataset_05.jsonl",
        "../Data/parsed_dataset_06.jsonl",
        "../Data/parsed_dataset_07.jsonl"
    ]

    all_datasets = [load_jsonl(p) for p in paths]

    # Save full merged dataset
    merged_dataset = merge_datasets(all_datasets)
    output_path_full = "../Data/merged_dataset.jsonl"
    with open(output_path_full, "w", encoding="utf-8") as f:
        for entry in merged_dataset:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"✅ Full merged dataset saved to {output_path_full}")

    # Save custom smaller merged dataset
    merged_custom = merge_custom_datasets(all_datasets)
    output_path_custom = "../Data/merged_dataset_1050.jsonl"
    with open(output_path_custom, "w", encoding="utf-8") as f:
        for entry in merged_custom:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"✅ Custom merged dataset saved to {output_path_custom}")

    # Count subdatasets in the custom merged dataset
    counts = count_subdatasets(output_path_custom)
    for ds, count in sorted(counts.items()):
        print(f"{ds}: {count}")

    # Sample 100 random instances from all_data
    sample_100 = random.sample(merged_custom, 100)
    output_path = "../Data/merged_dataset_100.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in sample_100:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"✅ Very short merged dataset saved to {output_path}")