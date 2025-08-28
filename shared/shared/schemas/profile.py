from __future__ import annotations

from email.policy import default
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

SCHEMA_VERSION = "0.1.1"

class ColumnProfile(BaseModel):
    dtype: str
    missing_rate: float | None = None
    unique_rate: float | None = None
    skew: float | None = None
    outlier_rate: float | None = None
    cardinality: int | None = None


class DatasetSection(BaseModel):
    rows: int
    cols: int
    memory_bites: int | None = None


class TimeseriesSection(BaseModel):
    detected: bool = False
    index: Optional[str] = None
    freq: Optional[str] = None
    seasonality: List[str] = []


class QualitySection(BaseModel):
    duplicates_rate: float | None = None


class DatasetProfile(BaseModel):
    schema_version: str = Field(default=SCHEMA_VERSION)
    dataset: DatasetSection
    columns: Dict[str, ColumnProfile]
    relationships: Dict[str, Any] | None = None
    timeseries: TimeseriesSection | None = None
    quality: QualitySection | None = None