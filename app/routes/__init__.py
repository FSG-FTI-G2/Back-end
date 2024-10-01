from fastapi import APIRouter


router = APIRouter(prefix="/api/v1", tags=["v1"])

# Include routes
from .auth import router as auth_router  
from .protected import router as middleware_router

router.include_router(auth_router)
router.include_router(middleware_router)