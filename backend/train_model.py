import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# Load dataset
df = pd.read_csv("dataset.csv")

# Features
X = df[
    [
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
]

# Target
y = df["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "phishing_model.pkl")

print("\nModel saved as phishing_model.pkl")