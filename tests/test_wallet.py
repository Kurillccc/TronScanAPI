import pytest
from httpx import AsyncClient
from app.main import app
from httpx import ASGITransport

@pytest.mark.asyncio
async def test_create_wallet_request():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/wallet", json={"wallet_address": "valid_wallet_address"})
    assert response.status_code == 200 or response.status_code == 404

