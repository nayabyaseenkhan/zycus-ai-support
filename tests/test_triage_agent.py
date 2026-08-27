from src.triage.agent import TriageAgent


def main():
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

    print(
        f"✓ Related tickets: "
        f"{len(context['account_tickets'])}"
    )

    print(
        f"✓ Knowledge results: "
        f"{len(context['knowledge'])}"
    )

    for result in context["knowledge"]:
        print(
            f"  → {result['source']} "
            f"(score={result['score']:.3f})"
        )

    print("\nTriage agent test passed successfully!")


if __name__ == "__main__":
    main()