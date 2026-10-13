# CyberGuard AI — Security Logic Test Summary

## Scope
Tested the risk calculation and recommendation logic using
controlled inputs.

## Results

| Test case | Expected result | Status |
|---|---|---|
| Low risk, no known threat | Low risk / Low risk action | PASS |
| Medium risk, no known threat | Medium risk / Proceed with caution | PASS |
| High risk, no known threat | High risk / Avoid this URL | PASS |
| Known malicious threat with low ML score | High risk / Avoid this URL | PASS |

## Important limitations
- These are controlled logic tests, not a measurement of ML accuracy.
- A URLhaus "No match" result does not prove a URL is safe.
- ML predictions and risk scores are estimates, not guarantees.
- Further testing with a labeled dataset and documented metrics
  is required to evaluate phishing detection performance.
