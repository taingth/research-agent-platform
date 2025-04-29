from google.adk.agents import Agent

from ....model_serving.models import LocalModelFactory
from ..sqlite_agent.sqlite_alchemy import (
    get_sqlite_alchemy_agent_async,
)
from ...tools.get_weather import get_weather

model = LocalModelFactory().create_model()


async def get_main_agent_async():
    # Get sqlite agent
    sqlite_agent, exit_stack = await get_sqlite_alchemy_agent_async()

    # Create the main agent
    agent = Agent(
        name="main_agent_v2",  # Give it a new version name
        model=model,
        description="The main coordinator agent",
        instruction="You are the main Weather Agent coordinating a team. Your primary responsibility is to provide weather information. "
        "Use the 'get_weather' tool ONLY for specific weather requests (e.g., 'weather in London'). "
        "You have specialized a sub-agent: 'sql_agent_v0': Handles SQLite database interactions. "
        "Analyze the user's query. If it requires database interaction, delegate it to the sub-agent. "
        "If the user asks for weather information, use the 'get_weather' tool. "
        "If the user asks for something else, respond appropriately or state you cannot handle it. ",
        tools=[
            get_weather
        ],  # Root agent still needs the weather tool for its core task
        # Key change: Link the sub-agents here!
        sub_agents=[sqlite_agent],
        generate_content_config={"temperature": 0.1},
    )

    return agent, exit_stack
