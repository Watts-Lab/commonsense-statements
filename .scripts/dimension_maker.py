import torch
import gradio as gr
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)
import os
import swifter
import pandas as pd
from huggingface_hub import login
from dimension_checker import process_files, get_unique_rows_by_hash
import hashlib


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


login(token=os.getenv("HUGGINGFACE_TOKEN"))

DIMENSIONS = [
    "behavior",
    "everyday",
    "figure_of_speech",
    "judgment",
    "opinion",
    "reasoning",
]

print(f"{bcolors.OKBLUE}Loading models...{bcolors.ENDC}")

# Cache directory for models - GitHub Actions compatible
CACHE_DIR = os.path.expanduser("~/.cache/huggingface/transformers")
os.makedirs(CACHE_DIR, exist_ok=True)


# Create a cache key based on model names for GitHub Actions caching
def get_cache_key():
    model_names = ["CSSLab/commonsense-statement-dimension-reasoning"] + [
        f"CSSLab/commonsense-statement-dimension-{dim}" for dim in DIMENSIONS
    ]
    cache_string = "|".join(sorted(model_names))
    return hashlib.md5(cache_string.encode()).hexdigest()[:8]


CACHE_KEY = get_cache_key()

tokenizer = AutoTokenizer.from_pretrained(
    "CSSLab/commonsense-statement-dimension-reasoning", token=True, cache_dir=CACHE_DIR
)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODELS = {}

for dimension in DIMENSIONS:
    # Check if accelerate is available for memory optimizations
    try:
        import accelerate

        has_accelerate = True
    except ImportError:
        has_accelerate = False

    # Configure model loading parameters based on available libraries
    model_kwargs = {
        "pretrained_model_name_or_path": f"CSSLab/commonsense-statement-dimension-{dimension}",
        "token": True,
        "cache_dir": CACHE_DIR,
    }

    # Add memory optimizations only if accelerate is available
    if has_accelerate:
        model_kwargs["low_cpu_mem_usage"] = True
        if torch.cuda.is_available():
            model_kwargs["torch_dtype"] = torch.float16

    model = AutoModelForSequenceClassification.from_pretrained(**model_kwargs)
    model.eval()
    model = model.to(DEVICE)

    # Only use JIT optimization if it's supported
    try:
        model = torch.jit.optimize_for_inference(model)
    except Exception:
        # JIT optimization might not be available for all models
        pass

    MODELS[dimension] = model
    print(f"{bcolors.OKGREEN}Loaded model for {dimension}.{bcolors.ENDC}")


def classify_text(text: str) -> pd.Series:
    # Encode the prompt
    inputs = tokenizer([text], padding=True, truncation=True, return_tensors="pt").to(
        DEVICE
    )
    scores = dict()

    # Use torch.no_grad() for inference to save memory and speed up
    with torch.no_grad():
        for dimension in DIMENSIONS:
            model = MODELS[dimension]
            outputs = model(**inputs)
            outputs = torch.softmax(outputs.logits, dim=1)
            outputs = outputs[:, 1]
            score = outputs.detach().cpu().numpy()[0]
            # Keep as float instead of converting to int
            scores[dimension] = float(score)  # Changed from int(score > 0.5)

    return pd.Series(scores)


if __name__ == "__main__":
    all_statements_df = process_files("raw_statements", "processed_statements")
    print(f"{bcolors.OKBLUE}Imported all statements from raw statements.{bcolors.ENDC}")

    if all_statements_df is None:
        print(
            f"{bcolors.FAIL}No statements found in raw_statements folder.{bcolors.ENDC}"
        )
        exit(1)

    try:
        old_ratings_df = pd.read_csv("features/ratings.csv")
    except FileNotFoundError:
        old_ratings_df = None

    if old_ratings_df is None:
        print(
            f"{bcolors.FAIL}No ratings found in features/ratings.csv. Creating a new file.{bcolors.ENDC}"
        )
        old_ratings_df = pd.DataFrame()

    all_statements_df = get_unique_rows_by_hash(all_statements_df, old_ratings_df)

    # Check if there are any new statements to rate
    if all_statements_df.empty:
        print(f"{bcolors.FAIL}No new statements found to rate.{bcolors.ENDC}")
        exit()

    ratings_df = all_statements_df["statement"].swifter.apply(classify_text)
    all_statements_df = all_statements_df.join(ratings_df)

    new_ratings_df = pd.concat([old_ratings_df, all_statements_df], ignore_index=True)
    new_ratings_df.to_csv("features/ratings.csv", index=False)

    print(
        f"{bcolors.OKGREEN}All statements have been rated and saved to features/ratings.csv{bcolors.ENDC}"
    )
