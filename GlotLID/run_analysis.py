from glotlid_processor import GlotLIDProcessor
from config import Config

def main():
    processor = GlotLIDProcessor()

    # Process data
    processor.process_jsonl(
        input_path=Config.INPUT_PATH,
        output_path=Config.OUTPUT_PATH,
        text_field=Config.TEXT_FIELD,
        batch_size=Config.BATCH_SIZE
    )

    # Generate metrics
    metrics = processor.generate_metrics(Config.OUTPUT_PATH)


if __name__ == "__main__":
    main()