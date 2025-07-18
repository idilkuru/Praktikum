import os

# Make PROMPT_DIR absolute relative to this file's location
PROMPT_DIR = os.path.join(os.path.dirname(__file__), "prompts")
prompt_id = 9  # same ID you use in your config

test_input_data = {
    "tokens": ["Hello", "world"],
    "glotlid_context": "- eng (confidence: 0.95)\n- spa (confidence: 0.03)",
    "text": "Hello world",
    "few_shot_block": "",
    "lang_composition": ""
}

prompt_files = sorted(os.listdir(PROMPT_DIR))
selected_file = prompt_files[prompt_id]
prompt_path = os.path.join(PROMPT_DIR, selected_file)

with open(prompt_path, "r", encoding="utf-8") as f:
    template = f.read()

print("Prompt file:", selected_file)
print("Rendered prompt:\n")
print(template.format(**test_input_data))
