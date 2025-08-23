from __future__ import annotations
from fastapi import FastAPI
from .routes.health import router as health_router
from .routes.datasets import router as datasets_router

app = FastAPI(title="EDA Storyteller Gateway", version="0.1.0")
app.include_router(health_router)
app.include_router(datasets_router, prefix="/v1")
