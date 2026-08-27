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

        subject = str(
            ticket.get("subject", "")
        )

        description = str(
            ticket.get("description", "")
        )

        query = " ".join(
            part
            for part in [subject, description]
            if part
        ).strip()

        knowledge = self.retriever.search(
            query,
            top_k=top_k,
        )

        risk = self.risk_detector.assess(
            ticket
        )

        summary = self.summarizer.summarize_context(
            ticket=ticket,
            account=customer_context["account"],
            account_tickets=customer_context[
                "account_tickets"
            ],
        )

        return {
            "ticket": ticket,
            "account": customer_context["account"],
            "account_tickets": customer_context[
                "account_tickets"
            ],
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

        ticket = context["ticket"]

        user_prompt = build_triage_prompt(
            context
        )

        llm_response = self.llm_client.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        risk = context["risk"]

        category = self.classify_category(
            ticket
        )

        product_area = self.classify_product_area(
            ticket
        )

        sentiment = self._classify_sentiment(
            ticket
        )

        priority = self._determine_priority(
            risk=risk,
            ticket=ticket,
        )

        recommended_team = (
            self._recommend_team(
                category=category,
                product_area=product_area,
                risk=risk,
            )
        )

        recommended_action = (
            self._recommend_action(
                risk=risk,
                category=category,
            )
        )

        knowledge_sources = list(
            dict.fromkeys(
                result["source"]
                for result in context["knowledge"]
                if result.get("source")
            )
        )

        known_issue = bool(
            knowledge_sources
        )

        reasoning = self._build_reasoning(
            category=category,
            product_area=product_area,
            priority=priority,
            sentiment=sentiment,
            risk=risk,
            known_issue=known_issue,
        )

        first_response = (
            self._build_first_response(
                ticket=ticket,
                category=category,
                recommended_team=recommended_team,
                knowledge_sources=knowledge_sources,
            )
        )

        return TriageResult(
            ticket_id=ticket_id,
            product_area=product_area,
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
            reasoning=reasoning,
            known_issue=known_issue,
            knowledge_sources=knowledge_sources,
            recommended_team=recommended_team,
            recommended_action=recommended_action,
            response=llm_response,
            first_response=first_response,
        )

    def classify_category(
        self,
        ticket: dict,
    ) -> str:
        """Classify the ticket issue category."""

        text = self._ticket_text(ticket)

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
                "single sign-on",
                "access",
                "locked out",
            ],
            "technical": [
                "error",
                "bug",
                "crash",
                "failure",
                "failed",
                "not working",
                "integration",
                "performance",
            ],
            "onboarding": [
                "setup",
                "getting started",
                "onboarding",
                "configure",
                "configuration",
            ],
        }

        for category, keywords in categories.items():
            if any(
                keyword in text
                for keyword in keywords
            ):
                return category

        return "general"

    def classify_product_area(
        self,
        ticket: dict,
    ) -> str:
        """Identify the product area from ticket content."""

        text = self._ticket_text(ticket)

        product_keywords = {
            "AnalyticsHub": [
                "analyticshub",
                "analytics hub",
                "analytics",
            ],
            "CloudSync": [
                "cloudsync",
                "cloud sync",
            ],
            "DataBridge Pro": [
                "databridge",
                "data bridge",
            ],
            "SecureVault": [
                "securevault",
                "secure vault",
            ],
            "WorkflowEngine": [
                "workflowengine",
                "workflow engine",
                "workflow",
            ],
        }

        for product, keywords in product_keywords.items():
            if any(
                keyword in text
                for keyword in keywords
            ):
                return product

        return "Platform / General"

    def _determine_priority(
        self,
        risk,
        ticket: dict,
    ) -> str:
        """Determine P1-P4 urgency deterministically."""

        text = self._ticket_text(ticket)

        if risk and risk.is_high_risk:
            return "P1"

        p2_keywords = [
            "urgent",
            "critical",
            "production down",
            "outage",
            "all users",
            "entire team",
            "security",
            "data loss",
        ]

        if any(
            keyword in text
            for keyword in p2_keywords
        ):
            return "P2"

        p3_keywords = [
            "not working",
            "failed",
            "failure",
            "error",
            "cannot",
            "unable",
            "issue",
            "problem",
        ]

        if any(
            keyword in text
            for keyword in p3_keywords
        ):
            return "P3"

        return "P4"

    def _classify_sentiment(
        self,
        ticket: dict,
    ) -> str:
        """Estimate ticket sentiment deterministically."""

        text = self._ticket_text(ticket)

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

    def _recommend_team(
        self,
        category: str,
        product_area: str,
        risk,
    ) -> str:
        """Recommend the responder team."""

        if risk and risk.is_high_risk:
            return "Technical Support - Escalations"

        if category == "billing":
            return "Billing Support"

        if category == "authentication":
            return "Technical Support - Identity & Access"

        if category == "technical":
            return "Technical Support - Engineering"

        if category == "onboarding":
            return "Customer Success / Onboarding"

        if product_area != "Platform / General":
            return "Technical Support - Product Specialists"

        return "Technical Support - General"

    def _recommend_action(
        self,
        risk,
        category: str,
    ) -> str:
        """Generate an action recommendation."""

        if risk and risk.is_high_risk:
            return (
                "Escalate to the appropriate support "
                "team immediately because high-risk "
                "indicators were detected."
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

    def _build_reasoning(
        self,
        category: str,
        product_area: str,
        priority: str,
        sentiment: str,
        risk,
        known_issue: bool,
    ) -> str:
        """Build deterministic triage reasoning."""

        risk_text = (
            "High-risk indicators were detected."
            if risk and risk.is_high_risk
            else "No high-risk indicators were detected."
        )

        knowledge_text = (
            "Relevant knowledge-base documentation "
            "was found."
            if known_issue
            else "No strong knowledge-base match was found."
        )

        return (
            f"The ticket was classified as {category} "
            f"for the {product_area} product area. "
            f"The urgency was assessed as {priority} "
            f"and the sentiment as {sentiment}. "
            f"{risk_text} {knowledge_text}"
        )

    def _build_first_response(
        self,
        ticket: dict,
        category: str,
        recommended_team: str,
        knowledge_sources: list[str],
    ) -> str:
        """Create a deterministic first-response draft."""

        subject = str(
            ticket.get(
                "subject",
                "your support request",
            )
        ).strip()

        if category == "authentication":
            next_step = (
                "We will review the authentication or "
                "SSO configuration and verify the relevant "
                "access settings."
            )
        elif category == "billing":
            next_step = (
                "We will review the billing and "
                "subscription details associated with "
                "your account."
            )
        elif category == "technical":
            next_step = (
                "We will investigate the reported technical "
                "issue and review the relevant troubleshooting "
                "guidance."
            )
        elif category == "onboarding":
            next_step = (
                "We will review the setup or configuration "
                "steps and provide the appropriate guidance."
            )
        else:
            next_step = (
                "We will review the available ticket "
                "information and determine the appropriate "
                "next steps."
            )

        knowledge_text = ""

        if knowledge_sources:
            knowledge_text = (
                " We have also identified relevant internal "
                "support documentation for this issue."
            )

        return (
            f"Hello, thank you for contacting support "
            f"regarding '{subject}'. "
            f"We have received your request and routed it "
            f"to {recommended_team}. "
            f"{next_step}"
            f"{knowledge_text} "
            f"We will follow up with the next steps."
        )

    @staticmethod
    def _ticket_text(
        ticket: dict,
    ) -> str:
        """Return normalized ticket text."""

        return (
            f"{ticket.get('subject', '')} "
            f"{ticket.get('description', '')}"
        ).lower().strip()