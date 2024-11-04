import os
from app.models.user_schema import UserSchema
from app.models.llm_config_schema import (
    LLMConfigSchema,
    SelectedModel,
    ModelConfigTypes
)
from app.providers import state
from app.providers.llm_provider import ModelWrapper
from app.configs.llm_config import (
    create_gpt_model,
    create_azure_gpt_model,
    create_gemini_model,
    create_ollama_model
)


def get_user_llm_config(user: UserSchema):
    # Create config if not exists
    config = LLMConfigSchema.find_by_user_id(user.id)
    if not config:
        config = LLMConfigSchema(user_id=user.id).create()
    return config


def __get_user_memory_llm_config(user: UserSchema):
    # Create config in memory if not exists
    mconfig = state.get(f"llm_memory_config_{user.id}")
    if not mconfig:
        state.set(f"llm_memory_config_{user.id}", {"model": None})
        mconfig = state.get(f"llm_memory_config_{user.id}")
    return mconfig


def load_model_config_by_user(user: UserSchema) -> ModelWrapper | None:
    # Get memory config
    memory_config = __get_user_memory_llm_config(user)
    if memory_config["model"] is not None:
        return memory_config["model"]

    # Get config from db
    config = get_user_llm_config(user)

    if config.selected_model is None:
        return None

    # Load model based on selected model
    if config.selected_model == SelectedModel.OpenAI:
        memory_config["model"] = ModelWrapper(create_gpt_model(
            config.config.openai.name_model, config.config.openai.api_key))

    elif config.selected_model == SelectedModel.AzureOpenAI:
        memory_config["model"] = ModelWrapper(create_azure_gpt_model(
            config.config.azure_openai.name_model, config.config.azure_openai.endpoint, config.config.azure_openai.api_key))

    elif config.selected_model == SelectedModel.GoogleGemini:
        memory_config["model"] = ModelWrapper(create_gemini_model(
            config.config.google_gemini.name_model, config.config.google_gemini.api_key))

    elif config.selected_model == SelectedModel.Ollama:
        memory_config["model"] = ModelWrapper(create_ollama_model(
            config.config.ollama.name_model, config.config.ollama.endpoint))
    return memory_config["model"]


def update_user_llm_config(user: UserSchema, selected_model: SelectedModel, model_config: ModelConfigTypes):
    config = get_user_llm_config(user)
    memory_config = __get_user_memory_llm_config(user)

    # Update config
    config.selected_model = selected_model
    # Update config based on model type
    if selected_model == SelectedModel.OpenAI:
        if not model_config.name_model:
            model_config.name_model = "gpt-4o"
        config.config.openai = model_config
        memory_config["model"] = ModelWrapper(create_gpt_model(
            model_config.name_model, model_config.api_key))

    elif selected_model == SelectedModel.AzureOpenAI:
        if not model_config.name_model:
            model_config.name_model = "gpt-4o"
        config.config.azure_openai = model_config
        memory_config["model"] = ModelWrapper(create_azure_gpt_model(
            model_config.name_model, model_config.endpoint, model_config.api_key))

    elif selected_model == SelectedModel.GoogleGemini:
        if not model_config.name_model:
            model_config.name_model = "gemini-pro"
        config.config.google_gemini = model_config
        memory_config["model"] = ModelWrapper(create_gemini_model(
            model_config.name_model, model_config.api_key))

    elif selected_model == SelectedModel.Ollama:
        if not model_config.name_model:
            model_config.name_model = "llama3.2"
        if not model_config.endpoint:
            model_config.endpoint = os.environ.get(
                "LLM_OLLAMA_HOST", "localhost")
        config.config.ollama = model_config
        memory_config["model"] = ModelWrapper(create_ollama_model(
            model_config.name_model, model_config.endpoint))
    config.update()

    return config
