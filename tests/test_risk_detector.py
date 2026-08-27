from src.tam.risk_detector import RiskDetector


def main():
    print("Testing risk detector...\n")

    detector = RiskDetector()

    # High-risk ticket
    high_risk_ticket = {
        "subject": "Security breach detected",
        "description": "Unauthorized access was detected in our account.",
    }

    result = detector.assess(high_risk_ticket)

    assert result.is_high_risk is True
    assert result.risk_level == "high"
    assert result.risk_reasons

    print("✓ High-risk ticket detected")
    print(f"  Reasons: {result.risk_reasons}")

    # Low-risk ticket
    low_risk_ticket = {
        "subject": "How can I update my profile?",
        "description": "I would like to change my profile information.",
    }

    result = detector.assess(low_risk_ticket)

    assert result.is_high_risk is False
    assert result.risk_level == "low"
    assert not result.risk_reasons

    print("✓ Low-risk ticket detected")

    # Empty ticket
    result = detector.assess({})

    assert result.risk_level == "unknown"

    print("✓ Empty ticket handled correctly")

    print("\nRisk detector test passed successfully!")


if __name__ == "__main__":
    main()