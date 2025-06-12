import json
import hashlib
import os
import ast
from pathlib import Path
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import AutoTokenizer
import torch
import nltk
import time
#nltk.download('punkt_tab')
#nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize
import sys
sys.path.insert(0, "/Users/faisal/PycharmProjects/PythonProject/olmo")
from hf_olmo import OLMoForCausalLM, OLMoTokenizerFast
import fasttext


# Loading FastText LID model
lang_model = fasttext.load_model("lid.176.bin")
LANG_MAP = {
    "en": "English", "ar": "Arabic", "fr": "French", "es": "Spanish", "de": "German", "tr": "Turkish",
    "hi": "Hindi", "id": "Indonesian","ne": "Nepali", "yo": "Yoruba","ha": "Hausa", "ff": "Fula", "pcm": "Nigerian Pidgin"
}

# Loading OLMo

#model = OLMoForCausalLM.from_pretrained("allenai/OLMo-2-0425-1B-Instruct").to(device)
#tokenizer = OLMoTokenizerFast.from_pretrained("allenai/OLMo-2-0425-1B-Instruct")

device = torch.device("cpu")
# Model ID for OLMo 1B Instruct
model_id = "allenai/OLMo-2-0425-1B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id).to(device)


# Caching setup
CACHE_DIR = Path(".olmo_cache")
CACHE_DIR.mkdir(exist_ok=True)

def tokenize(text):
    return word_tokenize(text, language="english")

#tokenizer_hf = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
'''
def tokenize(text):
    tokens = tokenizer_hf.tokenize(text)
    tokens = [t[2:] if t.startswith("##") else t for t in tokens]
    return tokens
'''
def hash_prompt(prompt):
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def get_cached_response(prompt):
    key = hash_prompt(prompt)
    cache_file = CACHE_DIR / f"{key}.txt"
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text())
        except json.JSONDecodeError:
            return None
    return None

def cache_response(prompt, response):
    key = hash_prompt(prompt)
    cache_file = CACHE_DIR / f"{key}.txt"
    if isinstance(response, list):
        response_str = json.dumps(response, ensure_ascii=False)
    else:
        response_str = response
    cache_file.write_text(response_str)


def detect_languages(text):
    langs = set()
    for word in text.split():
        try:
            pred = lang_model.predict(word)[0][0].replace("__label__", "")
            langs.add(pred)
        except:
            continue
    return sorted(langs)

def detect_languages_per_token(tokens):
    labels = []
    for token in tokens:
        try:
            pred = lang_model.predict(token)[0][0].replace("__label__", "")
            labels.append(pred)
        except:
            labels.append("unknown")
    return labels

EXAMPLE_POOL = [
    {
        "tokens": ["أنا", "going", "to", "المدرسة", "now"],
        "labels": ["ar", "en", "en", "ar", "en"]
    },
    {
        "tokens": ["Je", "suis", "very", "fatigué"],
        "labels": ["fr", "fr", "en", "fr"]
    },
]

def render_few_shot_examples(possible_langs):
    examples = []
    for ex in EXAMPLE_POOL:
        if any(label in possible_langs for label in ex["labels"]):
            examples.append(f"Tokens:\n{ex['tokens']}\nOutput:\n{ex['labels']}\n")
    return "\n".join(examples[:3])

