
def calculate_final_risk(
    ml_prediction,
    ml_score,
    threat_intelligence
):
    # Keep the ML score separate from the final risk score.
    ml_score = max(0.0, min(float(ml_score), 100.0))
    score = ml_score

    reputation = threat_intelligence.get(
        "reputation", "Unavailable"
    )
    known_threat = threat_intelligence.get(
        "known_threat", False
    )

    # Known malicious threat intelligence raises the minimum score.
    if known_threat is True or reputation == "Malicious":
        score = max(score, 90.0)

    # A phishing prediction should not be labeled Low risk.
    elif ml_prediction == 1:
        score = max(score, 30.0)

    score = max(0.0, min(score, 100.0))

    if score >= 70:
        final_risk = "High"
    elif score >= 30:
        final_risk = "Medium"
    else:
        final_risk = "Low"

    return {
        "ml_risk_score": round(ml_score, 2),
        "final_risk_score": round(score, 2),
        "final_risk_level": final_risk,
        "risk_adjusted": score > ml_score
    }
