import unittest
from unittest.mock import patch
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.embeddings.ollama import OllamaEmbedding
from app.providers.LLM import LLMProvider
from app.configs.llm import GPTClient, GeminiClient, OllamaClient

class TestLLMProvider(unittest.TestCase):
    def setUp(self):
        self.provider = LLMProvider()

    # @patch('os.environ.get')
    # def test_set_openai_model(self, mock_get_env):
    #     self.provider.set_model("openai")
    #     self.assertEqual(self.provider.model_name, "openai")
    #     self.assertEqual(self.provider.llm, GPTClient)
    #     self.assertIsInstance(self.provider.embed_model, OpenAIEmbedding)

    @patch('os.environ.get', return_value='dummy_api_key')
    def test_set_gemini_model(self, mock_get_env):
        self.provider.set_model("gemini")
        self.assertEqual(self.provider.model_name, "gemini")
        self.assertEqual(self.provider.llm, GeminiClient)
        self.assertIsInstance(self.provider.embed_model, GeminiEmbedding)

    def test_set_ollama_model(self):
        self.provider.set_model("ollama")
        self.assertEqual(self.provider.model_name, "ollama")
        self.assertEqual(self.provider.llm, OllamaClient)
        self.assertIsInstance(self.provider.embed_model, OllamaEmbedding)

    def test_invalid_model(self):
        llm, embed_model = self.provider.set_model("invalid_model")
        self.assertIsNone(llm)
        self.assertIsNone(embed_model)

