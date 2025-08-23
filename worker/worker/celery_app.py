from __future__ import annotations
import os
from celery import Celery


redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery("eda_storyteller", broker=redis_url, backend=redis_url)
celery_app.autodiscover_tasks(["worker.tasks"])