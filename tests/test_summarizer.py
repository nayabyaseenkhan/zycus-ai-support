from src.tam.summarizer import TicketSummarizer


def test_summarizer():
    print("Testing ticket summarizer...\n")

    summarizer = TicketSummarizer()

    ticket = {
        "subject": "Unable to login",
        "description": "The user cannot access the account.",
    }

    summary = summarizer.summarize_ticket(ticket)

    assert summary
    assert "Unable to login" in summary

    print("✓ Ticket summary generated")

    history = [
        {
            "subject": "Previous login issue",
            "description": "Login failed.",
        },
        {
            "subject": "Password reset",
            "description": "Password was reset.",
        },
    ]

    history_summary = summarizer.summarize_history(
        history
    )

    assert history_summary
    assert "Previous login issue" in history_summary
    assert "Password reset" in history_summary

    print("✓ Ticket history summarized")

    context = summarizer.summarize_context(
        ticket=ticket,
        account=None,
        account_tickets=history,
    )

    assert context["ticket_summary"]
    assert context["history_summary"]
    assert context["account_available"] is False

    print("✓ Customer context summarized")

    print(
        "\nTicket summarizer test passed successfully!"
    )