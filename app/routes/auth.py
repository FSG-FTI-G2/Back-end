from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserSchema
from app.utils.respone import response  
from app.controllers.auth_control import (
    authenticate_user,
    create_access_token,
    get_current_user
)

router = APIRouter()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username}) 
    return response(code=400, message="Login successful", data={"access_token": access_token})


@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
