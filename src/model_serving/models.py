# Ensure this import is present from your setup cells
from google.adk.models.lite_llm import LiteLlm


class LocalModelFactory:
    """Factory for creating local models."""

    def __init__(self, model_name: str = "hosted_vllm/Qwen/Qwen2.5-7B-Instruct"):
        self.model_name = model_name

    def create_model(self) -> LiteLlm:
        """Creates and returns a LiteLlm instance."""
        # Here you can add logic to load the model based on the model_name
        # For demonstration, we are just returning a new instance of LiteLlm
        return LiteLlm(
            model=self.model_name,
            api_base="http://localhost:3001/v1",
        )
