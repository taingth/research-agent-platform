from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from google.adk.runners import Runner
from typing import Optional
from google.genai import types 
from google.adk.sessions import InMemorySessionService
from .tool import get_rag_tool
import enum

application/json

def simple_before_model_modifier(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Inspects/modifies the LLM request or skips the call."""
    agent_name = callback_context.agent_name
    print(f"[Callback] Before model call for agent: {agent_name}")

    # Inspect the last user message in the request contents
    last_user_message = ""
    if llm_request.contents and llm_request.contents[-1].role == 'user':
         if llm_request.contents[-1].parts:
            last_user_message = llm_request.contents[-1].parts[0].text
    print(f"[Callback] Inspecting last user message: '{last_user_message}'")

    # --- Modification Example ---
    # Add a prefix to the system instruction
    original_instruction = llm_request.config.system_instruction or types.Content(role="system", parts=[])
    prefix = "[Modified by Callback] "
    # Ensure system_instruction is Content and parts list exists
    if not isinstance(original_instruction, types.Content):
         # Handle case where it might be a string (though config expects Content)
         original_instruction = types.Content(role="system", parts=[types.Part(text=str(original_instruction))])
    if not original_instruction.parts:
        original_instruction.parts.append(types.Part(text="")) # Add an empty part if none exist

    # Modify the text of the first part
    modified_text = prefix + (original_instruction.parts[0].text or "")
    original_instruction.parts[0].text = modified_text
    llm_request.config.system_instruction = original_instruction
    print(f"[Callback] Modified system instruction to: '{modified_text}'")

    # --- Skip Example ---
    # Check if the last user message contains "BLOCK"
    if "BLOCK" in last_user_message.upper():
        print("[Callback] 'BLOCK' keyword found. Skipping LLM call.")
        # Return an LlmResponse to skip the actual LLM call
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="LLM call was blocked by before_model_callback.")],
            )
        )
    else:
        print("[Callback] Proceeding with LLM call.")
        # Return None to allow the (modified) request to go to the LLM
        return None


def handle_media_message_before_model_modifier(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    Inspects/modifies the LLM request or skips the call.
    Example of request contents which contains media message:
    {"parts":[{"text":"hello"},{"inline_data":{"mime_type":"application/json"}}],"role":"user"}
    """
    rag_tool = get_rag_tool()
    agent_name = callback_context.agent_name
    print(f"[Callback] Before model call for agent: {agent_name}")
    
    # Through the contents of the LLM request
    for content in llm_request.contents:
        if content.role == "user":
            for part in content.parts:
                if part.inline_data:
                    print(f"[Callback] Found media message: {part.inline_data}")
                    rag_tool.add(
                        data_type=
                    )
                    # Return an LlmResponse to skip the actual LLM call
                    return LlmResponse(
                        content=types.Content(
                            role="model",
                            parts=[types.Part(text="LLM call was blocked by before_model_callback.")],
                        )
                    )