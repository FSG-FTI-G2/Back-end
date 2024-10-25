import unittest
import uuid
from app.providers import kafka_provider

class TestKafkaEmbedding(unittest.TestCase):
    def setUp(self):
        self.kafka_provider = kafka_provider

    def tearDown(self):
        self.kafka_provider.close()

    def test_send_and_receive_embedding(self):
        request_id = str(uuid.uuid4())
        text = "This is a sample text to test embedding."

        # Send a request to Kafka
        self.kafka_provider.send_request(text, request_id)

        # Function to process the response
        def process_response(response):
            self.assertEqual(response.get('request_id'), request_id)
            print("Embedding received:", response.get('embedding'))
            # Assert that the embedding is a list of floats
            self.assertIsInstance(response.get('embedding'), list)

        # Listen for the response and process it
        self.kafka_provider.listen_for_responses(process_response)

