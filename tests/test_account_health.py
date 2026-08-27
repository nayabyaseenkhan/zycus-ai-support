from src.tam.account_service import AccountService
from src.tam.summarizer import TicketSummarizer


def main():
    print("Testing TAM account health summarizer...")

    account_service = AccountService()
    summarizer = TicketSummarizer()

    accounts = account_service.accounts

    if not accounts:
        raise AssertionError("No accounts available.")

    account_id = accounts[0]["account_id"]

    print(f"Testing account: {account_id}")

    account = account_service.get_account(account_id)

    if account is None:
        raise AssertionError(
            "Account could not be loaded."
        )

    print("✓ Account loaded")

    tickets = account_service.get_account_tickets(
        account_id
    )

    print(
        f"✓ Account tickets loaded: {len(tickets)}"
    )

    recent_tickets = (
        summarizer.get_last_90_days_tickets(
            tickets
        )
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
        if section not in brief:
            raise AssertionError(
                f"Missing section: {section}"
            )

        print(
            f"✓ {section} generated"
        )

    if not brief["executive_summary"]:
        raise AssertionError(
            "Executive summary is empty."
        )

    if not isinstance(
        brief["open_risks"],
        list,
    ):
        raise AssertionError(
            "Open risks must be a list."
        )

    if not isinstance(
        brief["recommended_talking_points"],
        list,
    ):
        raise AssertionError(
            "Talking points must be a list."
        )

    # Verify deterministic output.
    brief_again = (
        summarizer.generate_account_brief(
            account_id=account_id,
            account=account,
            tickets=tickets,
        )
    )

    if brief != brief_again:
        raise AssertionError(
            "Account brief is not deterministic."
        )

    print(
        "✓ Deterministic output verified"
    )

    # Verify direct quotes for risk flags.
    for flag in brief["risk_flags"]:
        if not flag.get("quote"):
            raise AssertionError(
                "Risk flag does not contain "
                "a direct ticket quote."
            )

    print(
        "✓ Risk flags contain direct ticket quotes"
    )

    print()
    print("Executive Summary:")
    print(brief["executive_summary"])

    print()
    print("Open Risks & Flagged Issues:")

    for risk in brief["open_risks"]:
        print(
            f"- {risk['type']}"
        )

        if risk.get("ticket_id"):
            print(
                f"  Ticket: {risk['ticket_id']}"
            )

        print(
            f"  Reason: {risk['reason']}"
        )

        if risk.get("quote"):
            print(
                f"  Quote: \"{risk['quote']}\""
            )

    print()
    print("Recommended Talking Points:")

    for point in brief[
        "recommended_talking_points"
    ]:
        print(
            f"- {point}"
        )

    print()
    print(
        "TAM account health test passed successfully!"
    )


if __name__ == "__main__":
    main()