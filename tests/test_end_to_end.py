from src.triage.agent import TriageAgent
from src.models import TriageResult


def test_end_to_end_triage():
    print("Testing end-to-end triage scenarios...\n")

    agent = TriageAgent()

    # Scenario 1: Valid ticket
    ticket = agent.account_service.tickets[0]
    ticket_id = ticket["ticket_id"]

    result = agent.triage(
        ticket_id=ticket_id,
        top_k=3,
    )

    assert isinstance(result, TriageResult)
    assert result.ticket_id == ticket_id
    assert result.response

    print("✓ Valid ticket processed successfully")

    # Scenario 2: Find a ticket with a missing account
    missing_account_ticket = None

    for ticket in agent.account_service.tickets:
        account_id = ticket.get("account_id")

        if (
            account_id
            and agent.account_service.get_account(account_id) is None
        ):
            missing_account_ticket = ticket
            break

    assert missing_account_ticket is not None

    missing_account_ticket_id = (
        missing_account_ticket["ticket_id"]
    )

    result = agent.triage(
        ticket_id=missing_account_ticket_id,
        top_k=3,
    )

    assert isinstance(result, TriageResult)
    assert result.ticket_id == missing_account_ticket_id

    print(
        "✓ Missing-account ticket processed successfully"
    )

    # Scenario 3: Invalid ticket
    invalid_ticket_id = "invalid-ticket-id"

    try:
        agent.triage(
            ticket_id=invalid_ticket_id,
            top_k=3,
        )

        assert False, (
            "Expected ValueError was not raised."
        )

    except ValueError:
        print("✓ Invalid ticket handled correctly")

    print("\nEnd-to-end test passed successfully!")