# Code-Switch Language Detection with LLMs and Heuristic Guidance

This project performs token-level language identification on code-switched social media posts using large language models (LLMs). It integrates heuristic language detection tools (like GlotLID) as soft guidance and supports few-shot prompting for improved accuracy.

---

## 🧠 Key Features

- Token-level language classification for code-switched text
- Modular architecture supporting different input modes (raw text, tokenized, FastText, GlotLID, etc.)
- Optional few-shot examples and heuristic inputs (GlotLID) in prompts
- Plug-and-play LLM querying via a local or remote backend (e.g., Ollama)
- JSONL input/output for large-scale benchmarking

---


## Project Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/idilkuru/Praktikum.git
