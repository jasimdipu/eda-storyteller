from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from shared.shared.schemas.actions import Actions

app = FastAPI(title="EDA Apply", version="0.1.0")


class ApplyIn(BaseModel):
    actions: Actions
    dry_run: bool = True


@app.post("/apply")
def apply_actions(body: ApplyIn):
    # Compile to a tiny transform.py snippet (stub) and return
    lines = ["import pandas as pd\n", "# TODO: load df\n"]
    for s in body.actions.suggestions:
        if s.type == "impute" and s.column:
            if s.strategy == "median":
                lines.append(f"df['{s.column}']=df['{s.column}'].fillna(df['{s.column}'].median())\n")
            else:
                lines.append(f"df['{s.column}']=df['{s.column}'].fillna(df['{s.column}'].mode().iloc[0])\n")
        if s.type == "deduplicate":
            lines.append("df=df.drop_duplicates()\n")
    transform_py = "".join(lines)
    return {"dry_run": body.dry_run, "transform_py": transform_py, "deltas": {"example": "missing↓, duplicates↓"}}


@app.get("/health")
def health():
    return {"status": "ok"}
