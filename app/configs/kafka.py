from kafka import KafkaConsumer, KafkaProducer
import json
import os

KAFKA_BROKER = f"{os.environ.get('KAFKA_HOST')}:{os.environ.get('KAFKA_PORT')}"

consumer = KafkaConsumer(
    'embedding_responses', 
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',  
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
