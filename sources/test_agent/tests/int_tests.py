import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_run_agent_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"data": {"key": "value"}}
        response = await ac.post("/run_agent", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["input_received"] == {"key": "value"}

@pytest.mark.asyncio
async def test_run_agent_empty_data():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"data": {}}
        response = await ac.post("/run_agent", json=payload)
    assert response.status_code == 200
    assert response.json()["input_received"] == {}