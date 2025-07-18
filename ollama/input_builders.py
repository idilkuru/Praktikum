# Responsible for creating different input variations from the data

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



def build_input_raw_text(entry):
    """Return raw text only."""
    return entry["text"]

def build_input_raw_tokens(entry):
    """Return raw tokens only."""
    return entry["tokens"]


def build_input_tokenized(entry):
    import spacy
    nlp = spacy.load("en_core_web_sm")

    """Tokenize text using spaCy and return it as a dict with 'tokens' key."""
    doc = nlp(entry["text"])
    tokens = [token.text for token in doc]
    token_str = " ".join(tokens)  # or "\n".join(tokens) if your prompt prefers line breaks
    return {"tokens": token_str}

def build_input_dominant_lang(entry):
    """Return text with dominant language label (to be implemented)."""
    return f"[lang=??] {entry['text']}"



def build_input_token_lid(entry):
    from methodology.ollama_masklid_run import run_masklid

    """Use MaskLID to get token-language segments for LLM input."""
    # Original text
    text = entry["text"]

    # MaskLID predictions
    label_map = run_masklid(text)

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



def build_input_fasttext_lid(entry):
    import fasttext
    from pathlib import Path

    FASTTEXT_MODEL_PATH = Path(__file__).parent.parent / "models" / "lid.176.bin"
    fasttext_model = fasttext.load_model(str(FASTTEXT_MODEL_PATH))

    return entry["text"]


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


def build_input_panlex_api(entry):
    from panlex.panlex_utils import get_panlex_candidates_api

    tokens = build_input_raw_tokens(entry)

    lines = []
    for tok in tokens:
        # Skip short tokens (e.g. punctuation or stopwords)
        #if len(tok) < 3:
        #    continue

        langs = get_panlex_candidates_api(tok)          # Use PanLex API

        langs_str = ", ".join(langs) if langs else ""
        lines.append(f"{tok}: {langs_str}")

    candidates = "\n".join(lines)

    return {
        "tokens": tokens,
        "candidates": candidates,
    }

def build_input_panlex_offline(entry):
    from panlex.panlex_utils import get_panlex_candidates_offline

    tokens = build_input_raw_tokens(entry)

    lines = []
    for tok in tokens:

        langs = get_panlex_candidates_offline(tok)    # Use local PanLex CSV

        langs_str = ", ".join(langs) if langs else ""
        lines.append(f"{tok}: {langs_str}")

    candidates = "\n".join(lines)

    return {
        "tokens": tokens,
        "candidates": candidates,
    }

from GlotLID.glotlid_processor import GlotLIDProcessor
from prompt_builder import build_prompt
from config import CONFIG

def build_input_glotlid(entry):
    processor = GlotLIDProcessor()
    lang_info = processor.detect_language(entry["text"])
    top_langs = lang_info.get("languages", [])

    if top_langs:
        glotlid_context = "\n".join([
            f"- {item['language'].split('_')[0]} (confidence: {item['confidence']:.2f})"
            for item in top_langs
        ])
    else:
        glotlid_context = "No reliable language prediction available."

    tokens = entry["tokens"]

    return {
        "tokens": tokens,
        "text": entry["text"],
        "glotlid_context": glotlid_context,
    }


