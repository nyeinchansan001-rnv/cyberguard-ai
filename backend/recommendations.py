def get_recommendation(risk_level, threat_intelligence):
    threat_intelligence = threat_intelligence or {}

    reputation = threat_intelligence.get("reputation", "")
    known_threat = threat_intelligence.get("known_threat", False)

    # A confirmed threat must override a low ML risk level.
    if known_threat is True or reputation == "Malicious":
        return {
            "action": "Avoid this URL",
            "message": (
                "Threat intelligence identified this URL as malicious. "
                "Do not visit it or enter passwords, financial information, "
                "or other sensitive data."
            ),
        }

    if risk_level == "High":
        return {
            "action": "Avoid this URL",
            "message": (
                "The analysis indicates high risk. Avoid this URL and "
                "do not enter passwords or financial information."
            ),
        }

    if risk_level == "Medium":
        return {
            "action": "Proceed with caution",
            "message": (
                "The analysis indicates medium risk. Verify the domain "
                "independently before interacting with the website."
            ),
        }

    return {
        "action": "Low risk",
        "message": (
            "No significant risk indicators were detected by the current "
            "checks. This does not guarantee safety; verify the website "
            "before sharing sensitive information."
        ),
    }
