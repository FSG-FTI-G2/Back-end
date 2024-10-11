from typing import Optional, Union
from enum import Enum
from pydantic import Field, BaseModel
from app.models.base import BaseSchema
from app.providers import llm_config_db


class SelectedModel(str, Enum):
    '''
    Enum for LLM Selected Model Type
    '''
    # Llama = "llama"
    OpenAI = "openai"
    AzureOpenAI = "azure_openai"
    GoogleGemini = "google_gemini"
    Ollama = "ollama"


# class ModelLlamaConfig(BaseModel):
#     version: Optional[str] = Field(None, alias="version",
#                                    description="Version of the model")


class ModelOpenAIConfig(BaseModel):
    name_model: Optional[str] = Field(None, alias="name_model",
                                      description="Name of the OpenAI Model")
    api_key: Optional[str] = Field(None, alias="api_key",
                                   description="API Key for OpenAI Model")


class ModelAzureOpenAIConfig(BaseModel):
    endpoint: Optional[str] = Field(None, alias="endpoint",
                                    description="Endpoint of the Azure OpenAI Model")
    name_model: Optional[str] = Field(None, alias="name_model",
                                      description="Name of the Azure OpenAI Model")
    api_key: Optional[str] = Field(None, alias="api_key",
                                   description="API Key for Azure OpenAI Model")


class ModelGoogleGeminiConfig(BaseModel):
    name_model: Optional[str] = Field(None, alias="name_model",
                                      description="Name of the Google Gemini Model")
    api_key: Optional[str] = Field(None, alias="api_key",
                                   description="API Key for Google Gemini Model")

class ModelOllamaConfig(BaseModel):
    endpoint: Optional[str] = Field(None, alias="endpoint",
                                    description="Endpoint of the Ollama Model")
    name_model: Optional[str] = Field(None, alias="name_model",
                                      description="Name of the Ollama Model")

class ModelConfig(BaseModel):
    # llama: ModelLlamaConfig = ModelLlamaConfig()
    openai: ModelOpenAIConfig = ModelOpenAIConfig()
    azure_openai: ModelAzureOpenAIConfig = ModelAzureOpenAIConfig()
    google_gemini: ModelGoogleGeminiConfig = ModelGoogleGeminiConfig()
    ollama: ModelOllamaConfig = ModelOllamaConfig()


# Create index for user_id
llm_config_db.create_index("user_id")


class LLMConfigSchema(BaseSchema):
    user_id: str = Field(None, alias="user_id")
    selected_model: Optional[SelectedModel] = Field(
        None, alias="selected_model")
    config: ModelConfig = ModelConfig()

    @staticmethod
    def find_by_user_id(user_id: str) -> Union['LLMConfigSchema', None]:
        # Find by user_id
        data = llm_config_db.query({"user_id": user_id})
        if len(data) == 0:
            return None
        # Validate the data
        return LLMConfigSchema.model_validate(data[0])

    @staticmethod
    def find_by_id(id: str) -> Union['LLMConfigSchema', None]:
        # Find by id
        data = llm_config_db.get_by_id(id)
        # If data is None, return None
        if data is None:
            return None
        # Validate the data
        return LLMConfigSchema.model_validate(data)

    def create(self) -> 'LLMConfigSchema':
        # Modify the created_at and updated_at
        super().create()
        # Create the llm config
        created_id = llm_config_db.create(
            self.model_dump(exclude=["id"], mode="json", by_alias=True))
        self.id = created_id
        return self

    def update(self) -> int:
        # Modify the updated_at
        super().update()
        # Update the llm config
        return llm_config_db.update(
            self.id, self.model_dump(
                exclude={"id"}, exclude_none=True, mode="json", by_alias=True
            )
        )

    def delete(self) -> int:
        # Delete the llm config
        return llm_config_db.delete(self.id)
