from contextlib import AsyncExitStack

from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

from .mcp_client import get_brave_search_client, get_sqlite_alchemy_client


async def get_sqlite_agent():
    async_exit_stack = AsyncExitStack()

    sqlite_tools, _ = await get_sqlite_alchemy_client(async_exit_stack=async_exit_stack)

    brave_search_tools, _ = await get_brave_search_client(
        async_exit_stack=async_exit_stack
    )

    # model_name = "openai/Qwen/QwQ-32B-AWQ"
    model_name = "ollama_chat/qwen3:32b"
    agent = LlmAgent(
        model=LiteLlm(
            model=model_name,
        ),
        name="sqlite_agent",
        description="An agent to handle SQLite database queries and can search internet information.",
        instruction="You are a word of class agent. You should answer by Vietnamese language. You can answer and assist questions about the SQLite database with sqlite tool. If you don't know the answer or need search more information real-time or latest, you can search the Brave Search engine.",
        tools=[*sqlite_tools, *brave_search_tools],
        generate_content_config=types.GenerateContentConfig(
            temperature=0.3,
        ),
    )
    return agent, async_exit_stack


root_agent = get_sqlite_agent()
