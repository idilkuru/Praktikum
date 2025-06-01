import json

input_file = "/Users/faisal/PycharmProjects/PythonProject/Praktikum/Data/merged_dataset.jsonl"
# Output file in CoNLL format
output_file = "/Users/faisal/PycharmProjects/PythonProject/Praktikum/Data/merged_dataset.conll"

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        data = json.loads(line)
        tokens = data["tokens"]
        labels = data["labels_unified"]

        # Write each token and its corresponding label
        for token, label in zip(tokens, labels):
            outfile.write(f"{token}\t{label}\n")
        # Separate sentences with a blank line
        outfile.write("\n")

print(f"Conversion complete. CoNLL format saved to '{output_file}'")