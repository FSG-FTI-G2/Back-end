from app.middlewares.middleware import get_current_user_from_token
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/protected-route")
async def protected_route(user=Depends(get_current_user_from_token)):
    return {"message": "You are authorized", "user": user.username}