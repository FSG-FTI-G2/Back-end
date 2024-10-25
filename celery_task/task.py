from .app import app
from transformers import AutoTokenizer, AutoModel
from app.providers import kafka_provider
import torch
import json

MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"

@app.task
def create_embedding(request_id: str, input_data: str):
    """ Create embedding for input data """
    model = AutoModel.from_pretrained(MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    inputs = tokenizer(input_data, 
                       return_tensors="pt", 
                       padding=True, 
                       truncation=True)
    with torch.no_grad():
        embedding = model(**inputs).last_hidden_state.mean(dim=1).squeeze().tolist()

    send_to_kafka(request_id, embedding)

def send_to_kafka(request_id: str, embedding: list):
    """Send embedding to Kafka"""
    provider =  kafka_provider
    response = {
        'request_id': request_id,
        'embedding': embedding
    }
    provider.send_request(json.dumps(response), request_id)
    provider.close()

def listen_for_requests():
    """ Listen for requests from Kafka """
    provider = kafka_provider

    def process_request(request):
        request_id = request.get('request_id')
        text = request.get('text')
        print(f"Processing request: {request_id}")

        create_embedding.delay(request_id, text)

    provider.listen_for_responses(process_request)
