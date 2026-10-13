
"use client";

import { useState } from "react";

export default function Home() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showFullExplanation, setShowFullExplanation] = useState(false);

  async function analyzeURL() {
    if (!url.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
      }

      setResult(await response.json());
    } catch {
      setResult({
        error:
          "Could not connect to the API. Check that FastAPI is running and CORS is configured.",
      });
    } finally {
      setLoading(false);
    }
  }

  const finalLevel = result?.final_risk?.final_risk_level ?? result?.risk_level;
  const finalScore =
    result?.final_risk?.final_risk_score ?? result?.risk_score;

  const levelColor =
    finalLevel === "High"
      ? "#fb7185"
      : finalLevel === "Medium"
      ? "#fbbf24"
      : "#4ce0b3";

  return (
    <main className="cyber-shell">
      <nav className="cyber-nav">
        <div className="cyber-brand">
          <div className="cyber-logo">⌘</div>
          <div>
            <div>CyberGuard AI</div>
            <div className="cyber-muted">THREAT INTELLIGENCE PLATFORM</div>
          </div>
        </div>

        <div className="cyber-status">
          <span className="cyber-dot" />
          Local AI Scanner
        </div>
      </nav>

      <header className="cyber-hero">
        <p className="cyber-eyebrow">AI-powered URL security</p>
        <h1 className="cyber-title">
          Browse smarter.
          <br />
          <span className="cyber-gradient">Stay protected.</span>
        </h1>
        <p className="cyber-subtitle">
          Analyze suspicious links with machine learning, threat intelligence,
          and AI-generated security explanations.
        </p>
      </header>

      <section className="cyber-panel cyber-scanner">
        <p className="cyber-eyebrow">01 / URL SCANNER</p>
        <h2 style={{ marginTop: 10, fontSize: 21 }}>
          Check a website URL
        </h2>
        <p className="cyber-muted">
          Enter a URL to inspect its risk indicators and reputation.
        </p>

        <form
          onSubmit={(event) => {
            event.preventDefault();
            analyzeURL();
          }}
        >
          <label className="cyber-label" htmlFor="url-input">
            Website address
          </label>

          <div className="cyber-input-row">
            <input
              id="url-input"
              className="cyber-input"
              type="url"
              required
              placeholder="https://example.com"
              value={url}
              onChange={(event) => setUrl(event.target.value)}
            />

            <button className="cyber-button" type="submit" disabled={loading}>
              {loading ? "Analyzing..." : "⌕  Analyze URL"}
            </button>
          </div>
        </form>

        <p className="cyber-hint">
          Use URLs you are authorized to test. Do not open suspicious links to
          check them.
        </p>
      </section>

      {result?.error && (
        <div className="cyber-error">{result.error}</div>
      )}

      {result && !result.error && (
        <>
          <div className="cyber-results">
            <section className="cyber-result-card">
              <p className="cyber-eyebrow">02 / FINAL ASSESSMENT</p>
              <h2 style={{ marginTop: 12 }}>Risk overview</h2>
              <p className="cyber-muted">Final risk level</p>

              <div className="cyber-metric" style={{ color: levelColor }}>
                {finalLevel ?? "Unavailable"}
              </div>

              <p className="cyber-muted">
                Risk score: {finalScore ?? "Unavailable"}
                {finalScore !== undefined && finalScore !== null ? "%" : ""}
              </p>

              <div style={{
                height: 6,
                borderRadius: 8,
                background: "#263449",
                overflow: "hidden",
                marginTop: 18
              }}>
                <div style={{
                  height: "100%",
                  width: `${Math.max(0, Math.min(100, Number(finalScore) || 0))}%`,
                  background: levelColor,
                  borderRadius: 8
                }} />
              </div>

              <p className="cyber-muted" style={{ marginTop: 18 }}>
                ML prediction: <strong>{result.prediction}</strong>
              </p>


              <p className="cyber-muted" style={{ marginTop: 12 }}>
                ML risk score: <strong>{result.risk_score ?? "Unavailable"}%</strong>
              </p>

              <p className="cyber-muted" style={{ marginTop: 8 }}>
                Risk adjusted:{" "}
                <strong>
                  {result.final_risk?.risk_adjusted === true
                    ? "Yes — Risk Engine adjusted the score"
                    : result.final_risk?.risk_adjusted === false
                      ? "No — ML score was unchanged"
                      : "Unavailable"}
                </strong>
              </p>



            </section>

            <section className="cyber-result-card">
              <p className="cyber-eyebrow">03 / THREAT INTELLIGENCE</p>
              <h2 style={{ marginTop: 12 }}>URL reputation</h2>

              <p className="cyber-muted">Domain</p>
              <p>{result.threat_intelligence?.domain ?? "Unavailable"}</p>

              <p className="cyber-muted">Reputation</p>
              <p>
                {result.threat_intelligence?.reputation ?? "Unavailable"}
              </p>

              <p className="cyber-muted">Source</p>
              <p>{result.threat_intelligence?.source ?? "Unavailable"}</p>
            </section>

            <section className="cyber-result-card">
              <p className="cyber-eyebrow">04 / SECURITY ACTION</p>
              <h3 style={{ marginTop: 12 }}>
                {result.recommendation?.action ?? "Recommended precautions"}
              </h3>
              <p className="cyber-muted">
                {result.recommendation?.message ??
                  "Verify the domain independently before sharing sensitive information."}
              </p>
            </section>

            <section className="cyber-result-card cyber-ai-card">
              <p className="cyber-eyebrow">05 / LOCAL AI ANALYSIS</p>
              <h3 style={{ marginTop: 12 }}>AI explanation</h3>

              <div
                className="cyber-ai-content"
                style={{
                  maxHeight: showFullExplanation ? "none" : 180,
                  overflow: showFullExplanation ? "visible" : "hidden",
                }}
              >
                {result.ai_explanation ?? "No AI explanation returned."}
              </div>

              {String(result.ai_explanation ?? "").length > 240 && (
                <button
                  type="button"
                  className="cyber-expand-button"
                  onClick={() =>
                    setShowFullExplanation((previous) => !previous)
                  }
                >
                  {showFullExplanation ? "Show less ↑" : "Read full analysis ↓"}
                </button>
              )}
            </section>

            <section className="cyber-result-card" style={{ gridColumn: "1 / -1" }}>
              <p className="cyber-eyebrow">06 / FEATURE ANALYSIS</p>
              <h3 style={{ marginTop: 12 }}>Extracted URL features</h3>
              <pre className="cyber-pre">
                {JSON.stringify(result.features ?? {}, null, 2)}
              </pre>
            </section>
          </div>

          <p className="cyber-hint" style={{ marginTop: 20 }}>
            Security note: a threat-intelligence “no match” does not prove a
            URL is safe. ML scores are estimates, not guarantees.
          </p>
        </>
      )}

      <footer className="cyber-footer">
        CYBERGUARD AI · DEFENSIVE URL ANALYSIS
        <br />
        Machine learning · Threat intelligence · Local language model
      </footer>
    </main>
  );
}