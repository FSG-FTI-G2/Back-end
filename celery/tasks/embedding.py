import os
import torch
from sentence_transformers import SentenceTransformer
from celery import Task
from .utils import batch_splitter

if torch.cuda.is_available():
    torch.backends.cudnn.benchmark = True
    device = "cuda"
else:
    device = "cpu"

model_name = os.environ.get("MODEL_NAME", "all-mpnet-base-v2")
model_embedding = SentenceTransformer(model_name)
batch_size = os.environ.get("EMBEDDING_BATCH_SIZE", 4)


def embed_model(task: Task, text: str | list[str]) -> list[list[float]]:
    """Embed text using SentenceTransformer model"""
    if isinstance(text, str):
        text = [text]

    # Split batch size
    batches = batch_splitter(text, batch_size)
    # If the length of the last batch is not equal to the batch size
    # Extend the last element to fill the batch
    if len(batches[-1]) < batch_size:
        batches[-1].extend([batches[-1][-1]] * (batch_size - len(batches[-1])))

    embedded_results = []
    for i, batch in enumerate(batches):
        embeddings = model_embedding.encode(
            batch, convert_to_tensor=True, device=device)
        embedded_results.extend(embeddings.tolist())
        task.update_state(
            state="PROGRESS",
            meta={"progress": (i+1) * 100 / len(batches)}
        )

    return embedded_results
