import os
from llama_index.llms.openai import OpenAI
from llama_index.llms.gemini import Gemini
# from llama_index.llms.ollama import Ollama

GPTClient = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

GeminiClient = Gemini(
    api_key=os.environ.get("GEMINI_API_KEY")
)

# OllamaClient = Ollama(
#     base_url=os.environ.get("OLLAMA_URL", "http://localhost:11434"),
#     model="llama3.2",
#     request_timeout=120.0
# )
