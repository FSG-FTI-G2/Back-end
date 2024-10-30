import os
import torch
from sentence_transformers import SentenceTransformer
from celery import Task

if torch.cuda.is_available():
    torch.backends.cudnn.benchmark = True
    device = "cuda"
else:
    device = "cpu"

model_name = os.environ.get("MODEL_NAME", "all-mpnet-base-v2")
model_embedding = SentenceTransformer(model_name)
batch_size = int(os.environ.get("EMBEDDING_BATCH_SIZE", 8))


def embed_model(task: Task, text: str | list[str]) -> list[list[float]]:
    """Embed text using SentenceTransformer model"""
    if isinstance(text, str):
        text = [text]
    return model_embedding.encode(text, batch_size=batch_size).tolist()
