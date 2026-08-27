SYSTEM_PROMPT = """
You are an AI support triage assistant.

Your job is to analyze customer support tickets using:
1. The customer's ticket.
2. Customer account information when available.
3. Relevant previous tickets.
4. Relevant knowledge-base information.

You must:
- Identify the customer's main issue.
- Determine the appropriate category.
- Assess the urgency.
- Use the provided knowledge-base information when relevant.
- Never invent facts that are not present in the supplied context.
- Clearly indicate when information is unavailable.

Return a concise and professional support analysis.
"""


def build_triage_prompt(context: dict) -> str:
    """Build the prompt used for ticket triage."""

    ticket = context.get("ticket")
    account = context.get("account")
    account_tickets = context.get("account_tickets", [])
    knowledge = context.get("knowledge", [])

    if ticket is None:
        return "No valid ticket was found."

    prompt_parts = [
        "CUSTOMER TICKET",
        f"Ticket ID: {ticket.get('ticket_id', 'N/A')}",
        f"Subject: {ticket.get('subject', 'N/A')}",
        f"Description: {ticket.get('description', 'N/A')}",
        "",
    ]

    prompt_parts.extend(
        [
            "CUSTOMER ACCOUNT",
            str(account) if account else "Account information unavailable.",
            "",
        ]
    )

    prompt_parts.extend(
        [
            "PREVIOUS TICKETS",
            str(account_tickets)
            if account_tickets
            else "No previous tickets available.",
            "",
        ]
    )
    prompt_parts.extend(
        [
            "RISK ASSESSMENT",
            str(context.get("risk"))
            if context.get("risk")
            else "Risk assessment unavailable.",
            "",
            "CUSTOMER SUMMARY",
            str(context.get("summary"))
            if context.get("summary")
            else "Customer summary unavailable.",
            "",
        ]
    )

    prompt_parts.append("KNOWLEDGE BASE")

    if knowledge:
        for index, result in enumerate(knowledge, start=1):
            prompt_parts.extend(
                [
                    f"\nKnowledge Result {index}",
                    f"Source: {result.get('source', 'N/A')}",
                    f"Category: {result.get('category', 'N/A')}",
                    f"Content:\n{result.get('content', '')}",
                ]
            )
    else:
        prompt_parts.append("No relevant knowledge found.")

    return "\n".join(prompt_parts)