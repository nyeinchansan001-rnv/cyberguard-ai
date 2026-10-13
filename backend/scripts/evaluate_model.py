import os
import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_PATH = os.path.join(
    BASE_DIR, "data", "processed",
    "phishing_model_dephides.pkl"
)

TEST_PATH = os.path.join(
    BASE_DIR, "data", "processed",
    "dephides_features_clean.csv"
)

REPORT_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

FEATURES = [
    "url_length",
    "domain_length",
    "has_https",
    "has_ip",
    "has_at_symbol",
    "dot_count",
    "subdomain_count",
    "special_char_count",
    "digit_count",
    "suspicious_keyword_count",
]

print("Loading model and dataset...")

model = joblib.load(MODEL_PATH)
df = pd.read_csv(TEST_PATH)

if "source_split" not in df.columns:
    raise ValueError("Dataset is missing the source_split column.")

test_df = df[
    df["source_split"].astype(str).str.lower() == "test"
].dropna(subset=FEATURES + ["label"]).copy()

if test_df.empty:
    raise ValueError("No test rows found.")

X_test = test_df[FEATURES].astype(int)
y_test = test_df["label"].astype(int)
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

tn, fp, fn, tp = confusion_matrix(
    y_test, y_pred, labels=[0, 1]
).ravel()

metrics = pd.DataFrame([
    {"metric": "Test samples", "value": len(y_test)},
    {"metric": "Accuracy", "value": accuracy},
    {"metric": "Precision", "value": precision},
    {"metric": "Recall", "value": recall},
    {"metric": "F1-score", "value": f1},
    {"metric": "True Negative", "value": int(tn)},
    {"metric": "False Positive", "value": int(fp)},
    {"metric": "False Negative", "value": int(fn)},
    {"metric": "True Positive", "value": int(tp)},
])

metrics_path = os.path.join(
    REPORT_DIR, "evaluation_metrics.csv"
)
metrics.to_csv(metrics_path, index=False)

report = classification_report(
    y_test,
    y_pred,
    labels=[0, 1],
    target_names=["Legitimate", "Phishing"],
    output_dict=True,
    zero_division=0,
)

report_df = pd.DataFrame(report).transpose()
report_path = os.path.join(
    REPORT_DIR, "classification_report.csv"
)
report_df.to_csv(report_path, index=True)

print("\n=== EVALUATION RESULTS ===")
print(f"Test samples: {len(y_test)}")
print(f"Accuracy:     {accuracy:.4f}")
print(f"Precision:    {precision:.4f}")
print(f"Recall:       {recall:.4f}")
print(f"F1-score:     {f1:.4f}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")

print("\nReports saved:")
print(metrics_path)
print(report_path)