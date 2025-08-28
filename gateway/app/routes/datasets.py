from __future__ import annotations
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from shared.shared.schemas import DatasetProfile


router = APIRouter(tags=["datasets"])


class RunCreate(BaseModel):
    dataset_name: str
    s3_key: str # path in S3 (MinIO) under S3_BUCKET_RAW
    mode: str = "quick" # or full


@router.post("/datasets/{dataset_id}/runs")
def create_run(dataset_id: str, body: RunCreate):
    # For now, return a run_id and echo; orchestrator wiring to be added
    run_id = str(uuid.uuid4())
    return {"run_id": run_id, "status": "queued", "dataset_id": dataset_id, "input": body.model_dump()}


@router.get("/runs/{run_id}/profile", response_model=DatasetProfile)
def get_profile(run_id: str):
    # Stub: replace with S3 read for eda-profiles/<org>/<dataset>/<run>/profile.json
    raise HTTPException(status_code=404, detail="Profile not ready yet")