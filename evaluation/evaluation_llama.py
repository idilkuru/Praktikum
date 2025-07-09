from sklearn.metrics import precision_recall_fscore_support, accuracy_score, matthews_corrcoef, hamming_loss
from collections import Counter
import json

# Loading original benchmark file (ground truth)
with open("../Data/merged_dataset_1800.jsonl", "r", encoding="utf-8") as f:
    gold_data = {entry["id"]: entry for entry in map(json.loads, f)}

# Loading predictions file
with open("../Data/9_groq_r1_merged_dataset_1800.jsonl", "r", encoding="utf-8") as f:
    pred_data = [json.loads(line) for line in f]

gold_labels = []
pred_labels = []
included_labels = []
mismatch_ids = []

# For exact match
exact_match_ids = []
total_included_sequences = 0
exact_match_count = 0

# Temp store to check exact match later
exact_match_candidates = []

# Process and normalize labels
for pred_entry in pred_data:
    id_ = pred_entry["id"]

    if id_ not in gold_data:
        continue  # skip unmatched predictions

    gold_entry = gold_data[id_]

    # Normalize gold labels
    gold = [l if l != "named_entity" else "other" for l in gold_entry["labels_unified"]]
    # Normalize predicted labels
    pred = [l if l == "oth" else l for l in pred_entry["llama_labels"]]
    pred = [l if l != "id" else "ind" for l in pred]
    pred = [l if l != "idn" else "ind" for l in pred]
    pred = [l if l != "ids" else "ind" for l in pred]
    pred = [l if l != "esp" else "spa" for l in pred]
    pred = [l if l != "hind" else "hin" for l in pred]
    pred = [l if l != "hnd" else "hin" for l in pred]
    pred = [l if l != "hi" else "hin" for l in pred]
    pred = [l if l != "hne" else "hin" for l in pred]
    pred = [l if l != "germ" else "deu" for l in pred]
    pred = [l if l != "arab" else "arb" for l in pred]
    pred = [l if l != "ara" else "arb" for l in pred]
    pred = [l if l != "arabic" else "arb" for l in pred]
    pred = [l if l != "turk" else "tur" for l in pred]
    pred = [l if l != "npi" else "nep" for l in pred]
    pred = [l if l != "oth" else "other" for l in pred]

    # ✂️ Handle mismatch: truncate to shortest length
    if len(gold) != len(pred):
        mismatch_ids.append((id_, len(gold), len(pred)))
        min_len = min(len(gold), len(pred))
        gold = gold[:min_len]
        pred = pred[:min_len]

    gold_labels.extend(gold)
    pred_labels.extend(pred)

    # Store per-sample for exact match calculation
    exact_match_candidates.append((id_, gold, pred))

# Report mismatches
if mismatch_ids:
    print("\nMismatched token counts:")
    for mid, g_len, p_len in mismatch_ids:
        print(f"Length mismatch for ID {mid}: gold={g_len}, pred={p_len}")

# Get unique label set
label_set = sorted(set(gold_labels + pred_labels))

# Compute metrics
precision, recall, f1, support = precision_recall_fscore_support(
    gold_labels, pred_labels, labels=label_set, zero_division=0
)

# Filter labels with support > 0
results = []
included_labels = []
for l, p, r, f, s in zip(label_set, precision, recall, f1, support):
    if s > 0:
        results.append((l, round(p, 3), round(r, 3), round(f, 3), s))
        included_labels.append(l)

# Print table
print("\nLabel\tPrecision\tRecall\tF1\tSupport")
for row in results:
    print(f"{row[0]}\t{row[1]}\t\t{row[2]}\t\t{row[3]}\t{row[4]}")

# Overall accuracy (based only on included labels)
# Filter out any labels not in included_labels
filtered_gold = [g for g, p in zip(gold_labels, pred_labels) if g in included_labels]
filtered_pred = [p for g, p in zip(gold_labels, pred_labels) if g in included_labels]

accuracy = accuracy_score(filtered_gold, filtered_pred)
print(f"\nOverall Accuracy (all labels): {round(accuracy, 3)}")

# Compute false positive rate (included labels only)
false_positives = 0
total_pred_tokens = 0

for g_label, p_label in zip(gold_labels, pred_labels):
    if p_label in included_labels:
        total_pred_tokens += 1
        if p_label != g_label:
            false_positives += 1

false_positive_rate = false_positives / total_pred_tokens if total_pred_tokens > 0 else 0
print(f"\nFalse Positive Rate (all labels): {false_positive_rate:.3f}")

# Compute exact match (included labels only)
for id_, gold_seq, pred_seq in exact_match_candidates:
    filtered_gold = [g for g in gold_seq if g in included_labels]
    filtered_pred = [p for i, p in enumerate(pred_seq) if gold_seq[i] in included_labels]

    if filtered_gold == filtered_pred:
        exact_match_count += 1
    total_included_sequences += 1


# Computing Matthews Correlation Coefficient (MCC)
mcc = matthews_corrcoef(gold_labels, pred_labels)
print(f"Matthews Correlation Coefficient (MCC): {round(mcc, 3)}")

hamming = hamming_loss(gold_labels, pred_labels)
print(f"Hamming Loss: {round(hamming, 3)}")

exact_match_accuracy = exact_match_count / total_included_sequences if total_included_sequences > 0 else 0
print(f"Exact Match Accuracy (all labels): {exact_match_accuracy:.3f}")
