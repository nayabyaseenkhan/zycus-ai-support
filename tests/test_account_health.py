from src.tam.account_service import AccountService
from src.tam.summarizer import TicketSummarizer


def test_account_health():
    print("Testing TAM account health summarizer...")

    account_service = AccountService()
    summarizer = TicketSummarizer()

    accounts = account_service.accounts

    assert accounts, "No accounts available."

    account_id = accounts[0]["account_id"]

    print(f"Testing account: {account_id}")

    account = account_service.get_account(account_id)

    assert account is not None, "Account could not be loaded."

    print("✓ Account loaded")

    tickets = account_service.get_account_tickets(account_id)

    print(
        f"✓ Account tickets loaded: {len(tickets)}"
    )

    recent_tickets = summarizer.get_last_90_days_tickets(
        tickets
    )

    print(
        f"✓ Last 90 days tickets calculated: "
        f"{len(recent_tickets)}"
    )

    risk_flags = summarizer.detect_risk_flags(
        recent_tickets
    )

    print(
        f"✓ Risk detection completed: "
        f"{len(risk_flags)} flag(s)"
    )

    brief = summarizer.generate_account_brief(
        account_id=account_id,
        account=account,
        tickets=tickets,
    )

    required_sections = [
        "executive_summary",
        "open_risks",
        "recommended_talking_points",
    ]

    for section in required_sections:
        assert section in brief, f"Missing section: {section}"
        print(f"✓ {section} generated")

    assert brief["executive_summary"], (
        "Executive summary is empty."
    )

    assert isinstance(brief["open_risks"], list), (
        "Open risks must be a list."
    )

    assert isinstance(
        brief["recommended_talking_points"],
        list,
    ), "Talking points must be a list."

    # Verify deterministic output.
    brief_again = summarizer.generate_account_brief(
        account_id=account_id,
        account=account,
        tickets=tickets,
    )

    assert brief == brief_again, (
        "Account brief is not deterministic."
    )

    print("✓ Deterministic output verified")

    # Verify direct quotes for risk flags.
    for flag in brief["risk_flags"]:
        assert flag.get("quote"), (
            "Risk flag does not contain a direct ticket quote."
        )

    print("✓ Risk flags contain direct ticket quotes")

    print()
    print("Executive Summary:")
    print(brief["executive_summary"])

    print()
    print("Open Risks & Flagged Issues:")

    for risk in brief["open_risks"]:
        print(f"- {risk['type']}")

        if risk.get("ticket_id"):
            print(f"  Ticket: {risk['ticket_id']}")

        print(f"  Reason: {risk['reason']}")

        if risk.get("quote"):
            print(f'  Quote: "{risk["quote"]}"')

    print()
    print("Recommended Talking Points:")

    for point in brief["recommended_talking_points"]:
        print(f"- {point}")

    print()
    print("TAM account health test passed successfully!")