import os
from langchain_ollama.llms import OllamaLLM
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import ChatOpenAI, AzureChatOpenAI


def create_gpt_model(model_name: str, api_key: str):
    return ChatOpenAI(
        model=model_name,
        openai_api_key=api_key
    )


def create_azure_gpt_model(model_name: str, azure_endpoint: str, api_key: str):
    return AzureChatOpenAI(
        api_version="2020-08-01",
        model=model_name,
        azure_endpoint=azure_endpoint,
        api_key=api_key
    )


def create_gemini_model(model_name: str, google_api_key: str):
    return GoogleGenerativeAI(
        model=model_name,
        google_api_key=google_api_key
    )


def create_ollama_model(model_name: str, base_url: str):
    return OllamaLLM(
        base_url=base_url,
        model=model_name,
        request_timeout=120.0
    )


gpt = create_gpt_model(
    model_name="gpt-4o",
    api_key=os.environ.get("LLM_OPENAI_API_KEY", "dummysecret")
)

azure_gpt = create_azure_gpt_model(
    model_name="gpt-4o",
    azure_endpoint=os.environ.get("LLM_AZURE_ENDPOINT", "dummysecret"),
    api_key=os.environ.get("LLM_AZURE_API_KEY", "dummysecret")
)


gemini = create_gemini_model(
    model_name="gemini-pro",
    google_api_key=os.environ.get("LLM_GOOGLE_API_KEY", "dummysecret")
)

ollama = create_ollama_model(
    model_name="llama3.2",
    base_url=os.environ.get("LLM_OLLAMA_HOST", "localhost")
)
