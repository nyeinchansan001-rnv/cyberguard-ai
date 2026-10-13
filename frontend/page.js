
"use client";

import { useState } from "react";

export default function Home() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);

  async function analyzeURL() {
    if (!url.trim()) {
      alert("Please enter a URL.");
      return;
    }

    setResult({ loading: true });

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch {
      setResult({
        error: "Could not connect to CyberGuard AI backend. Make sure FastAPI is running.",
      });
    }
  }

  return (
    <main style={{
      minHeight: "100vh",
      background: "#080d18",
      color: "#e5edf8",
      padding: "48px 20px",
      fontFamily: "Arial, sans-serif"
    }}>
      <div style={{ maxWidth: "850px", margin: "0 auto" }}>
        <p style={{ color: "#38bdf8", letterSpacing: "3px" }}>
          CYBERSECURITY • AI
        </p>

        <h1 style={{ fontSize: "42px", marginBottom: "8px" }}>
          CyberGuard AI
        </h1>

        <p style={{ color: "#94a3b8", marginBottom: "32px" }}>
          AI-powered phishing URL analysis and threat intelligence.
        </p>

        <section style={{
          background: "#111827",
          border: "1px solid #263449",
          borderRadius: "16px",
          padding: "24px"
        }}>
          <label htmlFor="url" style={{ display: "block", marginBottom: "12px" }}>
            Enter URL to analyze
          </label>

          <input
            id="url"
            type="url"
            placeholder="https://example.com"
            value={url}
            onChange={(event) => setUrl(event.target.value)}
            style={{
              boxSizing: "border-box",
              width: "100%",
              padding: "14px",
              borderRadius: "8px",
              border: "1px solid #334155",
              background: "#080d18",
              color: "white",
              marginBottom: "16px"
            }}
          />

          <button
            onClick={analyzeURL}
            disabled={result?.loading}
            style={{
              padding: "13px 22px",
              borderRadius: "8px",
              border: "none",
              background: "#0284c7",
              color: "white",
              fontWeight: "bold",
              cursor: "pointer"
            }}
          >
            {result?.loading ? "Analyzing..." : "Analyze URL"}
          </button>
        </section>

        {result?.error && (
          <p style={{ color: "#f87171", marginTop: "24px" }}>
            {result.error}
          </p>
        )}

        {result && !result.loading && !result.error && (
          <section style={{
            marginTop: "24px",
            padding: "24px",
            borderRadius: "16px",
            background: "#111827",
            border: "1px solid #263449",
            overflowWrap: "anywhere"
          }}>
            <h2>Analysis Results</h2>

            <p><strong>URL:</strong> {result.url}</p>
            <p><strong>ML Prediction:</strong> {result.prediction}</p>
            <p><strong>ML Risk Score:</strong> {result.risk_score}%</p>
            <p><strong>ML Risk Level:</strong> {result.risk_level}</p>

           
          <h3>Final Risk</h3>
          <p>
            <strong>Final Risk Score:</strong>{" "}
            {result.final_risk?.final_risk_score != null
              ? `${result.final_risk.final_risk_score}%`
              : "Unavailable"}
          </p>
          <p>
            <strong>Final Risk Level:</strong>{" "}
            {result.final_risk?.final_risk_level ?? "Unavailable"}
          </p>
          <p>
            <strong>Risk Adjusted:</strong>{" "}
            {result.final_risk?.risk_adjusted === true
              ? "Yes — Risk Engine adjusted the score"
              : result.final_risk?.risk_adjusted === false
                ? "No — ML score was unchanged"
                : "Unavailable"}
          </p>


            <h3>Threat Intelligence</h3>
            <pre style={{ whiteSpace: "pre-wrap", color: "#93c5fd" }}>
              {JSON.stringify(result.threat_intelligence ?? {}, null, 2)}
            </pre>

            <h3>Security Recommendation</h3>
            <p>
              {result.recommendation?.message ?? "No recommendation returned."}
            </p>

            <h3>AI Explanation</h3>
            <p style={{ lineHeight: 1.7 }}>
              {result.ai_explanation ?? "No AI explanation returned."}
            </p>

            <p style={{ color: "#94a3b8", fontSize: "13px", marginTop: "24px" }}>
              Results are indicators, not proof of safety or malicious activity.
              Avoid opening suspicious URLs just to test them.
            </p>
          </section>
        )}
      </div>
    </main>
  );
}