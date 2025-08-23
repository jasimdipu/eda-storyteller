from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from .celery_client import celery_client

app = FastAPI(title="EDA Orchestrator", version="0.1.0")


class EnqueueJob(BaseModel):
    run_id: str
    s3_key: str
    mode: str = "quick"


@app.post("/enqueue")
def enqueue(job: EnqueueJob):
    task = celery_client.send_task("worker.tasks.run_profile", kwargs=job.model_dump())
    return {"task_id": task.id}


@app.get("/health")
def health():
    return {"status": "ok"}
