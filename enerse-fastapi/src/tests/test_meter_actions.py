import pytest
from unittest.mock import patch
from src.services.consumption_service import fetch_and_store_meter_consumption
from src.models.meter import Meter, Consumption


@pytest.mark.asyncio
async def test_fetch_and_store_meter_consumption_success(db_session):
    # Arrange: add a meter
    meter = Meter(
        id=1,
        name="Test Meter",
        utility_type="electricity",
        category="residential",
        is_virtual=False,
        meter_add=[],
        meter_sub=[],
        main_building_id="B1",
        external_meter_id="648_2000"
    )
    db_session.add(meter)
    db_session.commit()

    fake_response = [
        {"timestamp": "2025-09-01T14:00:00+02:00", "value": 36},
        {"timestamp": "2025-09-01T14:15:00+02:00", "value": 30.5},
    ]

    async def mock_fetch(*args, **kwargs):
        return [{"timestamp": item["timestamp"], "energy_use": item["value"]} for item in fake_response]

    with patch("src.services.consumption_service.fetch_external_meter_values", side_effect=mock_fetch):
        await fetch_and_store_meter_consumption(1)

    # Assert
    rows = db_session.query(Consumption).filter(Consumption.meter_id == 1).all()
    assert len(rows) == 2
    assert rows[0].energy_use == 36
    assert rows[1].energy_use == 30.5


@pytest.mark.asyncio
async def test_fetch_and_store_meter_consumption_no_external(db_session):
    # Arrange: meter without external ID
    meter = Meter(
        id=2,
        name="Local Only",
        utility_type="gas",
        category="industrial",
        is_virtual=False,
        meter_add=[],
        meter_sub=[],
        main_building_id="B2",
        external_meter_id=None
    )
    db_session.add(meter)
    db_session.commit()

    # Act
    await fetch_and_store_meter_consumption(2)

    # Assert (no consumption saved)
    rows = db_session.query(Consumption).filter(Consumption.meter_id == 2).all()
    assert len(rows) == 0
