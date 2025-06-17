# Responsible for creating different input variations from the data

import spacy

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from methodology.ollama_masklid_run import run_masklid


def build_input_raw_text(entry):
    """Return raw text only."""
    return entry["text"]


nlp = spacy.load("en_core_web_sm")
def build_input_tokenized(entry):
    """Use spaCy to tokenize the text and return list of tokens."""
    doc = nlp(entry["text"])
    tokens = [token.text for token in doc]
    print(f"[DEBUG] Tokenized input: {tokens}")  # Add this line
    return " ".join(tokens)  # returns string for prompt injection

def build_input_dominant_lang(entry):
    """Return text with dominant language label (to be implemented)."""
    return f"[lang=??] {entry['text']}"


def build_input_token_lid(entry):
    """Use MaskLID to get token-language segments for LLM input."""
    # Original text
    text = entry["text"]

    # MaskLID predictions
    label_map = run_masklid(text)

    # Pretty-print predictions (as string) for the prompt
    prediction_lines = []
    for label, segment in label_map.items():
        lang_code = label.replace("__label__", "")[:3]  # trim to ISO-639-3
        tokens = segment.strip().split()
        for token in tokens:
            prediction_lines.append(f"{token}: {lang_code}")

    masklid_predictions = "\n".join(prediction_lines)

    return {
        "text": text,
        "masklid_predictions": masklid_predictions
    }


    """""
    text = entry["text"]
    result = run_masklid(text)

    # Debug: show MaskLID segments
    print(f"[DEBUG] MaskLID result for text:\n{text}")
    for lang, seg in result.items():
        print(f"  {lang}: {seg}")

    # Format for LLM prompt
    segments = [f"{lang}: {seg}" for lang, seg in result.items()]
    return "\n".join(segments)
    """""

