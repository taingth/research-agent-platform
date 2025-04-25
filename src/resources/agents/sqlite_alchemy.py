from google.adk.agents import Agent

from ...model_serving.models import LocalModelFactory
from ..mcp_server.mcp_alchemy import get_sqlite_alchemy_client


model = LocalModelFactory().create_model()

async def get_sqlite_alchemy_agent_async():
    sqlite_tool, exit_stack = await get_sqlite_alchemy_client()
    sql_agent = Agent(
        name="sql_agent_v0",
        model=model,
        description="Provides interact with sqlite database.",  # Crucial for delegation later
        instruction="""
        Help user interact with the sqlite database using available tools.
        """,
        tools=sqlite_tool,
    )
    
    return sql_agent, exit_stack
