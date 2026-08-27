from src.triage.agent import TriageAgent


def test_triage_agent():
    print("Testing triage agent...\n")

    agent = TriageAgent()

    ticket = agent.account_service.tickets[0]
    ticket_id = ticket["ticket_id"]

    context = agent.build_context(
        ticket_id,
        top_k=3,
    )

    assert context["ticket"] is not None
    assert context["knowledge"]

    print(f"Ticket ID: {ticket_id}")
    print("✓ Ticket context loaded")

    if context["account"]:
        print("✓ Account context loaded")
    else:
        print("✓ Missing account handled gracefully")

    assert isinstance(
        context["account_tickets"],
        list,
    )

    print(
        f"✓ Related tickets: "
        f"{len(context['account_tickets'])}"
    )

    assert len(context["knowledge"]) <= 3

    print(
        f"✓ Knowledge results: "
        f"{len(context['knowledge'])}"
    )

    for result in context["knowledge"]:
        assert result["source"]
        assert result["content"]
        assert "score" in result

        print(
            f"  → {result['source']} "
            f"(score={result['score']:.3f})"
        )

    print("\nTriage agent test passed successfully!")