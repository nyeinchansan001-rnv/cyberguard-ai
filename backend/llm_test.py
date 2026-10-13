import requests

url = "http://secure-login-account.com/verify"

prediction = "Phishing"
risk_score = 75
risk_level = "High"

prompt = f"""
You are a cybersecurity assistant for a phishing URL analyzer.

Analyze this result:

URL: {url}
Prediction: {prediction}
Risk Score: {risk_score}%
Risk Level: {risk_level}

Explain in simple language:
1. Why the URL may be suspicious
2. Which security features are concerning
3. What the user should do

Important:
Do not claim that these features alone prove the URL is malicious.
Keep the explanation concise.
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False
    }
)

result = response.json()

print("\n===== CyberGuard AI Explanation =====\n")
print(result["response"])