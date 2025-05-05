from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters


async def get_sqlite_alchemy_client(async_exit_stack = None):
    """Creates and returns an SQLite Alchemy client."""
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
        ),
        async_exit_stack=async_exit_stack,
    )
    return tools, exit_stack


async def get_brave_search_client(async_exit_stack = None):
    """Creates and returns a Brave Search client."""
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command="docker",
            args=["run", "-i", "--rm", "-e", "BRAVE_API_KEY", "mcp/brave-search"],
            env={"BRAVE_API_KEY": "BSAjpQ2RNqMtUyVQKbJYPE5CIhxesck"},
        ),
        async_exit_stack=async_exit_stack,
    )
    return tools, exit_stack
