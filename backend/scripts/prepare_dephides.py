import csv
import re
import zipfile
from pathlib import Path
from urllib.parse import urlparse

ZIP_PATH = Path("data/external/dephides.zip")
OUTPUT_PATH = Path("data/processed/dephides_small_raw.csv")

FILES = [
    "dephides-main/dataset/small_dataset/train.txt",
    "dephides-main/dataset/small_dataset/val.txt",
    "dephides-main/dataset/small_dataset/test.txt",
]

def extract_url(raw):
    raw = raw.strip()

    # Extract the URL inside the first Markdown link brackets.
    if raw.startswith("["):
        closing = raw.find("](")
        if closing > 1:
            candidate = raw[1:closing].strip()
            if candidate.startswith(("http://", "https://")):
                return candidate

    if raw.startswith(("http://", "https://")):
        return raw

    return None

def main():
    if not ZIP_PATH.exists():
        raise FileNotFoundError(f"Dataset ZIP not found: {ZIP_PATH}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    counts = {"legitimate": 0, "phishing": 0, "skipped": 0}
    seen = set()

    with zipfile.ZipFile(ZIP_PATH) as archive:
        with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as output:
            writer = csv.DictWriter(
                output,
                fieldnames=["url", "label", "source_split"],
            )
            writer.writeheader()

            for filename in FILES:
                split = filename.rsplit("/", 1)[1].replace(".txt", "")

                with archive.open(filename) as file:
                    for raw_line in file:
                        line = raw_line.decode("utf-8", errors="replace").rstrip("\r\n")
                        parts = line.split("\t", 1)

                        if len(parts) != 2:
                            counts["skipped"] += 1
                            continue

                        label_text, raw_url = parts
                        label_text = label_text.strip().lower()

                        if label_text not in ("legitimate", "phishing"):
                            counts["skipped"] += 1
                            continue

                        url = extract_url(raw_url)
                        if not url:
                            counts["skipped"] += 1
                            continue

                        parsed = urlparse(url)
                        if parsed.scheme not in ("http", "https") or not parsed.hostname:
                            counts["skipped"] += 1
                            continue

                        key = (url, label_text)
                        if key in seen:
                            counts["skipped"] += 1
                            continue
                        seen.add(key)

                        writer.writerow({
                            "url": url,
                            "label": 1 if label_text == "phishing" else 0,
                            "source_split": split,
                        })
                        counts[label_text] += 1

    print("Finished preparing DEPHIDES data.")
    print("Output:", OUTPUT_PATH)
    print("Legitimate:", counts["legitimate"])
    print("Phishing:", counts["phishing"])
    print("Skipped rows:", counts["skipped"])
    print("Unique URL-label pairs:", len(seen))

if __name__ == "__main__":
    main()
