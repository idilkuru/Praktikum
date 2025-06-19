import json

file1_path = "../Data/merged_data_4.jsonl"
file2_path = "../Data/llama3_merged_data_5.jsonl"

# Load file 1 into dict: id -> labels_unified
labels_unified_dict = {}
with open(file1_path, "r", encoding="utf-8") as f1:
    for line in f1:
        data = json.loads(line)
        labels_unified = data.get("labels_unified")
        if labels_unified is not None:
            labels_unified_dict[data["id"]] = labels_unified

# Load file 2 into dict: id -> llama_labels
llama_labels_dict = {}
with open(file2_path, "r", encoding="utf-8") as f2:
    for line in f2:
        data = json.loads(line)
        llama_labels = data.get("llama_labels")
        if llama_labels is not None:
            llama_labels_dict[data["id"]] = llama_labels

# Compare lengths for ids present in both
mismatches = []
for id_ in labels_unified_dict:
    if id_ in llama_labels_dict:
        len_unified = len(labels_unified_dict[id_])
        len_llama = len(llama_labels_dict[id_])
        if len_unified != len_llama:
            mismatches.append({
                "id": id_,
                "labels_unified_len": len_unified,
                "llama_labels_len": len_llama,
            })
    else:
        print(f"Warning: ID {id_} found in file 1 but missing in file 2.")

if mismatches:
    print(f"Found {len(mismatches)} mismatches:")
    for m in mismatches:
        print(m)
else:
    print("✅ All matching IDs have equal lengths of labels_unified and llama_labels.")
