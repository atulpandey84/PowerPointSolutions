from fastapi import APIRouter

router = APIRouter()

from app.api.endpoints import router as analysis_router
router.include_router(analysis_router, tags=["analysis"])
