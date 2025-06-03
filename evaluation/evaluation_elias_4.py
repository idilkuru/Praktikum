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

    for entry in data:
        b_tokens = entry.get("tokens", [])
        p_tokens = entry.get("predicted_tokens", b_tokens)  # fallback to benchmark tokens if missing
        b_langs = entry.get("labels_unified", [])
        p_langs = entry.get("predicted_labels", [])

        total_b_tokens += len(b_tokens)
        total_p_tokens += len(p_tokens)

        sm = difflib.SequenceMatcher(None, b_tokens, p_tokens)
        for b_idx, p_idx, size in sm.get_matching_blocks():
            for i in range(size):
                if b_idx + i < len(b_langs) and p_idx + i < len(p_langs):
                    benchmark_labels.append(b_langs[b_idx + i])
                    predicted_labels.append(p_langs[p_idx + i])
                    total_aligned += 1

    # --- Accuracy ---
    accuracy = accuracy_score(benchmark_labels, predicted_labels)
    print("\n--- Overall Accuracy ---")
    print(f"Accuracy: {accuracy:.2f}")

    # --- Per-language Accuracy ---
    print("\n--- Per-Language Accuracy ---")
    correct_per_label = defaultdict(int)
    total_per_label = Counter(benchmark_labels)

    for b, p in zip(benchmark_labels, predicted_labels):
        if b == p:
            correct_per_label[b] += 1

    labels = sorted(total_per_label.keys())
    for label in labels:
        total = total_per_label[label]
        correct = correct_per_label[label]
        acc = correct / total if total > 0 else 0
        print(f"{label:>12}: {acc:.2f} ({correct}/{total})")

    # --- Token Alignment ---
    total_possible = max(total_b_tokens, total_p_tokens)
    token_alignment_rate = total_aligned / total_possible if total_possible > 0 else 0
    print("\n--- Token Alignment Summary ---")
    print(f"Aligned Tokens: {total_aligned}")
    print(f"Total Benchmark Tokens: {total_b_tokens}")
    print(f"Total Prediction Tokens: {total_p_tokens}")
    print(f"Token Alignment Rate: {token_alignment_rate:.2%}")

    # --- Classification Report ---
    print("\n--- Classification Report ---")
    print(classification_report(
        benchmark_labels, predicted_labels,
        digits=2, zero_division=0
    ))

    # --- Language Coverage ---
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
