import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from analyzer import extract_features

INPUT_PATH = Path("data/processed/dephides_small_raw.csv")
OUTPUT_PATH = Path("data/processed/dephides_features.csv")

FEATURE_NAMES = [
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
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    skipped = 0

    with INPUT_PATH.open("r", newline="", encoding="utf-8") as source, \
         OUTPUT_PATH.open("w", newline="", encoding="utf-8") as destination:

        reader = csv.DictReader(source)
        writer = csv.DictWriter(
            destination,
            fieldnames=["url", *FEATURE_NAMES, "label", "source_split"],
        )
        writer.writeheader()

        for row in reader:
            url = row["url"].strip()

            try:
                features = extract_features(url)
                if not url.startswith(("http://", "https://")):
                    skipped += 1
                    continue

                writer.writerow({
                    "url": url,
                    **features,
                    "label": int(row["label"]),
                    "source_split": row["source_split"],
                })
                total += 1

            except (ValueError, TypeError, KeyError):
                skipped += 1

    print("Feature extraction complete.")
    print("Output:", OUTPUT_PATH)
    print("Processed:", total)
    print("Skipped:", skipped)

if __name__ == "__main__":
    main()
