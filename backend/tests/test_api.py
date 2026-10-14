
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "url",
    [
        "",
        "example.com",
        "ftp://example.com",
        "https:///path",
        "https://user:pass@example.com",
        "https://example.com:99999",
        "https://example.com/" + "a" * 3000,
    ],
)
def test_invalid_urls_are_rejected(url):
    response = client.post("/analyze", json={"url": url})
    assert response.status_code == 422


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"url": 123},
        {"url": None},
    ],
)
def test_invalid_request_payloads_are_rejected(payload):
    response = client.post("/analyze", json=payload)
    assert response.status_code == 422

