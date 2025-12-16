import boto3
import os
import sys
from pathlib import Path

s3_client = boto3.client("s3")

BUCKET_NAME = "duploservices-ct-agskore-901907124952"


def upload_folder(local_folder_path: Path, bucket_name: str, commodity: str):
    if not local_folder_path.exists():
        raise FileNotFoundError(f"❌ Local path does not exist: {local_folder_path}")

    if not local_folder_path.is_dir():
        raise ValueError(f"❌ Provided path is not a directory: {local_folder_path}")

    # Extract last two folders (bdg_base_model/23)
    path_parts = local_folder_path.parts
    if len(path_parts) < 2:
        raise ValueError("❌ Path must contain at least two directories")

    model_root = Path(*path_parts[-2:])  # bdg_base_model/23

    for root, _, files in os.walk(local_folder_path):
        for filename in files:
            local_path = Path(root) / filename

            relative_path = local_path.relative_to(local_folder_path)

            s3_key = (
                f"model_store/"
                f"{commodity.lower()}/"
                f"{model_root.as_posix()}/"
                f"{relative_path.as_posix()}"
            )

            s3_client.upload_file(str(local_path), bucket_name, s3_key)
            print(f"✅ Uploaded: {local_path} → s3://{bucket_name}/{s3_key}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("❌ Usage: python upload.py <local_folder_path> <commodity>")
        sys.exit(1)

    local_path = Path(sys.argv[1]).resolve()
    commodity_selected = sys.argv[2]

    upload_folder(local_path, BUCKET_NAME, commodity_selected)
