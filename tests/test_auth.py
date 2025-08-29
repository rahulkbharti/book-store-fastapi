import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.app import app

BASE_URL = "http://testserver"

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        yield client
    # Explicitly close the transport
    await transport.aclose()

@pytest.mark.asyncio
async def test_hello(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_users(async_client):
    response = await async_client.get("/users/")
    assert response.status_code == 200
