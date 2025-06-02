import json
import sys
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def evaluate(jsonl_path):
    y_true = []
    y_pred = []

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            true_labels = item.get("labels_unified", [])
            pred_labels = item.get("predicted_labels", [])

            # Ensure matching lengths
            if len(true_labels) != len(pred_labels):
                continue

            y_true.extend(true_labels)
            y_pred.extend(pred_labels)

    print(f"Total tokens evaluated: {len(y_true)}\n")

    print("Classification Report:\n")
    print(classification_report(y_true, y_pred, digits=3))

    # --- Confusion Matrix ---
    labels = sorted(list(set(y_true + y_pred)))
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    print("\nConfusion Matrix:")
    print(pd.DataFrame(cm, index=labels, columns=labels))

    # Optional: plot confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=labels, yticklabels=labels, cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate_predictions.py path/to/data.jsonl")
        sys.exit(1)

    evaluate(sys.argv[1])