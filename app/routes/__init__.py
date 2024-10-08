from fastapi import APIRouter
from .auth import router as auth_router
from .upload import router as router_upload


router = APIRouter(prefix="/api/v1")

# Include routes
router.include_router(router_upload, prefix="/files", tags=["files"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
