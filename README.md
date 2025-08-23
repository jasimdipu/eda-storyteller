# 📊 EDA Storyteller

EDA Storyteller is a microservices-based application for **automated exploratory data analysis (EDA)**. It enables dataset uploads via pre‑signed S3/MinIO URLs, triggers asynchronous profiling jobs through an orchestrated pipeline (**Gateway → Orchestrator → Celery → Worker**), and writes analysis artifacts like `profile.json` back to object storage.

Designed for **scalability**, **clear service boundaries**, and **extensibility** (plug‑in analyzers, insights, and apply flows).

---

## 🚀 Features

* Dataset upload using **pre‑signed URLs** (S3‑compatible; works with MinIO)
* Distributed pipeline: **Gateway → Orchestrator → Celery → Worker**
* Workers generate `profile.json` (and more) into object storage
* **Shared package (`eda-shared`)** for Pydantic schemas, S3 helpers, and common logic
* Extensible **Analyzer** + **Insights** + **Apply** flows

---

## 🏗️ Architecture Overview

```text
+---------+       +--------------+       +----------------+       +-----------+
| Gateway | ----> | Orchestrator | ----> | Celery Broker  | ----> | Worker(s) |
+---------+       +--------------+       +----------------+       +-----------+
     |                      |                      |                      |
     |                      |                      |                      |
     v                      v                      v                      v
  [Presigned]           [Enqueue]             [Distribute]           [Analyze]
  Dataset Upload   →   Analysis Job   →   Celery Task Queue   →   Generate profile.json

Object Store (MinIO/S3): datasets in, profiles/insights out
```

---

## 📦 Repository Structure

```text
eda-storyteller/
├── gateway/         # FastAPI service for presign & API endpoints
├── orchestrator/    # Workflow API, enqueues Celery tasks
├── worker/          # Celery workers run analyzers, write artifacts
├── shared/          # Shared schemas & utilities (eda-shared)
│   ├── pyproject.toml
│   └── eda_shared/
│       ├── __init__.py
│       ├── schemas.py
│       ├── s3.py
│       └── ...
└── README.md        # You are here
```

---

## ⚙️ Shared Package: `eda-shared`

Common contracts and helpers for all services.

**`shared/pyproject.toml`:**

```toml
[project]
name = "eda-shared"
version = "0.1.0"
description = "Shared schemas and utilities for EDA Storyteller"
requires-python = ">=3.11"
dependencies = [
  "pydantic>=2",
  "boto3",
]

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
```

**Install locally (editable):**

```bash
cd shared
pip install -e .
```

**Use in services:**

```python
from eda_shared.schemas import DatasetUploadRequest, AnalysisJob
from eda_shared.s3 import presign_put_url
```

---

## 🔧 Getting Started (Local)

### Prerequisites

* Python **3.11+**
* Docker & Docker Compose (recommended for MinIO, Redis)
* Make (optional)

### Run MinIO (local S3)

```bash
docker run -d -p 9000:9000 -p 9090:9090 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  quay.io/minio/minio server /data --console-address ":9090"
```

Access console at: `http://localhost:9090` (default creds above; **change in prod**).

### Environment Variables (example)

Create a `.env` per service (or use your secrets manager in prod):

```
S3_ENDPOINT_URL=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
AWS_REGION=us-east-1

# Celery / Broker
REDIS_URL=redis://localhost:6379/0
```

---

## ▶️ Running Services

### Gateway (FastAPI)

```bash
cd gateway
uvicorn main:app --reload --port 8000
```

### Orchestrator

* Exposes endpoints to enqueue analysis jobs to Celery.

### Worker (Celery)

```bash
cd worker
celery -A tasks worker --loglevel=info
```

> In development, run Redis and MinIO via Docker. In production, use managed equivalents (Amazon ElastiCache for Redis, Amazon S3 or self‑managed MinIO, etc.).

---

## 📂 Example Workflow

1. **Request presigned upload URL**

```http
POST /datasets/presign
{
  "org_id": "org123",
  "dataset_name": "data.csv",
  "content_type": "text/csv"
}
```

Response → `{ upload_url, object_key }`

2. **Upload dataset to MinIO**

```bash
curl -X PUT -T data.csv "https://<minio-host>/eda-datasets/org123/data.csv?signature=..."
```

3. **Trigger analysis job**

```http
POST /datasets/analyze
{
  "org_id": "org123",
  "dataset_key": "s3://eda-datasets/org123/data.csv",
  "output_bucket": "eda-profiles",
  "output_key": "org123/data_profile.json"
}
```

4. **Worker generates `profile.json`** and uploads to `s3://eda-profiles/org123/data_profile.json`.

---

## 🧩 Development Notes

* Use `pip install -e ./shared` during local dev so services can import `eda_shared` without rebuilding wheels.
* Keep **Pydantic models** in `schemas.py` as your API contract between services.
* Put **S3/MinIO helpers** in `s3.py` (create clients, presign URLs, simple put/get wrappers).
* Add new analyzers under `worker/analyzers/` with a common interface (e.g., `run(df) -> dict`).

---

## 🛡️ Security & Ops (baseline)

* Rotate MinIO/S3 credentials; never commit secrets.
* Enforce content‑type and size limits on presigned uploads.
* Validate inputs via Pydantic models at the **Gateway** and **Orchestrator**.
* Add request tracing (X‑Request‑ID) across services.
* Prefer managed S3 in production; if using MinIO, deploy with TLS.

---

## 🗺️ Roadmap

* [ ] Expand analyzer plugins (nulls, distributions, correlations, drift)
* [ ] Visualization outputs (charts, HTML dashboards)
* [ ] Insights & Apply flows (LLM‑assisted narratives)
* [ ] CI/CD (GitHub Actions) + IaC (Terraform) + EKS deployment
* [ ] Multi‑tenant isolation and org‑level quotas

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-change`
3. Commit: `git commit -m "feat: add my change"`
4. Push: `git push origin feature/my-change`
5. Open a Pull Request

---

## 📜 License

MIT License – use and adapt freely.
