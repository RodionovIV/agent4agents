import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from app.main import run_agent, AgentRequest

@pytest.mark.asyncio
async def test_run_agent_success():
    # Arrange
    request_data = {"foo": "bar"}
    request = AgentRequest(data=request_data)
    mock_result = {"status": "success", "input_received": request_data}

    with patch("app.main.agent") as mock_agent:
        mock_agent.run.return_value = mock_result

        # Act
        response = await run_agent(request)

        # Assert
        assert response == mock_result
        mock_agent.run.assert_called_once_with(request_data)

@pytest.mark.asyncio
async def test_run_agent_failure():
    request_data = {"fail": True}
    request = AgentRequest(data=request_data)

    with patch("app.main.agent") as mock_agent:
        mock_agent.run.side_effect = ValueError("Test exception")

        with pytest.raises(HTTPException) as exc_info:
            await run_agent(request)

        assert exc_info.value.status_code == 500
        assert "Test exception" in str(exc_info.value.detail)