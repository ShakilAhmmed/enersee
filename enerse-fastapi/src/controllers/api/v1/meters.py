import logging

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from src.actions.meter_actions import MeterActions
from src.config.database import get_db
from src.schemas.consumption import ConsumptionResponse
from src.schemas.meter import MeterResponse, CreateMeter
from src.schemas.response import APIResponse
from src.schemas.user import UserCreate, UserUpdate, UserResponse
from src.actions.user_actions import UserActions
from fastapi import BackgroundTasks

from src.services.consumption_service import fetch_and_store_meter_consumption

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=APIResponse[MeterResponse], status_code=status.HTTP_201_CREATED)
def create_meters(meter: CreateMeter, background_tasks: BackgroundTasks = None, db: Session = Depends(get_db)):
    """Create a new meter"""
    try:
        meter = MeterActions.create_meter(db, meter)
        if meter.external_meter_id:
            logger.debug("Background task added for consumption records for meter %s", meter.external_meter_id)
            background_tasks.add_task(fetch_and_store_meter_consumption, meter.id)
        return APIResponse(
            message="Meter Created Successfully.",
            data=meter,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return APIResponse[None](
            message=f"Error creating meter: {str(e)}",
            data=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/", response_model=APIResponse[List[MeterResponse]])
def list_meters(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: Session = Depends(get_db)
):
    """Get list of meters"""
    try:
        meters = MeterActions.get_meters(db, skip, limit)
        return APIResponse(
            message="Meters fetched successfully",
            data=meters,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return APIResponse[None](
            message=f"Error fetching meters: {str(e)}",
            data=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/consumption/{meter_id}", response_model=APIResponse[List[ConsumptionResponse]])
def consumption(meter_id: int, db: Session = Depends(get_db)):
    try:
        consumptions = MeterActions.get_consumption(db, meter_id)
        return APIResponse(
            message="Computions fetched successfully",
            data=consumptions,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return APIResponse[None](
            message=f"Error fetching consumptions: {str(e)}",
            data=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
