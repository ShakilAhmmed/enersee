from datetime import datetime
from typing import List, Dict

from src.config.config import get_settings
from src.config.database import SessionLocal
from src.models.meter import Meter, Consumption
import logging
import aiohttp

logger = logging.getLogger(__name__)
settings = get_settings()


async def fetch_and_store_meter_consumption(meter_id: int):
    """Fetch consumption from external API and store in DB."""
    try:
        with SessionLocal() as db:
            meter = db.query(Meter).filter(Meter.id == meter_id).first()
            if not meter or not meter.external_meter_id:
                logger.warning("No external meter found for %s", meter_id)
                return

            logger.info("Fetching consumption for meter %s", meter_id)

            # Example: fetch last 30 days
            now = datetime.utcnow()
            from_dt = (now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)).strftime("%Y-%m-%d %H:%M")
            to_dt = now.strftime("%Y-%m-%d %H:%M")

            items = await fetch_external_meter_values(
                meter.external_meter_id, from_dt=from_dt, to_dt=to_dt
            )

            for item in items:
                ts = datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00"))
                db_item = Consumption(
                    meter_id=meter.id,
                    timestamp=ts,
                    energy_use=item["energy_use"]
                )
                db.add(db_item)

            db.commit()
            logger.info("Stored %d consumption records for meter %s", len(items), meter_id)

    except Exception as e:
        logger.exception("Failed to fetch/store consumption for meter %s: %s", meter_id, e)


async def fetch_external_meter_values(meter_id: int, from_dt: str = None, to_dt: str = None) -> List[
    Dict]:
    """Call external API and return a list of {timestamp, energy_use} dicts.
    """
    if not settings.EXTERNAL_API_KEY:
        raise RuntimeError("EXTERNAL_API_KEY not configured")

    url = f"{settings.EXTERNAL_API_BASE}/api/Meters/GetValues{meter_id}"
    params = {"from": from_dt, "to": to_dt}
    headers = {"x-functions-key": settings.EXTERNAL_API_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status != 200:
                text = await resp.text()
                logger.error("Failed to fetch external meter data: %s", text)
                return []
            data = await resp.json()
            # Transform to internal format
            results = [{"timestamp": item["timestamp"], "energy_use": item["value"]} for item in data]
            logger.debug("Fetched %d consumption records for meter %s", len(results), meter_id)
            return results
