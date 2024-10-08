import unittest
from app.models.llm_config import (
    LLMConfigSchema,
    SelectedModel,
    ModelLlamaConfig,
    ModelOpenAIConfig,
    ModelAzureOpenAIConfig,
    ModelGoogleGeminiConfig
)


class LLMConfigDbTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super(LLMConfigDbTestCase, self).__init__(*args, **kwargs)

    def __create_config(self):
        # Create a test config
        config = LLMConfigSchema(
            user_id="test_user",
        )
        config.create()
        # Test if config is created
        self.assertIsNotNone(config.id)
        # Validate the config
        config = LLMConfigSchema.find_by_id(config.id)
        self.assertIsNotNone(config)
        return config

    def __find_config(self, user_id: str):
        # Find the config by user_id with valid id
        config = LLMConfigSchema.find_by_user_id(user_id)
        self.assertIsNotNone(config)
        # Find the config by user_id with invalid id
        config = LLMConfigSchema.find_by_user_id("invalid_user")
        self.assertIsNone(config)

    def __update_llama_config(self, config: LLMConfigSchema, llama_config: ModelLlamaConfig):
        # Update the llama config
        config.selected_model = SelectedModel.Llama
        config.config.llama = llama_config
        config.update()
        # Validate the config
        config = LLMConfigSchema.find_by_id(config.id)
        self.assertEqual(config.selected_model, SelectedModel.Llama)
        # Validate the llama config
        self.assertEqual(config.config.llama.version,
                         llama_config.version)

    def __update_openai_config(self, config: LLMConfigSchema, openai_config: ModelOpenAIConfig):
        # Update the openai config
        config.selected_model = SelectedModel.OpenAI
        config.config.openai = openai_config
        config.update()
        # Validate the config
        config = LLMConfigSchema.find_by_id(config.id)
        self.assertEqual(config.selected_model, SelectedModel.OpenAI)
        # Validate the openai config
        self.assertEqual(config.config.openai.api_key,
                         openai_config.api_key)

    def __update_azure_openai_config(self, config: LLMConfigSchema, azure_openai_config: ModelAzureOpenAIConfig):
        # Update the azure openai config
        config.selected_model = SelectedModel.AzureOpenAI
        config.config.azure_openai = azure_openai_config
        config.update()
        # Validate the config
        config = LLMConfigSchema.find_by_id(config.id)
        self.assertEqual(config.selected_model, SelectedModel.AzureOpenAI)
        # Validate the azure openai config
        self.assertEqual(config.config.azure_openai.api_key,
                         azure_openai_config.api_key)

    def __update_google_gemini_config(self, config: LLMConfigSchema, google_gemini_config: ModelGoogleGeminiConfig):
        # Update the google gemini config
        config.selected_model = SelectedModel.GoogleGemini
        config.config.google_gemini = google_gemini_config
        config.update()
        # Validate the config
        config = LLMConfigSchema.find_by_id(config.id)
        self.assertEqual(config.selected_model, SelectedModel.GoogleGemini)
        # Validate the google gemini config
        self.assertEqual(config.config.google_gemini.api_key,
                         google_gemini_config.api_key)

    def __delete_config(self, config: LLMConfigSchema):
        # Delete the config
        config.delete()
        # Validate the delete
        config = LLMConfigSchema.find_by_id(config.id)
        self.assertIsNone(config)

    def test_llm_config_db(self):
        # Create a test config
        config = self.__create_config()
        # Find the config by user_id
        self.__find_config(config.user_id)
        # Update the llama config
        llama_config = ModelLlamaConfig(version="v1")
        self.__update_llama_config(config, llama_config)
        # Update the openai config
        openai_config = ModelOpenAIConfig(
            model_name="gpt-3", api_key="openai_key")
        self.__update_openai_config(config, openai_config)
        # Update the azure openai config
        azure_openai_config = ModelAzureOpenAIConfig(
            endpoint="https://azure.com", model_name="gpt-3", api_key="azure_openai_key")
        self.__update_azure_openai_config(config, azure_openai_config)
        # Update the google gemini config
        google_gemini_config = ModelGoogleGeminiConfig(
            api_key="google_gemini_key")
        self.__update_google_gemini_config(config, google_gemini_config)
        # Delete the config
        self.__delete_config(config)
