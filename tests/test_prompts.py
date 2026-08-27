from src.triage.agent import TriageAgent
from src.triage.prompts import (
    SYSTEM_PROMPT,
    build_triage_prompt,
)


def test_triage_prompt():
    print("Testing triage prompt...\n")

    agent = TriageAgent()

    ticket = agent.account_service.tickets[0]
    ticket_id = ticket["ticket_id"]

    context = agent.build_context(
        ticket_id,
        top_k=3,
    )

    prompt = build_triage_prompt(context)

    assert SYSTEM_PROMPT.strip()
    assert prompt.strip()

    assert "CUSTOMER TICKET" in prompt
    assert "KNOWLEDGE BASE" in prompt

    print("✓ System prompt loaded")
    print("✓ Ticket context included")
    print("✓ Knowledge-base context included")
    print("✓ Triage prompt generated")

    print("\nTriage prompt test passed successfully!")