from fastapi import APIRouter
from .auth import router as auth_router
from .files import router as files_router
from .serve_static_file_routes import router as serve_static_file_routes


router = APIRouter(prefix="/api/v1")

# Include routes
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(serve_static_file_routes,
                      prefix="/serve", tags=["serve"])
router.include_router(files_router, prefix="/files", tags=["files"])
