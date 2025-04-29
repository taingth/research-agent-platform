from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

from .sqlite_agent.agent import get_sqlite_agent


async def get_root_agent():
    sqlite_agent, exit_stack = await get_sqlite_agent()

    agent = Agent(
        model=LiteLlm(model="ollama_chat/qwen2.5:7b"),
        name="root_agent",
        sub_agents=[sqlite_agent],
        instruction="""
        You are a root agent.
        You can use the SQLite agent to handle questions about the SQLite database.
        If the question is not related to the SQLite database, you can answer it directly.
        """,
        generate_content_config=types.GenerateContentConfig(
            temperature=0.3,
        ),
    )

    return agent, exit_stack


root_agent = get_root_agent()
