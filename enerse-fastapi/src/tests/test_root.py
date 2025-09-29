import pytest
from httpx import AsyncClient
from src.main import app
from httpx import ASGITransport


@pytest.mark.asyncio
async def test_root_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Welcome to Enersee Application"
        assert data["version"] == "1.0.0"
        assert data["docs"] == "/docs"
        assert data["test"] == "Yeah Sync"
