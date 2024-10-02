from fastapi import APIRouter
from .auth import router as auth_router  

router = APIRouter(prefix="/api/v1", tags=["v1"])

# Include routes

router.include_router(auth_router)
