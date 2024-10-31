from langchain.text_splitter import RecursiveCharacterTextSplitter
from .celery_provider import CeleryProvider
from app.utils.logger import get_logger

logger = get_logger("EMBEDDING", color=94)


DEFAULT_CHUNK_SIZE = 1024
DEFAULT_CHUNK_OVERLAP = 200


class VectorEmbedder:
    def __init__(self, chunk_size: int = DEFAULT_CHUNK_SIZE, chunk_overlap: int = DEFAULT_CHUNK_OVERLAP):
        self.model = CeleryProvider[list[list[float]]]()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def embed(self, text: str | list[str]) -> list[list[float]]:
        task_id = self.model.execute("embed", text)
        result = self.model.get_result(task_id, wait_until_complete=True)
        embeddings = result["result"]
        logger(f"Text embedded `{len(embeddings)}, {len(embeddings[0])}`")
        return embeddings

    def chunk_text(self, text: str):
        chunks = self.text_splitter.split_text(text)
        logger(f"Text split into `{len(chunks)}` chunks")
        return chunks
