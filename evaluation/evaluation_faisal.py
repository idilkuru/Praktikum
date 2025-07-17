import json
import sys
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd

def evaluate(jsonl_path):
    y_true = []
    y_pred = []
    total_tokens = 0
    correct_tokens = 0

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            true_labels = item.get("labels_unified", [])
            pred_labels = item.get("predicted_labels", [])

            if len(true_labels) != len(pred_labels):
                continue

            for t, p in zip(true_labels, pred_labels):
                y_true.append(t)
                y_pred.append(p)
                total_tokens += 1
                if t == p:
                    correct_tokens += 1

    print(f"Total tokens evaluated: {total_tokens}")
    exact_match = correct_tokens / total_tokens if total_tokens else 0.0
    print(f"Token-level Exact Match Accuracy: {exact_match:.3f}\n")

    print("Classification Report:\n")
    print(classification_report(y_true, y_pred, digits=3))

    labels = sorted(list(set(y_true + y_pred)))
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    print("\nConfusion Matrix:")
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    print(cm_df)

    print("\nFalse Positive Rate (per class):")
    for i, label in enumerate(labels):
        FP = sum(cm[:, i]) - cm[i, i]
        TN = cm.sum() - (sum(cm[i, :]) + sum(cm[:, i]) - cm[i, i])
        fpr = FP / (FP + TN) if (FP + TN) > 0 else 0.0
        print(f"{label}: {fpr:.3f}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_predictions.py path/to/data.jsonl")
        sys.exit(1)

    evaluate(sys.argv[1])