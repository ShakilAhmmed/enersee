import pytest
from unittest.mock import patch, AsyncMock
from src.services.consumption_service import fetch_external_meter_values


class MockResponse:
    """Mock aiohttp response"""

    def __init__(self, status, json_data=None, text_data=None):
        self.status = status
        self._json = json_data
        self._text = text_data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def json(self):
        return self._json

    async def text(self):
        return self._text


class MockSession:
    """Mock aiohttp session"""

    def __init__(self, response):
        self._response = response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    def get(self, *args, **kwargs):
        return self._response


@pytest.mark.asyncio
async def test_fetch_external_meter_values_success():
    fake_response = [
        {"timestamp": "2025-09-01T14:00:00+02:00", "value": 36},
        {"timestamp": "2025-09-01T14:15:00+02:00", "value": 30.5},
    ]

    response = MockResponse(200, json_data=fake_response)

    with patch("aiohttp.ClientSession", return_value=MockSession(response)):
        result = await fetch_external_meter_values("648_2000")

        assert len(result) == 2
        assert result[0]["energy_use"] == 36
        assert result[1]["energy_use"] == 30.5


@pytest.mark.asyncio
async def test_fetch_external_meter_values_failure():
    response = MockResponse(500, text_data="Server error")

    with patch("aiohttp.ClientSession", return_value=MockSession(response)):
        result = await fetch_external_meter_values("999")

        assert result == []



