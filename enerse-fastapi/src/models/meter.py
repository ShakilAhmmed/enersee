from datetime import datetime

from sqlalchemy import Column, Integer, Text, String, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.config.database import Base


class Meter(Base):
    __tablename__ = "meters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    # Meta Data
    description = Column(Text, nullable=True)
    unit_type = Column(String(10), nullable=True)
    submeter = Column(Boolean, default=False)
    buildings_site = Column(String(100), nullable=False)
    end_client_id = Column(String(50), nullable=False)
    external_meter_id = Column(String(100), nullable=False)
    main_building_id = Column(Integer, nullable=False)
    sampling_period = Column(Integer, default=15)
    sampling_period_type = Column(String(30), default="MINUTE")
    official_meter = Column(Boolean, default=False)
    is_consumption = Column(Boolean, default=True)

    utility_type = Column(String(20), nullable=False)  # electricity, gas, water, etc.
    category = Column(String(50), nullable=False)  # residential, commercial, industrial
    is_virtual = Column(Boolean, default=False)
    meter_add = Column(JSON, default=list)  # List of meter IDs to add
    meter_sub = Column(JSON, default=list)  # List of meter IDs to subtract
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    consumption_records = relationship("Consumption", back_populates="meter")

class Consumption(Base):
    __tablename__ = "consumptions"

    id = Column(Integer, primary_key=True, index=True)
    meter_id = Column(Integer, ForeignKey("meters.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    energy_use = Column(Float, nullable=False)

    meter = relationship("Meter", back_populates="consumption_records")