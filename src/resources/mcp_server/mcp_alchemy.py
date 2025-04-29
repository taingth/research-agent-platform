from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from loguru import logger


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
        # connection_params=StdioServerParameters(
        #     command="uv",
        #     args=[
        #         "--directory",
        #         "/home/taint/CodeSpace/adk-samples/agents/servers/src/sqlite",
        #         "run",
        #         "mcp-server-sqlite",
        #         "--db-path",
        #         "home/taint/CodeSpace/adk-samples/agents/agent_demo/db/chinook.db",
        #     ],
        # )
    )
    return tools, exit_stack
