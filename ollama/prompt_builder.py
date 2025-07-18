
import os

PROMPT_DIR = os.path.join(os.path.dirname(__file__), "prompts")

def build_prompt(input_data, prompt_id: int, lang_composition: dict = None, few_shot_block: str = "") -> str:
    """
    Loads the prompt template from the prompts folder using the prompt_id.
    Replaces placeholders like {text} or {masklid_predictions} depending on the prompt.
    """
    if not os.path.exists(PROMPT_DIR):
        raise FileNotFoundError(f"Prompt directory does not exist: {PROMPT_DIR}")

    prompt_files = sorted(os.listdir(PROMPT_DIR))
    try:
        selected_file = prompt_files[prompt_id]
    except IndexError:
        raise ValueError(f"Prompt ID {prompt_id} is out of range. Found only {len(prompt_files)} prompts.")

    prompt_path = os.path.join(PROMPT_DIR, selected_file)

    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()

    if lang_composition:
        lang_comp_str = ", ".join(
            f"{k}: {v:.1f}%" if isinstance(v, float) else f"{k}: {v}%" for k, v in lang_composition.items())
    else:
        lang_comp_str = ""

    if isinstance(input_data, dict):
        format_vars = dict(input_data)
        format_vars.setdefault("text", "")  # if text not present
        format_vars.setdefault("tokens", "")
        format_vars.setdefault("candidates", "")
        format_vars.setdefault("glotlid_context", "")
        format_vars["lang_composition"] = lang_comp_str
        format_vars["few_shot_block"] = few_shot_block  # empty string by default
        return template.format(**format_vars)

    else:
        if isinstance(input_data, list):
            tokens_str = "[" + ", ".join(f'"{t}"' for t in input_data) + "]"
        else:
            tokens_str = input_data

        return template.format(
            text=tokens_str,
            tokens=tokens_str,
            lang_composition=lang_comp_str,
            few_shot_block=few_shot_block,
        )