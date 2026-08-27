from src.config import LLM_MODEL


class LLMClient:
    """Client interface for interacting with an LLM."""

    def __init__(self):
        self.model = LLM_MODEL

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """Generate a development-mode LLM response."""

        if not system_prompt.strip():
            raise ValueError("System prompt cannot be empty.")

        if not user_prompt.strip():
            raise ValueError("User prompt cannot be empty.")

        return (
            "Development-mode response. "
            "The ticket context was processed successfully. "
            "A production LLM should generate the final "
            "classification, reasoning, and recommended response."
        )