class Config:
    INPUT_PATH = "/Users/idilkuruoglu/PycharmProjects/Praktikum/Data/merged_dataset_1800.jsonl"
    OUTPUT_PATH = "/Users/idilkuruoglu/PycharmProjects/Praktikum/Data/cleaned_glotlid_output.jsonl"
    TEXT_FIELD = "text"
    CONFIDENCE_THRESHOLD = 0.3
    BATCH_SIZE = 100
    MODEL_NAME = "cis-lmu/glotlid"