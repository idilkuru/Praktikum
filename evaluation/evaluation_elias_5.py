import json
import difflib
from collections import defaultdict, Counter
from sklearn.metrics import classification_report, accuracy_score

# File path (single file with both benchmark and prediction)
data_path = "../Data/masklid_merged_dataset_100.jsonl"

def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def evaluate_code_switching(data):
    benchmark_labels = []
    predicted_labels = []
    total_aligned = 0
    total_b_tokens = 0
    total_p_tokens = 0

    exact_match_count = 0
    total_sequences = len(data)

    fp_per_label = defaultdict(int)
    tp_per_label = defaultdict(int)
    fn_per_label = defaultdict(int)
    total_per_label = Counter()

    # For accuracy per dataset prefix
    per_dataset_benchmark = defaultdict(list)
    per_dataset_predicted = defaultdict(list)

    for entry in data:
        b_tokens = entry.get("tokens", [])
        p_tokens = entry.get("predicted_tokens", b_tokens)
        b_langs = entry.get("labels_unified", [])
        p_langs = entry.get("predicted_labels", [])

        total_b_tokens += len(b_tokens)
        total_p_tokens += len(p_tokens)

        sm = difflib.SequenceMatcher(None, b_tokens, p_tokens)
        aligned_b = []
        aligned_p = []

        for b_idx, p_idx, size in sm.get_matching_blocks():
            for i in range(size):
                if b_idx + i < len(b_langs) and p_idx + i < len(p_langs):
                    benchmark_labels.append(b_langs[b_idx + i])
                    predicted_labels.append(p_langs[p_idx + i])
                    aligned_b.append(b_langs[b_idx + i])
                    aligned_p.append(p_langs[p_idx + i])
                    total_aligned += 1

        # Exact match check for this sequence (all tokens aligned and equal)
        if aligned_b == aligned_p and len(aligned_b) == len(b_langs):
            exact_match_count += 1

        # FP, TP, FN counts per label
        for b_label, p_label in zip(aligned_b, aligned_p):
            total_per_label[b_label] += 1
            if b_label == p_label:
                tp_per_label[b_label] += 1
            else:
                fp_per_label[p_label] += 1
                fn_per_label[b_label] += 1

        # Accuracy per dataset prefix (based on entry id)
        entry_id = entry.get("id", "unknown")
        prefix = entry_id.split("_")[0] if "_" in entry_id else "unknown"
        per_dataset_benchmark[prefix].extend(aligned_b)
        per_dataset_predicted[prefix].extend(aligned_p)

    # Overall accuracy
    accuracy = accuracy_score(benchmark_labels, predicted_labels)

    print("\n--- Overall Accuracy ---")
    print(f"Accuracy: {accuracy:.4f}")

    # Accuracy per dataset prefix
    print("\n--- Accuracy per Benchmark Dataset Prefix ---")
    for prefix in sorted(per_dataset_benchmark.keys()):
        b_labels = per_dataset_benchmark[prefix]
        p_labels = per_dataset_predicted[prefix]
        if b_labels and p_labels:
            acc = accuracy_score(b_labels, p_labels)
            print(f"{prefix:>8}: {acc:.4f} ({len(b_labels)} tokens)")
        else:
            print(f"{prefix:>8}: No data")

    # Accuracy dropping 'other' and 'named_entity'
    print("\n--- Accuracy Dropping 'other' and 'named_entity' ---")
    filtered_benchmark = []
    filtered_predicted = []
    for b, p in zip(benchmark_labels, predicted_labels):
        if b not in ("other", "named_entity"):
            filtered_benchmark.append(b)
            filtered_predicted.append(p)
    acc_filtered = accuracy_score(filtered_benchmark, filtered_predicted) if filtered_benchmark else 0.0
    print(f"Accuracy without 'other' and 'named_entity': {acc_filtered:.4f} ({len(filtered_benchmark)} tokens)")

    # Exact match ratio
    print("\n--- Exact Match ---")
    print(f"Exact match sequences: {exact_match_count} / {total_sequences} = {exact_match_count / total_sequences:.2%}")

    # False Positives per label
    print("\n--- False Positives per Label ---")
    labels = sorted(total_per_label.keys())
    for label in labels:
        fp = fp_per_label.get(label, 0)
        print(f"{label:>12}: FP = {fp}")

    # Classification Report
    print("\n--- Classification Report ---")
    print(classification_report(benchmark_labels, predicted_labels, digits=4, zero_division=0))

    # Token Alignment Summary
    total_possible = max(total_b_tokens, total_p_tokens)
    token_alignment_rate = total_aligned / total_possible if total_possible > 0 else 0
    print("\n--- Token Alignment Summary ---")
    print(f"Aligned Tokens: {total_aligned}")
    print(f"Total Benchmark Tokens: {total_b_tokens}")
    print(f"Total Prediction Tokens: {total_p_tokens}")
    print(f"Token Alignment Rate: {token_alignment_rate:.2%}")

    # Language Coverage
    benchmark_langs = set(label for x in data for label in x.get("labels_unified", []))
    predicted_langs = set(label for x in data for label in x.get("predicted_labels", []))

    common = benchmark_langs & predicted_langs
    missed = benchmark_langs - predicted_langs
    hallucinated = predicted_langs - benchmark_langs

    print("\n--- Language Coverage ---")
    print("Languages in both benchmark & prediction:")
    print("  " + ", ".join(sorted(common)) if common else "  None")
    print("Languages missed (in benchmark but not in prediction):")
    print("  " + ", ".join(sorted(missed)) if missed else "  None")
    print("Languages hallucinated (in prediction but not in benchmark):")
    print("  " + ", ".join(sorted(hallucinated)) if hallucinated else "  None")


if __name__ == "__main__":
    data = load_jsonl(data_path)
    evaluate_code_switching(data)
