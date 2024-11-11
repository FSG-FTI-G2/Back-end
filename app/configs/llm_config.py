import os
from langchain_ollama.llms import OllamaLLM
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import ChatOpenAI, AzureChatOpenAI

gpt = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=os.environ.get("LLM_OPENAI_API_KEY", "dummysecret")
)

azure_gpt = AzureChatOpenAI(
    api_version="2020-08-01",
    model="gpt-4o",
    azure_endpoint=os.environ.get("LLM_AZURE_ENDPOINT", "dummysecret"),
    api_key=os.environ.get("LLM_AZURE_API_KEY", "dummysecret")
)


gemini = GoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=os.environ.get("LLM_GOOGLE_API_KEY", "dummysecret")
)


ollama = OllamaLLM(
    base_url=os.environ.get('LLM_OLLAMA_HOST', 'localhost'),
    model="llama3.2",
    request_timeout=120.0,
)
