# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Заглушка для системы агента
class AgentSystem:
    def run(self, input_data: dict) -> dict:
        # Здесь будет логика агента
        return {"status": "success", "input_received": input_data}

agent = AgentSystem()

class AgentRequest(BaseModel):
    data: dict

class AgentResponse(BaseModel):
    status: str
    input_received: dict

@app.post("/run_agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    try:
        result = agent.run(request.data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))