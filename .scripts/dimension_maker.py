import torch
import gradio as gr
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)
from typing import Dict
import os
import pandas as pd
import swifter
from huggingface_hub import login


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


from dimension_checker import process_files

login(token=os.getenv("HUGGINGFACE_TOKEN"))

DIMENSIONS = [
    "behavior",
    "everyday",
    "figure_of_speech",
    "judgment",
    "opinion",
    "reasoning",
]

tokenizer = AutoTokenizer.from_pretrained(
    "CSSLab/commonsense-statement-dimension-reasoning", token=True
)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODELS = {}
for dimension in DIMENSIONS:
    model = AutoModelForSequenceClassification.from_pretrained(
        pretrained_model_name_or_path=f"CSSLab/commonsense-statement-dimension-{dimension}",
        token=True,
    )
    model.eval()
    MODELS[dimension] = model.to(DEVICE)


def classify_text(text: str) -> pd.Series:
    # Encode the prompt
    inputs = tokenizer([text], padding=True, truncation=True, return_tensors="pt").to(
        DEVICE
    )
    scores = dict()
    for dimension in DIMENSIONS:
        model = MODELS[dimension]
        outputs = model(**inputs)
        outputs = torch.softmax(outputs.logits, dim=1)
        outputs = outputs[:, 1]
        score = outputs.detach().cpu().numpy()[0]
        scores[dimension] = bool(score > 0.5)
    return pd.Series(scores)


if __name__ == "__main__":
    all_statements_df = process_files("raw_statements", "processed_statements")
    print(f"{bcolors.OKBLUE}Imported all statements from raw statements.{bcolors.ENDC}")

    if all_statements_df is None:
        print(
            f"{bcolors.FAIL}No statements found in raw_statements folder.{bcolors.ENDC}"
        )
        exit(1)

    ratings_df = all_statements_df["statement"].swifter.apply(classify_text)

    all_statements_df = all_statements_df.join(ratings_df)

    all_statements_df.to_csv("features/ratings.csv", index=False)

    print(
        f"{bcolors.OKGREEN}All statements have been rated and saved to features/ratings.csv{bcolors.ENDC}"
    )

    print(all_statements_df.head(20))
