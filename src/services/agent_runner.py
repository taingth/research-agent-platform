# @title Setup Session Service and Runner

from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from loguru import logger

from ..resources.agents.main_agent import (
    get_main_agent_async,  # Assuming this is a tool that fetches weather data
)


async def setup_session_service_and_runner():
    main_agent, exit_stack = await get_main_agent_async()
    # --- Session Management ---
    # Key Concept: SessionService stores conversation history & state.
    # InMemorySessionService is simple, non-persistent storage for this tutorial.
    session_service = InMemorySessionService()
    artifacts_service = InMemoryArtifactService()

    # Define constants for identifying the interaction context
    APP_NAME = "test"
    USER_ID = "user_1_agent_team"
    SESSION_ID = "session_001_agent_team"  # Using a fixed ID for simplicity

    # Create the specific session where the conversation will happen
    session = session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    logger.info(
        f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'"
    )

    # --- Runner ---
    # Key Concept: Runner orchestrates the agent execution loop.
    runner = Runner(
        agent=main_agent,  # The agent we want to run
        app_name=APP_NAME,  # Associates runs with our app
        session_service=session_service,  # Uses our session manager
        artifact_service=artifacts_service,  # Uses our artifact manager
    )
    logger.info(f"Runner created for agent '{runner.agent.name}'.")

    # --- Return the session and runner ---
    return session, runner, exit_stack
