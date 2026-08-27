from src.utils.data_loader import (
    load_tickets,
    load_accounts,
    get_ticket,
    get_account,
    get_account_tickets,
    get_recent_tickets,
)


def test_data_loader():
    print("Testing data loader functions...\n")

    # Load data
    tickets = load_tickets()
    accounts = load_accounts()

    assert tickets
    assert accounts

    print(f"Tickets available: {len(tickets)}")
    print(f"Accounts available: {len(accounts)}")

    # Test get_ticket()
    sample_ticket = tickets[0]
    ticket_id = sample_ticket["ticket_id"]

    ticket = get_ticket(ticket_id)

    assert ticket is not None
    assert ticket["ticket_id"] == ticket_id

    print("✓ get_ticket() passed")

    # Test missing ticket
    missing_ticket = get_ticket(
        "INVALID_TICKET_ID"
    )

    assert missing_ticket is None

    print("✓ Missing ticket handled correctly")

    # Test get_account()
    sample_account = accounts[0]
    account_id = sample_account["account_id"]

    account = get_account(account_id)

    assert account is not None
    assert account["account_id"] == account_id

    print("✓ get_account() passed")

    # Test missing account
    missing_account = get_account(
        "INVALID_ACCOUNT_ID"
    )

    assert missing_account is None

    print("✓ Missing account handled correctly")

    # Test account tickets
    account_tickets = get_account_tickets(
        account_id
    )

    for ticket in account_tickets:
        assert ticket["account_id"] == account_id

    print("✓ get_account_tickets() passed")

    # Test recent tickets
    recent_tickets = get_recent_tickets(
        account_id,
        days=90,
    )

    print("✓ get_recent_tickets() passed")
    print(
        f"  Recent tickets found: "
        f"{len(recent_tickets)}"
    )

    print("\nAll data loader tests passed successfully!")