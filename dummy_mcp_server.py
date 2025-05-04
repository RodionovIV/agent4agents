from fastmcp import FastMCP
import os
from datetime import datetime
import uvicorn

mcp = FastMCP("ConversationSaver")

@mcp.tool()
def save_conversation(conversation: str) -> str:
    """Сохраняет переданный текст в файл на рабочем столе с временной меткой."""
    desktop_path = os.path.expanduser("~/Code/agent4agents/instruments_results")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(desktop_path, f"conversation_{timestamp}.txt")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(conversation)
        return f"Разговор сохранён по пути: {file_path}"
    except Exception as e:
        return f"Ошибка при сохранении: {str(e)}"

if __name__ == "__main__":
#     uvicorn.run(mcp_server(), host="0.0.0.0", port=3333, reload=True)
   mcp.run()