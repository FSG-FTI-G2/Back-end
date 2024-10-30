import os
from langchain.llms import OpenAI, Ollama, Gemini


GPTClient = OpenAI(
    openai_api_key=os.environ.get("OPENAI_API_KEY")
)


GeminiClient = Gemini(
    api_key=os.environ.get("GEMINI_API_KEY", "AIzaSyCSYxGY0qTL4WzKIFygJUoC82XwUsZsFgU")
)


OllamaClient = Ollama(
    base_url=os.environ.get("OLLAMA_URL", "http://localhost:11434"),
    model="llama3.2",
    request_timeout=120.0,
)