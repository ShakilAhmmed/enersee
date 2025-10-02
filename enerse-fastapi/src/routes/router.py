from fastapi import APIRouter
from src.controllers.api.v1 import meters

router = APIRouter()
router.include_router(meters.router, prefix="/meters", tags=["meters"])
