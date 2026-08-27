from src.tam.account_service import AccountService


def main():
    print("Testing account service...\n")

    service = AccountService()

    assert service.tickets
    assert service.accounts

    print(f"Tickets available: {len(service.tickets)}")
    print(f"Accounts available: {len(service.accounts)}")

    # Test a real ticket
    ticket = service.tickets[0]
    ticket_id = ticket["ticket_id"]

    result = service.get_ticket(ticket_id)

    assert result is not None
    assert result["ticket_id"] == ticket_id

    print("✓ get_ticket() passed")

    # Test missing ticket
    missing_ticket = service.get_ticket("non-existent-ticket")

    assert missing_ticket is None

    print("✓ Missing ticket handled correctly")

    # Test customer context
    context = service.get_customer_context(ticket_id)

    assert context["ticket"] is not None

    print("✓ Customer context generated")

    if context["account"]:
        print("✓ Matching account found")
        print(
            f"  Account tickets: "
            f"{len(context['account_tickets'])}"
        )
    else:
        print("✓ Missing account handled gracefully")

    print("\nAccount service test passed successfully!")


if __name__ == "__main__":
    main()