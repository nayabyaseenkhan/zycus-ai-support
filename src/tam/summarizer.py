from datetime import datetime, timedelta
from typing import Any


class TicketSummarizer:
    """Create deterministic account health summaries for TAMs."""

    NEGATIVE_SIGNALS = [
        "angry",
        "frustrated",
        "unhappy",
        "dissatisfied",
        "cancel",
        "cancellation",
        "churn",
        "leaving",
        "switch",
        "competitor",
        "escalate",
        "escalation",
        "critical",
        "urgent",
        "blocked",
        "blocking",
        "outage",
        "not working",
        "failed",
        "failure",
        "unable",
        "cannot",
    ]

    ESCALATION_SIGNALS = [
        "escalate",
        "escalation",
        "critical",
        "urgent",
        "blocked",
        "blocking",
        "outage",
        "production down",
        "cannot access",
        "unable to access",
    ]

    CHURN_SIGNALS = [
        "cancel",
        "cancellation",
        "churn",
        "leaving",
        "switch",
        "competitor",
        "dissatisfied",
        "unhappy",
    ]

    def summarize_ticket(self, ticket: dict) -> str:
        """Create a short summary of a single ticket."""

        if not ticket:
            return "No ticket information available."

        subject = ticket.get(
            "subject",
            "No subject",
        )

        description = ticket.get(
            "description",
            "No description available.",
        )

        if not description:
            description = "No description available."

        return (
            f"Subject: {subject}\n"
            f"Issue: {description}"
        )

    def summarize_history(
        self,
        tickets: list[dict],
    ) -> str:
        """Create a deterministic summary of ticket history."""

        if not tickets:
            return "No previous ticket history available."

        summaries = []

        for ticket in tickets:
            ticket_id = ticket.get(
                "ticket_id",
                "Unknown",
            )

            subject = ticket.get(
                "subject",
                "No subject",
            )

            summaries.append(
                f"- {ticket_id}: {subject}"
            )

        return "\n".join(summaries)

    def summarize_context(
        self,
        ticket: dict,
        account: dict | None,
        account_tickets: list[dict],
    ) -> dict:
        """Create summarized customer support context."""

        return {
            "ticket_summary": self.summarize_ticket(
                ticket
            ),
            "history_summary": self.summarize_history(
                account_tickets
            ),
            "account_available": account is not None,
        }

    def get_last_90_days_tickets(
        self,
        tickets: list[dict],
        reference_date: datetime | None = None,
    ) -> list[dict]:
        """Return tickets created during the last 90 days."""

        if not tickets:
            return []

        if reference_date is None:
            reference_date = datetime.now()

        cutoff_date = (
            reference_date - timedelta(days=90)
        )

        recent_tickets = []

        for ticket in tickets:
            created_at = ticket.get(
                "created_at"
            )

            if not created_at:
                continue

            try:
                ticket_date = datetime.fromisoformat(
                    str(created_at).replace(
                        "Z",
                        "+00:00",
                    )
                )

                if ticket_date.tzinfo is not None:
                    ticket_date = ticket_date.replace(
                        tzinfo=None
                    )

                if ticket_date >= cutoff_date:
                    recent_tickets.append(ticket)

            except (
                ValueError,
                TypeError,
            ):
                continue

        return recent_tickets

    def detect_risk_flags(
        self,
        tickets: list[dict],
    ) -> list[dict]:
        """Detect churn and escalation signals."""

        flags = []

        for ticket in tickets:
            ticket_id = ticket.get(
                "ticket_id",
                "Unknown",
            )

            subject = str(
                ticket.get(
                    "subject",
                    "",
                )
            )

            description = str(
                ticket.get(
                    "description",
                    "",
                )
            )

            text = (
                f"{subject} {description}"
            ).strip()

            text_lower = text.lower()

            if not text:
                continue

            churn_matches = [
                signal
                for signal in self.CHURN_SIGNALS
                if signal in text_lower
            ]

            escalation_matches = [
                signal
                for signal in self.ESCALATION_SIGNALS
                if signal in text_lower
            ]

            if churn_matches:
                quote = self._create_quote(
                    subject,
                    description,
                    churn_matches[0],
                )

                flags.append(
                    {
                        "ticket_id": ticket_id,
                        "type": "Churn risk",
                        "reason": (
                            "The ticket contains language "
                            "that may indicate customer "
                            "dissatisfaction or potential "
                            "churn."
                        ),
                        "quote": quote,
                    }
                )

            if escalation_matches:
                quote = self._create_quote(
                    subject,
                    description,
                    escalation_matches[0],
                )

                flags.append(
                    {
                        "ticket_id": ticket_id,
                        "type": "Escalation risk",
                        "reason": (
                            "The ticket contains an "
                            "escalation or service-impact "
                            "signal."
                        ),
                        "quote": quote,
                    }
                )

        return flags

    def _create_quote(
        self,
        subject: str,
        description: str,
        signal: str,
    ) -> str:
        """Create a short direct quote containing the signal."""

        source_text = (
            description
            if description
            else subject
        )

        words = source_text.split()

        if not words:
            return subject

        lower_words = [
            word.lower().strip(
                ".,!?;:\"'()[]{}"
            )
            for word in words
        ]

        signal_words = signal.lower().split()

        match_index = -1

        for index in range(
            len(lower_words)
        ):
            if all(
                index + offset < len(lower_words)
                and signal_word
                in lower_words[index + offset]
                for offset, signal_word
                in enumerate(signal_words)
            ):
                match_index = index
                break

        if match_index == -1:
            return source_text[:200]

        start = max(
            0,
            match_index - 8,
        )

        end = min(
            len(words),
            match_index + len(signal_words) + 8,
        )

        quote = " ".join(
            words[start:end]
        )

        return quote[:250]

    def generate_account_brief(
        self,
        account_id: str,
        account: dict | None,
        tickets: list[dict],
    ) -> dict:
        """Generate the complete deterministic TAM account brief."""

        recent_tickets = self.get_last_90_days_tickets(
            tickets
        )

        risk_flags = self.detect_risk_flags(
            recent_tickets
        )

        account_name = self._get_account_name(
            account,
            account_id,
        )

        account_status = self._get_account_value(
            account,
            [
                "status",
                "account_status",
                "health_status",
            ],
            "Unknown",
        )

        plan = self._get_account_value(
            account,
            [
                "plan",
                "subscription",
                "subscription_plan",
            ],
            "Unknown",
        )

        executive_summary = (
            self._build_executive_summary(
                account_name=account_name,
                account_status=account_status,
                plan=plan,
                recent_tickets=recent_tickets,
                risk_flags=risk_flags,
            )
        )

        open_risks = self._build_open_risks(
            risk_flags,
            recent_tickets,
        )

        talking_points = (
            self._build_talking_points(
                account_status=account_status,
                recent_tickets=recent_tickets,
                risk_flags=risk_flags,
            )
        )

        return {
            "account_id": account_id,
            "account_name": account_name,
            "executive_summary": executive_summary,
            "open_risks": open_risks,
            "recommended_talking_points": (
                talking_points
            ),
            "recent_ticket_count": len(
                recent_tickets
            ),
            "risk_flags": risk_flags,
        }

    def _build_executive_summary(
        self,
        account_name: str,
        account_status: str,
        plan: str,
        recent_tickets: list[dict],
        risk_flags: list[dict],
    ) -> str:
        """Build a deterministic 3–5 sentence summary."""

        ticket_count = len(
            recent_tickets
        )

        risk_count = len(
            risk_flags
        )

        sentence_one = (
            f"{account_name} is currently "
            f"listed with account status "
            f"'{account_status}' and plan "
            f"'{plan}'."
        )

        sentence_two = (
            f"The account has {ticket_count} "
            f"support ticket(s) in the last "
            f"90 days."
        )

        if risk_count:
            sentence_three = (
                f"{risk_count} risk signal(s) were "
                f"identified from the recent "
                f"ticket history."
            )
        else:
            sentence_three = (
                "No churn or escalation signals "
                "were identified in the recent "
                "ticket history."
            )

        sentence_four = (
            "The QBR discussion should focus on "
            "recent support activity, unresolved "
            "issues, and any customer-impacting "
            "patterns."
        )

        return " ".join(
            [
                sentence_one,
                sentence_two,
                sentence_three,
                sentence_four,
            ]
        )

    def _build_open_risks(
        self,
        risk_flags: list[dict],
        recent_tickets: list[dict],
    ) -> list[dict]:
        """Build risk section with direct ticket quotes."""

        if not risk_flags:
            return [
                {
                    "type": "No flagged risks",
                    "ticket_id": None,
                    "reason": (
                        "No churn or escalation "
                        "signals were detected "
                        "in the last 90 days."
                    ),
                    "quote": None,
                }
            ]

        return risk_flags

    def _build_talking_points(
        self,
        account_status: str,
        recent_tickets: list[dict],
        risk_flags: list[dict],
    ) -> list[str]:
        """Generate actionable TAM talking points."""

        talking_points = []

        talking_points.append(
            "Review the account's current "
            f"status ({account_status}) and "
            "confirm whether any customer "
            "health concerns require attention."
        )

        if recent_tickets:
            talking_points.append(
                f"Discuss the {len(recent_tickets)} "
                "support ticket(s) recorded in "
                "the last 90 days and confirm "
                "whether the recurring issues "
                "have been resolved."
            )
        else:
            talking_points.append(
                "Confirm that the account has "
                "no recent support issues requiring "
                "TAM follow-up."
            )

        if risk_flags:
            talking_points.append(
                "Review each flagged churn or "
                "escalation signal with the customer "
                "and agree on concrete follow-up "
                "actions."
            )
        else:
            talking_points.append(
                "Ask whether there are any "
                "unreported product, support, "
                "or adoption concerns."
            )

        talking_points.append(
            "Identify any upcoming customer "
            "needs, configuration changes, or "
            "support priorities that should be "
            "tracked after the QBR."
        )

        return talking_points

    def _get_account_name(
        self,
        account: dict | None,
        account_id: str,
    ) -> str:
        """Extract an account/customer name safely."""

        if not account:
            return account_id

        return self._get_account_value(
            account,
            [
                "customer_name",
                "account_name",
                "company_name",
                "name",
            ],
            account_id,
        )

    def _get_account_value(
        self,
        account: dict | None,
        keys: list[str],
        default: Any,
    ) -> Any:
        """Read the first available account field."""

        if not account:
            return default

        for key in keys:
            value = account.get(key)

            if value not in (
                None,
                "",
            ):
                return value

        return default