# Builds the prompt using templates and input data

import os

PROMPT_DIR = "../Praktikum/ollama/prompts"

def build_prompt(input_data, prompt_id: int) -> str:
    """
    Loads the prompt template from the prompts folder using the prompt_id.
    Replaces placeholders like {text} or {masklid_predictions} depending on the prompt.
    """
    prompt_files = sorted(os.listdir(PROMPT_DIR))
    try:
        selected_file = prompt_files[prompt_id]
    except IndexError:
        raise ValueError(f"Prompt ID {prompt_id} is out of range. Found only {len(prompt_files)} prompts.")

    prompt_path = os.path.join(PROMPT_DIR, selected_file)

    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Safely apply formatting
    if isinstance(input_data, dict):
        return template.format(**input_data)
    else:
        return template.format(text=input_data)
