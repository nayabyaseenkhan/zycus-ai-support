from pydantic import ValidationError

from src.models import TriageResult


def main():
    print("Testing triage result model...\n")

    result = TriageResult(
        ticket_id="test-ticket",
        category="billing",
        priority="high",
        sentiment="negative",
        is_high_risk=True,
        risk_level="high",
        risk_reasons=[
        "High-risk keyword detected: 'security'"
        ],
        recommended_action="Investigate the billing issue.",
        response="The customer's billing issue requires investigation.",
        knowledge_sources=[
            "billing/billing-and-plans.md"
        ],
    )

    assert result.ticket_id == "test-ticket"
    assert result.category == "billing"
    assert result.priority == "high"
    assert result.sentiment == "negative"
    assert result.recommended_action
    assert result.response
    assert result.knowledge_sources

    print("✓ Valid triage result accepted")

    try:
        TriageResult(
            ticket_id="test-ticket",
            category="invalid-category",
            priority="high",
            sentiment="negative",
            recommended_action="Test action",
            response="Test response",
        )

        assert False, "Invalid category was accepted."

    except ValidationError:
        print("✓ Invalid category rejected")

    try:
        TriageResult(
            ticket_id="test-ticket",
            category="billing",
            priority="invalid-priority",
            sentiment="negative",
            recommended_action="Test action",
            response="Test response",
        )

        assert False, "Invalid priority was accepted."

    except ValidationError:
        print("✓ Invalid priority rejected")

    try:
        TriageResult(
            ticket_id="test-ticket",
            category="billing",
            priority="high",
            sentiment="invalid-sentiment",
            recommended_action="Test action",
            response="Test response",
        )

        assert False, "Invalid sentiment was accepted."

    except ValidationError:
        print("✓ Invalid sentiment rejected")

    print("\nTriage result model test passed successfully!")


if __name__ == "__main__":
    main()