from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.configs.embedding_config import model_embedding
from app.utils.logger import get_logger

logger = get_logger("EMBEDDING", color=94)


DEFAULT_CHUNK_SIZE = 1024
DEFAULT_CHUNK_OVERLAP = 200


class VectorEmbedder:
    def __init__(self, chunk_size: int = DEFAULT_CHUNK_SIZE, chunk_overlap: int = DEFAULT_CHUNK_OVERLAP):
        self.model = model_embedding
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def embed(self, text: str | list[str], batch_size: int = 8) -> list[list[float]]:
        if isinstance(text, str):
            text = [text]
        embeddings = self.model.encode(text, batch_size=batch_size).tolist()
        logger(f"Text embedded `{len(embeddings)}, {len(embeddings[0])}`")
        return embeddings

    def chunk_text(self, text: str):
        chunks = self.text_splitter.split_text(text)
        logger(f"Text split into `{len(chunks)}` chunks")
        return chunks
