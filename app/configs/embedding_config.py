from sentence_transformers import SentenceTransformer
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model_embedding = SentenceTransformer('all-mpnet-base-v2', device=device)
