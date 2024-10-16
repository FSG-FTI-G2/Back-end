from fastapi import APIRouter
from .auth import router as auth_router
from .switch_llm import router as router_switch_llm
from .files import router as files_router
from .view_history import router as view_router


router = APIRouter(prefix="/api/v1")

# Include routes
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(files_router, prefix="/files", tags=["files"])
router.include_router(router_switch_llm, prefix="/llm", tags=["llm"])
router.include_router(view_router, prefix="/view", tags=["view"])
