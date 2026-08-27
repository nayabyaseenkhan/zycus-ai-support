from src.tam.account_service import AccountService
from src.tam.risk_detector import RiskDetector
from src.tam.summarizer import TicketSummarizer

from src.triage.retriever import KnowledgeBaseRetriever
from src.triage.prompts import (
    SYSTEM_PROMPT,
    build_triage_prompt,
)

from src.utils.llm_client import LLMClient
from src.models import TriageResult


class TriageAgent:
    """AI agent for customer support ticket triage."""

    def __init__(self):
        self.account_service = AccountService()
        self.risk_detector = RiskDetector()
        self.summarizer = TicketSummarizer()
        self.retriever = KnowledgeBaseRetriever()
        self.llm_client = LLMClient()

    def build_context(
        self,
        ticket_id: str,
        top_k: int = 3,
    ) -> dict:
        """Build complete context for a support ticket."""

        customer_context = (
            self.account_service.get_customer_context(ticket_id)
        )

        ticket = customer_context["ticket"]

        if ticket is None:
            return {
                "ticket": None,
                "account": None,
                "account_tickets": [],
                "knowledge": [],
                "risk": None,
                "summary": None,
            }

        query_parts = [
            ticket.get("subject", ""),
            ticket.get("description", ""),
        ]

        query = " ".join(
            part
            for part in query_parts
            if part
        )

        knowledge = self.retriever.search(
            query,
            top_k=top_k,
        )

        risk = self.risk_detector.assess(ticket)

        summary = self.summarizer.summarize_context(
            ticket=ticket,
            account=customer_context["account"],
            account_tickets=customer_context["account_tickets"],
        )

        return {
            "ticket": ticket,
            "account": customer_context["account"],
            "account_tickets": customer_context["account_tickets"],
            "knowledge": knowledge,
            "risk": risk,
            "summary": summary,
        }

    def triage(
        self,
        ticket_id: str,
        top_k: int = 3,
    ) -> TriageResult:
        """Analyze a support ticket and return structured triage."""

        context = self.build_context(
            ticket_id=ticket_id,
            top_k=top_k,
        )

        if context["ticket"] is None:
            raise ValueError(
                f"Ticket '{ticket_id}' was not found."
            )

        user_prompt = build_triage_prompt(context)

        response = self.llm_client.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        risk = context["risk"]

        priority = (
            "high"
            if risk and risk.is_high_risk
            else "normal"
        )

        category = self.classify_category(
            context["ticket"]
        )

        sentiment = self._classify_sentiment(
            context["ticket"]
        )

        recommended_action = self._recommend_action(
            risk=risk,
            category=category,
        )

        knowledge_sources = list(
            dict.fromkeys(
                result["source"]
                for result in context["knowledge"]
            )
        )

        return TriageResult(
            ticket_id=ticket_id,
            category=category,
            priority=priority,
            sentiment=sentiment,
            is_high_risk=(
                risk.is_high_risk
                if risk
                else False
            ),
            risk_level=(
                risk.risk_level
                if risk
                else "unknown"
            ),
            risk_reasons=(
                risk.risk_reasons
                if risk
                else []
            ),
            recommended_action=recommended_action,
            response=response,
            knowledge_sources=knowledge_sources,
        )

    def classify_category(
        self,
        ticket: dict,
    ) -> str:
        """Classify a ticket using deterministic keywords."""

        text = (
            f"{ticket.get('subject', '')} "
            f"{ticket.get('description', '')}"
        ).lower()

        categories = {
            "billing": [
                "billing",
                "invoice",
                "payment",
                "subscription",
                "charge",
                "refund",
            ],
            "authentication": [
                "login",
                "password",
                "authentication",
                "sso",
                "access",
                "locked out",
            ],
            "technical": [
                "error",
                "bug",
                "crash",
                "failure",
                "not working",
                "integration",
            ],
            "onboarding": [
                "setup",
                "getting started",
                "onboarding",
                "configure",
            ],
        }

        for category, keywords in categories.items():
            if any(
                keyword in text
                for keyword in keywords
            ):
                return category

        return "general"

    def _classify_sentiment(
        self,
        ticket: dict,
    ) -> str:
        """Estimate ticket sentiment using simple rules."""

        text = (
            f"{ticket.get('subject', '')} "
            f"{ticket.get('description', '')}"
        ).lower()

        negative_words = [
            "angry",
            "frustrated",
            "urgent",
            "critical",
            "failed",
            "failure",
            "cannot",
            "unable",
            "not working",
            "problem",
            "issue",
        ]

        positive_words = [
            "thank",
            "thanks",
            "great",
            "appreciate",
            "happy",
        ]

        negative_count = sum(
            word in text
            for word in negative_words
        )

        positive_count = sum(
            word in text
            for word in positive_words
        )

        if negative_count > positive_count:
            return "negative"

        if positive_count > negative_count:
            return "positive"

        return "neutral"

    def _recommend_action(
        self,
        risk,
        category: str,
    ) -> str:
        """Generate an action recommendation."""

        if risk and risk.is_high_risk:
            return (
                "Escalate to the appropriate support team "
                "immediately because high-risk indicators "
                "were detected."
            )

        actions = {
            "billing": (
                "Review the customer's billing and "
                "subscription information."
            ),
            "authentication": (
                "Review authentication and account-access "
                "configuration."
            ),
            "technical": (
                "Investigate the technical issue using "
                "the relevant troubleshooting guidance."
            ),
            "onboarding": (
                "Provide the customer with the relevant "
                "onboarding and setup guidance."
            ),
            "general": (
                "Review the ticket and provide appropriate "
                "support based on the available context."
            ),
        }

        return actions.get(
            category,
            actions["general"],
        )