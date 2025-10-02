from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional
from datetime import datetime


class ConsumptionBase(BaseModel):
    meter_id: int
    timestamp: datetime
    energy_use: float


class ConsumptionCreate(ConsumptionBase):
    pass


class ConsumptionResponse(BaseModel):
    id: int
    meter_id: int
    timestamp: datetime
    energy_use: float

    class Config:
        from_attributes = True
