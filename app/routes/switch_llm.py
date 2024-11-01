from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.middlewares.auth_middleware import auth_user_middleware
from app.controllers.switch_llm_controller import get_user_llm_config, update_user_llm_config
from app.models.user_schema import UserSchema
from app.models.llm_config_schema import SelectedModel, ModelConfigTypes
from app.utils.response import response

router = APIRouter()


@router.get("/")
def get_llm_config(user: Annotated[UserSchema, Depends(auth_user_middleware)]):
    llm_config = get_user_llm_config(user)
    if not llm_config:
        raise HTTPException(
            status_code=404,
            detail=f"LLM Configuration not found: {user.user_id}"
        )
    return response(200, "LLM Configuration found.", llm_config.model_dump())


@router.post("/")
def update_llm_model(
    selected_model: SelectedModel,
    model_config: ModelConfigTypes,
    user: Annotated[UserSchema, Depends(auth_user_middleware)]
):
    llm_config = update_user_llm_config(user, selected_model, model_config)
    return response(200, "LLM Configuration updated.", llm_config.model_dump())
