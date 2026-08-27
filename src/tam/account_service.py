from src.utils.data_loader import (
    load_tickets,
    load_accounts,
    build_account_lookup,
)


class AccountService:
    """Service for retrieving customer account and ticket context."""

    def __init__(self):
        self.tickets = load_tickets()
        self.accounts = load_accounts()
        self.account_lookup = build_account_lookup(self.accounts)

    def get_ticket(self, ticket_id: str) -> dict | None:
        """Return a ticket by ticket ID."""

        for ticket in self.tickets:
            if ticket.get("ticket_id") == ticket_id:
                return ticket

        return None

    def get_account(self, account_id: str) -> dict | None:
        """Return an account by account ID."""

        return self.account_lookup.get(account_id)

    def get_account_tickets(self, account_id: str) -> list[dict]:
        """Return all tickets belonging to an account."""

        return [
            ticket
            for ticket in self.tickets
            if ticket.get("account_id") == account_id
        ]

    def get_customer_context(self, ticket_id: str) -> dict:
        """Build customer context for a support ticket."""

        ticket = self.get_ticket(ticket_id)

        if ticket is None:
            return {
                "ticket": None,
                "account": None,
                "account_tickets": [],
            }

        account_id = ticket.get("account_id")
        account = self.get_account(account_id)

        account_tickets = (
            self.get_account_tickets(account_id)
            if account
            else []
        )

        return {
            "ticket": ticket,
            "account": account,
            "account_tickets": account_tickets,
        }