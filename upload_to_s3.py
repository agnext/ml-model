import boto3
import os
from pathlib import Path

# S3 client (uses EC2/Instance IAM role automatically)
s3_client = boto3.client("s3")

# Local folder root
FILE_PATH = r"D:\s3Models"    # Upload this entire folder
BUCKET_NAME = "duploservices-ct-agskore-901907124952"


def upload_folder(local_folder_path, bucket_name):
    """
    Uploads a local folder to S3 recursively.

    Final S3 structure:
        model_store/<relative_path>
    """
    base_path = Path(local_folder_path)

    for root, _, files in os.walk(local_folder_path):
        for filename in files:

            local_path = Path(root) / filename
            relative_path = local_path.relative_to(base_path)

            # FIXED: Added missing "/"
            s3_key = f"model_store/{relative_path.as_posix()}"

            s3_client.upload_file(str(local_path), bucket_name, s3_key)

            print(f"✅ Uploaded: {local_path} → s3://{bucket_name}/{s3_key}")


if __name__ == "__main__":
    upload_folder(FILE_PATH, BUCKET_NAME)
