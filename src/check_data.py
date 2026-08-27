from src.utils.data_loader import (
    load_tickets,
    load_accounts,
    build_account_lookup,
)

from src.utils.validators import (
    validate_records,
    REQUIRED_TICKET_FIELDS,
    REQUIRED_ACCOUNT_FIELDS,
)


def main():
    print("Loading Zycus dataset...")

    tickets = load_tickets()
    accounts = load_accounts()

    print(f"Tickets loaded: {len(tickets)}")
    print(f"Accounts loaded: {len(accounts)}")

    validate_records(
        tickets,
        REQUIRED_TICKET_FIELDS,
        "ticket",
    )

    validate_records(
        accounts,
        REQUIRED_ACCOUNT_FIELDS,
        "account",
    )

    account_lookup = build_account_lookup(accounts)

    matched = sum(
        1
        for ticket in tickets
        if ticket["account_id"] in account_lookup
    )

    unmatched = len(tickets) - matched

    print(f"Tickets with matching accounts: {matched}")
    print(f"Tickets with missing accounts: {unmatched}")

    print("\nData validation successful.")


if __name__ == "__main__":
    main()