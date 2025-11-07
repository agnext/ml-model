import boto3, os
from datetime import datetime
from pathlib import Path

s3_client = boto3.client("s3")  # Automatically pulls credentials via instance metadata

FILE_PATH = r"D:\s3Models"
BUCKET_NAME = "duploservices-ct-agskore-901907124952"

def upload_folder(local_folder_path, bucket_name):
    base_path = Path(local_folder_path)
    for root, _, files in os.walk(local_folder_path):
        for filename in files:
            local_path = Path(root) / filename
            date_folder = datetime.now().strftime("%d-%m-%Y")
            relative_path = local_path.relative_to(base_path)
            s3_key = f"models/{date_folder}/{relative_path.as_posix()}"
            s3_client.upload_file(str(local_path), bucket_name, s3_key)
            print(f"✅ Uploaded: {local_path} → s3://{bucket_name}/{s3_key}")

if __name__ == "__main__":
    upload_folder(FILE_PATH, BUCKET_NAME)