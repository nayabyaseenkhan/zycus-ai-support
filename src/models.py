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
    "low",
    "normal",
    "high",
]

TicketSentiment = Literal[
    "positive",
    "neutral",
    "negative",
]


class TriageResult(BaseModel):
    """Structured result produced by the support triage system."""

    ticket_id: str
    category: TicketCategory
    priority: TicketPriority
    sentiment: TicketSentiment
    is_high_risk: bool
    risk_level: str
    risk_reasons: list[str] = Field(
        default_factory=list
    )
    recommended_action: str
    response: str
    knowledge_sources: list[str] = Field(
        default_factory=list
    )