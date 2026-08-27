class TicketSummarizer:
    """Create concise summaries from support ticket context."""

    def summarize_ticket(self, ticket: dict) -> str:
        """Create a short summary of a single ticket."""

        if not ticket:
            return "No ticket information available."

        subject = ticket.get("subject", "No subject")
        description = ticket.get(
            "description",
            "No description available.",
        )

        return (
            f"Subject: {subject}\n"
            f"Issue: {description}"
        )

    def summarize_history(
        self,
        tickets: list[dict],
    ) -> str:
        """Create a summary of previous ticket history."""

        if not tickets:
            return "No previous ticket history available."

        summaries = []

        for ticket in tickets:
            subject = ticket.get(
                "subject",
                "No subject",
            )

            summaries.append(
                f"- {subject}"
            )

        return "\n".join(summaries)

    def summarize_context(
        self,
        ticket: dict,
        account: dict | None,
        account_tickets: list[dict],
    ) -> dict:
        """Create a summarized customer support context."""

        return {
            "ticket_summary": self.summarize_ticket(ticket),
            "history_summary": self.summarize_history(
                account_tickets
            ),
            "account_available": account is not None,
        }