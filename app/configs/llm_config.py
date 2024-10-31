import os
from langchain_ollama.llms import OllamaLLM
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import ChatOpenAI, AzureChatOpenAI

gpt = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=os.environ.get("OPENAI_API_KEY")
)

azure_gpt = AzureChatOpenAI(
    api_version="2020-08-01",
    model="gpt-4o",
    azure_endpoint=os.environ.get("AZURE_ENDPOINT", "dummyendpoint"),
    api_key=os.environ.get("AZURE_API_KEY", "dummyapisecret")
)


gemini = GoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=os.environ.get("GOOGLE_API_KEY")
)


ollama = OllamaLLM(
    base_url=f"http://{os.environ.get('OLLAMA_HOST', 'localhost')}:{os.environ.get('OLLAMA_PORT', 11434)}",
    model="llama3.2",
    request_timeout=120.0,
)
