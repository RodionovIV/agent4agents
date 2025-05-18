import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from app.main import run_agent, AgentRequest, AgentResponse, AgentSystem

# Тестирование успешного выполнения агента
@pytest.mark.asyncio
async def test_run_agent_success():
    # Arrange
    request_data = {"num1": 5.0, "num2": 3.0}
    request = AgentRequest(**request_data)
    expected_result = {"status": "success", "result": 8.0}

    with patch.object(AgentSystem, "run", return_value=expected_result) as mock_agent_run:
        # Act
        response = await run_agent(request)
        print(response)

        # Assert
        assert isinstance(response, AgentResponse)
        assert response.status == "success"
        assert response.result == 8.0
        mock_agent_run.assert_called_once_with(request.dict())

# Тестирование обработки ошибки при отсутствии обязательных полей
@pytest.mark.asyncio
async def test_run_agent_missing_fields():
    # Arrange
    request_data = {"num1": 5.0}
    request = AgentRequest(**request_data)

    with patch.object(AgentSystem, "run", side_effect=HTTPException(status_code=400, detail="Оба числа должны быть указаны")) as mock_agent_run:
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await run_agent(request)

        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Оба числа должны быть указаны"
        mock_agent_run.assert_called_once_with(request.dict())

# Тестирование обработки внутренней ошибки
@pytest.mark.asyncio
async def test_run_agent_internal_error():
    # Arrange
    request_data = {"num1": 5.0, "num2": 3.0}
    request = AgentRequest(**request_data)

    with patch.object(AgentSystem, "run", side_effect=Exception("Internal error")) as mock_agent_run:
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await run_agent(request)

        assert exc_info.value.status_code == 500
        assert "Internal error" in str(exc_info.value.detail)
        mock_agent_run.assert_called_once_with(request.dict())