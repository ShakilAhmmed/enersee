import pytest
from httpx import AsyncClient
from src.main import app
from httpx import ASGITransport


@pytest.mark.asyncio
async def test_get_users():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as client:
        response = await client.get("/api/v1/users")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_user():
    transport = ASGITransport(app=app)
    payload = {"name": "Test User", "email": "test@example.com"}
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as client:
        response = await client.post("/api/v1/users", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test User"
        assert data["email"] == "test@example.com"