'''
def render_few_shot_examples(possible_langs):
    examples = []
    for ex in EXAMPLE_POOL:
        if any(label in possible_langs for label in ex["labels"]):
            tokens_str = "[" + ", ".join(f"'{tok}'" for tok in ex["tokens"]) + "]"
            #fasttext_str = "[" + ", ".join(f"'{lang}'" for lang in ex["fasttext"]) + "]"
            labels_str = "[" + ", ".join(f"'{label}'" for label in ex["labels"]) + "]"
            examples.append(
                f"Tokens:\n{tokens_str}\nFastText Predictions:\n{fasttext_str}\nOutput:\n{labels_str}\n"
            )
    return "\n".join(examples[:2])  # limit to 2 examples max
'''
def create_prompt(tokens, fasttext_tags):
    base = (
        "You are a linguistic model trained to identify the language of individual tokens in code-switched tweets.\n"
        "A code-switched tweet contains words from multiple languages, often mixed in one sentence.\n\n"
        "Task:\n"
        "Given a list of tokens from a tweet, and FastText's prediction of the language for each token,\n"
        "output a list of ISO 639-1 language codes identifying the true language of each token.\n"
        "Your output must be a Python-style list of strings with **exactly one language code per token** in the same order. The length of the output list must match the number of tokens.\n"
        "Only output the list for the final task. Do not generate any new tasks."

    )

    possible_langs = sorted(set(fasttext_tags))
    context = ""
    if possible_langs:
        lang_names = [LANG_MAP.get(code, code) for code in possible_langs]
        context = f"Context: This tweet likely contains {', '.join(lang_names)}.\n\n"

    few_shot = render_few_shot_examples(possible_langs)

    token_str = "[" + ", ".join(f"'{tok}'" for tok in tokens) + "]"
    fasttext_str = "[" + ", ".join(f"'{lang}'" for lang in fasttext_tags) + "]"

    task = f"--- NEW TASK ---\nTokens:\n{token_str}\nFastText Predictions:\n{fasttext_str}\nOutput:\n"

    return base + context + few_shot + "\n" + task

'''
def run_prompt(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    inputs.pop("token_type_ids", None)
    start = time.time()
    print("Calling OLMo generate...")
    try:
        outputs = model.generate(**inputs, max_new_tokens=64)
        print("Done. Took", time.time() - start, "seconds")
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    except Exception as e:
        print("Generation failed:", str(e))
        return ""
'''

def run_prompt(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    inputs.pop("token_type_ids", None)

    print("Calling OLMo generate...")
    start = time.time()

    outputs = model.generate(
        **inputs,
        max_new_tokens=1000,
        do_sample=False,  # deterministic
        eos_token_id=tokenizer.eos_token_id,  # stop at end-of-sequence
    )

    raw_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("Raw model output:", raw_output)
    print("Done. Took", time.time() - start, "seconds")

    # Extract only the new part
    # Remove the prompt from the generated output
    new_part = raw_output[len(prompt):].strip()

    # Now try to parse the new part as a Python list (e.g., ['es', 'fr', 'en'])
    try:
        predicted = eval(new_part.splitlines()[0])
    except Exception as e:
        print("Parsing failed:", e)
        predicted = []

    return predicted


def extract_tags(response):
    try:
        result = response.split("Output:")[-1].strip()
        return ast.literal_eval(result)
    except:
        return []



def process_tweet(tweet_obj):
    print(f"Processing tweet id: {tweet_obj['id']}")  # Debugging

    text = tweet_obj["text"]
    tokens = tokenize(text)
    print(f"Tokens: {tokens}")  # Debugging

    fasttext_tags = detect_languages_per_token(tokens)
    print(f"FastText tags: {fasttext_tags}")  # Debugging

    prompt = create_prompt(tokens, fasttext_tags)
    print(f"Prompt created. Length: {len(prompt)} chars")  # Debugging

    cached = get_cached_response(prompt)
    if cached:
        print("Using cached response.")  # Debugging
        response = cached
    else:
        print("Calling OLMo generate...")  # Debugging

        response = run_prompt(prompt)
        cache_response(prompt, response)

    tags = extract_tags(response)
    print(f"Predicted tags: {tags}")  # Debugging

    return {
        "id": tweet_obj["id"],
        "tokens": tokens,
        "predicted_labels": tags
    }

def main(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
        for line in tqdm(infile, desc="Processing tweets"):
            tweet = json.loads(line)
            result = process_tweet(tweet)
            outfile.write(json.dumps(result, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input JSONL file with 'id' and 'text' fields")
    parser.add_argument("--output", required=True, help="Output JSONL file with language predictions")
    args = parser.parse_args()

    main(args.input, args.output)