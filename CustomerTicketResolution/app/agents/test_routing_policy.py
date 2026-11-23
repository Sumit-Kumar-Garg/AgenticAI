
from app.agents.support_graph import route_after_reasoning


def make_state(
    category="OTHER",
    confidence=0.95,
    requires_human=False,
    priority="LOW",
    warnings=None
):
    return {
        "ticket": {
            "priority": priority
        },
        "analysis": {
            "category": category,
            "confidence": confidence,
            "requires_human": requires_human
        },
        "data_integrity_warnings": warnings or []
    }


def test_low_risk_case():
    state = make_state()
    assert route_after_reasoning(state) == "auto_resolution"


def test_refund_requires_human():
    state = make_state(category="REFUND")
    assert route_after_reasoning(state) == "human_review"


def test_payment_requires_human():
    state = make_state(category="PAYMENT")
    assert route_after_reasoning(state) == "human_review"


def test_cancellation_requires_human():
    state = make_state(category="CANCELLATION")
    assert route_after_reasoning(state) == "human_review"


def test_low_confidence_requires_human():
    state = make_state(confidence=0.65)
    assert route_after_reasoning(state) == "human_review"


def test_high_priority_requires_human():
    state = make_state(priority="HIGH")
    assert route_after_reasoning(state) == "human_review"


def test_data_integrity_warning_requires_human():
    state = make_state(
        warnings=["Customer and booking IDs do not match"]
    )
    assert route_after_reasoning(state) == "human_review"


def test_gemini_escalation_requires_human():
    state = make_state(requires_human=True)
    assert route_after_reasoning(state) == "human_review"


if __name__ == "__main__":
    test_low_risk_case()
    test_refund_requires_human()
    test_payment_requires_human()
    test_cancellation_requires_human()
    test_low_confidence_requires_human()
    test_high_priority_requires_human()
    test_data_integrity_warning_requires_human()
    test_gemini_escalation_requires_human()

    print("All routing policy tests passed!")
