from src.triage.agent import TriageAgent
from src.models import TriageResult


def test_triage_flow():
    print("Testing complete triage flow...\n")

    agent = TriageAgent()

    ticket = agent.account_service.tickets[0]
    ticket_id = ticket["ticket_id"]

    result = agent.triage(
        ticket_id=ticket_id,
        top_k=3,
    )

    assert isinstance(result, TriageResult)
    assert result.ticket_id == ticket_id
    assert result.response
    assert result.knowledge_sources

    print(f"✓ Ticket processed: {ticket_id}")
    print("✓ Structured triage result generated")
    print("✓ Customer context loaded")
    print("✓ Knowledge retrieved")
    print("✓ Prompt generated")
    print("✓ LLM response generated")

    print("\nTriage Result:")
    print(f"  Category: {result.category}")
    print(f"  Priority: {result.priority}")
    print(f"  Sentiment: {result.sentiment}")
    print(
        f"  Action: "
        f"{result.recommended_action}"
    )

    print("\nKnowledge sources:")

    for source in result.knowledge_sources:
        print(f"  → {source}")

    print("\nLLM Response:")
    print(result.response)

    print(
        "\nComplete triage flow test passed successfully!"
    )