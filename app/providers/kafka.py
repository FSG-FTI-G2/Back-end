from app.configs.kafka import consumer, producer

class KafkaProvider:
    def __init__(self):
        self.request_topic = 'embedding_requests'
        self.response_topic = 'embedding_responses'
        self.consumer = consumer
        self.producer = producer

    def send_request(self, text: str, request_id: str) -> None:
        """Send request to Kafka"""
        message = {
            'request_id': request_id,
            'text': text
        }
        self.producer.send(self.request_topic, message)
        self.producer.flush()
        print(f"Sent request: {message}")

    def listen_for_responses(self, process_response_callback) -> None:
        """Listen for responses from Kafka and process them"""
        for message in self.consumer:
            response = message.value
            process_response_callback(response)
            print(f"Received response: {response}")

    def close(self) -> None:
        """Close Kafka connection"""
        self.consumer.close()
        self.producer.close()
