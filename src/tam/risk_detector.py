from dataclasses import dataclass


@dataclass
class RiskAssessment:
    """Represents the risk assessment for a support ticket."""

    is_high_risk: bool
    risk_level: str
    risk_reasons: list[str]


class RiskDetector:
    """Detect support-ticket risk using deterministic rules."""

    HIGH_RISK_KEYWORDS = {
        "security",
        "breach",
        "hacked",
        "fraud",
        "unauthorized",
        "data leak",
        "data loss",
        "outage",
        "production down",
        "system down",
        "cannot access",
        "locked out",
        "urgent",
        "critical",
    }

    def assess(self, ticket: dict) -> RiskAssessment:
        """Assess risk based on ticket content."""

        if not ticket:
            return RiskAssessment(
                is_high_risk=False,
                risk_level="unknown",
                risk_reasons=[],
            )

        subject = str(ticket.get("subject", ""))
        description = str(ticket.get("description", ""))

        text = f"{subject} {description}".lower()

        reasons = []

        for keyword in self.HIGH_RISK_KEYWORDS:
            if keyword in text:
                reasons.append(
                    f"High-risk keyword detected: '{keyword}'"
                )

        if reasons:
            return RiskAssessment(
                is_high_risk=True,
                risk_level="high",
                risk_reasons=reasons,
            )

        return RiskAssessment(
            is_high_risk=False,
            risk_level="low",
            risk_reasons=[],
        )