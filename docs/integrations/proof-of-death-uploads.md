# Proof of death uploads to S3

When a user successfully uploads a file as proof of death, we:

1. Save the uploaded file to S3 under a holding prefix.
2. Store the returned S3 object key in the `form_data` session data.

Later, when payment is created, the S3 object key is saved to the `proof_of_death` field on the `ServiceRecordRequest` database record. Then, after payment is confirmed, the application uses that field to move the file from the holding prefix to the submitted prefix. See [Moving proof-of-death files after payment](proof-of-death-file-movement.md).

## Initial upload

The application gives each file a unique object key: a UUID with the original file extension, stored under the configured holding prefix (by default, `holding/`). It uploads the file to the configured bucket and saves the returned key in the `form_data` session data.

The holding prefix is temporary storage for uploads awaiting payment. If the user does not pay, an S3 retention policy deletes the file after its retention period (The exact period depends on the deployed S3 policy).

## Checks

- **File provided:** if no file is supplied, the upload is not attempted. Empty files are rejected.
- **Content type:** the supplied type is used unless it is missing or `application/octet-stream`. In those cases, the type is inferred from the filename, falling back to `application/octet-stream`.
- **Bucket available:** the application checks that the configured bucket exists before uploading.
- **Upload succeeds:** S3 upload errors are retried up to `MAX_UPLOAD_ATTEMPTS` times (default `3`). If all attempts fail, no key is returned and the request journey shows the upload failure page.

The file contents are read into memory once, allowing the application to check for an empty file and retry with the same file data.

## Configuration

Set `PROOF_OF_DEATH_BUCKET_NAME` to the bucket used for these files. Configure the holding and submitted prefixes with `PROOF_OF_DEATH_HOLDING_PREFIX` and `PROOF_OF_DEATH_SUBMITTED_PREFIX`. S3 clients use `AWS_DEFAULT_REGION` and Boto3's default credential chain.

## Mock S3

For local development, `S3_ENDPOINT` points the S3 client at the Docker Compose S3 Ninja service.

S3 integration tests empty the configured bucket, so run them only against the local mock S3 service.
