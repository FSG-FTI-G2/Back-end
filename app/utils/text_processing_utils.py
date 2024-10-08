from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.configs.embedding_config import model_embedding

CHUNK_SIZE = 1024
CHUNK_OVERLAP = 200

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> list:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(text)
    return chunks

def vector_embedding(text):
        return model_embedding.encode(text).tolist()