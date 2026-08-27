from typing import Literal

from pydantic import BaseModel, Field


TicketCategory = Literal[
    "billing",
    "authentication",
    "technical",
    "onboarding",
    "general",
]

TicketPriority = Literal[
    "P1",
    "P2",
    "P3",
    "P4",
]

TicketSentiment = Literal[
    "positive",
    "neutral",
    "negative",
]


class TriageResult(BaseModel):
    """Structured result produced by the support triage system."""

    ticket_id: str

    product_area: str

    category: TicketCategory

    priority: TicketPriority

    sentiment: TicketSentiment

    is_high_risk: bool

    risk_level: str

    risk_reasons: list[str] = Field(
        default_factory=list
    )

    reasoning: str

    known_issue: bool

    knowledge_sources: list[str] = Field(
        default_factory=list
    )

    recommended_team: str

    recommended_action: str

    response: str

    first_response: str