
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import re
import joblib
import requests
import pandas as pd

from analyzer import extract_features
from threat_intel import check_threat_intelligence
from risk_engine import calculate_final_risk
from recommendations import get_recommendation

app = FastAPI(title="CyberGuard AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained ML model
model = joblib.load("data/processed/phishing_model_dephides.pkl")


class URLRequest(BaseModel):
    url: str


def get_ai_explanation(
    url,
    prediction,
    risk_score,
    risk_level,
    features,
    threat_intelligence
):
    reputation = threat_intelligence.get(
        "reputation", "Unavailable"
    )

    known_threat = threat_intelligence.get(
        "known_threat", False
    )

    prompt = f"""
You are a careful cybersecurity assistant for CyberGuard AI.

Analyze the following URL analysis results using only the
evidence provided. Do not claim that you visited the URL.

URL: {url}

Machine Learning Prediction: {prediction}
ML Risk Score: {risk_score}%
ML Risk Level: {risk_level}

Extracted URL Features:
{features}

Threat Intelligence Result:
{threat_intelligence}

URLhaus Reputation: {reputation}
Known Threat: {known_threat}

Instructions:
1. Explain the ML prediction as an estimate, not a certainty.
2. Explain which supplied URL features may be suspicious.
3. Do not invent facts about the website or its behavior.
4. HTTPS encrypts a connection but does not guarantee that a
   website is safe.
5. Digits, dots, special characters, and long URLs alone do not
   prove that a URL is malicious.
6. If URLhaus reports "Malicious", explain that a known threat
   was found by the threat intelligence check.
7. If URLhaus reports "No match", explain that no matching
   threat was found in this query. This does not guarantee safety.
8. If URLhaus reports "Unavailable", explain that threat
   intelligence could not provide a result.
9. If the ML prediction and threat intelligence disagree,
   clearly explain the disagreement.
10. Give practical safety advice. Tell users not to enter
    passwords or payment details on suspicious websites.
11. Keep the response concise and easy to understand.
12. Use these headings:
    Assessment
    Evidence
    Threat Intelligence
    Recommendation
13. Feature interpretation rules:

* has_https = 1 means HTTPS is present.
* has_https = 0 means HTTPS is not present.
* has_ip = 1 means the URL uses an IP address as its host.
* has_at_symbol = 1 means the URL contains an @ symbol.
* subdomain_count = 0 means no subdomains were detected.
* A low or high feature count alone does not prove phishing.
* Do not describe a URL as long without a justified comparison.
* Explain only the features that are relevant to this URL.

14. Do not conclude that a URL is legitimate solely because it has a low ML risk score or no URLhaus match.
15. Avoid recommending extra caution solely because a URL is long or contains special characters; explain the actual evidence instead.
16. End with a balanced conclusion that clearly states the limitations of the ML model and threat intelligence.

17. Do not call a URL relatively long based only on its
    character count. Avoid unsupported comparisons.

18. If the URL uses an IP address, explain that this can
    deserve attention but does not prove malicious activity.

19. Keep the conclusion consistent with the actual ML risk
    score and risk level. Never call a medium or high score low.

20. Do not assume that a URLhaus "No match" result confirms
    that a domain or IP address is safe.

21. If the URL uses the documentation IP range 192.0.2.0/24,
    recognize that it is reserved for documentation and testing,
    not a normal public destination.

22. Avoid repeating the same safety warning in multiple sections.

23. Never tell users that they can safely enter passwords, payment details, or other sensitive information based only on a Low risk score or a URLhaus "No match" result.

24. Never claim that a website is safe or trustworthy unless the supplied evidence supports that claim.

25. For Low risk URLs, say that no significant risk indicators were detected by the current checks, but the result does not guarantee safety.

26. Keep the Recommendation consistent with the separate recommendation object returned by the API. Never contradict its safety advice.
Do not exaggerate the risk or make unsupported claims.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2
                }
            },
            timeout=90
        )

        response.raise_for_status()
        result = response.json()

        
        explanation = result.get(
            "response",
            "AI explanation is unavailable."
        ).strip()

        # Remove Markdown bold markers and escaped asterisks.
        explanation = re.sub(
            r"\\?\*\*(.*?)\\?\*\*",
            r"\1",
            explanation
        )

        # Convert Markdown-style bullet markers into readable bullets.
        explanation = re.sub(
            r"(?m)^\s*\\?\*\s+",
            "• ",
            explanation
        )

        # Remove remaining escaped asterisks.
        explanation = explanation.replace(r"\*", "")

        return explanation


    except requests.RequestException as error:
        print("Ollama API error:", str(error))

        return (
            "AI explanation is temporarily unavailable. "
            "The URL analysis results are still available. "
            "Please check whether Ollama is running."
        )


@app.get("/")
def home():
    return {
        "message": "CyberGuard AI is running!"
    }


@app.post("/analyze")
def analyze_url(request: URLRequest):

    # 1. Extract URL features
    features = extract_features(request.url)

    # 2. Prepare features for the ML model
    feature_values = pd.DataFrame([{
        "url_length": features["url_length"],
        "domain_length": features["domain_length"],
        "has_https": features["has_https"],
        "has_ip": features["has_ip"],
        "has_at_symbol": features["has_at_symbol"],
        "dot_count": features["dot_count"],
        "subdomain_count": features["subdomain_count"],
        "special_char_count": features["special_char_count"],
        "digit_count": features["digit_count"],
        "suspicious_keyword_count": features["suspicious_keyword_count"],
    }])



    # 3. Get ML prediction
    prediction_value = model.predict(feature_values)[0]

    probabilities = model.predict_proba(feature_values)[0]
    print("Model classes:", model.classes_)
    print("Prediction probabilities:", probabilities)
    # Find the probability corresponding to class 1
    classes = list(model.classes_)

    if 1 in classes:
        phishing_probability = float(
            probabilities[classes.index(1)]
        )
    else:
        phishing_probability = 0.0

    if prediction_value == 1:
        prediction = "Phishing"
    else:
        prediction = "Legitimate"

    risk_score = round(
        phishing_probability * 100, 2
    )

    # 4. Determine ML risk level
    if phishing_probability <= 0.30:
        risk_level = "Low"
    elif phishing_probability <= 0.70:
        risk_level = "Medium"
    else:
        risk_level = "High"

    # 5. Check threat intelligence
    threat_intel = check_threat_intelligence(
        request.url
    )

    # 6. Calculate combined risk
    final_risk = calculate_final_risk(
        prediction_value,
        phishing_probability * 100,
        threat_intel
    )

    recommendation = get_recommendation(
        final_risk["final_risk_level"],
        threat_intel
    )

    # 7. Generate AI explanation
    ai_explanation = get_ai_explanation(
        request.url,
        prediction,
        risk_score,
        risk_level,
        features,
        threat_intel
    )

    # 8. Return results
    return {
        "url": request.url,
        "prediction": prediction,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "features": features,
        "ai_explanation": ai_explanation,
        "threat_intelligence": threat_intel,
        "final_risk": final_risk,
        "recommendation": recommendation,
    }
