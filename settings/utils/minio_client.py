from settings.settings import (
    MINIO_STORAGE_ACCESS_KEY,
    MINIO_STORAGE_SECRET_KEY,
    MINIO_STORAGE_ENDPOINT,
    MINIO_STORAGE_USE_HTTPS,
    MINIO_STORAGE_MEDIA_BUCKET_NAME,
)
from minio import Minio


def minio_client():
    """Return instance of minio client"""

    client = Minio(
        endpoint=MINIO_STORAGE_ENDPOINT,
        access_key=MINIO_STORAGE_ACCESS_KEY,
        secret_key=MINIO_STORAGE_SECRET_KEY,
        secure=MINIO_STORAGE_USE_HTTPS,
    )

    found = client.bucket_exists(MINIO_STORAGE_MEDIA_BUCKET_NAME)
    if not found:
        client.make_bucket(MINIO_STORAGE_MEDIA_BUCKET_NAME)

    return client
