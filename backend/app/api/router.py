from fastapi import APIRouter

from app.api.routes.analysis import router as analysis_router
from app.api.routes.report import router as report_router
from app.api.routes.upload import router as upload_router


api_router = APIRouter(
    prefix="/api",
)


api_router.include_router(
    upload_router
)

api_router.include_router(
    analysis_router
)

api_router.include_router(
    report_router
)