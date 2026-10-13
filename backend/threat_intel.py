import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

URLHAUS_AUTH_KEY = os.getenv("URLHAUS_AUTH_KEY")


def check_threat_intelligence(url: str):

    parsed = urlparse(url)
    domain = parsed.hostname or ""

    if not URLHAUS_AUTH_KEY:
        return {
            "domain": domain,
            "known_threat": False,
            "reputation": "Unavailable",
            "source": "URLhaus",
            "message": "URLhaus API key is not configured."
        }

    try:
        response = requests.post(
            "https://urlhaus-api.abuse.ch/v1/url/",
            headers={
                "Auth-Key": URLHAUS_AUTH_KEY
            },
            data={
                "url": url
            },
            timeout=10
        )

        if response.status_code != 200:
            return {
                "domain": domain,
                "known_threat": False,
                "reputation": "Unavailable",
                "source": "URLhaus",
                "message": f"API request failed with status {response.status_code}"
            }

        data = response.json()

        if data.get("query_status") == "ok":
            return {
                "domain": domain,
                "known_threat": True,
                "reputation": "Malicious",
                "source": "URLhaus",
                "url_status": data.get("url_status"),
                "threat": data.get("threat")
            }

        return {
            "domain": domain,
            "known_threat": False,
            "reputation": "No match",
            "source": "URLhaus",
            "query_status": data.get("query_status")
        }

    except requests.RequestException as e:
        return {
            "domain": domain,
            "known_threat": False,
            "reputation": "Unavailable",
            "source": "URLhaus",
            "message": str(e)
        }