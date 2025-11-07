import os
import sys
import boto3
from datetime import datetime, timedelta
from pathlib import Path

# --- AWS S3 Configuration ---
BUCKET_NAME = "duploservices-ct-agskore-901907124952"
s3_client = boto3.client("s3")  # Uses IAM / Instance credentials automatically


def get_default_download_folder():
    """Return user's default Downloads directory."""
    home = Path.home()
    download_dir = home / "Downloads"
    download_dir.mkdir(parents=True, exist_ok=True)
    return str(download_dir)


def find_latest_available_date(bucket, commodity_name, max_days=7):
    """
    Check S3 for available folders up to `max_days` back.
    Returns (date_str, prefix) if found, else (None, None)
    """
    for i in range(max_days):
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime("%d-%m-%Y")
        prefix = f"models/{date_str}/{commodity_name}/"

        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=1)
        if "Contents" in response:
            return date_str, prefix

    return None, None


def download_commodity_from_s3(commodity_name):
    """Download all model files for a given commodity (auto fallback to past days)."""
    date_str, prefix = find_latest_available_date(BUCKET_NAME, commodity_name)

    if not date_str:
        print(f"❌ No models found for '{commodity_name}' in the last 7 days.\n")
        return

    print(f"\n📦 Found latest models for {commodity_name} on {date_str}")
    print(f"📦 Downloading from s3://{BUCKET_NAME}/{prefix}")

    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)

        # ✅ Confirm actual files exist
        if "Contents" not in response or len(response["Contents"]) == 0:
            print(f"⚠️ No downloadable files found for {commodity_name}.\n")
            return

        # Only create local folder once files are confirmed
        local_download_dir = os.path.join(
            get_default_download_folder(), "models", date_str, commodity_name
        )
        os.makedirs(local_download_dir, exist_ok=True)

        print(f"📁 Saving to: {local_download_dir}\n")

        for obj in response["Contents"]:
            s3_key = obj["Key"]
            file_name = os.path.basename(s3_key)
            if not file_name:
                continue

            local_path = os.path.join(local_download_dir, file_name)
            s3_client.download_file(BUCKET_NAME, s3_key, local_path)
            print(f"✅ Downloaded: {file_name}")

        print(f"\n🎯 Completed download for {commodity_name} ({date_str}).\n")

    except Exception as e:
        print(f"❌ Error downloading {commodity_name}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ Please provide one or more commodity names.\nExample:")
        print("   python download_from_s3.py Almonds Cashew Blueberry")
        sys.exit(1)

    commodities = sys.argv[1:]
    print(f"🧺 Downloading models for: {', '.join(commodities)}\n")

    for commodity in commodities:
        download_commodity_from_s3(commodity)
