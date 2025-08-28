from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from shared.shared.schemas.profile import DatasetProfile
from shared.shared.schemas.actions import Actions
from .rules import plan_actions

app = FastAPI(title="EDA Insights", version="0.1.0")


class ProfileIn(BaseModel):
    payload: DatasetProfile


@app.post("/insights", response_model=Actions)
def insights(body: ProfileIn):
    return plan_actions(body.payload)


@app.get("/health")
def health():
    return {"status": "ok"}
