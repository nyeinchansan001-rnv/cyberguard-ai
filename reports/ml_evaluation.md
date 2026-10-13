# CyberGuard AI — ML Model Evaluation

## Evaluation Dataset
- Dataset: dephides_features_clean.csv
- Split: test
- Test samples: 51,428
- Legitimate samples: 28,532
- Phishing samples: 22,896
- Metrics: Accuracy, Precision, Recall, F1-score, Confusion Matrix

## Model A: phishing_model_dephides.pkl

| Metric | Result |
|---|---:|
| Accuracy | 90.56% |
| Phishing Precision | 87.88% |
| Phishing Recall | 91.39% |
| Phishing F1-score | 89.60% |

Confusion Matrix (actual rows, predicted columns):

| Actual | Predicted Legitimate | Predicted Phishing |
|---|---:|---:|
| Legitimate | 25,647 | 2,885 |
| Phishing | 1,971 | 20,925 |

## Model B: phishing_model_v2.pkl

| Metric | Result |
|---|---:|
| Accuracy | 44.72% |
| Phishing Precision | 44.61% |
| Phishing Recall | 99.97% |
| Phishing F1-score | 61.69% |

Confusion Matrix (actual rows, predicted columns):

| Actual | Predicted Legitimate | Predicted Phishing |
|---|---:|---:|
| Legitimate | 109 | 28,423 |
| Phishing | 7 | 22,889 |

## Interpretation
- On this test split, the Dephides model has a more balanced result.
- The V2 model labels nearly all URLs as phishing on this dataset, producing many false positives.
- Do not select a model using phishing recall alone; consider precision, false positives, and the intended operational use.

## Limitations
- These results describe performance on this dataset only.
- The V2 training history and dataset provenance have not been verified.
- Dataset leakage and duplicate records across training and evaluation data have not been fully ruled out.
- The Dephides model's saved artifact has not yet been confirmed to match the recorded training script and dataset version.
- Further validation on a separate, representative dataset is needed before making real-world performance claims.
- ML predictions and risk scores are estimates, not guarantees of website safety.
