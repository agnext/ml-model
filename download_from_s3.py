import os
import sys
import json
import boto3
from pathlib import Path

BUCKET_NAME = "duploservices-ct-agskore-901907124952"
s3 = boto3.client("s3")

CONFIG_FILE = "models.json"

# --- ROOT BASE PATH (generic for all OS) ---
ROOT_FOLDER = Path.home() / "ml-models"      # example: C:\Users\User\.ml-models
ROOT_FOLDER.mkdir(exist_ok=True)


def load_config():
    """Load model configuration from models.json"""
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Config file not found: {CONFIG_FILE}")
        sys.exit(1)

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)["model_config_list"]


def sanitize_base_path(raw_path):
    """
    Ensure base_path NEVER duplicates ml-models folder.
    """
    clean = raw_path.lstrip("/")

    # Remove leading ml-models/
    if clean.startswith("ml-models/"):
        clean = clean.replace("ml-models/", "", 1)

    return clean


def download_s3_folder(bucket, prefix, local_dir):
    """Download S3 folder recursively."""
    paginator = s3.get_paginator("list_objects_v2")

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]

            if key.endswith("/"):
                continue

            rel_path = key[len(prefix):]
            local_path = os.path.join(local_dir, rel_path)

            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            if os.path.exists(local_path):
                print(f"⏩ Skipping (exists): {rel_path}")
                continue

            s3.download_file(bucket, key, local_path)
            print(f"✔ Downloaded: {rel_path}")


def download_for_commodity(commodity, config):
    """Download all model folders for a given commodity."""
    models = [m for m in config if m["commodity"].lower() == commodity.lower()]

    if not models:
        print(f"❌ No models found for commodity: {commodity}")
        return

    print(f"\n📦 Found {len(models)} model(s) for: {commodity}")

    for model in models:
        model_name = model["name"]
        base_path = sanitize_base_path(model["base_path"])

        # S3 path
        s3_prefix = f"model_store/{commodity.lower()}/{model_name}/"

        # Local path → ~/.ml-models/<base_path>/<model_name>
        local_path = ROOT_FOLDER / base_path / model_name
        os.makedirs(local_path, exist_ok=True)

        print(f"\n📥 Downloading model: {model_name}")
        print(f"🔹 S3 : s3://{BUCKET_NAME}/{s3_prefix}")
        print(f"🔹 Local: {local_path}")

        download_s3_folder(BUCKET_NAME, s3_prefix, local_path)

    print(f"\n🎉 Completed: {commodity}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:\n  python download_models.py Almonds\n")
        sys.exit(1)

    commodities = sys.argv[1:]
    config = load_config()

    for commodity in commodities:
        download_for_commodity(commodity, config)
