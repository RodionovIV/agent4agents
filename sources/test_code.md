# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Реализация агента, который складывает два числа
class AgentSystem:
    def run(self, input_data: dict) -> dict:
        # Проверяем, что в input_data есть оба числа
        if "num1" not in input_data or "num2" not in input_data:
            raise HTTPException(status_code=400, detail="Оба числа должны быть указаны")
        
        # Складываем числа
        result = input_data["num1"] + input_data["num2"]
        
        return {"status": "success", "result": result}

agent = AgentSystem()

# Протокол запроса к агенту
class AgentRequest(BaseModel):
    num1: float
    num2: float

# Протокол ответа от агента
class AgentResponse(BaseModel):
    status: str
    result: float

# Обработчик запроса к агенту
@app.post("/run_agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    try:
        result = agent.run(request.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)