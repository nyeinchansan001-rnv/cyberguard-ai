# CyberGuard AI — Phishing URL Risk Analyzer

CyberGuard AI is a defensive security project that analyzes URLs using machine learning, threat intelligence, and a locally hosted language model to provide risk assessments and security recommendations.

## Features

- **Machine Learning:** Predicts whether a URL is likely legitimate or phishing.
- **Risk Assessment:** Combines the model's score with threat intelligence to determine a final risk level.
- **Threat Intelligence:** Queries URLhaus for known malicious URL information.
- **AI Explanation:** Uses a local Ollama language model to explain the analysis.
- **Security Recommendations:** Provides precautionary actions based on the final assessment.
- **Web Dashboard:** Displays risk scores, URL features, threat intelligence, and recommendations.

## Technology Stack

- Python
- FastAPI
- scikit-learn / joblib
- URLhaus
- Ollama (`llama3.2:3b`)
- Next.js
- JavaScript and CSS

## Project Structure

```text
cyberguard-ai/
├── backend/
│   ├── main.py
│   ├── threat_intel.py
│   ├── risk_engine.py
│   ├── recommendations.py
│   ├── data/
│   └── scripts/
├── frontend/
│   └── app/
│       ├── page.js
│       ├── globals.css
│       └── layout.tsx
└── README.md
```

## Running Locally

### 1. Start the Backend

Open a terminal and navigate to the backend directory:

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

The API should be available at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 2. Start Ollama

Ensure Ollama is installed and running, and that the configured model is available:

```bash
ollama list
```

If `llama3.2:3b` is not installed, download it with:

```bash
ollama pull llama3.2:3b
```

### 3. Start the Frontend

Open another terminal from the project root:

```bash
cd frontend
npm install
npm run dev
```

Open the local dashboard at:

```text
http://localhost:3000
```

## API Example

**Endpoint:** `POST /analyze`

Request body:

```json
{
  "url": "https://example.com"
}
```

The response includes the model prediction, risk score, extracted URL features, threat intelligence result, final risk assessment, recommendation, and AI-generated explanation.

## Risk Interpretation

The application reports Low, Medium, or High risk based on its configured risk engine.

- **Low:** No significant risk indicators were detected by the current checks.
- **Medium:** Additional verification is recommended.
- **High:** Avoid the URL and do not submit sensitive information.

These levels are estimates from the configured checks, not guarantees of website safety.

## Security Considerations and Limitations

- A URLhaus "No match" result does not prove that a URL is safe.
- HTTPS encrypts a connection but does not guarantee that a website is trustworthy.
- Machine-learning predictions can produce false positives and false negatives.
- AI-generated explanations may contain errors and should be checked against the structured analysis results.
- Model performance must be evaluated on representative, independent datasets before real-world effectiveness is claimed.
- This project is intended for defensive analysis and educational demonstration, not as a replacement for a complete security solution.

## Testing and Evaluation

The project includes controlled risk-logic tests and documented machine-learning evaluation results. See the `reports/` directory if the reports are present in your local project.

Reported evaluation results apply only to the evaluated dataset and should not be interpreted as guaranteed real-world detection performance.

## Future Improvements

- Expand automated API and frontend tests.
- Improve AI explanation formatting and consistency.
- Add more robust URL validation and error handling.
- Evaluate the model against additional independent datasets.
- Improve dashboard accessibility and responsive behavior.

## Author

Security-focused portfolio project for demonstrating URL analysis, threat intelligence integration, risk assessment, and AI-assisted security explanations.
