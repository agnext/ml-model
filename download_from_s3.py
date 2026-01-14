import os
import sys
import json
import boto3
from pathlib import Path
from urllib.parse import urlparse

# ================= S3 CONFIG =================

BUCKET_NAME = "duploservices-ct-agskore-901907124952"
s3 = boto3.client("s3")
CONFIG_FILE = "models.json"


# ================= ROOT PATH RESOLUTION =================

def find_ml_models_root():
    """
    Priority:
    1. ML_MODELS_ROOT env variable
    2. Existing ml-models folder in common locations
    3. Create fallback in user's home directory
    """

    # 1️⃣ ENV override
    env_root = os.environ.get("ML_MODELS_ROOT")
    if env_root:
        path = Path(env_root).expanduser().resolve()
        path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Using ML_MODELS_ROOT: {path}")
        return path

    search_roots = []

    if os.name == "nt":  # Windows
        search_roots.extend([
            Path.home(),
            Path.home() / "Documents",
            Path.home() / "Downloads",
        ])
    else:  # Linux / macOS
        search_roots.extend([
            Path("/data"),
            Path("/mnt"),
            Path("/opt"),
            Path("/srv"),
            Path.home(),
            Path.home() / "Music",
            Path.home() / "Documents",
            Path.home() / "Downloads",
        ])

    for root in search_roots:
        candidate = root / "ml-models"
        if candidate.exists() and candidate.is_dir():
            print(f"📁 Found existing ml-models: {candidate}")
            return candidate.resolve()

    # 3️⃣ Fallback
    fallback = Path.home() / "ml-models"
    fallback.mkdir(parents=True, exist_ok=True)
    print(f"📁 Created fallback ml-models: {fallback}")
    return fallback.resolve()


ROOT_FOLDER = find_ml_models_root()


# ================= CONFIG =================

def load_config():
    if not Path(CONFIG_FILE).exists():
        print(f"❌ Config file not found: {CONFIG_FILE}")
        sys.exit(1)

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)["model_config_list"]


def sanitize_base_path(raw_path: str) -> str:
    """
    Remove duplicate ml-models if present in base_path.
    """
    clean = raw_path.lstrip("/")
    if clean.startswith("ml-models/"):
        clean = clean.replace("ml-models/", "", 1)
    return clean


# ================= S3 PREFIX HANDLING =================

def extract_s3_prefix(model: dict) -> str:
    """
    If version exists → download only that version
    Else → download full model folder
    """
    parsed = urlparse(model["s3_path"].strip())
    parts = parsed.path.lstrip("/").split("/")

    # model_store/<commodity>/<model_name>
    base_prefix = "/".join(parts[:3])

    if "version" in model and model["version"]:
        return f"{base_prefix}/{model['version']}/"

    return f"{base_prefix}/"



# ================= S3 DOWNLOAD =================

def download_s3_folder(bucket: str, prefix: str, local_dir: Path):
    paginator = s3.get_paginator("list_objects_v2")
    downloaded = False

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]

            if key.endswith("/"):
                continue

            downloaded = True
            rel_path = key[len(prefix):]
            local_path = local_dir / rel_path
            local_path.parent.mkdir(parents=True, exist_ok=True)

            if local_path.exists():
                print(f"⏩ Skipped (exists): {rel_path}")
                continue

            s3.download_file(bucket, key, str(local_path))
            print(f"✔ Downloaded: {rel_path}")

    if not downloaded:
        print(f"⚠️ No files found under prefix: {prefix}")


# ================= CORE LOGIC =================

def download_for_commodity(commodity: str, config: list):
    models = [m for m in config if m["commodity"].lower() == commodity.lower()]

    if not models:
        print(f"❌ No models found for commodity: {commodity}")
        return

    print(f"\n📦 Found {len(models)} model(s) for: {commodity}")

    for model in models:
        model_name = model["name"]
        base_path = sanitize_base_path(model["base_path"])
        s3_prefix = extract_s3_prefix(model)

        # ✅ FIX: local path must be computed PER MODEL
        if model.get("version"):
            local_path = ROOT_FOLDER / base_path / model_name / str(model["version"])
        else:
            local_path = ROOT_FOLDER / base_path / model_name

        local_path.mkdir(parents=True, exist_ok=True)

        print("\n📥 Downloading model")
        print(f"🔹 Name   : {model_name}")
        print(f"🔹 S3     : s3://{BUCKET_NAME}/{s3_prefix}")
        print(f"🔹 Local  : {local_path}")

        download_s3_folder(BUCKET_NAME, s3_prefix, local_path)

    print(f"\n🎉 Completed: {commodity}\n")


# ================= MAIN =================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:\n  python download_models.py babycarrot blueberry\n")
        sys.exit(1)

    commodities = sys.argv[1:]
    config = load_config()

    for commodity in commodities:
        download_for_commodity(commodity, config)
