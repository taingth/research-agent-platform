from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types
from google.adk.tools.crewai_tool import CrewaiTool
from .tool import get_rag_tool


def get_rag_agent():
    rag_tool = get_rag_tool()
    adk_RagTool = CrewaiTool(
        tool=rag_tool,
        name="rag_tool",
        description="A tool to answer questions using a knowledge base and add new knowledge to the knowledge base from any sources.",
    )
    
    agent = LlmAgent(
        model=LiteLlm(
            model="ollama_chat/qwen3:32b",
        ),
        name="rag_agent",
        description="An agent to handle knowledge base queries and can search internet information.",
        instruction="You are a word of class agent. You should answer by Vietnamese language. You can answer and assist questions about the knowledge base with rag tool.",
        tools=[adk_RagTool],
        generate_content_config=types.GenerateContentConfig(
            temperature=0.3,
        ),
    )
    
    return agent

root_agent = get_rag_agent()
