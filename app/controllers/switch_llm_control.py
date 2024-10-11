from fastapi import HTTPException
from app.models.llm_config import (
                    LLMConfigSchema, 
                    SelectedModel, 
                    ModelConfig, 
                    ModelOpenAIConfig, 
                    ModelAzureOpenAIConfig, 
                    ModelGoogleGeminiConfig, 
                    ModelOllamaConfig
                    )


class SwitchLLMControl:
    @staticmethod
    def get_user_llm_config(user_id: str) -> LLMConfigSchema:
        llm_config = LLMConfigSchema.find_by_user_id(user_id)
        if not llm_config:
            raise HTTPException(status_code=404,
                                detail=f"LLM Configuration not found for user_id: {user_id}")
        return llm_config

    @staticmethod
    def update_user_llm_config(user_id: str, 
                               selected_model: SelectedModel, 
                               model_config: dict) -> LLMConfigSchema:
        llm_config = LLMConfigSchema.find_by_user_id(user_id)

        if not llm_config:
            llm_config = LLMConfigSchema(
                user_id=user_id,
                selected_model=selected_model,
                config=SwitchLLMControl._build_model_config(selected_model, model_config)
            )
            return llm_config.create()
        else:
            llm_config.selected_model = selected_model
            llm_config.config = SwitchLLMControl._fetch_and_update_config(
                llm_config.config, selected_model, model_config
            )
            llm_config.update()
            return llm_config

    @staticmethod
    def delete_user_llm_config(user_id: str) -> str:
        llm_config = LLMConfigSchema.find_by_user_id(user_id)
        if not llm_config:
            raise HTTPException(status_code=404,
                                detail=f"LLM Configuration not found for user_id: {user_id}")
        
        llm_config.delete()
        return f"LLM Configuration for user_id {user_id} has been deleted."

    @staticmethod
    def switch_llm_model(user_id: str, 
                         model_type: SelectedModel, 
                         config_data: dict) -> str:
        
        if model_type not in SelectedModel:
            raise HTTPException(status_code=400,
                                detail=f"Invalid model type: {model_type}")

        if model_type in [SelectedModel.OpenAI, SelectedModel.GoogleGemini]:
            if not config_data.get("name_model") or not config_data.get("api_key"):
                raise HTTPException(status_code=400,
                                    detail=f"Model Type {model_type} requires 'name_model' and 'api_key'")
            
        elif model_type in [SelectedModel.AzureOpenAI, SelectedModel.Ollama]:
            if not config_data.get("endpoint") or not config_data.get("name_model"):
                raise HTTPException(status_code=400,
                                    detail=f"Model Type {model_type} requires 'endpoint' and 'name_model'")

        SwitchLLMControl.update_user_llm_config(user_id, model_type, config_data)
        return f"LLM model switched successfully to {model_type} for user {user_id}."

    @staticmethod
    def _build_model_config(selected_model: SelectedModel, 
                            model_config: dict) -> ModelConfig:
        
        if selected_model == SelectedModel.OpenAI:
            return ModelConfig(openai=ModelOpenAIConfig(**model_config))
        
        elif selected_model == SelectedModel.AzureOpenAI:
            return ModelConfig(azure_openai=ModelAzureOpenAIConfig(**model_config))
        
        elif selected_model == SelectedModel.GoogleGemini:
            return ModelConfig(google_gemini=ModelGoogleGeminiConfig(**model_config))
        
        elif selected_model == SelectedModel.Ollama:
            return ModelConfig(ollama=ModelOllamaConfig(**model_config))
        
        else:
            raise HTTPException(status_code=400, 
                                detail=f"Invalid model type: {selected_model}")

    @staticmethod
    def _fetch_and_update_config(current_config: ModelConfig, 
                                 selected_model: SelectedModel, 
                                 new_config: dict) -> ModelConfig:
        cur_dict = current_config.dict()
        
        model_config_key = selected_model.value
        current_model_config = cur_dict.get(model_config_key, {})

        for key, value in new_config.items():
            if value is not None:
                current_model_config[key] = value

        cur_dict[model_config_key] = current_model_config

        return ModelConfig(**cur_dict)