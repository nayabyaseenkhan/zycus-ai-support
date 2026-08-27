import os

from src.config import LLM_MODEL


class LLMClient:
    """Client interface for interacting with an LLM."""

    def __init__(self):
        self.model = LLM_MODEL
        self.client = None

        # Development mode does not require an external API.
        if self.model == "development-mock":
            return

        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=api_key
        )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """Generate an LLM response."""

        if not system_prompt.strip():
            raise ValueError(
                "System prompt cannot be empty."
            )

        if not user_prompt.strip():
            raise ValueError(
                "User prompt cannot be empty."
            )

        # Local development mode.
        if self.model == "development-mock":
            return (
                "Development-mode response. "
                "The ticket context was processed successfully. "
                "A production LLM should generate the final "
                "classification, reasoning, and recommended response."
            )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0,
        )

        return response.choices[0].message.content or ""