from app.models.user import UserSchema
from app.models.llm_config import (
    LLMConfigSchema,
    SelectedModel,
    ModelConfigTypes
)


def get_user_llm_config(user: UserSchema):
    config = LLMConfigSchema.find_by_user_id(user.id)
    # Create config if not exists
    if not config:
        config = LLMConfigSchema(user_id=user.id).create()
    return config


def update_user_llm_config(user: UserSchema, selected_model: SelectedModel, model_config: ModelConfigTypes):
    config = LLMConfigSchema.find_by_user_id(user.id)

    # Update config if exists
    if config:
        config.selected_model = selected_model
        # Update config based on model type
        if selected_model == SelectedModel.OpenAI:
            config.config.openai = model_config
        elif selected_model == SelectedModel.AzureOpenAI:
            config.config.azure_openai = model_config
        elif selected_model == SelectedModel.GoogleGemini:
            config.config.google_gemini = model_config
        elif selected_model == SelectedModel.Ollama:
            config.config.ollama = model_config
        config.update()

    return config
