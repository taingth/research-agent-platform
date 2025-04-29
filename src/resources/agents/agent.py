from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from loguru import logger

model = LiteLlm(
    model="hosted_vllm/Qwen/QwQ-32B-AWQ",
    api_base="http://localhost:3001/v1",
)


async def get_sqlite_alchemy_client():
    logger.info("Attempting to connect to Alchemy client...")
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command="uvx",
            args=[
                "--from",
                "mcp-alchemy==2025.04.16.110003",
                "--refresh-package",
                "mcp-alchemy",
                "mcp-alchemy",
            ],
            env={
                "DB_URL": "sqlite://////home/taint/CodeSpace/adk-samples/agents/agent_demo/db/chinook.db"
            },
        )
    )
    return tools, exit_stack


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


async def get_main_agent_async():
    # Get sqlite agent
    sqlite_agent, exit_stack = await get_sqlite_alchemy_agent_async()

    # Create the main agent
    agent = Agent(
        name="main_agent_v2",  # Give it a new version name
        model=model,
        description="The main coordinator agent",
        instruction="You are the main Agent coordinating a team."
        "You have specialized a sub-agent: 'sql_agent_v0': Handles SQLite database interactions. "
        "Analyze the user's query. If it requires database interaction, delegate it to the sub-agent. "
        "If the user asks for something else, respond appropriately or state you cannot handle it. ",
        # Key change: Link the sub-agents here!
        sub_agents=[sqlite_agent],
        generate_content_config={"temperature": 0.1},
    )

    return agent, exit_stack


root_agent = get_main_agent_async()
