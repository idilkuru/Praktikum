import json
import argparse
import random


def strip_jsonl(input_file, output_file, sample_size=5000):
    valid_lines = []

    # Read and filter valid lines
    with open(input_file, "r", encoding="utf-8") as infile:
        for line in infile:
            try:
                obj = json.loads(line)
                if all(k in obj for k in ("id", "text", "labels")):
                    minimal_obj = {
                        "id": obj["id"],
                        "text": obj["text"],
                        "labels": obj["labels"]
                    }
                    valid_lines.append(minimal_obj)
                else:
                    print(f"Skipping line due to missing keys: {obj}")
            except Exception as e:
                print(f"Skipping line due to error: {e}")

    # Randomly sample
    sample_size = min(sample_size, len(valid_lines))
    sampled_lines = random.sample(valid_lines, sample_size)

    # Write to output
    with open(output_file, "w", encoding="utf-8") as outfile:
        for obj in sampled_lines:
            outfile.write(json.dumps(obj, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input JSONL file")
    parser.add_argument("--output", required=True, help="Output JSONL file with only id, text, and labels")
    parser.add_argument("--sample_size", type=int, default=5000, help="Number of lines to sample (default: 5000)")
    args = parser.parse_args()

    strip_jsonl(args.input, args.output, sample_size=args.sample_size)