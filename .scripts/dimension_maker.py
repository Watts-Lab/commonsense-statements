import torch
import gradio as gr
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)
from typing import Dict
import os
import pandas as pd
from huggingface_hub import login

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
    "CSSLab/commonsense-statement-dimension-reasoning", use_auth_token=True
)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODELS = {}
for dimension in DIMENSIONS:
    model = AutoModelForSequenceClassification.from_pretrained(
        pretrained_model_name_or_path=f"CSSLab/commonsense-statement-dimension-{dimension}",
        use_auth_token=True,
    )
    model.eval()
    MODELS[dimension] = model.to(DEVICE)


def classify_text(text: str) -> Dict[str, float]:
    # Encode the prompt
    inputs = tokenizer([text], padding=True, truncation=True, return_tensors="pt").to(
        DEVICE
    )
    scores = []
    for dimension in DIMENSIONS:
        model = MODELS[dimension]
        outputs = model(**inputs)
        outputs = torch.softmax(outputs.logits, dim=1)
        outputs = outputs[:, 1]
        score = outputs.detach().cpu().numpy()[0]
        scores.append([dimension, score])
    scores = pd.DataFrame(scores, columns=["dimension", "score"])
    return scores
