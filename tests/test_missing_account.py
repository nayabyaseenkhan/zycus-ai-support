from src.tam.account_service import AccountService


def main():
    print("Testing missing-account handling...\n")

    service = AccountService()

    missing_account_ticket = None

    for ticket in service.tickets:
        account_id = ticket.get("account_id")

        if account_id and service.get_account(account_id) is None:
            missing_account_ticket = ticket
            break

    assert missing_account_ticket is not None

    ticket_id = missing_account_ticket["ticket_id"]

    context = service.get_customer_context(ticket_id)

    assert context["ticket"] is not None
    assert context["account"] is None

    print(f"Ticket tested: {ticket_id}")
    print("✓ Ticket found")
    print("✓ Missing account detected")
    print("✓ Missing account handled gracefully")

    print("\nMissing-account test passed successfully!")


if __name__ == "__main__":
    main()