from __future__ import annotations

import os

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

# This script is a test/local setup helper to ensure the fixed S3 Ninja
# bucket exists before integration/Playwright tests run.


def _is_missing_bucket_error(error: ClientError) -> bool:
    # "Bucket not found" may be reported either as a numeric HTTP-style code
    # ("404") or an API-style symbolic code ("NoSuchBucket"), depending on
    # which S3-compatible provider is in use.
    code = str(error.response.get("Error", {}).get("Code", ""))
    return code in {"404", "NoSuchBucket"}


def main() -> int:
    # Keep local behavior deterministic: one fixed bucket name for upload tests.
    bucket_name = os.getenv("LOCAL_BUCKET", "proof-of-death")
    # This helper is executed in the app container via docker compose.
    # Inside the compose network, S3 Ninja is reached via service DNS `s3:9000`.
    endpoint_url = os.getenv("S3_ENDPOINT_URL", "http://s3:9000")

    # Use path-style addressing to stay compatible with S3 Ninja/local S3 emulators.
    s3 = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "AKIAIOSFODNN7EXAMPLE"),
        aws_secret_access_key=os.getenv(
            "AWS_SECRET_ACCESS_KEY", "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        ),
        region_name=os.getenv("AWS_DEFAULT_REGION", "eu-west-2"),
        config=Config(s3={"addressing_style": "path"}),
    )

    try:
        # `head_bucket` is a lightweight existence check.
        s3.head_bucket(Bucket=bucket_name)
        print(f"S3 bucket already exists: {bucket_name}")
        return 0
    except ClientError as error:
        # Only create the bucket when it is genuinely missing.
        # Any other error should fail fast so setup issues are visible.
        if not _is_missing_bucket_error(error):
            raise

    s3.create_bucket(Bucket=bucket_name, ACL="public-read-write")
    print(f"Created S3 bucket: {bucket_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
