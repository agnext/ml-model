import os
import sys
import json
import boto3
from pathlib import Path

BUCKET_NAME = "duploservices-ct-agskore-901907124952"
s3 = boto3.client("s3")

CONFIG_FILE = "models.json"


# ================= ROOT FOLDER RESOLUTION =================

def find_ml_models_root():
   

    # 1️⃣ ENV override (recommended for prod)
    env_root = os.environ.get("ML_MODELS_ROOT")
    if env_root:
        path = Path(env_root).expanduser().resolve()
        path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Using ML_MODELS_ROOT from env: {path}")
        return path

    candidates = []

    if os.name == "nt":  # Windows
        drives = [
            f"{chr(d)}:\\" for d in range(67, 91)
            if os.path.exists(f"{chr(d)}:\\")
        ]
        for drive in drives:
            candidates.append(Path(drive) / "ml-models")
    else:  # Linux / macOS
        candidates.extend([
            Path("/data/ml-models"),
            Path("/opt/ml-models"),
            Path("/mnt/ml-models"),
            Path("/srv/ml-models"),
            Path.home() / "ml-models"
        ])

    for path in candidates:
        if path.exists() and path.is_dir():
            print(f"📁 Found existing ml-models directory: {path}")
            return path.resolve()

    # 3️⃣ Fallback
    fallback = Path.home() / "ml-models"
    fallback.mkdir(parents=True, exist_ok=True)
    print(f"📁 Created fallback ml-models directory: {fallback}")
    return fallback.resolve()


# ✅ ROOT BASE PATH (NOW SAFE)
ROOT_FOLDER = find_ml_models_root()


# ================= CONFIG =================

def load_config():
    """Load model configuration from models.json"""
    if not Path(CONFIG_FILE).exists():
        print(f"❌ Config file not found: {CONFIG_FILE}")
        sys.exit(1)

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)["model_config_list"]


def sanitize_base_path(raw_path: str) -> str:
    """Ensure base_path NEVER duplicates ml-models folder."""
    clean = raw_path.lstrip("/")

    if clean.startswith("ml-models/"):
        clean = clean.replace("ml-models/", "", 1)

    return clean


# ================= S3 DOWNLOAD =================

def download_s3_folder(bucket, prefix, local_dir: Path):
    """Download S3 folder recursively."""
    paginator = s3.get_paginator("list_objects_v2")

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]

            if key.endswith("/"):
                continue

            rel_path = key[len(prefix):]
            local_path = local_dir / rel_path
            local_path.parent.mkdir(parents=True, exist_ok=True)

            if local_path.exists():
                print(f"⏩ Skipping (exists): {rel_path}")
                continue

            s3.download_file(bucket, key, str(local_path))
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

        s3_prefix = f"model_store/{commodity.lower()}/{model_name}/"
        local_path = ROOT_FOLDER / base_path / model_name
        local_path.mkdir(parents=True, exist_ok=True)

        print(f"\n📥 Downloading model: {model_name}")
        print(f"🔹 S3    : s3://{BUCKET_NAME}/{s3_prefix}")
        print(f"🔹 Local : {local_path}")

        download_s3_folder(BUCKET_NAME, s3_prefix, local_path)

    print(f"\n🎉 Completed: {commodity}\n")


# ================= MAIN =================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:\n  python download_models.py Almonds\n")
        sys.exit(1)

    commodities = sys.argv[1:]
    config = load_config()

    for commodity in commodities:
        download_for_commodity(commodity, config)
