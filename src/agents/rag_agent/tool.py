from crewai_tools import RagTool
import yaml


def get_rag_tool():
    config_path = "src/agents/rag_agent/config/embedchain.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    rag_tool = RagTool(config=config)
    rag_tool.add(data_type="pdf_file", source="/home/taint/CodeSpace/adk-samples/agents/agent_demo/data/GCP Professional Cloud Architect Crash Course - Day 1.pdf")
    return rag_tool
