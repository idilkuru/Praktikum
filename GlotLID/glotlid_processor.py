import json
import pandas as pd
from pathlib import Path
import fasttext
from huggingface_hub import hf_hub_download
from tqdm import tqdm
from .config import Config
import re


class GlotLIDProcessor:
    def __init__(self):
        # Initialize FastText language identification model
        model_path = hf_hub_download(repo_id=Config.MODEL_NAME, filename="model.bin")
        self.model = fasttext.load_model(model_path)

    def clean_text(self, text):
        """
        Keep more Unicode characters (e.g. Turkish, Hindi, emoji),
        and only strip out obvious punctuation/symbols.
        """
        # keep any token with at least one letter
        tokens = re.findall(r'\b\w+\b', text, flags=re.UNICODE)
        cleaned_tokens = [tok for tok in tokens if any(c.isalpha() for c in tok)]
        return " ".join(cleaned_tokens)

    def detect_language(self, text, threshold=Config.CONFIDENCE_THRESHOLD, max_languages=10):
        try:
            if not text or not isinstance(text, str) or not text.strip():
                return {"languages": [], "is_reliable": False}

            # fallback for short texts
            if len(text.split()) <= 3:
                cleaned_text = text
            else:
                cleaned_text = self.clean_text(text)

            labels, probs = self.model.predict(cleaned_text, k=max_languages)

            results = [
                {
                    "language": label.replace("__label__", ""),
                    "confidence": float(prob)
                }
                for label, prob in zip(labels, probs)
                if prob >= threshold
            ]

            is_reliable = results[0]["confidence"] > 0.5 if results else False

            return {
                "languages": results,
                "is_reliable": is_reliable
            }

        except Exception as e:
            print(f"Error processing text: {str(e)}")
            return {"languages": [], "is_reliable": False}

    def process_jsonl(self, input_path, output_path, text_field="text", batch_size=100):
        with open(input_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        results = []
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        for line in tqdm(lines, desc="Processing JSONL"):
            try:
                entry = json.loads(line)
                text = entry.get(text_field, "")

                lang_info = self.detect_language(text)

                results.append({
                    **entry,
                    "language_info": lang_info
                })

                if len(results) % batch_size == 0:
                    self._save_results(results, output_path)

            except json.JSONDecodeError:
                print(f"Skipping malformed line: {line[:100]}...")
                continue

        self._save_results(results, output_path)
        print(f"Processed {len(results)} records. Saved to {output_path}")

    def _save_results(self, results, output_path):
        if output_path.endswith('.csv'):
            pd.DataFrame(results).to_csv(output_path, index=False, mode='a')
        else:
            with open(output_path, "w", encoding="utf-8") as f:
                for result in results:
                    f.write(json.dumps(result) + "\n")

    def generate_metrics(self, results_path):
        if results_path.endswith('.csv'):
            df = pd.read_csv(results_path)
            lang_info = df['language_info'].apply(eval)
        else:
            data = []
            with open(results_path, "r", encoding="utf-8") as f:
                for line in f:
                    data.append(json.loads(line))
            df = pd.DataFrame(data)
            lang_info = df['language_info']

        df['language'] = lang_info.apply(lambda x: x['languages'][0]['language'] if x['languages'] else 'unk')
        df['confidence'] = lang_info.apply(lambda x: x['languages'][0]['confidence'] if x['languages'] else 0.0)

        metrics = {
            "total_posts": len(df),
            "language_distribution": df['language'].value_counts().to_dict(),
            "confidence_stats": {
                "mean": df['confidence'].mean(),
                "median": df['confidence'].median(),
                "std": df['confidence'].std()
            },
            "top_languages": df['language'].value_counts().head(10).to_dict(),
            "reliable_predictions": {
                "count": len(df[df['confidence'] > 0.5]),
                "percentage": len(df[df['confidence'] > 0.5]) / len(df) * 100
            }
        }

        metrics_path = str(Path(results_path).parent / "language_metrics.json")
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)

        print(f"Metrics saved to {metrics_path}")
        return metrics


if __name__ == "__main__":
    processor = GlotLIDProcessor()

    processor.process_jsonl(
        input_path=Config.INPUT_PATH,
        output_path=Config.OUTPUT_PATH,
        text_field=Config.TEXT_FIELD,
        batch_size=Config.BATCH_SIZE
    )

    metrics = processor.generate_metrics(Config.OUTPUT_PATH)
    print("\nLanguage Metrics:")
    print(json.dumps(metrics, indent=2))
