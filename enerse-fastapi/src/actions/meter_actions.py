from collections import defaultdict

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from src.models.meter import Meter, Consumption
from src.models.user import User
from src.schemas.meter import CreateMeter
from fastapi import HTTPException, status


class MeterActions:
    @staticmethod
    def create_meter(db: Session, payload: CreateMeter) -> Meter:
        """Create a new meter"""
        try:
            meter = Meter(
                name=payload.name,
                description=payload.description,
                unit_type=payload.unit_type,
                utility_type=payload.utility_type,
                submeter=payload.submeter,
                buildings_site=payload.buildings_site,
                end_client_id=payload.end_client_id,
                external_meter_id=payload.external_meter_id,
                main_building_id=payload.main_building_id,
                sampling_period=payload.sampling_period,
                sampling_period_type=payload.sampling_period_type,
                category=payload.category,
                official_meter=payload.official_meter,
                is_virtual=payload.is_virtual,
                is_consumption=payload.is_consumption,
                meter_add=payload.meter_add,
                meter_sub=payload.meter_sub,
            )
            db.add(meter)
            db.commit()
            db.refresh(meter)
            return meter
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Something went wrong",
            )

    @staticmethod
    def get_meters(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get list of meters"""
        return db.query(Meter).offset(skip).limit(limit).all()

    @staticmethod
    def get_consumption(db: Session, meter_id: int):
        """
        Fetch consumption for a meter.
        If meter is virtual, calculate sum/sub of children on the fly.
        """
        meter = db.query(Meter).filter(Meter.id == meter_id).first()
        if not meter:
            return []

        if not meter.is_virtual:
            # Regular meter: return stored consumption
            return db.query(Consumption).filter(Consumption.meter_id == meter.id).order_by(Consumption.timestamp).all()

        agg = defaultdict(float)
        # Add children
        if meter.meter_add:
            rows = db.query(Consumption).filter(Consumption.meter_id.in_(meter.meter_add)).all()
            for row in rows:
                agg[row.timestamp] += row.energy_use

        # Subtract children
        if meter.meter_sub:
            rows = db.query(Consumption).filter(Consumption.meter_id.in_(meter.meter_sub)).all()
            for r in rows:
                agg[r.timestamp] -= r.energy_use

        # Convert to list of Consumption-like dicts
        result = [{"meter_id": meter.id, "timestamp": ts, "energy_use": val} for ts, val in sorted(agg.items())]
        return result
