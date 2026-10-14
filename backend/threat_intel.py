import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

URLHAUS_AUTH_KEY = os.getenv("URLHAUS_AUTH_KEY")
URLHAUS_API_URL = "https://urlhaus-api.abuse.ch/v1/url/"


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
            URLHAUS_API_URL,
            headers={"Auth-Key": URLHAUS_AUTH_KEY},
            data={"url": url},
            timeout=10
        )

        if response.status_code != 200:
            return {
                "domain": domain,
                "known_threat": False,
                "reputation": "Unavailable",
                "source": "URLhaus",
                "message": "URLhaus API request failed."
            }

        try:
            data = response.json()
        except ValueError:
            return {
                "domain": domain,
                "known_threat": False,
                "reputation": "Unavailable",
                "source": "URLhaus",
                "message": "URLhaus returned an invalid response."
            }

        query_status = data.get("query_status")

        if query_status == "ok":
            return {
                "domain": domain,
                "known_threat": True,
                "reputation": "Malicious",
                "source": "URLhaus",
                "url_status": data.get("url_status"),
                "threat": data.get("threat")
            }

        if query_status == "no_results":
            return {
                "domain": domain,
                "known_threat": False,
                "reputation": "No match",
                "source": "URLhaus",
                "query_status": query_status,
                "message": (
                    "No matching URL was found in URLhaus. "
                    "This does not mean the URL is safe."
                )
            }

        return {
            "domain": domain,
            "known_threat": False,
            "reputation": "Unavailable",
            "source": "URLhaus",
            "message": "URLhaus returned an unexpected response status."
        }

    except requests.RequestException:
        return {
            "domain": domain,
            "known_threat": False,
            "reputation": "Unavailable",
            "source": "URLhaus",
            "message": "Could not connect to URLhaus."
        }
