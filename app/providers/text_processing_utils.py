from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
from transformers import AutoTokenizer, pipeline, BartTokenizer, BartForConditionalGeneration
import torch

VECTOR_SIZE = 768
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 200

device = "cuda" if torch.cuda.is_available() else "cpu"
model_embedding = SentenceTransformer('all-mpnet-base-v2')
model_summarize = "sshleifer/distilbart-cnn-12-6"
tokenizer = BartTokenizer.from_pretrained(model_summarize)
model = BartForConditionalGeneration.from_pretrained(model_summarize).to(device)

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> list:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(text)
    return chunks

def preprocess_for_summarize(text, max_length=130, min_length=30):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024).to(device)
    summary_ids = model.generate(inputs['input_ids'], max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def chunk_text_for_summarize(text, max_token_length=1024):
    inputs = tokenizer(text, return_tensors="pt", add_special_tokens=False)
    tokens = inputs['input_ids'][0]

    chunks = [tokens[i:i + max_token_length] for i in range(0, len(tokens), max_token_length)]
    return [tokenizer.decode(chunk, skip_special_tokens=True) for chunk in chunks]
def summarize_text(text):
    if len(tokenizer.encode(text)) > 1024:
        chunks = chunk_text_for_summarize(text)
        summaries = [preprocess_for_summarize(chunk) for chunk in chunks]
        full_summary = " ".join(summaries)
    else:
        full_summary = preprocess_for_summarize(text)

    return full_summary