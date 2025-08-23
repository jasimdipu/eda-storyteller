from __future__ import annotations
import io, json
import polars as pl
from celery import shared_task
from shared.storage.s3_client import s3_client
from shared.config import settings
from shared.schemas.profile import DatasetProfile, DatasetSection, ColumnProfile, QualitySection, TimeseriesSection


@shared_task(name="worker.tasks.run_profile")
def run_profile(run_id: str, s3_key: str, mode: str = "quick"):
    s3 = s3_client()
    # Read CSV from MinIO S3
    obj = s3.get_object(Bucket=settings.S3_BUCKET_RAW, Key=s3_key)
    buf = io.BytesIO(obj["Body"].read())
    df = pl.read_csv(buf)

    # Sampling for quick mode
    if mode == "quick" and df.height > 100_000:
        df = df.sample(100_000, seed=42)

    # Minimal profiling
    cols = {}
    for c in df.columns:
        s = df[c]
        dtype = str(s.dtype)
        missing = float(s.null_count() / df.height) if s.null_count() else 0.0
        unique = float(s.n_unique() / df.height)
        skew = None
        outlier_rate = None
        card = None
        if s.dtype.is_numeric():
            desc = s.describe()
        # IQR outlier rate
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        if (iqr is not None) and (iqr > 0):
            mask = (s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)
            outlier_rate = float(mask.mean())
        else:
            card = int(s.n_unique())
        cols[c] = ColumnProfile(dtype=dtype, missing_rate=missing, unique_rate=unique, skew=skew,
                            outlier_rate=outlier_rate, cardinality=card).model_dump()

    ts = TimeseriesSection(detected=False)
    if any("date" in c.lower() for c in df.columns):
        ts.detected = True
    ts.index = [c for c in df.columns if "date" in c.lower()][0]

    profile = DatasetProfile(
        dataset=DatasetSection(rows=int(df.height), cols=int(df.width)),
        columns=cols,
        quality=QualitySection(duplicates_rate=float(df.is_duplicated().mean())),
        timeseries=ts,
        relationships=None,
    ).model_dump()

    # Write profile.json to S3 (eda-profiles/<run_id>/profile.json)
    key = f"{run_id}/profile.json"
    s3.put_object(Bucket=settings.S3_BUCKET_PROFILES, Key=key, Body=json.dumps(profile).encode("utf-8"))
    return {"profile_key": key}
