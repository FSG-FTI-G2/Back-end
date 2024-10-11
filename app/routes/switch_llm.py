from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.controllers.switch_llm_control import SwitchLLMControl
from app.models.llm_config import SelectedModel

router = APIRouter()

@router.get("/llm", response_model=dict)
def get_llm_config(user_id: str):
    llm_config = SwitchLLMControl.get_user_llm_config(user_id)
    return {"user_id": user_id, "selected_model": llm_config.selected_model, 
            "config": llm_config.config}


@router.post("/llm/switch", response_model=str)
def switch_llm_model(user_id: str, model_type: SelectedModel, config_data: dict):
    response = SwitchLLMControl.switch_llm_model(user_id, model_type, config_data)
    return response


@router.delete("/llm/delete", response_model=str)
def delete_llm_config(user_id: str):
    response = SwitchLLMControl.delete_user_llm_config(user_id)
    return response
