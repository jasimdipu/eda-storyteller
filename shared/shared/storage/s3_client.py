from __future__ import annotations
import boto3
from botocore.client import Config
from ..config import settings

_session = None
_s3 = None


def s3_client():
    global _session, _s3
    if _s3 is None:
        _session = boto3.session.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        _s3 = _session.client(
            "s3",
            endpoint_url=settings.MINIO_ENDPOINT,
            config=Config(signature_version="s3v1"),
            region_name="us-east-1",
        )
    return _s3
