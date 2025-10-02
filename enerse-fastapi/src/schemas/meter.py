from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional
from datetime import datetime


class MeterBase(BaseModel):
    name: str
    description: Optional[str] = None
    unit_type: Optional[str] = None
    submeter: bool = False
    buildings_site: str
    end_client_id: str
    external_meter_id: str
    main_building_id: int
    sampling_period: Optional[int]
    sampling_period_type: Optional[str]
    utility_type: str
    category: str
    official_meter: bool = False
    is_virtual: bool = False
    is_consumption: bool = False
    meter_add: List[int] = Field(default_factory=list)
    meter_sub: List[int] = Field(default_factory=list)


class CreateMeter(MeterBase):
    pass


class MeterResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    unit_type: str
    utility_type: str
    submeter: bool
    buildings_site: str
    end_client_id: str
    external_meter_id: str
    main_building_id: int
    sampling_period: Optional[int]
    sampling_period_type: Optional[str]
    category: str
    utility_type: str
    category: str
    official_meter: bool
    is_virtual: bool
    is_consumption: bool
    meter_add: List[int]
    meter_sub: List[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
