
import pandas as pd
import joblib

from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

DATA_PATH = Path("data/processed/dephides_features_clean.csv")
MODEL_PATH = Path("data/processed/phishing_model_dephides.pkl")

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


def main():
    df = pd.read_csv(DATA_PATH)

    train = df[df["source_split"] == "train"]
    val = df[df["source_split"] == "val"]
    test = df[df["source_split"] == "test"]

    X_train = train[FEATURES]
    y_train = train["label"]

    X_val = val[FEATURES]
    y_val = val["label"]

    X_test = test[FEATURES]
    y_test = test["label"]

    print("Training rows:", len(train))
    print("Validation rows:", len(val))
    print("Test rows:", len(test))
    print("\nTraining model...")

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=2,
    )

    model.fit(X_train, y_train)

    print("\n--- Validation results ---")
    val_pred = model.predict(X_val)
    print("Accuracy:", round(accuracy_score(y_val, val_pred), 4))
    print("Precision:", round(precision_score(y_val, val_pred), 4))
    print("Recall:", round(recall_score(y_val, val_pred), 4))
    print("F1:", round(f1_score(y_val, val_pred), 4))

    print("\n--- Final test results ---")
    test_pred = model.predict(X_test)
    print("Accuracy:", round(accuracy_score(y_test, test_pred), 4))
    print("Precision:", round(precision_score(y_test, test_pred), 4))
    print("Recall:", round(recall_score(y_test, test_pred), 4))
    print("F1:", round(f1_score(y_test, test_pred), 4))
    print("\nConfusion matrix:")
    print(confusion_matrix(y_test, test_pred))
    print("\nClassification report:")
    print(classification_report(y_test, test_pred, target_names=[
        "Legitimate", "Phishing"
    ]))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print("\nNew model saved to:", MODEL_PATH)


if __name__ == "__main__":
    main()

