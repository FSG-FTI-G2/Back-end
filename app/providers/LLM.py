import os
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings
from llama_index.core.llms import ChatMessage
from typing import Optional, Dict, Any
from pydantic import BaseModel
from app.utils.prompt_template import *
from app.configs.llm import GPTClient, GeminiClient, OllamaClient


class Output(BaseModel):
    """Data model for structured response."""
    query: str
    model: str
    role: str
    response: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = {
        "name": "User",
        "title": "Default Title",
        "author": "Anonymous"
    }

class LLMProvider:
    def __init__(self):
        self.model_name : str = ""
        self.embed_model = None
        self.llm = None
    
    def set_model(self, model_name: str):
        self.model_name = model_name
        if self.model_name == "openai":
            self.llm = GPTClient
            self.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
        elif self.model_name == "gemini":
            self.llm = GeminiClient
            self.embed_model = GeminiEmbedding(model_name= "models/embedding-001", 
                                          api_key=os.environ.get("GEMINI_API_KEY"))
        elif self.model_name == "ollama":
            self.llm = OllamaClient
            self.embed_model = OllamaEmbedding(model_name="llama2",
                                            base_url="http://localhost:11434",
                                            ollama_additional_kwargs={"mirostat": 0},
                                            )
        return self.llm, self.embed_model
    
    def template(self, question, role="student") -> str:
        if role == "student":
            return template_base_knowledge.format(question=question)
        elif role == "expert":
            return template_professor_knowledge.format(question=question)
        else:
            return question
        
    def structured_response(self, model_name: str, question: str, role: str = "student") -> Dict[str, Any]:
        llm, embed_model = self.set_model(model_name)
        Settings.llm = llm
        Settings.embed_model = embed_model
    
        sllm = llm.as_structured_llm(output_cls=Output)
        input_msg = ChatMessage.from_str(question)
        output = sllm.chat([input_msg])
        return output.raw
        
    def get_response(self, question: str, role: str = "student"):
        template = self.template(question, role)
        response = self.llm.complete(template)
        return response
        
    def retrieval_response(self, model_name, question: str, role: str = "student") -> Dict[str, Any]:
        formatted_prompt = self.template(question, role)
        structured_response = self.structured_response(model_name, formatted_prompt, role)
        return structured_response
   

