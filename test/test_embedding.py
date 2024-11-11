import unittest
from app.providers import embedder


class TestEmbedder(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.sample_text = "This is a sample text for testing."
        self.sample_text_2 = "This is a testing sample text."

    def test_embed_text(self):
        vectors = embedder.embed([self.sample_text, self.sample_text_2])
        self.assertEqual(len(vectors), 2)
        self.assertEqual(len(vectors[0]), 768)
