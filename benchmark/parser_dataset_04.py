import json
import re

def map_label(label):
    label = label.lower()
    lang_map = {
        "lang1": "eng",
        "lang2": "spa",
        "en": "eng",
        "english": "eng",
        "es": "spa",
        "spanish": "spa",
        "de": "deu",
        "tr": "tur",
        "hi": "hin",
        "id": "ind",
        "ne": "named_entity",
        "un": "other",
        "other": "other",
        "OTHER": "Other"
    }
    return lang_map.get(label, "other")  # default "other" if unknown

def parse_dataset_04(filepath):
    parsed_data = []
    sentence_tokens = []
    sentence_labels = []
    sentence_labels_unified = []
    sentence_pos = []
    sentence_xpos = []
    sentence_feats = []
    sentence_head = []
    sentence_deprel = []
    sentence_deps = []
    sentence_misc = []

    sent_id = None
    text = None
    sent_counter = 0

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line.startswith("#"):
                if line.startswith("# sent_id"):
                    sent_id = line.split("=", 1)[1].strip()
                elif line.startswith("# text"):
                    text = line.split("=", 1)[1].strip()
                continue

            if line == "":
                if sentence_tokens:
                    sent_counter += 1
                    entry = {
                        "id": f"ds4_{sent_counter:06d}",
                        "text": text,
                        "tokens": sentence_tokens,
                        "labels_unified": sentence_labels_unified,
                        #"sent_id": sent_id,
                        "labels": sentence_labels,
                        #"pos": sentence_pos,
                        #"xpos": sentence_xpos,
                        #"feats": sentence_feats,
                        #"head": sentence_head,
                        #"deprel": sentence_deprel,
                        #"deps": sentence_deps,
                        #"misc": sentence_misc
                    }
                    parsed_data.append(entry)

                    # reset all for next sentence
                    sentence_tokens = []
                    sentence_labels = []
                    sentence_labels_unified = []
                    sentence_pos = []
                    sentence_xpos = []
                    sentence_feats = []
                    sentence_head = []
                    sentence_deprel = []
                    sentence_deps = []
                    sentence_misc = []
                    sent_id = None
                    text = None
                continue

            parts = line.split("\t")
            if len(parts) != 10:
                # skip multi-word tokens and malformed lines
                continue

            token_id, form, lemma, upos, xpos, feats, head, deprel, deps, misc = parts

            # Extract CSID label from MISC field: "CSID=TR|Lang=tr|..."
            csid_match = re.search(r"CSID=([A-Za-z]+)", misc)
            label = csid_match.group(1).lower() if csid_match else "other"

            # Map label to unified label
            label_unified = map_label(label)

            # Append token info
            sentence_tokens.append(form)
            sentence_labels.append(label)
            sentence_labels_unified.append(label_unified)
            sentence_pos.append(upos)
            sentence_xpos.append(xpos)
            sentence_feats.append(feats)
            sentence_head.append(head)
            sentence_deprel.append(deprel)
            sentence_deps.append(deps)
            sentence_misc.append(misc)

        # Handle last sentence if no trailing newline
        if sentence_tokens:
            sent_counter += 1
            entry = {
                "id": f"ds4_{sent_counter:06d}",
                "text": text,
                "tokens": sentence_tokens,
                "labels_unified": sentence_labels_unified,
                "sent_id": sent_id,
                "labels": sentence_labels,
                "pos": sentence_pos,
                "xpos": sentence_xpos,
                "feats": sentence_feats,
                "head": sentence_head,
                "deprel": sentence_deprel,
                "deps": sentence_deps,
                "misc": sentence_misc
            }
            parsed_data.append(entry)

    return parsed_data

if __name__ == "__main__":
    filepath = "/Users/faisal/PycharmProjects/PythonProject/Praktikum/Data/dataset_04.conllu"
    parsed_data = parse_dataset_04(filepath)

    print("Sample entries:")
    for entry in parsed_data[:2]:
        print(json.dumps(entry, indent=2, ensure_ascii=False))

    output_path = "/Users/faisal/PycharmProjects/PythonProject/Praktikum/Data/parsed_dataset_04.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in parsed_data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"\n✅ Saved to {output_path}")
