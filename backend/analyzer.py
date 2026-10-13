from urllib.parse import urlparse
import re
import ipaddress


def extract_features(url: str):
    parsed = urlparse(url)

    hostname = parsed.hostname or ""
    path = parsed.path or ""

    # 1. URL length
    url_length = len(url)

    # 2. Domain length
    domain_length = len(hostname)

    # 3. HTTPS
    has_https = 1 if parsed.scheme == "https" else 0

    # 4. IP address instead of domain
    try:
        ipaddress.ip_address(hostname)
        has_ip = 1
    except ValueError:
        has_ip = 0

    # 5. @ symbol
    has_at_symbol = 1 if "@" in url else 0

    # 6. Number of dots
    dot_count = url.count(".")

   # 7. Number of subdomains
    try:
        ipaddress.ip_address(hostname)
        subdomain_count = 0
    except ValueError:
        subdomain_count = max(0, len(hostname.split(".")) - 2)
    # 8. Number of special characters
    special_char_count = len(re.findall(r"[^a-zA-Z0-9]", url))

    # 9. Number of digits
    digit_count = len(re.findall(r"\d", url))

    # 10. Suspicious keywords
    suspicious_words = [
        "login",
        "verify",
        "account",
        "update",
        "secure",
        "password",
        "bank",
        "signin"
    ]

    keyword_count = sum(
        1 for word in suspicious_words
        if word in url.lower()
    )

    return {
        "url_length": url_length,
        "domain_length": domain_length,
        "has_https": has_https,
        "has_ip": has_ip,
        "has_at_symbol": has_at_symbol,
        "dot_count": dot_count,
        "subdomain_count": subdomain_count,
        "special_char_count": special_char_count,
        "digit_count": digit_count,
        "suspicious_keyword_count": keyword_count
    }