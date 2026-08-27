from src.utils.llm_client import LLMClient


def main():
    print("Testing LLM client...\n")

    client = LLMClient()

    response = client.generate(
        system_prompt="You are a support assistant.",
        user_prompt="Analyze this support ticket.",
    )

    assert response
    assert isinstance(response, str)

    print("✓ LLM client initialized")
    print("✓ Prompt accepted")
    print("✓ Mock response generated")
    print(f"\nResponse:\n{response}")

    print("\nLLM client test passed successfully!")


if __name__ == "__main__":
    main()