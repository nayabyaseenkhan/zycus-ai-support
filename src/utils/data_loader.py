import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]

TICKETS_PATH = PROJECT_ROOT / "data" / "tickets.json"
ACCOUNTS_PATH = PROJECT_ROOT / "data" / "accounts.json"


def load_json(file_path: Path) -> Any:
    """Load and return JSON data from a file."""
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_tickets() -> list[dict]:
    """Load all support tickets."""
    return load_json(TICKETS_PATH)


def load_accounts() -> list[dict]:
    """Load all customer accounts."""
    return load_json(ACCOUNTS_PATH)


def build_account_lookup(accounts: list[dict]) -> dict[str, dict]:
    """Create an account_id -> account mapping."""
    return {
        account["account_id"]: account
        for account in accounts
    }


def get_ticket(ticket_id: str) -> dict | None:
    """Return a ticket by ticket ID."""
    tickets = load_tickets()

    for ticket in tickets:
        if ticket.get("ticket_id") == ticket_id:
            return ticket

    return None


def get_account(account_id: str) -> dict | None:
    """Return an account by account ID."""
    accounts = load_accounts()

    for account in accounts:
        if account.get("account_id") == account_id:
            return account

    return None


def get_account_tickets(account_id: str) -> list[dict]:
    """Return all tickets belonging to an account."""
    tickets = load_tickets()

    return [
        ticket
        for ticket in tickets
        if ticket.get("account_id") == account_id
    ]


def get_recent_tickets(account_id: str, days: int = 90) -> list[dict]:
    """Return recent tickets for an account.

    Tickets are filtered using their created_at date.
    """
    from datetime import datetime, timedelta

    cutoff_date = datetime.now() - timedelta(days=days)

    account_tickets = get_account_tickets(account_id)

    recent_tickets = []

    for ticket in account_tickets:
        created_at = ticket.get("created_at")

        if not created_at:
            continue

        try:
            ticket_date = datetime.fromisoformat(
                created_at.replace("Z", "+00:00")
            )

            ticket_date = ticket_date.replace(tzinfo=None)

            if ticket_date >= cutoff_date:
                recent_tickets.append(ticket)

        except (ValueError, TypeError):
            continue

    return recent_tickets