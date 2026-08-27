from src.models import TriageResult


def test_triage_result_model():
    print("Testing triage result model...")

    result = TriageResult(
        ticket_id="test-ticket",
        product_area="AnalyticsHub",
        category="technical",
        priority="P2",
        sentiment="negative",
        is_high_risk=True,
        risk_level="high",
        risk_reasons=[
            "Production impact detected."
        ],
        reasoning=(
            "The ticket describes a technical issue "
            "affecting the AnalyticsHub product. "
            "The urgency is P2 because the issue "
            "has significant production impact."
        ),
        known_issue=True,
        knowledge_sources=[
            "troubleshooting/performance-and-integrations.md"
        ],
        recommended_team=(
            "Technical Support - Engineering"
        ),
        recommended_action=(
            "Investigate the technical issue using "
            "the relevant troubleshooting guidance."
        ),
        response=(
            "Mock LLM response for testing."
        ),
        first_response=(
            "Hello, thank you for contacting support. "
            "We have received your request and routed "
            "it to Technical Support - Engineering."
        ),
    )

    assert result.ticket_id == "test-ticket"
    print("✓ Ticket ID validated")

    assert result.product_area == "AnalyticsHub"
    print("✓ Product area validated")

    assert result.category == "technical"
    print("✓ Category validated")

    assert result.priority == "P2"
    print("✓ Priority validated")

    assert result.sentiment == "negative"
    print("✓ Sentiment validated")

    assert result.is_high_risk is True
    print("✓ High-risk flag validated")

    assert result.risk_level == "high"
    print("✓ Risk level validated")

    assert len(result.risk_reasons) > 0
    print("✓ Risk reasons validated")

    assert result.reasoning
    print("✓ Reasoning validated")

    assert result.known_issue is True
    print("✓ Known issue validated")

    assert len(result.knowledge_sources) > 0
    print("✓ Knowledge sources validated")

    assert result.recommended_team
    print("✓ Recommended team validated")

    assert result.recommended_action
    print("✓ Recommended action validated")

    assert result.response
    print("✓ LLM response validated")

    assert result.first_response
    print("✓ First response validated")

    print()
    print("Triage result model test passed successfully!")