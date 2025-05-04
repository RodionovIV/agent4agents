import asyncio

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.client import MultiServerMCPClient

async def get_tools():
    async with MultiServerMCPClient() as client:
        await client.connect_to_server(
            "storywriter",
            command="/home/ts777/datascience/venv/bin/python",
            args=["dummy_mcp_server.py"],
            encoding_error_handler="ignore",
        )
        tools = client.get_tools()
    return tools

if __name__=="__main__":
    # server_params = {
    #     "conversation_saver": {
    #         "url": "http://localhost:3001/tools",
    #         "transport": "sse",
    #     }
    # }
    tools = asyncio.run(get_tools())
    print(tools)