from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserSchema
from app.controllers.auth_control import (
    authenticate_user,
    create_access_token,
)
from app.middlewares.middleware import auth_user_middleware
from app.utils.response import response

router = APIRouter()


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"uid": user.id})
    return response(code=200, message="Login successful", data={"token": access_token})


@router.get("/me")
async def read_users_me(user: Annotated[UserSchema, Depends(auth_user_middleware)]):
    return response(code=200, message="Get user successfully", data=user.model_dump(exclude=["password"]))
